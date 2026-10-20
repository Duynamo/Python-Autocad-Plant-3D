import math
from typing import Optional

try:
    import varmain.primitiv as prim
except ImportError:
    from .nut import prim

from ..models.jis_b2404_specs import GasketSpec
from ..db.jis_b2404_reader import get_auto_gasket_for_flange, get_sheet_gasket_dimension


class GasketObject:
    """Wrapper cho đối tượng Solid 3D Gioăng đệm làm kín chuẩn JIS B 2404 : 2018."""
    def __init__(self, shape, od: float, id_: float, thickness: float, spec: Optional[GasketSpec] = None):
        self._shape = shape
        self.od = od
        self.id = id_
        self.thickness = thickness
        self.spec = spec
        self.is_insulating = spec.is_insulating if spec else False

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
        return self.translate(vec)

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


def Gasket(
    s,
    od: Optional[float] = None,
    id_: Optional[float] = None,
    thickness: Optional[float] = None,
    spec: Optional[GasketSpec] = None,
    rating: Optional[str] = None,
    dn: Optional[int] = None,
    facing: str = "RF",
    flange=None,
    flange1=None,
    flange2=None,
    flange1_material: str = "CARBON_STEEL",
    flange2_material: str = "CARBON_STEEL",
    gasket_override: Optional[str] = None,
    insulation_kit: bool = False,
) -> GasketObject:
    """Tạo tấm đệm gioăng làm kín (Gasket) tiêu chuẩn JIS B 2404 : 2018.
    Hỗ trợ tự động nhận diện theo mặt bích, nhận diện lệch kim loại (Cách 1) và tương thích ngược.

    Gốc tọa độ đặt tại tâm đối xứng (Z = -tg/2 đến +tg/2).

    Args:
        s: Subpart container
        spec: Đối tượng GasketSpec tra từ jis_b2404_reader
        rating: Cấp áp suất bích ('10K', '16K', '20K'...)
        dn: Cỡ danh định bích (15, 20, 50, 100, 200...)
        facing: Kiểu bề mặt bích ('RF', 'FF', 'MF', 'TG')
        flange1, flange2: Đối tượng JisFlangeObject để tự động nhận diện cặp kim loại khác nhau
        insulation_kit: Ép dùng bộ cách điện
        od, id_: Kích thước trực tiếp (tương thích ngược)
        thickness: Chiều dày gioăng tg (mặc định 3.0mm, quấn xoắn 4.5mm)
    """
    # 1. Trích xuất thông số nếu truyền đối tượng bích
    if flange1 is not None:
        dim1 = getattr(flange1, "dim", None)
        if dim1:
            rating = rating or dim1.rating
            dn = dn or dim1.dn
        mat1 = getattr(flange1, "material", flange1_material)
        mat2 = getattr(flange2, "material", flange2_material) if flange2 else mat1
    else:
        mat1 = flange1_material
        mat2 = flange2_material

    if flange is not None and rating is None and dn is None:
        f_dim = getattr(flange, "dim", None)
        if f_dim:
            rating = f_dim.rating
            dn = f_dim.dn

    # 2. Tự động tra cứu GasketSpec nếu chưa có
    if spec is None and rating is not None and dn is not None:
        spec = get_auto_gasket_for_flange(
            rating=rating,
            dn=dn,
            facing=facing,
            flange1_material=mat1,
            flange2_material=mat2,
            gasket_override=gasket_override,
            insulation_kit=insulation_kit,
            thickness_override=thickness
        )

    # 3. Phân giải kích thước hình học
    if spec:
        tg = spec.thickness
        d_out = spec.d_outer
        d_in = spec.d_inner
    else:
        tg = float(thickness) if thickness else 3.0
        d_out = float(od) if od else 100.0
        d_in = float(id_) if id_ else 50.0

    r_out = d_out / 2.0
    r_in = d_in / 2.0

    # 4. Dựng khối Solid 3D theo từng chủng loại JIS B 2404
    # --------------------------------------------------------------------------
    # CHỦNG LOẠI A: GIOĂNG KIM LOẠI QUẤN XOẮN (SPIRAL WOUND GASKET - SWG)
    # --------------------------------------------------------------------------
    if spec and spec.family == "SPIRAL_WOUND" and spec.d2_winding_in and spec.d3_winding_out:
        # Thân dải quấn chính (Winding core) dày tg = 4.5mm
        r_w_out = spec.d3_winding_out / 2.0
        r_w_in = spec.d2_winding_in / 2.0
        gasket_solid = prim.CYLINDER(s, R=r_w_out, H=tg, O=r_w_in)
        gasket_solid.translate((0, 0, -tg / 2.0))

        # Vành ngoài định tâm (Outer Ring) dày 3.0mm nếu có
        if spec.d4_outer_ring and spec.d4_outer_ring > spec.d3_winding_out:
            t_ring = 3.0
            r_ring_out = spec.d4_outer_ring / 2.0
            outer_ring = prim.CYLINDER(s, R=r_ring_out, H=t_ring, O=r_w_out)
            outer_ring.translate((0, 0, -t_ring / 2.0))
            gasket_solid.uniteWith(outer_ring)
            outer_ring.erase()

        # Vành trong bảo vệ (Inner Ring) dày 3.0mm nếu có
        if spec.d1_inner_ring and spec.d1_inner_ring < spec.d2_winding_in:
            t_ring = 3.0
            r_ring_in = spec.d1_inner_ring / 2.0
            inner_ring = prim.CYLINDER(s, R=r_w_in, H=t_ring, O=r_ring_in)
            inner_ring.translate((0, 0, -t_ring / 2.0))
            gasket_solid.uniteWith(inner_ring)
            inner_ring.erase()

    # --------------------------------------------------------------------------
    # CHỦNG LOẠI B: GIOĂNG TẤM TOÀN MẶT ĐỤC LỖ (FULL-FACE SHEET GASKET)
    # --------------------------------------------------------------------------
    elif spec and spec.shape_code == "FULL_FACE" and spec.hole_count and spec.pcd and spec.hole_dia:
        gasket_solid = prim.CYLINDER(s, R=r_out, H=tg, O=r_in)
        gasket_solid.translate((0, 0, -tg / 2.0))

        # Đục n lỗ bu lông quanh vòng chia PCD
        n_holes = spec.hole_count
        r_pcd = spec.pcd / 2.0
        r_hole = spec.hole_dia / 2.0
        h_cut = tg * 2.0

        for i in range(n_holes):
            rad = (2.0 * math.pi / n_holes) * i
            hx = r_pcd * math.cos(rad)
            hy = r_pcd * math.sin(rad)
            cutter = prim.CYLINDER(s, R=r_hole, H=h_cut, O=0)
            cutter.translate((hx, hy, -h_cut / 2.0))
            gasket_solid.subtractFrom(cutter)
            cutter.erase()

    # --------------------------------------------------------------------------
    # CHỦNG LOẠI C: GIOĂNG VÀNH TIÊU CHUẨN (RING SHEET HOẶC INSULATING RING)
    # --------------------------------------------------------------------------
    else:
        gasket_solid = prim.CYLINDER(s, R=r_out, H=tg, O=r_in)
        gasket_solid.translate((0, 0, -tg / 2.0))

    return GasketObject(gasket_solid, od=d_out, id_=d_in, thickness=tg, spec=spec)
