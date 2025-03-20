from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ContentGenerationResponseUsage")


@_attrs_define
class ContentGenerationResponseUsage:
    """
    Attributes:
        total_tokens (Union[Unset, int]): The Usage total tokens Example: 84.0.
        prompt_tokens (Union[Unset, int]): The Usage prompt tokens Example: 34.0.
        completion_tokens (Union[Unset, int]): The Usage completion tokens Example: 50.0.
    """

    total_tokens: Union[Unset, int] = UNSET
    prompt_tokens: Union[Unset, int] = UNSET
    completion_tokens: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_tokens = self.total_tokens

        prompt_tokens = self.prompt_tokens

        completion_tokens = self.completion_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if prompt_tokens is not UNSET:
            field_dict["prompt_tokens"] = prompt_tokens
        if completion_tokens is not UNSET:
            field_dict["completion_tokens"] = completion_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        total_tokens = d.pop("total_tokens", UNSET)

        prompt_tokens = d.pop("prompt_tokens", UNSET)

        completion_tokens = d.pop("completion_tokens", UNSET)

        content_generation_response_usage = cls(
            total_tokens=total_tokens,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )

        content_generation_response_usage.additional_properties = d
        return content_generation_response_usage

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
