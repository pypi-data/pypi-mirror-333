from datetime import date
from typing import Annotated, Optional
from pydantic import Field, BeforeValidator

from .common import ModelBase
from ..validators import (
    BoolType,
    date_validator,
    LazyString,
    ImpactValue,
    NullableInt,
    make_bool_validator,
    make_int_validator,
)


class SystemModel(ModelBase):
    system_id: Annotated[NullableInt, Field(alias="System ID")]


class FismaInventoryItemBase(SystemModel):
    vasi_id: Annotated[LazyString, Field(alias="VASI ID")] = None
    organization: Annotated[str, Field(alias="Organization")]
    geo_association: Annotated[
        Optional[str], Field(alias="Geographical Association")
    ] = None
    system_development_life_cycle: Annotated[
        Optional[str], Field(alias="System Development Life Cycle")
    ] = None
    system_name: Annotated[str, Field(alias="System Name")]
    system_acronym: Annotated[str, Field(alias="System Acronym")]
    system_description: Annotated[str, Field(alias="System Description")]
    system_environment: Annotated[Optional[str], Field(alias="System Environment")] = (
        None
    )
    confidentiality: Annotated[str, Field(alias="Confidentiality")]
    integrity: Annotated[str, Field(alias="Integrity")]
    availability: Annotated[str, Field(alias="Availability")]
    impact: Annotated[ImpactValue, Field(alias="Impact")] = None
    has_pii: Annotated[BoolType, Field(alias="PII")] = False
    has_phi: Annotated[BoolType, Field(alias="PHI")] = False
    piv_status: Annotated[Optional[str], Field(alias="PIV Status")] = None
    mfa_details_internal: Annotated[
        Optional[str], Field(alias="MFA Details (Internal Users)")
    ] = None
    mfa_details_external: Annotated[
        Optional[str], Field(alias="MFA Details (External Users)")
    ] = None
    encryption_of_data: Annotated[Optional[str], Field(alias="Encryption of Data")] = (
        None
    )
    group_tagging: Annotated[Optional[str], Field(alias="Group Tagging")] = None
    system_steward_list: Annotated[Optional[str], Field(alias="System Steward")] = None
    isso_list: Annotated[
        Optional[str], Field(alias="Information System Security Officer")
    ] = None
    so_list: Annotated[Optional[str], Field(alias="Information System Owner")] = None
    ao_list: Annotated[Optional[str], Field(alias="Authorizing Official")] = None
    has_external_user_accounts: Annotated[
        BoolType, Field(alias="External User Accounts")
    ] = False
    allows_external_connections: Annotated[
        BoolType, Field(alias="External Connection(s)")
    ] = False
    security_review_completion_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Security Review Completion Date"),
    ] = None
    bia_is_required: Annotated[BoolType, Field(alias="BIA Required")] = False
    bia_last_reviewed_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="BIA Last Reviewed Date"),
    ] = None
    cp_is_required: Annotated[BoolType, Field(alias="Contingency Plan Required")] = (
        False
    )
    cp_last_reviewed_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Contingency Plan Last Reviewed Date"),
    ] = None
    cp_has_been_tested: Annotated[BoolType, Field(alias="Contingency Plan Tested")] = (
        False
    )
    cp_last_test_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Contingency Plan Test Date"),
    ] = None
    irp_is_required: Annotated[
        BoolType,
        Field(alias="Incident Response Plan Required"),
    ] = False
    irp_last_reviewed_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Incident Response Plan Last Reviewed Date"),
    ] = None
    irp_last_test_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Incident Response Test Date"),
    ] = None
    drp_is_required: Annotated[
        BoolType,
        Field(alias="Disaster Recovery Plan Required"),
    ] = False
    drp_last_reviewed_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Disaster Recovery Plan Last Reviewed Date"),
    ] = None
    drp_last_test_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Disaster Recovery Test Date"),
    ] = None
    cmp_is_required: Annotated[
        BoolType,
        Field(alias="Configuration Management Plan Required"),
    ] = False
    cmp_last_reviewed_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Configuration Management Plan Last Reviewed Date"),
    ] = None
    pia_is_required: Annotated[
        BoolType,
        Field(alias="Privacy Impact Assessment Required"),
    ] = False
    pia_last_reviewed_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Privacy Impact Assessment Last Reviewed Date"),
    ] = None
    pta_is_required: Annotated[
        BoolType,
        Field(alias="Privacy Threshold Analysis Required"),
    ] = False
    pta_last_reviewed_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Privacy Threshold Analysis Last Reviewed Date"),
    ] = None
    is_fisma_reportable: Annotated[
        BoolType,
        Field(alias="FISMA Reportable"),
    ] = False


class SystemStatusDetailsBase(SystemModel):
    financial_management_system: Annotated[
        Optional[str], Field(alias="Financial Management System")
    ] = None


class PoamBase(SystemModel):
    policy: Annotated[Optional[str], Field(alias="Policy")] = None
    geo_association: Annotated[
        Optional[str], Field(alias="Geographical Association")
    ] = None
    id: Annotated[LazyString, Field(alias="ID")] = None
    control_title: Annotated[Optional[str], Field(alias="Control Title")] = None
    status: Annotated[Optional[str], Field(alias="POA&M Item Status")] = None
    source: Annotated[Optional[str], Field(alias="Source")] = None
    is_approved: Annotated[
        Optional[bool],
        BeforeValidator(make_bool_validator(["approved"])),
        Field(alias="POA&M Item Review Status"),
    ] = None
    review_status: Annotated[
        Optional[str],
        Field(alias="POA&M Item Review Status"),
    ] = None
    scheduled_completion_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Scheduled Completion Date"),
    ] = None
    pending_extension_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Pending Extension Date"),
    ] = None
    extension_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Extension Date"),
    ] = None
    completion_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Completion Date"),
    ] = None
    artifact_attachment_count: Annotated[
        Optional[int],
        BeforeValidator(make_int_validator()),
        Field(alias="Artifact Attachments"),
    ] = None
    created_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Created Date"),
    ] = None
    last_modified_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Last Modified Date"),
    ] = None
    milestone_scheduled_completion_date: Annotated[
        Optional[date],
        date_validator,
        Field(alias="Milestone Scheduled Completion Date"),
    ] = None
    likelihood: Annotated[Optional[str], Field(alias="Likelihood")] = None
    residual_risk: Annotated[Optional[str], Field(alias="Residual Risk")] = None
