from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.image_analysis_request_image_type import ImageAnalysisRequestImageType
from typing import Union


T = TypeVar("T", bound="ImageAnalysisRequest")


@_attrs_define
class ImageAnalysisRequest:
    """
    Attributes:
        prompt (str): The user prompt for the chat completion request Example: Which organization holds the leading
            position in the field of Robotic Process Automation (RPA)?.
        image_type (ImageAnalysisRequestImageType): The type of image to send along with a message if image analysis is
            needed
        max_tokens (Union[Unset, int]): The maximum number of tokens to generate in the completion. The token count of
            your prompt plus those from the result/completion cannot exceed the value provided for this field. It's best to
            set this value to be a less than the model maximum count so as to have some room for the prompt token count.
            Example: 50.0.
        presence_penalty (Union[Unset, int]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
            whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Defaults to
            0 Example: 1.0.
        n (Union[Unset, int]): The number of completion choices to generate for the request. The higher the value of
            this field, the more the number of tokens that will get used, and hence will result in a higher cost, so the
            user needs to be aware of that when setting the value of this field. Defaults to 1 Example: 1.0.
        stop (Union[Unset, str]): Up to 4 sequences where the API will stop generating further tokens. The returned text
            will not contain the stop sequence. Defaults to null.
        top_p (Union[Unset, int]): A number between 0 and 1.  The lower the number, the fewer tokens are considered.
            Defaults to 1 Example: 1.0.
        topP (Union[Unset, float]): A number between 0 and 1.  The lower the number, the lesser the randomness. Defaults
            to 0.8. Example: 0.8.
        top_k (Union[Unset, int]): A number between 1 and 40.  The higher the number the higher the diversity of
            generated text. Defaults to 40. Example: 40.0.
        frequency_penalty (Union[Unset, int]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
            their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
            Defaults to 0 Example: 1.0.
        instruction (Union[Unset, str]): The system prompt or context instruction of the chat completion request
            Example: You are a informational provider.
        temperature (Union[Unset, float]): The value of the creativity factor or sampling temperature to use. Higher
            values means the model will take more risks. Try 0.9 for more creative responses or completions, and 0 (also
            called argmax sampling) for ones with a well-defined or more exact answer.  The general recommendation is to
            alter, from the default value, this or the Nucleus Sample value, but not both values. Defaults to 1
        image_url (Union[Unset, str]): The publicly accessible URL of the image to send along with the user prompt
    """

    prompt: str
    image_type: ImageAnalysisRequestImageType
    max_tokens: Union[Unset, int] = UNSET
    presence_penalty: Union[Unset, int] = UNSET
    n: Union[Unset, int] = UNSET
    stop: Union[Unset, str] = UNSET
    top_p: Union[Unset, int] = UNSET
    topP: Union[Unset, float] = UNSET
    top_k: Union[Unset, int] = UNSET
    frequency_penalty: Union[Unset, int] = UNSET
    instruction: Union[Unset, str] = UNSET
    temperature: Union[Unset, float] = UNSET
    image_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        image_type = self.image_type.value

        max_tokens = self.max_tokens

        presence_penalty = self.presence_penalty

        n = self.n

        stop = self.stop

        top_p = self.top_p

        topP = self.topP

        top_k = self.top_k

        frequency_penalty = self.frequency_penalty

        instruction = self.instruction

        temperature = self.temperature

        image_url = self.image_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
                "image_type": image_type,
            }
        )
        if max_tokens is not UNSET:
            field_dict["max_tokens"] = max_tokens
        if presence_penalty is not UNSET:
            field_dict["presence_penalty"] = presence_penalty
        if n is not UNSET:
            field_dict["n"] = n
        if stop is not UNSET:
            field_dict["stop"] = stop
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if topP is not UNSET:
            field_dict["topP"] = topP
        if top_k is not UNSET:
            field_dict["topK"] = top_k
        if frequency_penalty is not UNSET:
            field_dict["frequency_penalty"] = frequency_penalty
        if instruction is not UNSET:
            field_dict["instruction"] = instruction
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if image_url is not UNSET:
            field_dict["image_url"] = image_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        image_type = ImageAnalysisRequestImageType(d.pop("image_type"))

        max_tokens = d.pop("max_tokens", UNSET)

        presence_penalty = d.pop("presence_penalty", UNSET)

        n = d.pop("n", UNSET)

        stop = d.pop("stop", UNSET)

        top_p = d.pop("top_p", UNSET)

        topP = d.pop("topP", UNSET)

        top_k = d.pop("topK", UNSET)

        frequency_penalty = d.pop("frequency_penalty", UNSET)

        instruction = d.pop("instruction", UNSET)

        temperature = d.pop("temperature", UNSET)

        image_url = d.pop("image_url", UNSET)

        image_analysis_request = cls(
            prompt=prompt,
            image_type=image_type,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            n=n,
            stop=stop,
            top_p=top_p,
            topP=topP,
            top_k=top_k,
            frequency_penalty=frequency_penalty,
            instruction=instruction,
            temperature=temperature,
            image_url=image_url,
        )

        image_analysis_request.additional_properties = d
        return image_analysis_request

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
