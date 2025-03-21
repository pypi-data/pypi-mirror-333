"""
gtsfm submodule
"""
from __future__ import annotations
import gtsam.gtsam
import numpy
import numpy.typing
import typing
__all__ = ['Keypoints', 'tracksFromPairwiseMatches']
class Keypoints:
    def __init__(self, coordinates: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 2]"]) -> None:
        ...
    @property
    def coordinates(self) -> typing.Annotated[numpy.typing.NDArray[numpy.float64], "[m, 2]"]:
        ...
    @coordinates.setter
    def coordinates(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64, "[m, 2]"]) -> None:
        ...
def tracksFromPairwiseMatches(matches_dict: dict[gtsam.gtsam.IndexPair, typing.Annotated[numpy.typing.ArrayLike, numpy.int32, "[m, 2]"]], keypoints_list: list[Keypoints], verbose: bool = False) -> list[gtsam.gtsam.SfmTrack2d]:
    ...
