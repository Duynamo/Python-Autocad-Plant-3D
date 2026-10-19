"""DAO truy vấn thông số đai ốc lục giác theo tiêu chuẩn JIS B 1181 : 2014."""
import os
from typing import Optional, Dict, Tuple, List
from ..models.jis_b1181_specs import NutDimensionSpec, NutTypeSpec, HexNutSpec
from ..data.jis_b1181_dataset import (
    JIS_B1181_NUT_TYPES,
    JIS_B1181_PITCH_SPECS,
    JIS_B1181_NUT_DIMENSIONS,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DATA_DIR, "jis_b1181.sqlite")

# Cache bộ nhớ RAM tốc độ cao
_DIM_CACHE: Dict[Tuple[str, str], NutDimensionSpec] = {}
_TYPE_CACHE: Dict[str, NutTypeSpec] = {}


def get_nut_type(type_code: str = "ISO_4032_STYLE_1_COARSE") -> Optional[NutTypeSpec]:
    """Lấy thông tin định danh và đặc tính của chủng loại đai ốc theo JIS B 1181.
    
    Args:
        type_code: Mã nhận diện chủng loại (ví dụ: 'ISO_4032_STYLE_1_COARSE', 'ISO_4035_STYLE_0_THIN_COARSE', 'JA_TYPE_1_REGULAR')
    """
    code_clean = type_code.strip().upper()
    if code_clean in _TYPE_CACHE:
        return _TYPE_CACHE[code_clean]

    # 1. Tra cứu thuần Python (RAM Cache - Zero IO)
    if code_clean in JIS_B1181_NUT_TYPES:
        item = JIS_B1181_NUT_TYPES[code_clean]
        _TYPE_CACHE[code_clean] = item
        return item

    # 2. Dự phòng SQLite nếu type_code chưa có trong cache RAM
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT standard, type_id, type_code, type_name_ja, type_name_en, iso_standard,
                       nut_style, pitch_type, product_grade, dimension_series, is_flange_default, description_vi
                FROM jis_b1181_nut_types
                WHERE type_code = ?
            """, (code_clean,))
            row = cur.fetchone()
            conn.close()
            if row:
                spec = NutTypeSpec(
                    standard=row[0],
                    type_id=row[1],
                    type_code=row[2],
                    type_name_ja=row[3],
                    type_name_en=row[4],
                    iso_standard=row[5],
                    nut_style=row[6],
                    pitch_type=row[7],
                    product_grade=row[8],
                    dimension_series=row[9],
                    is_flange_default=bool(row[10]),
                    description_vi=row[11]
                )
                _TYPE_CACHE[code_clean] = spec
                return spec
    except Exception:
        pass

    return None


def list_available_nut_types() -> List[NutTypeSpec]:
    """Liệt kê toàn bộ 12 chủng loại đai ốc JIS B 1181 : 2014."""
    return list(JIS_B1181_NUT_TYPES.values())


def get_nut_dimension(nut_size: str = "M16", series: str = "ISO_STYLE_1") -> Optional[NutDimensionSpec]:
    """Truy vấn kích thước hình học đai ốc (s, m, e, dw, da) theo cỡ ren và dòng series.
    
    Args:
        nut_size: Cỡ ren (ví dụ: 'M16', 'M20', 'M30x3')
        series: Dòng series kích thước:
            - 'ISO_STYLE_1': Đai ốc tiêu chuẩn Style 1 (ISO 4032 / 8673)
            - 'ISO_STYLE_2': Đai ốc dày Style 2 (ISO 4033 / 8674)
            - 'ISO_STYLE_0_THIN': Đai ốc mỏng Style 0 (ISO 4035 / 8675)
            - 'ISO_GRADE_C': Đai ốc thô Cấp C (ISO 4034)
            - 'ANNEX_JA_REGULAR': Hệ truyền thống Nhật (Loại 1, 2, 4)
            - 'ANNEX_JA_THIN': Hệ truyền thống Nhật (Loại 3 mỏng)
            - 'ANNEX_JA_SMALL': Hệ truyền thống Nhật (Loại giác nhỏ 小形)
    """
    size_clean = nut_size.strip().upper().replace("X", "x")
    series_clean = series.strip().upper()
    cache_key = (series_clean, size_clean)

    if cache_key in _DIM_CACHE:
        return _DIM_CACHE[cache_key]

    # 1. Tra cứu thuần Python RAM
    if cache_key in JIS_B1181_NUT_DIMENSIONS:
        dim = JIS_B1181_NUT_DIMENSIONS[cache_key]
        _DIM_CACHE[cache_key] = dim
        return dim

    # Thử fallback không có phần đuôi bước ren (ví dụ M30x3 lấy M30 nếu cỡ mịn chưa định nghĩa riêng)
    base_size = size_clean.split("x")[0]
    fallback_key = (series_clean, base_size)
    if fallback_key in JIS_B1181_NUT_DIMENSIONS:
        dim = JIS_B1181_NUT_DIMENSIONS[fallback_key]
        _DIM_CACHE[cache_key] = dim
        return dim

    # 2. Dự phòng SQLite
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT standard, series, nut_size, nominal_dia, pitch, s_nominal, s_min, s_max,
                       m_nominal, m_min, m_max, e_min, dw_min, da_min, da_max, chamfer_angle_deg, chamfer_sides
                FROM jis_b1181_nut_dimensions
                WHERE series = ? AND nut_size = ?
            """, (series_clean, size_clean))
            row = cur.fetchone()
            conn.close()
            if row:
                spec = NutDimensionSpec(
                    standard=row[0],
                    series=row[1],
                    nut_size=row[2],
                    nominal_dia=row[3],
                    pitch=row[4],
                    s_nominal=row[5],
                    s_min=row[6],
                    s_max=row[7],
                    m_nominal=row[8],
                    m_min=row[9],
                    m_max=row[10],
                    e_min=row[11],
                    dw_min=row[12],
                    da_min=row[13],
                    da_max=row[14],
                    chamfer_angle_deg=row[15],
                    chamfer_sides=row[16]
                )
                _DIM_CACHE[cache_key] = spec
                return spec
    except Exception:
        pass

    return None


def list_available_nut_sizes(series: str = "ISO_STYLE_1") -> List[str]:
    """Lấy danh sách các cỡ ren có sẵn trong series."""
    series_clean = series.strip().upper()
    sizes = [sz for (ser, sz) in JIS_B1181_NUT_DIMENSIONS.keys() if ser == series_clean]
    return sorted(list(set(sizes)), key=lambda x: float(x.replace("M", "").split("x")[0]))


def get_hex_nut(
    nut_size: str = "M16",
    type_code: str = "ISO_4032_STYLE_1_COARSE",
    material: str = "STEEL_CLASS_8"
) -> Optional[HexNutSpec]:
    """Khởi tạo đặc tính đối tượng đai ốc hoàn chỉnh phục vụ dựng hình 3D Solid và lập bảng kê BOM.
    
    Args:
        nut_size: 'M16', 'M20', 'M30x3'...
        type_code: Mã loại đai ốc
        material: Cấp bền vật liệu ('STEEL_CLASS_8', 'STEEL_CLASS_10', 'STAINLESS_A2_70'...)
    """
    nut_type = get_nut_type(type_code)
    if not nut_type:
        return None

    dim = get_nut_dimension(nut_size, nut_type.dimension_series)
    if not dim:
        return None

    # Tên thương mại chuẩn hóa hiển thị trên BOM
    full_designation = f"Hex Nut {nut_type.iso_standard} {nut_size} ({material})"

    return HexNutSpec(
        standard="JIS_B_1181",
        type_code=nut_type.type_code,
        nut_size=nut_size.strip().upper(),
        nominal_dia=dim.nominal_dia,
        pitch=dim.pitch,
        dimensions=dim,
        material=material,
        full_designation=full_designation
    )


def get_matching_nut_for_bolt(bolt_size: str = "M16", prefer_style: str = "STYLE_1") -> Optional[NutDimensionSpec]:
    """Tự động tìm kiếm quy cách đai ốc tương thích hoàn toàn với cỡ bu-lông (JIS B 1217 / JIS B 1180).
    
    Args:
        bolt_size: Cỡ bu-lông (ví dụ 'M16', 'M20', 'M30x3')
        prefer_style: 'STYLE_1' (tiêu chuẩn mặc định), 'STYLE_2' (đai ốc cao), 'STYLE_0' (đai ốc mỏng), hoặc 'ANNEX_JA'
    """
    style_upper = prefer_style.strip().upper()
    if style_upper in ["STYLE_1", "ISO_STYLE_1"]:
        series = "ISO_STYLE_1"
    elif style_upper in ["STYLE_2", "ISO_STYLE_2"]:
        series = "ISO_STYLE_2"
    elif style_upper in ["STYLE_0", "STYLE_0_THIN", "ISO_STYLE_0"]:
        series = "ISO_STYLE_0_THIN"
    elif "JA" in style_upper or "ANNEX" in style_upper:
        series = "ANNEX_JA_REGULAR"
    else:
        series = "ISO_STYLE_1"

    return get_nut_dimension(bolt_size, series)
