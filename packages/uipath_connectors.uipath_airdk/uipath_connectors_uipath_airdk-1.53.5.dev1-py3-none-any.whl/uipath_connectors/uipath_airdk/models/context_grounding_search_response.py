from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.context_grounding_search_response_search_result_array_array_item_ref import (
        ContextGroundingSearchResponseSearchResultArrayArrayItemRef,
    )


T = TypeVar("T", bound="ContextGroundingSearchResponse")


@_attrs_define
class ContextGroundingSearchResponse:
    r"""
    Attributes:
        search_result (Union[Unset, str]): The outcome of the search query. Example: [{"source":"List of Day Care
            Surgeries for Magma HDI GIC Ltd_f0834f2d174_1712824796337.pdf","content":"# List of Day Care Surgeries for Magma
            HDI GIC Ltd\n\n## CARDIOLOGY RELATED\n1 CORONARY ANGIOGRAPHY\n\n## CRITICAL CARE RELATED\n2 INSERT NON- TUNNEL
            CV CATH","page_number":"1"},{"source":"List of Day Care Surgeries for Magma HDI GIC
            Ltd_f0834f2d174_1712824796337.pdf","content":"```markdown\nList of Day Care Surgeries for Magma HDI GIC
            Ltd\n\nCARDIOLOGY RELATED\n1 CORONARY ANGIOGRAPHY","page_number":"1"}].
        search_result_array (Union[Unset, list['ContextGroundingSearchResponseSearchResultArrayArrayItemRef']]):
    """

    search_result: Union[Unset, str] = UNSET
    search_result_array: Union[
        Unset, list["ContextGroundingSearchResponseSearchResultArrayArrayItemRef"]
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        search_result = self.search_result

        search_result_array: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.search_result_array, Unset):
            search_result_array = []
            for componentsschemas_context_grounding_search_response_search_result_array_item_data in self.search_result_array:
                componentsschemas_context_grounding_search_response_search_result_array_item = componentsschemas_context_grounding_search_response_search_result_array_item_data.to_dict()
                search_result_array.append(
                    componentsschemas_context_grounding_search_response_search_result_array_item
                )

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if search_result is not UNSET:
            field_dict["searchResult"] = search_result
        if search_result_array is not UNSET:
            field_dict["searchResultArray"] = search_result_array

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.context_grounding_search_response_search_result_array_array_item_ref import (
            ContextGroundingSearchResponseSearchResultArrayArrayItemRef,
        )

        d = src_dict.copy()
        search_result = d.pop("searchResult", UNSET)

        search_result_array = []
        _search_result_array = d.pop("searchResultArray", UNSET)
        for componentsschemas_context_grounding_search_response_search_result_array_item_data in (
            _search_result_array or []
        ):
            componentsschemas_context_grounding_search_response_search_result_array_item = ContextGroundingSearchResponseSearchResultArrayArrayItemRef.from_dict(
                componentsschemas_context_grounding_search_response_search_result_array_item_data
            )

            search_result_array.append(
                componentsschemas_context_grounding_search_response_search_result_array_item
            )

        context_grounding_search_response = cls(
            search_result=search_result,
            search_result_array=search_result_array,
        )

        context_grounding_search_response.additional_properties = d
        return context_grounding_search_response

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
