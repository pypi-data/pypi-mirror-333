import typing

import faker
import httpx
import pydantic
import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

import any_llm_client
from any_llm_client.clients.yandexgpt import YandexGPTAlternative, YandexGPTResponse, YandexGPTResult
from tests.conftest import LLMFuncRequest, LLMFuncRequestFactory, consume_llm_message_chunks


class YandexGPTConfigFactory(ModelFactory[any_llm_client.YandexGPTConfig]): ...


class TestYandexGPTRequestLLMResponse:
    @pytest.mark.parametrize("func_request", LLMFuncRequestFactory.coverage())
    async def test_ok(self, faker: faker.Faker, func_request: LLMFuncRequest) -> None:
        expected_result: typing.Final = faker.pystr()
        response: typing.Final = httpx.Response(
            200,
            json=YandexGPTResponse(
                result=YandexGPTResult(
                    alternatives=[YandexGPTAlternative(message=any_llm_client.AssistantMessage(expected_result))]
                )
            ).model_dump(mode="json"),
        )

        result: typing.Final = await any_llm_client.get_client(
            YandexGPTConfigFactory.build(), transport=httpx.MockTransport(lambda _: response)
        ).request_llm_message(**func_request)

        assert result == expected_result

    async def test_fails_without_alternatives(self) -> None:
        response: typing.Final = httpx.Response(
            200, json=YandexGPTResponse(result=YandexGPTResult.model_construct(alternatives=[])).model_dump(mode="json")
        )
        client: typing.Final = any_llm_client.get_client(
            YandexGPTConfigFactory.build(), transport=httpx.MockTransport(lambda _: response)
        )

        with pytest.raises(pydantic.ValidationError):
            await client.request_llm_message(**LLMFuncRequestFactory.build())


class TestYandexGPTRequestLLMMessageChunks:
    @pytest.mark.parametrize("func_request", LLMFuncRequestFactory.coverage())
    async def test_ok(self, faker: faker.Faker, func_request: LLMFuncRequest) -> None:
        expected_result: typing.Final = faker.pylist(value_types=[str])
        config: typing.Final = YandexGPTConfigFactory.build()
        response_content: typing.Final = (
            "\n".join(
                YandexGPTResponse(
                    result=YandexGPTResult(
                        alternatives=[
                            YandexGPTAlternative(
                                message=any_llm_client.AssistantMessage("".join(expected_result[: one_index + 1]))
                            )
                        ]
                    )
                ).model_dump_json()
                for one_index in range(len(expected_result))
            )
            + "\n"
        )
        response: typing.Final = httpx.Response(200, content=response_content)

        result: typing.Final = await consume_llm_message_chunks(
            any_llm_client.get_client(
                config, transport=httpx.MockTransport(lambda _: response)
            ).stream_llm_message_chunks(**func_request)
        )

        assert result == expected_result

    async def test_fails_without_alternatives(self) -> None:
        response_content: typing.Final = (
            YandexGPTResponse(result=YandexGPTResult.model_construct(alternatives=[])).model_dump_json() + "\n"
        )
        response: typing.Final = httpx.Response(200, content=response_content)

        client: typing.Final = any_llm_client.get_client(
            YandexGPTConfigFactory.build(), transport=httpx.MockTransport(lambda _: response)
        )

        with pytest.raises(pydantic.ValidationError):
            await consume_llm_message_chunks(client.stream_llm_message_chunks(**LLMFuncRequestFactory.build()))


class TestYandexGPTLLMErrors:
    @pytest.mark.parametrize("stream", [True, False])
    @pytest.mark.parametrize("status_code", [400, 500])
    async def test_fails_with_unknown_error(self, stream: bool, status_code: int) -> None:
        client: typing.Final = any_llm_client.get_client(
            YandexGPTConfigFactory.build(), transport=httpx.MockTransport(lambda _: httpx.Response(status_code))
        )

        coroutine: typing.Final = (
            consume_llm_message_chunks(client.stream_llm_message_chunks(**LLMFuncRequestFactory.build()))
            if stream
            else client.request_llm_message(**LLMFuncRequestFactory.build())
        )

        with pytest.raises(any_llm_client.LLMError) as exc_info:
            await coroutine
        assert type(exc_info.value) is any_llm_client.LLMError

    @pytest.mark.parametrize("stream", [True, False])
    @pytest.mark.parametrize(
        "response_content",
        [
            b"...folder_id=1111: number of input tokens must be no more than 8192, got 28498...",
            b"...folder_id=1111: text length is 349354, which is outside the range (0, 100000]...",
        ],
    )
    async def test_fails_with_out_of_tokens_error(self, stream: bool, response_content: bytes | None) -> None:
        response: typing.Final = httpx.Response(400, content=response_content)
        client: typing.Final = any_llm_client.get_client(
            YandexGPTConfigFactory.build(), transport=httpx.MockTransport(lambda _: response)
        )

        coroutine: typing.Final = (
            consume_llm_message_chunks(client.stream_llm_message_chunks(**LLMFuncRequestFactory.build()))
            if stream
            else client.request_llm_message(**LLMFuncRequestFactory.build())
        )

        with pytest.raises(any_llm_client.OutOfTokensOrSymbolsError):
            await coroutine
