import math
try:
    import varmain.primitiv as prim
except ImportError:
    class _MockPrimitive:
        def __init__(self, *args, **kwargs): pass
        def translate(self, *args, **kwargs): return self
        def rotateX(self, *args, **kwargs): return self
        def rotateY(self, *args, **kwargs): return self
        def rotateZ(self, *args, **kwargs): return self
        def uniteWith(self, *args, **kwargs): return self
        def subtractFrom(self, *args, **kwargs): return self
        def intersectWith(self, *args, **kwargs): return self
        def erase(self): pass

    class _MockPrimModule:
        CYLINDER = _MockPrimitive
        CONE = _MockPrimitive
        BOX = _MockPrimitive

    prim = _MockPrimModule()

from ..db.jis_b1217_reader import get_metric_bolt_spec
from ..models.jis_b1217_specs import MetricBoltSpec

class FastenerObject:
    """Wrapper cho đối tượng Solid 3D Fastener trong AutoCAD Plant 3D.
    Hỗ trợ method chaining: .rotateX().rotateY().move().uniteWith()
    """
    def __init__(self, shape, spec: MetricBoltSpec):
        self._shape = shape
        self.spec = spec

    def rotateX(self, deg: float):
        if self._shape is not None:
            self._shape.rotateX(deg)
        return self

    def rotateY(self, deg: float):
        if self._shape is not None:
            self._shape.rotateY(deg)
        return self

    def rotateZ(self, deg: float):
        if self._shape is not None:
            self._shape.rotateZ(deg)
        return self

    def translate(self, vec):
        if self._shape is not None:
            self._shape.translate(vec)
        return self

    def move(self, vec):
        if self._shape is not None:
            self._shape.translate(vec)
        return self

    def uniteWith(self, other):
        if self._shape is not None:
            if hasattr(other, "_shape") and other._shape is not None:
                self._shape.uniteWith(other._shape)
                other._shape.erase()
            elif not hasattr(other, "_shape") and other is not None:
                self._shape.uniteWith(other)
                other.erase()
        return self

    def subtractFrom(self, other):
        if self._shape is not None:
            if hasattr(other, "_shape") and other._shape is not None:
                self._shape.subtractFrom(other._shape)
            elif not hasattr(other, "_shape") and other is not None:
                self._shape.subtractFrom(other)
        return self

    def erase(self):
        if self._shape is not None:
            self._shape.erase()

    def unwrap(self):
        return self._shape


def build_hex_prism(s, width_across_flats: float, height: float):
    """Dựng lăng trụ lục giác đều (Hexagonal Prism) chuẩn xác bằng cách gọt khối trụ tròn.
    Gốc tọa độ: Đáy tại Z = 0, Đỉnh tại Z = height.
    
    Args:
        s: Subpart container
        width_across_flats: Bề rộng giác cờ-lê s (mm)
        height: Chiều cao lăng trụ (mm)
    """
    s_val = float(width_across_flats)
    h_val = float(height)
    
    # Bán kính đường tròn ngoại tiếp đỉnh lục giác: R = (s / 2) / cos(30 deg) = s / sqrt(3)
    r_circ = s_val / math.sqrt(3.0)
    
    # 1. Khởi tạo khối trụ tròn ngoại tiếp (đáy tại Z = 0, đỉnh tại Z = h_val)
    hex_solid = prim.CYLINDER(s, R=r_circ, H=h_val, O=0)
    
    # 2. Tạo các hộp cắt (cutter) để gọt phẳng 6 mặt cách tâm s/2
    t_cut = s_val
    w_cut = r_circ * 3.0
    h_cut = h_val * 3.0
    dist_cut = s_val / 2.0 + t_cut / 2.0
    
    # Cắt 3 cặp mặt đối xứng (0 deg, 60 deg, 120 deg)
    for deg in [0.0, 60.0, 120.0]:
        rad = math.radians(deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # Hộp cắt phía dương (+dist_cut)
        c1 = prim.BOX(s, L=t_cut, W=w_cut, H=h_cut).rotateZ(deg).translate((dist_cut * cos_a, dist_cut * sin_a, h_val / 2.0))
        hex_solid.subtractFrom(c1)
        c1.erase()
        
        # Hộp cắt phía âm (-dist_cut)
        c2 = prim.BOX(s, L=t_cut, W=w_cut, H=h_cut).rotateZ(deg).translate((-dist_cut * cos_a, -dist_cut * sin_a, h_val / 2.0))
        hex_solid.subtractFrom(c2)
        c2.erase()
        
    return hex_solid


def HexNut(s, bolt_size: str = "M16", has_hole: bool = True) -> FastenerObject:
    """Tạo đai ốc lục giác (Hex Nut) chuẩn JIS B 1181 (Style 1).
    Gốc tọa độ đặt tại tâm đáy đai ốc (Z = 0 đến Z = m).
    
    Args:
        s: Subpart container
        bolt_size: Cỡ ren ('M12', 'M16', 'M20', 'M30x3'...)
        has_hole: True nếu muốn khoét rỗng lỗ ren ở giữa
    """
    spec = get_metric_bolt_spec(bolt_size)
    if not spec:
        spec = MetricBoltSpec("JIS_B_1180", bolt_size, 16.0, 2.0, 24.0, 27.71, 13.0, 10.0, 3.0, 30.0)
        
    nut_solid = build_hex_prism(s, width_across_flats=spec.s, height=spec.m)
    
    if has_hole:
        hole_r = spec.nominal_dia / 2.0
        # Khoét lỗ ren xuyên suốt chiều dày đai ốc từ Z = -0.1*m đến 1.1*m
        hole = prim.CYLINDER(s, R=hole_r, H=spec.m * 1.2, O=0).translate((0, 0, -spec.m * 0.1))
        nut_solid.subtractFrom(hole)
        hole.erase()
        
    return FastenerObject(nut_solid, spec)

