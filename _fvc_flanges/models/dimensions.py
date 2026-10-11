from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class FlangeDimensions:
    rating: str          # Cấp áp: '10K', '7K5', '5K', '20K'
    flange_type: str     # Loại bích: 'IT', 'SOP', 'SOH', 'WN', 'BL', 'SW', 'TR', 'LJ'
    dn: int              # Cỡ danh định A (10, 15, ..., 1500)
    
    # 1. Kích thước kết nối bu lông (接合寸法)
    d: float             # Đường kính ngoài mặt bích (D)
    c: float             # Đường kính tâm vòng chia bu lông (C / PCD)
    h: float             # Đường kính lỗ bu lông (h / Dh)
    no: int              # Số lượng lỗ bu lông (ボルトの本数)
    bolt_name: str       # Ký hiệu ren bu lông (M12, M16, M20...)
    
    # 2. Gờ nổi Raised Face (平面座)
    g: float             # Đường kính gờ nâng (g)
    f: float             # Chiều cao gờ nâng (f)
    
    # 3. Kích thước bích & cổ bích
    t: float             # Chiều dày bích (t)
    total_len: float     # Tổng chiều dài bích (T)
    hub_small: float     # Đường kính cổ nhỏ (a)
    hub_large: float     # Đường kính cổ lớn (b)
    inner_dia: float     # Đường kính trong lỗ khoét (d0 / d)
