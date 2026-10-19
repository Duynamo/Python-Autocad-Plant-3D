from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class WasherDimensionSpec:
    """Quy cách kích thước hình học vòng đệm phẳng theo JIS B 1256 : 2008."""
    standard: str                     # Luôn là 'JIS_B_1256'
    series: str                       # 'ISO_NORMAL_A', 'ISO_NORMAL_CHAMFERED_A', 'ISO_NORMAL_C', 'ISO_SMALL_A', 'ISO_LARGE_A', 'ISO_LARGE_C', 'ISO_EXTRA_LARGE_C', 'ANNEX_JA_SQUARE', 'JIS_POLISHED_ROUND', 'JIS_COMMERCIAL_ROUND'
    bolt_size: str                    # Cỡ bu lông: 'M6', 'M8', 'M10', 'M12', 'M16', 'M20', 'M24', 'M30' v.v.
    nominal_dia: float                # Đường kính danh nghĩa bu lông d (mm)
    d1_nominal: float                 # Đường kính lỗ trong danh nghĩa (mm)
    d1_min: float                     # Lỗ trong tối thiểu (mm)
    d1_max: float                     # Lỗ trong tối đa (mm)
    d2_nominal: float                 # Đường kính ngoài danh nghĩa (mm)
    d2_min: float                     # Đường kính ngoài tối thiểu (mm)
    d2_max: float                     # Đường kính ngoài tối đa (mm)
    h_nominal: float                  # Chiều dày danh nghĩa (mm)
    h_min: float                      # Chiều dày tối thiểu (mm)
    h_max: float                      # Chiều dày tối đa (mm)
    chamfer_angle_deg: float = 0.0    # Góc vát mép ngoài (30 - 45 độ đối với ISO 7090, 0 độ nếu phẳng)
    chamfer_c: Optional[float] = None # Kích thước vát mép c (mm, nếu có)


@dataclass(frozen=True)
class WasherTypeSpec:
    """Định danh chủng loại vòng đệm phẳng trong JIS B 1256 : 2008."""
    standard: str                     # 'JIS_B_1256'
    type_id: int                      # Số thứ tự
    type_code: str                    # Mã code hệ thống (ví dụ: 'ISO_7089_NORMAL_GRADE_A')
    type_name_ja: str                 # Tên tiếng Nhật chuẩn
    type_name_en: str                 # Tên tiếng Anh chuẩn
    iso_standard: str                 # Tiêu chuẩn tương đương ('ISO 7089', 'ISO 7090'...)
    washer_series: str                # 'NORMAL', 'NORMAL_CHAMFERED', 'SMALL', 'LARGE', 'EXTRA_LARGE', 'ANNEX_JA'
    product_grade: str                # 'GRADE_A', 'GRADE_C', 'JIS'
    dimension_series: str             # Trỏ đến bảng kích thước tương ứng
    is_flange_default: bool           # True cho ISO 7089 Normal A (Mặc định cho mối nối mặt bích)
    description_vi: str               # Mô tả chi tiết tiếng Việt


@dataclass(frozen=True)
class PlainWasherSpec:
    """Thông số đối tượng vòng đệm hoàn chỉnh phục vụ dựng mô hình 3D Solid và bảng kê BOM."""
    standard: str                     # 'JIS_B_1256'
    type_code: str                    # Mã chủng loại vòng đệm
    bolt_size: str                    # 'M16', 'M20', 'M30' v.v.
    dimensions: WasherDimensionSpec   # Thông số kích thước d1, d2, h
    hardness_class: str = "200_HV"    # '100_HV', '200_HV', '300_HV'
    material: str = "CARBON_STEEL"    # 'CARBON_STEEL', 'STAINLESS_A2', 'STAINLESS_A4', 'BRASS'
    full_designation: str = ""        # Tên thương mại hiển thị trên BOM
