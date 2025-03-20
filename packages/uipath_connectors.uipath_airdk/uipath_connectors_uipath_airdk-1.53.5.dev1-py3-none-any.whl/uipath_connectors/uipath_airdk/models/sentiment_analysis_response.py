from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.sentiment_analysis_response_usage import (
        SentimentAnalysisResponseUsage,
    )
    from ..models.sentiment_analysis_response_sentiment_analysis import (
        SentimentAnalysisResponseSentimentAnalysis,
    )


T = TypeVar("T", bound="SentimentAnalysisResponse")


@_attrs_define
class SentimentAnalysisResponse:
    """
    Attributes:
        sentiment_analysis (Union[Unset, SentimentAnalysisResponseSentimentAnalysis]):
        usage (Union[Unset, SentimentAnalysisResponseUsage]):
        prompt_tokens (Union[Unset, int]): Tokens generated from the prompt used in sentiment analysis. Example: 577.0.
        model (Union[Unset, str]): The model used for performing sentiment analysis. Example: gpt-4o-2024-05-13.
        id (Union[Unset, str]): A unique identifier for the sentiment analysis request. Example:
            chatcmpl-A2yTgC2UHbkfRAH5wKtYUCK4uQ0bM.
        completion_tokens (Union[Unset, int]): Indicates the count of tokens utilized to complete the analysis. Example:
            301.0.
        method (Union[Unset, str]): Specifies the HTTP method employed for the API call. Example: POST.
        created (Union[Unset, int]): The date and time when the analysis was performed. Example: 1.725272496E9.
        object_ (Union[Unset, str]): The text content that is being analyzed for sentiment. Example: chat.completion.
        total_tokens (Union[Unset, int]): The total count of processed tokens in the text. Example: 878.0.
    """

    sentiment_analysis: Union[Unset, "SentimentAnalysisResponseSentimentAnalysis"] = (
        UNSET
    )
    usage: Union[Unset, "SentimentAnalysisResponseUsage"] = UNSET
    prompt_tokens: Union[Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    completion_tokens: Union[Unset, int] = UNSET
    method: Union[Unset, str] = UNSET
    created: Union[Unset, int] = UNSET
    object_: Union[Unset, str] = UNSET
    total_tokens: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        sentiment_analysis: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sentiment_analysis, Unset):
            sentiment_analysis = self.sentiment_analysis.to_dict()

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        prompt_tokens = self.prompt_tokens

        model = self.model

        id = self.id

        completion_tokens = self.completion_tokens

        method = self.method

        created = self.created

        object_ = self.object_

        total_tokens = self.total_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sentiment_analysis is not UNSET:
            field_dict["sentimentAnalysis"] = sentiment_analysis
        if usage is not UNSET:
            field_dict["usage"] = usage
        if prompt_tokens is not UNSET:
            field_dict["promptTokens"] = prompt_tokens
        if model is not UNSET:
            field_dict["model"] = model
        if id is not UNSET:
            field_dict["id"] = id
        if completion_tokens is not UNSET:
            field_dict["completionTokens"] = completion_tokens
        if method is not UNSET:
            field_dict["method"] = method
        if created is not UNSET:
            field_dict["created"] = created
        if object_ is not UNSET:
            field_dict["object"] = object_
        if total_tokens is not UNSET:
            field_dict["totalTokens"] = total_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.sentiment_analysis_response_usage import (
            SentimentAnalysisResponseUsage,
        )
        from ..models.sentiment_analysis_response_sentiment_analysis import (
            SentimentAnalysisResponseSentimentAnalysis,
        )

        d = src_dict.copy()
        _sentiment_analysis = d.pop("sentimentAnalysis", UNSET)
        sentiment_analysis: Union[Unset, SentimentAnalysisResponseSentimentAnalysis]
        if isinstance(_sentiment_analysis, Unset):
            sentiment_analysis = UNSET
        else:
            sentiment_analysis = SentimentAnalysisResponseSentimentAnalysis.from_dict(
                _sentiment_analysis
            )

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, SentimentAnalysisResponseUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = SentimentAnalysisResponseUsage.from_dict(_usage)

        prompt_tokens = d.pop("promptTokens", UNSET)

        model = d.pop("model", UNSET)

        id = d.pop("id", UNSET)

        completion_tokens = d.pop("completionTokens", UNSET)

        method = d.pop("method", UNSET)

        created = d.pop("created", UNSET)

        object_ = d.pop("object", UNSET)

        total_tokens = d.pop("totalTokens", UNSET)

        sentiment_analysis_response = cls(
            sentiment_analysis=sentiment_analysis,
            usage=usage,
            prompt_tokens=prompt_tokens,
            model=model,
            id=id,
            completion_tokens=completion_tokens,
            method=method,
            created=created,
            object_=object_,
            total_tokens=total_tokens,
        )

        sentiment_analysis_response.additional_properties = d
        return sentiment_analysis_response

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
