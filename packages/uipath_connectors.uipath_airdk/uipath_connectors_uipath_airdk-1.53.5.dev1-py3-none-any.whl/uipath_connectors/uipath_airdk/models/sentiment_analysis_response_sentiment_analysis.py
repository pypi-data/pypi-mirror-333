from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.sentiment_analysis_response_sentiment_analysis_overall_sentiment import (
        SentimentAnalysisResponseSentimentAnalysisOverallSentiment,
    )
    from ..models.sentiment_analysis_response_sentiment_analysis_sentiment_breakdown import (
        SentimentAnalysisResponseSentimentAnalysisSentimentBreakdown,
    )


T = TypeVar("T", bound="SentimentAnalysisResponseSentimentAnalysis")


@_attrs_define
class SentimentAnalysisResponseSentimentAnalysis:
    """
    Attributes:
        analysis (Union[Unset, str]): Detailed explanation of the sentiment analysis Example: The text contains a mix of
            positive and negative sentiments. The speaker feels lucky for not being at the office, indicating a positive
            sentiment towards their own situation. However, they also mention chaos in the office, which adds a negative
            sentiment about the office environment. The balance between these sentiments leans slightly towards the positive
            due to the speaker's personal relief..
        sentiment_breakdown (Union[Unset, SentimentAnalysisResponseSentimentAnalysisSentimentBreakdown]):
        overall_sentiment (Union[Unset, SentimentAnalysisResponseSentimentAnalysisOverallSentiment]):
        sentiment_breakdown_str (Union[Unset, str]): Counts of positive, negative, neutral, and total statements
            Example: {"positiveStatements":1,"negativeStatements":1,"neutralStatements":0,"totalStatements":2}.
        confidence_level (Union[Unset, int]): The overall confidence level of the analysis Example: 80.0.
        overall_sentiment_str (Union[Unset, str]): Contains the sentiment score and label Example:
            {"score":33,"label":"Slightly Positive"}.
        key_phrases_str (Union[Unset, list[str]]):  Example: {"phrase":"I am feeling lucky to have missed office
            today","sentiment":"Positive","confidence":0.9}.
        undertones_str (Union[Unset, list[str]]):  Example: {"description":"Relief for missing a chaotic situation at
            work","impact":"The positive sentiment of relief is more dominant, contributing to an overall slightly positive
            score."}.
    """

    analysis: Union[Unset, str] = UNSET
    sentiment_breakdown: Union[
        Unset, "SentimentAnalysisResponseSentimentAnalysisSentimentBreakdown"
    ] = UNSET
    overall_sentiment: Union[
        Unset, "SentimentAnalysisResponseSentimentAnalysisOverallSentiment"
    ] = UNSET
    sentiment_breakdown_str: Union[Unset, str] = UNSET
    confidence_level: Union[Unset, int] = UNSET
    overall_sentiment_str: Union[Unset, str] = UNSET
    key_phrases_str: Union[Unset, list[str]] = UNSET
    undertones_str: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        analysis = self.analysis

        sentiment_breakdown: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sentiment_breakdown, Unset):
            sentiment_breakdown = self.sentiment_breakdown.to_dict()

        overall_sentiment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.overall_sentiment, Unset):
            overall_sentiment = self.overall_sentiment.to_dict()

        sentiment_breakdown_str = self.sentiment_breakdown_str

        confidence_level = self.confidence_level

        overall_sentiment_str = self.overall_sentiment_str

        key_phrases_str: Union[Unset, list[str]] = UNSET
        if not isinstance(self.key_phrases_str, Unset):
            key_phrases_str = self.key_phrases_str

        undertones_str: Union[Unset, list[str]] = UNSET
        if not isinstance(self.undertones_str, Unset):
            undertones_str = self.undertones_str

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if analysis is not UNSET:
            field_dict["analysis"] = analysis
        if sentiment_breakdown is not UNSET:
            field_dict["sentimentBreakdown"] = sentiment_breakdown
        if overall_sentiment is not UNSET:
            field_dict["overallSentiment"] = overall_sentiment
        if sentiment_breakdown_str is not UNSET:
            field_dict["sentimentBreakdownStr"] = sentiment_breakdown_str
        if confidence_level is not UNSET:
            field_dict["confidenceLevel"] = confidence_level
        if overall_sentiment_str is not UNSET:
            field_dict["overallSentimentStr"] = overall_sentiment_str
        if key_phrases_str is not UNSET:
            field_dict["keyPhrasesStr"] = key_phrases_str
        if undertones_str is not UNSET:
            field_dict["undertonesStr"] = undertones_str

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.sentiment_analysis_response_sentiment_analysis_overall_sentiment import (
            SentimentAnalysisResponseSentimentAnalysisOverallSentiment,
        )
        from ..models.sentiment_analysis_response_sentiment_analysis_sentiment_breakdown import (
            SentimentAnalysisResponseSentimentAnalysisSentimentBreakdown,
        )

        d = src_dict.copy()
        analysis = d.pop("analysis", UNSET)

        _sentiment_breakdown = d.pop("sentimentBreakdown", UNSET)
        sentiment_breakdown: Union[
            Unset, SentimentAnalysisResponseSentimentAnalysisSentimentBreakdown
        ]
        if isinstance(_sentiment_breakdown, Unset):
            sentiment_breakdown = UNSET
        else:
            sentiment_breakdown = (
                SentimentAnalysisResponseSentimentAnalysisSentimentBreakdown.from_dict(
                    _sentiment_breakdown
                )
            )

        _overall_sentiment = d.pop("overallSentiment", UNSET)
        overall_sentiment: Union[
            Unset, SentimentAnalysisResponseSentimentAnalysisOverallSentiment
        ]
        if isinstance(_overall_sentiment, Unset):
            overall_sentiment = UNSET
        else:
            overall_sentiment = (
                SentimentAnalysisResponseSentimentAnalysisOverallSentiment.from_dict(
                    _overall_sentiment
                )
            )

        sentiment_breakdown_str = d.pop("sentimentBreakdownStr", UNSET)

        confidence_level = d.pop("confidenceLevel", UNSET)

        overall_sentiment_str = d.pop("overallSentimentStr", UNSET)

        key_phrases_str = cast(list[str], d.pop("keyPhrasesStr", UNSET))

        undertones_str = cast(list[str], d.pop("undertonesStr", UNSET))

        sentiment_analysis_response_sentiment_analysis = cls(
            analysis=analysis,
            sentiment_breakdown=sentiment_breakdown,
            overall_sentiment=overall_sentiment,
            sentiment_breakdown_str=sentiment_breakdown_str,
            confidence_level=confidence_level,
            overall_sentiment_str=overall_sentiment_str,
            key_phrases_str=key_phrases_str,
            undertones_str=undertones_str,
        )

        sentiment_analysis_response_sentiment_analysis.additional_properties = d
        return sentiment_analysis_response_sentiment_analysis

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
