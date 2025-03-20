from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.image_analysis_response_usage import ImageAnalysisResponseUsage
    from ..models.image_analysis_response_choices_array_item_ref import (
        ImageAnalysisResponseChoicesArrayItemRef,
    )


T = TypeVar("T", bound="ImageAnalysisResponse")


@_attrs_define
class ImageAnalysisResponse:
    """
    Attributes:
        choices (Union[Unset, list['ImageAnalysisResponseChoicesArrayItemRef']]):
        usage (Union[Unset, ImageAnalysisResponseUsage]):
        created (Union[Unset, int]): The Created Example: 1.709197578E9.
        model (Union[Unset, str]): The name or ID of the model or deployment to use for the chat completion Example:
            gpt-35-turbo-16k.
        id (Union[Unset, str]): The ID Example: chatcmpl-8xWeoCeGSDzgCUaMs3edg3X6n78PP.
        text (Union[Unset, str]): The image analysis completion text Example: UiPath is widely considered to be the
            leading organization in the field of Robotic Process Automation (RPA). It offers a comprehensive RPA platform
            that enables businesses to automate repetitive tasks, streamline processes, and improve operational efficiency.
            UiPath has gained significant.
        object_ (Union[Unset, str]): The Object Example: chat.completion.
        total_tokens (Union[Unset, int]): The count of total tokens processed in the request Example: 912.0.
        completion_tokens (Union[Unset, int]): The number of tokens the model is allowed to use for generating the
            completion Example: 259.0.
        prompt_tokens (Union[Unset, int]): The number of tokens used in the prompt for generating the completion
            Example: 653.0.
    """

    choices: Union[Unset, list["ImageAnalysisResponseChoicesArrayItemRef"]] = UNSET
    usage: Union[Unset, "ImageAnalysisResponseUsage"] = UNSET
    created: Union[Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    object_: Union[Unset, str] = UNSET
    total_tokens: Union[Unset, int] = UNSET
    completion_tokens: Union[Unset, int] = UNSET
    prompt_tokens: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        choices: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.choices, Unset):
            choices = []
            for (
                componentsschemas_image_analysis_response_choices_item_data
            ) in self.choices:
                componentsschemas_image_analysis_response_choices_item = componentsschemas_image_analysis_response_choices_item_data.to_dict()
                choices.append(componentsschemas_image_analysis_response_choices_item)

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        created = self.created

        model = self.model

        id = self.id

        text = self.text

        object_ = self.object_

        total_tokens = self.total_tokens

        completion_tokens = self.completion_tokens

        prompt_tokens = self.prompt_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if choices is not UNSET:
            field_dict["choices"] = choices
        if usage is not UNSET:
            field_dict["usage"] = usage
        if created is not UNSET:
            field_dict["created"] = created
        if model is not UNSET:
            field_dict["model"] = model
        if id is not UNSET:
            field_dict["id"] = id
        if text is not UNSET:
            field_dict["text"] = text
        if object_ is not UNSET:
            field_dict["object"] = object_
        if total_tokens is not UNSET:
            field_dict["totalTokens"] = total_tokens
        if completion_tokens is not UNSET:
            field_dict["completionTokens"] = completion_tokens
        if prompt_tokens is not UNSET:
            field_dict["promptTokens"] = prompt_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.image_analysis_response_usage import ImageAnalysisResponseUsage
        from ..models.image_analysis_response_choices_array_item_ref import (
            ImageAnalysisResponseChoicesArrayItemRef,
        )

        d = src_dict.copy()
        choices = []
        _choices = d.pop("choices", UNSET)
        for componentsschemas_image_analysis_response_choices_item_data in (
            _choices or []
        ):
            componentsschemas_image_analysis_response_choices_item = (
                ImageAnalysisResponseChoicesArrayItemRef.from_dict(
                    componentsschemas_image_analysis_response_choices_item_data
                )
            )

            choices.append(componentsschemas_image_analysis_response_choices_item)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, ImageAnalysisResponseUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = ImageAnalysisResponseUsage.from_dict(_usage)

        created = d.pop("created", UNSET)

        model = d.pop("model", UNSET)

        id = d.pop("id", UNSET)

        text = d.pop("text", UNSET)

        object_ = d.pop("object", UNSET)

        total_tokens = d.pop("totalTokens", UNSET)

        completion_tokens = d.pop("completionTokens", UNSET)

        prompt_tokens = d.pop("promptTokens", UNSET)

        image_analysis_response = cls(
            choices=choices,
            usage=usage,
            created=created,
            model=model,
            id=id,
            text=text,
            object_=object_,
            total_tokens=total_tokens,
            completion_tokens=completion_tokens,
            prompt_tokens=prompt_tokens,
        )

        image_analysis_response.additional_properties = d
        return image_analysis_response

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
