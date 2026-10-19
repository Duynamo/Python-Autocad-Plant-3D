import sys
import os
import math

# 1. Đảm bảo AutoCAD nhận diện được các package _fvc_flanges và _fvc_fasteners
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

workspace_dir = r"c:\Users\95053\Desktop\Hello World\Python-Autocad-Plant-3D"
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
)

# ==============================================================================
# CẤU HÌNH THÔNG SỐ TEST CỤM KẾT NỐI (TÙY CHỈNH DỄ DÀNG KHI KIỂM TRA)
# ==============================================================================
TEST_RATING = "10K"                  # Cấp áp suất: '5K', '10K', '16K', '20K', '30K', '40K', '63K'
TEST_DN = 200                        # Cỡ danh định DN (15, 20, 25, 50, 80, 100, 150, 200, 300...)
TEST_FLANGE_TYPE = "SOP"             # Loại bích: 'SOP', 'WN', 'IT', 'BL'
TEST_GASKET_THICKNESS = 3.0          # Chiều dày gioăng đệm làm kín tg (mm)
TEST_HAS_WASHERS = True              # True: có thêm vòng đệm JIS B 1256 dưới mũ và đai ốc
TEST_WASHER_SERIES = "ISO_NORMAL_A"  # Dòng đệm: 'ISO_NORMAL_A', 'ISO_NORMAL_CHAMFERED_A', 'ANNEX_JA_SQUARE'...

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
        tg = float(TEST_GASKET_THICKNESS)

        # 2. Khởi tạo Flange 1 và Flange 2 (JIS B 2220)
        flange1 = JisFlange(
            s=s,
            rating=TEST_RATING,
            dn=TEST_DN,
            flange_type=TEST_FLANGE_TYPE,
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
            has_holes=True,
            has_rf=True,
            has_hub=False,
            has_bore=True,
            has_bolts=False
        )
        dim = flange1.dim

        # 3. Tạo gioăng đệm làm kín Gasket (đặt tại tâm đối xứng Z = 0, trải từ -tg/2 đến +tg/2)
        gasket_od = dim.g if (dim.g > 0) else dim.d
        gasket_id = dim.d0 if (dim.d0 > 0) else dim.bore
        gasket = Gasket(s, od=gasket_od, id_=gasket_id, thickness=tg)

        # 4. Định vị Flange 1: Mặt RF tiếp xúc mặt dưới gioăng (-tg/2), mặt sau quay về -Z
        dz1 = -tg / 2.0 - dim.t
        flange1.translate((0, 0, dz1))

        # 5. Định vị Flange 2: Xoay 180 độ đối đầu, mặt RF tiếp xúc mặt trên gioăng (+tg/2), mặt sau quay về +Z
        flange2.rotateY(180)
        dz2 = tg / 2.0 + dim.t
        flange2.translate((0, 0, dz2))

        # Tọa độ mặt sau của 2 mặt bích
        z_back1 = dz1  # Mặt sau Flange 1 (nơi mũ bu lông tỳ vào)
        z_back2 = dz2  # Mặt sau Flange 2 (nơi đai ốc tỳ vào)

        # 6. Tra cứu kích thước vòng đệm JIS B 1256 nếu bật HAS_WASHERS
        w_spec = get_washer_dimension(bolt_sz, TEST_WASHER_SERIES) if TEST_HAS_WASHERS else None
        hw = float(w_spec.h_nominal) if w_spec else 3.0

        # Tọa độ mặt đáy cắm bu lông và đáy đai ốc
        z_bolt_base = (z_back1 - hw) if TEST_HAS_WASHERS else z_back1
        z_nut_base = (z_back2 + hw) if TEST_HAS_WASHERS else z_back2

        # 7. Khởi tạo cụm chi tiết chính từ Flange 1
        main_assembly = flange1
        main_assembly.uniteWith(gasket)
        main_assembly.uniteWith(flange2)

        # 8. Cắm toàn bộ dàn bu lông, vòng đệm, đai ốc quanh đường tròn chia bu lông (PCD = dim.c)
        r_bolt = dim.c / 2.0
        n_holes = dim.no
        angle_step = 360.0 / n_holes

        for i in range(n_holes):
            rad = math.radians(i * angle_step)
            bx = r_bolt * math.cos(rad)
            by = r_bolt * math.sin(rad)

            # Bu lông xuyên suốt: mũ tại mặt sau Flange 1, ren kéo dài qua Flange 2
            bolt_item = HexBolt(s, bolt_size=bolt_sz, length=bolt_len)
            bolt_item.translate((bx, by, z_bolt_base))
            main_assembly.uniteWith(bolt_item)

            if TEST_HAS_WASHERS:
                # Vòng đệm 1: Tỳ vào mặt sau Flange 1 (dưới mũ bu lông)
                w1 = PlainWasher(s, bolt_size=bolt_sz, series=TEST_WASHER_SERIES, has_hole=True)
                w1.translate((bx, by, z_back1 - hw))
                main_assembly.uniteWith(w1)

                # Vòng đệm 2: Tỳ vào mặt sau Flange 2 (dưới đai ốc)
                w2 = PlainWasher(s, bolt_size=bolt_sz, series=TEST_WASHER_SERIES, has_hole=True)
                w2.translate((bx, by, z_back2))
                main_assembly.uniteWith(w2)

            # Đai ốc: Vặn chặt tỳ vào mặt sau Flange 2 (hoặc tỳ lên vòng đệm 2)
            nut_item = HexNut(s, bolt_size=bolt_sz, has_hole=True)
            nut_item.translate((bx, by, z_nut_base))
            main_assembly.uniteWith(nut_item)

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
        bolt = HexBolt(s=s, bolt_size=bolt_sz, length=l_val)
        nut = HexNut(s=s, bolt_size=bolt_sz, has_hole=True)
        nut_z = l_val - float(nut.spec.m) - 5.0
        nut.translate((0, 0, nut_z))
        bolt.uniteWith(nut)

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
        bolt = HexBolt(s=s, bolt_size=bolt_sz, length=l_val)
        washer = PlainWasher(s=s, bolt_size=bolt_sz, series="ISO_NORMAL_A", has_hole=True)
        h_washer = float(washer.spec.h_nominal)
        nut = HexNut(s=s, bolt_size=bolt_sz, has_hole=True)
        m_nut = float(nut.spec.m)

        nut_z = l_val - m_nut - 5.0
        washer_z = nut_z - h_washer

        washer.translate((0, 0, washer_z))
        nut.translate((0, 0, nut_z))

        bolt.uniteWith(washer)
        bolt.uniteWith(nut)

        k_val = bolt.spec.head.k_nominal if hasattr(bolt.spec, "head") else 10.0
        s.setPoint((0, 0, -k_val), (0, 0, -1))
        s.setPoint((0, 0, l_val), (0, 0, 1))
        return bolt.unwrap()
