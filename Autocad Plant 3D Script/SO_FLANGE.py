#region ___import Python Package
from aqa.math import *  #type: ignore
from varmain.primitiv import *  #type: ignore
from varmain.custom import *  #type: ignore
#endregion

#region __metaData
@activate (Group="Flange",
          TooltipShort="SO_Flange",
          TooltipLong="Slip On Flange",
          FirstPortEndtypes="FL",
          LengthUnit="mm",
          Ports="2")
@group ("MainDimensions") #type: ignore
@param (D=LENGTH, TooltipShort="Outer Diameter of the Flange") #type: ignore
@param (T=LENGTH, TooltipLong="Thickness of the Flange") #type: ignore
@group (Name="meaningless enum")  #type: ignore
@param (K=ENUM) #type: ignore
@enum  (1, "align X") #type: ignore
@enum  (2, "align Y") #type: ignore
@enum  (3, "align Z") #type: ignore
#endregion

def SO_Flange(s, D=210.0,  T=10,  K=1, ** kw):
    F = CYLINDER(s, R=D/2, H=T).rotateY(90) #type: ignore
    return None

flange = SO_Flange

OUT = flange