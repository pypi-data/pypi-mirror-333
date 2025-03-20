from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.content_generation_response_choices_array_item_ref import (
        ContentGenerationResponseChoicesArrayItemRef,
    )
    from ..models.content_generation_response_usage import (
        ContentGenerationResponseUsage,
    )
    from ..models.content_generation_response_detected_entities_array_item_ref import (
        ContentGenerationResponseDetectedEntitiesArrayItemRef,
    )
    from ..models.content_generation_response_context_grounding_citations_array_item_ref import (
        ContentGenerationResponseContextGroundingCitationsArrayItemRef,
    )


T = TypeVar("T", bound="ContentGenerationResponse")


@_attrs_define
class ContentGenerationResponse:
    """
    Attributes:
        choices (Union[Unset, list['ContentGenerationResponseChoicesArrayItemRef']]):
        usage (Union[Unset, ContentGenerationResponseUsage]):
        created (Union[Unset, int]): The Created Example: 1.709197578E9.
        model (Union[Unset, str]): The name or ID of the model or deployment to use for the chat completion Example:
            gpt-4o-mini-2024-07-18.
        id (Union[Unset, str]): The ID Example: chatcmpl-8xWeoCeGSDzgCUaMs3edg3X6n78PP.
        text (Union[Unset, str]): The Text Example: UiPath is widely considered to be the leading organization in the
            field of Robotic Process Automation (RPA). It offers a comprehensive RPA platform that enables businesses to
            automate repetitive tasks, streamline processes, and improve operational efficiency. UiPath has gained
            significant.
        object_ (Union[Unset, str]): The Object Example: chat.completion.
        masked_text (Union[Unset, str]): This field represents the input prompt where any potential PII data has been
            replaced with masked placeholders. Example: You are tasked with drafting a notification email to inform
            individuals about a data breach incident involving Personally Identifiable Information (PII). The breach
            involved unauthorized access to a database containing customer records. Use the following sample PII data to
            create a realistic notification email: Sample PII data: Name: Person-336 Date of Birth: DateTime-362 Social
            Security Number (SSN): 123-45-6789 Address: Address-429 Email: Email-466 Phone Number: PhoneNumber-503 Draft an
            email to notify affected individuals about the breach, reassure them of steps being taken to address the issue,
            and provide guidance on protecting their information. Ensure that the email is clear, concise, and empathetic..
        detected_entities (Union[Unset, list['ContentGenerationResponseDetectedEntitiesArrayItemRef']]):
        context_grounding_citations (Union[Unset,
            list['ContentGenerationResponseContextGroundingCitationsArrayItemRef']]):
        context_grounding_citations_string (Union[Unset, str]): The Context grounding citations string Example:
            [{"reference":"","source":"OP2_MedLM_Results.pdf","page_number":0}].
    """

    choices: Union[Unset, list["ContentGenerationResponseChoicesArrayItemRef"]] = UNSET
    usage: Union[Unset, "ContentGenerationResponseUsage"] = UNSET
    created: Union[Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    object_: Union[Unset, str] = UNSET
    masked_text: Union[Unset, str] = UNSET
    detected_entities: Union[
        Unset, list["ContentGenerationResponseDetectedEntitiesArrayItemRef"]
    ] = UNSET
    context_grounding_citations: Union[
        Unset, list["ContentGenerationResponseContextGroundingCitationsArrayItemRef"]
    ] = UNSET
    context_grounding_citations_string: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        choices: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.choices, Unset):
            choices = []
            for (
                componentsschemas_content_generation_response_choices_item_data
            ) in self.choices:
                componentsschemas_content_generation_response_choices_item = componentsschemas_content_generation_response_choices_item_data.to_dict()
                choices.append(
                    componentsschemas_content_generation_response_choices_item
                )

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        created = self.created

        model = self.model

        id = self.id

        text = self.text

        object_ = self.object_

        masked_text = self.masked_text

        detected_entities: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.detected_entities, Unset):
            detected_entities = []
            for componentsschemas_content_generation_response_detected_entities_item_data in self.detected_entities:
                componentsschemas_content_generation_response_detected_entities_item = componentsschemas_content_generation_response_detected_entities_item_data.to_dict()
                detected_entities.append(
                    componentsschemas_content_generation_response_detected_entities_item
                )

        context_grounding_citations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.context_grounding_citations, Unset):
            context_grounding_citations = []
            for componentsschemas_content_generation_response_context_grounding_citations_item_data in self.context_grounding_citations:
                componentsschemas_content_generation_response_context_grounding_citations_item = componentsschemas_content_generation_response_context_grounding_citations_item_data.to_dict()
                context_grounding_citations.append(
                    componentsschemas_content_generation_response_context_grounding_citations_item
                )

        context_grounding_citations_string = self.context_grounding_citations_string

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
        if masked_text is not UNSET:
            field_dict["maskedText"] = masked_text
        if detected_entities is not UNSET:
            field_dict["detectedEntities"] = detected_entities
        if context_grounding_citations is not UNSET:
            field_dict["contextGroundingCitations"] = context_grounding_citations
        if context_grounding_citations_string is not UNSET:
            field_dict["contextGroundingCitationsString"] = (
                context_grounding_citations_string
            )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.content_generation_response_choices_array_item_ref import (
            ContentGenerationResponseChoicesArrayItemRef,
        )
        from ..models.content_generation_response_usage import (
            ContentGenerationResponseUsage,
        )
        from ..models.content_generation_response_detected_entities_array_item_ref import (
            ContentGenerationResponseDetectedEntitiesArrayItemRef,
        )
        from ..models.content_generation_response_context_grounding_citations_array_item_ref import (
            ContentGenerationResponseContextGroundingCitationsArrayItemRef,
        )

        d = src_dict.copy()
        choices = []
        _choices = d.pop("choices", UNSET)
        for componentsschemas_content_generation_response_choices_item_data in (
            _choices or []
        ):
            componentsschemas_content_generation_response_choices_item = (
                ContentGenerationResponseChoicesArrayItemRef.from_dict(
                    componentsschemas_content_generation_response_choices_item_data
                )
            )

            choices.append(componentsschemas_content_generation_response_choices_item)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, ContentGenerationResponseUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = ContentGenerationResponseUsage.from_dict(_usage)

        created = d.pop("created", UNSET)

        model = d.pop("model", UNSET)

        id = d.pop("id", UNSET)

        text = d.pop("text", UNSET)

        object_ = d.pop("object", UNSET)

        masked_text = d.pop("maskedText", UNSET)

        detected_entities = []
        _detected_entities = d.pop("detectedEntities", UNSET)
        for (
            componentsschemas_content_generation_response_detected_entities_item_data
        ) in _detected_entities or []:
            componentsschemas_content_generation_response_detected_entities_item = ContentGenerationResponseDetectedEntitiesArrayItemRef.from_dict(
                componentsschemas_content_generation_response_detected_entities_item_data
            )

            detected_entities.append(
                componentsschemas_content_generation_response_detected_entities_item
            )

        context_grounding_citations = []
        _context_grounding_citations = d.pop("contextGroundingCitations", UNSET)
        for componentsschemas_content_generation_response_context_grounding_citations_item_data in (
            _context_grounding_citations or []
        ):
            componentsschemas_content_generation_response_context_grounding_citations_item = ContentGenerationResponseContextGroundingCitationsArrayItemRef.from_dict(
                componentsschemas_content_generation_response_context_grounding_citations_item_data
            )

            context_grounding_citations.append(
                componentsschemas_content_generation_response_context_grounding_citations_item
            )

        context_grounding_citations_string = d.pop(
            "contextGroundingCitationsString", UNSET
        )

        content_generation_response = cls(
            choices=choices,
            usage=usage,
            created=created,
            model=model,
            id=id,
            text=text,
            object_=object_,
            masked_text=masked_text,
            detected_entities=detected_entities,
            context_grounding_citations=context_grounding_citations,
            context_grounding_citations_string=context_grounding_citations_string,
        )

        content_generation_response.additional_properties = d
        return content_generation_response

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
