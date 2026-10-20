from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SheetGasketDimension:
    """Kích thước gioăng tấm đệm phẳng (Sheet Gasket) theo JIS B 2404 : 2018 (Bảng 6 - Bảng 10)."""
    standard: str                     # 'JIS_B_2404'
    rating: str                       # '2K', '5K', '10K', '10K_THIN', '16K', '20K', '30K'
    dn: int                           # Cỡ danh định mm (10, 15, ..., 1500)
    shape: str                        # 'FULL_FACE' (全面形) hoặc 'RING' (リング)
    facing: str                       # 'FF', 'RF', 'MF', 'TG'
    d1: float                         # Đường kính trong gioăng (mm)
    d2: float                         # Đường kính ngoài gioăng (mm, D hoặc D3)
    c: Optional[float] = None         # Đường kính vòng chia bu lông PCD (cho Full-Face)
    h: Optional[float] = None         # Đường kính lỗ bu lông (cho Full-Face)
    no: Optional[int] = None          # Số lỗ bu lông (cho Full-Face)
    nominal_thickness: float = 3.0    # Chiều dày tiêu chuẩn (0.5, 0.8, 1.0, 1.5, 2.0, 3.0 mm)


@dataclass(frozen=True)
class SpiralWoundGasketDimension:
    """Kích thước gioăng kim loại quấn xoắn (Spiral Wound Gasket - SWG) theo JIS B 2404 : 2018 (Bảng 15 - 26)."""
    standard: str                     # 'JIS_B_2404'
    rating: str                       # '10K', '16K', '20K', '30K', '40K', '63K'
    dn: int                           # Cỡ danh định mm (10, 15, ..., 600)
    construction: str                 # 'BASIC' (基本形), 'INNER_RING' (内輪付き), 'OUTER_RING' (外輪付き), 'INNER_OUTER_RING' (内外輪付き)
    facing: str                       # 'RF', 'MF', 'TG'
    d1: Optional[float]               # Đường kính trong vành trong (Inner Ring ID)
    d2: float                         # Đường kính trong dải quấn (Winding ID)
    d3: float                         # Đường kính ngoài dải quấn (Winding OD)
    d4: Optional[float]               # Đường kính ngoài vành ngoài (Outer Ring OD)
    t_winding: float = 4.5            # Chiều dày dải quấn thân (4.5 hoặc 3.2 mm)
    t_ring: float = 3.0               # Chiều dày vành dẫn hướng (3.0 hoặc 2.0 mm)


@dataclass(frozen=True)
class PtfeJacketGasketDimension:
    """Kích thước gioăng bọc màng PTFE (PTFE Jacketed Gasket) theo JIS B 2404 : 2018 (Bảng 13 - 14)."""
    standard: str                     # 'JIS_B_2404'
    rating: str                       # '5K', '10K', '10K_THIN', '16K', '20K'
    dn: int                           # Cỡ danh định mm (15, 20, ..., 600)
    jacket_type: str                  # 'S' (切込み - Slit), 'M' (くり抜き - Milled), 'F' (融着 - Welded)
    facing: str                       # 'FF', 'RF'
    d1: float                         # Đường kính trong (mm)
    d2: float                         # Đường kính ngoài (mm)
    nominal_thickness: float = 3.0    # 2.0 hoặc 3.0 mm


@dataclass(frozen=True)
class GasketSpec:
    """Quy cách gioăng đệm mặt bích hợp nhất phục vụ dựng mô hình 3D Solid và bảng kê BOM."""
    standard: str                     # 'JIS_B_2404'
    family: str                       # 'SHEET', 'SPIRAL_WOUND', 'PTFE_JACKET', 'INSULATING_KIT'
    rating: str                       # '10K', '20K'...
    dn: int                           # Cỡ danh định
    facing: str                       # 'RF', 'FF', 'MF', 'TG'
    d_inner: float                    # Đường kính trong nhỏ nhất của gioăng (d1 hoặc d2)
    d_outer: float                    # Đường kính ngoài lớn nhất của gioăng (d2 hoặc d4)
    thickness: float                  # Chiều dày làm việc tổng thể tg (mm)
    shape_code: str                   # 'RING', 'FULL_FACE', 'SWIC', 'SWC', 'SWI', 'SW_BASIC', 'JACKET_M', 'JACKET_S'
    
    # Chi tiết cho Full-Face
    pcd: Optional[float] = None       # PCD nếu có lỗ bu lông
    hole_dia: Optional[float] = None  # Đường kính lỗ bu lông
    hole_count: Optional[int] = None  # Số lỗ bu lông

    # Chi tiết cho Spiral Wound
    d1_inner_ring: Optional[float] = None
    d2_winding_in: Optional[float] = None
    d3_winding_out: Optional[float] = None
    d4_outer_ring: Optional[float] = None

    # Thuộc tính cách điện chống ăn mòn điện hóa (Galvanic Insulation Kit)
    is_insulating: bool = False
    gasket_material: str = "NON_ASBESTOS"  # 'NON_ASBESTOS', 'GRAPHITE', 'PTFE', 'G10_EPOXY', '316L_GRAPHITE'
    sleeve_material: Optional[str] = None  # 'MYLAR', 'G10' nếu cách điện
    washer_material: Optional[str] = None  # 'G10' nếu cách điện
    full_designation: str = ""        # Tên thương mại hiển thị trên bản vẽ BOM
