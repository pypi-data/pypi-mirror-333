from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SentimentAnalysisResponseUsage")


@_attrs_define
class SentimentAnalysisResponseUsage:
    """
    Attributes:
        total_tokens (Union[Unset, int]): The count of total tokens consumed by the request. Example: 878.0.
        completion_tokens (Union[Unset, int]): The number of tokens consumed to complete the API request. Example:
            301.0.
        prompt_tokens (Union[Unset, int]): Indicates the number of tokens used in the prompt. Example: 577.0.
    """

    total_tokens: Union[Unset, int] = UNSET
    completion_tokens: Union[Unset, int] = UNSET
    prompt_tokens: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_tokens = self.total_tokens

        completion_tokens = self.completion_tokens

        prompt_tokens = self.prompt_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if completion_tokens is not UNSET:
            field_dict["completion_tokens"] = completion_tokens
        if prompt_tokens is not UNSET:
            field_dict["prompt_tokens"] = prompt_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        total_tokens = d.pop("total_tokens", UNSET)

        completion_tokens = d.pop("completion_tokens", UNSET)

        prompt_tokens = d.pop("prompt_tokens", UNSET)

        sentiment_analysis_response_usage = cls(
            total_tokens=total_tokens,
            completion_tokens=completion_tokens,
            prompt_tokens=prompt_tokens,
        )

        sentiment_analysis_response_usage.additional_properties = d
        return sentiment_analysis_response_usage

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
