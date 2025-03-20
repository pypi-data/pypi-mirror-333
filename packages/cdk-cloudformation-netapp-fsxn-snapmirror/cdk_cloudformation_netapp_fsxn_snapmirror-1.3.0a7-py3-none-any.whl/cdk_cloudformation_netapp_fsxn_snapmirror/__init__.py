r'''
# netapp-fsxn-snapmirror

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NetApp::FSxN::SnapMirror` v1.3.0.

## Description

FSx for ONTAP offers SnapMirror for efficient data replication between file systems, aiding in data protection, disaster recovery, and long-term retention. To use SnapMirror, set up cluster peering and SVM peering between the source and target FSx for ONTAP file systems. Once activated, you need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you must first create the Link module.

## References

* [Source](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NetApp::FSxN::SnapMirror \
  --publisher-id a25d267c2b9b86b8d408fce3c7a4d94d34c90946 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/a25d267c2b9b86b8d408fce3c7a4d94d34c90946/NetApp-FSxN-SnapMirror \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NetApp::FSxN::SnapMirror`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnetapp-fsxn-snapmirror+v1.3.0).
* Issues related to `NetApp::FSxN::SnapMirror` should be reported to the [publisher](https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider).

## License

Distributed under the Apache-2.0 License.
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
import constructs as _constructs_77d1e7e8


class CfnSnapMirror(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.CfnSnapMirror",
):
    '''A CloudFormation ``NetApp::FSxN::SnapMirror``.

    :cloudformationResource: NetApp::FSxN::SnapMirror
    :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        fsxn_destination_info: typing.Union["FsxnDestination", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
        policy: builtins.str,
        snap_mirror_endpoint: typing.Union["Endpoint", typing.Dict[builtins.str, typing.Any]],
        snap_mirror_source_endpoint: typing.Union["Endpoint", typing.Dict[builtins.str, typing.Any]],
        healthy_status: typing.Optional[typing.Union["HealthyStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        reverse: typing.Optional[builtins.bool] = None,
        snap_mirror_destination_creation: typing.Optional[typing.Union["SnapMirrorDestinationCreation", typing.Dict[builtins.str, typing.Any]]] = None,
        state_action: typing.Optional["CfnSnapMirrorPropsStateAction"] = None,
        throttle: typing.Optional[jsii.Number] = None,
        transfer_schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``NetApp::FSxN::SnapMirror``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param fsxn_destination_info: The destination information for the Cluster Peer relationship.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param policy: The SnapMirror policy to be used for the SnapMirror relationship.
        :param snap_mirror_endpoint: Destination endpoint of a SnapMirror relationship.
        :param snap_mirror_source_endpoint: Source endpoint of a SnapMirror relationship.
        :param healthy_status: The health status of the SnapMirror relationship.
        :param reverse: Reverse the direction of relationship by making the source endpoint as the new destination endpoint and making the destination endpoint as the new source endpoint. Can be set during modify only.
        :param snap_mirror_destination_creation: Use this object to provision the destination endpoint when establishing a SnapMirror relationship for a volume. For FlexGroup SnapMirror relationships, the source and destination FlexGroups must be spread over the same number of aggregates with the same number of constituents per aggregate.
        :param state_action: Modify the SnapMirror replication status using 'StateAction' in the CloudFormation template when the relationship exists. Follow ONTAP protocol: set to 'paused' to pause, 'snapmirrored' to resync, and 'update' to trigger the transfer API. For subsequent updates, first clear the prior 'StateAction' then set it again.
        :param throttle: Throttle, in KBs per second. This 'throttle' overrides the 'throttle' set on the SnapMirror relationship's policy. If neither of these are set, the throttle defaults to 0, which is interpreted as unlimited.
        :param transfer_schedule: Schedule used to update asynchronous relationships. This 'transfer_schedule' overrides the 'transfer_schedule' set on the SnapMirror relationship's policy. Remove the property to revert. Only cron schedules are supported for SnapMirror.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea53c0cdeb8c48c40c150b8f59b02c7fc809429230ef6c4883bd12fed52937f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSnapMirrorProps(
            file_system_id=file_system_id,
            fsx_admin_password_source=fsx_admin_password_source,
            fsxn_destination_info=fsxn_destination_info,
            link_arn=link_arn,
            policy=policy,
            snap_mirror_endpoint=snap_mirror_endpoint,
            snap_mirror_source_endpoint=snap_mirror_source_endpoint,
            healthy_status=healthy_status,
            reverse=reverse,
            snap_mirror_destination_creation=snap_mirror_destination_creation,
            state_action=state_action,
            throttle=throttle,
            transfer_schedule=transfer_schedule,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDestinationPath")
    def attr_destination_path(self) -> builtins.str:
        '''Attribute ``NetApp::FSxN::SnapMirror.DestinationPath``.

        :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDestinationPath"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``NetApp::FSxN::SnapMirror.ID``.

        :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrSourcePath")
    def attr_source_path(self) -> builtins.str:
        '''Attribute ``NetApp::FSxN::SnapMirror.SourcePath``.

        :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourcePath"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''Attribute ``NetApp::FSxN::SnapMirror.State``.

        :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrUuid")
    def attr_uuid(self) -> builtins.str:
        '''Attribute ``NetApp::FSxN::SnapMirror.UUID``.

        :link: https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUuid"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnSnapMirrorProps":
        '''Resource props.'''
        return typing.cast("CfnSnapMirrorProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.CfnSnapMirrorProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "fsx_admin_password_source": "fsxAdminPasswordSource",
        "fsxn_destination_info": "fsxnDestinationInfo",
        "link_arn": "linkArn",
        "policy": "policy",
        "snap_mirror_endpoint": "snapMirrorEndpoint",
        "snap_mirror_source_endpoint": "snapMirrorSourceEndpoint",
        "healthy_status": "healthyStatus",
        "reverse": "reverse",
        "snap_mirror_destination_creation": "snapMirrorDestinationCreation",
        "state_action": "stateAction",
        "throttle": "throttle",
        "transfer_schedule": "transferSchedule",
    },
)
class CfnSnapMirrorProps:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        fsxn_destination_info: typing.Union["FsxnDestination", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
        policy: builtins.str,
        snap_mirror_endpoint: typing.Union["Endpoint", typing.Dict[builtins.str, typing.Any]],
        snap_mirror_source_endpoint: typing.Union["Endpoint", typing.Dict[builtins.str, typing.Any]],
        healthy_status: typing.Optional[typing.Union["HealthyStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        reverse: typing.Optional[builtins.bool] = None,
        snap_mirror_destination_creation: typing.Optional[typing.Union["SnapMirrorDestinationCreation", typing.Dict[builtins.str, typing.Any]]] = None,
        state_action: typing.Optional["CfnSnapMirrorPropsStateAction"] = None,
        throttle: typing.Optional[jsii.Number] = None,
        transfer_schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''FSx for ONTAP offers SnapMirror for efficient data replication between file systems, aiding in data protection, disaster recovery, and long-term retention.

        To use SnapMirror, set up cluster peering and SVM peering between the source and target FSx for ONTAP file systems. Once activated, you need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you must first create the Link module.

        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param fsxn_destination_info: The destination information for the Cluster Peer relationship.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.
        :param policy: The SnapMirror policy to be used for the SnapMirror relationship.
        :param snap_mirror_endpoint: Destination endpoint of a SnapMirror relationship.
        :param snap_mirror_source_endpoint: Source endpoint of a SnapMirror relationship.
        :param healthy_status: The health status of the SnapMirror relationship.
        :param reverse: Reverse the direction of relationship by making the source endpoint as the new destination endpoint and making the destination endpoint as the new source endpoint. Can be set during modify only.
        :param snap_mirror_destination_creation: Use this object to provision the destination endpoint when establishing a SnapMirror relationship for a volume. For FlexGroup SnapMirror relationships, the source and destination FlexGroups must be spread over the same number of aggregates with the same number of constituents per aggregate.
        :param state_action: Modify the SnapMirror replication status using 'StateAction' in the CloudFormation template when the relationship exists. Follow ONTAP protocol: set to 'paused' to pause, 'snapmirrored' to resync, and 'update' to trigger the transfer API. For subsequent updates, first clear the prior 'StateAction' then set it again.
        :param throttle: Throttle, in KBs per second. This 'throttle' overrides the 'throttle' set on the SnapMirror relationship's policy. If neither of these are set, the throttle defaults to 0, which is interpreted as unlimited.
        :param transfer_schedule: Schedule used to update asynchronous relationships. This 'transfer_schedule' overrides the 'transfer_schedule' set on the SnapMirror relationship's policy. Remove the property to revert. Only cron schedules are supported for SnapMirror.

        :schema: CfnSnapMirrorProps
        '''
        if isinstance(fsx_admin_password_source, dict):
            fsx_admin_password_source = PasswordSource(**fsx_admin_password_source)
        if isinstance(fsxn_destination_info, dict):
            fsxn_destination_info = FsxnDestination(**fsxn_destination_info)
        if isinstance(snap_mirror_endpoint, dict):
            snap_mirror_endpoint = Endpoint(**snap_mirror_endpoint)
        if isinstance(snap_mirror_source_endpoint, dict):
            snap_mirror_source_endpoint = Endpoint(**snap_mirror_source_endpoint)
        if isinstance(healthy_status, dict):
            healthy_status = HealthyStatus(**healthy_status)
        if isinstance(snap_mirror_destination_creation, dict):
            snap_mirror_destination_creation = SnapMirrorDestinationCreation(**snap_mirror_destination_creation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84e076be56b589d77e84a54adc104d5e90e08ad1b4a11d9942110b344c0a40c)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument fsx_admin_password_source", value=fsx_admin_password_source, expected_type=type_hints["fsx_admin_password_source"])
            check_type(argname="argument fsxn_destination_info", value=fsxn_destination_info, expected_type=type_hints["fsxn_destination_info"])
            check_type(argname="argument link_arn", value=link_arn, expected_type=type_hints["link_arn"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument snap_mirror_endpoint", value=snap_mirror_endpoint, expected_type=type_hints["snap_mirror_endpoint"])
            check_type(argname="argument snap_mirror_source_endpoint", value=snap_mirror_source_endpoint, expected_type=type_hints["snap_mirror_source_endpoint"])
            check_type(argname="argument healthy_status", value=healthy_status, expected_type=type_hints["healthy_status"])
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
            check_type(argname="argument snap_mirror_destination_creation", value=snap_mirror_destination_creation, expected_type=type_hints["snap_mirror_destination_creation"])
            check_type(argname="argument state_action", value=state_action, expected_type=type_hints["state_action"])
            check_type(argname="argument throttle", value=throttle, expected_type=type_hints["throttle"])
            check_type(argname="argument transfer_schedule", value=transfer_schedule, expected_type=type_hints["transfer_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_system_id": file_system_id,
            "fsx_admin_password_source": fsx_admin_password_source,
            "fsxn_destination_info": fsxn_destination_info,
            "link_arn": link_arn,
            "policy": policy,
            "snap_mirror_endpoint": snap_mirror_endpoint,
            "snap_mirror_source_endpoint": snap_mirror_source_endpoint,
        }
        if healthy_status is not None:
            self._values["healthy_status"] = healthy_status
        if reverse is not None:
            self._values["reverse"] = reverse
        if snap_mirror_destination_creation is not None:
            self._values["snap_mirror_destination_creation"] = snap_mirror_destination_creation
        if state_action is not None:
            self._values["state_action"] = state_action
        if throttle is not None:
            self._values["throttle"] = throttle
        if transfer_schedule is not None:
            self._values["transfer_schedule"] = transfer_schedule

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.

        :schema: CfnSnapMirrorProps#FileSystemId
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fsx_admin_password_source(self) -> "PasswordSource":
        '''The password source for the FSx admin user.

        :schema: CfnSnapMirrorProps#FsxAdminPasswordSource
        '''
        result = self._values.get("fsx_admin_password_source")
        assert result is not None, "Required property 'fsx_admin_password_source' is missing"
        return typing.cast("PasswordSource", result)

    @builtins.property
    def fsxn_destination_info(self) -> "FsxnDestination":
        '''The destination information for the Cluster Peer relationship.

        :schema: CfnSnapMirrorProps#FsxnDestinationInfo
        '''
        result = self._values.get("fsxn_destination_info")
        assert result is not None, "Required property 'fsxn_destination_info' is missing"
        return typing.cast("FsxnDestination", result)

    @builtins.property
    def link_arn(self) -> builtins.str:
        '''The ARN of the AWS Lambda function that will be invoked to manage the resource.

        :schema: CfnSnapMirrorProps#LinkArn
        '''
        result = self._values.get("link_arn")
        assert result is not None, "Required property 'link_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy(self) -> builtins.str:
        '''The SnapMirror policy to be used for the SnapMirror relationship.

        :schema: CfnSnapMirrorProps#Policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snap_mirror_endpoint(self) -> "Endpoint":
        '''Destination endpoint of a SnapMirror relationship.

        :schema: CfnSnapMirrorProps#SnapMirrorEndpoint
        '''
        result = self._values.get("snap_mirror_endpoint")
        assert result is not None, "Required property 'snap_mirror_endpoint' is missing"
        return typing.cast("Endpoint", result)

    @builtins.property
    def snap_mirror_source_endpoint(self) -> "Endpoint":
        '''Source endpoint of a SnapMirror relationship.

        :schema: CfnSnapMirrorProps#SnapMirrorSourceEndpoint
        '''
        result = self._values.get("snap_mirror_source_endpoint")
        assert result is not None, "Required property 'snap_mirror_source_endpoint' is missing"
        return typing.cast("Endpoint", result)

    @builtins.property
    def healthy_status(self) -> typing.Optional["HealthyStatus"]:
        '''The health status of the SnapMirror relationship.

        :schema: CfnSnapMirrorProps#HealthyStatus
        '''
        result = self._values.get("healthy_status")
        return typing.cast(typing.Optional["HealthyStatus"], result)

    @builtins.property
    def reverse(self) -> typing.Optional[builtins.bool]:
        '''Reverse the direction of relationship by making the source endpoint as the new destination endpoint and making the destination endpoint as the new source endpoint.

        Can be set during modify only.

        :schema: CfnSnapMirrorProps#Reverse
        '''
        result = self._values.get("reverse")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def snap_mirror_destination_creation(
        self,
    ) -> typing.Optional["SnapMirrorDestinationCreation"]:
        '''Use this object to provision the destination endpoint when establishing a SnapMirror relationship for a volume.

        For FlexGroup SnapMirror relationships, the source and destination FlexGroups must be spread over the same number of aggregates with the same number of constituents per aggregate.

        :schema: CfnSnapMirrorProps#SnapMirrorDestinationCreation
        '''
        result = self._values.get("snap_mirror_destination_creation")
        return typing.cast(typing.Optional["SnapMirrorDestinationCreation"], result)

    @builtins.property
    def state_action(self) -> typing.Optional["CfnSnapMirrorPropsStateAction"]:
        '''Modify the SnapMirror replication status using 'StateAction' in the CloudFormation template when the relationship exists.

        Follow ONTAP protocol: set to 'paused' to pause, 'snapmirrored' to resync, and 'update' to trigger the transfer API. For subsequent updates, first clear the prior 'StateAction' then set it again.

        :schema: CfnSnapMirrorProps#StateAction
        '''
        result = self._values.get("state_action")
        return typing.cast(typing.Optional["CfnSnapMirrorPropsStateAction"], result)

    @builtins.property
    def throttle(self) -> typing.Optional[jsii.Number]:
        '''Throttle, in KBs per second.

        This 'throttle' overrides the 'throttle' set on the SnapMirror relationship's policy. If neither of these are set, the throttle defaults to 0, which is interpreted as unlimited.

        :schema: CfnSnapMirrorProps#Throttle
        '''
        result = self._values.get("throttle")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def transfer_schedule(self) -> typing.Optional[builtins.str]:
        '''Schedule used to update asynchronous relationships.

        This 'transfer_schedule' overrides the 'transfer_schedule' set on the SnapMirror relationship's policy. Remove the property to revert. Only cron schedules are supported for SnapMirror.

        :schema: CfnSnapMirrorProps#TransferSchedule
        '''
        result = self._values.get("transfer_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSnapMirrorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.CfnSnapMirrorPropsStateAction"
)
class CfnSnapMirrorPropsStateAction(enum.Enum):
    '''Modify the SnapMirror replication status using 'StateAction' in the CloudFormation template when the relationship exists.

    Follow ONTAP protocol: set to 'paused' to pause, 'snapmirrored' to resync, and 'update' to trigger the transfer API. For subsequent updates, first clear the prior 'StateAction' then set it again.

    :schema: CfnSnapMirrorPropsStateAction
    '''

    BROKEN_UNDERSCORE_OFF = "BROKEN_UNDERSCORE_OFF"
    '''broken_off.'''
    PAUSED = "PAUSED"
    '''paused.'''
    SNAPMIRRORED = "SNAPMIRRORED"
    '''snapmirrored.'''
    IN_UNDERSCORE_SYNC = "IN_UNDERSCORE_SYNC"
    '''in_sync.'''
    UPDATE = "UPDATE"
    '''update.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.Endpoint",
    jsii_struct_bases=[],
    name_mapping={"svm": "svm", "volume": "volume"},
)
class Endpoint:
    def __init__(
        self,
        *,
        svm: typing.Union["NameWithUuidRef", typing.Dict[builtins.str, typing.Any]],
        volume: builtins.str,
    ) -> None:
        '''
        :param svm: The SVM identifier.
        :param volume: The volume name within the SVM.

        :schema: Endpoint
        '''
        if isinstance(svm, dict):
            svm = NameWithUuidRef(**svm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ce600e5b1147bc2b2489149df1cd95da83d37f29069604c5726ef9af699caa)
            check_type(argname="argument svm", value=svm, expected_type=type_hints["svm"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "svm": svm,
            "volume": volume,
        }

    @builtins.property
    def svm(self) -> "NameWithUuidRef":
        '''The SVM identifier.

        :schema: Endpoint#SVM
        '''
        result = self._values.get("svm")
        assert result is not None, "Required property 'svm' is missing"
        return typing.cast("NameWithUuidRef", result)

    @builtins.property
    def volume(self) -> builtins.str:
        '''The volume name within the SVM.

        :schema: Endpoint#Volume
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Endpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.FsxnDestination",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "fsx_admin_password_source": "fsxAdminPasswordSource",
        "link_arn": "linkArn",
    },
)
class FsxnDestination:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        fsx_admin_password_source: typing.Union["PasswordSource", typing.Dict[builtins.str, typing.Any]],
        link_arn: builtins.str,
    ) -> None:
        '''
        :param file_system_id: The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.
        :param fsx_admin_password_source: The password source for the FSx admin user.
        :param link_arn: The ARN of the AWS Lambda function that will be invoked to manage the resource.

        :schema: FsxnDestination
        '''
        if isinstance(fsx_admin_password_source, dict):
            fsx_admin_password_source = PasswordSource(**fsx_admin_password_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63061142c1cf784d31bf1550a2343ecdd6c840e5dfbec85b3e91d86590029214)
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument fsx_admin_password_source", value=fsx_admin_password_source, expected_type=type_hints["fsx_admin_password_source"])
            check_type(argname="argument link_arn", value=link_arn, expected_type=type_hints["link_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_system_id": file_system_id,
            "fsx_admin_password_source": fsx_admin_password_source,
            "link_arn": link_arn,
        }

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''The file system ID of the Amazon FSx for NetApp ONTAP file system in which the resource is created.

        :schema: FsxnDestination#FileSystemId
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fsx_admin_password_source(self) -> "PasswordSource":
        '''The password source for the FSx admin user.

        :schema: FsxnDestination#FsxAdminPasswordSource
        '''
        result = self._values.get("fsx_admin_password_source")
        assert result is not None, "Required property 'fsx_admin_password_source' is missing"
        return typing.cast("PasswordSource", result)

    @builtins.property
    def link_arn(self) -> builtins.str:
        '''The ARN of the AWS Lambda function that will be invoked to manage the resource.

        :schema: FsxnDestination#LinkArn
        '''
        result = self._values.get("link_arn")
        assert result is not None, "Required property 'link_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxnDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.HealthyStatus",
    jsii_struct_bases=[],
    name_mapping={"healthy": "healthy", "unhealthy_reason": "unhealthyReason"},
)
class HealthyStatus:
    def __init__(
        self,
        *,
        healthy: typing.Optional[builtins.bool] = None,
        unhealthy_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param healthy: Indicates whether the relationship is healthy.
        :param unhealthy_reason: Reason the relationship is not healthy.

        :schema: HealthyStatus
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b92923a5aedb7eab6d656f4d50800070e6ba469169b407f6db86ce82e3234e)
            check_type(argname="argument healthy", value=healthy, expected_type=type_hints["healthy"])
            check_type(argname="argument unhealthy_reason", value=unhealthy_reason, expected_type=type_hints["unhealthy_reason"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if healthy is not None:
            self._values["healthy"] = healthy
        if unhealthy_reason is not None:
            self._values["unhealthy_reason"] = unhealthy_reason

    @builtins.property
    def healthy(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the relationship is healthy.

        :schema: HealthyStatus#Healthy
        '''
        result = self._values.get("healthy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def unhealthy_reason(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Reason the relationship is not healthy.

        :schema: HealthyStatus#UnhealthyReason
        '''
        result = self._values.get("unhealthy_reason")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthyStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.NameWithUuidRef",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "uuid": "uuid"},
)
class NameWithUuidRef:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        uuid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name part of the reference, which can be used to identify resources such as SVM.
        :param uuid: The UUID part of the reference, which can be used to identify resources such as SVM.

        :schema: NameWithUuidRef
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf6d9794438277eb7334292bf6a972b084e5dee099996560e13588e2d3e0272)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if uuid is not None:
            self._values["uuid"] = uuid

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name part of the reference, which can be used to identify resources such as SVM.

        :schema: NameWithUuidRef#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''The UUID part of the reference, which can be used to identify resources such as SVM.

        :schema: NameWithUuidRef#UUID
        '''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NameWithUuidRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.PasswordSource",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret"},
)
class PasswordSource:
    def __init__(
        self,
        *,
        secret: typing.Union["SecretSource", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param secret: A reference to the source of the password, typically an AWS Secrets Manager secret.

        :schema: PasswordSource
        '''
        if isinstance(secret, dict):
            secret = SecretSource(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051661304b890c115993f8b41b8f5fd97f533dd7991d114e0528d6cf8c02e7fb)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }

    @builtins.property
    def secret(self) -> "SecretSource":
        '''A reference to the source of the password, typically an AWS Secrets Manager secret.

        :schema: PasswordSource#Secret
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast("SecretSource", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PasswordSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.SecretSource",
    jsii_struct_bases=[],
    name_mapping={"secret_arn": "secretArn", "secret_key": "secretKey"},
)
class SecretSource:
    def __init__(self, *, secret_arn: builtins.str, secret_key: builtins.str) -> None:
        '''
        :param secret_arn: The ARN of the secret stored in AWS Secrets Manager.
        :param secret_key: Reference for the SecretKey. The actual password is stored in AWS Secret Manager.

        :schema: SecretSource
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac0b762da703edbfffc6ba827c5626a3e50f637bab23278ddb27723ffc3f040)
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_arn": secret_arn,
            "secret_key": secret_key,
        }

    @builtins.property
    def secret_arn(self) -> builtins.str:
        '''The ARN of the secret stored in AWS Secrets Manager.

        :schema: SecretSource#SecretArn
        '''
        result = self._values.get("secret_arn")
        assert result is not None, "Required property 'secret_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_key(self) -> builtins.str:
        '''Reference for the SecretKey.

        The actual password is stored in AWS Secret Manager.

        :schema: SecretSource#SecretKey
        '''
        result = self._values.get("secret_key")
        assert result is not None, "Required property 'secret_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/netapp-fsxn-snapmirror.SnapMirrorDestinationCreation",
    jsii_struct_bases=[],
    name_mapping={"aggregates": "aggregates"},
)
class SnapMirrorDestinationCreation:
    def __init__(self, *, aggregates: typing.Sequence[builtins.str]) -> None:
        '''
        :param aggregates: List of aggregate names that host the volume.

        :schema: SnapMirrorDestinationCreation
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275518d4056147436a647c52f81f4d0955d92ee0bb03f150b175d418f4bb8ad4)
            check_type(argname="argument aggregates", value=aggregates, expected_type=type_hints["aggregates"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregates": aggregates,
        }

    @builtins.property
    def aggregates(self) -> typing.List[builtins.str]:
        '''List of aggregate names that host the volume.

        :schema: SnapMirrorDestinationCreation#Aggregates
        '''
        result = self._values.get("aggregates")
        assert result is not None, "Required property 'aggregates' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnapMirrorDestinationCreation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSnapMirror",
    "CfnSnapMirrorProps",
    "CfnSnapMirrorPropsStateAction",
    "Endpoint",
    "FsxnDestination",
    "HealthyStatus",
    "NameWithUuidRef",
    "PasswordSource",
    "SecretSource",
    "SnapMirrorDestinationCreation",
]

publication.publish()

def _typecheckingstub__eea53c0cdeb8c48c40c150b8f59b02c7fc809429230ef6c4883bd12fed52937f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    fsxn_destination_info: typing.Union[FsxnDestination, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    policy: builtins.str,
    snap_mirror_endpoint: typing.Union[Endpoint, typing.Dict[builtins.str, typing.Any]],
    snap_mirror_source_endpoint: typing.Union[Endpoint, typing.Dict[builtins.str, typing.Any]],
    healthy_status: typing.Optional[typing.Union[HealthyStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    reverse: typing.Optional[builtins.bool] = None,
    snap_mirror_destination_creation: typing.Optional[typing.Union[SnapMirrorDestinationCreation, typing.Dict[builtins.str, typing.Any]]] = None,
    state_action: typing.Optional[CfnSnapMirrorPropsStateAction] = None,
    throttle: typing.Optional[jsii.Number] = None,
    transfer_schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84e076be56b589d77e84a54adc104d5e90e08ad1b4a11d9942110b344c0a40c(
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    fsxn_destination_info: typing.Union[FsxnDestination, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
    policy: builtins.str,
    snap_mirror_endpoint: typing.Union[Endpoint, typing.Dict[builtins.str, typing.Any]],
    snap_mirror_source_endpoint: typing.Union[Endpoint, typing.Dict[builtins.str, typing.Any]],
    healthy_status: typing.Optional[typing.Union[HealthyStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    reverse: typing.Optional[builtins.bool] = None,
    snap_mirror_destination_creation: typing.Optional[typing.Union[SnapMirrorDestinationCreation, typing.Dict[builtins.str, typing.Any]]] = None,
    state_action: typing.Optional[CfnSnapMirrorPropsStateAction] = None,
    throttle: typing.Optional[jsii.Number] = None,
    transfer_schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ce600e5b1147bc2b2489149df1cd95da83d37f29069604c5726ef9af699caa(
    *,
    svm: typing.Union[NameWithUuidRef, typing.Dict[builtins.str, typing.Any]],
    volume: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63061142c1cf784d31bf1550a2343ecdd6c840e5dfbec85b3e91d86590029214(
    *,
    file_system_id: builtins.str,
    fsx_admin_password_source: typing.Union[PasswordSource, typing.Dict[builtins.str, typing.Any]],
    link_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b92923a5aedb7eab6d656f4d50800070e6ba469169b407f6db86ce82e3234e(
    *,
    healthy: typing.Optional[builtins.bool] = None,
    unhealthy_reason: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf6d9794438277eb7334292bf6a972b084e5dee099996560e13588e2d3e0272(
    *,
    name: typing.Optional[builtins.str] = None,
    uuid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051661304b890c115993f8b41b8f5fd97f533dd7991d114e0528d6cf8c02e7fb(
    *,
    secret: typing.Union[SecretSource, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac0b762da703edbfffc6ba827c5626a3e50f637bab23278ddb27723ffc3f040(
    *,
    secret_arn: builtins.str,
    secret_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275518d4056147436a647c52f81f4d0955d92ee0bb03f150b175d418f4bb8ad4(
    *,
    aggregates: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
