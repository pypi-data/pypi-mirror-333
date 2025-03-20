from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.summarise_text_new_request_output_language import (
    SummariseTextNewRequestOutputLanguage,
)
from ..models.summarise_text_new_request_summary_format import (
    SummariseTextNewRequestSummaryFormat,
)
from typing import Union


T = TypeVar("T", bound="SummariseTextNewRequest")


@_attrs_define
class SummariseTextNewRequest:
    """
    Attributes:
        prompt (str): The text to summarize Example: If requestBody['instruction'] is an empty string, null, or
            undefined, the result of the expression if(requestBody['instruction']) will be false.In JavaScript, empty
            strings, null, and undefined are considered falsy values. Therefore, the condition
            if(requestBody['instruction']) will evaluate to false if requestBody['instruction'] is any of these falsy
            values, and the code block within the if statement will not be executed..
        summary_format (Union[Unset, SummariseTextNewRequestSummaryFormat]): The format for the generated summarized
            text, e.g., organized in paragraph form or as a bulleted item list, etc. Example: paragraph.
        max_word_count (Union[Unset, int]): The maximum word count for the summary of the provided text. If not
            populated, model will determine appropriate length
        temperature (Union[Unset, float]): A number between 0.0 and 2.0 indicating the creativity factor or sampling
            temperature to use. Higher values means the model will be more creative with the summarization, but also take
            more risks, which could lead to more variance from the input text to summarize. Defaults to 0.5
        detect_input_language (Union[Unset, bool]): Detect the language input and either return the summary in the same
            language or a different language
        output_language (Union[Unset, SummariseTextNewRequestOutputLanguage]): Language preference for output if not the
            same as input Example: German.
    """

    prompt: str
    summary_format: Union[Unset, SummariseTextNewRequestSummaryFormat] = UNSET
    max_word_count: Union[Unset, int] = UNSET
    temperature: Union[Unset, float] = UNSET
    detect_input_language: Union[Unset, bool] = UNSET
    output_language: Union[Unset, SummariseTextNewRequestOutputLanguage] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        summary_format: Union[Unset, str] = UNSET
        if not isinstance(self.summary_format, Unset):
            summary_format = self.summary_format.value

        max_word_count = self.max_word_count

        temperature = self.temperature

        detect_input_language = self.detect_input_language

        output_language: Union[Unset, str] = UNSET
        if not isinstance(self.output_language, Unset):
            output_language = self.output_language.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if summary_format is not UNSET:
            field_dict["summaryFormat"] = summary_format
        if max_word_count is not UNSET:
            field_dict["maxWordCount"] = max_word_count
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if detect_input_language is not UNSET:
            field_dict["detectInputLanguage"] = detect_input_language
        if output_language is not UNSET:
            field_dict["outputLanguage"] = output_language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        _summary_format = d.pop("summaryFormat", UNSET)
        summary_format: Union[Unset, SummariseTextNewRequestSummaryFormat]
        if isinstance(_summary_format, Unset):
            summary_format = UNSET
        else:
            summary_format = SummariseTextNewRequestSummaryFormat(_summary_format)

        max_word_count = d.pop("maxWordCount", UNSET)

        temperature = d.pop("temperature", UNSET)

        detect_input_language = d.pop("detectInputLanguage", UNSET)

        _output_language = d.pop("outputLanguage", UNSET)
        output_language: Union[Unset, SummariseTextNewRequestOutputLanguage]
        if isinstance(_output_language, Unset):
            output_language = UNSET
        else:
            output_language = SummariseTextNewRequestOutputLanguage(_output_language)

        summarise_text_new_request = cls(
            prompt=prompt,
            summary_format=summary_format,
            max_word_count=max_word_count,
            temperature=temperature,
            detect_input_language=detect_input_language,
            output_language=output_language,
        )

        summarise_text_new_request.additional_properties = d
        return summarise_text_new_request

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
