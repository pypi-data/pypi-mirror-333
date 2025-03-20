from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateNotebookInstanceRequest")


@_attrs_define
class CreateNotebookInstanceRequest:
    """
    Attributes:
        name (str):
        instance_type (str): AWS EC2 Instance Type (see list of available options) Example: ml.t3.medium.
        accelerator_types (List[str]):
        volume_size_gb (int):
        is_shared_with_project (Union[Unset, bool]): Whether the notebook is shared with the project Default: False.
    """

    name: str
    instance_type: str
    accelerator_types: List[str]
    volume_size_gb: int
    is_shared_with_project: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        instance_type = self.instance_type

        accelerator_types = self.accelerator_types

        volume_size_gb = self.volume_size_gb

        is_shared_with_project = self.is_shared_with_project

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "instanceType": instance_type,
                "acceleratorTypes": accelerator_types,
                "volumeSizeGB": volume_size_gb,
            }
        )
        if is_shared_with_project is not UNSET:
            field_dict["isSharedWithProject"] = is_shared_with_project

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        instance_type = d.pop("instanceType")

        accelerator_types = cast(List[str], d.pop("acceleratorTypes"))

        volume_size_gb = d.pop("volumeSizeGB")

        is_shared_with_project = d.pop("isSharedWithProject", UNSET)

        create_notebook_instance_request = cls(
            name=name,
            instance_type=instance_type,
            accelerator_types=accelerator_types,
            volume_size_gb=volume_size_gb,
            is_shared_with_project=is_shared_with_project,
        )

        create_notebook_instance_request.additional_properties = d
        return create_notebook_instance_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())
