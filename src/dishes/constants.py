from decimal import Decimal

from typing_extensions import Annotated

DICIMAL_FLOAT_TO_STR = {
    Decimal: str,
    float: str,
}

DECIMAL_NUM_16_2 = Annotated[Decimal, 16]
