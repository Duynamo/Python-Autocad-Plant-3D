#region ___import Python Package
from aqa.math import *  #type: ignore
from varmain.primitiv import *  #type: ignore
from varmain.custom import *  #type: ignore
#endregion

#region __metaData
@activate (Group="Valve",
          TooltipShort="Diaphragm Valve",
          TooltipLong="Diaphragm Valve with Bonnet Cover",
          FirstPortEndtypes="FL",
          LengthUnit="mm",
          Ports="2")
@group ("MainDimensions") #type: ignore
@param (L=LENGTH, TooltipShort="Length (Face to Face)") #type: ignore
@param (D=LENGTH, TooltipShort="Flange Diameter") #type: ignore
@param (T=LENGTH, TooltipShort="Flange Thickness") #type: ignore
@param (B=LENGTH, TooltipShort="Body Box Size") #type: ignore
@param (H=LENGTH, TooltipShort="Total Height") #type: ignore
@param (W=LENGTH, TooltipShort="Diaphragm Cover Diameter") #type: ignore
#endregion

def DiaphragmValve(s, L=250.0, D=200.0, T=22.0, B=120.0, H=280.0, W=220.0, **kw):
    # 1. Left Flange
    f1 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((-L/2, 0, 0))
    
    # 2. Right Flange
    f2 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((L/2-T, 0, 0))
    
    # 3. Nozzles (Horizontal cylinders connecting flanges to body)
    noz_d = D * 0.5
    noz_len = (L/2 - T) - (B/2)
    noz1 = CYLINDER(s, R=noz_d/2, H=noz_len).rotateY(90).translate((-L/2+T, 0, 0))
    noz2 = CYLINDER(s, R=noz_d/2, H=noz_len).rotateY(90).translate((B/2, 0, 0))
    f1.uniteWith(noz1)
    f1.uniteWith(noz2)
    f1.uniteWith(f2)
    
    # 4. Central Body (Main BOX)
    # Using a Box for the central junction
    body_box = BOX(s, L=B, W=B, H=B).translate((0, 0, -B/2))
    f1.uniteWith(body_box)
    
    # 5. Bonnet Transition (Truncated Cone)
    cone_h = H * 0.3
    # CONE(s, R1=Bottom, R2=Top, H=Height)
    bonnet_cone = CONE(s, R1=B/2 * 0.8, R2=W/4, H=cone_h).translate((0, 0, B/2))
    f1.uniteWith(bonnet_cone)
    
    # 6. Diaphragm Cover (Large Cylinder on top)
    cover_t = 30.0
    cover = CYLINDER(s, R=W/2, H=cover_t).translate((0, 0, B/2 + cone_h))
    f1.uniteWith(cover)
    
    # 7. Top Adjustment Part (Small Cone)
    top_h = 40.0
    top_cone = CONE(s, R1=W/6, R2=W/10, H=top_h).translate((0, 0, B/2 + cone_h + cover_t))
    f1.uniteWith(top_cone)

    # Ports
    s.setPoint((-L/2, 0, 0), (-1, 0, 0)) # Port 1
    s.setPoint((L/2, 0, 0), (1, 0, 0))   # Port 2
    
    return f1

diaphragm_valve = DiaphragmValve
OUT = diaphragm_valve
