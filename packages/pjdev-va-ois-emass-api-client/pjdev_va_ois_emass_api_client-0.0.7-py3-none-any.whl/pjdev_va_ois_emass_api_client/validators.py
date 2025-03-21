import enum
import math
import re
from datetime import date, datetime
from typing import Optional, Callable, Any, Annotated, List, Type
from pydantic import BeforeValidator
from loguru import logger


def make_bool_validator(true_values: List[Any]) -> Callable[[str], bool]:
    def validator(v: Optional[str]) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in true_values
        if isinstance(v, int):
            return v in true_values

        return False

    return validator


def make_date_validator(
    date_format: str, date_obj_type: Type[date | datetime] = datetime
) -> Callable[[str], Optional[date]]:
    def validator(v: Optional[Any]) -> Optional[date]:
        if not v:
            return None

        valid_types = [datetime, date, str, float, int]

        is_a_valid_type = any([isinstance(v, t) for t in valid_types])
        if not is_a_valid_type:
            return None

        if isinstance(v, datetime):
            return v if date_obj_type is datetime else v.date()

        if isinstance(v, date):
            return v

        if (isinstance(v, float) or isinstance(v, int)) and date_format != "%s":
            return None

        if isinstance(v, str):
            stripped_value = v.strip()

            if stripped_value in ["-", ""]:
                return None

        if date_format == "%s":
            value = datetime.fromtimestamp(float(v))
        else:
            value = datetime.strptime(v, date_format)
        return value.date() if date_obj_type is date else value

    return validator


def make_date_validator_for_formats(
    date_formats: List[str], date_obj_type: Type[date | datetime] = datetime
) -> Callable[[str], Optional[date]]:
    def validator(v: Optional[Any]) -> Optional[date]:
        for fmt in date_formats:
            try:
                return make_date_validator(fmt, date_obj_type)(v)
            except ValueError:
                continue
        logger.warning(f"Could not find a matching date format for: {v}")
        return None

    return validator


def make_str_validator() -> Callable[[str], Optional[str]]:
    def validator(v: Optional[Any]) -> Optional[str]:
        if isinstance(v, str):
            if v.strip() in ["-", ""]:
                return None
            return v
        if isinstance(v, int) or isinstance(v, float):
            if str(v) == "nan":
                return None
            return str(v)
        if not v:
            return None
        return str(v)

    return validator


class Impact(str, enum.Enum):
    Low = "Low"
    Moderate = "Moderate"
    High = "High"


def make_impact_validator() -> Callable[[Any], Optional[Impact]]:
    valid_string_values = [v.value.lower() for v in Impact]

    def validator(v: Optional[Any]) -> Optional[Impact]:
        if isinstance(v, Impact):
            return v
        str_value = make_str_validator()(v)
        if str_value is None:
            return None

        if str_value.lower() in valid_string_values:
            return Impact(str_value.capitalize())

        return None

    return validator


def make_int_validator() -> Callable[[str], Optional[int]]:
    def validator(v: Optional[str]) -> Optional[int]:
        if isinstance(v, int):
            return v
        if isinstance(v, float):
            return int(v)
        if not v or not isinstance(v, str):
            return None

        return int(v) if v.strip().isdigit() else None

    return validator


def make_nullable_int_validator_with_pattern() -> Callable[[str], Optional[int]]:
    regex = re.compile(r"\d+")

    def validator(v: Optional[str]) -> Optional[int]:
        if v is None:
            return None

        if isinstance(v, int):
            return v

        if isinstance(v, float):
            return int(v) if not math.isnan(v) else 0

        if not v or not isinstance(v, str):
            return 0

        match = regex.search(v)
        if not match:
            return None

        value = match.group(0)

        return make_int_validator()(value)

    return validator


BoolType = Annotated[
    bool, BeforeValidator(make_bool_validator(["yes", 1, True, "true"]))
]
date_validator = BeforeValidator(
    make_date_validator_for_formats(["%s", "%d-%b-%Y", "%m/%d/%Y", "%m/%d/%y"], date)
)
LazyString = Annotated[Optional[str], BeforeValidator(make_str_validator())]
ImpactValue = Annotated[Optional[Impact], BeforeValidator(make_impact_validator())]
NullableInt = Annotated[
    Optional[int], BeforeValidator(make_nullable_int_validator_with_pattern())
]
