import sys
import os
import math

# 1. Đảm bảo AutoCAD nhận diện được các package _fvc_flanges và _fvc_fasteners
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

workspace_dir = r"c:\Users\Laptop\OneDrive\Desktop\Hello World\Python-Autocad-Plant-3D"
if os.path.exists(workspace_dir) and workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

# 2. Tự động reload cả 2 package để luôn cập nhật logic hình học và CSDL mới nhất khi chỉnh sửa code
for mod_name in list(sys.modules.keys()):
    if mod_name.startswith('_fvc_flanges') or mod_name.startswith('_fvc_fasteners'):
        del sys.modules[mod_name]

from _fvc_flanges import JisFlange
from _fvc_fasteners import (
    HexBolt,
    HexNut,
    StudBolt,
    PlainWasher,
    Gasket,
    get_hex_bolt,
    get_bolt_for_flange,
    get_washer_dimension,
    get_auto_gasket_for_flange,
)

try:
    import varmain.primitiv as prim #type: ignore
except ImportError: 
    from _fvc_fasteners.geometry.nut import prim

# ==============================================================================
# CẤU HÌNH THÔNG SỐ TEST CỤM KẾT NỐI (TÙY CHỈNH DỄ DÀNG KHI KIỂM TRA)
# ==============================================================================
TEST_RATING = "10K"                  # Cấp áp suất: '5K', '10K', '16K', '20K', '30K', '40K', '63K'
TEST_DN = 100                        # Cỡ danh định DN (15, 20, 25, 50, 80, 100, 150, 200, 300...)
TEST_FLANGE_TYPE = "SOP"             # Loại bích: 'SOP', 'WN', 'IT', 'BL'

# CẤU HÌNH VẬT LIỆU BÍCH - TỰ ĐỘNG PHÁT HIỆN CẶP KIM LOẠI KHÁC NHAU (CÁCH 1):
TEST_FLANGE1_MATERIAL = "CARBON_STEEL"  # Mác thép bích 1 (VD: "CARBON_STEEL", "SS400", "SF440A")
TEST_FLANGE2_MATERIAL = "CARBON_STEEL"  # Mác thép bích 2: Đổi thành "SUS304" / "SUS316" để tự động kích hoạt Bộ đệm cách điện!

# CẤU HÌNH GIOĂNG ĐỆM JIS B 2404 : 2018:
TEST_GASKET_TYPE = "auto"               # "auto": tự động chọn theo JIS B 2404 & vật liệu 2 bích (RF Sheet / SWG / Insulating Kit)
                                        # hoặc ép loại: "SHEET_RF", "SHEET_FF", "SWIC", "INSULATING_KIT"
TEST_GASKET_THICKNESS = 0.0             # 0.0: tự động chuẩn JIS B 2404 (Sheet: 3.0mm, SWG: 4.5mm), hoặc ghi đè số cụ thể
TEST_HAS_WASHERS = True                 # True: có thêm vòng đệm JIS B 1256 dưới mũ và đai ốc
TEST_WASHER_SERIES = "ISO_NORMAL_A"     # Dòng đệm: 'ISO_NORMAL_A', 'ISO_NORMAL_CHAMFERED_A', 'ANNEX_JA_SQUARE'...

# ==============================================================================
# CHỌN CHẾ ĐỘ TEST (BẠN CHỌN 1 TRONG 5 CHẾ ĐỘ DƯỚI ĐÂY)
# ==============================================================================
# - "FLANGE_CONNECTION_COMBO": CỤM COMBO 2 BÍCH ĐỐI ĐẦU: bolt -> flange1 -> gasket -> flange2 -> nut [MẶC ĐỊNH]
# - "FLANGE_WITH_BOLTS":       1 Mặt bích JIS B 2220 cắm dàn bu lông quanh vòng chia
# - "STANDALONE_BOLT":         1 Con bu lông lục giác JIS B 1180 đứng độc lập (soi giác s, mũ k)
# - "BOLT_AND_NUT":            1 Con bu lông lục giác kèm Đai ốc vặn ở đuôi ren
# - "BOLT_NUT_WASHER":         1 Con bu lông lục giác kèm Vòng đệm JIS B 1256 và Đai ốc
TEST_MODE = "FLANGE_CONNECTION_COMBO"


def run(s, **kw):
    """Hàm entry point của AutoCAD Plant 3D để render hình học."""

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 1: CỤM KẾT NỐI 2 MẶT BÍCH (bolt -> flange1 -> gasket -> flange2 -> nut)
    # --------------------------------------------------------------------------
    if TEST_MODE == "FLANGE_CONNECTION_COMBO":
        # 1. Tra cứu thông số bu lông tiêu chuẩn từ JIS B 1217
        bolt_info = get_bolt_for_flange(rating=TEST_RATING, dn=TEST_DN)
        bolt_sz = bolt_info.bolt_size if bolt_info else "M20"
        bolt_len = bolt_info.l if bolt_info else 80.0

        # 2. Khởi tạo Flange 1 và Flange 2 (JIS B 2220) kèm vật liệu tương ứng
        flange1 = JisFlange(
            s=s,
            rating=TEST_RATING,
            dn=TEST_DN,
            flange_type=TEST_FLANGE_TYPE,
            material=TEST_FLANGE1_MATERIAL,
            has_holes=True,
            has_rf=True,
            has_hub=False,
            has_bore=True,
            has_bolts=False
        )
        flange2 = JisFlange(
            s=s,
            rating=TEST_RATING,
            dn=TEST_DN,
            flange_type=TEST_FLANGE_TYPE,
            material=TEST_FLANGE2_MATERIAL,
            has_holes=True,
            has_rf=True,
            has_hub=False,
            has_bore=True,
            has_bolts=False
        )
        dim = flange1.dim

        # 3. Tạo gioăng đệm làm kín Gasket JIS B 2404 : 2018
        # Tự động chọn theo JIS B 2404 và tự động nhận diện cặp kim loại khác nhau (Cách 1 -> Bộ cách điện Dielectric Kit)
        gasket = Gasket(
            s=s,
            rating=TEST_RATING,
            dn=TEST_DN,
            facing="RF",
            flange1=flange1,
            flange2=flange2,
            flange1_material=TEST_FLANGE1_MATERIAL,
            flange2_material=TEST_FLANGE2_MATERIAL,
            gasket_override=None if TEST_GASKET_TYPE == "auto" else TEST_GASKET_TYPE,
            thickness=TEST_GASKET_THICKNESS if TEST_GASKET_THICKNESS > 0 else None,
        )
        tg = gasket.thickness
        is_dielectric = getattr(gasket, "is_insulating", False)

        # 4. Định vị Flange 1: Mặt tiếp xúc mặt dưới gioăng (-tg/2), mặt sau quay về -Z
        dz1 = -tg / 2.0 - dim.t
        flange1.translate((0, 0, dz1))

        # 5. Định vị Flange 2: Xoay 180 độ đối đầu, mặt tiếp xúc mặt trên gioăng (+tg/2), mặt sau quay về +Z
        flange2.rotateY(180)
        dz2 = tg / 2.0 + dim.t
        flange2.translate((0, 0, dz2))

        # Tọa độ mặt sau của 2 mặt bích
        z_back1 = dz1  # Mặt sau Flange 1 (nơi mũ bu lông tỳ vào)
        z_back2 = dz2  # Mặt sau Flange 2 (nơi đai ốc tỳ vào)

        # 6. Tra cứu kích thước vòng đệm JIS B 1256 nếu bật HAS_WASHERS hoặc Bộ đệm cách điện
        w_spec = get_washer_dimension(bolt_sz, TEST_WASHER_SERIES) if (TEST_HAS_WASHERS or is_dielectric) else None
        hw = float(w_spec.h_nominal) if w_spec else 3.0

        # Nếu là Bộ cách điện Dielectric Kit: Mỗi bên dùng đệm đôi (1 đệm cách điện G10 + 1 đệm thép JIS B 1256)
        extra_w = (hw * 2.0) if is_dielectric else (hw if TEST_HAS_WASHERS else 0.0)
        actual_bolt_len = (bolt_len + 15.0) if is_dielectric else bolt_len

        # Tọa độ mặt đáy cắm bu lông và đáy đai ốc
        z_bolt_base = z_back1 - extra_w
        z_nut_base = z_back2 + extra_w

        # 7. Khởi tạo cụm chi tiết chính từ Flange 1
        main_assembly = flange1
        main_assembly.uniteWith(gasket)
        main_assembly.uniteWith(flange2)

        # Chiều dài đoạn kẹp từ mặt mũ bu lông đến mặt đáy đai ốc (qua đệm 1, bích 1, gioăng, bích 2, đệm 2)
        clamped_len = z_nut_base - z_bolt_base

        # 8. Cắm toàn bộ dàn bu lông, vòng đệm, đai ốc quanh đường tròn chia bu lông (PCD = dim.c)
        r_bolt = dim.c / 2.0
        n_holes = dim.no
        angle_step = 360.0 / n_holes

        for i in range(n_holes):
            rad = math.radians(i * angle_step)
            bx = r_bolt * math.cos(rad)
            by = r_bolt * math.sin(rad)

            # Bu lông tích hợp đai ốc và ren nhô (chuỗi: bolt head -> shank kẹp -> nut -> thread tip)
            # Khởi tạo theo phân đoạn Z chuẩn ACIS giúp đai ốc hiển thị sắc nét 100%, không bị lỗi nuốt khối
            bolt_item = HexBolt(
                s,
                bolt_size=bolt_sz,
                length=actual_bolt_len,
                with_nut=True,
                grip_length=clamped_len
            )
            bolt_item.translate((bx, by, z_bolt_base))

            if is_dielectric:
                # BỘ CÁCH ĐIỆN FLANGE INSULATION KIT (FIK - CÁCH 1):
                # 1. Ống lót cách điện Mylar/G10 quanh thân bu lông lót kín trong lỗ bích
                sleeve_len = 2.0 * dim.t + tg
                sleeve_od = dim.h
                sleeve_id = float(bolt_item.spec.d) if hasattr(bolt_item.spec, "d") else (sleeve_od - 2.0)
                sleeve = prim.CYLINDER(s, R=sleeve_od / 2.0, H=sleeve_len, O=sleeve_id / 2.0)
                sleeve.translate((bx, by, -sleeve_len / 2.0))
                bolt_item.uniteWith(sleeve)
                sleeve.erase()

                # 2. Phía Flange 1: 1 Đệm cách điện G10 + 1 Đệm thép bảo vệ (dưới mũ bu lông)
                w_ins1 = PlainWasher(s, bolt_size=bolt_sz, series=TEST_WASHER_SERIES, has_hole=True)
                w_ins1.translate((bx, by, z_back1 - hw))
                bolt_item.uniteWith(w_ins1)

                w_steel1 = PlainWasher(s, bolt_size=bolt_sz, series=TEST_WASHER_SERIES, has_hole=True)
                w_steel1.translate((bx, by, z_back1 - 2.0 * hw))
                bolt_item.uniteWith(w_steel1)

                # 3. Phía Flange 2: 1 Đệm cách điện G10 + 1 Đệm thép bảo vệ (dưới đai ốc)
                w_ins2 = PlainWasher(s, bolt_size=bolt_sz, series=TEST_WASHER_SERIES, has_hole=True)
                w_ins2.translate((bx, by, z_back2))
                bolt_item.uniteWith(w_ins2)

                w_steel2 = PlainWasher(s, bolt_size=bolt_sz, series=TEST_WASHER_SERIES, has_hole=True)
                w_steel2.translate((bx, by, z_back2 + hw))
                bolt_item.uniteWith(w_steel2)

            elif TEST_HAS_WASHERS:
                # Vòng đệm 1: Tỳ vào mặt sau Flange 1 (dưới mũ bu lông)
                w1 = PlainWasher(s, bolt_size=bolt_sz, series=TEST_WASHER_SERIES, has_hole=True)
                w1.translate((bx, by, z_back1 - hw))
                bolt_item.uniteWith(w1)

                # Vòng đệm 2: Tỳ vào mặt sau Flange 2 (dưới đai ốc)
                w2 = PlainWasher(s, bolt_size=bolt_sz, series=TEST_WASHER_SERIES, has_hole=True)
                w2.translate((bx, by, z_back2))
                bolt_item.uniteWith(w2)

            # Gộp trọn bộ liên kết bu lông + đệm + đai ốc vào cụm chính
            main_assembly.uniteWith(bolt_item)

        # 9. Thiết lập Ports kết nối đường ống tiêu chuẩn cho AutoCAD Plant 3D
        # Port 1: Tại mặt sau bích 1 (hướng ra ngoài -Z)
        s.setPoint((0, 0, z_back1), (0, 0, -1))
        # Port 2: Tại mặt sau bích 2 (hướng ra ngoài +Z)
        s.setPoint((0, 0, z_back2), (0, 0, 1))

        return main_assembly.unwrap()

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 2: 1 MẶT BÍCH KÈM CỤM BU LÔNG QUANH VÒNG CHIA (FLANGE_WITH_BOLTS)
    # --------------------------------------------------------------------------
    elif TEST_MODE == "FLANGE_WITH_BOLTS":
        flange = JisFlange(
            s=s,
            rating=TEST_RATING,
            dn=TEST_DN,
            flange_type=TEST_FLANGE_TYPE,
            has_holes=True,
            has_rf=True,
            has_hub=False,
            has_bore=True,
            has_bolts=True,
            bolt_type="HEX"
        )
        dim = flange.dim
        s.setPoint((0, 0, dim.t), (0, 0, 1))
        s.setPoint((0, 0, 0), (0, 0, -1))
        return flange.unwrap()

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 3: BU LÔNG LỤC GIÁC JIS B 1180 ĐỨNG ĐỘC LẬP (STANDALONE_BOLT)
    # --------------------------------------------------------------------------
    elif TEST_MODE == "STANDALONE_BOLT":
        bolt = HexBolt(
            s=s,
            bolt_size="M16",
            length=65.0,
            type_code="TYPE_2_NOMINAL_COARSE_GRADE_AB",
        )
        spec = bolt.spec
        k_val = spec.head.k_nominal if hasattr(spec, "head") else 10.0
        l_val = 65.0
        s.setPoint((0, 0, -k_val), (0, 0, -1))
        s.setPoint((0, 0, l_val), (0, 0, 1))
        return bolt.unwrap()

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 4: CỤM BU LÔNG LỤC GIÁC KÈM ĐAI ỐC (BOLT_AND_NUT)
    # --------------------------------------------------------------------------
    elif TEST_MODE == "BOLT_AND_NUT":
        bolt_sz = "M16"
        l_val = 65.0
        bolt = HexBolt(s=s, bolt_size=bolt_sz, length=l_val, with_nut=True)
        k_val = bolt.spec.head.k_nominal if hasattr(bolt.spec, "head") else 10.0
        s.setPoint((0, 0, -k_val), (0, 0, -1))
        s.setPoint((0, 0, l_val), (0, 0, 1))
        return bolt.unwrap()

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 5: CỤM BU LÔNG + VÒNG ĐỆM JIS B 1256 + ĐAI ỐC JIS B 1181
    # --------------------------------------------------------------------------
    elif TEST_MODE == "BOLT_NUT_WASHER":
        bolt_sz = "M16"
        l_val = 65.0
        hw = 3.0
        grip = l_val - 14.8 - 5.0
        bolt = HexBolt(s=s, bolt_size=bolt_sz, length=l_val, with_nut=True, grip_length=grip)
        washer = PlainWasher(s=s, bolt_size=bolt_sz, series="ISO_NORMAL_A", has_hole=True)
        washer.translate((0, 0, grip - hw))
        bolt.uniteWith(washer)

        k_val = bolt.spec.head.k_nominal if hasattr(bolt.spec, "head") else 10.0
        s.setPoint((0, 0, -k_val), (0, 0, -1))
        s.setPoint((0, 0, l_val), (0, 0, 1))
        return bolt.unwrap()

