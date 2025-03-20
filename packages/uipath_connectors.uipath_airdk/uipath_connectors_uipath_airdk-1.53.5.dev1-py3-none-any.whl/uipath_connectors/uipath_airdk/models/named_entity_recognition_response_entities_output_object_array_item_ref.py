from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="NamedEntityRecognitionResponseEntitiesOutputObjectArrayItemRef")


@_attrs_define
class NamedEntityRecognitionResponseEntitiesOutputObjectArrayItemRef:
    """
    Attributes:
        type_ (Union[Unset, str]): The category or class of the recognized entity Example: Organisation.
        text (Union[Unset, str]): The actual text of the entity that was recognized Example: Apple.
    """

    type_: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = d.pop("type", UNSET)

        text = d.pop("text", UNSET)

        named_entity_recognition_response_entities_output_object_array_item_ref = cls(
            type_=type_,
            text=text,
        )

        named_entity_recognition_response_entities_output_object_array_item_ref.additional_properties = d
        return named_entity_recognition_response_entities_output_object_array_item_ref

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
