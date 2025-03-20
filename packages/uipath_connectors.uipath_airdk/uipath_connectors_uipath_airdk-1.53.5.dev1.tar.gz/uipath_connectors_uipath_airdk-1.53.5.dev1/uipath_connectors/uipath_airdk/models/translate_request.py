from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.translate_request_language import TranslateRequestLanguage


T = TypeVar("T", bound="TranslateRequest")


@_attrs_define
class TranslateRequest:
    """
    Attributes:
        input_text (str): Text to be translated. Example: हाल के युग में तकनीकी प्रगति का विशाल उत्साह देखने को मिल रहा
            है, और एक सुबह का सपना है कि आर्टिफिशियल इंटेलिजेंस अब हमारे दैनिक जीवन के हर क्षेत्र में गहराई से प्रवेश कर रही
            है। स्मार्टफोन से स्मार्ट होम, वर्चुअल रियलिटी से स्वयं चलने वाली गाड़ियों तक, एआई तकनीक हमारे जीवनशैली और काम
            के तरीके को बदल रही है। जबकि एआई कई सुविधाएँ और अवसर लाती है, वह कुछ चुनौतियों और समस्याओं को भी साथ में लाती
            है। हमें समाज पर एआई प्रौद्योगिकी के सकारात्मक प्रभाव को सुनिश्चित करने के लिए सतर्क रहना चाहिए।, रहना चाहिए।.
        language (TranslateRequestLanguage): Specify language to be translated to. Example: German.
    """

    input_text: str
    language: TranslateRequestLanguage
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_text = self.input_text

        language = self.language.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputText": input_text,
                "language": language,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        input_text = d.pop("inputText")

        language = TranslateRequestLanguage(d.pop("language"))

        translate_request = cls(
            input_text=input_text,
            language=language,
        )

        translate_request.additional_properties = d
        return translate_request

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
