from typing import Optional
try:
    import varmain.primitiv as prim
except ImportError:
    from .nut import prim

class GasketObject:
    """Wrapper cho đối tượng Solid 3D Gioăng đệm làm kín."""
    def __init__(self, shape, od: float, id_: float, thickness: float):
        self._shape = shape
        self.od = od
        self.id = id_
        self.thickness = thickness

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
        self._shape.translate(vec)
        return self

    def uniteWith(self, other):
        if hasattr(other, "_shape"):
            self._shape.uniteWith(other._shape)
            other._shape.erase()
        else:
            self._shape.uniteWith(other)
            other.erase()
        return self

    def erase(self):
        self._shape.erase()

    def unwrap(self):
        return self._shape


def Gasket(
    s,
    od: float,
    id_: float,
    thickness: float = 3.0
) -> GasketObject:
    """Tạo tấm đệm gioăng làm kín (Gasket) tiêu chuẩn JIS B 2220 / JIS B 1217.
    Gốc tọa độ đặt tại tâm đối xứng (Z = -tg/2 đến +tg/2).
    
    Args:
        s: Subpart container
        od: Đường kính ngoài gioăng (thường bằng gờ Raised Face g của bích)
        id_: Đường kính trong gioăng (thường bằng d0 hoặc d_bore của bích)
        thickness: Chiều dày gioăng tg (mặc định 3.0mm cho <20K, 4.5mm cho >=20K)
    """
    tg = float(thickness)
    r_out = float(od) / 2.0
    r_in = float(id_) / 2.0
    
    gasket_solid = prim.CYLINDER(s, R=r_out, H=tg, O=r_in)
    gasket_solid.translate((0, 0, -tg / 2.0))
    
    return GasketObject(gasket_solid, od=od, id_=id_, thickness=tg)
