"""Package _fvc_flanges: Thư viện mặt bích tiêu chuẩn Nhật Bản JIS B 2220.
Tương thích với AutoCAD Plant 3D.
"""

from .jis_b2220_flange import JisB2220Flange, JisFlange, JisFlangeObject
from .db.jis_b2220_reader import get_flange_dimensions
from .models.dimensions import FlangeDimensions

__all__ = [
    "JisB2220Flange",
    "JisFlange",
    "JisFlangeObject",
    "get_flange_dimensions",
    "FlangeDimensions"
]
