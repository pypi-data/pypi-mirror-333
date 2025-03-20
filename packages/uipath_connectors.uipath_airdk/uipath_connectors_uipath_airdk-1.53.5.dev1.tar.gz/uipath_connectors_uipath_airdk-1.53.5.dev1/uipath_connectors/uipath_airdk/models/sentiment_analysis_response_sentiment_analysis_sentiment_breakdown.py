from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SentimentAnalysisResponseSentimentAnalysisSentimentBreakdown")


@_attrs_define
class SentimentAnalysisResponseSentimentAnalysisSentimentBreakdown:
    """
    Attributes:
        neutral_statements (Union[Unset, int]): The number of statements classified as neutral. Example: 0.0.
        positive_statements (Union[Unset, int]): Provides an array of statements identified as positive. Example: 1.0.
        total_statements (Union[Unset, int]): The total count of statements evaluated for sentiment analysis. Example:
            2.0.
        negative_statements (Union[Unset, int]): The number of statements identified as negative. Example: 1.0.
    """

    neutral_statements: Union[Unset, int] = UNSET
    positive_statements: Union[Unset, int] = UNSET
    total_statements: Union[Unset, int] = UNSET
    negative_statements: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        neutral_statements = self.neutral_statements

        positive_statements = self.positive_statements

        total_statements = self.total_statements

        negative_statements = self.negative_statements

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if neutral_statements is not UNSET:
            field_dict["neutralStatements"] = neutral_statements
        if positive_statements is not UNSET:
            field_dict["positiveStatements"] = positive_statements
        if total_statements is not UNSET:
            field_dict["totalStatements"] = total_statements
        if negative_statements is not UNSET:
            field_dict["negativeStatements"] = negative_statements

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        neutral_statements = d.pop("neutralStatements", UNSET)

        positive_statements = d.pop("positiveStatements", UNSET)

        total_statements = d.pop("totalStatements", UNSET)

        negative_statements = d.pop("negativeStatements", UNSET)

        sentiment_analysis_response_sentiment_analysis_sentiment_breakdown = cls(
            neutral_statements=neutral_statements,
            positive_statements=positive_statements,
            total_statements=total_statements,
            negative_statements=negative_statements,
        )

        sentiment_analysis_response_sentiment_analysis_sentiment_breakdown.additional_properties = d
        return sentiment_analysis_response_sentiment_analysis_sentiment_breakdown

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
