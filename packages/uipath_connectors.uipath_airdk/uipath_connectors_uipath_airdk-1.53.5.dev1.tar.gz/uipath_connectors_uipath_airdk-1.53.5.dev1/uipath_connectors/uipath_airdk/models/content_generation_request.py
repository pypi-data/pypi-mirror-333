from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.content_generation_request_context_grounding import (
    ContentGenerationRequestContextGrounding,
)
from ..models.content_generation_request_pii_language import (
    ContentGenerationRequestPIILanguage,
)
from ..models.content_generation_request_piiphi_category import (
    ContentGenerationRequestPIIPHICategory,
)
from typing import Union


T = TypeVar("T", bound="ContentGenerationRequest")


@_attrs_define
class ContentGenerationRequest:
    """
    Attributes:
        prompt (str): The user prompt for the chat completion request Example: Which organization holds the leading
            position in the field of Robotic Process Automation (RPA)?.
        max_tokens (Union[Unset, int]): The maximum number of tokens to generate in the completion.  The token count of
            your prompt plus those from the result/completion cannot exceed the value provided for this field. It's best to
            set this value to be a less than the model maximum count so as to have some room for the prompt token count.
            Example: 50.0.
        presence_penalty (Union[Unset, int]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
            whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Defaults to
            0 Example: 1.0.
        n (Union[Unset, int]): The number of completion choices to generate for the request. The higher the value of
            this field, the more the number of tokens that will get used, and hence will result in a higher cost, so the
            user needs to be aware of that when setting the value of this field. Defaults to 1 Example: 1.0.
        stop (Union[Unset, str]): Up to 4 sequences where the API will stop generating further tokens. The returned text
            will not contain the stop sequence. Defaults to null.
        top_p (Union[Unset, int]): A number between 0 and 1.  The lower the number, the fewer tokens are considered.
            Defaults to 1 Example: 1.0.
        topP (Union[Unset, float]): A number between 0 and 1.  The lower the number, the lesser the randomness. Defaults
            to 0.8. Example: 0.8.
        top_k (Union[Unset, int]): A number between 1 and 40.  The higher the number the higher the diversity of
            generated text. Defaults to 40. Example: 40.0.
        frequency_penalty (Union[Unset, int]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
            their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
            Defaults to 0 Example: 1.0.
        instruction (Union[Unset, str]): The system prompt or context instruction of the chat completion request
            Example: You are a informational provider.
        temperature (Union[Unset, float]): The value of the creativity factor or sampling temperature to use. Higher
            values means the model will take more risks. Try 0.9 for more creative responses or completions, and 0 (also
            called argmax sampling) for ones with a well-defined or more exact answer.  The general recommendation is to
            alter, from the default value, this or the Nucleus Sample value, but not both values. Defaults to 1
        is_pii_enabled (Union[Unset, bool]): Whether to detect PII from the input prompt.  Defaults to false.
        is_filter_pii_enabled (Union[Unset, bool]): If set to true, any detected PII/PHI will be masked before sending
            to the LLM. If false, detected PII will be included in the prompt.  In both cases, the detected PII will be
            available in the output.  Note that if set to true the quality of the output may be impacted.
        language_code (Union[Unset, ContentGenerationRequestPIILanguage]): The language of the prompt input and output
            to scan for PII.
        pii_entity_categories (Union[Unset, list[ContentGenerationRequestPIIPHICategory]]):
        confidence_threshold (Union[Unset, float]): The minimum confidence score required in order to qualify as PII and
            be redacted Example: 0.5.
        context_grounding (Union[Unset, ContentGenerationRequestContextGrounding]): Ground the prompt in context to
            increase quality and accuracy of the output.  This feature allows users to insert proprietary business logic and
            knowledge into the prompt.  If selected, users can reference an Orchestrator Bucket where documents have been
            uploaded or upload a file directly for one time use.
        index_id (Union[Unset, str]): Name or ID of the index to ground the prompt in Example: None.
        number_of_results (Union[Unset, int]): Indicates the number of results to be returned. Example: 1.0.
    """

    prompt: str
    max_tokens: Union[Unset, int] = UNSET
    presence_penalty: Union[Unset, int] = UNSET
    n: Union[Unset, int] = UNSET
    stop: Union[Unset, str] = UNSET
    top_p: Union[Unset, int] = UNSET
    topP: Union[Unset, float] = UNSET
    top_k: Union[Unset, int] = UNSET
    frequency_penalty: Union[Unset, int] = UNSET
    instruction: Union[Unset, str] = UNSET
    temperature: Union[Unset, float] = UNSET
    is_pii_enabled: Union[Unset, bool] = UNSET
    is_filter_pii_enabled: Union[Unset, bool] = UNSET
    language_code: Union[Unset, ContentGenerationRequestPIILanguage] = UNSET
    pii_entity_categories: Union[
        Unset, list[ContentGenerationRequestPIIPHICategory]
    ] = UNSET
    confidence_threshold: Union[Unset, float] = UNSET
    context_grounding: Union[Unset, ContentGenerationRequestContextGrounding] = UNSET
    index_id: Union[Unset, str] = UNSET
    number_of_results: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        max_tokens = self.max_tokens

        presence_penalty = self.presence_penalty

        n = self.n

        stop = self.stop

        top_p = self.top_p

        topP = self.topP

        top_k = self.top_k

        frequency_penalty = self.frequency_penalty

        instruction = self.instruction

        temperature = self.temperature

        is_pii_enabled = self.is_pii_enabled

        is_filter_pii_enabled = self.is_filter_pii_enabled

        language_code: Union[Unset, str] = UNSET
        if not isinstance(self.language_code, Unset):
            language_code = self.language_code.value

        pii_entity_categories: Union[Unset, list[str]] = UNSET
        if not isinstance(self.pii_entity_categories, Unset):
            pii_entity_categories = []
            for pii_entity_categories_item_data in self.pii_entity_categories:
                pii_entity_categories_item = pii_entity_categories_item_data.value
                pii_entity_categories.append(pii_entity_categories_item)

        confidence_threshold = self.confidence_threshold

        context_grounding: Union[Unset, str] = UNSET
        if not isinstance(self.context_grounding, Unset):
            context_grounding = self.context_grounding.value

        index_id = self.index_id

        number_of_results = self.number_of_results

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if presence_penalty is not UNSET:
            field_dict["presence_penalty"] = presence_penalty
        if n is not UNSET:
            field_dict["n"] = n
        if stop is not UNSET:
            field_dict["stop"] = stop
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if topP is not UNSET:
            field_dict["topP"] = topP
        if top_k is not UNSET:
            field_dict["topK"] = top_k
        if frequency_penalty is not UNSET:
            field_dict["frequency_penalty"] = frequency_penalty
        if instruction is not UNSET:
            field_dict["instruction"] = instruction
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if is_pii_enabled is not UNSET:
            field_dict["isPIIEnabled"] = is_pii_enabled
        if is_filter_pii_enabled is not UNSET:
            field_dict["isFilterPIIEnabled"] = is_filter_pii_enabled
        if language_code is not UNSET:
            field_dict["languageCode"] = language_code
        if pii_entity_categories is not UNSET:
            field_dict["piiEntityCategories"] = pii_entity_categories
        if confidence_threshold is not UNSET:
            field_dict["confidenceThreshold"] = confidence_threshold
        if context_grounding is not UNSET:
            field_dict["contextGrounding"] = context_grounding
        if index_id is not UNSET:
            field_dict["indexID"] = index_id
        if number_of_results is not UNSET:
            field_dict["numberOfResults"] = number_of_results

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        max_tokens = d.pop("max_tokens", UNSET)

        presence_penalty = d.pop("presence_penalty", UNSET)

        n = d.pop("n", UNSET)

        stop = d.pop("stop", UNSET)

        top_p = d.pop("top_p", UNSET)

        topP = d.pop("topP", UNSET)

        top_k = d.pop("topK", UNSET)

        frequency_penalty = d.pop("frequency_penalty", UNSET)

        instruction = d.pop("instruction", UNSET)

        temperature = d.pop("temperature", UNSET)

        is_pii_enabled = d.pop("isPIIEnabled", UNSET)

        is_filter_pii_enabled = d.pop("isFilterPIIEnabled", UNSET)

        _language_code = d.pop("languageCode", UNSET)
        language_code: Union[Unset, ContentGenerationRequestPIILanguage]
        if isinstance(_language_code, Unset):
            language_code = UNSET
        else:
            language_code = ContentGenerationRequestPIILanguage(_language_code)

        pii_entity_categories = []
        _pii_entity_categories = d.pop("piiEntityCategories", UNSET)
        for pii_entity_categories_item_data in _pii_entity_categories or []:
            pii_entity_categories_item = ContentGenerationRequestPIIPHICategory(
                pii_entity_categories_item_data
            )

            pii_entity_categories.append(pii_entity_categories_item)

        confidence_threshold = d.pop("confidenceThreshold", UNSET)

        _context_grounding = d.pop("contextGrounding", UNSET)
        context_grounding: Union[Unset, ContentGenerationRequestContextGrounding]
        if isinstance(_context_grounding, Unset):
            context_grounding = UNSET
        else:
            context_grounding = ContentGenerationRequestContextGrounding(
                _context_grounding
            )

        index_id = d.pop("indexID", UNSET)

        number_of_results = d.pop("numberOfResults", UNSET)

        content_generation_request = cls(
            prompt=prompt,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            n=n,
            stop=stop,
            top_p=top_p,
            topP=topP,
            top_k=top_k,
            frequency_penalty=frequency_penalty,
            instruction=instruction,
            temperature=temperature,
            is_pii_enabled=is_pii_enabled,
            is_filter_pii_enabled=is_filter_pii_enabled,
            language_code=language_code,
            pii_entity_categories=pii_entity_categories,
            confidence_threshold=confidence_threshold,
            context_grounding=context_grounding,
            index_id=index_id,
            number_of_results=number_of_results,
        )

        content_generation_request.additional_properties = d
        return content_generation_request

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
