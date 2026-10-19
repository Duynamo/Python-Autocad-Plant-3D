import sys
import os

# 1. Đảm bảo AutoCAD nhận diện được thư mục làm việc và các package
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

workspace_dir = r"c:\Users\95053\Desktop\Hello World\Python-Autocad-Plant-3D"
if os.path.exists(workspace_dir) and workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

# 2. Tự động reload module hotreload_impl và các package để luôn cập nhật logic mới nhất khi lưu code
for mod_name in list(sys.modules.keys()):
    if (
        mod_name.startswith('hotreload_impl')
        or mod_name.startswith('_fvc_flanges')
        or mod_name.startswith('_fvc_fasteners')
    ):
        del sys.modules[mod_name]

import hotreload_impl


def run(s, **kw):
    """Hàm entry point của AutoCAD Plant 3D để render cụm kết nối bu lông - mặt bích.
    Ủy quyền thực thi trực tiếp sang hotreload_impl.py.
    """
    return hotreload_impl.run(s, **kw)
