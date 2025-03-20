from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SemanticSimilarityResponseSemanticSimilarity")


@_attrs_define
class SemanticSimilarityResponseSemanticSimilarity:
    """
    Attributes:
        list_of_scores (Union[Unset, str]): A list containing similarity scores for multiple comparisons (only for list
            of score). Example: [{"string":"Machine learning is transforming multiple
            sectors.","similarityScore":0.85,"similarityExplanation":"High similarity due to shared context and intent. Both
            sentences discuss the impact of advanced technologies (AI and machine learning) on various industries or
            sectors. The key concepts of technological transformation and industry impact are present in both. The
            vocabulary differs slightly but conveys a similar theme."},{"string":"Traditional methods are becoming
            obsolete.","similarityScore":0.4,"similarityExplanation":"Moderate similarity. While the primary string
            discusses the positive impact of AI on industries, this comparison string implies a negative consequence
            (obsolescence of traditional methods) which can be indirectly related to the rise of AI. The context of
            technological change is present, but the intent and sentiment differ."},{"string":"AI applications are limited
            to tech companies.","similarityScore":0.6,"similarityExplanation":"Moderate to high similarity. Both sentences
            discuss AI, but the primary string emphasizes its broad impact across various industries, while the comparison
            string suggests a limitation to tech companies. The key concept of AI is shared, but the scope and sentiment
            differ, with the comparison string presenting a more restricted view."}].
        string (Union[Unset, str]): Best match string out of the provided comparison array (only for best match).
        similarity_score (Union[Unset, float]): The calculated score representing the semantic similarity (only for
            string to string or best match). Example: 0.3.
        similarity_explanation (Union[Unset, str]): Provides an explanation of the semantic similarity result (only for
            string to string or best match).
    """

    list_of_scores: Union[Unset, str] = UNSET
    string: Union[Unset, str] = UNSET
    similarity_score: Union[Unset, float] = UNSET
    similarity_explanation: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        list_of_scores = self.list_of_scores

        string = self.string

        similarity_score = self.similarity_score

        similarity_explanation = self.similarity_explanation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if list_of_scores is not UNSET:
            field_dict["listOfScores"] = list_of_scores
        if string is not UNSET:
            field_dict["string"] = string
        if similarity_score is not UNSET:
            field_dict["similarityScore"] = similarity_score
        if similarity_explanation is not UNSET:
            field_dict["similarityExplanation"] = similarity_explanation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        list_of_scores = d.pop("listOfScores", UNSET)

        string = d.pop("string", UNSET)

        similarity_score = d.pop("similarityScore", UNSET)

        similarity_explanation = d.pop("similarityExplanation", UNSET)

        semantic_similarity_response_semantic_similarity = cls(
            list_of_scores=list_of_scores,
            string=string,
            similarity_score=similarity_score,
            similarity_explanation=similarity_explanation,
        )

        semantic_similarity_response_semantic_similarity.additional_properties = d
        return semantic_similarity_response_semantic_similarity

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
