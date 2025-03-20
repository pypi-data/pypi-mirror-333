from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ContextGroundingSearchRequestQuery")


@_attrs_define
class ContextGroundingSearchRequestQuery:
    """
    Attributes:
        query (str): Text used to query the index or file and return similar context Example: List of Day Care Surgeries
            for Magma HDI GIC Ltd.
        number_of_results (Union[Unset, int]): The total number of results returned by the query Example: 3.0.
        threshold (Union[Unset, float]): The minimum relevance score for search results Example: 0.85.
    """

    query: str
    number_of_results: Union[Unset, int] = UNSET
    threshold: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        number_of_results = self.number_of_results

        threshold = self.threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if number_of_results is not UNSET:
            field_dict["numberOfResults"] = number_of_results
        if threshold is not UNSET:
            field_dict["threshold"] = threshold

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        query = d.pop("query")

        number_of_results = d.pop("numberOfResults", UNSET)

        threshold = d.pop("threshold", UNSET)

        context_grounding_search_request_query = cls(
            query=query,
            number_of_results=number_of_results,
            threshold=threshold,
        )

        context_grounding_search_request_query.additional_properties = d
        return context_grounding_search_request_query

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
