from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.image_comparison_response_output import ImageComparisonResponseOutput


T = TypeVar("T", bound="ImageComparisonResponse")


@_attrs_define
class ImageComparisonResponse:
    """
    Attributes:
        output (Union[Unset, ImageComparisonResponseOutput]):
    """

    output: Union[Unset, "ImageComparisonResponseOutput"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        output: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if output is not UNSET:
            field_dict["output"] = output

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.image_comparison_response_output import (
            ImageComparisonResponseOutput,
        )

        d = src_dict.copy()
        _output = d.pop("output", UNSET)
        output: Union[Unset, ImageComparisonResponseOutput]
        if isinstance(_output, Unset):
            output = UNSET
        else:
            output = ImageComparisonResponseOutput.from_dict(_output)

        image_comparison_response = cls(
            output=output,
        )

        image_comparison_response.additional_properties = d
        return image_comparison_response

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
