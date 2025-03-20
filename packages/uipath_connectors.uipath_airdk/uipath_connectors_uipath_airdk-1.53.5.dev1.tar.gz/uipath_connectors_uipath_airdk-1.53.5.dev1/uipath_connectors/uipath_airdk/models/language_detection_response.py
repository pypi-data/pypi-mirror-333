from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="LanguageDetectionResponse")


@_attrs_define
class LanguageDetectionResponse:
    """
    Attributes:
        confidence_score (Union[Unset, int]): A numerical value representing the certainty of the detected language
            Example: 1.0.
        language (Union[Unset, str]): The detected language. Example: English.
        language_code (Union[Unset, str]): The standardized code representing the detected language Example: en.
    """

    confidence_score: Union[Unset, int] = UNSET
    language: Union[Unset, str] = UNSET
    language_code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        confidence_score = self.confidence_score

        language = self.language

        language_code = self.language_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if confidence_score is not UNSET:
            field_dict["confidenceScore"] = confidence_score
        if language is not UNSET:
            field_dict["language"] = language
        if language_code is not UNSET:
            field_dict["languageCode"] = language_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        confidence_score = d.pop("confidenceScore", UNSET)

        language = d.pop("language", UNSET)

        language_code = d.pop("languageCode", UNSET)

        language_detection_response = cls(
            confidence_score=confidence_score,
            language=language,
            language_code=language_code,
        )

        language_detection_response.additional_properties = d
        return language_detection_response

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
