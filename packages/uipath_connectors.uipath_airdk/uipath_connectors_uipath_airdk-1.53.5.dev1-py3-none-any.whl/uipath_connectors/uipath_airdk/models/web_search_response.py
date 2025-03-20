from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.web_search_response_results_array_item_ref import (
        WebSearchResponseResultsArrayItemRef,
    )


T = TypeVar("T", bound="WebSearchResponse")


@_attrs_define
class WebSearchResponse:
    """
    Attributes:
        formatted_results (Union[Unset, str]): The search results string containing title, URL, and snippet
        results (Union[Unset, list['WebSearchResponseResultsArrayItemRef']]):
    """

    formatted_results: Union[Unset, str] = UNSET
    results: Union[Unset, list["WebSearchResponseResultsArrayItemRef"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        formatted_results = self.formatted_results

        results: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for componentsschemas_web_search_response_results_item_data in self.results:
                componentsschemas_web_search_response_results_item = (
                    componentsschemas_web_search_response_results_item_data.to_dict()
                )
                results.append(componentsschemas_web_search_response_results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if formatted_results is not UNSET:
            field_dict["formattedResults"] = formatted_results
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.web_search_response_results_array_item_ref import (
            WebSearchResponseResultsArrayItemRef,
        )

        d = src_dict.copy()
        formatted_results = d.pop("formattedResults", UNSET)

        results = []
        _results = d.pop("results", UNSET)
        for componentsschemas_web_search_response_results_item_data in _results or []:
            componentsschemas_web_search_response_results_item = (
                WebSearchResponseResultsArrayItemRef.from_dict(
                    componentsschemas_web_search_response_results_item_data
                )
            )

            results.append(componentsschemas_web_search_response_results_item)

        web_search_response = cls(
            formatted_results=formatted_results,
            results=results,
        )

        web_search_response.additional_properties = d
        return web_search_response

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
