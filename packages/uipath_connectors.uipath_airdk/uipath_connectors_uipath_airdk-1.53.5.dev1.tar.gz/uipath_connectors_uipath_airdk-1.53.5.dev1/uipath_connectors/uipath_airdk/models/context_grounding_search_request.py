from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.context_grounding_search_request_query import (
        ContextGroundingSearchRequestQuery,
    )
    from ..models.context_grounding_search_request_schema import (
        ContextGroundingSearchRequestSchema,
    )


T = TypeVar("T", bound="ContextGroundingSearchRequest")


@_attrs_define
class ContextGroundingSearchRequest:
    """
    Attributes:
        query (Union[Unset, ContextGroundingSearchRequestQuery]):
        schema (Union[Unset, ContextGroundingSearchRequestSchema]):
    """

    query: Union[Unset, "ContextGroundingSearchRequestQuery"] = UNSET
    schema: Union[Unset, "ContextGroundingSearchRequestSchema"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        query: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.query, Unset):
            query = self.query.to_dict()

        schema: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query is not UNSET:
            field_dict["query"] = query
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.context_grounding_search_request_query import (
            ContextGroundingSearchRequestQuery,
        )
        from ..models.context_grounding_search_request_schema import (
            ContextGroundingSearchRequestSchema,
        )

        d = src_dict.copy()
        _query = d.pop("query", UNSET)
        query: Union[Unset, ContextGroundingSearchRequestQuery]
        if isinstance(_query, Unset):
            query = UNSET
        else:
            query = ContextGroundingSearchRequestQuery.from_dict(_query)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, ContextGroundingSearchRequestSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = ContextGroundingSearchRequestSchema.from_dict(_schema)

        context_grounding_search_request = cls(
            query=query,
            schema=schema,
        )

        context_grounding_search_request.additional_properties = d
        return context_grounding_search_request

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
