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
    t: float             # Tổng chiều dày bích (t) - ĐÃ BAO GỒM CHIỀU CAO GỜ NÂNG f (Vành ngoài dày t - f)
    total_len: float     # Tổng chiều dài bích (T)
    hub_small: float     # Đường kính cổ nhỏ (a)
    hub_large: float     # Đường kính cổ lớn (b)

    # 4. Nhóm kích thước đường kính trong & hàn ống (内径 & 鋼管外径)
    d0: float            # Đường kính trong lỗ khoét bích hàn trượt SOP, SOH, SW (d0) - Nơi lồng ống vào để hàn
    pipe_od: float       # Đường kính ngoài ống thép tương ứng (OD ống, khớp với mép hàn a của WN)
    d_bore: float        # Đường kính trong lòng ống / cổ hàn WN, SW (d a) hoặc IT (d 参考)
    
    # Alias hỗ trợ tương thích ngược
    inner_dia: float = 0.0 # Tương đương d0 hoặc d_bore

    @property
    def base_t(self) -> float:
        """Chiều dày vành bích cơ sở ngoài (phần không có gờ nâng) = t - f"""
        return (self.t - self.f) if self.f > 0 else self.t
