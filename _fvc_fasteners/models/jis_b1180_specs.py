from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class HexHeadSpec:
    """Quy cách kích thước hình học đầu lục giác theo JIS B 1180 : 2014."""
    standard: str               # Luôn là 'JIS_B_1180'
    series: str                 # 'ISO_GRADE_AB', 'ISO_GRADE_C', hoặc 'ANNEX_JA'
    bolt_size: str              # Cỡ bu lông: 'M6', 'M8', 'M10', 'M12', 'M16', 'M20', 'M24', 'M30' v.v.
    s_nominal: float            # Bề rộng cờ-lê / giác lục giác danh nghĩa (mm)
    s_min: float                # Giác cờ-lê tối thiểu (mm)
    s_max: float                # Giác cờ-lê tối đa (mm)
    k_nominal: float            # Chiều cao đầu lục giác danh nghĩa (mm)
    k_min: float                # Chiều cao đầu tối thiểu (mm)
    k_max: float                # Chiều cao đầu tối đa (mm)
    e_min: float                # Đường kính đỉnh góc lục giác (mm)
    dw_min: Optional[float]     # Đường kính gờ đệm mặt tỳ (washer face) (mm, None nếu Cấp C)
    c_min: Optional[float]      # Chiều dày gờ đệm tối thiểu (mm, None nếu Cấp C)
    c_max: Optional[float]      # Chiều dày gờ đệm tối đa (mm, None nếu Cấp C)
    r_min: float                # Bán kính lượn góc chân cổ bu lông (mm)
    chamfer_angle_deg: float = 30.0  # Góc vát mép đỉnh đầu lục giác (15 đến 30 độ)


@dataclass(frozen=True)
class BoltTypeSpec:
    """Định danh phân loại bu lông trong JIS B 1180 : 2014 (7 loại chính + Phụ lục JA)."""
    standard: str               # 'JIS_B_1180'
    type_id: int                # 1 đến 8
    type_code: str              # Mã ngắn trong Python, ví dụ 'TYPE_2_NOMINAL_COARSE_GRADE_AB'
    type_name_ja: str           # Tên tiếng Nhật chuẩn
    iso_standard: str           # Tiêu chuẩn ISO tương đương ('ISO 4014', 'ISO 4017'...)
    thread_style: str           # 'NOMINAL_SHANK' (ren lửng), 'FULL_THREAD' (ren suốt), 'REDUCED_SHANK' (thân thắt)
    pitch_type: str             # 'COARSE' (bước thô) hoặc 'FINE' (bước mịn)
    head_series: str            # 'ISO_GRADE_AB', 'ISO_GRADE_C', hoặc 'ANNEX_JA'
    is_flange_default: bool     # True cho Loại 2 (mặc định của mặt bích đường ống)
    description_vi: str         # Mô tả tiếng Việt


@dataclass(frozen=True)
class HexBoltSpec:
    """Thông số hoàn chỉnh của một bu lông lục giác cụ thể phục vụ dựng hình 3D và BOM."""
    standard: str               # 'JIS_B_1180'
    type_code: str              # Mã loại bu lông
    bolt_size: str              # 'M16', 'M20', 'M30x3' v.v.
    nominal_dia: float          # Đường kính thân danh nghĩa d (mm)
    pitch: float                # Bước ren P (mm)
    length: float               # Chiều dài danh nghĩa l (mm)
    thread_length: float        # Chiều dài ren b (mm)
    shank_length: float         # Chiều dài thân trơn ls = l - b (mm)
    shank_dia: float            # Đường kính thân ds (mm)
    head: HexHeadSpec           # Thông số kích thước đầu lục giác
    full_designation: str       # Tên hiển thị thương mại chuẩn (BOM)
