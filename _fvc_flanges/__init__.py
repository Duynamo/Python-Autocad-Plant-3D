"""Bộ thư viện FVC Flanges cho tiêu chuẩn mặt bích Nhật Bản JIS B 2220 / JIS B 2062.
Tương thích với AutoCAD Plant 3D.
"""

from .jis_flange import JisFlange, JisFlangeObject
from .db.reader import get_flange_dimensions
from .models.dimensions import FlangeDimensions

__all__ = [
    "JisFlange",
    "JisFlangeObject",
    "get_flange_dimensions",
    "FlangeDimensions"
]
