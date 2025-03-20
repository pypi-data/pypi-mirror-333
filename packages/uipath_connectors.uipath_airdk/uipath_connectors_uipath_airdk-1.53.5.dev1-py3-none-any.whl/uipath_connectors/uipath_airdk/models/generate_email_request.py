from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.generate_email_request_output_format import (
    GenerateEmailRequestOutputFormat,
)
from ..models.generate_email_request_output_language import (
    GenerateEmailRequestOutputLanguage,
)
from ..models.generate_email_request_salutation import GenerateEmailRequestSalutation
from ..models.generate_email_request_sign_off import GenerateEmailRequestSignOff
from ..models.generate_email_request_style import GenerateEmailRequestStyle
from typing import Union


T = TypeVar("T", bound="GenerateEmailRequest")


@_attrs_define
class GenerateEmailRequest:
    """
    Attributes:
        need_salutation (bool): Include salutation if needed Example: True.
        need_sign_off (bool): Include sign-off if needed Example: True.
        email_content (str): The content to include in the email. This should be all of the things that must be included
            in the email. Example: Dear team,

            I am pleased to inform you that our project has been successfully completed ahead of schedule. This achievement
            is a testament to your hard work, dedication, and teamwork. I would like to extend my heartfelt gratitude to
            each and every one of you for your contributions and commitment to excellence.

            As we celebrate this milestone, let us continue to strive for excellence in all our endeavors. Together, we can
            overcome any challenge and achieve even greater success in the future.

            Thank you once again for your outstanding efforts.

            Best regards,
            [Your Name].
        salutation_string (Union[Unset, GenerateEmailRequestSalutation]): Type a custom salutation or use a value in the
            dropdown Example: Hello.
        sign_off_string (Union[Unset, GenerateEmailRequestSignOff]): Type a custom sign-off or use a value in the
            dropdown Example: None.
        sign_off_name (Union[Unset, str]): The name to sign-off with.
        total_words (Union[Unset, int]): Approximate number of words to return. If not populated, model will determine
            appropriate length Example: 250.0.
        example (Union[Unset, str]): Example of an email to match style and tone Example: Dear team, I am pleased to
            inform you that our project has been successfully completed ahead of schedule....
        output_format (Union[Unset, GenerateEmailRequestOutputFormat]): The desired format for the generated email
            output. Example: Plain text.
        emailContent (Union[Unset, str]): The content of the email after translation. Example: Esteemed Colleagues,

            It is with immense pride and sincere appreciation that I share with you the remarkable news of our project’s
            early and successful completion. This significant milestone is not just a marker of success, but a resounding
            affirmation of your unparalleled commitment, unwavering dedication, and collaborative spirit which have been
            instrumental in surpassing our collective goals.

            Your individual contributions have coalesced into an extraordinary display of excellence that not only meets but
            exceeds the high standards we set for ourselves. As we take a moment to bask in the glory of our achievement,
            let it also serve as an impetus to continue pushing the boundaries of what we can accomplish. The road ahead is
            laden with opportunities to elevate our collective prowess and to carve out new echelons of success.

            May we take this success as a foundation upon which we will build ever more ambitious projects. Let the
            commendable work ethic and drive seen in this endeavor be the benchmark for all future undertakings. I am
            earnestly grateful for your formidable efforts and I look forward to our continued journey towards excellence.

            Thank you once again for your dedication and for setting a stellar example of teamwork in action.

            Warm regards,
            [Your Name].
        style (Union[Unset, GenerateEmailRequestStyle]): The style of writing to output. Example: Persuasive.
        detect_input_language (Union[Unset, bool]): Detect the language input and either return the email content in the
            same language or a different language
        output_language (Union[Unset, GenerateEmailRequestOutputLanguage]): Language preference for output if not the
            same as input Example: German.
        creativity (Union[Unset, float]): The value of the creativity factor or sampling temperature to use. Higher
            values means the model will take more risks.
        salutation_name (Union[Unset, str]): Name to use with salutation greeting Example: Bubba.
    """

    need_salutation: bool
    need_sign_off: bool
    email_content: str
    salutation_string: Union[Unset, GenerateEmailRequestSalutation] = UNSET
    sign_off_string: Union[Unset, GenerateEmailRequestSignOff] = UNSET
    sign_off_name: Union[Unset, str] = UNSET
    total_words: Union[Unset, int] = UNSET
    example: Union[Unset, str] = UNSET
    output_format: Union[Unset, GenerateEmailRequestOutputFormat] = UNSET
    emailContent: Union[Unset, str] = UNSET
    style: Union[Unset, GenerateEmailRequestStyle] = UNSET
    detect_input_language: Union[Unset, bool] = UNSET
    output_language: Union[Unset, GenerateEmailRequestOutputLanguage] = UNSET
    creativity: Union[Unset, float] = UNSET
    salutation_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        need_salutation = self.need_salutation

        need_sign_off = self.need_sign_off

        email_content = self.email_content

        salutation_string: Union[Unset, str] = UNSET
        if not isinstance(self.salutation_string, Unset):
            salutation_string = self.salutation_string.value

        sign_off_string: Union[Unset, str] = UNSET
        if not isinstance(self.sign_off_string, Unset):
            sign_off_string = self.sign_off_string.value

        sign_off_name = self.sign_off_name

        total_words = self.total_words

        example = self.example

        output_format: Union[Unset, str] = UNSET
        if not isinstance(self.output_format, Unset):
            output_format = self.output_format.value

        emailContent = self.emailContent

        style: Union[Unset, str] = UNSET
        if not isinstance(self.style, Unset):
            style = self.style.value

        detect_input_language = self.detect_input_language

        output_language: Union[Unset, str] = UNSET
        if not isinstance(self.output_language, Unset):
            output_language = self.output_language.value

        creativity = self.creativity

        salutation_name = self.salutation_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "need_salutation": need_salutation,
                "need_sign_off": need_sign_off,
                "email_content": email_content,
            }
        )
        if salutation_string is not UNSET:
            field_dict["salutation_string"] = salutation_string
        if sign_off_string is not UNSET:
            field_dict["sign_off_string"] = sign_off_string
        if sign_off_name is not UNSET:
            field_dict["sign_off_name"] = sign_off_name
        if total_words is not UNSET:
            field_dict["total_words"] = total_words
        if example is not UNSET:
            field_dict["example"] = example
        if output_format is not UNSET:
            field_dict["output_format"] = output_format
        if emailContent is not UNSET:
            field_dict["emailContent"] = emailContent
        if style is not UNSET:
            field_dict["style"] = style
        if detect_input_language is not UNSET:
            field_dict["detectInputLanguage"] = detect_input_language
        if output_language is not UNSET:
            field_dict["outputLanguage"] = output_language
        if creativity is not UNSET:
            field_dict["creativity"] = creativity
        if salutation_name is not UNSET:
            field_dict["salutation_name"] = salutation_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        need_salutation = d.pop("need_salutation")

        need_sign_off = d.pop("need_sign_off")

        email_content = d.pop("email_content")

        _salutation_string = d.pop("salutation_string", UNSET)
        salutation_string: Union[Unset, GenerateEmailRequestSalutation]
        if isinstance(_salutation_string, Unset):
            salutation_string = UNSET
        else:
            salutation_string = GenerateEmailRequestSalutation(_salutation_string)

        _sign_off_string = d.pop("sign_off_string", UNSET)
        sign_off_string: Union[Unset, GenerateEmailRequestSignOff]
        if isinstance(_sign_off_string, Unset):
            sign_off_string = UNSET
        else:
            sign_off_string = GenerateEmailRequestSignOff(_sign_off_string)

        sign_off_name = d.pop("sign_off_name", UNSET)

        total_words = d.pop("total_words", UNSET)

        example = d.pop("example", UNSET)

        _output_format = d.pop("output_format", UNSET)
        output_format: Union[Unset, GenerateEmailRequestOutputFormat]
        if isinstance(_output_format, Unset):
            output_format = UNSET
        else:
            output_format = GenerateEmailRequestOutputFormat(_output_format)

        emailContent = d.pop("emailContent", UNSET)

        _style = d.pop("style", UNSET)
        style: Union[Unset, GenerateEmailRequestStyle]
        if isinstance(_style, Unset):
            style = UNSET
        else:
            style = GenerateEmailRequestStyle(_style)

        detect_input_language = d.pop("detectInputLanguage", UNSET)

        _output_language = d.pop("outputLanguage", UNSET)
        output_language: Union[Unset, GenerateEmailRequestOutputLanguage]
        if isinstance(_output_language, Unset):
            output_language = UNSET
        else:
            output_language = GenerateEmailRequestOutputLanguage(_output_language)

        creativity = d.pop("creativity", UNSET)

        salutation_name = d.pop("salutation_name", UNSET)

        generate_email_request = cls(
            need_salutation=need_salutation,
            need_sign_off=need_sign_off,
            email_content=email_content,
            salutation_string=salutation_string,
            sign_off_string=sign_off_string,
            sign_off_name=sign_off_name,
            total_words=total_words,
            example=example,
            output_format=output_format,
            emailContent=emailContent,
            style=style,
            detect_input_language=detect_input_language,
            output_language=output_language,
            creativity=creativity,
            salutation_name=salutation_name,
        )

        generate_email_request.additional_properties = d
        return generate_email_request

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
