from .db.reader import get_flange_dimensions
from .geometry.builder import build_jis_flange_solid
from .models.dimensions import FlangeDimensions

class JisFlangeObject:
    """Wrapper cho đối tượng Solid 3D mặt bích JIS trong AutoCAD Plant 3D.
    Hỗ trợ method chaining: .rotateY(90).translate((x, y, z))
    """
    def __init__(self, shape, dim: FlangeDimensions):
        self._shape = shape
        self.dim = dim

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


def JisFlange(
    s,
    rating: str = "10K",
    dn: int = 50,
    flange_type: str = "IT",
    has_holes: bool = False,
    has_rf: bool = True,
    has_hub: bool = False,
    has_bore: bool = False
) -> JisFlangeObject:
    """Hàm Factory chính tạo mặt bích tiêu chuẩn Nhật Bản JIS B 2220.
    
    Args:
        s: Subpart container của AutoCAD Plant 3D.
        rating: Cấp áp suất ('10K', '7K5', '5K', '20K'). Mặc định là '10K'.
        dn: Cỡ danh định A (10, 15, ..., 1500). Mặc định là 50.
        flange_type: Loại bích ('IT', 'SOP', 'WN', 'BL'). Mặc định là 'IT' (cho Van).
        has_holes: True nếu muốn đục lỗ bu lông (LOD cao). Mặc định là False (nhẹ model).
        has_rf: True nếu muốn gờ nổi Raised Face. Mặc định là True.
        has_hub: True nếu muốn dựng thêm cổ côn bích. Mặc định là False.
        has_bore: True nếu muốn khoét rỗng lỗ tâm d0 hoặc d_bore (khi dùng làm bích rời kết nối ống).
        
    Returns:
        JisFlangeObject: Đối tượng Solid bọc ngoài với đầy đủ method xoay, dịch chuyển và thuộc tính .dim.
    """
    dim = get_flange_dimensions(rating=rating, dn=dn, flange_type=flange_type)
    shape = build_jis_flange_solid(
        s=s,
        dim=dim,
        has_holes=has_holes,
        has_rf=has_rf,
        has_hub=has_hub,
        has_bore=has_bore
    )
    return JisFlangeObject(shape, dim)
