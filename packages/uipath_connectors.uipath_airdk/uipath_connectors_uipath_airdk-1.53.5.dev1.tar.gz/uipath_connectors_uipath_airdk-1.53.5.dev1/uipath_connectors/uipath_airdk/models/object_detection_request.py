from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.object_detection_request_entities import (
        ObjectDetectionRequestEntities,
    )
    from ..models.object_detection_request_additional_instructions_for_detection import (
        ObjectDetectionRequestAdditionalInstructionsForDetection,
    )


T = TypeVar("T", bound="ObjectDetectionRequest")


@_attrs_define
class ObjectDetectionRequest:
    """
    Attributes:
        entities (ObjectDetectionRequestEntities): Entity name and description to search the image for
        additional_instructions (Union[Unset, ObjectDetectionRequestAdditionalInstructionsForDetection]): Optional
            instructions to refine the object detection process.
    """

    entities: "ObjectDetectionRequestEntities"
    additional_instructions: Union[
        Unset, "ObjectDetectionRequestAdditionalInstructionsForDetection"
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        entities = self.entities.to_dict()

        additional_instructions: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.additional_instructions, Unset):
            additional_instructions = self.additional_instructions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entities": entities,
            }
        )
        if additional_instructions is not UNSET:
            field_dict["additionalInstructions"] = additional_instructions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.object_detection_request_entities import (
            ObjectDetectionRequestEntities,
        )
        from ..models.object_detection_request_additional_instructions_for_detection import (
            ObjectDetectionRequestAdditionalInstructionsForDetection,
        )

        d = src_dict.copy()
        entities = ObjectDetectionRequestEntities.from_dict(d.pop("entities"))

        _additional_instructions = d.pop("additionalInstructions", UNSET)
        additional_instructions: Union[
            Unset, ObjectDetectionRequestAdditionalInstructionsForDetection
        ]
        if isinstance(_additional_instructions, Unset):
            additional_instructions = UNSET
        else:
            additional_instructions = (
                ObjectDetectionRequestAdditionalInstructionsForDetection.from_dict(
                    _additional_instructions
                )
            )

        object_detection_request = cls(
            entities=entities,
            additional_instructions=additional_instructions,
        )

        object_detection_request.additional_properties = d
        return object_detection_request

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
