from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.pii_detection_response_detected_entities_array_item_ref import (
        PIIDetectionResponseDetectedEntitiesArrayItemRef,
    )


T = TypeVar("T", bound="PIIDetectionResponse")


@_attrs_define
class PIIDetectionResponse:
    """
    Attributes:
        initial_text (Union[Unset, str]): The Initial text Example: Call our office at 312-555-1234, or send an email to
            support@contoso.com.
        detected_entities (Union[Unset, list['PIIDetectionResponseDetectedEntitiesArrayItemRef']]):
        masked_text (Union[Unset, str]): Redacted text for all PII/PHI discovered in input Example: Call our office at
            PhoneNumber-19, or send an email to Email-53.
    """

    initial_text: Union[Unset, str] = UNSET
    detected_entities: Union[
        Unset, list["PIIDetectionResponseDetectedEntitiesArrayItemRef"]
    ] = UNSET
    masked_text: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        initial_text = self.initial_text

        detected_entities: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.detected_entities, Unset):
            detected_entities = []
            for (
                componentsschemas_pii_detection_response_detected_entities_item_data
            ) in self.detected_entities:
                componentsschemas_pii_detection_response_detected_entities_item = componentsschemas_pii_detection_response_detected_entities_item_data.to_dict()
                detected_entities.append(
                    componentsschemas_pii_detection_response_detected_entities_item
                )

        masked_text = self.masked_text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if initial_text is not UNSET:
            field_dict["initialText"] = initial_text
        if detected_entities is not UNSET:
            field_dict["detectedEntities"] = detected_entities
        if masked_text is not UNSET:
            field_dict["maskedText"] = masked_text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.pii_detection_response_detected_entities_array_item_ref import (
            PIIDetectionResponseDetectedEntitiesArrayItemRef,
        )

        d = src_dict.copy()
        initial_text = d.pop("initialText", UNSET)

        detected_entities = []
        _detected_entities = d.pop("detectedEntities", UNSET)
        for componentsschemas_pii_detection_response_detected_entities_item_data in (
            _detected_entities or []
        ):
            componentsschemas_pii_detection_response_detected_entities_item = (
                PIIDetectionResponseDetectedEntitiesArrayItemRef.from_dict(
                    componentsschemas_pii_detection_response_detected_entities_item_data
                )
            )

            detected_entities.append(
                componentsschemas_pii_detection_response_detected_entities_item
            )

        masked_text = d.pop("maskedText", UNSET)

        pii_detection_response = cls(
            initial_text=initial_text,
            detected_entities=detected_entities,
            masked_text=masked_text,
        )

        pii_detection_response.additional_properties = d
        return pii_detection_response

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
