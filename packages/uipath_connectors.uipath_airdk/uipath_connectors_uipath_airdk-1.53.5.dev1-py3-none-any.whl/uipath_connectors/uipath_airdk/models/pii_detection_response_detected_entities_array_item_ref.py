from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="PIIDetectionResponseDetectedEntitiesArrayItemRef")


@_attrs_define
class PIIDetectionResponseDetectedEntitiesArrayItemRef:
    """
    Attributes:
        identifier (Union[Unset, str]): Detected entities identifier Example: PhoneNumber-19.
        text (Union[Unset, str]): Detected entities text Example: 312-555-1234.
        confidence_score (Union[Unset, float]): The Detected entities confidence score Example: 0.8.
    """

    identifier: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    confidence_score: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        identifier = self.identifier

        text = self.text

        confidence_score = self.confidence_score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if text is not UNSET:
            field_dict["text"] = text
        if confidence_score is not UNSET:
            field_dict["confidenceScore"] = confidence_score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        identifier = d.pop("identifier", UNSET)

        text = d.pop("text", UNSET)

        confidence_score = d.pop("confidenceScore", UNSET)

        pii_detection_response_detected_entities_array_item_ref = cls(
            identifier=identifier,
            text=text,
            confidence_score=confidence_score,
        )

        pii_detection_response_detected_entities_array_item_ref.additional_properties = d
        return pii_detection_response_detected_entities_array_item_ref

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
