from collections import defaultdict
from copy import deepcopy
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    DefaultDict,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Protocol,
    Tuple,
    Type,
)

from opentelemetry.util.types import AttributeValue

from fi.integrations.otel.frameworks.mistralai._utils import (
    _as_output_attributes,
    _to_dict,
    _ValueAndType,
)
from fi.integrations.otel.instrumentation import safe_json_dumps
from fi.integrations.otel.fi_types import FiMimeTypeValues, SpanAttributes

if TYPE_CHECKING:
    from mistralai.models import CompletionChunk, CompletionEvent

__all__ = ("_ChatCompletionAccumulator",)


class _CanGetAttributesFromResponse(Protocol):
    def get_attributes_from_response(
        self,
        response: Any,
        request_parameters: Mapping[str, Any],
    ) -> Iterator[Tuple[str, AttributeValue]]: ...


class _ChatCompletionAccumulator:
    __slots__ = (
        "_is_null",
        "_values",
        "_cached_result",
        "_request_parameters",
        "_response_attributes_extractor",
        "_chat_completion_type",
        "_content",
        "_raw_data",
    )

    def __init__(
        self,
        request_parameters: Mapping[str, Any],
        chat_completion_type: Type["CompletionEvent"],
        response_attributes_extractor: Optional[_CanGetAttributesFromResponse] = None,
    ) -> None:
        self._chat_completion_type = chat_completion_type
        self._request_parameters = request_parameters
        self._response_attributes_extractor = response_attributes_extractor
        self._is_null = True
        self._cached_result: Optional[Dict[str, Any]] = None
        self._content: List[str] = []
        self._raw_data: List[Dict[str, Any]] = []
        self._values = _ValuesAccumulator(
            data=_ValuesAccumulator(
                choices=_IndexedAccumulator(
                    lambda: _ValuesAccumulator(
                        message=_ValuesAccumulator(
                            content=_StringAccumulator(),
                            tool_calls=_IndexedAccumulator(
                                lambda: _ValuesAccumulator(
                                    function=_ValuesAccumulator(
                                        arguments=_StringAccumulator()
                                    ),
                                )
                            ),
                        ),
                    ),
                ),
            ),
        )

    def process_chunk(self, chunk: Any) -> None:
        raw_chunk = _to_dict(chunk)
        self._raw_data.append(raw_chunk)

        if "choices" in raw_chunk.get("data", {}):
            choices = raw_chunk["data"]["choices"]
            if choices and isinstance(choices, list):
                delta = choices[0].get("delta", {})
                content = delta.get("content")
                if content is not None:
                    self._content.append(content)

    def _result(self) -> Optional[Dict[str, Any]]:
        if self._is_null:
            return None
        if not self._cached_result:
            self._cached_result = dict(self._values)
        return self._cached_result

    def get_attributes(self) -> Iterator[Tuple[str, AttributeValue]]:
        # Combine the accumulated content and raw data
        output_value = "".join(self._content)
        raw_output = safe_json_dumps(self._raw_data)
        yield SpanAttributes.OUTPUT_VALUE, output_value
        yield SpanAttributes.RAW_OUTPUT, raw_output
        yield SpanAttributes.OUTPUT_MIME_TYPE, FiMimeTypeValues.JSON.value

    def get_extra_attributes(self) -> Iterator[Tuple[str, AttributeValue]]:
        if not (result := self._result()):
            return
        if self._response_attributes_extractor:
            yield from self._response_attributes_extractor.get_attributes_from_response(
                self._chat_completion_type.construct(**result),
                self._request_parameters,
            )


class _ValuesAccumulator:
    __slots__ = ("_values",)

    def __init__(self, **values: Any) -> None:
        self._values: Dict[str, Any] = values

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for key, value in self._values.items():
            if value is None:
                continue
            if isinstance(value, _ValuesAccumulator):
                if dict_value := dict(value):
                    yield key, dict_value
            elif isinstance(value, _IndexedAccumulator):
                if list_value := list(value):
                    yield key, list_value
            elif isinstance(value, _StringAccumulator):
                if str_value := str(value):
                    yield key, str_value
            else:
                yield key, value

    def __iadd__(self, values: Optional[Mapping[str, Any]]) -> "_ValuesAccumulator":
        if not values:
            return self
        for key in self._values.keys():
            if (value := values.get(key)) is None:
                continue
            self_value = self._values[key]
            if isinstance(self_value, _ValuesAccumulator):
                if isinstance(value, Mapping):
                    self_value += value
            elif isinstance(self_value, _StringAccumulator):
                if isinstance(value, str):
                    self_value += value
            elif isinstance(self_value, _IndexedAccumulator):
                if isinstance(value, Iterable):
                    for index, v in enumerate(value):
                        if isinstance(v, Dict) and "index" not in v:
                            v["index"] = index
                        self_value += v
                else:
                    self_value += value
            elif isinstance(self_value, List) and isinstance(value, Iterable):
                self_value.extend(value)
            else:
                self._values[key] = value  # replacement
        for key in values.keys():
            if key in self._values or (value := values[key]) is None:
                continue
            value = deepcopy(value)
            if isinstance(value, Mapping):
                value = _ValuesAccumulator(**value)
            self._values[key] = value  # new entry
        return self


class _StringAccumulator:
    __slots__ = ("_fragments",)

    def __init__(self) -> None:
        self._fragments: List[str] = []

    def __str__(self) -> str:
        return "".join(self._fragments)

    def __iadd__(self, value: Optional[str]) -> "_StringAccumulator":
        if not value:
            return self
        self._fragments.append(value)
        return self


class _IndexedAccumulator:
    __slots__ = ("_indexed",)

    def __init__(self, factory: Callable[[], _ValuesAccumulator]) -> None:
        self._indexed: DefaultDict[int, _ValuesAccumulator] = defaultdict(factory)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        for _, values in sorted(self._indexed.items()):
            yield dict(values)

    def __iadd__(self, values: Optional[Mapping[str, Any]]) -> "_IndexedAccumulator":
        if (
            not values
            or not hasattr(values, "get")
            or (index := values.get("index")) is None
        ):
            return self
        self._indexed[index] += values
        return self
