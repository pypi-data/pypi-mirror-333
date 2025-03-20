from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GenerateEmailResponse")


@_attrs_define
class GenerateEmailResponse:
    """
    Attributes:
        need_salutation (Union[Unset, bool]): Include salutation if needed Example: True.
        need_sign_off (Union[Unset, bool]): Include sign-off if needed Example: True.
        total_words (Union[Unset, int]): Approximate number of words to return. If not populated, model will determine
            appropriate length Example: 250.0.
        email_content (Union[Unset, str]): The content of the email after translation. Example: Esteemed Colleagues,

            It is with immense pride and sincere appreciation that I share with you the remarkable news of our project’s
            early and successful completion. This significant milestone is not just a marker of success, but a resounding
            affirmation of your unparalleled commitment, unwavering dedication, and collaborative spirit which have been
            instrumental in surpassing our collective goals.

            Your individual contributions have coalesced into an extraordinary display of excellence that not only meets but
            exceeds the high standards we set for ourselves. As we take a moment to bask in the glory of our achievement,
            let it also serve as an impetus to continue pushing the boundaries of what we can accomplish. The road ahead is
            laden with opportunities to elevate our collective prowess and to carve out new echelons of success.

            May we take this success as a foundation upon which we will build ever more ambitious projects. Let the
            commendable work ethic and drive seen in this endeavor be the benchmark for all future undertakings. I am
            earnestly grateful for your formidable efforts and I look forward to our continued journey towards excellence.

            Thank you once again for your dedication and for setting a stellar example of teamwork in action.

            Warm regards,
            [Your Name].
    """

    need_salutation: Union[Unset, bool] = UNSET
    need_sign_off: Union[Unset, bool] = UNSET
    total_words: Union[Unset, int] = UNSET
    email_content: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        need_salutation = self.need_salutation

        need_sign_off = self.need_sign_off

        total_words = self.total_words

        email_content = self.email_content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if need_salutation is not UNSET:
            field_dict["need_salutation"] = need_salutation
        if need_sign_off is not UNSET:
            field_dict["need_sign_off"] = need_sign_off
        if total_words is not UNSET:
            field_dict["total_words"] = total_words
        if email_content is not UNSET:
            field_dict["emailContent"] = email_content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        need_salutation = d.pop("need_salutation", UNSET)

        need_sign_off = d.pop("need_sign_off", UNSET)

        total_words = d.pop("total_words", UNSET)

        email_content = d.pop("emailContent", UNSET)

        generate_email_response = cls(
            need_salutation=need_salutation,
            need_sign_off=need_sign_off,
            total_words=total_words,
            email_content=email_content,
        )

        generate_email_response.additional_properties = d
        return generate_email_response

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
