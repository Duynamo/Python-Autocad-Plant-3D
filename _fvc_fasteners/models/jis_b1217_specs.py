from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MetricBoltSpec:
    """Quy chuẩn kích thước hình học bu-lông hệ mét theo JIS B 1180 / JIS B 1181."""
    standard: str        # 'JIS_B_1180' / 'JIS_B_1181'
    size: str            # M10, M12, M16, M20, M22, M24, M30, M30x3, M36, M36x3, M42, M42x3
    nominal_dia: float   # Đường kính danh định ren d (mm)
    pitch: float         # Bước ren P (mm)
    s: float             # Bề rộng giác ê-cu / mũ bu-lông (Width across flats) (mm)
    e: float             # Đường kính đỉnh giác ê-cu (e ≈ 1.1547 * s) (mm)
    m: float             # Chiều cao đai ốc tiêu chuẩn Style 1 (mm)
    k: float             # Chiều cao mũ bu-lông lục giác (mm)
    washer_t: float      # Bề dày vòng đệm phẳng tiêu chuẩn (mm)
    washer_od: float     # Đường kính ngoài vòng đệm (mm)


@dataclass(frozen=True)
class FlangeBoltSelection:
    """Thông số cấu hình bu-lông tiêu chuẩn cho mối nối mặt bích theo JIS B 1217 : 2018."""
    standard: str        # 'JIS_B_1217' (Tiêu chuẩn bu-lông)
    flange_std: str      # 'JIS_B_2220' (Tiêu chuẩn bích thép) hoặc 'JIS_B_2239' (Tiêu chuẩn bích gang)
    rating: str          # Cấp áp lực: '5K', '10K', '10K_THIN', '16K', '20K', '30K', '40K', '63K'
    dn: int              # Cỡ danh định A (10, 15, ..., 1500)
    bolt_size: str       # Cỡ ren bu-lông (M12, M16, M20, M30x3...)
    bolt_count: int      # Số lượng con bu-lông cho 1 mối nối (本数)
    l: float             # Chiều dài danh định bu-lông lục giác (mm)
    b: float             # Chiều dài ren bu-lông lục giác (mm)
    lt: float            # Chiều dài toàn bộ gu-zông / bu-lông 2 đầu ren (mm)
    bt: float            # Chiều dài ren gu-zông (mm)
    tg: float            # Chiều dày gioăng đệm quy ước (3.0mm hoặc 4.5mm)
