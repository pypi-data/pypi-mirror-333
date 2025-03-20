from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ReformatResponse")


@_attrs_define
class ReformatResponse:
    """
    Attributes:
        generated_output (Union[Unset, str]): The reformatted output Example: ```json
            [
                {
                    "name": "manas",
                    "age": 28
                },
                {
                    "name": "krishna",
                    "age": 29
                }
            ]
            ```.
    """

    generated_output: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        generated_output = self.generated_output

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if generated_output is not UNSET:
            field_dict["generatedOutput"] = generated_output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        generated_output = d.pop("generatedOutput", UNSET)

        reformat_response = cls(
            generated_output=generated_output,
        )

        reformat_response.additional_properties = d
        return reformat_response

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
