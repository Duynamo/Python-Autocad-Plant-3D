from varmain.primitiv import *
from varmain.custom import *

@activate(Group="CustomScriptTutorial", TooltipShort="Support", TooltipLong="Support CustomScriptTutorial", LengthUnit="mm", Ports="1")
@group("MainDimensions")
@param(A=LENGTH, TooltipShort="A", TooltipLong="A")

def CustomScriptTutorial_1(s, A=100., **kw):

    main = BOX(s, L = A, W = 100, H = 100).translate((0, 0, 100 / 2))

    sub = BOX(s, L = 50, W = 150, H = 50).translate((0, 0, -150 / 2))

    main.uniteWith(sub)
    sub.erase()

    return main
