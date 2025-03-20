from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.image_comparison_request_categories_of_comparison import (
        ImageComparisonRequestCategoriesOfComparison,
    )


T = TypeVar("T", bound="ImageComparisonRequest")


@_attrs_define
class ImageComparisonRequest:
    """
    Attributes:
        comparison_categories (Union[Unset, ImageComparisonRequestCategoriesOfComparison]): The comparison categories to
            search for across the images. If not identified, a general comparison will be returned.
        additional_context (Union[Unset, str]): Extra information that provides context for the image comparison.
    """

    comparison_categories: Union[
        Unset, "ImageComparisonRequestCategoriesOfComparison"
    ] = UNSET
    additional_context: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        comparison_categories: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.comparison_categories, Unset):
            comparison_categories = self.comparison_categories.to_dict()

        additional_context = self.additional_context

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if comparison_categories is not UNSET:
            field_dict["comparisonCategories"] = comparison_categories
        if additional_context is not UNSET:
            field_dict["additionalContext"] = additional_context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.image_comparison_request_categories_of_comparison import (
            ImageComparisonRequestCategoriesOfComparison,
        )

        d = src_dict.copy()
        _comparison_categories = d.pop("comparisonCategories", UNSET)
        comparison_categories: Union[
            Unset, ImageComparisonRequestCategoriesOfComparison
        ]
        if isinstance(_comparison_categories, Unset):
            comparison_categories = UNSET
        else:
            comparison_categories = (
                ImageComparisonRequestCategoriesOfComparison.from_dict(
                    _comparison_categories
                )
            )

        additional_context = d.pop("additionalContext", UNSET)

        image_comparison_request = cls(
            comparison_categories=comparison_categories,
            additional_context=additional_context,
        )

        image_comparison_request.additional_properties = d
        return image_comparison_request

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
