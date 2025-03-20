from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.semantic_similarity_request_output_format import (
    SemanticSimilarityRequestOutputFormat,
)
from ..models.semantic_similarity_request_similarity_type import (
    SemanticSimilarityRequestSimilarityType,
)
from typing import Union


T = TypeVar("T", bound="SemanticSimilarityRequest")


@_attrs_define
class SemanticSimilarityRequest:
    """
    Attributes:
        second_comparison_input (str): The second string of text for calculating similarity. Example: AI applications
            are limited to tech companies..
        first_comparison_input (str): The first string of text for calculating similarity. Example: Artificial
            intelligence is revolutionizing various industries..
        similarity_type (SemanticSimilarityRequestSimilarityType): The type of similarity which can either be a string
            to string comparison or a string to a list of strings. Example: String to string.
        output_format (Union[Unset, SemanticSimilarityRequestOutputFormat]): If  'best match’ is selected for similarity
            type, the output will be the most likely match.  If list of scores is selected, the output will assign a
            similarity score for for the whole list of outputs. Example: Best match.
        comparison_array (Union[Unset, str]): Array of strings to compare first input against for matching. Example:
            ["Machine learning is transforming multiple sectors.", "Traditional methods are becoming obsolete.", "AI
            applications are limited to tech companies."].
    """

    second_comparison_input: str
    first_comparison_input: str
    similarity_type: SemanticSimilarityRequestSimilarityType
    output_format: Union[Unset, SemanticSimilarityRequestOutputFormat] = UNSET
    comparison_array: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        second_comparison_input = self.second_comparison_input

        first_comparison_input = self.first_comparison_input

        similarity_type = self.similarity_type.value

        output_format: Union[Unset, str] = UNSET
        if not isinstance(self.output_format, Unset):
            output_format = self.output_format.value

        comparison_array = self.comparison_array

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "secondComparisonInput": second_comparison_input,
                "firstComparisonInput": first_comparison_input,
                "similarityType": similarity_type,
            }
        )
        if output_format is not UNSET:
            field_dict["outputFormat"] = output_format
        if comparison_array is not UNSET:
            field_dict["comparisonArray"] = comparison_array

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        second_comparison_input = d.pop("secondComparisonInput")

        first_comparison_input = d.pop("firstComparisonInput")

        similarity_type = SemanticSimilarityRequestSimilarityType(
            d.pop("similarityType")
        )

        _output_format = d.pop("outputFormat", UNSET)
        output_format: Union[Unset, SemanticSimilarityRequestOutputFormat]
        if isinstance(_output_format, Unset):
            output_format = UNSET
        else:
            output_format = SemanticSimilarityRequestOutputFormat(_output_format)

        comparison_array = d.pop("comparisonArray", UNSET)

        semantic_similarity_request = cls(
            second_comparison_input=second_comparison_input,
            first_comparison_input=first_comparison_input,
            similarity_type=similarity_type,
            output_format=output_format,
            comparison_array=comparison_array,
        )

        semantic_similarity_request.additional_properties = d
        return semantic_similarity_request

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
