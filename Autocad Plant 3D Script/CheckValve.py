#region ___import Python Package
from aqa.math import *  #type: ignore
from varmain.primitiv import *  #type: ignore
from varmain.custom import *  #type: ignore
#endregion

#region __metaData
@activate (Group="Valve",
          TooltipShort="Check Valve",
          TooltipLong="Swing Check Valve with Side Cover",
          FirstPortEndtypes="FL",
          LengthUnit="mm",
          Ports="2")
@group ("MainDimensions") #type: ignore
@param (L=LENGTH, TooltipShort="Length (Face to Face)") #type: ignore
@param (D=LENGTH, TooltipShort="Flange Diameter") #type: ignore
@param (T=LENGTH, TooltipShort="Flange Thickness") #type: ignore
@param (D1=LENGTH, TooltipShort="Body Diameter (Middle)") #type: ignore
@param (D2=LENGTH, TooltipShort="Neck Diameter") #type: ignore
@param (B=LENGTH, TooltipShort="Side Cover Distance") #type: ignore
#endregion

def CheckValve(s, L=250.0, D=200.0, T=22.0, D1=220.0, D2=150.0, B=120.0, **kw):
    # 1. Left Flange
    f1 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((-L/2, 0, 0))
    
    # 2. Right Flange
    f2 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((L/2-T, 0, 0))
    
    # 3. Necks (Cylinders connecting flanges to body)
    neck_len = (L/2 - T) - (D1/4) # Approximate neck length
    neck1 = CYLINDER(s, R=D2/2, H=neck_len).rotateY(90).translate((-L/2+T, 0, 0))
    neck2 = CYLINDER(s, R=D2/2, H=neck_len).rotateY(90).translate((L/2-T-neck_len, 0, 0))
    f1.uniteWith(neck1)
    f1.uniteWith(neck2)
    f1.uniteWith(f2)
    
    # 4. Center Body (The bulbous part)
    # Using a Sphere for the central part. In Plant 3D, SPHERE(s, R)
    center_body = SPHERE(s, R=D1/2) 
    f1.uniteWith(center_body)
    
    # 5. Side Cover Extension (The part on the side)
    cover_d = D2 * 0.7
    cover_h = B - (D1/2) # Distance from center
    # Position it horizontally towards the side (Y axis) or Z axis. 
    # Let's use Y for "side" view in CAD.
    side_neck = CYLINDER(s, R=cover_d/2, H=cover_h).rotateX(-90).translate((0, D1/2, 0))
    f1.uniteWith(side_neck)
    
    # 6. Side Cover Plate (The disc at the end of the side extension)
    plate_d = cover_d * 1.2
    plate_t = 15.0
    side_plate = CYLINDER(s, R=plate_d/2, H=plate_t).rotateX(-90).translate((0, B, 0))
    f1.uniteWith(side_plate)
    
    # 7. Side Hex Nut (The small bolt on the side)
    hex_s = 25.0
    # On the same cover face
    side_hex = CYLINDER(s, R=hex_s/2, H=15.0).rotateX(-90).translate((0, B+plate_t, 0))
    f1.uniteWith(side_hex)
    
    # 8. Hinge Pin Protrusion (The small bit on the body)
    hinge_s = 30.0
    hinge = CYLINDER(s, R=hinge_s/2, H=10.0).rotateX(-90).translate((20, D1/2-5, 0))
    f1.uniteWith(hinge)

    # Ports
    s.setPoint((-L/2, 0, 0), (-1, 0, 0)) # Port 1
    s.setPoint((L/2, 0, 0), (1, 0, 0))   # Port 2
    
    return f1

check_valve = CheckValve
OUT = check_valve
