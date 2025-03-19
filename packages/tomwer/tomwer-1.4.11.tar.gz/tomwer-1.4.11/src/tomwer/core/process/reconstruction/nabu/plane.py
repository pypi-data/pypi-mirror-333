"""Define nabu Axis"""

from silx.utils.enum import Enum as _Enum


class NabuPlane(_Enum):
    YZ = "YZ"
    XZ = "XZ"
    XY = "XY"

    @classmethod
    def from_value(cls, value):
        if value == 0:
            return NabuPlane.XY
        elif value == 1:
            return NabuPlane.XZ
        elif value == 2:
            return NabuPlane.YZ
        return super().from_value(value=value)
