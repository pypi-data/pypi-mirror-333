from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.categorize_request_categories import CategorizeRequestCategories


T = TypeVar("T", bound="CategorizeRequest")


@_attrs_define
class CategorizeRequest:
    """
    Attributes:
        categories (CategorizeRequestCategories): Categories
        content (str): The content to categorize. This must be provided as a string. Example: I am unable to access my
            email account. Whenever I try to log in, I receive an error message saying 'Invalid username or password.
        description (Union[Unset, str]): Short description of the content being categorized.  For example, product
            support tickets, customer reviews, etc. Example: A helpdesk representative wants to set up an automation that
            takes customer queries/product support tickets and categorizes them according to pre-defined categories to route
            to the appropriate team..
    """

    categories: "CategorizeRequestCategories"
    content: str
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        categories = self.categories.to_dict()

        content = self.content

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "categories": categories,
                "content": content,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.categorize_request_categories import CategorizeRequestCategories

        d = src_dict.copy()
        categories = CategorizeRequestCategories.from_dict(d.pop("categories"))

        content = d.pop("content")

        description = d.pop("description", UNSET)

        categorize_request = cls(
            categories=categories,
            content=content,
            description=description,
        )

        categorize_request.additional_properties = d
        return categorize_request

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
