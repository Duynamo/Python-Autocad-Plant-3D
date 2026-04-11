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

def ARC3D(s, D, R, A):
    """
    Tạo co (elbow) thông thường.
    @param s: Đối tượng chính.
    @param D: 1/2 đường kính (bán kính ống). (Ghi chú: Tài liệu ghi D là 1/2 đường kính).
    @param R: Bán kính uốn (Bend radius - khoảng cách từ tâm xoay đến tâm ống).
    @param A: Góc uốn (Bend angle - ví dụ 90.0, 45.0).
    Ghi chú: Điểm gốc là giao điểm của đường tâm xuyên qua cả hai đầu.
    """
    pass

def ARC3D2(s, D, D2, R, A):
    """
    Tạo co giảm (Reduced elbow).
    @param D: 1/2 đường kính đầu thứ nhất.
    @param D2: 1/2 đường kính đầu thứ hai (nếu không đặt, D2 sẽ bằng D).
    @param R: Bán kính uốn.
    @param A: Góc uốn.
    """
    pass

def ARC3DS(s, D, D2, R, A, S):
    """
    Tạo co phân đoạn (Segmented elbow/Miter elbow).
    @param S: Số lượng phân đoạn (Number of segments).
    """
    pass

def BOX(s, L, W, H):
    """
    Tạo một khối hộp chữ nhật.
    @param L: Chiều dài khối hộp (Length).
    @param W: Chiều rộng khối hộp (Width).
    @param H: Chiều cao khối hộp (Height).
    Ghi chú: Điểm gốc (Base point) nằm ở trọng tâm khối (Center of gravity).
    """
    pass

def CONE(s, R1, R2, H, E=0.0):
    """
    Tạo khối nón hoặc nón cụt.
    @param R1: Bán kính đáy dưới (Bottom radius).
    @param R2: Bán kính đáy trên (Upper radius). Nếu R2 = 0.0 sẽ tạo nón nhọn, R2 > 0.0 tạo nón cụt (Frustum).
    @param H: Chiều cao (Height).
    @param E: Độ lệch tâm giữa tâm đáy trên và tâm đáy dưới (Eccentricity).
    Ghi chú: Điểm gốc nằm ở tâm mặt đáy dưới.
    """
    pass

def CYLINDER(s, R, H, O=0.0):
    """
    Tạo khối trụ tròn.
    @param R: Bán kính (Radius).
    @param H: Chiều cao (Height).
    @param O: Bán kính lỗ rỗng xuyên tâm (Hole radius).
    Ghi chú: Điểm gốc nằm ở tâm mặt đáy.
    """
    pass

def ELLIPSOIDHEAD(s, R):
    """
    Tạo nắp chỏm cầu elip chuẩn (Normalized ellipsoid head).
    @param R: Bán kính.
    Ghi chú: Có thể dùng obj.parameters() để lấy chiều cao H tính toán được.
    """
    pass

def ELLIPSOIDHEAD2(s, R):
    """
    Tạo nắp chỏm cầu elip với chiều cao cố định h = 0.5 * R.
    """
    pass

def ELLIPSOIDSEGMENT(s, RX, RY, A1, A2, A3, A4):
    """
    Tạo một phân đoạn hình elip (giống quả bóng bầu dục).
    @param RX: Trục elip lớn (Big ellipsoid axis).
    @param RY: Trục elip nhỏ (Small ellipsoid axis).
    @param A1: Góc xoay hoàn toàn (Complete rotation angle).
    @param A2: Góc bắt đầu xoay (Start angle of rotation).
    @param A3: Góc bắt đầu của elip (Start angle of ellipse).
    @param A4: Góc kết thúc của elip (End angle of ellipse).
    """
    pass

def HALFSPHERE(s, R):
    """
    Tạo khối bán cầu (Half sphere).
    @param R: Bán kính.
    """
    pass

def PYRAMID(s, L, W, H, HT):
    """
    Tạo hình kim tự tháp hoặc kim tự tháp cụt (Frustum pyramid).
    @param L: Chiều dài đáy.
    @param W: Chiều rộng đáy.
    @param H: Chiều cao khối cụt. Nếu HT không được đặt, H là tổng chiều cao.
    @param HT: Tổng chiều cao đến đỉnh kim tự tháp.
    Ghi chú: Điểm gốc nằm giữa hình chữ nhật đáy.
    """
    pass

def ROUNDRECT(s, L, W, H, R2, E):
    """
    Tạo khối chuyển tiếp từ hình chữ nhật sang hình tròn (Transition rectangle to circle).
    @param L, W: Kích thước hình chữ nhật đáy.
    @param H: Chiều cao khối.
    @param R2: Bán kính hình tròn đỉnh.
    @param E: Độ lệch tâm giữa tâm đỉnh và tâm đáy.
    """
    pass

def SPHERESEGMENT(s, R, P, Q):
    """
    Tạo một phân đoạn hình cầu (Sphere segment).
    @param R: Bán kính hình cầu.
    @param P: Chiều cao phân đoạn.
    @param Q: Chiều cao tính từ tâm quả cầu đến điểm bắt đầu phân đoạn.
    """
    pass

def TORISPHERICHEAD(s, R):
    """
    Tạo nắp chỏm cầu Torispheric chuẩn.
    """
    pass

def TORISPHERICHEAD2(s, R):
    """
    Tạo nắp chỏm cầu Torispheric với bán kính nhỏ mặc định = 25.00.
    """
    pass

def TORISPHERICHEADH(s, R, H):
    """
    Tạo nắp chỏm cầu Torispheric có khai báo chiều cao H cụ thể.
    """
    pass

def TORUS(s, R1, R2):
    """
    Tạo khối hình xuyến (Torus).
    @param R1: Bán kính ngoài (Outer radius).
    @param R2: Bán kính trong/bán kính ống (Inner radius).
    """
    pass

# =========================================================================
# 3. CÁC HÀM HIỆU CHỈNH (MODIFIER FUNCTIONS)
# =========================================================================

"""
Ghi chú quan trọng: Sau khi thực hiện các phép toán Boolean (uniteWith, subtractFrom, intersectWith),
phải gọi hàm .erase() cho đối tượng phụ để giải phóng bộ nhớ.
"""

# --- uniteWith & subtractFrom ---
# Ví dụ thực tế: Hàm CPMB (Compound Multi-Block)
def CPMB_Reference(s, L=54.0, B=22.0, D1=220.0, D2=114.3, ID="CPMB", **kw):
    O = CON_OF_DIV(D2)/2.0
    o1 = CYLINDER(s, R=D2/2.0, H=L-B, O=O).rotateY(90).translate((B, 0, 0))
    o0 = CYLINDER(s, R=D1/2.0, H=B, O=O).rotateY(90)
    o0.uniteWith(o1) # Hợp nhất o1 vào o0
    o1.erase()      # Xóa o1 khỏi bộ nhớ
    
    o2 = CYLINDER(s, R=O, H=L-B, O=0.0).rotateY(90).translate((B, 0, 0))
    o0.subtractFrom(o2) # Trừ khối o2 khỏi o0
    o2.erase()
    s.setPoint((0, 0, 0), (-1, 0, 0))
    s.setPoint((L, 0, 0), (1, 0, 0))

# --- intersectWith ---
# Ví dụ thực tế: Hàm CADAPT_SQ2RO_Sub (Trang 25)
def CADAPT_SQ2RO_Sub_Reference(s, LL=715.0, LW=700.0, R=225.0, OL=919.19, OW=698.28, H=2515.45, **kw):
    # (Phần tính toán tọa độ RB, RA, RE...)
    o1 = CONE(s, R1=RB, R2=R, H=H, E=RE).rotateZ(RA)
    o2 = CADAPT_SQ2SQ_Sub(s, LL=LL, LW=LW, ...)
    o1.intersectWith(o2) # Lấy phần giao giữa nón và hình hộp cụt
    o2.erase()

# --- rotateX & rotateZ ---
# Ví dụ thực tế: Hàm CSGC004 (Trang 27, 29)
def CSGC004_Reference(s, D=116.0, L=30.0, W=4.0, K=0.0, H=95.0, M1=10.0, M2=0.0, **kw):
    # (Phần tính toán R1, R2, H1, H2, KWdt...)
    o1a = BOX(s, L=M1, W=KWdt, H=H2).translate((0.0-(H2/2.0)-H1, 0.0, 0.0))
    o1b = BOX(s, L=M1, W=KWdt, H=H2).translate((0.0-(H2/2.0)-H1, 0.0, 0.0)).rotateX(60.0)
    o1c = BOX(s, L=M1, W=KWdt, H=H2).translate((0.0-(H2/2.0)-H1, 0.0, 0.0)).rotateX(-60.0)
    o1a.uniteWith(o1b)
    o1b.erase()
    o1a.uniteWith(o1c)
    o1c.erase()
    o1a.rotateZ(180.0)

# --- setTransformationMatrix, pointAt, directionAt ---
# Ví dụ thực tế: Hàm CPNO (Trang 31, 36, 37)
def CPNO_Reference(s, D=114.3, R=300.0, L=100.0, D2=0.0, A=90.0, OF=0.0, **kw):
    vC = CPNO_util(D=D, D2=D2, OF=OF, L=L, R=R, A=A)
    o1 = ARC3D(s, D=R, R=vC[6], A=vC[2])
    p2 = o1.pointAt(1) # Lấy vị trí port 1 của co
    
    # Tính toán xMove, yMove dựa trên tọa độ port p2
    t1 = mTransform().translate((xMove, yMove, 0.0))
    o1.setTransformationMatrix(t1) # Di chuyển toàn bộ co theo ma trận
    
    s.setPoint((0, 0, 0), (0, -1, 0))
    # Đặt port cho đối tượng chính dựa trên port của đối tượng con sau khi biến đổi
    s.setPoint(t1 * o1.pointAt(1), o1.directionAt(1))

# =========================================================================
# 4. CÁC HÀM TRUY VẤN THÔNG TIN (REQUEST FUNCTIONS)
# =========================================================================

def parameters_example():
    """
    VÍ DỤ LẤY THÔNG SỐ (.parameters):
    # Lấy thông số của một khối đã dựng (ví dụ nắp chỏm cầu để biết chiều cao thực tế)
    o2 = TORISPHERICHEAD(s, R=D/2.0).rotateY(90.0)
    vT = o2.parameters()
    vTH = float(vT["H"]) # Lấy chiều cao H từ danh sách tham số của o2
    """
    pass

def pointAt_example():
    """
    VÍ DỤ TRUY VẤN PORT (.pointAt / .directionAt):
    p2 = o1.pointAt(1)      # Lấy tọa độ điểm kết nối số 1 của đối tượng o1
    dir2 = o1.directionAt(1) # Lấy hướng của điểm kết nối số 1
    
    # Dùng kết quả để đặt port cho đối tượng chính 's'
    s.setPoint(p2, dir2)
    """
    pass

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

# =========================================================================
# 6. VÍ DỤ HOÀN CHỈNH (COMPLETE SCRIPT EXAMPLES)
# =========================================================================

"""
Dưới đây là các ví dụ hoàn chỉnh trích từ tài liệu để bạn tham khảo cấu trúc
kết hợp giữa Metadata và Logic dựng hình.
"""

# -------------------------------------------------------------------------
# VÍ DỤ 1: CPFLR (Lapped Flange - Mặt bích xoay) - Trang 2 & 39
# -------------------------------------------------------------------------

@activate(Group="Flange", TooltipShort="Lapped Flange", LengthUnit="mm")
@group("MainDimensions")
@param(L=LENGTH, TooltipShort="Length")
@param(D1=LENGTH, TooltipShort="Outer Diameter")
@param(D2=LENGTH, TooltipShort="Inner Diameter")
def CPFLR(s, L=22.0, D1=220.0, D2=114.3, ID="CPFLR", **kw):
    # Dựng hình trụ cơ bản và xoay 90 độ quanh trục Y
    o0 = CYLINDER(s, R=D1/2.0, H=L, O=D2/2.0).rotateY(90.0)
    
    # Thiết lập 2 điểm kết nối ở 2 mặt bích
    s.setPoint((0.0, 0.0, 0.0), (-1.0, 0.0, 0.0), 0.0)
    s.setPoint((L, 0.0, 0.0), (1.0, 0.0, 0.0), 0.0)

# -------------------------------------------------------------------------
# VÍ DỤ 2: CPMB (Compound Multi-Block) - Trang 23-32
# Ví dụ này minh họa đầy đủ các phép toán Unite, Subtract và Translate
# -------------------------------------------------------------------------

def CPMB(s, L=54.0, B=22.0, D1=220.0, D2=114.3, ID="CPMB", **kw):
    # Tính toán bán kính lỗ rỗng
    O = CON_OF_DIV(D2)/2.0
    
    # 1. Tạo đối tượng nhánh (o1), xoay và di chuyển
    o1 = CYLINDER(s, R=D2/2.0, H=L-B, O=O).rotateY(90).translate((B, 0, 0))
    
    # 2. Tạo đối tượng gốc (o0)
    o0 = CYLINDER(s, R=D1/2.0, H=B, O=O).rotateY(90)
    
    # 3. Hợp nhất o1 vào o0 và xóa o1 khỏi bộ nhớ
    o0.uniteWith(o1)
    o1.erase()
    
    # 4. Tạo khối trừ (o2) để tạo lỗ rỗng xuyên suốt
    o2 = CYLINDER(s, R=O, H=L-B, O=0.0).rotateY(90).translate((B, 0, 0))
    o0.subtractFrom(o2)
    o2.erase()
    
    # 5. Đặt các điểm kết nối
    s.setPoint((0, 0, 0), (-1, 0, 0))
    s.setPoint((L, 0, 0), (1, 0, 0))

# -------------------------------------------------------------------------
# VÍ DỤ 3: TESTSCRIPT (Script đơn giản để test) - Trang 46
# -------------------------------------------------------------------------

@activate(Group="Support", TooltipShort="Test script", LengthUnit="in")
@group("MainDimensions")
@param(D=LENGTH, TooltipShort="Cylinder Diameter")
@param(L=LENGTH, TooltipShort="Length of the Cylinder")
def TESTSCRIPT(s, D=80.0, L=150.0, OF=-1, K=1, **kw):
    # Dựng một ống trụ đơn giản nằm ngang
    CYLINDER(s, R=D/2, H=L, O=0.0).rotateY(90)
    s.setPoint((0,0,0), (-1,0,0))
    s.setPoint((L,0,0), (1,0,0))
