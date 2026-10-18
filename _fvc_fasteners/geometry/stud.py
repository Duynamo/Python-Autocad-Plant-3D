from typing import Optional
try:
    import varmain.primitiv as prim
except ImportError:
    prim = None

from ..db.jis_b1217_reader import get_metric_bolt_spec
from ..models.jis_b1217_specs import MetricBoltSpec
from .nut import FastenerObject, build_hex_prism

def StudBolt(
    s,
    bolt_size: str = "M16",
    length: float = 88.0,
    with_nuts: bool = True
) -> FastenerObject:
    """Tạo gu-zông / bu-lông 2 đầu ren (Stud Bolt) kèm 2 đai ốc tiêu chuẩn JIS B 1217.
    Gốc tọa độ đặt tại tâm đối xứng của thanh ren (Z = -length/2 đến +length/2).
    
    Args:
        s: Subpart container
        bolt_size: Cỡ ren ('M12', 'M16', 'M20', 'M30x3'...)
        length: Chiều dài toàn bộ gu-zông lt (mm)
        with_nuts: True nếu muốn tự động gắn 2 đai ốc ở 2 đầu
    """
    spec = get_metric_bolt_spec(bolt_size)
    if not spec:
        spec = MetricBoltSpec("JIS_B_1180", bolt_size, 16.0, 2.0, 24.0, 27.71, 13.0, 10.0, 3.0, 30.0)
        
    lt_val = float(length)
    r_stud = float(spec.nominal_dia) / 2.0
    m_val = float(spec.m)
    pitch_val = float(spec.pitch)
    
    # 1. Dựng thân gu-zông
    stud = prim.CYLINDER(s, R=r_stud, H=lt_val, O=0)
    stud.translate((0, 0, -lt_val / 2.0))
    
    # 2. Gắn 2 đai ốc ở 2 đầu
    if with_nuts:
        proj = 2.0 * pitch_val
        
        # Đai ốc trên (+Z): mặt ngoài đai ốc cách đầu ren một khoảng proj
        z_nut_top = (lt_val / 2.0) - proj - m_val
        nut_top = build_hex_prism(s, width_across_flats=spec.s, height=m_val)
        nut_top.translate((0, 0, z_nut_top))
        stud.uniteWith(nut_top)
        nut_top.erase()
        
        # Đai ốc dưới (-Z): mặt ngoài đai ốc cách đầu ren một khoảng proj
        z_nut_bot = (-lt_val / 2.0) + proj
        nut_bot = build_hex_prism(s, width_across_flats=spec.s, height=m_val)
        nut_bot.translate((0, 0, z_nut_bot))
        stud.uniteWith(nut_bot)
        nut_bot.erase()
        
    return FastenerObject(stud, spec)
