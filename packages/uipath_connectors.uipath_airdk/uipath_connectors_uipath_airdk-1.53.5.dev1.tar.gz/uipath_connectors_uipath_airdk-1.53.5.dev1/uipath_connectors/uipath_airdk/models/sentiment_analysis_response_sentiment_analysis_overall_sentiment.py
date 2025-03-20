from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SentimentAnalysisResponseSentimentAnalysisOverallSentiment")


@_attrs_define
class SentimentAnalysisResponseSentimentAnalysisOverallSentiment:
    """
    Attributes:
        label (Union[Unset, str]): Categorizes the overall sentiment expressed in the text. Example: Slightly Positive.
        score (Union[Unset, int]): A numerical score representing the overall sentiment. Example: 20.0.
    """

    label: Union[Unset, str] = UNSET
    score: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        score = self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if score is not UNSET:
            field_dict["score"] = score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label", UNSET)

        score = d.pop("score", UNSET)

        sentiment_analysis_response_sentiment_analysis_overall_sentiment = cls(
            label=label,
            score=score,
        )

        sentiment_analysis_response_sentiment_analysis_overall_sentiment.additional_properties = d
        return sentiment_analysis_response_sentiment_analysis_overall_sentiment

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
