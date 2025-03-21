from datetime import date, datetime
from typing import List, Tuple, Optional, Any, Annotated

import pytest
from pydantic import BaseModel

from pjdev_va_ois_emass_api_client import FismaInventoryItemBase
from pjdev_va_ois_emass_api_client.validators import (
    make_bool_validator,
    BoolType,
    date_validator,
    make_nullable_int_validator_with_pattern,
)

bool_validator_test_data: List[Tuple[List[Any], Optional[Any], bool]] = [
    ([], None, False),
    (["yes", 1, True, "true"], None, False),
    (["yes", 1, True, "true"], 1, True),
    (["yes", 1, True, "true"], 0, False),
    (["yes", 1, True, "true"], "abasdlg", False),
    (["yes", 1, True, "true"], dict(random="blah"), False),
    (["yes", 1, True, "true"], [], False),
    (["yes", 1, True, "true"], True, True),
    (["yes", 1, True, "true"], False, False),
]


@pytest.mark.parametrize(
    "true_values, input_value, expected_result", bool_validator_test_data
)
def test_make_bool_validator(
    true_values: List[Any], input_value: Any, expected_result: Optional[bool]
):
    validator = make_bool_validator(true_values)
    result = validator(input_value)

    assert result == expected_result


object_id_validator_test_data: List[Tuple[Optional[Any], Optional[int]]] = [
    ("2345|4356", 2345),
    ("2345 | 4356", 2345),
    (None, None),
    (5645, 5645),
    (5645.98, 5645),
    ("a random value", None),
    ("a random value 9847 and ntoaser 8473", 9847),
]


@pytest.mark.parametrize("input_value, expected_result", object_id_validator_test_data)
def test_make_object_id_validator(input_value: Any, expected_result: Optional[int]):
    validator = make_nullable_int_validator_with_pattern()
    result = validator(input_value)

    assert result == expected_result


bool_type_test_data: List[Tuple[Optional[Any], bool]] = [
    (None, False),
    (1, True),
    (2, False),
    (0, False),
    ("YES", True),
    ("yES", True),
    ("true", True),
    ("True", True),
    ("TRUE", True),
    ("truee", False),
]


@pytest.mark.parametrize("input_value, expected_result", bool_type_test_data)
def test_BoolType(input_value: Any, expected_result: Optional[bool]):
    class BoolTypeModel(BaseModel):
        some_field: BoolType

    obj = dict(some_field=input_value)

    model = BoolTypeModel.model_validate(obj)
    assert model.some_field == expected_result


common_date_type_test_data: List[Tuple[Optional[str | datetime], Optional[date]]] = [
    (None, None),
    ("05-Jan-2024", date(year=2024, month=1, day=5)),
    ("06-Apr-2023", date(year=2023, month=4, day=6)),
    ("", None),
    ("-", None),
    ("   ", None),
    (datetime(year=2026, month=4, day=17), date(year=2026, month=4, day=17)),
    (date(year=2026, month=4, day=17), date(year=2026, month=4, day=17)),
]


date_type_test_data: List[Tuple[Optional[str | datetime], Optional[date]]] = [
    ("1/5/24", date(year=2024, month=1, day=5)),
    ("01/05/2024", date(year=2024, month=1, day=5)),
    (1660667933, date(year=2022, month=8, day=16)),
    (1660667933.0, date(year=2022, month=8, day=16)),
    (1660667933.045, date(year=2022, month=8, day=16)),
    (None, None),
    ([], None),
    (b"test", None),
    ("<NA>", None),
    ("1660667933", date(year=2022, month=8, day=16)),
    ("Unspecified", None),
]


@pytest.mark.parametrize(
    "input_value, expected_result", common_date_type_test_data + date_type_test_data
)
def test_date_validator(input_value: Any, expected_result: Optional[bool]):
    class TestModel(BaseModel):
        some_field: Annotated[Optional[date], date_validator] = None

    obj = dict(some_field=input_value)

    model = TestModel.model_validate(obj)
    assert model.some_field == expected_result


def test_FismaInventory_validation() -> None:
    obj = {
        "Organization": "SRSN",
        "System Acronym": "SRSN",
        "System Name": "some random system name",
        "System ID": "8510",
        "System Description": "blhas aslkdgh alskdg",
        "Confidentiality": "High",
        "Integrity": "High",
        "Availability": "High",
        "Security Review Completion Date": "06-Apr-2023",
        "Contingency Plan Tested": "No",
        "Contingency Plan Test Date": "-",
        "Incident Response Test Date": "27-Feb-2024",
        "Disaster Recovery Test Date": "20-Mar-2023",
        "Encryption of Data": "Data in Use; Data in Transit; Data at Rest",
        "BIA Required": "No",
        "BIA Last Reviewed Date": "-",
        "Contingency Plan Required": "No",
        "Contingency Plan Last Reviewed Date": "-",
        "Incident Response Plan Required": "Yes",
        "Incident Response Plan Last Reviewed Date": "29-Feb-2024",
        "Disaster Recovery Plan Required": "Yes",
        "Disaster Recovery Plan Last Reviewed Date": "01-Nov-2023",
        "Configuration Management Plan Required": "Yes",
        "Configuration Management Plan Last Reviewed Date": "24-Oct-2023",
        "Privacy Threshold Analysis Required": "Yes",
        "Privacy Threshold Analysis Last Reviewed Date": "25-Oct-2023",
        "Privacy Impact Assessment Required": "No",
        "Privacy Impact Assessment Last Reviewed Date": "-",
        "PIV Status": "Not Enabled",
        "MFA Details (Internal Users)": "System enforces an MFA credential that is verifier "
        "impersonation-resistant (e.g., mutual TLS, or Web Authentication) as a "
        "required authentication mechanism for internal users",
        "External User Accounts": "No",
        "MFA Details (External Users)": "-",
        "PII": "No",
        "PHI": "No",
        "External Connection(s)": "No",
        "Group Tagging": "-",
    }

    model = FismaInventoryItemBase.model_validate(obj)
    assert model.pta_is_required is True
