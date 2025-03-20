from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ContentGenerationResponseDetectedEntitiesArrayItemRef")


@_attrs_define
class ContentGenerationResponseDetectedEntitiesArrayItemRef:
    """
    Attributes:
        identifier (Union[Unset, str]): Unique code representing a detected entity in the text. Example: Person-336.
        text (Union[Unset, str]): The text of the entity that was detected in the input. Example: John Smith.
        confidence_score (Union[Unset, int]): A numerical value representing the AI's certainty in the entity detection
            Example: 1.0.
        category (Union[Unset, str]): It represents the detected category of the text. Example: Person.
    """

    identifier: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    confidence_score: Union[Unset, int] = UNSET
    category: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        identifier = self.identifier

        text = self.text

        confidence_score = self.confidence_score

        category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if text is not UNSET:
            field_dict["text"] = text
        if confidence_score is not UNSET:
            field_dict["confidenceScore"] = confidence_score
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        identifier = d.pop("identifier", UNSET)

        text = d.pop("text", UNSET)

        confidence_score = d.pop("confidenceScore", UNSET)

        category = d.pop("category", UNSET)

        content_generation_response_detected_entities_array_item_ref = cls(
            identifier=identifier,
            text=text,
            confidence_score=confidence_score,
            category=category,
        )

        content_generation_response_detected_entities_array_item_ref.additional_properties = d
        return content_generation_response_detected_entities_array_item_ref

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
