from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.pii_detection_request_language import PIIDetectionRequestLanguage
from ..models.pii_detection_request_piiphi_category import (
    PIIDetectionRequestPIIPHICategory,
)
from typing import Union


T = TypeVar("T", bound="PIIDetectionRequest")


@_attrs_define
class PIIDetectionRequest:
    """
    Attributes:
        text (str): The document or text string containing the content to analyze for PII Example: Call our office at
            312-555-1234, or send an email to support@contoso.com.
        confidence_threshold (Union[Unset, float]): The minimum confidence score required in order to be considered.
            This is between 0-1 with 0 being the lowest and 1 being the highest confidence.  If not set, all detection
            results are returned regardless of the confidence score Example: 0.5.
        language_code (Union[Unset, PIIDetectionRequestLanguage]): The language of the text or document input.  Defaults
            to English if not set.  Please note that not all PII/PHI categories are supported for all languages Example: en.
        pii_entity_categories (Union[Unset, list[PIIDetectionRequestPIIPHICategory]]):  Example: PhoneNumber.
    """

    text: str
    confidence_threshold: Union[Unset, float] = UNSET
    language_code: Union[Unset, PIIDetectionRequestLanguage] = UNSET
    pii_entity_categories: Union[Unset, list[PIIDetectionRequestPIIPHICategory]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        confidence_threshold = self.confidence_threshold

        language_code: Union[Unset, str] = UNSET
        if not isinstance(self.language_code, Unset):
            language_code = self.language_code.value

        pii_entity_categories: Union[Unset, list[str]] = UNSET
        if not isinstance(self.pii_entity_categories, Unset):
            pii_entity_categories = []
            for pii_entity_categories_item_data in self.pii_entity_categories:
                pii_entity_categories_item = pii_entity_categories_item_data.value
                pii_entity_categories.append(pii_entity_categories_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
            }
        )
        if confidence_threshold is not UNSET:
            field_dict["confidenceThreshold"] = confidence_threshold
        if language_code is not UNSET:
            field_dict["languageCode"] = language_code
        if pii_entity_categories is not UNSET:
            field_dict["piiEntityCategories"] = pii_entity_categories

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        text = d.pop("text")

        confidence_threshold = d.pop("confidenceThreshold", UNSET)

        _language_code = d.pop("languageCode", UNSET)
        language_code: Union[Unset, PIIDetectionRequestLanguage]
        if isinstance(_language_code, Unset):
            language_code = UNSET
        else:
            language_code = PIIDetectionRequestLanguage(_language_code)

        pii_entity_categories = []
        _pii_entity_categories = d.pop("piiEntityCategories", UNSET)
        for pii_entity_categories_item_data in _pii_entity_categories or []:
            pii_entity_categories_item = PIIDetectionRequestPIIPHICategory(
                pii_entity_categories_item_data
            )

            pii_entity_categories.append(pii_entity_categories_item)

        pii_detection_request = cls(
            text=text,
            confidence_threshold=confidence_threshold,
            language_code=language_code,
            pii_entity_categories=pii_entity_categories,
        )

        pii_detection_request.additional_properties = d
        return pii_detection_request

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
