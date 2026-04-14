from varmain.primitiv import *
from varmain.custom import *

@activate(Group="CustomScriptTutorial", TooltipShort="Support", TooltipLong="Support CustomScriptTutorial", LengthUnit="mm", Ports="1")
@group("MainDimensions")
@param(A=LENGTH, TooltipShort="A", TooltipLong="A")

def CustomScriptTutorial_2(s, A=100., **kw):

    main = BOX(s, L = A, W = 100, H = 100).translate((0, 0, 100 / 2))

    sub = BOX(s, L = 50, W = 150, H = 50).translate((0, 0, -150 / 2))

    main.uniteWith(sub)
    sub.erase()

    sub = BOX(s, L = 300, W = 150, H = 300).translate((0, 0, 150 / 2)).rotateX(45)

    main.subtractFrom(sub)
    sub.erase()

    return main
