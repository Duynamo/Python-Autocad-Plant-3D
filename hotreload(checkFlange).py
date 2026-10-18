import sys
import os

# Đảm bảo AutoCAD nhận diện được package _fvc_flanges
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Tự động reload package _fvc_flanges để luôn cập nhật logic hình học mới nhất
for mod_name in list(sys.modules.keys()):
    if mod_name.startswith('_fvc_flanges'):
        del sys.modules[mod_name]

from _fvc_flanges import JisFlange

def run(s, **kw):
    """Hàm test dựng hình mặt bích JIS B 2220."""
    # 1. Khởi tạo mặt bích
    flange = JisFlange(
        s=s,
        rating="10K",       # '10K', '7K5', '5K', '20K'
        dn=200,             # Cỡ danh định DN (ví dụ: 50, 80, 100, 200...)
        flange_type="SOP",   # 'IT' (cho Van), 'SOP', 'WN', 'BL'
        has_holes=True,     # True: đục lỗ bu lông (LOD cao để kiểm tra)
        has_rf=True,        # True: có gờ nổi Raised Face (chiều cao f)
        has_hub=False,      # True: có cổ côn
        has_bore=True       # True: khoét rỗng lỗ tâm
    )

    dim = flange.dim

    # 2. Định nghĩa Ports (Bắt buộc cho AutoCAD Plant 3D nhận diện)
    # Port 1: Tại mặt tiếp xúc gioăng RF (Z = dim.t), vector hướng ra ngoài +Z
    s.setPoint((0, 0, dim.t), (0, 0, 1))
    # Port 2: Tại mặt sau bích (Z = 0), vector hướng ra ngoài -Z
    s.setPoint((0, 0, 0), (0, 0, -1))

    # 3. Trả về khối Solid gốc cho AutoCAD (gọi .unwrap())
    return flange.unwrap()