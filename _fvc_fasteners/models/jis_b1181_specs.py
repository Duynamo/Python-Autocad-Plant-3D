from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class NutDimensionSpec:
    """Quy cách kích thước hình học đai ốc lục giác theo JIS B 1181 : 2014."""
    standard: str                     # Luôn là 'JIS_B_1181'
    series: str                       # 'ISO_STYLE_1', 'ISO_STYLE_2', 'ISO_STYLE_0_THIN', 'ISO_GRADE_C', 'ANNEX_JA_REGULAR', 'ANNEX_JA_SMALL'
    nut_size: str                     # Cỡ ren: 'M6', 'M8', 'M10', 'M12', 'M16', 'M20', 'M24', 'M30', 'M30x3' v.v.
    nominal_dia: float                # Đường kính danh nghĩa ren d (mm)
    pitch: float                      # Bước ren P (mm)
    s_nominal: float                  # Bề rộng giác cờ-lê danh nghĩa (Width across flats) (mm)
    s_min: float                      # Giác cờ-lê tối thiểu (mm)
    s_max: float                      # Giác cờ-lê tối đa (mm)
    m_nominal: float                  # Chiều cao đai ốc danh nghĩa (Height of nut) (mm)
    m_min: float                      # Chiều cao tối thiểu (mm)
    m_max: float                      # Chiều cao tối đa (mm)
    e_min: float                      # Đường kính đỉnh góc lục giác tối thiểu (Corner diameter) (mm)
    dw_min: Optional[float]           # Đường kính gờ đệm mặt tỳ (Washer face diameter) (mm, None nếu Cấp C hoặc không có)
    da_min: Optional[float]           # Đường kính vát mép miệng ren tối thiểu (mm)
    da_max: Optional[float]           # Đường kính vát mép miệng ren tối đa (mm)
    chamfer_angle_deg: float = 30.0   # Góc vát mép ngoài (15 đến 30 độ)
    chamfer_sides: int = 2            # Số mặt vát mép: 1 mặt, 2 mặt hoặc 0 mặt (unchamfered)


@dataclass(frozen=True)
class NutTypeSpec:
    """Định danh 12 chủng loại đai ốc trong JIS B 1181 : 2014 (8 ISO + 4 Phụ lục JA)."""
    standard: str                     # 'JIS_B_1181'
    type_id: int                      # 1 đến 12
    type_code: str                    # Mã code duy nhất trong hệ thống, ví dụ 'ISO_4032_STYLE_1_COARSE'
    type_name_ja: str                 # Tên tiếng Nhật chuẩn trong tiêu chuẩn
    type_name_en: str                 # Tên tiếng Anh kỹ thuật chuẩn
    iso_standard: str                 # Tiêu chuẩn ISO tương đương ('ISO 4032', 'ISO 4033', 'ANNEX_JA'...)
    nut_style: str                    # 'STYLE_1', 'STYLE_2', 'STYLE_0_THIN', 'ANNEX_JA'
    pitch_type: str                   # 'COARSE', 'FINE', hoặc 'COARSE_AND_FINE'
    product_grade: str                # 'GRADE_AB', 'GRADE_C', 'JIS_JA'
    dimension_series: str             # Trỏ đến series kích thước hình học ('ISO_STYLE_1', 'ISO_STYLE_2'...)
    is_flange_default: bool           # True cho ISO 4032 Style 1 Coarse (mặc định mặt bích)
    description_vi: str               # Mô tả chi tiết tiếng Việt


@dataclass(frozen=True)
class HexNutSpec:
    """Thông số đối tượng đai ốc hoàn chỉnh phục vụ dựng hình 3D Solid và xuất bảng kê BOM."""
    standard: str                     # 'JIS_B_1181'
    type_code: str                    # Mã loại đai ốc
    nut_size: str                     # 'M16', 'M20', 'M30x3' v.v.
    nominal_dia: float                # Đường kính ren danh nghĩa (mm)
    pitch: float                      # Bước ren P (mm)
    dimensions: NutDimensionSpec      # Thông số hình học chi tiết s, m, e, dw
    material: str = "STEEL_CLASS_8"   # Cấp bền vật liệu mặc định
    full_designation: str = ""        # Tên thương mại hiển thị trên bản vẽ / BOM
