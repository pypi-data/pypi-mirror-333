r'''
# Cross-region cross-account SSM parameter reader construct for AWS CDK

Easy-to-use CDK construct for reading SSM parameters in a cross-account cross-region fashion, overcoming the limits of the native SSM parameter.

## Introduction

This construct has been created to be able to share pieces of information across regions (and accounts) in deployment pipelines but it can be used also outside of the CI/CD context.

## Cross-region example

This strategy is particularly useful in case of a deployment pipeline where you want to share the same parameter across regions **within the same account**.

As part of a stack deployed in `region-1`, create the parameter as usual:

```python
new StringParameter(this, 'param', {
    parameterName: '/param/name'
    stringValue: 'param value',
});
```

When in `region-2`, use the following to read the parameter value:

```python
const paramValue = new SSMParameterReader(this, 'SSMParameterReader', {
    parameterName: '/param/name',
    region: 'region-1',
}).retrieveParameterValue();
```

## Cross-account example

This strategy is useful still in a deployment pipeline but to share a parameter across regions **and** accounts.
For example, let's assume we want to share the same transit gateway across accounts and regions.
The pipeline can be deployed in a CICD account, separated from the usual target accounts (i.e. dev, test and prod).

In this case you would share the resource using Resource Access Manager (out of scope for this example) and you will create two parameters in `region-1` and in the CICD account, to share the **transit gateway ID** and the **shared resource ARN**:

```python
const principals = [ new AccountPrincipal(devAccount), new AccountPrincipal(testAccount), new AccountPrincipal(prodAccount)];

const transitGWParam = new StringParameter(this, 'transitGWParam', {
    parameterName: 'transitGW',
    stringValue: transitGW.attrId,
});

const transitShareParam = new StringParameter(this, 'transitShareParam', {
    parameterName: 'transitShare',
    stringValue: resourceShare.attrArn,
});

new Role(this,'transitRole',{
    assumedBy: new CompositePrincipal(...principals),
    roleName: 'transit-role-region-1'
}).addToPrincipalPolicy(new PolicyStatement({
    actions: [ 'ssm:GetParameter*' ],
    resources: [ transitGWParam.parameterArn, transitShareParam.parameterArn ]
}));
```

When in `region-2` and in one of the target accounts, to read the parameters value:

```python
const cicdAccount = 12345678;
const cicdRegion = region-1;

const transitGW = new SSMParameterReader(this, 'transitGWReader', {
    parameterName: 'transitGW',
    region: cicdRegion,
    roleArn: `arn:aws:iam::${cicdAccount}:role/transit-role-${cicdRegion}`
}).retrieveParameterValue();
```
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

import aws_cdk.custom_resources as _aws_cdk_custom_resources_ceddda9d
import constructs as _constructs_77d1e7e8


class SSMParameterReader(
    _aws_cdk_custom_resources_ceddda9d.AwsCustomResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="xregion-ssm-parameter-reader.SSMParameterReader",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        parameter_name: builtins.str,
        region: builtins.str,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param parameter_name: 
        :param region: 
        :param role_arn: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016552517393ea1ae516dba5bd4fe110130101240d06a0e102ab0e018cfc4ff7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = SSMParameterReaderProps(
            parameter_name=parameter_name, region=region, role_arn=role_arn
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @jsii.member(jsii_name="retrieveParameterValue")
    def retrieve_parameter_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "retrieveParameterValue", []))


@jsii.data_type(
    jsii_type="xregion-ssm-parameter-reader.SSMParameterReaderProps",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_name": "parameterName",
        "region": "region",
        "role_arn": "roleArn",
    },
)
class SSMParameterReaderProps:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        region: builtins.str,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameter_name: 
        :param region: 
        :param role_arn: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ecbbebcd590c9d12ebd3b08cd74334b7538e6980a7958b113a0781afd1ac66)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_name": parameter_name,
            "region": region,
        }
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def parameter_name(self) -> builtins.str:
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SSMParameterReaderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SSMParameterReader",
    "SSMParameterReaderProps",
]

publication.publish()

def _typecheckingstub__016552517393ea1ae516dba5bd4fe110130101240d06a0e102ab0e018cfc4ff7(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    parameter_name: builtins.str,
    region: builtins.str,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ecbbebcd590c9d12ebd3b08cd74334b7538e6980a7958b113a0781afd1ac66(
    *,
    parameter_name: builtins.str,
    region: builtins.str,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
