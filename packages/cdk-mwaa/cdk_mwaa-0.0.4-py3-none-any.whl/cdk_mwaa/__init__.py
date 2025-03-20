r'''
# cdk-mwaa

This project provides an AWS CDK construct library for creating and managing Amazon Managed Workflows for Apache Airflow (MWAA) environments.

## Features

* Create and manage MWAA environments
* Configure environment properties such as webserver access mode, Airflow version, environment class, and more
* Validate and set default values for environment properties
* Automatically create and configure necessary AWS resources such as S3 buckets and VPCs

## Installation

To use this construct library in your AWS CDK project, add it as a dependency:

```sh
npm install cdk-mwaa
# or
yarn add cdk-mwaa
```

## Usage

Here is an example of how to use the `cdk-mwaa` construct library in your AWS CDK project:

```python
import * as path from 'node:path';
import * as cdk from 'aws-cdk-lib';
import * as mwaa from 'cdk-mwaa';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'MwaaStack');

const dagStorage = new mwaa.DagStorage(stack, 'MyMwaaDagStorage', {
    bucketName: 'my-mwaa-dag-storage',
    dagsConfig: {
        localPath: path.join(__dirname, 'dags'),
        s3Path: 'dags/',
    },
    // additional configuration options...
});

new mwaa.Environment(stack, 'MyMwaaEnvironment', {
    name: 'my-mwaa-environment',
    dagStorage,
    airflowVersion: '2.10.3',
    sizing: mwaa.Sizing.mw1Micro(),
    // additional configuration options...
});

app.synth();
```

## Enabling Secrets Backend

To enable the secrets backend for your MWAA environment, you can use the `enableSecretsBackend` method. This allows you to securely manage secrets and environment variables.

Here is an example of how to enable the secrets backend in your MWAA environment:

```python
import * as cdk from 'aws-cdk-lib';
import * as mwaa from 'cdk-mwaa';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'MwaaStack');

const dagStorage = new mwaa.DagStorage(stack, 'MyMwaaDagStorage', {
    bucketName: 'my-mwaa-dag-storage',
    // additional configuration options...
});

const environment = new mwaa.Environment(stack, 'MyMwaaEnvironment', {
    name: 'my-mwaa-environment',
    dagStorage,
    airflowVersion: '2.10.3',
    sizing: mwaa.Sizing.mw1Micro(),
    // additional configuration options...
});

// Enabling Secrets Backend
environment.enableSecretsBackend();

app.synth();
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class DagStorage(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-mwaa.DagStorage",
):
    '''Represents an S3 storage solution for MWAA DAGs and dependencies.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        dags_config: typing.Optional[typing.Union["DagStorageConfigOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        noncurrent_version_expiration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        plugins_config: typing.Optional[typing.Union["DagStorageConfigOptionsWithS3ObjectVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        requirements_config: typing.Optional[typing.Union["DagStorageConfigOptionsWithS3ObjectVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        startup_script_config: typing.Optional[typing.Union["DagStorageConfigOptionsWithS3ObjectVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: Custom bucket name (optional).
        :param dags_config: Configuration for DAG storage.
        :param noncurrent_version_expiration: Lifecycle rule for expiring non-current object versions.
        :param plugins_config: Configuration for plugins storage.
        :param removal_policy: Bucket removal policy.
        :param requirements_config: Configuration for requirements storage.
        :param startup_script_config: Configuration for startup script storage.
        :param versioned: Enable versioning for the bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95a166027e8ebcfead2708b1c3388e60862a4fb6d86763bf56854f275bdd2390)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DagStorageProps(
            bucket_name=bucket_name,
            dags_config=dags_config,
            noncurrent_version_expiration=noncurrent_version_expiration,
            plugins_config=plugins_config,
            removal_policy=removal_policy,
            requirements_config=requirements_config,
            startup_script_config=startup_script_config,
            versioned=versioned,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        '''The S3 bucket storing DAGs, plugins, requirements, and startup scripts.'''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="dagS3Path")
    def dag_s3_path(self) -> typing.Optional[builtins.str]:
        '''S3 path for DAGs.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dagS3Path"))

    @builtins.property
    @jsii.member(jsii_name="pluginsConfig")
    def plugins_config(
        self,
    ) -> typing.Optional["DagStorageConfigOptionsWithS3ObjectVersion"]:
        '''Plugin storage configuration.'''
        return typing.cast(typing.Optional["DagStorageConfigOptionsWithS3ObjectVersion"], jsii.get(self, "pluginsConfig"))

    @builtins.property
    @jsii.member(jsii_name="requirementsConfig")
    def requirements_config(
        self,
    ) -> typing.Optional["DagStorageConfigOptionsWithS3ObjectVersion"]:
        '''Requirements storage configuration.'''
        return typing.cast(typing.Optional["DagStorageConfigOptionsWithS3ObjectVersion"], jsii.get(self, "requirementsConfig"))

    @builtins.property
    @jsii.member(jsii_name="startupScriptConfig")
    def startup_script_config(
        self,
    ) -> typing.Optional["DagStorageConfigOptionsWithS3ObjectVersion"]:
        '''Startup script storage configuration.'''
        return typing.cast(typing.Optional["DagStorageConfigOptionsWithS3ObjectVersion"], jsii.get(self, "startupScriptConfig"))


@jsii.data_type(
    jsii_type="cdk-mwaa.DagStorageConfigOptions",
    jsii_struct_bases=[],
    name_mapping={
        "s3_path": "s3Path",
        "deploy_options": "deployOptions",
        "local_path": "localPath",
    },
)
class DagStorageConfigOptions:
    def __init__(
        self,
        *,
        s3_path: builtins.str,
        deploy_options: typing.Optional[typing.Union["DagStorageDeployOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration options for DAG storage.

        :param s3_path: The S3 path where the resource is stored.
        :param deploy_options: Deployment options for DAG storage.
        :param local_path: Optional local path for the resource.
        '''
        if isinstance(deploy_options, dict):
            deploy_options = DagStorageDeployOptions(**deploy_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a9b5242a26a2093aa8052dd8b86bea06801d5a767c2e5f908776c3f849eb63)
            check_type(argname="argument s3_path", value=s3_path, expected_type=type_hints["s3_path"])
            check_type(argname="argument deploy_options", value=deploy_options, expected_type=type_hints["deploy_options"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_path": s3_path,
        }
        if deploy_options is not None:
            self._values["deploy_options"] = deploy_options
        if local_path is not None:
            self._values["local_path"] = local_path

    @builtins.property
    def s3_path(self) -> builtins.str:
        '''The S3 path where the resource is stored.'''
        result = self._values.get("s3_path")
        assert result is not None, "Required property 's3_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deploy_options(self) -> typing.Optional["DagStorageDeployOptions"]:
        '''Deployment options for DAG storage.'''
        result = self._values.get("deploy_options")
        return typing.cast(typing.Optional["DagStorageDeployOptions"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''Optional local path for the resource.'''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DagStorageConfigOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-mwaa.DagStorageConfigOptionsWithS3ObjectVersion",
    jsii_struct_bases=[DagStorageConfigOptions],
    name_mapping={
        "s3_path": "s3Path",
        "deploy_options": "deployOptions",
        "local_path": "localPath",
        "s3_object_version": "s3ObjectVersion",
    },
)
class DagStorageConfigOptionsWithS3ObjectVersion(DagStorageConfigOptions):
    def __init__(
        self,
        *,
        s3_path: builtins.str,
        deploy_options: typing.Optional[typing.Union["DagStorageDeployOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        s3_object_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_path: The S3 path where the resource is stored.
        :param deploy_options: Deployment options for DAG storage.
        :param local_path: Optional local path for the resource.
        :param s3_object_version: S3 object version identifier.
        '''
        if isinstance(deploy_options, dict):
            deploy_options = DagStorageDeployOptions(**deploy_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd77af7d832e6c1f66f71849ff7971c010e8282b5b3a43d573c7892c43539cf)
            check_type(argname="argument s3_path", value=s3_path, expected_type=type_hints["s3_path"])
            check_type(argname="argument deploy_options", value=deploy_options, expected_type=type_hints["deploy_options"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_path": s3_path,
        }
        if deploy_options is not None:
            self._values["deploy_options"] = deploy_options
        if local_path is not None:
            self._values["local_path"] = local_path
        if s3_object_version is not None:
            self._values["s3_object_version"] = s3_object_version

    @builtins.property
    def s3_path(self) -> builtins.str:
        '''The S3 path where the resource is stored.'''
        result = self._values.get("s3_path")
        assert result is not None, "Required property 's3_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deploy_options(self) -> typing.Optional["DagStorageDeployOptions"]:
        '''Deployment options for DAG storage.'''
        result = self._values.get("deploy_options")
        return typing.cast(typing.Optional["DagStorageDeployOptions"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''Optional local path for the resource.'''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_object_version(self) -> typing.Optional[builtins.str]:
        '''S3 object version identifier.'''
        result = self._values.get("s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DagStorageConfigOptionsWithS3ObjectVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-mwaa.DagStorageDeployOptions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude": "exclude",
        "prune": "prune",
        "retain_on_delete": "retainOnDelete",
    },
)
class DagStorageDeployOptions:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        prune: typing.Optional[builtins.bool] = None,
        retain_on_delete: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options for deploying files to the DAG storage bucket.

        :param exclude: Patterns to exclude from deployment.
        :param prune: Whether to remove outdated file versions.
        :param retain_on_delete: Whether to retain files upon stack deletion.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4eb47db99cbba877092424afc09de8c308a38be2c61e698dd0c28933b9c3b42)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument prune", value=prune, expected_type=type_hints["prune"])
            check_type(argname="argument retain_on_delete", value=retain_on_delete, expected_type=type_hints["retain_on_delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if prune is not None:
            self._values["prune"] = prune
        if retain_on_delete is not None:
            self._values["retain_on_delete"] = retain_on_delete

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Patterns to exclude from deployment.'''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prune(self) -> typing.Optional[builtins.bool]:
        '''Whether to remove outdated file versions.'''
        result = self._values.get("prune")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def retain_on_delete(self) -> typing.Optional[builtins.bool]:
        '''Whether to retain files upon stack deletion.'''
        result = self._values.get("retain_on_delete")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DagStorageDeployOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-mwaa.DagStorageProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "dags_config": "dagsConfig",
        "noncurrent_version_expiration": "noncurrentVersionExpiration",
        "plugins_config": "pluginsConfig",
        "removal_policy": "removalPolicy",
        "requirements_config": "requirementsConfig",
        "startup_script_config": "startupScriptConfig",
        "versioned": "versioned",
    },
)
class DagStorageProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        dags_config: typing.Optional[typing.Union[DagStorageConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        noncurrent_version_expiration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        plugins_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        requirements_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        startup_script_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        versioned: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties for configuring the DAG storage bucket.

        :param bucket_name: Custom bucket name (optional).
        :param dags_config: Configuration for DAG storage.
        :param noncurrent_version_expiration: Lifecycle rule for expiring non-current object versions.
        :param plugins_config: Configuration for plugins storage.
        :param removal_policy: Bucket removal policy.
        :param requirements_config: Configuration for requirements storage.
        :param startup_script_config: Configuration for startup script storage.
        :param versioned: Enable versioning for the bucket.
        '''
        if isinstance(dags_config, dict):
            dags_config = DagStorageConfigOptions(**dags_config)
        if isinstance(plugins_config, dict):
            plugins_config = DagStorageConfigOptionsWithS3ObjectVersion(**plugins_config)
        if isinstance(requirements_config, dict):
            requirements_config = DagStorageConfigOptionsWithS3ObjectVersion(**requirements_config)
        if isinstance(startup_script_config, dict):
            startup_script_config = DagStorageConfigOptionsWithS3ObjectVersion(**startup_script_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4bace9647a9566f3af4198e17ef015306e92a6d5f673b579ba6fdfcb5231da)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument dags_config", value=dags_config, expected_type=type_hints["dags_config"])
            check_type(argname="argument noncurrent_version_expiration", value=noncurrent_version_expiration, expected_type=type_hints["noncurrent_version_expiration"])
            check_type(argname="argument plugins_config", value=plugins_config, expected_type=type_hints["plugins_config"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument requirements_config", value=requirements_config, expected_type=type_hints["requirements_config"])
            check_type(argname="argument startup_script_config", value=startup_script_config, expected_type=type_hints["startup_script_config"])
            check_type(argname="argument versioned", value=versioned, expected_type=type_hints["versioned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if dags_config is not None:
            self._values["dags_config"] = dags_config
        if noncurrent_version_expiration is not None:
            self._values["noncurrent_version_expiration"] = noncurrent_version_expiration
        if plugins_config is not None:
            self._values["plugins_config"] = plugins_config
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if requirements_config is not None:
            self._values["requirements_config"] = requirements_config
        if startup_script_config is not None:
            self._values["startup_script_config"] = startup_script_config
        if versioned is not None:
            self._values["versioned"] = versioned

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Custom bucket name (optional).'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dags_config(self) -> typing.Optional[DagStorageConfigOptions]:
        '''Configuration for DAG storage.'''
        result = self._values.get("dags_config")
        return typing.cast(typing.Optional[DagStorageConfigOptions], result)

    @builtins.property
    def noncurrent_version_expiration(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Lifecycle rule for expiring non-current object versions.'''
        result = self._values.get("noncurrent_version_expiration")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def plugins_config(
        self,
    ) -> typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion]:
        '''Configuration for plugins storage.'''
        result = self._values.get("plugins_config")
        return typing.cast(typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Bucket removal policy.'''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def requirements_config(
        self,
    ) -> typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion]:
        '''Configuration for requirements storage.'''
        result = self._values.get("requirements_config")
        return typing.cast(typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion], result)

    @builtins.property
    def startup_script_config(
        self,
    ) -> typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion]:
        '''Configuration for startup script storage.'''
        result = self._values.get("startup_script_config")
        return typing.cast(typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion], result)

    @builtins.property
    def versioned(self) -> typing.Optional[builtins.bool]:
        '''Enable versioning for the bucket.'''
        result = self._values.get("versioned")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DagStorageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-mwaa.EmailBackendOptions",
    jsii_struct_bases=[],
    name_mapping={"from_email": "fromEmail", "conn_id": "connId"},
)
class EmailBackendOptions:
    def __init__(
        self,
        *,
        from_email: builtins.str,
        conn_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for configuring the Email backend.

        :param from_email: 
        :param conn_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e90f0cf9b9873d2646653b49d16d81a04d7e328760c253beb412d5e74258d3)
            check_type(argname="argument from_email", value=from_email, expected_type=type_hints["from_email"])
            check_type(argname="argument conn_id", value=conn_id, expected_type=type_hints["conn_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "from_email": from_email,
        }
        if conn_id is not None:
            self._values["conn_id"] = conn_id

    @builtins.property
    def from_email(self) -> builtins.str:
        result = self._values.get("from_email")
        assert result is not None, "Required property 'from_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def conn_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("conn_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailBackendOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-mwaa.EndpointManagement")
class EndpointManagement(enum.Enum):
    '''Enum for the endpoint management type for the MWAA environment.'''

    CUSTOMER = "CUSTOMER"
    SERVICE = "SERVICE"


class Environment(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-mwaa.Environment",
):
    '''Represents an MWAA environment.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        airflow_version: builtins.str,
        dag_storage: DagStorage,
        name: builtins.str,
        sizing: "Sizing",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        endpoint_management: typing.Optional[EndpointManagement] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        logging_configuration: typing.Optional[typing.Union["LoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        webserver_access_mode: typing.Optional["WebserverAccessMode"] = None,
        weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates an MWAA environment.

        :param scope: - The scope of the construct.
        :param id: - The unique ID of the construct.
        :param airflow_version: 
        :param dag_storage: 
        :param name: 
        :param sizing: 
        :param vpc: 
        :param airflow_configuration_options: 
        :param endpoint_management: 
        :param kms_key: 
        :param logging_configuration: 
        :param security_groups: 
        :param tags: 
        :param webserver_access_mode: 
        :param weekly_maintenance_window_start: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc587b767dfc724460675574ff2adf5d781edef0bcce6da7e68d76012bd53c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EnvironmentProps(
            airflow_version=airflow_version,
            dag_storage=dag_storage,
            name=name,
            sizing=sizing,
            vpc=vpc,
            airflow_configuration_options=airflow_configuration_options,
            endpoint_management=endpoint_management,
            kms_key=kms_key,
            logging_configuration=logging_configuration,
            security_groups=security_groups,
            tags=tags,
            webserver_access_mode=webserver_access_mode,
            weekly_maintenance_window_start=weekly_maintenance_window_start,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(
        self,
        statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    ) -> None:
        '''Adds a policy statement to the execution role's policy.

        :param statement: - The IAM policy statement to add to the role's policy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0979be1ca1dd29bc506f750b97db2634a5864c9d6ab41e834a41ad36343c373)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToRolePolicy", [statement]))

    @jsii.member(jsii_name="enableEmailBackend")
    def enable_email_backend(
        self,
        *,
        from_email: builtins.str,
        conn_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Enables the email backend for Airflow to send email notifications.

        :param from_email: 
        :param conn_id: 
        '''
        options = EmailBackendOptions(from_email=from_email, conn_id=conn_id)

        return typing.cast(None, jsii.invoke(self, "enableEmailBackend", [options]))

    @jsii.member(jsii_name="enableSecretsBackend")
    def enable_secrets_backend(
        self,
        *,
        connections_lookup_pattern: typing.Optional[builtins.str] = None,
        connections_prefix: typing.Optional[builtins.str] = None,
        variables_lookup_pattern: typing.Optional[builtins.str] = None,
        variables_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Enables the use of AWS Secrets Manager as a backend for storing Airflow connections and variables.

        :param connections_lookup_pattern: 
        :param connections_prefix: 
        :param variables_lookup_pattern: 
        :param variables_prefix: 
        '''
        options = SecretsBackendOptions(
            connections_lookup_pattern=connections_lookup_pattern,
            connections_prefix=connections_prefix,
            variables_lookup_pattern=variables_lookup_pattern,
            variables_prefix=variables_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "enableSecretsBackend", [options]))

    @jsii.member(jsii_name="setAirflowConfigurationOption")
    def set_airflow_configuration_option(
        self,
        key: builtins.str,
        value: typing.Any,
    ) -> None:
        '''Sets an Airflow configuration option.

        :param key: - The configuration option key.
        :param value: - The configuration option value.

        :return: void
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9f30a55d827570e6513bf50541c7cfa225d4591c531a693874230f8932899e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setAirflowConfigurationOption", [key, value]))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="celeryExecutorQueue")
    def celery_executor_queue(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "celeryExecutorQueue"))

    @builtins.property
    @jsii.member(jsii_name="dagProcessingLogsGroupArn")
    def dag_processing_logs_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dagProcessingLogsGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="databaseVpcEndpointService")
    def database_vpc_endpoint_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseVpcEndpointService"))

    @builtins.property
    @jsii.member(jsii_name="schedulerLogsGroupArn")
    def scheduler_logs_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedulerLogsGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="taskLogsGroupArn")
    def task_logs_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskLogsGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="webserverLogsGroupArn")
    def webserver_logs_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webserverLogsGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="webserverUrl")
    def webserver_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webserverUrl"))

    @builtins.property
    @jsii.member(jsii_name="webserverVpcEndpointService")
    def webserver_vpc_endpoint_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webserverVpcEndpointService"))

    @builtins.property
    @jsii.member(jsii_name="workerLogsGroupArn")
    def worker_logs_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerLogsGroupArn"))


@jsii.enum(jsii_type="cdk-mwaa.EnvironmentClass")
class EnvironmentClass(enum.Enum):
    '''Represents the available environment classes for MWAA (Managed Workflows for Apache Airflow).'''

    MW1_MICRO = "MW1_MICRO"
    MW1_SMALL = "MW1_SMALL"
    MW1_MEDIUM = "MW1_MEDIUM"
    MW1_LARGE = "MW1_LARGE"


@jsii.data_type(
    jsii_type="cdk-mwaa.EnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "airflow_version": "airflowVersion",
        "dag_storage": "dagStorage",
        "name": "name",
        "sizing": "sizing",
        "vpc": "vpc",
        "airflow_configuration_options": "airflowConfigurationOptions",
        "endpoint_management": "endpointManagement",
        "kms_key": "kmsKey",
        "logging_configuration": "loggingConfiguration",
        "security_groups": "securityGroups",
        "tags": "tags",
        "webserver_access_mode": "webserverAccessMode",
        "weekly_maintenance_window_start": "weeklyMaintenanceWindowStart",
    },
)
class EnvironmentProps:
    def __init__(
        self,
        *,
        airflow_version: builtins.str,
        dag_storage: DagStorage,
        name: builtins.str,
        sizing: "Sizing",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        endpoint_management: typing.Optional[EndpointManagement] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        logging_configuration: typing.Optional[typing.Union["LoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        webserver_access_mode: typing.Optional["WebserverAccessMode"] = None,
        weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for creating an MWAA environment.

        :param airflow_version: 
        :param dag_storage: 
        :param name: 
        :param sizing: 
        :param vpc: 
        :param airflow_configuration_options: 
        :param endpoint_management: 
        :param kms_key: 
        :param logging_configuration: 
        :param security_groups: 
        :param tags: 
        :param webserver_access_mode: 
        :param weekly_maintenance_window_start: 
        '''
        if isinstance(logging_configuration, dict):
            logging_configuration = LoggingConfiguration(**logging_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58cfc6f1183850b5b51999d54a17bf62c6f7b5c3c75133b721818d02e12a9b8)
            check_type(argname="argument airflow_version", value=airflow_version, expected_type=type_hints["airflow_version"])
            check_type(argname="argument dag_storage", value=dag_storage, expected_type=type_hints["dag_storage"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sizing", value=sizing, expected_type=type_hints["sizing"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument airflow_configuration_options", value=airflow_configuration_options, expected_type=type_hints["airflow_configuration_options"])
            check_type(argname="argument endpoint_management", value=endpoint_management, expected_type=type_hints["endpoint_management"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument webserver_access_mode", value=webserver_access_mode, expected_type=type_hints["webserver_access_mode"])
            check_type(argname="argument weekly_maintenance_window_start", value=weekly_maintenance_window_start, expected_type=type_hints["weekly_maintenance_window_start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "airflow_version": airflow_version,
            "dag_storage": dag_storage,
            "name": name,
            "sizing": sizing,
            "vpc": vpc,
        }
        if airflow_configuration_options is not None:
            self._values["airflow_configuration_options"] = airflow_configuration_options
        if endpoint_management is not None:
            self._values["endpoint_management"] = endpoint_management
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tags is not None:
            self._values["tags"] = tags
        if webserver_access_mode is not None:
            self._values["webserver_access_mode"] = webserver_access_mode
        if weekly_maintenance_window_start is not None:
            self._values["weekly_maintenance_window_start"] = weekly_maintenance_window_start

    @builtins.property
    def airflow_version(self) -> builtins.str:
        result = self._values.get("airflow_version")
        assert result is not None, "Required property 'airflow_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dag_storage(self) -> DagStorage:
        result = self._values.get("dag_storage")
        assert result is not None, "Required property 'dag_storage' is missing"
        return typing.cast(DagStorage, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sizing(self) -> "Sizing":
        result = self._values.get("sizing")
        assert result is not None, "Required property 'sizing' is missing"
        return typing.cast("Sizing", result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def airflow_configuration_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        result = self._values.get("airflow_configuration_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def endpoint_management(self) -> typing.Optional[EndpointManagement]:
        result = self._values.get("endpoint_management")
        return typing.cast(typing.Optional[EndpointManagement], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def logging_configuration(self) -> typing.Optional["LoggingConfiguration"]:
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional["LoggingConfiguration"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def webserver_access_mode(self) -> typing.Optional["WebserverAccessMode"]:
        result = self._values.get("webserver_access_mode")
        return typing.cast(typing.Optional["WebserverAccessMode"], result)

    @builtins.property
    def weekly_maintenance_window_start(self) -> typing.Optional[builtins.str]:
        result = self._values.get("weekly_maintenance_window_start")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-mwaa.LogLevel")
class LogLevel(enum.Enum):
    '''Enum for the log level for Apache Airflow.'''

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


@jsii.data_type(
    jsii_type="cdk-mwaa.LoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "dag_processing_logs": "dagProcessingLogs",
        "scheduler_logs": "schedulerLogs",
        "task_logs": "taskLogs",
        "webserver_logs": "webserverLogs",
        "worker_logs": "workerLogs",
    },
)
class LoggingConfiguration:
    def __init__(
        self,
        *,
        dag_processing_logs: typing.Optional[typing.Union["LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        scheduler_logs: typing.Optional[typing.Union["LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        task_logs: typing.Optional[typing.Union["LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        webserver_logs: typing.Optional[typing.Union["LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        worker_logs: typing.Optional[typing.Union["LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Logging configuration for the MWAA environment.

        :param dag_processing_logs: 
        :param scheduler_logs: 
        :param task_logs: 
        :param webserver_logs: 
        :param worker_logs: 
        '''
        if isinstance(dag_processing_logs, dict):
            dag_processing_logs = LoggingConfigurationProperty(**dag_processing_logs)
        if isinstance(scheduler_logs, dict):
            scheduler_logs = LoggingConfigurationProperty(**scheduler_logs)
        if isinstance(task_logs, dict):
            task_logs = LoggingConfigurationProperty(**task_logs)
        if isinstance(webserver_logs, dict):
            webserver_logs = LoggingConfigurationProperty(**webserver_logs)
        if isinstance(worker_logs, dict):
            worker_logs = LoggingConfigurationProperty(**worker_logs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2c2b7229af680332026a2523648e1c7f223df1a7e4c0c75768ae0221551c16)
            check_type(argname="argument dag_processing_logs", value=dag_processing_logs, expected_type=type_hints["dag_processing_logs"])
            check_type(argname="argument scheduler_logs", value=scheduler_logs, expected_type=type_hints["scheduler_logs"])
            check_type(argname="argument task_logs", value=task_logs, expected_type=type_hints["task_logs"])
            check_type(argname="argument webserver_logs", value=webserver_logs, expected_type=type_hints["webserver_logs"])
            check_type(argname="argument worker_logs", value=worker_logs, expected_type=type_hints["worker_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dag_processing_logs is not None:
            self._values["dag_processing_logs"] = dag_processing_logs
        if scheduler_logs is not None:
            self._values["scheduler_logs"] = scheduler_logs
        if task_logs is not None:
            self._values["task_logs"] = task_logs
        if webserver_logs is not None:
            self._values["webserver_logs"] = webserver_logs
        if worker_logs is not None:
            self._values["worker_logs"] = worker_logs

    @builtins.property
    def dag_processing_logs(self) -> typing.Optional["LoggingConfigurationProperty"]:
        result = self._values.get("dag_processing_logs")
        return typing.cast(typing.Optional["LoggingConfigurationProperty"], result)

    @builtins.property
    def scheduler_logs(self) -> typing.Optional["LoggingConfigurationProperty"]:
        result = self._values.get("scheduler_logs")
        return typing.cast(typing.Optional["LoggingConfigurationProperty"], result)

    @builtins.property
    def task_logs(self) -> typing.Optional["LoggingConfigurationProperty"]:
        result = self._values.get("task_logs")
        return typing.cast(typing.Optional["LoggingConfigurationProperty"], result)

    @builtins.property
    def webserver_logs(self) -> typing.Optional["LoggingConfigurationProperty"]:
        result = self._values.get("webserver_logs")
        return typing.cast(typing.Optional["LoggingConfigurationProperty"], result)

    @builtins.property
    def worker_logs(self) -> typing.Optional["LoggingConfigurationProperty"]:
        result = self._values.get("worker_logs")
        return typing.cast(typing.Optional["LoggingConfigurationProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-mwaa.LoggingConfigurationProperty",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "log_level": "logLevel"},
)
class LoggingConfigurationProperty:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        log_level: typing.Optional[LogLevel] = None,
    ) -> None:
        '''Defines the logging configuration properties for various Airflow log types.

        :param enabled: Indicates whether to enable the Apache Airflow log type (e.g. DagProcessingLogs) in CloudWatch Logs.
        :param log_level: Defines the log level for the specified log type (e.g. DagProcessingLogs). Valid values: CRITICAL, ERROR, WARNING, INFO, DEBUG.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e478654aa87904502c267bca96d1a7c0ca8f8e5e749464cb92a7cd1fd2c4b0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if log_level is not None:
            self._values["log_level"] = log_level

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to enable the Apache Airflow log type (e.g. DagProcessingLogs) in CloudWatch Logs.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_level(self) -> typing.Optional[LogLevel]:
        '''Defines the log level for the specified log type (e.g. DagProcessingLogs). Valid values: CRITICAL, ERROR, WARNING, INFO, DEBUG.'''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[LogLevel], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingConfigurationProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-mwaa.MWAAProps",
    jsii_struct_bases=[],
    name_mapping={
        "airflow_version": "airflowVersion",
        "environment_name": "environmentName",
        "airflow_configuration_options": "airflowConfigurationOptions",
        "bucket_name": "bucketName",
        "dags_config": "dagsConfig",
        "plugins_config": "pluginsConfig",
        "removal_policy": "removalPolicy",
        "requirements_config": "requirementsConfig",
        "sizing": "sizing",
        "startup_script_config": "startupScriptConfig",
        "vpc": "vpc",
    },
)
class MWAAProps:
    def __init__(
        self,
        *,
        airflow_version: builtins.str,
        environment_name: builtins.str,
        airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        dags_config: typing.Optional[typing.Union[DagStorageConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        plugins_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        requirements_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        sizing: typing.Optional["Sizing"] = None,
        startup_script_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''Interface defining the properties for configuring MWAA (Managed Airflow).

        :param airflow_version: The version of Airflow to deploy.
        :param environment_name: The name of the Airflow environment.
        :param airflow_configuration_options: Airflow configuration options as key-value pairs. These configuration options are passed to the Airflow environment.
        :param bucket_name: The name of the S3 bucket used for storing DAGs. If not provided, a default bucket is created.
        :param dags_config: Configuration for DAG storage.
        :param plugins_config: Configuration for plugins storage.
        :param removal_policy: The removal policy for the MWAA resources. Determines what happens to the resources when they are deleted. Defaults to 'RETAIN' if not specified.
        :param requirements_config: Configuration for requirements storage.
        :param sizing: Optional sizing configuration for the MWAA environment. Defines the compute resources.
        :param startup_script_config: Configuration for startup script storage.
        :param vpc: The VPC in which to deploy the MWAA environment. If not provided, a default VPC will be created.
        '''
        if isinstance(dags_config, dict):
            dags_config = DagStorageConfigOptions(**dags_config)
        if isinstance(plugins_config, dict):
            plugins_config = DagStorageConfigOptionsWithS3ObjectVersion(**plugins_config)
        if isinstance(requirements_config, dict):
            requirements_config = DagStorageConfigOptionsWithS3ObjectVersion(**requirements_config)
        if isinstance(startup_script_config, dict):
            startup_script_config = DagStorageConfigOptionsWithS3ObjectVersion(**startup_script_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73d818937427f32bb22179ff7d13eb6aa0201131959780924f6ec21b94dd128)
            check_type(argname="argument airflow_version", value=airflow_version, expected_type=type_hints["airflow_version"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument airflow_configuration_options", value=airflow_configuration_options, expected_type=type_hints["airflow_configuration_options"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument dags_config", value=dags_config, expected_type=type_hints["dags_config"])
            check_type(argname="argument plugins_config", value=plugins_config, expected_type=type_hints["plugins_config"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument requirements_config", value=requirements_config, expected_type=type_hints["requirements_config"])
            check_type(argname="argument sizing", value=sizing, expected_type=type_hints["sizing"])
            check_type(argname="argument startup_script_config", value=startup_script_config, expected_type=type_hints["startup_script_config"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "airflow_version": airflow_version,
            "environment_name": environment_name,
        }
        if airflow_configuration_options is not None:
            self._values["airflow_configuration_options"] = airflow_configuration_options
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if dags_config is not None:
            self._values["dags_config"] = dags_config
        if plugins_config is not None:
            self._values["plugins_config"] = plugins_config
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if requirements_config is not None:
            self._values["requirements_config"] = requirements_config
        if sizing is not None:
            self._values["sizing"] = sizing
        if startup_script_config is not None:
            self._values["startup_script_config"] = startup_script_config
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def airflow_version(self) -> builtins.str:
        '''The version of Airflow to deploy.'''
        result = self._values.get("airflow_version")
        assert result is not None, "Required property 'airflow_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment_name(self) -> builtins.str:
        '''The name of the Airflow environment.'''
        result = self._values.get("environment_name")
        assert result is not None, "Required property 'environment_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def airflow_configuration_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Airflow configuration options as key-value pairs.

        These configuration options are passed to the Airflow environment.
        '''
        result = self._values.get("airflow_configuration_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the S3 bucket used for storing DAGs.

        If not provided, a default bucket is created.
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dags_config(self) -> typing.Optional[DagStorageConfigOptions]:
        '''Configuration for DAG storage.'''
        result = self._values.get("dags_config")
        return typing.cast(typing.Optional[DagStorageConfigOptions], result)

    @builtins.property
    def plugins_config(
        self,
    ) -> typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion]:
        '''Configuration for plugins storage.'''
        result = self._values.get("plugins_config")
        return typing.cast(typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy for the MWAA resources.

        Determines what happens to the resources when they are deleted.
        Defaults to 'RETAIN' if not specified.
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def requirements_config(
        self,
    ) -> typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion]:
        '''Configuration for requirements storage.'''
        result = self._values.get("requirements_config")
        return typing.cast(typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion], result)

    @builtins.property
    def sizing(self) -> typing.Optional["Sizing"]:
        '''Optional sizing configuration for the MWAA environment.

        Defines the compute resources.
        '''
        result = self._values.get("sizing")
        return typing.cast(typing.Optional["Sizing"], result)

    @builtins.property
    def startup_script_config(
        self,
    ) -> typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion]:
        '''Configuration for startup script storage.'''
        result = self._values.get("startup_script_config")
        return typing.cast(typing.Optional[DagStorageConfigOptionsWithS3ObjectVersion], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''The VPC in which to deploy the MWAA environment.

        If not provided, a default VPC will be created.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MWAAProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PublicRoutingMWAA(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-mwaa.PublicRoutingMWAA",
):
    '''PublicRoutingMWAA constructs a Managed Airflow (MWAA) environment with public webserver access.

    It creates the necessary VPC, S3 storage for DAGs, and an Airflow environment.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        airflow_version: builtins.str,
        environment_name: builtins.str,
        airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        dags_config: typing.Optional[typing.Union[DagStorageConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        plugins_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        requirements_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        sizing: typing.Optional["Sizing"] = None,
        startup_script_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param airflow_version: The version of Airflow to deploy.
        :param environment_name: The name of the Airflow environment.
        :param airflow_configuration_options: Airflow configuration options as key-value pairs. These configuration options are passed to the Airflow environment.
        :param bucket_name: The name of the S3 bucket used for storing DAGs. If not provided, a default bucket is created.
        :param dags_config: Configuration for DAG storage.
        :param plugins_config: Configuration for plugins storage.
        :param removal_policy: The removal policy for the MWAA resources. Determines what happens to the resources when they are deleted. Defaults to 'RETAIN' if not specified.
        :param requirements_config: Configuration for requirements storage.
        :param sizing: Optional sizing configuration for the MWAA environment. Defines the compute resources.
        :param startup_script_config: Configuration for startup script storage.
        :param vpc: The VPC in which to deploy the MWAA environment. If not provided, a default VPC will be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5715af45a5664383ddb469b7bffe2c8a7d75c3dfe608847aae4c9fd79f034c9e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MWAAProps(
            airflow_version=airflow_version,
            environment_name=environment_name,
            airflow_configuration_options=airflow_configuration_options,
            bucket_name=bucket_name,
            dags_config=dags_config,
            plugins_config=plugins_config,
            removal_policy=removal_policy,
            requirements_config=requirements_config,
            sizing=sizing,
            startup_script_config=startup_script_config,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-mwaa.SecretsBackendOptions",
    jsii_struct_bases=[],
    name_mapping={
        "connections_lookup_pattern": "connectionsLookupPattern",
        "connections_prefix": "connectionsPrefix",
        "variables_lookup_pattern": "variablesLookupPattern",
        "variables_prefix": "variablesPrefix",
    },
)
class SecretsBackendOptions:
    def __init__(
        self,
        *,
        connections_lookup_pattern: typing.Optional[builtins.str] = None,
        connections_prefix: typing.Optional[builtins.str] = None,
        variables_lookup_pattern: typing.Optional[builtins.str] = None,
        variables_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for configuring the Secrets backend.

        :param connections_lookup_pattern: 
        :param connections_prefix: 
        :param variables_lookup_pattern: 
        :param variables_prefix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a26a4745b2f3c0bf73fea3716d2c2582a993bce95da0be81eb790bf091aa13)
            check_type(argname="argument connections_lookup_pattern", value=connections_lookup_pattern, expected_type=type_hints["connections_lookup_pattern"])
            check_type(argname="argument connections_prefix", value=connections_prefix, expected_type=type_hints["connections_prefix"])
            check_type(argname="argument variables_lookup_pattern", value=variables_lookup_pattern, expected_type=type_hints["variables_lookup_pattern"])
            check_type(argname="argument variables_prefix", value=variables_prefix, expected_type=type_hints["variables_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connections_lookup_pattern is not None:
            self._values["connections_lookup_pattern"] = connections_lookup_pattern
        if connections_prefix is not None:
            self._values["connections_prefix"] = connections_prefix
        if variables_lookup_pattern is not None:
            self._values["variables_lookup_pattern"] = variables_lookup_pattern
        if variables_prefix is not None:
            self._values["variables_prefix"] = variables_prefix

    @builtins.property
    def connections_lookup_pattern(self) -> typing.Optional[builtins.str]:
        result = self._values.get("connections_lookup_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connections_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("connections_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables_lookup_pattern(self) -> typing.Optional[builtins.str]:
        result = self._values.get("variables_lookup_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variables_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("variables_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretsBackendOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityGroup(
    _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-mwaa.SecurityGroup",
):
    '''A custom Security Group with a self-referencing ingress rule for MWAA.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        disable_inline_rules: typing.Optional[builtins.bool] = None,
        security_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new Security Group with self-referencing ingress rules.

        :param scope: The parent construct.
        :param id: The unique identifier for this construct.
        :param vpc: The VPC in which to create the security group.
        :param allow_all_ipv6_outbound: Whether to allow all outbound ipv6 traffic by default. If this is set to true, there will only be a single egress rule which allows all outbound ipv6 traffic. If this is set to false, no outbound traffic will be allowed by default and all egress ipv6 traffic must be explicitly authorized. To allow all ipv4 traffic use allowAllOutbound Default: false
        :param allow_all_outbound: Whether to allow all outbound traffic by default. If this is set to true, there will only be a single egress rule which allows all outbound traffic. If this is set to false, no outbound traffic will be allowed by default and all egress traffic must be explicitly authorized. To allow all ipv6 traffic use allowAllIpv6Outbound Default: true
        :param description: A description of the security group. Default: The default name will be the construct's CDK path.
        :param disable_inline_rules: Whether to disable inline ingress and egress rule optimization. If this is set to true, ingress and egress rules will not be declared under the SecurityGroup in cloudformation, but will be separate elements. Inlining rules is an optimization for producing smaller stack templates. Sometimes this is not desirable, for example when security group access is managed via tags. The default value can be overridden globally by setting the context variable '@aws-cdk/aws-ec2.securityGroupDisableInlineRules'. Default: false
        :param security_group_name: The name of the security group. For valid values, see the GroupName parameter of the CreateSecurityGroup action in the Amazon EC2 API Reference. It is not recommended to use an explicit group name. Default: If you don't specify a GroupName, AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c0edc0cc9086762fba282b3b093245709fb50595ba3be1a94386b8ffc61a0b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecurityGroupProps(
            vpc=vpc,
            allow_all_ipv6_outbound=allow_all_ipv6_outbound,
            allow_all_outbound=allow_all_outbound,
            description=description,
            disable_inline_rules=disable_inline_rules,
            security_group_name=security_group_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-mwaa.SecurityGroupProps",
    jsii_struct_bases=[_aws_cdk_aws_ec2_ceddda9d.SecurityGroupProps],
    name_mapping={
        "vpc": "vpc",
        "allow_all_ipv6_outbound": "allowAllIpv6Outbound",
        "allow_all_outbound": "allowAllOutbound",
        "description": "description",
        "disable_inline_rules": "disableInlineRules",
        "security_group_name": "securityGroupName",
    },
)
class SecurityGroupProps(_aws_cdk_aws_ec2_ceddda9d.SecurityGroupProps):
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        disable_inline_rules: typing.Optional[builtins.bool] = None,
        security_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a Security Group.

        :param vpc: The VPC in which to create the security group.
        :param allow_all_ipv6_outbound: Whether to allow all outbound ipv6 traffic by default. If this is set to true, there will only be a single egress rule which allows all outbound ipv6 traffic. If this is set to false, no outbound traffic will be allowed by default and all egress ipv6 traffic must be explicitly authorized. To allow all ipv4 traffic use allowAllOutbound Default: false
        :param allow_all_outbound: Whether to allow all outbound traffic by default. If this is set to true, there will only be a single egress rule which allows all outbound traffic. If this is set to false, no outbound traffic will be allowed by default and all egress traffic must be explicitly authorized. To allow all ipv6 traffic use allowAllIpv6Outbound Default: true
        :param description: A description of the security group. Default: The default name will be the construct's CDK path.
        :param disable_inline_rules: Whether to disable inline ingress and egress rule optimization. If this is set to true, ingress and egress rules will not be declared under the SecurityGroup in cloudformation, but will be separate elements. Inlining rules is an optimization for producing smaller stack templates. Sometimes this is not desirable, for example when security group access is managed via tags. The default value can be overridden globally by setting the context variable '@aws-cdk/aws-ec2.securityGroupDisableInlineRules'. Default: false
        :param security_group_name: The name of the security group. For valid values, see the GroupName parameter of the CreateSecurityGroup action in the Amazon EC2 API Reference. It is not recommended to use an explicit group name. Default: If you don't specify a GroupName, AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc85564bef1cef94bed0ad8e10d0c4a5b9d253034b927359a0c50ae7fbafa03)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument allow_all_ipv6_outbound", value=allow_all_ipv6_outbound, expected_type=type_hints["allow_all_ipv6_outbound"])
            check_type(argname="argument allow_all_outbound", value=allow_all_outbound, expected_type=type_hints["allow_all_outbound"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_inline_rules", value=disable_inline_rules, expected_type=type_hints["disable_inline_rules"])
            check_type(argname="argument security_group_name", value=security_group_name, expected_type=type_hints["security_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if allow_all_ipv6_outbound is not None:
            self._values["allow_all_ipv6_outbound"] = allow_all_ipv6_outbound
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if description is not None:
            self._values["description"] = description
        if disable_inline_rules is not None:
            self._values["disable_inline_rules"] = disable_inline_rules
        if security_group_name is not None:
            self._values["security_group_name"] = security_group_name

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC in which to create the security group.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def allow_all_ipv6_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow all outbound ipv6 traffic by default.

        If this is set to true, there will only be a single egress rule which allows all
        outbound ipv6 traffic. If this is set to false, no outbound traffic will be allowed by
        default and all egress ipv6 traffic must be explicitly authorized.

        To allow all ipv4 traffic use allowAllOutbound

        :default: false
        '''
        result = self._values.get("allow_all_ipv6_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow all outbound traffic by default.

        If this is set to true, there will only be a single egress rule which allows all
        outbound traffic. If this is set to false, no outbound traffic will be allowed by
        default and all egress traffic must be explicitly authorized.

        To allow all ipv6 traffic use allowAllIpv6Outbound

        :default: true
        '''
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the security group.

        :default: The default name will be the construct's CDK path.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_inline_rules(self) -> typing.Optional[builtins.bool]:
        '''Whether to disable inline ingress and egress rule optimization.

        If this is set to true, ingress and egress rules will not be declared under the
        SecurityGroup in cloudformation, but will be separate elements.

        Inlining rules is an optimization for producing smaller stack templates. Sometimes
        this is not desirable, for example when security group access is managed via tags.

        The default value can be overridden globally by setting the context variable
        '@aws-cdk/aws-ec2.securityGroupDisableInlineRules'.

        :default: false
        '''
        result = self._values.get("disable_inline_rules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the security group.

        For valid values, see the GroupName
        parameter of the CreateSecurityGroup action in the Amazon EC2 API
        Reference.

        It is not recommended to use an explicit group name.

        :default:

        If you don't specify a GroupName, AWS CloudFormation generates a
        unique physical ID and uses that ID for the group name.
        '''
        result = self._values.get("security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Sizing(metaclass=jsii.JSIIMeta, jsii_type="cdk-mwaa.Sizing"):
    '''Provides predefined and customizable sizing options for an MWAA environment.'''

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(
        cls,
        *,
        environment_class: EnvironmentClass,
        max_webservers: jsii.Number,
        max_workers: jsii.Number,
        min_webservers: jsii.Number,
        min_workers: jsii.Number,
        schedulers: jsii.Number,
    ) -> "Sizing":
        '''Creates a custom-sized MWAA environment based on user-defined configuration.

        :param environment_class: The environment class determining the available resources.
        :param max_webservers: Maximum number of webservers in the MWAA environment.
        :param max_workers: Maximum number of workers in the MWAA environment.
        :param min_webservers: Minimum number of webservers in the MWAA environment.
        :param min_workers: Minimum number of workers in the MWAA environment.
        :param schedulers: Number of schedulers in the MWAA environment.
        '''
        config = SizingProps(
            environment_class=environment_class,
            max_webservers=max_webservers,
            max_workers=max_workers,
            min_webservers=min_webservers,
            min_workers=min_workers,
            schedulers=schedulers,
        )

        return typing.cast("Sizing", jsii.sinvoke(cls, "custom", [config]))

    @jsii.member(jsii_name="mw1Large")
    @builtins.classmethod
    def mw1_large(cls) -> "Sizing":
        '''Creates an MW1_LARGE sized environment with a predefined range of workers and webservers.'''
        return typing.cast("Sizing", jsii.sinvoke(cls, "mw1Large", []))

    @jsii.member(jsii_name="mw1Medium")
    @builtins.classmethod
    def mw1_medium(cls) -> "Sizing":
        '''Creates an MW1_MEDIUM sized environment with a predefined range of workers and webservers.'''
        return typing.cast("Sizing", jsii.sinvoke(cls, "mw1Medium", []))

    @jsii.member(jsii_name="mw1Micro")
    @builtins.classmethod
    def mw1_micro(cls) -> "Sizing":
        '''Creates an MW1_MICRO sized environment with a single worker, webserver, and scheduler.'''
        return typing.cast("Sizing", jsii.sinvoke(cls, "mw1Micro", []))

    @jsii.member(jsii_name="mw1Small")
    @builtins.classmethod
    def mw1_small(cls) -> "Sizing":
        '''Creates an MW1_SMALL sized environment with a predefined range of workers and webservers.'''
        return typing.cast("Sizing", jsii.sinvoke(cls, "mw1Small", []))

    @builtins.property
    @jsii.member(jsii_name="environmentClass")
    def environment_class(self) -> EnvironmentClass:
        '''Returns the environment class.'''
        return typing.cast(EnvironmentClass, jsii.get(self, "environmentClass"))

    @builtins.property
    @jsii.member(jsii_name="maxWebservers")
    def max_webservers(self) -> jsii.Number:
        '''Returns the maximum number of webservers.'''
        return typing.cast(jsii.Number, jsii.get(self, "maxWebservers"))

    @builtins.property
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> jsii.Number:
        '''Returns the maximum number of workers.'''
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkers"))

    @builtins.property
    @jsii.member(jsii_name="minWebservers")
    def min_webservers(self) -> jsii.Number:
        '''Returns the minimum number of webservers.'''
        return typing.cast(jsii.Number, jsii.get(self, "minWebservers"))

    @builtins.property
    @jsii.member(jsii_name="minWorkers")
    def min_workers(self) -> jsii.Number:
        '''Returns the minimum number of workers.'''
        return typing.cast(jsii.Number, jsii.get(self, "minWorkers"))

    @builtins.property
    @jsii.member(jsii_name="schedulers")
    def schedulers(self) -> jsii.Number:
        '''Returns the number of schedulers.'''
        return typing.cast(jsii.Number, jsii.get(self, "schedulers"))


@jsii.data_type(
    jsii_type="cdk-mwaa.SizingProps",
    jsii_struct_bases=[],
    name_mapping={
        "environment_class": "environmentClass",
        "max_webservers": "maxWebservers",
        "max_workers": "maxWorkers",
        "min_webservers": "minWebservers",
        "min_workers": "minWorkers",
        "schedulers": "schedulers",
    },
)
class SizingProps:
    def __init__(
        self,
        *,
        environment_class: EnvironmentClass,
        max_webservers: jsii.Number,
        max_workers: jsii.Number,
        min_webservers: jsii.Number,
        min_workers: jsii.Number,
        schedulers: jsii.Number,
    ) -> None:
        '''Defines the configuration properties for sizing an MWAA environment.

        :param environment_class: The environment class determining the available resources.
        :param max_webservers: Maximum number of webservers in the MWAA environment.
        :param max_workers: Maximum number of workers in the MWAA environment.
        :param min_webservers: Minimum number of webservers in the MWAA environment.
        :param min_workers: Minimum number of workers in the MWAA environment.
        :param schedulers: Number of schedulers in the MWAA environment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__379e3b2e8fe393bf82766c342457e207198846f531bd3cef817a10a9a171a08d)
            check_type(argname="argument environment_class", value=environment_class, expected_type=type_hints["environment_class"])
            check_type(argname="argument max_webservers", value=max_webservers, expected_type=type_hints["max_webservers"])
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument min_webservers", value=min_webservers, expected_type=type_hints["min_webservers"])
            check_type(argname="argument min_workers", value=min_workers, expected_type=type_hints["min_workers"])
            check_type(argname="argument schedulers", value=schedulers, expected_type=type_hints["schedulers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "environment_class": environment_class,
            "max_webservers": max_webservers,
            "max_workers": max_workers,
            "min_webservers": min_webservers,
            "min_workers": min_workers,
            "schedulers": schedulers,
        }

    @builtins.property
    def environment_class(self) -> EnvironmentClass:
        '''The environment class determining the available resources.'''
        result = self._values.get("environment_class")
        assert result is not None, "Required property 'environment_class' is missing"
        return typing.cast(EnvironmentClass, result)

    @builtins.property
    def max_webservers(self) -> jsii.Number:
        '''Maximum number of webservers in the MWAA environment.'''
        result = self._values.get("max_webservers")
        assert result is not None, "Required property 'max_webservers' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_workers(self) -> jsii.Number:
        '''Maximum number of workers in the MWAA environment.'''
        result = self._values.get("max_workers")
        assert result is not None, "Required property 'max_workers' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_webservers(self) -> jsii.Number:
        '''Minimum number of webservers in the MWAA environment.'''
        result = self._values.get("min_webservers")
        assert result is not None, "Required property 'min_webservers' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_workers(self) -> jsii.Number:
        '''Minimum number of workers in the MWAA environment.'''
        result = self._values.get("min_workers")
        assert result is not None, "Required property 'min_workers' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def schedulers(self) -> jsii.Number:
        '''Number of schedulers in the MWAA environment.'''
        result = self._values.get("schedulers")
        assert result is not None, "Required property 'schedulers' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SizingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-mwaa.WebserverAccessMode")
class WebserverAccessMode(enum.Enum):
    '''Enum for the webserver access mode of the MWAA environment.'''

    PRIVATE_ONLY = "PRIVATE_ONLY"
    PUBLIC_ONLY = "PUBLIC_ONLY"


__all__ = [
    "DagStorage",
    "DagStorageConfigOptions",
    "DagStorageConfigOptionsWithS3ObjectVersion",
    "DagStorageDeployOptions",
    "DagStorageProps",
    "EmailBackendOptions",
    "EndpointManagement",
    "Environment",
    "EnvironmentClass",
    "EnvironmentProps",
    "LogLevel",
    "LoggingConfiguration",
    "LoggingConfigurationProperty",
    "MWAAProps",
    "PublicRoutingMWAA",
    "SecretsBackendOptions",
    "SecurityGroup",
    "SecurityGroupProps",
    "Sizing",
    "SizingProps",
    "WebserverAccessMode",
]

publication.publish()

def _typecheckingstub__95a166027e8ebcfead2708b1c3388e60862a4fb6d86763bf56854f275bdd2390(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    dags_config: typing.Optional[typing.Union[DagStorageConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    noncurrent_version_expiration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    plugins_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    requirements_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    startup_script_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    versioned: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a9b5242a26a2093aa8052dd8b86bea06801d5a767c2e5f908776c3f849eb63(
    *,
    s3_path: builtins.str,
    deploy_options: typing.Optional[typing.Union[DagStorageDeployOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd77af7d832e6c1f66f71849ff7971c010e8282b5b3a43d573c7892c43539cf(
    *,
    s3_path: builtins.str,
    deploy_options: typing.Optional[typing.Union[DagStorageDeployOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4eb47db99cbba877092424afc09de8c308a38be2c61e698dd0c28933b9c3b42(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    prune: typing.Optional[builtins.bool] = None,
    retain_on_delete: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4bace9647a9566f3af4198e17ef015306e92a6d5f673b579ba6fdfcb5231da(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    dags_config: typing.Optional[typing.Union[DagStorageConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    noncurrent_version_expiration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    plugins_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    requirements_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    startup_script_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    versioned: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e90f0cf9b9873d2646653b49d16d81a04d7e328760c253beb412d5e74258d3(
    *,
    from_email: builtins.str,
    conn_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc587b767dfc724460675574ff2adf5d781edef0bcce6da7e68d76012bd53c2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    airflow_version: builtins.str,
    dag_storage: DagStorage,
    name: builtins.str,
    sizing: Sizing,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    endpoint_management: typing.Optional[EndpointManagement] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    logging_configuration: typing.Optional[typing.Union[LoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    webserver_access_mode: typing.Optional[WebserverAccessMode] = None,
    weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0979be1ca1dd29bc506f750b97db2634a5864c9d6ab41e834a41ad36343c373(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9f30a55d827570e6513bf50541c7cfa225d4591c531a693874230f8932899e(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58cfc6f1183850b5b51999d54a17bf62c6f7b5c3c75133b721818d02e12a9b8(
    *,
    airflow_version: builtins.str,
    dag_storage: DagStorage,
    name: builtins.str,
    sizing: Sizing,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    endpoint_management: typing.Optional[EndpointManagement] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    logging_configuration: typing.Optional[typing.Union[LoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    webserver_access_mode: typing.Optional[WebserverAccessMode] = None,
    weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2c2b7229af680332026a2523648e1c7f223df1a7e4c0c75768ae0221551c16(
    *,
    dag_processing_logs: typing.Optional[typing.Union[LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduler_logs: typing.Optional[typing.Union[LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    task_logs: typing.Optional[typing.Union[LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    webserver_logs: typing.Optional[typing.Union[LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    worker_logs: typing.Optional[typing.Union[LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e478654aa87904502c267bca96d1a7c0ca8f8e5e749464cb92a7cd1fd2c4b0(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    log_level: typing.Optional[LogLevel] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73d818937427f32bb22179ff7d13eb6aa0201131959780924f6ec21b94dd128(
    *,
    airflow_version: builtins.str,
    environment_name: builtins.str,
    airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    dags_config: typing.Optional[typing.Union[DagStorageConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    plugins_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    requirements_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    sizing: typing.Optional[Sizing] = None,
    startup_script_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5715af45a5664383ddb469b7bffe2c8a7d75c3dfe608847aae4c9fd79f034c9e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    airflow_version: builtins.str,
    environment_name: builtins.str,
    airflow_configuration_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    dags_config: typing.Optional[typing.Union[DagStorageConfigOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    plugins_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    requirements_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    sizing: typing.Optional[Sizing] = None,
    startup_script_config: typing.Optional[typing.Union[DagStorageConfigOptionsWithS3ObjectVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a26a4745b2f3c0bf73fea3716d2c2582a993bce95da0be81eb790bf091aa13(
    *,
    connections_lookup_pattern: typing.Optional[builtins.str] = None,
    connections_prefix: typing.Optional[builtins.str] = None,
    variables_lookup_pattern: typing.Optional[builtins.str] = None,
    variables_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c0edc0cc9086762fba282b3b093245709fb50595ba3be1a94386b8ffc61a0b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    disable_inline_rules: typing.Optional[builtins.bool] = None,
    security_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc85564bef1cef94bed0ad8e10d0c4a5b9d253034b927359a0c50ae7fbafa03(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    disable_inline_rules: typing.Optional[builtins.bool] = None,
    security_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379e3b2e8fe393bf82766c342457e207198846f531bd3cef817a10a9a171a08d(
    *,
    environment_class: EnvironmentClass,
    max_webservers: jsii.Number,
    max_workers: jsii.Number,
    min_webservers: jsii.Number,
    min_workers: jsii.Number,
    schedulers: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
