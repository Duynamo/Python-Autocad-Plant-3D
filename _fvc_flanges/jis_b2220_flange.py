import math
from typing import Optional
from .db.jis_b2220_reader import get_flange_dimensions
from .geometry.builder import build_jis_flange_solid
from .models.dimensions import FlangeDimensions

# Kết nối sang package _fvc_fasteners độc lập
try:
    from _fvc_fasteners import get_bolt_for_flange, HexBolt, StudBolt, FlangeBoltSelection
except ImportError:
    get_bolt_for_flange = None
    HexBolt = None
    StudBolt = None
    FlangeBoltSelection = None

class JisFlangeObject:
    """Wrapper cho đối tượng Solid 3D mặt bích JIS trong AutoCAD Plant 3D.
    Hỗ trợ method chaining: .rotateY(90).translate((x, y, z))
    """
    def __init__(self, shape, dim: FlangeDimensions, bolt=None, material: str = "CARBON_STEEL"):
        self._shape = shape
        self.dim = dim
        self.bolt = bolt
        self.material = material

    def rotateX(self, deg: float):
        self._shape.rotateX(deg)
        return self

    def rotateY(self, deg: float):
        self._shape.rotateY(deg)
        return self

    def rotateZ(self, deg: float):
        self._shape.rotateZ(deg)
        return self

    def translate(self, vec):
        self._shape.translate(vec)
        return self

    def move(self, vec):
        """Alias cho translate"""
        self._shape.translate(vec)
        return self

    def uniteWith(self, other):
        """Gộp khối other vào bích này và tự động erase other."""
        if hasattr(other, "_shape"):
            self._shape.uniteWith(other._shape)
            other._shape.erase()
        else:
            self._shape.uniteWith(other)
            other.erase()
        return self

    def subtractFrom(self, other):
        """Trừ khối other khỏi bích này và tự động erase other."""
        if hasattr(other, "_shape"):
            self._shape.subtractFrom(other._shape)
            other._shape.erase()
        else:
            self._shape.subtractFrom(other)
            other.erase()
        return self

    def erase(self):
        """Giải phóng khối này khỏi bộ nhớ AutoCAD."""
        self._shape.erase()

    def unwrap(self):
        """Lấy raw shape object để trả về cho engine Plant 3D."""
        return self._shape


def JisB2220Flange(
    s,
    rating: str = "10K",
    dn: int = 50,
    flange_type: str = "IT",
    standard: str = "JIS_B_2220",
    has_holes: bool = False,
    has_rf: bool = True,
    has_hub: bool = False,
    has_bore: bool = False,
    has_bolts: bool = False,
    bolt_type: str = "HEX",
    material: str = "CARBON_STEEL"
) -> JisFlangeObject:
    """Hàm Factory tạo mặt bích thép tiêu chuẩn Nhật Bản JIS B 2220.
    
    Args:
        s: Subpart container của AutoCAD Plant 3D.
        rating: Cấp áp suất ('5K', '10K', '7K5', '16K', '20K', '30K', '40K', '63K').
        dn: Cỡ danh định A (10, 15, ..., 1500). Mặc định là 50.
        flange_type: Loại bích ('IT', 'SOP', 'WN', 'BL'). Mặc định là 'IT' (cho Van).
        standard: Tiêu chuẩn bích ('JIS_B_2220'). Mặc định là 'JIS_B_2220'.
        has_holes: True nếu muốn đục lỗ bu lông (LOD cao). Mặc định là False.
        has_rf: True nếu muốn gờ nổi Raised Face. Mặc định là True.
        has_hub: True nếu muốn dựng thêm cổ côn bích. Mặc định là False.
        has_bore: True nếu muốn khoét rỗng lỗ tâm d0 hoặc d_bore.
        has_bolts: True nếu muốn tự động dựng cụm bu-lông từ _fvc_fasteners quanh vòng chia C.
        bolt_type: 'HEX' (Bu-lông lục giác) hoặc 'STUD' (Gu-zông 2 đầu ren).
        material: Mác vật liệu bích (mặc định 'CARBON_STEEL', ví dụ 'SUS304', 'SUS316'...)
        
    Returns:
        JisFlangeObject: Đối tượng Solid bọc ngoài với method xoay, dịch chuyển, thuộc tính .dim và .bolt.
    """
    dim = get_flange_dimensions(rating=rating, dn=dn, flange_type=flange_type, standard=standard)
    
    bolt_info = None
    if get_bolt_for_flange is not None:
        bolt_info = get_bolt_for_flange(rating=rating, dn=dn, flange_std=standard)
    
    # 1. Dựng khối Solid mặt bích
    shape = build_jis_flange_solid(
        s=s,
        dim=dim,
        has_holes=has_holes,
        has_rf=has_rf,
        has_hub=has_hub,
        has_bore=has_bore
    )
    
    # 2. Dựng cụm bu-lông nếu has_bolts=True và có module fasteners
    if has_bolts and bolt_info and HexBolt is not None:
        r_bolt = dim.c / 2.0
        n_holes = dim.no
        angle_step = 360.0 / n_holes
        
        for i in range(n_holes):
            rad = math.radians(i * angle_step)
            bx = r_bolt * math.cos(rad)
            by = r_bolt * math.sin(rad)
            
            if bolt_type.upper() == "STUD" and StudBolt is not None:
                bolt_obj = StudBolt(s, bolt_size=bolt_info.bolt_size, length=bolt_info.lt)
                bolt_obj.translate((bx, by, dim.t / 2.0))
            else:
                bolt_obj = HexBolt(s, bolt_size=bolt_info.bolt_size, length=bolt_info.l)
                bolt_obj.translate((bx, by, 0.0))
                
            shape.uniteWith(bolt_obj.unwrap())
            bolt_obj.erase()
            
    return JisFlangeObject(shape, dim, bolt_info, material=material)

# Alias tương thích ngược
JisFlange = JisB2220Flange
