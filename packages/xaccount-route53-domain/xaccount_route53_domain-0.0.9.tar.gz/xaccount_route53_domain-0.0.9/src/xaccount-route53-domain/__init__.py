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

import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import constructs as _constructs_77d1e7e8


class CrossRegionAccountSubZone(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="xaccount-route53-domain.CrossRegionAccountSubZone",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        parent_zone_name: builtins.str,
        parent_zone_id: builtins.str,
        intermediate_zone_prefix: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param parent_zone_name: -
        :param parent_zone_id: -
        :param intermediate_zone_prefix: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d943411636f5a6bf19592dca3f0ecc2b986cc8ff5f2d9c9ebc0192f7ee3be7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parent_zone_name", value=parent_zone_name, expected_type=type_hints["parent_zone_name"])
            check_type(argname="argument parent_zone_id", value=parent_zone_id, expected_type=type_hints["parent_zone_id"])
            check_type(argname="argument intermediate_zone_prefix", value=intermediate_zone_prefix, expected_type=type_hints["intermediate_zone_prefix"])
        jsii.create(self.__class__, self, [scope, id, parent_zone_name, parent_zone_id, intermediate_zone_prefix])

    @jsii.member(jsii_name="retrieveIntermediateZoneName")
    def retrieve_intermediate_zone_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "retrieveIntermediateZoneName", []))

    @jsii.member(jsii_name="setupCommon")
    def setup_common(
        self,
        scope: _constructs_77d1e7e8.Construct,
        accounts: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param scope: -
        :param accounts: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621000b5ce07b48e319c0eee25970002a21e9d402337636d057e068e3928dafe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
        return typing.cast(None, jsii.invoke(self, "setupCommon", [scope, accounts]))

    @jsii.member(jsii_name="setupDns")
    def setup_dns(
        self,
        scope: _constructs_77d1e7e8.Construct,
        env_name: builtins.str,
        config: "ICrossRegionAccountSubZoneConfig",
    ) -> _aws_cdk_aws_route53_ceddda9d.IPublicHostedZone:
        '''
        :param scope: -
        :param env_name: -
        :param config: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282c5084da128de0f5717e8e3c0b941260d4d5215df85393867379bdbef3034a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument env_name", value=env_name, expected_type=type_hints["env_name"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IPublicHostedZone, jsii.invoke(self, "setupDns", [scope, env_name, config]))

    @builtins.property
    @jsii.member(jsii_name="intermediateZoneName")
    def _intermediate_zone_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intermediateZoneName"))

    @_intermediate_zone_name.setter
    def _intermediate_zone_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121ab644d163d8fe94eeabcd4568e4bee00e7acbc1220fde84eac56fd6e7a2cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intermediateZoneName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intermediateZonePrefix")
    def _intermediate_zone_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intermediateZonePrefix"))

    @_intermediate_zone_prefix.setter
    def _intermediate_zone_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c863da5997081333ed94e5ae1f8070c90c1416da3218964dbaf958b7e55046bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intermediateZonePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentZoneId")
    def _parent_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentZoneId"))

    @_parent_zone_id.setter
    def _parent_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e999c2ee362947277e65a826e345c038082ba1ad96a604eaffde142bb388b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentZoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentZoneName")
    def _parent_zone_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentZoneName"))

    @_parent_zone_name.setter
    def _parent_zone_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1849f433ebd5e0707b692ec9745ecff9cd219c697411c89e8e55503c3eb592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentZoneName", value) # pyright: ignore[reportArgumentType]


@jsii.interface(jsii_type="xaccount-route53-domain.ICrossRegionAccountSubZoneConfig")
class ICrossRegionAccountSubZoneConfig(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(self) -> builtins.bool:
        ...

    @builtins.property
    @jsii.member(jsii_name="primaryRegion")
    def primary_region(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="secondaryRegion")
    def secondary_region(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="cicdAccount")
    def cicd_account(self) -> typing.Optional[builtins.str]:
        ...


class _ICrossRegionAccountSubZoneConfigProxy:
    __jsii_type__: typing.ClassVar[str] = "xaccount-route53-domain.ICrossRegionAccountSubZoneConfig"

    @builtins.property
    @jsii.member(jsii_name="primary")
    def primary(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "primary"))

    @builtins.property
    @jsii.member(jsii_name="primaryRegion")
    def primary_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryRegion"))

    @builtins.property
    @jsii.member(jsii_name="secondaryRegion")
    def secondary_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryRegion"))

    @builtins.property
    @jsii.member(jsii_name="cicdAccount")
    def cicd_account(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cicdAccount"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICrossRegionAccountSubZoneConfig).__jsii_proxy_class__ = lambda : _ICrossRegionAccountSubZoneConfigProxy


__all__ = [
    "CrossRegionAccountSubZone",
    "ICrossRegionAccountSubZoneConfig",
]

publication.publish()

def _typecheckingstub__0d943411636f5a6bf19592dca3f0ecc2b986cc8ff5f2d9c9ebc0192f7ee3be7a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    parent_zone_name: builtins.str,
    parent_zone_id: builtins.str,
    intermediate_zone_prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621000b5ce07b48e319c0eee25970002a21e9d402337636d057e068e3928dafe(
    scope: _constructs_77d1e7e8.Construct,
    accounts: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282c5084da128de0f5717e8e3c0b941260d4d5215df85393867379bdbef3034a(
    scope: _constructs_77d1e7e8.Construct,
    env_name: builtins.str,
    config: ICrossRegionAccountSubZoneConfig,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121ab644d163d8fe94eeabcd4568e4bee00e7acbc1220fde84eac56fd6e7a2cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c863da5997081333ed94e5ae1f8070c90c1416da3218964dbaf958b7e55046bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e999c2ee362947277e65a826e345c038082ba1ad96a604eaffde142bb388b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1849f433ebd5e0707b692ec9745ecff9cd219c697411c89e8e55503c3eb592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
