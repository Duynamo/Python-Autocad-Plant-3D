import os
import primitives as _primitives  # type: ignore

from varmain.primitiv import *  # type: ignore
from varmain.var_basic import *  # type: ignore
from varmain.custom import *  # type: ignore

_IMPL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "hotreload_impl.py"
)

print("hotreload.py: imported")


@activate(Group="Valve", TooltipShort="Hot-Reload Valve", TooltipLong="Hot-Reload for complex valve script", LengthUnit="mm", Ports="2")
@group("MainDimensions")
@param(L=LENGTH, TooltipShort="Length (Face to Face)")
@param(D=LENGTH, TooltipShort="Flange Diameter")
@param(T=LENGTH, TooltipShort="Flange Thickness")
@param(H=LENGTH, TooltipShort="Total Height")
def hotreload(s, L=250.0, D=200.0, T=22.0, H=130.0, **kw):
    try:
        with open(_IMPL_PATH, encoding="utf-8") as f:
            source = f.read()
        ns = dict(globals())
        ns["primitives"] = _primitives
        exec(compile(source, _IMPL_PATH, "exec"), ns)
        # Truyền tất cả các tham số đã định nghĩa vào hàm run
        return ns["run"](s, L=L, D=D, T=T, H=H, **kw)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Trả về một khối hộp báo lỗi nếu có vấn đề
        return BOX(s, L=100, W=100, H=100)
