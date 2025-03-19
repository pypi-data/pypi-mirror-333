import contextlib
import dataclasses
import os
import types
import typing
from http import HTTPStatus

import annotated_types
import httpx
import httpx_sse
import pydantic
import typing_extensions

from any_llm_client.core import (
    LLMClient,
    LLMConfig,
    LLMConfigValue,
    LLMError,
    Message,
    MessageRole,
    OutOfTokensOrSymbolsError,
    UserMessage,
)
from any_llm_client.http import get_http_client_from_kwargs, make_http_request, make_streaming_http_request
from any_llm_client.retry import RequestRetryConfig


OPENAI_AUTH_TOKEN_ENV_NAME: typing.Final = "ANY_LLM_CLIENT_OPENAI_AUTH_TOKEN"  # noqa: S105


class OpenAIConfig(LLMConfig):
    if typing.TYPE_CHECKING:
        url: str
    else:
        url: pydantic.HttpUrl
    auth_token: str | None = pydantic.Field(default_factory=lambda: os.environ.get(OPENAI_AUTH_TOKEN_ENV_NAME))
    model_name: str
    request_extra: dict[str, typing.Any] = pydantic.Field(default_factory=dict)
    force_user_assistant_message_alternation: bool = False
    "Gemma 2 doesn't support {role: system, text: ...} message, and requires alternated messages"
    api_type: typing.Literal["openai"] = "openai"


class ChatCompletionsMessage(pydantic.BaseModel):
    role: MessageRole
    content: str


class ChatCompletionsRequest(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="allow")
    stream: bool
    model: str
    messages: list[ChatCompletionsMessage]
    temperature: float


class OneStreamingChoiceDelta(pydantic.BaseModel):
    role: typing.Literal[MessageRole.assistant] | None = None
    content: str | None = None


class OneStreamingChoice(pydantic.BaseModel):
    delta: OneStreamingChoiceDelta


class ChatCompletionsStreamingEvent(pydantic.BaseModel):
    choices: typing.Annotated[list[OneStreamingChoice], annotated_types.MinLen(1)]


class OneNotStreamingChoice(pydantic.BaseModel):
    message: ChatCompletionsMessage


class ChatCompletionsNotStreamingResponse(pydantic.BaseModel):
    choices: typing.Annotated[list[OneNotStreamingChoice], annotated_types.MinLen(1)]


def _make_user_assistant_alternate_messages(
    messages: typing.Iterable[ChatCompletionsMessage],
) -> typing.Iterable[ChatCompletionsMessage]:
    current_message_role = MessageRole.user
    current_message_content_chunks = []

    for one_message in messages:
        if not one_message.content.strip():
            continue

        if (
            one_message.role in {MessageRole.system, MessageRole.user} and current_message_role == MessageRole.user
        ) or one_message.role == current_message_role == MessageRole.assistant:
            current_message_content_chunks.append(one_message.content)
        else:
            if current_message_content_chunks:
                yield ChatCompletionsMessage(
                    role=current_message_role, content="\n\n".join(current_message_content_chunks)
                )
            current_message_content_chunks = [one_message.content]
            current_message_role = one_message.role

    if current_message_content_chunks:
        yield ChatCompletionsMessage(role=current_message_role, content="\n\n".join(current_message_content_chunks))


def _handle_status_error(*, status_code: int, content: bytes) -> typing.NoReturn:
    if status_code == HTTPStatus.BAD_REQUEST and b"Please reduce the length of the messages" in content:  # vLLM
        raise OutOfTokensOrSymbolsError(response_content=content)
    raise LLMError(response_content=content)


@dataclasses.dataclass(slots=True, init=False)
class OpenAIClient(LLMClient):
    config: OpenAIConfig
    httpx_client: httpx.AsyncClient
    request_retry: RequestRetryConfig

    def __init__(
        self,
        config: OpenAIConfig,
        *,
        request_retry: RequestRetryConfig | None = None,
        **httpx_kwargs: typing.Any,  # noqa: ANN401
    ) -> None:
        self.config = config
        self.request_retry = request_retry or RequestRetryConfig()
        self.httpx_client = get_http_client_from_kwargs(httpx_kwargs)

    def _build_request(self, payload: dict[str, typing.Any]) -> httpx.Request:
        return self.httpx_client.build_request(
            method="POST",
            url=str(self.config.url),
            json=payload,
            headers={"Authorization": f"Bearer {self.config.auth_token}"} if self.config.auth_token else None,
        )

    def _prepare_messages(self, messages: str | list[Message]) -> list[ChatCompletionsMessage]:
        messages = [UserMessage(messages)] if isinstance(messages, str) else messages
        initial_messages: typing.Final = (
            ChatCompletionsMessage(role=one_message.role, content=one_message.text) for one_message in messages
        )
        return (
            list(_make_user_assistant_alternate_messages(initial_messages))
            if self.config.force_user_assistant_message_alternation
            else list(initial_messages)
        )

    def _prepare_payload(
        self, *, messages: str | list[Message], temperature: float, stream: bool, extra: dict[str, typing.Any] | None
    ) -> dict[str, typing.Any]:
        return ChatCompletionsRequest(
            stream=stream,
            model=self.config.model_name,
            messages=self._prepare_messages(messages),
            temperature=self.config._resolve_request_temperature(temperature),  # noqa: SLF001
            **self.config.request_extra | (extra or {}),
        ).model_dump(mode="json")

    async def request_llm_message(
        self,
        messages: str | list[Message],
        *,
        temperature: float = LLMConfigValue(attr="temperature"),
        extra: dict[str, typing.Any] | None = None,
    ) -> str:
        payload: typing.Final = self._prepare_payload(
            messages=messages, temperature=temperature, stream=False, extra=extra
        )
        try:
            response: typing.Final = await make_http_request(
                httpx_client=self.httpx_client,
                request_retry=self.request_retry,
                build_request=lambda: self._build_request(payload),
            )
        except httpx.HTTPStatusError as exception:
            _handle_status_error(status_code=exception.response.status_code, content=exception.response.content)
        try:
            return ChatCompletionsNotStreamingResponse.model_validate_json(response.content).choices[0].message.content
        finally:
            await response.aclose()

    async def _iter_response_chunks(self, response: httpx.Response) -> typing.AsyncIterable[str]:
        async for event in httpx_sse.EventSource(response).aiter_sse():
            if event.data == "[DONE]":
                break
            validated_response = ChatCompletionsStreamingEvent.model_validate_json(event.data)
            if not (one_chunk := validated_response.choices[0].delta.content):
                continue
            yield one_chunk

    @contextlib.asynccontextmanager
    async def stream_llm_message_chunks(
        self,
        messages: str | list[Message],
        *,
        temperature: float = LLMConfigValue(attr="temperature"),
        extra: dict[str, typing.Any] | None = None,
    ) -> typing.AsyncIterator[typing.AsyncIterable[str]]:
        payload: typing.Final = self._prepare_payload(
            messages=messages, temperature=temperature, stream=True, extra=extra
        )
        try:
            async with make_streaming_http_request(
                httpx_client=self.httpx_client,
                request_retry=self.request_retry,
                build_request=lambda: self._build_request(payload),
            ) as response:
                yield self._iter_response_chunks(response)
        except httpx.HTTPStatusError as exception:
            content: typing.Final = await exception.response.aread()
            await exception.response.aclose()
            _handle_status_error(status_code=exception.response.status_code, content=content)

    async def __aenter__(self) -> typing_extensions.Self:
        await self.httpx_client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        await self.httpx_client.__aexit__(exc_type=exc_type, exc_value=exc_value, traceback=traceback)
