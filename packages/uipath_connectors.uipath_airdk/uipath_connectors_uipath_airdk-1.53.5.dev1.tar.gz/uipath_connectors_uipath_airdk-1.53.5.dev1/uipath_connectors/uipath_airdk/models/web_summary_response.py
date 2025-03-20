from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="WebSummaryResponse")


@_attrs_define
class WebSummaryResponse:
    """
    Attributes:
        response (Union[Unset, str]): The summary of the web search results.
        citations (Union[Unset, list[str]]):
    """

    response: Union[Unset, str] = UNSET
    citations: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response = self.response

        citations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.citations, Unset):
            citations = self.citations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if response is not UNSET:
            field_dict["response"] = response
        if citations is not UNSET:
            field_dict["citations"] = citations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        response = d.pop("response", UNSET)

        citations = cast(list[str], d.pop("citations", UNSET))

        web_summary_response = cls(
            response=response,
            citations=citations,
        )

        web_summary_response.additional_properties = d
        return web_summary_response

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
