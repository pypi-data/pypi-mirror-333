from typing import Annotated

from fastapi import Path
from pydantic import Field, StringConstraints

postcode_validation_pattern = r"^[A-Za-z]{1,2}\d{1,2}[A-Za-z]?\s?\d[A-Za-z]{2}$"

postcode_constraint = Annotated[
    str, StringConstraints(pattern=postcode_validation_pattern)
]

postcode_description = "UK postcode in format 'AA9A 9AA', 'A9A 9AA', 'A9 9AA', 'A99 9AA', 'AA9 9AA', or 'AA99 9AA'"

postcode_field = Field(
    description=postcode_description,
    json_schema_extra={"pattern": postcode_validation_pattern},
)

postcode_query = Path(
    ..., pattern=postcode_validation_pattern, description=postcode_description
)

Postcode = Annotated[str, postcode_constraint]
