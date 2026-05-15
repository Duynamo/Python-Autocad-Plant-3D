import os
import primitives as _primitives  # type: ignore

from varmain.primitiv import *  # type: ignore
from varmain.var_basic import *  # type: ignore
from varmain.custom import *  # type: ignore

_IMPL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"hotreload_impl.py") #type: ignore
print("hotreload.py: imported") #type: ignore

#Check Valve

@activate(Group="Valve", TooltipShort="Hot-Reload Valve", TooltipLong="Hot-Reload for complex valve script", LengthUnit="mm", Ports="2") #type: ignore
@group("MainDimensions") #type: ignore
@group("MainDimensions") #type: ignore
@param(L=LENGTH, TooltipShort="Length (Face to Face)") #type: ignore
@param(D=LENGTH, TooltipShort="Flange Diameter") #type: ignore
@param(T=LENGTH, TooltipShort="Flange Thickness") #type: ignore
@param(H=LENGTH, TooltipShort="Total Height") #type: ignore
@param(H1=LENGTH, TooltipShort="Total Height without top flange") #type: ignore
@param(D1=LENGTH, TooltipShort="Handle Diameter") #type: ignore
@param(No=INT, TooltipShort="Number of holes") #type: ignore
@param(Dh=LENGTH, TooltipShort="Bolt hole Diameter") #type: ignore
@param(PCD=LENGTH, TooltipShort="PCDA") #type: ignore
@param(F=LENGTH, TooltipShort="Groove on Flange Diameter Thickness") #type: ignore
@param(G=LENGTH, TooltipShort="Groove on Flange Diameter") #type: ignore
def hotreload(s, L=500.0, D=342.0, T=27.0, H=260.0, D1=340.0, No=8, Dh=19.0,H1 = 210.0, PCD=299.0, F=3.0, G=256.0, **kw): #type: ignore
    try:
        with open(_IMPL_PATH, encoding="utf-8") as f:
            source = f.read()
        ns = dict(globals())
        ns["primitives"] = _primitives
        exec(compile(source, _IMPL_PATH, "exec"), ns)
        # Truyền tất cả các tham số đã định nghĩa vào hàm run
        return ns["run"](s, L=L, D=D, T=T, H=H, H1=H1, D1=D1, No=No, Dh=Dh, PCD=PCD,F=F,G=G, **kw)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Trả về một khối hộp báo lỗi nếu có vấn đề
        return BOX(s, L=100, W=100, H=200) #type: ignore
#L: kích thước OY
#H: kích thước OX
#W: kích thước OZ