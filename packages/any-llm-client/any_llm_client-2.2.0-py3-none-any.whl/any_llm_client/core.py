import contextlib
import dataclasses
import enum
import types
import typing

import pydantic
import typing_extensions


class MessageRole(str, enum.Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


@pydantic.dataclasses.dataclass(kw_only=True)
class Message:
    role: MessageRole
    text: str


if typing.TYPE_CHECKING:

    @pydantic.dataclasses.dataclass
    class SystemMessage(Message):
        role: typing.Literal[MessageRole.system] = pydantic.Field(MessageRole.system, init=False)
        text: str

    @pydantic.dataclasses.dataclass
    class UserMessage(Message):
        role: typing.Literal[MessageRole.user] = pydantic.Field(MessageRole.user, init=False)
        text: str

    @pydantic.dataclasses.dataclass
    class AssistantMessage(Message):
        role: typing.Literal[MessageRole.assistant] = pydantic.Field(MessageRole.assistant, init=False)
        text: str
else:

    def SystemMessage(text: str) -> Message:  # noqa: N802
        return Message(role=MessageRole.system, text=text)

    def UserMessage(text: str) -> Message:  # noqa: N802
        return Message(role=MessageRole.user, text=text)

    def AssistantMessage(text: str) -> Message:  # noqa: N802
        return Message(role=MessageRole.assistant, text=text)


class LLMConfig(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(protected_namespaces=())
    api_type: str
    temperature: float = 0.2
    request_extra: dict[str, typing.Any] = pydantic.Field(default_factory=dict)

    def _resolve_request_temperature(self, temperature_arg_value: float) -> float:
        return (
            self.temperature
            if isinstance(temperature_arg_value, LLMConfigValue)  # type: ignore[arg-type]
            else temperature_arg_value
        )


if typing.TYPE_CHECKING:

    def LLMConfigValue(*, attr: str) -> typing.Any:  # noqa: ANN401, N802
        """Defaults to value from LLMConfig."""
else:

    @dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
    class LLMConfigValue:
        """Defaults to value from LLMConfig."""

        attr: str


@dataclasses.dataclass(slots=True, init=False)
class LLMClient(typing.Protocol):
    async def request_llm_message(
        self,
        messages: str | list[Message],
        *,
        temperature: float = LLMConfigValue(attr="temperature"),
        extra: dict[str, typing.Any] | None = None,
    ) -> str: ...  # raises LLMError

    @contextlib.asynccontextmanager
    def stream_llm_message_chunks(
        self,
        messages: str | list[Message],
        *,
        temperature: float = LLMConfigValue(attr="temperature"),
        extra: dict[str, typing.Any] | None = None,
    ) -> typing.AsyncIterator[typing.AsyncIterable[str]]: ...  # raises LLMError

    async def __aenter__(self) -> typing_extensions.Self: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...


@dataclasses.dataclass
class LLMError(Exception):
    response_content: bytes

    def __str__(self) -> str:
        return self.__repr__().removeprefix(self.__class__.__name__)


@dataclasses.dataclass
class OutOfTokensOrSymbolsError(LLMError): ...
