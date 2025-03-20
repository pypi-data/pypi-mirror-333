from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.named_entity_recognition_response_entities_output_object_array_item_ref import (
        NamedEntityRecognitionResponseEntitiesOutputObjectArrayItemRef,
    )


T = TypeVar("T", bound="NamedEntityRecognitionResponse")


@_attrs_define
class NamedEntityRecognitionResponse:
    """
    Attributes:
        entities_output (Union[Unset, str]): List of entities recognized by the NER model in the input text Example:
            [{"text":"Apple","type":"Organisation","start":0,"end":5}].
        entities_output_object (Union[Unset, list['NamedEntityRecognitionResponseEntitiesOutputObjectArrayItemRef']]):
    """

    entities_output: Union[Unset, str] = UNSET
    entities_output_object: Union[
        Unset, list["NamedEntityRecognitionResponseEntitiesOutputObjectArrayItemRef"]
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        entities_output = self.entities_output

        entities_output_object: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.entities_output_object, Unset):
            entities_output_object = []
            for componentsschemas_named_entity_recognition_response_entities_output_object_item_data in self.entities_output_object:
                componentsschemas_named_entity_recognition_response_entities_output_object_item = componentsschemas_named_entity_recognition_response_entities_output_object_item_data.to_dict()
                entities_output_object.append(
                    componentsschemas_named_entity_recognition_response_entities_output_object_item
                )

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entities_output is not UNSET:
            field_dict["entitiesOutput"] = entities_output
        if entities_output_object is not UNSET:
            field_dict["entitiesOutputObject"] = entities_output_object

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.named_entity_recognition_response_entities_output_object_array_item_ref import (
            NamedEntityRecognitionResponseEntitiesOutputObjectArrayItemRef,
        )

        d = src_dict.copy()
        entities_output = d.pop("entitiesOutput", UNSET)

        entities_output_object = []
        _entities_output_object = d.pop("entitiesOutputObject", UNSET)
        for componentsschemas_named_entity_recognition_response_entities_output_object_item_data in (
            _entities_output_object or []
        ):
            componentsschemas_named_entity_recognition_response_entities_output_object_item = NamedEntityRecognitionResponseEntitiesOutputObjectArrayItemRef.from_dict(
                componentsschemas_named_entity_recognition_response_entities_output_object_item_data
            )

            entities_output_object.append(
                componentsschemas_named_entity_recognition_response_entities_output_object_item
            )

        named_entity_recognition_response = cls(
            entities_output=entities_output,
            entities_output_object=entities_output_object,
        )

        named_entity_recognition_response.additional_properties = d
        return named_entity_recognition_response

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
