# -*- coding: utf-8 -*-
"""
THƯ VIỆN THAM KHẢO LẬP TRÌNH SCRIPT TRONG AUTOCAD PLANT 3D
Tổng hợp từ tài liệu: PD4214-L Radhakrishnan Annex B
Người thực hiện: Antigravity AI
"""

# =========================================================================
# 1. QUY TẮC DỰNG HÌNH CƠ BẢN (BASIC MODELING RULES)
# =========================================================================
"""
- Script là một chương trình con Python tạo ra các khối hình học parametric từ các tham số kích thước.
- Kết quả đầu ra thường là một khối solid nằm trong một block.
- Các điểm kết nối (Ports/Connection Points) cực kỳ quan trọng để căn chỉnh tự động trong mô hình piping.
- Mỗi điểm kết nối bao gồm: Vị trí (Position) và Vector hướng (Direction).
- Đơn vị tính: Thường sử dụng mm hoặc inch tùy thuộc vào thiết lập của Catalog/Spec.
"""

# =========================================================================
# 2. CÁC HÀM HÌNH HỌC CƠ BẢN (GEOMETRIC PRIMITIVES)
# =========================================================================

def BOX(s, L, W, H):
    """
    Tạo một khối hộp chữ nhật.
    @param s: Đối tượng chính (thường là tham số 's' truyền vào function)
    @param L: Chiều dài (Length)
    @param W: Chiều rộng (Width)
    @param H: Chiều cao (Height)
    Ghi chú: Điểm gốc (Base point) nằm ở trọng tâm khối.
    """
    pass

def CYLINDER(s, R, H, O=0.0):
    """
    Tạo khối trụ tròn hoặc elip.
    @param s: Đối tượng chính
    @param R: Bán kính (Radius). Nếu truyền (R1, R2) sẽ tạo trụ elip.
    @param H: Chiều cao (Height)
    @param O: Bán kính lỗ rỗng bên trong (Hole radius)
    Ghi chú: Điểm gốc nằm ở tâm mặt đáy.
    """
    pass

def CONE(s, R1, R2, H, E=0.0):
    """
    Tạo khối nón hoặc nón cụt.
    @param s: Đối tượng chính
    @param R1: Bán kính đáy dưới
    @param R2: Bán kính đáy trên (nếu = 0 thì là nón nhọn)
    @param H: Chiều cao
    @param E: Độ lệch tâm giữa tâm đáy trên và dưới (Eccentricity)
    Ghi chú: Điểm gốc nằm ở tâm mặt đáy dưới.
    """
    pass

def SPHERE(s, R):
    """
    Tạo khối cầu.
    @param R: Bán kính
    """
    pass

def TORUS(s, R1, R2):
    """
    Tạo khối hình xuyến (bánh xe).
    @param R1: Bán kính ngoài
    @param R2: Bán kính trong (ống)
    Ghi chú: Điểm gốc là giao điểm của đường tâm xuyên qua 2 đầu.
    """
    pass

def ARC3D(s, D, R, A):
    """
    Tạo co (elbow) thông thường.
    @param D: Đường kính ống (D/2 là bán kính ống)
    @param R: Bán kính uốn (Bend radius)
    @param A: Góc uốn (Bend angle)
    """
    pass

def ELLIPSOIDHEAD(s, R):
    """
    Tạo nắp chỏm cầu elip chuẩn (tỉ lệ 2:1).
    @param R: Bán kính
    """
    pass

# Các hàm khác như: PYRAMID, ROUNDRECT, HALFSPHERE, SPHERESEGMENT...

# =========================================================================
# 3. CÁC HÀM HIỆU CHỈNH (MODIFIER FUNCTIONS)
# =========================================================================

"""
Ghi chú quan trọng: Sau khi thực hiện uniteWith, subtractFrom hoặc intersectWith,
đối tượng phụ cần phải được xóa khỏi bộ nhớ bằng hàm .erase() để tối ưu hiệu suất.
"""

# obj.uniteWith(oobj)        : Hợp nhất (Union) hai đối tượng solid.
# obj.subtractFrom(oobj)     : Trừ khối (Subtraction) - lấy obj trừ đi oobj.
# obj.intersectWith(oobj)    : Lấy phần giao (Intersection) giữa hai đối tượng.
# obj.erase()                : Xóa đối tượng khỏi bộ nhớ.
# obj.rotateX(angle)         : Xoay đối tượng quanh trục X (đơn vị: độ).
# obj.rotateY(angle)         : Xoay đối tượng quanh trục Y (đơn vị: độ).
# obj.rotateZ(angle)         : Xoay đối tượng quanh trục Z (đơn vị: độ).
# obj.translate((x, y, z))   : Di chuyển đối tượng theo vector (x, y, z).
# obj.setPoint(pos, dir)      : Định nghĩa điểm kết nối (Port) cho đối tượng.
#                              pos: Tọa độ điểm (x,y,z), dir: Vector hướng (x,y,z).

# =========================================================================
# 4. CÁC HÀM TRUY VẤN THÔNG TIN (REQUEST FUNCTIONS)
# =========================================================================

# obj.parameters()           : Trả về các tham số dựng hình của đối tượng.
# obj.transformationMatrix()  : Trả về ma trận biến đổi hiện tại.
# obj.numberOfPoints()       : Trả về số lượng điểm kết nối đã định nghĩa.
# obj.pointAt(index)         : Trả về tọa độ điểm kết nối thứ 'index'.
# obj.directionAt(index)     : Trả về vector hướng của điểm kết nối thứ 'index'.

# =========================================================================
# 5. ĐỊNH NGHĨA METADATA (DECORATORS)
# =========================================================================

"""
Metadata dùng để hiển thị thông tin trong Spec Editor và Catalog Creator.
Thứ tự sử dụng:
1. @activate: Khai báo Metadata của script. Đây PHẢI là decorator đầu tiên.
   Các thuộc tính: Group, TooltipShort, TooltipLong, LengthUnit, v.v.
2. @group: Định nghĩa nhóm tham số (ví dụ: "Main Dimensions").
3. @param: Định nghĩa thông tin tham số (tên, kiểu dữ liệu, tooltip, v.v.).
4. @enum: Định nghĩa danh sách tùy chọn cho tham số kiểu ENUM.
"""

# Ví dụ cấu trúc một Script:
"""
from varmain.primitiv import *
from varmain.custom import *

@activate(Group="Support", TooltipShort="My Custom Component")
@group("Main Dimensions")
@param(D=LENGTH, TooltipShort="Diameter")
@param(L=LENGTH, TooltipShort="Length")
def MY_SCRIPT(s, D=80.0, L=150.0, **kw):
    # Dựng hình ở đây
    o1 = CYLINDER(s, R=D/2, H=L).rotateY(90)
    s.setPoint((0, 0, 0), (-1, 0, 0))
    s.setPoint((L, 0, 0), (1, 0, 0))
"""
