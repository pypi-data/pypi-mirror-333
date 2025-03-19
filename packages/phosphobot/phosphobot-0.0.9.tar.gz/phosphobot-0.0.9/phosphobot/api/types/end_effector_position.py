# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class EndEffectorPosition(UniversalBaseModel):
    """
    End effector position for a movement in absolute frame.
    All zeros means the initial position, that you get by calling /move/init
    """

    open: float = pydantic.Field()
    """
    0 for closed, 1 for open
    """

    rx: float = pydantic.Field()
    """
    Absolute Pitch in degrees
    """

    ry: float = pydantic.Field()
    """
    Absolute Yaw in degrees
    """

    rz: float = pydantic.Field()
    """
    Absolute Roll in degrees
    """

    x: float = pydantic.Field()
    """
    X position in centimeters
    """

    y: float = pydantic.Field()
    """
    Y position in centimeters
    """

    z: float = pydantic.Field()
    """
    Z position in centimeters
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
            extra="allow", frozen=True
        )  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
