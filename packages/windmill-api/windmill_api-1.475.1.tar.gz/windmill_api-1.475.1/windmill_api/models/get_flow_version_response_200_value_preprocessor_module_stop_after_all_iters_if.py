from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFlowVersionResponse200ValuePreprocessorModuleStopAfterAllItersIf")


@_attrs_define
class GetFlowVersionResponse200ValuePreprocessorModuleStopAfterAllItersIf:
    """
    Attributes:
        expr (str):
        skip_if_stopped (Union[Unset, bool]):
    """

    expr: str
    skip_if_stopped: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expr = self.expr
        skip_if_stopped = self.skip_if_stopped

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expr": expr,
            }
        )
        if skip_if_stopped is not UNSET:
            field_dict["skip_if_stopped"] = skip_if_stopped

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expr = d.pop("expr")

        skip_if_stopped = d.pop("skip_if_stopped", UNSET)

        get_flow_version_response_200_value_preprocessor_module_stop_after_all_iters_if = cls(
            expr=expr,
            skip_if_stopped=skip_if_stopped,
        )

        get_flow_version_response_200_value_preprocessor_module_stop_after_all_iters_if.additional_properties = d
        return get_flow_version_response_200_value_preprocessor_module_stop_after_all_iters_if

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
