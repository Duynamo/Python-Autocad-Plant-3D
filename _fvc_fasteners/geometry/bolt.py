from typing import Optional
try:
    import varmain.primitiv as prim
except ImportError:
    from .nut import prim

from ..db.jis_b1180_reader import get_hex_bolt
from ..models.jis_b1180_specs import HexBoltSpec
from .nut import FastenerObject, build_hex_prism


def HexBolt(
    s,
    bolt_size: str = "M16",
    length: float = 65.0,
    thread_length: Optional[float] = None,
    type_code: str = "TYPE_2_NOMINAL_COARSE_GRADE_AB",
    series_override: Optional[str] = None
) -> FastenerObject:
    """Tạo bu-lông lục giác (Hex Bolt) tiêu chuẩn JIS B 1180 : 2014.
    Gốc tọa độ đặt tại mặt dưới của mũ bu-lông (Z = 0).
    - Mũ lục giác nằm từ Z = -k đến Z = 0.
    - Thân bu-lông tròn kéo dài từ Z = 0 đến Z = length (+Z).
    
    Args:
        s: Subpart container
        bolt_size: Cỡ ren ('M12', 'M16', 'M20', 'M30x3'...)
        length: Chiều dài thân bu-lông l (mm)
        thread_length: Chiều dài ren b (mm, tùy chọn ghi đè)
        type_code: Loại bu lông trong 7 loại JIS B 1180 (mặc định Type 2 cho mặt bích)
        series_override: Ép họ đầu ('ANNEX_JA' để dùng giác cờ-lê Nhật cũ)
    """
    spec = get_hex_bolt(bolt_size, length, type_code, series_override)
    if not spec:
        # Dự phòng trường hợp không tìm thấy
        from ..db.jis_b1217_reader import get_metric_bolt_spec
        m_spec = get_metric_bolt_spec(bolt_size)
        s_nom = m_spec.s if m_spec else 24.0
        k_nom = m_spec.k if m_spec else 10.0
        r_shank = (m_spec.nominal_dia / 2.0) if m_spec else 8.0
    else:
        s_nom = spec.head.s_nominal
        k_nom = spec.head.k_nominal
        r_shank = spec.shank_dia / 2.0

    l_val = float(length)
    k_val = float(k_nom)

    if prim is None:
        # Chế độ chạy kiểm thử bên ngoài AutoCAD
        return FastenerObject(None, spec)

    # 1. Dựng mũ lục giác giác s, chiều cao k
    head = build_hex_prism(s, width_across_flats=s_nom, height=k_val)
    # Dịch chuyển mũ xuống phía -Z để mặt tì của đầu bu-lông (bearing face) nằm chính xác tại Z = 0
    # Mũ lục giác trải từ Z = -k_val đến Z = 0 (áp sát mặt sau phẳng của bích).
    head.translate((0, 0, -k_val))

    # 2. Dựng thân bu-lông (bắt đầu từ Z = 0 xuyên qua lỗ bích theo hướng +Z)
    shank = prim.CYLINDER(s, R=r_shank, H=l_val, O=0)

    # 3. Gộp mũ và thân
    head.uniteWith(shank)
    shank.erase()

    return FastenerObject(head, spec)

