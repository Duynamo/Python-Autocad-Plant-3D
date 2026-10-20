"""Data Access Object (DAO) và Bộ máy suy luận thông minh (Smart Inference Engine)
cho tiêu chuẩn gioăng mặt bích JIS B 2404 : 2018.
"""
import os
from typing import Optional, Dict, Tuple

from ..models.jis_b2404_specs import (
    SheetGasketDimension,
    SpiralWoundGasketDimension,
    PtfeJacketGasketDimension,
    GasketSpec,
)
from ..data.jis_b2404_dataset import (
    SHEET_GASKET_D1,
    RING_GASKET_D3,
    SPIRAL_WOUND_DIMENSIONS,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DATA_DIR, "jis_b2404.sqlite")

# Cache RAM tốc độ cao
_SHEET_CACHE: Dict[Tuple[str, int, str, str], SheetGasketDimension] = {}
_SWG_CACHE: Dict[Tuple[str, int, str, str], SpiralWoundGasketDimension] = {}


def get_sheet_gasket_dimension(
    rating: str,
    dn: int,
    shape: str = "RING",
    facing: str = "RF",
    thickness: float = 3.0
) -> Optional[SheetGasketDimension]:
    """Tra cứu kích thước gioăng tấm đệm phẳng JIS B 2404 (Bảng 6 - Bảng 10).
    Hoạt động thuần RAM 100%, an toàn tuyệt đối trong AutoCAD Plant 3D (không đòi hỏi _sqlite3.pyd).
    """
    norm_rating = rating.upper().replace(" ", "")
    norm_shape = shape.upper().replace(" ", "_")
    norm_facing = facing.upper().replace(" ", "")
    cache_key = (norm_rating, dn, norm_shape, norm_facing)

    if cache_key in _SHEET_CACHE:
        return _SHEET_CACHE[cache_key]

    # 1. Tra RAM nhanh cho Ring Gasket (Bảng 9 JIS B 2404)
    if norm_shape == "RING":
        d3 = RING_GASKET_D3.get((norm_rating, dn))
        d1 = SHEET_GASKET_D1.get(dn)
        if d3 is not None and d1 is not None:
            spec = SheetGasketDimension(
                standard="JIS_B_2404",
                rating=norm_rating,
                dn=dn,
                shape="RING",
                facing=norm_facing,
                d1=d1,
                d2=d3,
                nominal_thickness=thickness
            )
            _SHEET_CACHE[cache_key] = spec
            return spec

    # 2. Tra cứu Full-Face qua _fvc_flanges (Bảng 6 - Bảng 8 JIS B 2404: D2 = D bích, PCD = C, h, no)
    if norm_shape == "FULL_FACE":
        try:
            from _fvc_flanges.db.jis_b2220_reader import get_flange_dimensions
            f_dim = get_flange_dimensions(norm_rating, dn)
            if f_dim:
                d1 = SHEET_GASKET_D1.get(dn, f_dim.d0)
                spec = SheetGasketDimension(
                    standard="JIS_B_2404",
                    rating=norm_rating,
                    dn=dn,
                    shape="FULL_FACE",
                    facing=norm_facing,
                    d1=d1,
                    d2=f_dim.d,
                    c=f_dim.c,
                    h=f_dim.h,
                    no=f_dim.no,
                    nominal_thickness=thickness
                )
                _SHEET_CACHE[cache_key] = spec
                return spec
        except Exception:
            pass

    # 3. Dự phòng tra SQLite nếu có môi trường hỗ trợ
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
            SELECT d1, d2, c, h, no, nominal_thickness
            FROM sheet_gaskets
            WHERE rating = ? AND dn = ? AND shape = ?
            LIMIT 1;
            """, (norm_rating, dn, norm_shape))
            row = cur.fetchone()
            conn.close()
            if row:
                spec = SheetGasketDimension(
                    standard="JIS_B_2404",
                    rating=norm_rating,
                    dn=dn,
                    shape=norm_shape,
                    facing=norm_facing,
                    d1=row[0],
                    d2=row[1],
                    c=row[2],
                    h=row[3],
                    no=row[4],
                    nominal_thickness=thickness if thickness > 0 else row[5]
                )
                _SHEET_CACHE[cache_key] = spec
                return spec
    except Exception:
        pass

    return None


def get_spiral_wound_gasket_dimension(
    rating: str,
    dn: int,
    construction: str = "INNER_OUTER_RING",
    facing: str = "RF"
) -> Optional[SpiralWoundGasketDimension]:
    """Tra cứu kích thước gioăng kim loại quấn xoắn SWG JIS B 2404 (Bảng 15 - Bảng 26)."""
    norm_rating = rating.upper().replace(" ", "")
    norm_const = construction.upper().replace(" ", "_")
    norm_facing = facing.upper().replace(" ", "")
    cache_key = (norm_rating, dn, norm_const, norm_facing)

    if cache_key in _SWG_CACHE:
        return _SWG_CACHE[cache_key]

    dims = SPIRAL_WOUND_DIMENSIONS.get((norm_rating, dn))
    if dims:
        d1_in, d2_in, d3_out, d4_out = dims
        # Tùy biến vành trong / vành ngoài theo construction
        has_inner = "INNER" in norm_const
        has_outer = "OUTER" in norm_const

        actual_d1 = d1_in if has_inner else None
        actual_d4 = d4_out if has_outer else None

        spec = SpiralWoundGasketDimension(
            standard="JIS_B_2404",
            rating=norm_rating,
            dn=dn,
            construction=norm_const,
            facing=norm_facing,
            d1=actual_d1,
            d2=d2_in,
            d3=d3_out,
            d4=actual_d4,
            t_winding=4.5,
            t_ring=3.0
        )
        _SWG_CACHE[cache_key] = spec
        return spec

    return None


def get_auto_gasket_for_flange(
    rating: str = "10K",
    dn: int = 100,
    facing: str = "RF",
    flange_type: str = "SOP",
    flange1_material: str = "CARBON_STEEL",
    flange2_material: str = "CARBON_STEEL",
    gasket_override: Optional[str] = None,
    insulation_kit: bool = False,
    thickness_override: Optional[float] = None
) -> GasketSpec:
    """Bộ máy suy luận tự động thông minh (Smart Inference Engine) cho cụm kết nối mặt bích.
    
    Quy tắc suy luận:
    1. CÁCH 1 (Galvanic Dissimilar Metal Detection):
       Nếu insulation_kit=True HOẶC flange1_material != flange2_material (ví dụ thép nối inox):
       -> Tự động kích hoạt bộ cách điện mặt bích (Flange Dielectric Insulation Kit: G10/PTFE + Sleeves + Washers).
    2. Cấp áp suất cao >= 16K trên bích gờ Raised Face:
       -> Tự động chọn Spiral Wound Gasket có cả vành trong & ngoài (内外輪 - SWIC).
    3. Mặt bích phẳng (Flat Face - FF):
       -> Tự động chọn Sheet Gasket toàn mặt (Full-Face 全面形) đục đầy đủ lỗ bu lông.
    4. Mặt bích gờ nổi thông dụng (5K, 10K RF):
       -> Tự động chọn Sheet Gasket dạng vành (Ring Gasket).
    5. Ghi đè chỉ định (Override):
       -> Nếu gasket_override được chỉ định ('SPIRAL_WOUND', 'PTFE_JACKET'...), ưu tiên loại đó.
    """
    norm_rating = rating.upper().replace(" ", "")
    norm_facing = facing.upper().replace(" ", "")
    mat1 = flange1_material.upper()
    mat2 = flange2_material.upper()

    # 1. Kiểm tra phát hiện cặp kim loại khác nhau (Cách 1)
    is_dielectric = insulation_kit or (mat1 != mat2)

    # 2. Xác định họ Gasket (Gasket Family)
    if gasket_override:
        family = gasket_override.upper()
    elif is_dielectric:
        family = "INSULATING_KIT"
    elif norm_facing == "FF":
        family = "SHEET"
    elif norm_rating in ["16K", "20K", "30K", "40K", "63K"] and norm_facing == "RF":
        family = "SPIRAL_WOUND"
    elif norm_facing in ["TG", "MF"]:
        family = "SPIRAL_WOUND"
    else:
        family = "SHEET"

    # 3. Tạo GasketSpec tương ứng
    # --------------------------------------------------------------------------
    # TRƯỜNG HỢP A: BỘ CÁCH ĐIỆN MẶT BÍCH (DIELECTRIC INSULATION KIT)
    # --------------------------------------------------------------------------
    if is_dielectric:
        # Gioăng cách điện G10 / PTFE
        ring_dim = get_sheet_gasket_dimension(norm_rating, dn, shape="RING", facing=norm_facing)
        d_in = ring_dim.d1 if ring_dim else float(dn)
        d_out = ring_dim.d2 if ring_dim else (float(dn) * 1.5)
        tg = thickness_override if thickness_override else 3.0

        return GasketSpec(
            standard="JIS_B_2404",
            family="INSULATING_KIT",
            rating=norm_rating,
            dn=dn,
            facing=norm_facing,
            d_inner=d_in,
            d_outer=d_out,
            thickness=tg,
            shape_code="DIELECTRIC_RING",
            is_insulating=True,
            gasket_material="G10_EPOXY_GLASS",
            sleeve_material="G10_MYLAR",
            washer_material="G10_DOUBLE_WASHER",
            full_designation=f"Flange Dielectric Isolation Kit JIS B 2404 {norm_rating} DN{dn} (G10/PTFE)"
        )

    # --------------------------------------------------------------------------
    # TRƯỜNG HỢP B: GIOĂNG XOẮN KIM LOẠI (SPIRAL WOUND GASKET)
    # --------------------------------------------------------------------------
    if family == "SPIRAL_WOUND":
        const_type = "INNER_OUTER_RING" if norm_facing == "RF" else "BASIC"
        swg_dim = get_spiral_wound_gasket_dimension(norm_rating, dn, construction=const_type, facing=norm_facing)
        if swg_dim:
            d_min = swg_dim.d1 if swg_dim.d1 else swg_dim.d2
            d_max = swg_dim.d4 if swg_dim.d4 else swg_dim.d3
            return GasketSpec(
                standard="JIS_B_2404",
                family="SPIRAL_WOUND",
                rating=norm_rating,
                dn=dn,
                facing=norm_facing,
                d_inner=d_min,
                d_outer=d_max,
                thickness=swg_dim.t_winding,
                shape_code="SWIC" if const_type == "INNER_OUTER_RING" else "SW_BASIC",
                d1_inner_ring=swg_dim.d1,
                d2_winding_in=swg_dim.d2,
                d3_winding_out=swg_dim.d3,
                d4_outer_ring=swg_dim.d4,
                gasket_material="SUS316L_GRAPHITE",
                full_designation=f"Spiral Wound Gasket JIS B 2404 {norm_rating} DN{dn} (SUS316L/Graphite SWIC)"
            )

    # --------------------------------------------------------------------------
    # TRƯỜNG HỢP C: GIOĂNG TẤM ĐỆM TOÀN MẶT (FULL-FACE SHEET GASKET)
    # --------------------------------------------------------------------------
    if norm_facing == "FF":
        ff_dim = get_sheet_gasket_dimension(norm_rating, dn, shape="FULL_FACE", facing="FF")
        if ff_dim:
            tg = thickness_override if thickness_override else ff_dim.nominal_thickness
            return GasketSpec(
                standard="JIS_B_2404",
                family="SHEET",
                rating=norm_rating,
                dn=dn,
                facing="FF",
                d_inner=ff_dim.d1,
                d_outer=ff_dim.d2,
                thickness=tg,
                shape_code="FULL_FACE",
                pcd=ff_dim.c,
                hole_dia=ff_dim.h,
                hole_count=ff_dim.no,
                gasket_material="NON_ASBESTOS",
                full_designation=f"Sheet Gasket Full-Face JIS B 2404 {norm_rating} DN{dn} (Non-Asbestos t={tg}mm)"
            )

    # --------------------------------------------------------------------------
    # TRƯỜNG HỢP D: GIOĂNG TẤM ĐỆM DẠNG VÀNH TIÊU CHUẨN (RING SHEET GASKET)
    # --------------------------------------------------------------------------
    ring_dim = get_sheet_gasket_dimension(norm_rating, dn, shape="RING", facing="RF")
    if ring_dim:
        tg = thickness_override if thickness_override else ring_dim.nominal_thickness
        return GasketSpec(
            standard="JIS_B_2404",
            family="SHEET",
            rating=norm_rating,
            dn=dn,
            facing="RF",
            d_inner=ring_dim.d1,
            d_outer=ring_dim.d2,
            thickness=tg,
            shape_code="RING",
            gasket_material="NON_ASBESTOS",
            full_designation=f"Sheet Gasket Ring Type JIS B 2404 {norm_rating} DN{dn} (Non-Asbestos t={tg}mm)"
        )

    # Dự phòng an toàn (Fallback)
    d1_fallback = SHEET_GASKET_D1.get(dn, float(dn))
    d2_fallback = float(dn) * 1.5
    return GasketSpec(
        standard="JIS_B_2404",
        family="SHEET",
        rating=norm_rating,
        dn=dn,
        facing=norm_facing,
        d_inner=d1_fallback,
        d_outer=d2_fallback,
        thickness=3.0,
        shape_code="RING",
        gasket_material="NON_ASBESTOS",
        full_designation=f"Sheet Gasket JIS B 2404 {norm_rating} DN{dn} (Fallback)"
    )
