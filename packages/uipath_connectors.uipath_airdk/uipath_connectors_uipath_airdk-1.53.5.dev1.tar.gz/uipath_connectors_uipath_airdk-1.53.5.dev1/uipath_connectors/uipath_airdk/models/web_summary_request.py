from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.web_summary_request_search_engine import WebSummaryRequestSearchEngine


T = TypeVar("T", bound="WebSummaryRequest")


@_attrs_define
class WebSummaryRequest:
    """
    Attributes:
        query (str): The natural language query to search the web for
        provider (WebSummaryRequestSearchEngine): The search engine to use.
    """

    query: str
    provider: WebSummaryRequestSearchEngine
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        provider = self.provider.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "provider": provider,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        query = d.pop("query")

        provider = WebSummaryRequestSearchEngine(d.pop("provider"))

        web_summary_request = cls(
            query=query,
            provider=provider,
        )

        web_summary_request.additional_properties = d
        return web_summary_request

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
