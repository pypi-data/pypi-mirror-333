
# This is a generated file

"""hybrid - Hybrid processing"""

# VERSION: 1

from typing import Any, Final, Mapping, TypedDict

from .. import ssc
from ._types import *

DataDict = TypedDict('DataDict', {
    'input': Table,
    'output': Table
}, total=False)

class Data(ssc.DataDict):
    input: Table = INPUT(label='input_table for multiple technologies and one financial market', type='TABLE', required='*')
    output: Final[Table] = OUTPUT(label='output_table for multiple technologies and one financial market', type='TABLE', required='*')

    def __init__(self, *args: Mapping[str, Any],
                 input: Table = ...) -> None: ...
    def to_dict(self) -> DataDict: ...  # type: ignore[override]

class Module(ssc.Module[Data]):
    def __init__(self) -> None: ...
