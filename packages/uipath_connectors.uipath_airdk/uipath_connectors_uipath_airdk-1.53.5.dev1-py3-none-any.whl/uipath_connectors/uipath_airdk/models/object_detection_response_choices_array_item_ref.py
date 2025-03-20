from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.object_detection_response_choices_message import (
        ObjectDetectionResponseChoicesMessage,
    )


T = TypeVar("T", bound="ObjectDetectionResponseChoicesArrayItemRef")


@_attrs_define
class ObjectDetectionResponseChoicesArrayItemRef:
    """
    Attributes:
        index (Union[Unset, int]): The unique identifier for each detection choice. Example: 0.0.
        finish_reason (Union[Unset, str]): The reason why the detection choice process finished. Example: stop.
        message (Union[Unset, ObjectDetectionResponseChoicesMessage]):
    """

    index: Union[Unset, int] = UNSET
    finish_reason: Union[Unset, str] = UNSET
    message: Union[Unset, "ObjectDetectionResponseChoicesMessage"] = UNSET
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
        from ..models.object_detection_response_choices_message import (
            ObjectDetectionResponseChoicesMessage,
        )

        d = src_dict.copy()
        index = d.pop("index", UNSET)

        finish_reason = d.pop("finish_reason", UNSET)

        _message = d.pop("message", UNSET)
        message: Union[Unset, ObjectDetectionResponseChoicesMessage]
        if isinstance(_message, Unset):
            message = UNSET
        else:
            message = ObjectDetectionResponseChoicesMessage.from_dict(_message)

        object_detection_response_choices_array_item_ref = cls(
            index=index,
            finish_reason=finish_reason,
            message=message,
        )

        object_detection_response_choices_array_item_ref.additional_properties = d
        return object_detection_response_choices_array_item_ref

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
