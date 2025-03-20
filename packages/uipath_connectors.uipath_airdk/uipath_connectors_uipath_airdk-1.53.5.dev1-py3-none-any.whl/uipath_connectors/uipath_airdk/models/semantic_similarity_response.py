from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.semantic_similarity_response_semantic_similarity import (
        SemanticSimilarityResponseSemanticSimilarity,
    )


T = TypeVar("T", bound="SemanticSimilarityResponse")


@_attrs_define
class SemanticSimilarityResponse:
    """
    Attributes:
        semantic_similarity (Union[Unset, SemanticSimilarityResponseSemanticSimilarity]):
    """

    semantic_similarity: Union[
        Unset, "SemanticSimilarityResponseSemanticSimilarity"
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        semantic_similarity: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.semantic_similarity, Unset):
            semantic_similarity = self.semantic_similarity.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if semantic_similarity is not UNSET:
            field_dict["semanticSimilarity"] = semantic_similarity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.semantic_similarity_response_semantic_similarity import (
            SemanticSimilarityResponseSemanticSimilarity,
        )

        d = src_dict.copy()
        _semantic_similarity = d.pop("semanticSimilarity", UNSET)
        semantic_similarity: Union[Unset, SemanticSimilarityResponseSemanticSimilarity]
        if isinstance(_semantic_similarity, Unset):
            semantic_similarity = UNSET
        else:
            semantic_similarity = (
                SemanticSimilarityResponseSemanticSimilarity.from_dict(
                    _semantic_similarity
                )
            )

        semantic_similarity_response = cls(
            semantic_similarity=semantic_similarity,
        )

        semantic_similarity_response.additional_properties = d
        return semantic_similarity_response

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
