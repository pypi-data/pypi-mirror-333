from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="WebSearchResponseResultsArrayItemRef")


@_attrs_define
class WebSearchResponseResultsArrayItemRef:
    """
    Attributes:
        title (Union[Unset, str]): The title of a search result item.
        snippet (Union[Unset, str]): A brief summary or excerpt of a search result item.
        url (Union[Unset, str]): The web address of the search result.
    """

    title: Union[Unset, str] = UNSET
    snippet: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        snippet = self.snippet

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if snippet is not UNSET:
            field_dict["snippet"] = snippet
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title", UNSET)

        snippet = d.pop("snippet", UNSET)

        url = d.pop("url", UNSET)

        web_search_response_results_array_item_ref = cls(
            title=title,
            snippet=snippet,
            url=url,
        )

        web_search_response_results_array_item_ref.additional_properties = d
        return web_search_response_results_array_item_ref

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
