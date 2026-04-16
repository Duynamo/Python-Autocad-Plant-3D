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


@activate(Group="Custom", TooltipShort="hotreload", TooltipLong="hotreload", LengthUnit="mm", Ports="1")
@group("MainDimensions")
@param(A=LENGTH, TooltipShort="A", TooltipLong="A")
def hotreload(s, A=100., **kw):
    try:
        with open(_IMPL_PATH, encoding="utf-8") as f:
            source = f.read()
        ns = dict(globals())
        ns["primitives"] = _primitives
        exec(compile(source, _IMPL_PATH, "exec"), ns)
        return ns["run"](s, A=A)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return BOX(s, L=A, W=A, H=A)
