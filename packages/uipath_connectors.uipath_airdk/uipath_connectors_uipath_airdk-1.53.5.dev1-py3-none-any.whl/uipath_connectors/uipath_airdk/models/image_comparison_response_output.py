from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ImageComparisonResponseOutput")


@_attrs_define
class ImageComparisonResponseOutput:
    """
    Attributes:
        comparison_description (Union[Unset, str]): The general comparison description between the images.
        comparison_object (Union[Unset, str]): Comparison category and content associated for the image comparison.
    """

    comparison_description: Union[Unset, str] = UNSET
    comparison_object: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        comparison_description = self.comparison_description

        comparison_object = self.comparison_object

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if comparison_description is not UNSET:
            field_dict["comparisonDescription"] = comparison_description
        if comparison_object is not UNSET:
            field_dict["comparisonObject"] = comparison_object

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        comparison_description = d.pop("comparisonDescription", UNSET)

        comparison_object = d.pop("comparisonObject", UNSET)

        image_comparison_response_output = cls(
            comparison_description=comparison_description,
            comparison_object=comparison_object,
        )

        image_comparison_response_output.additional_properties = d
        return image_comparison_response_output

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
