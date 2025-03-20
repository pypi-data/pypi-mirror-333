from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ObjectDetectionResponseDetectedObjectsArrayItemRef")


@_attrs_define
class ObjectDetectionResponseDetectedObjectsArrayItemRef:
    """
    Attributes:
        details (Union[Unset, str]): Provides additional information about the detected objects. Example: Multiple
            packages are placed in front of the doorstep, clearly visible and accessible..
        name (Union[Unset, str]): The label or identifier for the detected object. Example: Package.
        detected (Union[Unset, str]): Specifies whether the object was successfully detected. Example: Yes.
    """

    details: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    detected: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        details = self.details

        name = self.name

        detected = self.detected

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if details is not UNSET:
            field_dict["details"] = details
        if name is not UNSET:
            field_dict["name"] = name
        if detected is not UNSET:
            field_dict["detected"] = detected

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        details = d.pop("details", UNSET)

        name = d.pop("name", UNSET)

        detected = d.pop("detected", UNSET)

        object_detection_response_detected_objects_array_item_ref = cls(
            details=details,
            name=name,
            detected=detected,
        )

        object_detection_response_detected_objects_array_item_ref.additional_properties = d
        return object_detection_response_detected_objects_array_item_ref

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
