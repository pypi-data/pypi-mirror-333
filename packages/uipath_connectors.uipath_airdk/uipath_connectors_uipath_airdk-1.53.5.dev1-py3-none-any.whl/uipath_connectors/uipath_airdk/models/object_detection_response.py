from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.object_detection_response_choices_array_item_ref import (
        ObjectDetectionResponseChoicesArrayItemRef,
    )
    from ..models.object_detection_response_usage import ObjectDetectionResponseUsage
    from ..models.object_detection_response_detected_objects_array_item_ref import (
        ObjectDetectionResponseDetectedObjectsArrayItemRef,
    )


T = TypeVar("T", bound="ObjectDetectionResponse")


@_attrs_define
class ObjectDetectionResponse:
    """
    Attributes:
        choices (Union[Unset, list['ObjectDetectionResponseChoicesArrayItemRef']]):
        usage (Union[Unset, ObjectDetectionResponseUsage]):
        prompt_tokens (Union[Unset, int]): Specifies the count of tokens used in the prompt. Example: 874.0.
        model (Union[Unset, str]): The AI model used for detecting objects. Example: gpt-4o-2024-05-13.
        id (Union[Unset, str]): A unique identifier for the detection request. Example:
            chatcmpl-9zJq77Je0RCy4tpS1BhLmwrlijjXl.
        text (Union[Unset, str]): The textual description of the detected object. Example: {
              "detected_entities": [
                {
                  "name": "Package",
                  "detected": "Yes",
                  "details": "Multiple packages are placed in front of the doorstep, clearly visible and accessible."
                },
                {
                  "name": "Doorstep",
                  "detected": "No",
                  "details": "The doorstep is partially blocked by multiple packages."
                }
              ]
            }.
        completion_tokens (Union[Unset, int]): The count of tokens used to complete the object detection task. Example:
            84.0.
        created (Union[Unset, int]): The date and time when the object detection task was created. Example:
            1.724401299E9.
        total_tokens (Union[Unset, int]): The total number of tokens consumed by the object detection task. Example:
            958.0.
        detected_objects (Union[Unset, list['ObjectDetectionResponseDetectedObjectsArrayItemRef']]):
        detected_object_names (Union[Unset, list[str]]):  Example: Package.
        detected_objects_string (Union[Unset, str]): Array of entities detected Example:
            [{"name":"Package","detected":"Yes","details":"Multiple packages are placed in front of the doorstep, clearly
            visible and accessible."},{"name":"Doorstep","detected":"No","details":"The doorstep is partially blocked by
            multiple packages."}].
        object_ (Union[Unset, str]): The specific object that the detection algorithm should look for. Example:
            chat.completion.
    """

    choices: Union[Unset, list["ObjectDetectionResponseChoicesArrayItemRef"]] = UNSET
    usage: Union[Unset, "ObjectDetectionResponseUsage"] = UNSET
    prompt_tokens: Union[Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    completion_tokens: Union[Unset, int] = UNSET
    created: Union[Unset, int] = UNSET
    total_tokens: Union[Unset, int] = UNSET
    detected_objects: Union[
        Unset, list["ObjectDetectionResponseDetectedObjectsArrayItemRef"]
    ] = UNSET
    detected_object_names: Union[Unset, list[str]] = UNSET
    detected_objects_string: Union[Unset, str] = UNSET
    object_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        choices: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.choices, Unset):
            choices = []
            for (
                componentsschemas_object_detection_response_choices_item_data
            ) in self.choices:
                componentsschemas_object_detection_response_choices_item = componentsschemas_object_detection_response_choices_item_data.to_dict()
                choices.append(componentsschemas_object_detection_response_choices_item)

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        prompt_tokens = self.prompt_tokens

        model = self.model

        id = self.id

        text = self.text

        completion_tokens = self.completion_tokens

        created = self.created

        total_tokens = self.total_tokens

        detected_objects: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.detected_objects, Unset):
            detected_objects = []
            for (
                componentsschemas_object_detection_response_detected_objects_item_data
            ) in self.detected_objects:
                componentsschemas_object_detection_response_detected_objects_item = componentsschemas_object_detection_response_detected_objects_item_data.to_dict()
                detected_objects.append(
                    componentsschemas_object_detection_response_detected_objects_item
                )

        detected_object_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.detected_object_names, Unset):
            detected_object_names = self.detected_object_names

        detected_objects_string = self.detected_objects_string

        object_ = self.object_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if choices is not UNSET:
            field_dict["choices"] = choices
        if usage is not UNSET:
            field_dict["usage"] = usage
        if prompt_tokens is not UNSET:
            field_dict["promptTokens"] = prompt_tokens
        if model is not UNSET:
            field_dict["model"] = model
        if id is not UNSET:
            field_dict["id"] = id
        if text is not UNSET:
            field_dict["text"] = text
        if completion_tokens is not UNSET:
            field_dict["completionTokens"] = completion_tokens
        if created is not UNSET:
            field_dict["created"] = created
        if total_tokens is not UNSET:
            field_dict["totalTokens"] = total_tokens
        if detected_objects is not UNSET:
            field_dict["detectedObjects"] = detected_objects
        if detected_object_names is not UNSET:
            field_dict["detectedObjectNames"] = detected_object_names
        if detected_objects_string is not UNSET:
            field_dict["detectedObjectsString"] = detected_objects_string
        if object_ is not UNSET:
            field_dict["object"] = object_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.object_detection_response_choices_array_item_ref import (
            ObjectDetectionResponseChoicesArrayItemRef,
        )
        from ..models.object_detection_response_usage import (
            ObjectDetectionResponseUsage,
        )
        from ..models.object_detection_response_detected_objects_array_item_ref import (
            ObjectDetectionResponseDetectedObjectsArrayItemRef,
        )

        d = src_dict.copy()
        choices = []
        _choices = d.pop("choices", UNSET)
        for componentsschemas_object_detection_response_choices_item_data in (
            _choices or []
        ):
            componentsschemas_object_detection_response_choices_item = (
                ObjectDetectionResponseChoicesArrayItemRef.from_dict(
                    componentsschemas_object_detection_response_choices_item_data
                )
            )

            choices.append(componentsschemas_object_detection_response_choices_item)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, ObjectDetectionResponseUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = ObjectDetectionResponseUsage.from_dict(_usage)

        prompt_tokens = d.pop("promptTokens", UNSET)

        model = d.pop("model", UNSET)

        id = d.pop("id", UNSET)

        text = d.pop("text", UNSET)

        completion_tokens = d.pop("completionTokens", UNSET)

        created = d.pop("created", UNSET)

        total_tokens = d.pop("totalTokens", UNSET)

        detected_objects = []
        _detected_objects = d.pop("detectedObjects", UNSET)
        for componentsschemas_object_detection_response_detected_objects_item_data in (
            _detected_objects or []
        ):
            componentsschemas_object_detection_response_detected_objects_item = ObjectDetectionResponseDetectedObjectsArrayItemRef.from_dict(
                componentsschemas_object_detection_response_detected_objects_item_data
            )

            detected_objects.append(
                componentsschemas_object_detection_response_detected_objects_item
            )

        detected_object_names = cast(list[str], d.pop("detectedObjectNames", UNSET))

        detected_objects_string = d.pop("detectedObjectsString", UNSET)

        object_ = d.pop("object", UNSET)

        object_detection_response = cls(
            choices=choices,
            usage=usage,
            prompt_tokens=prompt_tokens,
            model=model,
            id=id,
            text=text,
            completion_tokens=completion_tokens,
            created=created,
            total_tokens=total_tokens,
            detected_objects=detected_objects,
            detected_object_names=detected_object_names,
            detected_objects_string=detected_objects_string,
            object_=object_,
        )

        object_detection_response.additional_properties = d
        return object_detection_response

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
