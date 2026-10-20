"""Package _fvc_fasteners: Thư viện bu-lông, đai ốc, gu-zông, gioăng và vòng đệm tiêu chuẩn JIS B 1217 / JIS B 1180 / JIS B 1181 / JIS B 1256.
Tương thích với AutoCAD Plant 3D.
"""

from .models.jis_b1217_specs import MetricBoltSpec, FlangeBoltSelection
from .models.jis_b1180_specs import HexHeadSpec, BoltTypeSpec, HexBoltSpec
from .models.jis_b1181_specs import NutDimensionSpec, NutTypeSpec, HexNutSpec
from .models.jis_b1256_specs import WasherDimensionSpec, WasherTypeSpec, PlainWasherSpec
from .models.jis_b2404_specs import (
    SheetGasketDimension,
    SpiralWoundGasketDimension,
    PtfeJacketGasketDimension,
    GasketSpec,
)
from .db.jis_b1217_reader import get_bolt_for_flange, get_metric_bolt_spec
from .db.jis_b1180_reader import (
    get_hex_bolt,
    get_head_dimension,
    get_bolt_type,
    list_available_bolt_types,
    calculate_thread_length,
)
from .db.jis_b1181_reader import (
    get_nut_dimension,
    get_nut_type,
    list_available_nut_types,
    list_available_nut_sizes,
    get_hex_nut,
    get_matching_nut_for_bolt,
)
from .db.jis_b1256_reader import (
    get_washer_dimension,
    get_washer_type,
    list_available_washer_types,
    list_available_washer_sizes,
    get_hardness_spec,
    get_plain_washer,
    get_matching_washer_for_bolt,
)
from .db.jis_b2404_reader import (
    get_sheet_gasket_dimension,
    get_spiral_wound_gasket_dimension,
    get_auto_gasket_for_flange,
)
from .geometry.nut import HexNut, FastenerObject, build_hex_prism
from .geometry.bolt import HexBolt
from .geometry.stud import StudBolt
from .geometry.gasket import Gasket, GasketObject
from .geometry.washer import PlainWasher, SquareWasher

__all__ = [
    # Models
    "MetricBoltSpec",
    "FlangeBoltSelection",
    "HexHeadSpec",
    "BoltTypeSpec",
    "HexBoltSpec",
    "NutDimensionSpec",
    "NutTypeSpec",
    "HexNutSpec",
    "WasherDimensionSpec",
    "WasherTypeSpec",
    "PlainWasherSpec",
    "SheetGasketDimension",
    "SpiralWoundGasketDimension",
    "PtfeJacketGasketDimension",
    "GasketSpec",
    # Reader functions
    "get_bolt_for_flange",
    "get_metric_bolt_spec",
    "get_hex_bolt",
    "get_head_dimension",
    "get_bolt_type",
    "list_available_bolt_types",
    "calculate_thread_length",
    "get_nut_dimension",
    "get_nut_type",
    "list_available_nut_types",
    "list_available_nut_sizes",
    "get_hex_nut",
    "get_matching_nut_for_bolt",
    "get_washer_dimension",
    "get_washer_type",
    "list_available_washer_types",
    "list_available_washer_sizes",
    "get_hardness_spec",
    "get_plain_washer",
    "get_matching_washer_for_bolt",
    "get_sheet_gasket_dimension",
    "get_spiral_wound_gasket_dimension",
    "get_auto_gasket_for_flange",
    # 3D Geometries
    "HexNut",
    "HexBolt",
    "StudBolt",
    "Gasket",
    "FastenerObject",
    "GasketObject",
    "build_hex_prism",
    "PlainWasher",
    "SquareWasher",
]

