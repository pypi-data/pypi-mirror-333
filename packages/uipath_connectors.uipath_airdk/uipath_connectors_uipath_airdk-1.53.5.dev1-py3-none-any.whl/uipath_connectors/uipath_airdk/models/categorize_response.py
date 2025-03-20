from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="CategorizeResponse")


@_attrs_define
class CategorizeResponse:
    """
    Attributes:
        content (Union[Unset, str]): The content to categorize. This must be provided as a string. Example: I am unable
            to access my email account. Whenever I try to log in, I receive an error message saying 'Invalid username or
            password.
        category (Union[Unset, str]): The inferred category of the content
    """

    content: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content", UNSET)

        category = d.pop("category", UNSET)

        categorize_response = cls(
            content=content,
            category=category,
        )

        categorize_response.additional_properties = d
        return categorize_response

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
