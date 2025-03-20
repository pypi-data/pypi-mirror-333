from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.signature_similarity_response_usage import (
        SignatureSimilarityResponseUsage,
    )


T = TypeVar("T", bound="SignatureSimilarityResponse")


@_attrs_define
class SignatureSimilarityResponse:
    """
    Attributes:
        usage (Union[Unset, SignatureSimilarityResponseUsage]):
        created (Union[Unset, int]): The date and time when the analysis was performed. Example: 1.72542702E9.
        reasoning (Union[Unset, str]): The explanation of how the conclusion was reached Example: Both images contain
            signatures. The overall appearance of the two signatures, including size, slant, and spacing, matches closely.
            Specific characteristics such as line quality appear consistent, with smooth and slightly variable pressure. The
            speed seems to be fast and steady in both signatures. The formation and proportion of letters, especially in 'P'
            and 'esch' parts, are similar, with minor variations in beginning and ending strokes, which are normal. The
            connections between letters and the unique identifiers align well in both signatures..
        total_tokens (Union[Unset, int]): The total number of tokens processed in the request. Example: 1948.0.
        score (Union[Unset, str]): A score between 0 and 100 indicating the similarity of the signatures Example: 85.
        prompt_tokens (Union[Unset, int]): The number of tokens used in the input prompt. Example: 1798.0.
        model (Union[Unset, str]): The unique identifier of the AI model used. Example: gpt-4o-2024-05-13.
        id (Union[Unset, str]): The unique identifier of the API request. Example:
            chatcmpl-A3cg08k2zVTkMu7v68WWLaxmq9qLu.
        completion_tokens (Union[Unset, int]): The number of tokens used to complete the analysis. Example: 150.0.
        object_ (Union[Unset, str]): The detailed information of the object analyzed for similarity. Example:
            chat.completion.
    """

    usage: Union[Unset, "SignatureSimilarityResponseUsage"] = UNSET
    created: Union[Unset, int] = UNSET
    reasoning: Union[Unset, str] = UNSET
    total_tokens: Union[Unset, int] = UNSET
    score: Union[Unset, str] = UNSET
    prompt_tokens: Union[Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    completion_tokens: Union[Unset, int] = UNSET
    object_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        created = self.created

        reasoning = self.reasoning

        total_tokens = self.total_tokens

        score = self.score

        prompt_tokens = self.prompt_tokens

        model = self.model

        id = self.id

        completion_tokens = self.completion_tokens

        object_ = self.object_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if usage is not UNSET:
            field_dict["usage"] = usage
        if created is not UNSET:
            field_dict["created"] = created
        if reasoning is not UNSET:
            field_dict["reasoning"] = reasoning
        if total_tokens is not UNSET:
            field_dict["totalTokens"] = total_tokens
        if score is not UNSET:
            field_dict["score"] = score
        if prompt_tokens is not UNSET:
            field_dict["promptTokens"] = prompt_tokens
        if model is not UNSET:
            field_dict["model"] = model
        if id is not UNSET:
            field_dict["id"] = id
        if completion_tokens is not UNSET:
            field_dict["completionTokens"] = completion_tokens
        if object_ is not UNSET:
            field_dict["object"] = object_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.signature_similarity_response_usage import (
            SignatureSimilarityResponseUsage,
        )

        d = src_dict.copy()
        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, SignatureSimilarityResponseUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = SignatureSimilarityResponseUsage.from_dict(_usage)

        created = d.pop("created", UNSET)

        reasoning = d.pop("reasoning", UNSET)

        total_tokens = d.pop("totalTokens", UNSET)

        score = d.pop("score", UNSET)

        prompt_tokens = d.pop("promptTokens", UNSET)

        model = d.pop("model", UNSET)

        id = d.pop("id", UNSET)

        completion_tokens = d.pop("completionTokens", UNSET)

        object_ = d.pop("object", UNSET)

        signature_similarity_response = cls(
            usage=usage,
            created=created,
            reasoning=reasoning,
            total_tokens=total_tokens,
            score=score,
            prompt_tokens=prompt_tokens,
            model=model,
            id=id,
            completion_tokens=completion_tokens,
            object_=object_,
        )

        signature_similarity_response.additional_properties = d
        return signature_similarity_response

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
