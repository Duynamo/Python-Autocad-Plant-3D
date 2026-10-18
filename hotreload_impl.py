import sys
import os

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
from _fvc_fasteners import HexBolt, HexNut, StudBolt, get_hex_bolt

# ==============================================================================
# CẤU HÌNH CHẾ ĐỘ TEST (BẠN CHỌN 1 TRONG 3 CHẾ ĐỘ DƯỚI ĐÂY)
# ==============================================================================
# - "FLANGE_WITH_BOLTS": Mặt bích JIS B 2220 tự động cắm dàn bu lông JIS B 1217 quanh vòng chia
# - "STANDALONE_BOLT":   Một con bu lông lục giác JIS B 1180 đứng độc lập (zoom sát soi giác s, mũ k)
# - "BOLT_AND_NUT":      Một cụm Bu lông lục giác kèm Đai ốc vặn ở đuôi ren
TEST_MODE = "FLANGE_WITH_BOLTS"


def run(s, **kw):
    """Hàm entry point của AutoCAD Plant 3D để render hình học."""

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 1: MẶT BÍCH KÈM CỤM BU LÔNG QUANH VÒNG CHIA (FLANGE_WITH_BOLTS)
    # --------------------------------------------------------------------------
    if TEST_MODE == "FLANGE_WITH_BOLTS":
        flange = JisFlange(
            s=s,
            rating="10K",       # '10K', '7K5', '5K', '16K', '20K', '30K', '40K', '63K'
            dn=600,             # Cỡ danh định DN (50, 80, 100, 150, 200...)
            flange_type="SOP",  # 'IT' (cho Van), 'SOP', 'WN', 'BL'
            has_holes=True,     # True: đục lỗ bu lông
            has_rf=True,        # True: có gờ nổi Raised Face
            has_hub=False,      # True: có cổ côn
            has_bore=True,      # True: khoét rỗng lỗ tâm
            has_bolts=True,     # BẬT TRUE: Tự động tra JIS B 1217 & gắn bu lông quanh vòng chia
            bolt_type="HEX"     # 'HEX' (Bu lông lục giác JIS B 1180) hoặc 'STUD' (Gu-zông 2 đầu)
        )

        dim = flange.dim
        # Port 1: Tại mặt tiếp xúc gioăng RF (Z = dim.t), vector hướng ra ngoài +Z
        s.setPoint((0, 0, dim.t), (0, 0, 1))
        # Port 2: Tại mặt sau bích (Z = 0), vector hướng ra ngoài -Z
        s.setPoint((0, 0, 0), (0, 0, -1))

        return flange.unwrap()

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 2: BU LÔNG LỤC GIÁC JIS B 1180 ĐỨNG ĐỘC LẬP (STANDALONE_BOLT)
    # --------------------------------------------------------------------------
    elif TEST_MODE == "STANDALONE_BOLT":
        # Tạo bu lông M16 x 65 mm (Loại 2 - ISO 4014 Cấp A/B Coarse)
        bolt = HexBolt(
            s=s,
            bolt_size="M16",                          # Cỡ bu lông: 'M12', 'M16', 'M20', 'M24'...
            length=65.0,                              # Chiều dài bu lông l (mm)
            type_code="TYPE_2_NOMINAL_COARSE_GRADE_AB",# 1 trong 7 loại bu lông JIS B 1180
            # series_override="ANNEX_JA"              # Bỏ comment nếu muốn test giác cờ-lê Nhật cũ (M10 giác 17, M12 giác 19)
        )

        spec = bolt.spec
        k_val = spec.head.k_nominal if hasattr(spec, "head") else 10.0
        l_val = float(length if 'length' in locals() else 65.0) #type: ignore

        # Port 1: Tại đỉnh mũ bu lông (Z = -k), hướng ra ngoài -Z
        s.setPoint((0, 0, -k_val), (0, 0, -1))
        # Port 2: Tại mút cuối ren bu lông (Z = length), hướng ra ngoài +Z
        s.setPoint((0, 0, l_val), (0, 0, 1))

        return bolt.unwrap()

    # --------------------------------------------------------------------------
    # CHẾ ĐỘ 3: CỤM BU LÔNG LỤC GIÁC KÈM ĐAI ỐC (BOLT_AND_NUT)
    # --------------------------------------------------------------------------
    elif TEST_MODE == "BOLT_AND_NUT":
        bolt_sz = "M16"
        l_val = 65.0

        # 1. Dựng bu lông lục giác
        bolt = HexBolt(s=s, bolt_size=bolt_sz, length=l_val)
        
        # 2. Dựng đai ốc (Hex Nut JIS B 1181) và vặn vào đoạn cuối thân ren
        nut = HexNut(s=s, bolt_size=bolt_sz, has_hole=True)
        # Tọa độ đai ốc: đặt cách mút ren 5 mm để thấy rõ phần ren nhô an toàn
        nut_z = l_val - float(nut.spec.m) - 5.0
        nut.translate((0, 0, nut_z))
        
        # Gộp đai ốc vào bu lông
        bolt.uniteWith(nut)

        k_val = bolt.spec.head.k_nominal if hasattr(bolt.spec, "head") else 10.0
        s.setPoint((0, 0, -k_val), (0, 0, -1))
        s.setPoint((0, 0, l_val), (0, 0, 1))

        return bolt.unwrap()
