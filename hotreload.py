import os
import primitives as _primitives  # type: ignore

from varmain.primitiv import *  # type: ignore
from varmain.var_basic import *  # type: ignore
from varmain.custom import *  # type: ignore

# ==============================================================================
# AUTOCAD PLANT 3D ACP ADAPTER PROXY (STATIC WRAPPER)
# ==============================================================================
# Lưu ý: File này đóng vai trò là "vỏ bọc giao tiếp cố định" với engine AutoCAD.
# Các decorator @activate, @group, @param bên dưới giữ nguyên để khớp hoàn toàn
# với HOTRELOAD.xml trong catalog Plant 3D.
# BẠN KHÔNG CẦN CHỈNH SỬA FILE NÀY!
# Toàn bộ logic dựng hình 3D vui lòng viết tại: hotreload_impl.py
# ==============================================================================

_WORKSPACE_IMPL = r"c:\Users\Laptop\OneDrive\Desktop\Hello World\Python-Autocad-Plant-3D\hotreload_impl.py"
if os.path.exists(_WORKSPACE_IMPL):
    _IMPL_PATH = _WORKSPACE_IMPL
else:
    _IMPL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hotreload_impl.py")

@activate(Group="Testing", TooltipShort="Hot Reload Tester", TooltipLong="Dynamic Hot-Reload Proxy", FirstPortEndtypes="FL", LengthUnit="mm", Ports="2") # type: ignore
@group("MainDimensions") # type: ignore
@param(D=LENGTH, TooltipShort="Nominal Size") # type: ignore
def hotreload(s, D=100.0, **kw):
    try:
        with open(_IMPL_PATH, encoding="utf-8") as f:
            source = f.read()
        ns = dict(globals())
        ns["primitives"] = _primitives
        exec(compile(source, _IMPL_PATH, "exec"), ns)
        return ns["run"](s, D=D, **kw)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return BOX(s, L=100, W=100, H=200) # type: ignore