"""Package _fvc_fasteners: Thư viện bu-lông, đai ốc, gu-zông và gioăng đệm tiêu chuẩn JIS B 1217 / JIS B 1180 / JIS B 1181.
Tương thích với AutoCAD Plant 3D.
"""

from .models.jis_b1217_specs import MetricBoltSpec, FlangeBoltSelection
from .models.jis_b1180_specs import HexHeadSpec, BoltTypeSpec, HexBoltSpec
from .db.jis_b1217_reader import get_bolt_for_flange, get_metric_bolt_spec
from .db.jis_b1180_reader import (
    get_hex_bolt,
    get_head_dimension,
    get_bolt_type,
    list_available_bolt_types,
    calculate_thread_length,
)
from .geometry.nut import HexNut, FastenerObject, build_hex_prism
from .geometry.bolt import HexBolt
from .geometry.stud import StudBolt
from .geometry.gasket import Gasket, GasketObject

__all__ = [
    "MetricBoltSpec",
    "FlangeBoltSelection",
    "HexHeadSpec",
    "BoltTypeSpec",
    "HexBoltSpec",
    "get_bolt_for_flange",
    "get_metric_bolt_spec",
    "get_hex_bolt",
    "get_head_dimension",
    "get_bolt_type",
    "list_available_bolt_types",
    "calculate_thread_length",
    "HexNut",
    "HexBolt",
    "StudBolt",
    "Gasket",
    "FastenerObject",
    "GasketObject",
    "build_hex_prism",
]
