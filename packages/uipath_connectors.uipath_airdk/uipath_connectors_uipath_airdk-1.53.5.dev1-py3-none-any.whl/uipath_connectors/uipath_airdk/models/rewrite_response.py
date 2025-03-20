from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="RewriteResponse")


@_attrs_define
class RewriteResponse:
    """
    Attributes:
        rewritten_content (Union[Unset, str]): The final rewritten version of the original content. Example: प्रोटोकॉल
            बफर्स, जिसे प्रोटोबफ भी कहा जाता है, एक ऐसी तकनीक है जो डेटा को संरचित और संक्षिप्त रूप में सहेजती है। गूगल
            द्वारा विकसित, यह उनकी आंतरिक सेवाओं में संचार और डेटा संग्रहण के लिए खूब इस्तेमाल होती है। यह भाषा और मंच की
            सीमाओं से परे है और इसे विस्तारित किया जा सकता है। इसकी मुख्य विशेषताएं हैं: भाषा स्वतंत्रता, दक्षता,
            विस्तारशीलता और क्रॉस-प्लेटफॉर्म समर्थन। यह आपको विभिन्न प्रोग्रामिंग भाषाओं में डेटा को आसानी से संग्रहित और
            पुनर्प्राप्त करने की सुविधा देता है।.
    """

    rewritten_content: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rewritten_content = self.rewritten_content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rewritten_content is not UNSET:
            field_dict["rewrittenContent"] = rewritten_content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        rewritten_content = d.pop("rewrittenContent", UNSET)

        rewrite_response = cls(
            rewritten_content=rewritten_content,
        )

        rewrite_response.additional_properties = d
        return rewrite_response

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
