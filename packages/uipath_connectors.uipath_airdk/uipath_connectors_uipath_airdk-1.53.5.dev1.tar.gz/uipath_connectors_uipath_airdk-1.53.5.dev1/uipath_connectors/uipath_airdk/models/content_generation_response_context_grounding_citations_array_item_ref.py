from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ContentGenerationResponseContextGroundingCitationsArrayItemRef")


@_attrs_define
class ContentGenerationResponseContextGroundingCitationsArrayItemRef:
    """
    Attributes:
        reference (Union[Unset, str]): The Context grounding citations reference
        source (Union[Unset, str]): The Context grounding citations source Example: OP2_MedLM_Results.pdf.
        page_number (Union[Unset, int]): The Context grounding citations page number Example: 0.0.
    """

    reference: Union[Unset, str] = UNSET
    source: Union[Unset, str] = UNSET
    page_number: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reference = self.reference

        source = self.source

        page_number = self.page_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reference is not UNSET:
            field_dict["reference"] = reference
        if source is not UNSET:
            field_dict["source"] = source
        if page_number is not UNSET:
            field_dict["page_number"] = page_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        reference = d.pop("reference", UNSET)

        source = d.pop("source", UNSET)

        page_number = d.pop("page_number", UNSET)

        content_generation_response_context_grounding_citations_array_item_ref = cls(
            reference=reference,
            source=source,
            page_number=page_number,
        )

        content_generation_response_context_grounding_citations_array_item_ref.additional_properties = d
        return content_generation_response_context_grounding_citations_array_item_ref

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
