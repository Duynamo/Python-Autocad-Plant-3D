"""DAO truy vấn thông số bu lông lục giác theo tiêu chuẩn JIS B 1180 : 2014."""
import os
from typing import Optional, Dict, Tuple, List
from ..models.jis_b1180_specs import HexHeadSpec, BoltTypeSpec, HexBoltSpec
from ..data.jis_b1180_dataset import (
    JIS_B1180_BOLT_TYPES,
    JIS_B1180_PITCH_SPECS,
    JIS_B1180_HEAD_DIMENSIONS,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DATA_DIR, "jis_b1180.sqlite")

# Cache bộ nhớ RAM
_HEAD_CACHE: Dict[Tuple[str, str], HexHeadSpec] = {}
_TYPE_CACHE: Dict[str, BoltTypeSpec] = {}


def get_bolt_type(type_code: str = "TYPE_2_NOMINAL_COARSE_GRADE_AB") -> Optional[BoltTypeSpec]:
    """Lấy thông tin định danh của loại bu lông theo JIS B 1180."""
    code_clean = type_code.strip().upper()
    if code_clean in _TYPE_CACHE:
        return _TYPE_CACHE[code_clean]

    # 1. Tra cứu thuần Python
    if code_clean in JIS_B1180_BOLT_TYPES:
        item = JIS_B1180_BOLT_TYPES[code_clean]
        _TYPE_CACHE[code_clean] = item
        return item

    # 2. Dự phòng SQLite
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT standard, type_id, type_code, type_name_ja, iso_standard, thread_style, pitch_type, head_series, is_flange_default, description_vi
                FROM jis_b1180_bolt_types
                WHERE type_code = ?
            """, (code_clean,))
            row = cur.fetchone()
            conn.close()
            if row:
                spec = BoltTypeSpec(
                    standard=row[0],
                    type_id=row[1],
                    type_code=row[2],
                    type_name_ja=row[3],
                    iso_standard=row[4],
                    thread_style=row[5],
                    pitch_type=row[6],
                    head_series=row[7],
                    is_flange_default=bool(row[8]),
                    description_vi=row[9]
                )
                _TYPE_CACHE[code_clean] = spec
                return spec
    except Exception:
        pass

    return None


def get_head_dimension(bolt_size: str = "M16", series: str = "ISO_GRADE_AB") -> Optional[HexHeadSpec]:
    """Truy vấn kích thước hình học đầu lục giác (s, k, e, dw, c, r) theo JIS B 1180."""
    size_clean = bolt_size.strip().upper().replace("X", "x")
    series_clean = series.strip().upper()
    cache_key = (series_clean, size_clean)

    if cache_key in _HEAD_CACHE:
        return _HEAD_CACHE[cache_key]

    # 1. Tra cứu thuần Python
    if cache_key in JIS_B1180_HEAD_DIMENSIONS:
        head = JIS_B1180_HEAD_DIMENSIONS[cache_key]
        _HEAD_CACHE[cache_key] = head
        return head

    # Thử tìm kiếm không có phần x3 (ví dụ M30x3 thì lấy đầu M30 nếu chưa có)
    base_size = size_clean.split("x")[0]
    fallback_key = (series_clean, base_size)
    if fallback_key in JIS_B1180_HEAD_DIMENSIONS:
        head = JIS_B1180_HEAD_DIMENSIONS[fallback_key]
        _HEAD_CACHE[cache_key] = head
        return head

    # 2. Dự phòng SQLite
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT standard, series, bolt_size, s_nominal, s_min, s_max, k_nominal, k_min, k_max, e_min, dw_min, c_min, c_max, r_min, chamfer_angle_deg
                FROM jis_b1180_head_dimensions
                WHERE series = ? AND bolt_size = ?
            """, (series_clean, size_clean))
            row = cur.fetchone()
            conn.close()
            if row:
                head = HexHeadSpec(
                    standard=row[0],
                    series=row[1],
                    bolt_size=row[2],
                    s_nominal=row[3],
                    s_min=row[4],
                    s_max=row[5],
                    k_nominal=row[6],
                    k_min=row[7],
                    k_max=row[8],
                    e_min=row[9],
                    dw_min=row[10],
                    c_min=row[11],
                    c_max=row[12],
                    r_min=row[13],
                    chamfer_angle_deg=row[14]
                )
                _HEAD_CACHE[cache_key] = head
                return head
    except Exception:
        pass

    return None


def calculate_thread_length(length: float, nominal_dia: float, thread_style: str = "NOMINAL_SHANK") -> float:
    """Tính chiều dài ren b theo công thức tiêu chuẩn JIS B 1180 : 2014."""
    l_val = float(length)
    d_val = float(nominal_dia)

    if thread_style == "FULL_THREAD":
        return l_val

    # Công thức bu lông ren lửng JIS B 1180 (ISO 4014)
    if l_val <= 125.0:
        b = 2.0 * d_val + 6.0
    elif l_val <= 200.0:
        b = 2.0 * d_val + 12.0
    else:
        b = 2.0 * d_val + 25.0

    # Chiều dài ren không vượt quá chiều dài tổng bu lông
    return min(b, l_val)


def get_hex_bolt(
    bolt_size: str = "M16",
    length: float = 65.0,
    type_code: str = "TYPE_2_NOMINAL_COARSE_GRADE_AB",
    series_override: Optional[str] = None
) -> Optional[HexBoltSpec]:
    """Lấy quy cách hoàn chỉnh của bu lông lục giác phục vụ dựng hình 3D và BOM.
    
    Args:
        bolt_size: Cỡ bu lông ('M12', 'M16', 'M20', 'M30x3'...)
        length: Chiều dài bu lông l (mm)
        type_code: Loại bu lông trong 7 loại JIS B 1180 (mặc định Type 2 cho mặt bích)
        series_override: Cho phép ép họ đầu (ví dụ ép sang 'ANNEX_JA' để dùng giác cờ-lê Nhật cũ)
    """
    size_clean = bolt_size.strip().upper().replace("X", "x")
    type_spec = get_bolt_type(type_code)
    if not type_spec:
        type_spec = get_bolt_type("TYPE_2_NOMINAL_COARSE_GRADE_AB")

    # Xác định họ đầu
    series = series_override if series_override else type_spec.head_series
    head = get_head_dimension(size_clean, series)
    if not head:
        head = get_head_dimension(size_clean, "ISO_GRADE_AB")
    if not head:
        return None

    # Lấy thông số bước ren & đường kính thân
    pitch_info = JIS_B1180_PITCH_SPECS.get(size_clean)
    if not pitch_info:
        base_size = size_clean.split("x")[0]
        pitch_info = JIS_B1180_PITCH_SPECS.get(base_size, {"nominal_dia": 16.0, "pitch_coarse": 2.0, "pitch_fine": 1.5})

    nominal_dia = pitch_info["nominal_dia"]
    if type_spec.pitch_type == "FINE" and pitch_info["pitch_fine"] is not None:
        pitch = pitch_info["pitch_fine"]
    else:
        pitch = pitch_info["pitch_coarse"]

    # Xác định đường kính thân ds
    if type_spec.thread_style == "REDUCED_SHANK":
        # Thân thắt xấp xỉ đường kính trung bình ren d2 (d2 ≈ d - 0.6495 * P)
        shank_dia = round(nominal_dia - 0.6495 * pitch, 2)
    else:
        shank_dia = nominal_dia

    # Tính chiều dài ren b và thân trơn ls
    thread_length = calculate_thread_length(length, nominal_dia, type_spec.thread_style)
    shank_length = max(0.0, float(length) - thread_length)

    # Tên thương mại chuẩn BOM
    designation = f"Hex Bolt JIS B 1180 {size_clean}x{int(length) if length.is_integer() else length} ({type_spec.iso_standard} {head.series})"

    return HexBoltSpec(
        standard="JIS_B_1180",
        type_code=type_spec.type_code,
        bolt_size=size_clean,
        nominal_dia=nominal_dia,
        pitch=pitch,
        length=float(length),
        thread_length=thread_length,
        shank_length=shank_length,
        shank_dia=shank_dia,
        head=head,
        full_designation=designation
    )


def list_available_bolt_types() -> List[BoltTypeSpec]:
    """Liệt kê toàn bộ các phân loại bu lông được hỗ trợ trong JIS B 1180 : 2014."""
    return list(JIS_B1180_BOLT_TYPES.values())
