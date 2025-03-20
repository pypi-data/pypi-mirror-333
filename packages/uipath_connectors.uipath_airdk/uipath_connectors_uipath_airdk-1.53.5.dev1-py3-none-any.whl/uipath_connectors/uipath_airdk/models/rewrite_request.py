from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.rewrite_request_output_language import RewriteRequestOutputLanguage
from typing import Union


T = TypeVar("T", bound="RewriteRequest")


@_attrs_define
class RewriteRequest:
    """
    Attributes:
        content_to_rewrite (str): Enter the text content you want to be rewritten Example: Protocol Buffers, also known
            as protobuf, is a method for serializing structured data. It's developed by Google and is used extensively
            within Google for communication between internal services and for data storage. It's designed to be language-
            neutral, platform-neutral, and extensible. At its core, Protocol Buffers defines a language-independent,
            platform-neutral format for serializing structured data. It allows you to define the structure of your data in a
            language-neutral way using a simple interface description language (IDL), and then generate code in various
            programming languages to easily serialize and deserialize data in that format. Key features of Protocol Buffers
            include: Language Independence: You can define your data structures in a .proto file using Protocol Buffers'
            Interface Definition Language (IDL), and then use code generation tools to generate code in multiple programming
            languages. This makes it easy to work with structured data across different programming languages and platforms.
            Efficiency: Protocol Buffers uses a binary serialization format that is more compact and efficient compared to
            text-based formats like JSON or XML. This results in smaller message sizes, faster serialization and
            deserialization, and reduced network and storage overhead. Extensibility: Protocol Buffers supports schema
            evolution, allowing you to evolve your data schema over time without breaking backward compatibility. You can
            add new fields, remove existing fields, and make other changes to your data schema while ensuring that older
            clients can still read messages serialized with the newer schema. Cross-Platform Support: Protocol Buffers
            supports a wide range of programming languages, including C++, Java, Python, Go, and more. This makes it easy to
            integrate Protocol Buffers into your existing projects and work with structured data across different platforms.
            Overall, Protocol Buffers provides a flexible, efficient, and language-independent way to serialize structured
            data, making it ideal for use cases such as inter-service communication, data storage, and API serialization..
        output_language (Union[Unset, RewriteRequestOutputLanguage]): Language preference for output if not the same as
            input Example: German.
        detect_input_language (Union[Unset, bool]): Detect the language input and either return the rewrite in the same
            language or a different language
        total_words (Union[Unset, int]): The total count of words in the output text. If not populated, model will
            determine appropriate length Example: 30.0.
        example (Union[Unset, str]): A sample of rewritten content that helps identify appropriate style and tone
        temperature (Union[Unset, float]): Determines the level of creativity applied to the output. A value of 0
            indicates minimal creativity, sticking closely to the original content, while a value of 1 encourages maximum
            creativity, potentially introducing more novel rephrasings. Adjust this setting based on how closely you want
            the output to adhere to the input.
        rewrite_instructions (Union[Unset, str]): Style guidelines for rewrite. This should be concise and focus on
            things like tone, audience, purpose, etc. Example: Rewrite in a more engaging and informative style, using
            simpler terms and focusing on key insights..
    """

    content_to_rewrite: str
    output_language: Union[Unset, RewriteRequestOutputLanguage] = UNSET
    detect_input_language: Union[Unset, bool] = UNSET
    total_words: Union[Unset, int] = UNSET
    example: Union[Unset, str] = UNSET
    temperature: Union[Unset, float] = UNSET
    rewrite_instructions: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_to_rewrite = self.content_to_rewrite

        output_language: Union[Unset, str] = UNSET
        if not isinstance(self.output_language, Unset):
            output_language = self.output_language.value

        detect_input_language = self.detect_input_language

        total_words = self.total_words

        example = self.example

        temperature = self.temperature

        rewrite_instructions = self.rewrite_instructions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_to_rewrite": content_to_rewrite,
            }
        )
        if output_language is not UNSET:
            field_dict["outputLanguage"] = output_language
        if detect_input_language is not UNSET:
            field_dict["detectInputLanguage"] = detect_input_language
        if total_words is not UNSET:
            field_dict["total_words"] = total_words
        if example is not UNSET:
            field_dict["example"] = example
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if rewrite_instructions is not UNSET:
            field_dict["rewrite_instructions"] = rewrite_instructions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        content_to_rewrite = d.pop("content_to_rewrite")

        _output_language = d.pop("outputLanguage", UNSET)
        output_language: Union[Unset, RewriteRequestOutputLanguage]
        if isinstance(_output_language, Unset):
            output_language = UNSET
        else:
            output_language = RewriteRequestOutputLanguage(_output_language)

        detect_input_language = d.pop("detectInputLanguage", UNSET)

        total_words = d.pop("total_words", UNSET)

        example = d.pop("example", UNSET)

        temperature = d.pop("temperature", UNSET)

        rewrite_instructions = d.pop("rewrite_instructions", UNSET)

        rewrite_request = cls(
            content_to_rewrite=content_to_rewrite,
            output_language=output_language,
            detect_input_language=detect_input_language,
            total_words=total_words,
            example=example,
            temperature=temperature,
            rewrite_instructions=rewrite_instructions,
        )

        rewrite_request.additional_properties = d
        return rewrite_request

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
