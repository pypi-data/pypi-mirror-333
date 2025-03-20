from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.content_generation_response_choices_message import (
        ContentGenerationResponseChoicesMessage,
    )


T = TypeVar("T", bound="ContentGenerationResponseChoicesArrayItemRef")


@_attrs_define
class ContentGenerationResponseChoicesArrayItemRef:
    """
    Attributes:
        index (Union[Unset, int]): The Choices index Example: 0.0.
        finish_reason (Union[Unset, str]): The Choices finish reason Example: length.
        message (Union[Unset, ContentGenerationResponseChoicesMessage]):
    """

    index: Union[Unset, int] = UNSET
    finish_reason: Union[Unset, str] = UNSET
    message: Union[Unset, "ContentGenerationResponseChoicesMessage"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        index = self.index

        finish_reason = self.finish_reason

        message: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.message, Unset):
            message = self.message.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if index is not UNSET:
            field_dict["index"] = index
        if finish_reason is not UNSET:
            field_dict["finish_reason"] = finish_reason
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.content_generation_response_choices_message import (
            ContentGenerationResponseChoicesMessage,
        )

        d = src_dict.copy()
        index = d.pop("index", UNSET)

        finish_reason = d.pop("finish_reason", UNSET)

        _message = d.pop("message", UNSET)
        message: Union[Unset, ContentGenerationResponseChoicesMessage]
        if isinstance(_message, Unset):
            message = UNSET
        else:
            message = ContentGenerationResponseChoicesMessage.from_dict(_message)

        content_generation_response_choices_array_item_ref = cls(
            index=index,
            finish_reason=finish_reason,
            message=message,
        )

        content_generation_response_choices_array_item_ref.additional_properties = d
        return content_generation_response_choices_array_item_ref

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
