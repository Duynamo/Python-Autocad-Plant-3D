"""DAO truy vấn thông số vòng đệm phẳng theo tiêu chuẩn JIS B 1256 : 2008."""
import os
from typing import Optional, Dict, Tuple, List
from ..models.jis_b1256_specs import WasherDimensionSpec, WasherTypeSpec, PlainWasherSpec
from ..data.jis_b1256_dataset import (
    JIS_B1256_WASHER_TYPES,
    JIS_B1256_HARDNESS_SPECS,
    JIS_B1256_WASHER_DIMENSIONS,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DATA_DIR, "jis_b1256.sqlite")

# Cache bộ nhớ RAM tốc độ cao
_DIM_CACHE: Dict[Tuple[str, str], WasherDimensionSpec] = {}
_TYPE_CACHE: Dict[str, WasherTypeSpec] = {}

# Bảng ánh xạ alias linh hoạt cho series
_SERIES_ALIAS_MAP: Dict[str, str] = {
    "ISO 7089": "ISO_NORMAL_A",
    "ISO_7089": "ISO_NORMAL_A",
    "ISO_7089_NORMAL_GRADE_A": "ISO_NORMAL_A",
    "NORMAL": "ISO_NORMAL_A",
    "NORMAL_A": "ISO_NORMAL_A",
    "ISO 7090": "ISO_NORMAL_CHAMFERED_A",
    "ISO_7090": "ISO_NORMAL_CHAMFERED_A",
    "ISO_7090_NORMAL_CHAMFERED_GRADE_A": "ISO_NORMAL_CHAMFERED_A",
    "CHAMFERED": "ISO_NORMAL_CHAMFERED_A",
    "NORMAL_CHAMFERED": "ISO_NORMAL_CHAMFERED_A",
    "ISO 7091": "ISO_NORMAL_C",
    "ISO_7091": "ISO_NORMAL_C",
    "ISO_7091_NORMAL_GRADE_C": "ISO_NORMAL_C",
    "NORMAL_C": "ISO_NORMAL_C",
    "ISO 7092": "ISO_SMALL_A",
    "ISO_7092": "ISO_SMALL_A",
    "ISO_7092_SMALL_GRADE_A": "ISO_SMALL_A",
    "SMALL": "ISO_SMALL_A",
    "SMALL_A": "ISO_SMALL_A",
    "ISO 7093": "ISO_LARGE_A",
    "ISO 7093-1": "ISO_LARGE_A",
    "ISO_7093_1": "ISO_LARGE_A",
    "ISO_7093_1_LARGE_GRADE_A": "ISO_LARGE_A",
    "LARGE": "ISO_LARGE_A",
    "LARGE_A": "ISO_LARGE_A",
    "ISO 7093-2": "ISO_LARGE_C",
    "ISO_7093_2": "ISO_LARGE_C",
    "ISO_7093_2_LARGE_GRADE_C": "ISO_LARGE_C",
    "LARGE_C": "ISO_LARGE_C",
    "ISO 7094": "ISO_EXTRA_LARGE_C",
    "ISO_7094": "ISO_EXTRA_LARGE_C",
    "ISO_7094_EXTRA_LARGE_GRADE_C": "ISO_EXTRA_LARGE_C",
    "EXTRA_LARGE": "ISO_EXTRA_LARGE_C",
    "EXTRA_LARGE_C": "ISO_EXTRA_LARGE_C",
    "ANNEX_JA": "ANNEX_JA_SQUARE",
    "SQUARE": "ANNEX_JA_SQUARE",
    "JA_SQUARE": "ANNEX_JA_SQUARE",
    "POLISHED": "JIS_POLISHED_ROUND",
    "MIGAKI": "JIS_POLISHED_ROUND",
    "COMMERCIAL": "JIS_COMMERCIAL_ROUND",
    "NAMI": "JIS_COMMERCIAL_ROUND",
}


def _normalize_series(series: str) -> str:
    """Chuẩn hóa tên dòng series sang định danh chuẩn nội bộ."""
    s_clean = series.strip().upper().replace("-", "_").replace(" ", "_")
    if s_clean in _SERIES_ALIAS_MAP:
        return _SERIES_ALIAS_MAP[s_clean]
    # Thử tra cứu nguyên bản không replace
    s_orig = series.strip().upper()
    if s_orig in _SERIES_ALIAS_MAP:
        return _SERIES_ALIAS_MAP[s_orig]
    return s_clean


def get_washer_type(type_code: str = "ISO_7089_NORMAL_GRADE_A") -> Optional[WasherTypeSpec]:
    """Lấy thông tin định danh và đặc tính kỹ thuật của chủng loại vòng đệm theo JIS B 1256.
    
    Args:
        type_code: Mã nhận diện chủng loại (ví dụ: 'ISO_7089_NORMAL_GRADE_A', 'ISO_7090_NORMAL_CHAMFERED_GRADE_A', 'ANNEX_JA_SQUARE')
    """
    code_clean = type_code.strip().upper()
    if code_clean in _TYPE_CACHE:
        return _TYPE_CACHE[code_clean]

    # 1. Tra cứu thuần Python RAM Cache (Zero-IO)
    if code_clean in JIS_B1256_WASHER_TYPES:
        spec = JIS_B1256_WASHER_TYPES[code_clean]
        _TYPE_CACHE[code_clean] = spec
        return spec

    # Thử qua alias
    norm_series = _normalize_series(code_clean)
    for t in JIS_B1256_WASHER_TYPES.values():
        if t.dimension_series == norm_series or t.washer_series == code_clean:
            _TYPE_CACHE[code_clean] = t
            return t

    # 2. Dự phòng SQLite nếu type_code chưa nạp trong cache
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT standard, type_id, type_code, type_name_ja, type_name_en, iso_standard,
                       washer_series, product_grade, dimension_series, is_flange_default, description_vi
                FROM jis_b1256_washer_types
                WHERE type_code = ?
            """, (code_clean,))
            row = cur.fetchone()
            conn.close()
            if row:
                spec = WasherTypeSpec(
                    standard="JIS_B_1256",
                    type_id=row[1],
                    type_code=row[2],
                    type_name_ja=row[3],
                    type_name_en=row[4],
                    iso_standard=row[5],
                    washer_series=row[6],
                    product_grade=row[7],
                    dimension_series=row[8],
                    is_flange_default=bool(row[9]),
                    description_vi=row[10]
                )
                _TYPE_CACHE[code_clean] = spec
                return spec
    except Exception:
        pass

    return None


def list_available_washer_types() -> List[WasherTypeSpec]:
    """Liệt kê toàn bộ các chủng loại vòng đệm JIS B 1256 : 2008 & hệ liên quan."""
    return list(JIS_B1256_WASHER_TYPES.values())


def get_washer_dimension(bolt_size: str = "M16", series: str = "ISO_NORMAL_A") -> Optional[WasherDimensionSpec]:
    """Truy vấn kích thước hình học chi tiết của vòng đệm (d1, d2, h, góc vát chamfer).
    
    Args:
        bolt_size: Cỡ bu lông áp dụng (ví dụ: 'M16', 'M20', 'M30')
        series: Dòng series kích thước:
            - 'ISO_NORMAL_A': Vòng đệm thường cấp A (ISO 7089 - Mặc định bích)
            - 'ISO_NORMAL_CHAMFERED_A': Vòng đệm thường vát mép cấp A (ISO 7090)
            - 'ISO_NORMAL_C': Vòng đệm thường cấp C dập thô (ISO 7091)
            - 'ISO_SMALL_A': Vòng đệm vành nhỏ cấp A (ISO 7092)
            - 'ISO_LARGE_A': Vòng đệm vành lớn cấp A (ISO 7093-1)
            - 'ISO_LARGE_C': Vòng đệm vành lớn cấp C (ISO 7093-2)
            - 'ISO_EXTRA_LARGE_C': Vòng đệm vành cực lớn dày cấp C (ISO 7094)
            - 'ANNEX_JA_SQUARE': Vòng đệm vuông phụ lục JA
            - 'JIS_POLISHED_ROUND': Vòng đệm tròn mài bóng JIS B 1250 (ミガキ丸)
            - 'JIS_COMMERCIAL_ROUND': Vòng đệm tròn thông dụng JIS B 1250 (並丸)
    """
    size_clean = bolt_size.strip().upper()
    norm_series = _normalize_series(series)
    cache_key = (norm_series, size_clean)

    if cache_key in _DIM_CACHE:
        return _DIM_CACHE[cache_key]

    # 1. Tra cứu thuần Python RAM Cache
    if cache_key in JIS_B1256_WASHER_DIMENSIONS:
        dim = JIS_B1256_WASHER_DIMENSIONS[cache_key]
        _DIM_CACHE[cache_key] = dim
        return dim

    # 2. Dự phòng SQLite
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT standard, series, bolt_size, nominal_dia,
                       d1_nominal, d1_min, d1_max,
                       d2_nominal, d2_min, d2_max,
                       h_nominal, h_min, h_max,
                       chamfer_angle_deg, chamfer_c
                FROM jis_b1256_washer_dimensions
                WHERE series = ? AND bolt_size = ?
            """, (norm_series, size_clean))
            row = cur.fetchone()
            conn.close()
            if row:
                dim = WasherDimensionSpec(
                    standard=row[0],
                    series=row[1],
                    bolt_size=row[2],
                    nominal_dia=row[3],
                    d1_nominal=row[4],
                    d1_min=row[5],
                    d1_max=row[6],
                    d2_nominal=row[7],
                    d2_min=row[8],
                    d2_max=row[9],
                    h_nominal=row[10],
                    h_min=row[11],
                    h_max=row[12],
                    chamfer_angle_deg=row[13],
                    chamfer_c=row[14]
                )
                _DIM_CACHE[cache_key] = dim
                return dim
    except Exception:
        pass

    return None


def list_available_washer_sizes(series: str = "ISO_NORMAL_A") -> List[str]:
    """Liệt kê danh sách các cỡ bu lông hỗ trợ theo dòng series."""
    norm_series = _normalize_series(series)
    sizes = []
    for (ser, sz) in JIS_B1256_WASHER_DIMENSIONS.keys():
        if ser == norm_series:
            sizes.append(sz)
    return sizes


def get_hardness_spec(hardness_class: str = "200_HV") -> Optional[Dict]:
    """Lấy thông số độ cứng Vickers và yêu cầu kỹ thuật tương ứng."""
    h_clean = hardness_class.strip().upper().replace(" ", "_")
    return JIS_B1256_HARDNESS_SPECS.get(h_clean)


def get_plain_washer(
    bolt_size: str = "M16",
    series: str = "ISO_NORMAL_A",
    hardness_class: str = "200_HV",
    material: str = "CARBON_STEEL"
) -> Optional[PlainWasherSpec]:
    """Khởi tạo đối tượng PlainWasherSpec hoàn chỉnh phục vụ dựng mô hình 3D và BOM.
    
    Args:
        bolt_size: Cỡ ren (ví dụ: 'M16', 'M20')
        series: Dòng series (mặc định 'ISO_NORMAL_A')
        hardness_class: '100_HV', '200_HV', '300_HV'
        material: 'CARBON_STEEL', 'STAINLESS_A2', 'STAINLESS_A4', 'BRASS'
    """
    dim = get_washer_dimension(bolt_size, series)
    if not dim:
        return None

    norm_series = _normalize_series(series)
    type_code = "ISO_7089_NORMAL_GRADE_A"
    for t in JIS_B1256_WASHER_TYPES.values():
        if t.dimension_series == norm_series:
            type_code = t.type_code
            break

    # Xây dựng tên thương mại BOM (full_designation)
    mat_label = "Thép cacbon" if material == "CARBON_STEEL" else ("Inox SUS304 (A2)" if material == "STAINLESS_A2" else material)
    h_label = hardness_class.replace("_", " ")
    designation = f"Vòng đệm phẳng JIS B 1256 {dim.series} {dim.bolt_size} - {h_label} ({mat_label})"

    return PlainWasherSpec(
        standard="JIS_B_1256",
        type_code=type_code,
        bolt_size=dim.bolt_size,
        dimensions=dim,
        hardness_class=hardness_class,
        material=material,
        full_designation=designation
    )


def get_matching_washer_for_bolt(bolt_size: str, prefer_series: str = "ISO_NORMAL_A") -> WasherDimensionSpec:
    """Tự động tra cứu vòng đệm phẳng tương thích tốt nhất cho cỡ bu lông chỉ định.
    Nếu series ưu tiên không hỗ trợ cỡ ren này, tự động fallback sang ISO_NORMAL_A.
    """
    dim = get_washer_dimension(bolt_size, prefer_series)
    if dim:
        return dim

    # Fallback sang ISO_NORMAL_A nếu tìm series khác không có
    dim_fallback = get_washer_dimension(bolt_size, "ISO_NORMAL_A")
    if dim_fallback:
        return dim_fallback

    # Trường hợp cỡ ren ngoại cỡ không có trong bảng, tính toán theo tỷ lệ tiêu chuẩn ISO 7089 (d1 = d + 1mm, d2 = 2.0d, h = 0.15d ~ 0.2d)
    nom_d = 16.0
    if bolt_size.upper().startswith("M"):
        try:
            nom_d = float(bolt_size[1:].split("X")[0])
        except Exception:
            nom_d = 16.0
    d1_calc = nom_d + (1.0 if nom_d <= 16 else (2.0 if nom_d <= 36 else 3.0))
    d2_calc = round(nom_d * 2.0)
    h_calc = round(max(3.0, nom_d * 0.18))
    return WasherDimensionSpec(
        standard="JIS_B_1256",
        series="ISO_NORMAL_A",
        bolt_size=bolt_size.upper(),
        nominal_dia=nom_d,
        d1_nominal=d1_calc,
        d1_min=d1_calc,
        d1_max=d1_calc + 0.3,
        d2_nominal=d2_calc,
        d2_min=d2_calc - 0.6,
        d2_max=d2_calc,
        h_nominal=h_calc,
        h_min=h_calc - 0.3,
        h_max=h_calc + 0.3,
        chamfer_angle_deg=0.0,
        chamfer_c=None
    )
