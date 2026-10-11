import math
try:
    from varmain.primitiv import * # type: ignore
except ImportError:
    pass
from ..models.dimensions import FlangeDimensions

def build_jis_flange_solid(
    s,
    dim: FlangeDimensions,
    has_holes: bool = False,
    has_rf: bool = True,
    has_hub: bool = False,
    has_bore: bool = False
):
    """Dựng khối Solid 3D mặt bích JIS B 2220 chuẩn.
    
    Hệ tọa độ cục bộ ban đầu:
    - Trục mặt bích dọc theo trục Z.
    - Chiều dày bích chính (Disc) trải từ Z = 0 đến Z = dim.t.
    - Gờ nổi Raised Face (RF) trải từ Z = dim.t đến Z = dim.t + dim.f.
    - Cổ bích (Hub) nếu có trải ngược từ Z = 0 về Z = -(dim.total_len - dim.t).
    
    Args:
        s: Subpart container của Plant 3D
        dim: FlangeDimensions (chứa d0, pipe_od, d_bore, d, t, c, h, no...)
        has_holes: True để đục lỗ bu lông (LOD cao)
        has_rf: True để tạo gờ nâng Raised Face
        has_hub: True để tạo cổ côn bích (cho IT/WN)
        has_bore: True để khoét rỗng lỗ tâm d0 hoặc d_bore (khi dùng làm bích rời kết nối ống)
    """
    # 1. Đĩa bích chính (Main Disc)
    root_shape = CYLINDER(s, R=dim.d / 2.0, H=dim.t).translate((0, 0, dim.t / 2.0))

    # 2. Gờ nâng (Raised Face)
    if has_rf and dim.f > 0 and dim.g > 0:
        rf = CYLINDER(s, R=dim.g / 2.0, H=dim.f).translate((0, 0, dim.t + dim.f / 2.0))
        root_shape.uniteWith(rf)
        rf.erase()

    # 3. Cổ bích (Hub) cho loại IT / WN nếu được yêu cầu
    if has_hub and dim.hub_large > 0 and dim.hub_small > 0:
        hub_h = dim.total_len - dim.t
        if hub_h > 0:
            hub = CONE(s, R1=dim.hub_large / 2.0, R2=dim.hub_small / 2.0, H=hub_h).translate((0, 0, -hub_h / 2.0))
            root_shape.uniteWith(hub)
            hub.erase()

    # 4. Khoét rỗng lỗ trong (Bore) theo d0 (cho SOP) hoặc d_bore (cho WN/IT)
    if has_bore and dim.flange_type != "BL":
        bore_dia = dim.d0 if dim.flange_type in ["SOP", "SOH", "SW"] else dim.d_bore
        if bore_dia > 0:
            total_bore_h = dim.total_len + dim.f + 10.0
            bore = CYLINDER(s, R=bore_dia / 2.0, H=total_bore_h).translate((0, 0, dim.t / 2.0))
            root_shape.subtractFrom(bore)
            bore.erase()

    # 5. Đục lỗ bu lông (Bolt Holes)
    if has_holes and dim.no > 0 and dim.h > 0:
        cut_h = dim.t + dim.f + 6.0
        for i in range(dim.no):
            angle = (2.0 * math.pi / dim.no) * i
            hx = (dim.c / 2.0) * math.cos(angle)
            hy = (dim.c / 2.0) * math.sin(angle)
            hole = CYLINDER(s, R=dim.h / 2.0, H=cut_h).translate((hx, hy, dim.t / 2.0))
            root_shape.subtractFrom(hole)
            hole.erase()

    return root_shape
