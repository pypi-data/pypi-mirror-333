from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field



if TYPE_CHECKING:
    from ..models.named_entity_recognition_request_entities import (
        NamedEntityRecognitionRequestEntities,
    )


T = TypeVar("T", bound="NamedEntityRecognitionRequest")


@_attrs_define
class NamedEntityRecognitionRequest:
    """
    Attributes:
        entities (NamedEntityRecognitionRequestEntities): The list of entities and their descriptions to search the text
            for
        text (str): The text to analyze for named entities Example: Apple is planning to build a new data center in
            Arizona, which will create 2,000 jobs. The company is also investing $2 billion in the project..
    """

    entities: "NamedEntityRecognitionRequestEntities"
    text: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        entities = self.entities.to_dict()

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entities": entities,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.named_entity_recognition_request_entities import (
            NamedEntityRecognitionRequestEntities,
        )

        d = src_dict.copy()
        entities = NamedEntityRecognitionRequestEntities.from_dict(d.pop("entities"))

        text = d.pop("text")

        named_entity_recognition_request = cls(
            entities=entities,
            text=text,
        )

        named_entity_recognition_request.additional_properties = d
        return named_entity_recognition_request

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
