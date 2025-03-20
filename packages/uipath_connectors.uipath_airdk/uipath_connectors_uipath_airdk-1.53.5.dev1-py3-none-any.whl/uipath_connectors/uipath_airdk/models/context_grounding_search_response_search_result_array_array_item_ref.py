from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ContextGroundingSearchResponseSearchResultArrayArrayItemRef")


@_attrs_define
class ContextGroundingSearchResponseSearchResultArrayArrayItemRef:
    """
    Attributes:
        content (Union[Unset, str]): The content of each item in the search results. Example: # List of Day Care
            Surgeries for Magma HDI GIC Ltd

            ## CARDIOLOGY RELATED
            1 CORONARY ANGIOGRAPHY

            ## CRITICAL CARE RELATED
            2 INSERT NON- TUNNEL CV CATH.
        source (Union[Unset, str]): Indicates the origin of the search result. Example: List of Day Care Surgeries for
            Magma HDI GIC Ltd_f0834f2d174_1712824796337.pdf.
        page_number (Union[Unset, str]): The page number where the search result is found. Example: 1.
    """

    content: Union[Unset, str] = UNSET
    source: Union[Unset, str] = UNSET
    page_number: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        source = self.source

        page_number = self.page_number

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if source is not UNSET:
            field_dict["source"] = source
        if page_number is not UNSET:
            field_dict["page_number"] = page_number

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content", UNSET)

        source = d.pop("source", UNSET)

        page_number = d.pop("page_number", UNSET)

        context_grounding_search_response_search_result_array_array_item_ref = cls(
            content=content,
            source=source,
            page_number=page_number,
        )

        context_grounding_search_response_search_result_array_array_item_ref.additional_properties = d
        return context_grounding_search_response_search_result_array_array_item_ref

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
