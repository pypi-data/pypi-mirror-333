from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="TranslateResponse")


@_attrs_define
class TranslateResponse:
    """
    Attributes:
        translated_text (Union[Unset, str]): The translated text. Where supported, the output will be transliterated
            into the appropriate script or alphabet. Example: In der jüngsten Zeit wird eine immense Begeisterung für
            technologischen Fortschritt beobachtet, und es ist wie ein Morgentraum, dass künstliche Intelligenz nun tief in
            jeden Bereich unseres täglichen Lebens eindringt. Von Smartphones bis zu Smart Homes, von virtueller Realität
            bis zu selbstfahrenden Autos, die AI-Technologie verändert unsere Lebensweise und Art zu arbeiten. Während AI
            viele Annehmlichkeiten und Möglichkeiten mit sich bringt, bringt sie auch einige Herausforderungen und Probleme
            mit sich. Wir müssen wachsam bleiben, um den positiven Einfluss der AI-Technologie auf die Gesellschaft zu
            gewährleisten..
    """

    translated_text: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        translated_text = self.translated_text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if translated_text is not UNSET:
            field_dict["translatedText"] = translated_text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        translated_text = d.pop("translatedText", UNSET)

        translate_response = cls(
            translated_text=translated_text,
        )

        translate_response.additional_properties = d
        return translate_response

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
