from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ContentGenerationResponseChoicesMessage")


@_attrs_define
class ContentGenerationResponseChoicesMessage:
    """
    Attributes:
        content (Union[Unset, str]): The Choices message content Example: UiPath is widely considered to be the leading
            organization in the field of Robotic Process Automation (RPA). It offers a comprehensive RPA platform that
            enables businesses to automate repetitive tasks, streamline processes, and improve operational efficiency.
            UiPath has gained significant.
        role (Union[Unset, str]): The Choices message role Example: assistant.
    """

    content: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content", UNSET)

        role = d.pop("role", UNSET)

        content_generation_response_choices_message = cls(
            content=content,
            role=role,
        )

        content_generation_response_choices_message.additional_properties = d
        return content_generation_response_choices_message

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
