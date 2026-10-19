"""Mô đun dựng hình học 3D Solid cho vòng đệm phẳng và vòng đệm vuông JIS B 1256."""
from typing import Optional
try:
    import varmain.primitiv as prim
except ImportError:
    from .nut import prim

from .nut import FastenerObject
from ..db.jis_b1256_reader import (
    get_washer_dimension,
    get_matching_washer_for_bolt,
    get_plain_washer,
)
from ..models.jis_b1256_specs import WasherDimensionSpec, PlainWasherSpec


def PlainWasher(
    s,
    bolt_size: str = "M16",
    series: str = "ISO_NORMAL_A",
    has_hole: bool = True
) -> FastenerObject:
    """Tạo vòng đệm tròn phẳng (Plain Washer) theo tiêu chuẩn JIS B 1256 : 2008.
    
    Gốc tọa độ đặt tại tâm mặt tỳ dưới của vòng đệm:
    - Vòng đệm có chiều dày h kéo dài từ Z = 0 đến Z = h.
    - Đường kính ngoài d2, đường kính lỗ xỏ bu lông d1.
    
    Args:
        s: Subpart container
        bolt_size: Cỡ bu lông ('M12', 'M16', 'M20', 'M30'...)
        series: Dòng series vòng đệm:
            - 'ISO_NORMAL_A': Vành thường cấp A (ISO 7089 - mặc định mặt bích)
            - 'ISO_NORMAL_CHAMFERED_A': Vành thường vát mép cấp A (ISO 7090)
            - 'ISO_NORMAL_C': Vành thường cấp C (ISO 7091)
            - 'ISO_SMALL_A': Vành nhỏ cấp A (ISO 7092)
            - 'ISO_LARGE_A': Vành lớn cấp A (ISO 7093-1)
            - 'ISO_LARGE_C': Vành lớn cấp C (ISO 7093-2)
            - 'ISO_EXTRA_LARGE_C': Vành cực lớn cấp C (ISO 7094)
            - 'JIS_POLISHED_ROUND': Mài bóng JIS B 1250 (ミガキ丸)
            - 'JIS_COMMERCIAL_ROUND': Thông dụng JIS B 1250 (並丸)
        has_hole: True nếu khoét rỗng lỗ tâm d1
    """
    washer_dim = get_washer_dimension(bolt_size, series)
    if not washer_dim:
        washer_dim = get_matching_washer_for_bolt(bolt_size, series)

    d1_val = washer_dim.d1_nominal
    d2_val = washer_dim.d2_nominal
    h_val = washer_dim.h_nominal

    r_outer = d2_val / 2.0
    r_inner = d1_val / 2.0

    # 1. Tạo hình trụ vành ngoài (từ Z = 0 đến Z = h)
    washer_solid = prim.CYLINDER(s, R=r_outer, H=h_val, O=0)

    # 2. Khoét rỗng lỗ tâm d1
    if has_hole and r_inner > 0:
        h_hole = h_val * 1.4
        hole = prim.CYLINDER(s, R=r_inner, H=h_hole, O=0).translate((0, 0, -h_val * 0.2))
        washer_solid.subtractFrom(hole)
        hole.erase()

    return FastenerObject(washer_solid, washer_dim)


def SquareWasher(
    s,
    bolt_size: str = "M16",
    has_hole: bool = True
) -> FastenerObject:
    """Tạo vòng đệm vuông (Square Washer) theo phụ lục JA JIS B 1256 (角座金).
    
    Gốc tọa độ đặt tại tâm mặt tỳ dưới của đệm vuông:
    - Kích thước cạnh vuông a x a, chiều dày t kéo dài từ Z = 0 đến Z = t.
    - Lỗ tròn tâm d1.
    
    Args:
        s: Subpart container
        bolt_size: Cỡ bu lông ('M6', 'M8', 'M10', 'M12', 'M16', 'M20', 'M22', 'M24')
        has_hole: True nếu khoét lỗ xỏ tròn ở giữa
    """
    washer_dim = get_washer_dimension(bolt_size, "ANNEX_JA_SQUARE")
    if not washer_dim:
        washer_dim = get_matching_washer_for_bolt(bolt_size, "ANNEX_JA_SQUARE")

    a_side = washer_dim.d2_nominal
    d1_val = washer_dim.d1_nominal
    h_val = washer_dim.h_nominal

    # 1. Tạo khối hộp vuông a x a x h
    sq_solid = prim.BOX(s, L=a_side, W=a_side, H=h_val).translate((0, 0, h_val / 2.0))

    # 2. Khoét rỗng lỗ tròn tâm d1
    if has_hole and d1_val > 0:
        r_inner = d1_val / 2.0
        h_hole = h_val * 1.4
        hole = prim.CYLINDER(s, R=r_inner, H=h_hole, O=0).translate((0, 0, -h_val * 0.2))
        sq_solid.subtractFrom(hole)
        hole.erase()

    return FastenerObject(sq_solid, washer_dim)
