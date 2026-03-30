#region ___import Python Package
from aqa.math import *  #type: ignore
from varmain.primitiv import *  #type: ignore
from varmain.custom import *  #type: ignore
#endregion

#region __metaData
@activate (Group="Valve",
          TooltipShort="Gate Valve JIS10K",
          TooltipLong="Gate Valve with Handwheel",
          FirstPortEndtypes="FL",
          LengthUnit="mm",
          Ports="2")
@group ("MainDimensions") #type: ignore
@param (L=LENGTH, TooltipShort="Overall Length (Face to Face)") #type: ignore
@param (D=LENGTH, TooltipShort="Flange Outer Diameter") #type: ignore
@param (T=LENGTH, TooltipShort="Flange Thickness") #type: ignore
@param (D1=LENGTH, TooltipShort="Body Outer Diameter") #type: ignore
@param (H=LENGTH, TooltipShort="Height to Center of Handwheel") #type: ignore
@param (W=LENGTH, TooltipShort="Handwheel Diameter") #type: ignore
@param (B=LENGTH, TooltipShort="Body Width (Gate Housing)") #type: ignore
@param (h1=LENGTH, TooltipShort="Height of Lower Extension") #type: ignore
#endregion

def GateValve(s, L=250.0, D=150.0, T=20.0, D1=100.0, H=350.0, W=200.0, B=80.0, h1=40.0, **kw):
    # 1. Left Flange
    f1 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((-L/2, 0, 0))
    
    # 2. Right Flange
    f2 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((L/2-T, 0, 0))
    
    # 3. Main Center Body (The vertical cylinder highlighted in Cyan)
    h_center = D1 * 1.1
    center_body = CYLINDER(s, R=D1/2, H=h_center).translate((0, 0, -h_center/2))
    f1.uniteWith(center_body)
    f1.uniteWith(f2)
    
    # 3a. Horizontal Nozzles (Left and Right pipe segments)
    noz_d = D1 * 0.85
    noz_len = (L/2 - T - D1/2)
    noz1 = CYLINDER(s, R=noz_d/2, H=noz_len).rotateY(90).translate((-L/2+T, 0, 0))
    noz2 = CYLINDER(s, R=noz_d/2, H=noz_len).rotateY(90).translate((D1/2, 0, 0))
    f1.uniteWith(noz1)
    f1.uniteWith(noz2)
    
    # 5. Bonnet (Cylindrical part above body)
    bonnet_h = H * 0.25
    bonnet = CYLINDER(s, R=D1/2, H=bonnet_h).translate((0, 0, h_center/2))
    f1.uniteWith(bonnet)


    
    # 6. Body Flange (Middle disc)
    mf_t = 15.0
    mf_d = B * 1.3
    m_flange = CYLINDER(s, R=mf_d/2, H=mf_t).translate((0, 0, bonnet_h))
    f1.uniteWith(m_flange)
    
    # 7. Cage/Yoke Legs (The two legs above the body flange)
    cage_h = H * 0.4
    leg_w = B * 0.15
    leg1 = BOX(s, L=leg_w, W=leg_w, H=cage_h).translate((B/3, 0, bonnet_h + mf_t + cage_h/2))
    leg2 = BOX(s, L=leg_w, W=leg_w, H=cage_h).translate((-B/3, 0, bonnet_h + mf_t + cage_h/2))
    f1.uniteWith(leg1)
    f1.uniteWith(leg2)
    
    # 8. Yoke Cap (on top of legs)
    cap_h = 20.0
    cap = BOX(s, L=B*0.8, W=leg_w*2, H=cap_h).translate((0, 0, bonnet_h + mf_t + cage_h + cap_h/2))
    f1.uniteWith(cap)
    
    # 9. Stem (Thin rod in center)
    stem_d = B * 0.1
    stem = CYLINDER(s, R=stem_d/2, H=H - bonnet_h).translate((0, 0, bonnet_h))
    f1.uniteWith(stem)
    
    # 10. Handwheel Rim
    rim_t = 12.0
    rim = CYLINDER(s, R=W/2, H=rim_t).translate((0, 0, H))
    # Or use TORUS for better look:
    # rim = TORUS(s, R1=(W-rim_t)/2, R2=rim_t/2).translate((0,0, H+rim_t/2))
    f1.uniteWith(rim)
    
    # 11. Handwheel Spokes (5 spokes)
    spoke_w = rim_t * 0.8
    for i in range(5):
        angle = 72 * i
        spoke = BOX(s, L=W/2, W=spoke_w, H=spoke_w).translate((W/4, 0, H + rim_t/2)).rotateZ(angle)
        f1.uniteWith(spoke)
        
    # 12. Top Hex Nut
    nut_s = rim_t * 1.5
    nut = CYLINDER(s, R=nut_s/2, H=rim_t).translate((0, 0, H + rim_t/2)) # Hex would be better but cylinder is safe
    f1.uniteWith(nut)

    # Connection Points
    s.setPoint((-L/2, 0, 0), (-1, 0, 0)) # CP1
    s.setPoint((L/2, 0, 0), (1, 0, 0))   # CP2
    
    return f1

# Standard assignment for Plant 3D
valve = GateValve
OUT = valve
