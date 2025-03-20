from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.image_classification_request_image_type import (
    ImageClassificationRequestImageType,
)
from typing import Union

if TYPE_CHECKING:
    from ..models.image_classification_request_categories import (
        ImageClassificationRequestCategories,
    )


T = TypeVar("T", bound="ImageClassificationRequest")


@_attrs_define
class ImageClassificationRequest:
    """
    Attributes:
        categories (ImageClassificationRequestCategories): Categories
        image_type (ImageClassificationRequestImageType): The type of image to send along with a message if image
            analysis is needed
        description (Union[Unset, str]): Description of the given image
        image_url (Union[Unset, str]): The publicly accessible URL of the image to send along with the user prompt
    """

    categories: "ImageClassificationRequestCategories"
    image_type: ImageClassificationRequestImageType
    description: Union[Unset, str] = UNSET
    image_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        categories = self.categories.to_dict()

        image_type = self.image_type.value

        description = self.description

        image_url = self.image_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "categories": categories,
                "image_type": image_type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if image_url is not UNSET:
            field_dict["image_url"] = image_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.image_classification_request_categories import (
            ImageClassificationRequestCategories,
        )

        d = src_dict.copy()
        categories = ImageClassificationRequestCategories.from_dict(d.pop("categories"))

        image_type = ImageClassificationRequestImageType(d.pop("image_type"))

        description = d.pop("description", UNSET)

        image_url = d.pop("image_url", UNSET)

        image_classification_request = cls(
            categories=categories,
            image_type=image_type,
            description=description,
            image_url=image_url,
        )

        image_classification_request.additional_properties = d
        return image_classification_request

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
