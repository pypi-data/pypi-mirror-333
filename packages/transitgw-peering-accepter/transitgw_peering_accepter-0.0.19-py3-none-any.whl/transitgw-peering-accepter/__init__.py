r'''
# replace this
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import constructs as _constructs_77d1e7e8


class AcceptTransitPeering(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="transitgw-peering-accepter.AcceptTransitPeering",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        transit_gateway_attachment_id: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param transit_gateway_attachment_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc00e8dc09428903658c36339803c75d3c9f5bf0daeb90ec0bb0c54be9e0bc2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument transit_gateway_attachment_id", value=transit_gateway_attachment_id, expected_type=type_hints["transit_gateway_attachment_id"])
        jsii.create(self.__class__, self, [scope, id, transit_gateway_attachment_id])


__all__ = [
    "AcceptTransitPeering",
]

publication.publish()

def _typecheckingstub__ccc00e8dc09428903658c36339803c75d3c9f5bf0daeb90ec0bb0c54be9e0bc2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    transit_gateway_attachment_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
