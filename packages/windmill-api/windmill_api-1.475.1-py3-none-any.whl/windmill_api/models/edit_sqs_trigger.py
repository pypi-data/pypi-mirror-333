from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditSqsTrigger")


@_attrs_define
class EditSqsTrigger:
    """
    Attributes:
        queue_url (str):
        aws_resource_path (str):
        path (str):
        script_path (str):
        is_flow (bool):
        enabled (bool):
        message_attributes (Union[Unset, List[str]]):
    """

    queue_url: str
    aws_resource_path: str
    path: str
    script_path: str
    is_flow: bool
    enabled: bool
    message_attributes: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        queue_url = self.queue_url
        aws_resource_path = self.aws_resource_path
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        enabled = self.enabled
        message_attributes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.message_attributes, Unset):
            message_attributes = self.message_attributes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queue_url": queue_url,
                "aws_resource_path": aws_resource_path,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "enabled": enabled,
            }
        )
        if message_attributes is not UNSET:
            field_dict["message_attributes"] = message_attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        queue_url = d.pop("queue_url")

        aws_resource_path = d.pop("aws_resource_path")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        enabled = d.pop("enabled")

        message_attributes = cast(List[str], d.pop("message_attributes", UNSET))

        edit_sqs_trigger = cls(
            queue_url=queue_url,
            aws_resource_path=aws_resource_path,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            enabled=enabled,
            message_attributes=message_attributes,
        )

        edit_sqs_trigger.additional_properties = d
        return edit_sqs_trigger

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
