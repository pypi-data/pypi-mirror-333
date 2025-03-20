from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reformat_request_input_format import ReformatRequestInputFormat
from ..models.reformat_request_output_format import ReformatRequestOutputFormat
from typing import Union


T = TypeVar("T", bound="ReformatRequest")


@_attrs_define
class ReformatRequest:
    """
    Attributes:
        content_to_be_reformatted (str): String representation of the content to be reformatted from its original format
            into a different format.  This can also correct malformatted inputs (ex. JSON to JSON). Example: name,age
            manas,28
            krishna,29
            .
        output_format (ReformatRequestOutputFormat): The output format Example: JSON.
        example_schema (Union[Unset, str]): Example of an output with proper format Example: [{<name>: <age>}].
        input_type (Union[Unset, ReformatRequestInputFormat]): The input format.  This field is optional and the
            activity will automatically detect if not set. Example: CSV.
    """

    content_to_be_reformatted: str
    output_format: ReformatRequestOutputFormat
    example_schema: Union[Unset, str] = UNSET
    input_type: Union[Unset, ReformatRequestInputFormat] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_to_be_reformatted = self.content_to_be_reformatted

        output_format = self.output_format.value

        example_schema = self.example_schema

        input_type: Union[Unset, str] = UNSET
        if not isinstance(self.input_type, Unset):
            input_type = self.input_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contentToBeReformatted": content_to_be_reformatted,
                "outputFormat": output_format,
            }
        )
        if example_schema is not UNSET:
            field_dict["exampleSchema"] = example_schema
        if input_type is not UNSET:
            field_dict["inputType"] = input_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        content_to_be_reformatted = d.pop("contentToBeReformatted")

        output_format = ReformatRequestOutputFormat(d.pop("outputFormat"))

        example_schema = d.pop("exampleSchema", UNSET)

        _input_type = d.pop("inputType", UNSET)
        input_type: Union[Unset, ReformatRequestInputFormat]
        if isinstance(_input_type, Unset):
            input_type = UNSET
        else:
            input_type = ReformatRequestInputFormat(_input_type)

        reformat_request = cls(
            content_to_be_reformatted=content_to_be_reformatted,
            output_format=output_format,
            example_schema=example_schema,
            input_type=input_type,
        )

        reformat_request.additional_properties = d
        return reformat_request

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
