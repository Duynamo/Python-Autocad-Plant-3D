import math
try:
    import varmain.primitiv as prim #type: ignore
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
                other._shape.erase()
            elif not hasattr(other, "_shape") and other is not None:
                self._shape.subtractFrom(other)
                other.erase()
        return self

    def intersectWith(self, other):
        if self._shape is not None:
            if hasattr(other, "_shape") and other._shape is not None:
                self._shape.intersectWith(other._shape)
                other._shape.erase()
            elif not hasattr(other, "_shape") and other is not None:
                self._shape.intersectWith(other)
                other.erase()
        return self

    def erase(self):
        if self._shape is not None:
            self._shape.erase()

    def unwrap(self):
        return self._shape


def build_hex_prism(s, width_across_flats: float, height: float):
    """Dựng lăng trụ lục giác đều (Hexagonal Prism) chuẩn xác bằng cách gọt khối trụ tròn.
    Gốc tọa độ: Đáy tại Z = 0, Đỉnh tại Z = height.
    
    Phương pháp (chuẩn theo đầu lục giác của Bolt):
    1. Khởi tạo khối trụ tròn ngoại tiếp CYLINDER bán kính R = s / sqrt(3), chiều cao height.
    2. Dùng 6 hộp gọt BOX tịnh tiến ra khoảng cách dist_cut theo trục X, sau đó xoay rotateZ
       quanh gốc (0,0) ở 6 góc: 0°, 60°, 120°, 180°, 240°, 300°.
    """
    s_val = float(width_across_flats)
    h_val = float(height)
    
    # Bán kính đường tròn ngoại tiếp đỉnh lục giác: R = (s / 2) / cos(30 deg) = s / sqrt(3)
    r_circ = s_val / math.sqrt(3.0)
    hex_solid = prim.CYLINDER(s, R=r_circ, H=h_val, O=0)
    
    t_cut = s_val
    w_cut = r_circ * 3.0
    h_cut = h_val * 2.5
    dist_cut = s_val / 2.0 + t_cut / 2.0
    
    for deg in [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]:
        c = prim.BOX(s, L=t_cut, W=w_cut, H=h_cut).translate((dist_cut, 0, h_val / 2.0)).rotateZ(deg)
        hex_solid.subtractFrom(c)
        c.erase()
        
    return hex_solid


def HexNut(s, bolt_size: str = "M16", series: str = "ISO_STYLE_1", has_hole: bool = False) -> FastenerObject:
    """Tạo đai ốc lục giác (Hex Nut) chuẩn JIS B 1181 : 2014 dạng đặc (tương tự đầu lục giác bu lông).
    Gốc tọa độ đặt tại tâm đáy đai ốc (Z = 0 đến Z = m).
    
    Args:
        s: Subpart container
        bolt_size: Cỡ ren ('M12', 'M16', 'M20', 'M30x3'...)
        series: Dòng series ('ISO_STYLE_1', 'ISO_STYLE_2', 'ISO_STYLE_0_THIN', 'ANNEX_JA_REGULAR'...)
        has_hole: Tạm thời vô hiệu hóa tạo lỗ rỗng để đai ốc ở dạng đặc nguyên bản.
    """
    from ..db.jis_b1181_reader import get_nut_dimension
    
    nut_dim = get_nut_dimension(bolt_size, series)
    if nut_dim:
        s_val = float(nut_dim.s_nominal)
        m_val = float(nut_dim.m_nominal)
        d_val = float(nut_dim.nominal_dia)
        # Tạo spec tương thích ngược cho FastenerObject
        spec = MetricBoltSpec("JIS_B_1181", bolt_size, d_val, nut_dim.pitch, s_val, nut_dim.e_min, m_val, m_val, 3.0, 30.0)
    else:
        spec = get_metric_bolt_spec(bolt_size)
        if not spec:
            spec = MetricBoltSpec("JIS_B_1181", bolt_size, 16.0, 2.0, 24.0, 27.71, 14.8, 10.0, 3.0, 30.0)
        s_val = float(spec.s)
        m_val = float(spec.m)
        d_val = float(spec.nominal_dia)
        
    # Tạo khối đai ốc lục giác đặc nguyên bản (giống đầu lục giác của Bolt)
    nut_solid = build_hex_prism(s, width_across_flats=s_val, height=m_val)
    return FastenerObject(nut_solid, spec)



