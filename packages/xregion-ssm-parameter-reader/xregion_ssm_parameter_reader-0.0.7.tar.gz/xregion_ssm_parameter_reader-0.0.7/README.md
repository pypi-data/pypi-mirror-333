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
