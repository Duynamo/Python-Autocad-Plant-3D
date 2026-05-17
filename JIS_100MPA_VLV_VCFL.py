#region ___import Python Package
from aqa.math import *  #type: ignore
from varmain.primitiv import *  #type: ignore
from varmain.custom import *  #type: ignore
#endregion

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

# (testacpscript "JIS_100MPA_VLV_VCFL")

def JIS_100MPA_VLV_VCFL(s, L=500.0, D=330.0, T=26.0, H=260.0, D1=340.0, No=12, Dh=23.0, H1 = 210.0, PCD=290.0, **kw): #type: ignore

    # 1. Left Flange
    f1 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((-L/2, 0, 0)) #type: ignore
    
    # 2. Right Flange
    f2 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((L/2 - T, 0, 0)) #type: ignore
    f1.uniteWith(f2)
    f2.erase()

    # 3. Body 1 (Horizontal cylinders connecting left and right flanges)
    body1_D = D * 0.6
    body1_L = (L - 2*T ) 
    body1 = CYLINDER(s, R=body1_D/2, H=body1_L).rotateY(90).translate((-body1_L/2, 0, 0)) #type: ignore

    f1.uniteWith(body1)
    body1.erase()

    # 5. Body main
    RX = 0.53 * (L - 2*T )
    RY = 0.9 * body1_D 
    A1 = 360
    A2 = 0
    A3 = 0
    A4 = 180
    body_main = ELLIPSOIDSEGMENT(s, RX=RX, RY=RY, A1=A1, A2=A2, A3=A3, A4=A4) #type: ignore
    f1.uniteWith(body_main)
    body_main.erase()

    # 6. Horizontal Nozzel 
    nozzel_D = 0.8 * D
    nozzel_L =  H-40
    nozzel = CYLINDER(s, R=nozzel_D/2, H=nozzel_L).translate((0, 0, 0)) #type: ignore
    f1.uniteWith(nozzel)
    nozzel.erase()

    # 7. Body Flange
    bodyFlange_L = 20
    bodyFlange_D = 0.98 * D1
    bodyFlange = CYLINDER(s, R=bodyFlange_D/2, H=bodyFlange_L).translate((0, 0, H-40)) #type: ignore
    f1.uniteWith(bodyFlange)
    bodyFlange.erase()

    # 8. Top Flange
    topFlange_L = 20
    topFlange_D = D1
    topFlange = CYLINDER(s, R=topFlange_D/2, H=topFlange_L).translate((0, 0, H-20)) #type: ignore
    f1.uniteWith(topFlange)
    topFlange.erase()

    # 9. Hinger pin
    hinger_D = 55
    hinger_L = 1.4 * body1_D / 2  
    hinger = CYLINDER(s, R=hinger_D/2, H=hinger_L).rotateX(90).translate((-0.6*0.5*nozzel_D, 0, 0.7*H)) #type: ignore
    f1.uniteWith(hinger)
    hinger.erase()

    # 10. Hinger pin bolt
    hex_L = 40
    hex_W = 40
    hex_H = 23.1
    x_pos = -0.6*0.5*nozzel_D
    z_pos = 0.7*H
    
    hex1 = BOX(s, L=hex_L, W=hex_W, H=hex_H).rotateX(90).translate((x_pos, -hinger_L, z_pos))#type: ignore
    hex2 = BOX(s, L=hex_L, W=hex_W, H=hex_H).rotateZ(60).rotateX(90).translate((x_pos, -hinger_L, z_pos))#type: ignore
    hex3 = BOX(s, L=hex_L, W=hex_W, H=hex_H).rotateZ(120).rotateX(90).translate((x_pos, -hinger_L, z_pos))#type: ignore

    hex1.uniteWith(hex2)
    hex2.erase()
   
    hex1.uniteWith(hex3)
    hex3.erase()

    f1.uniteWith(hex1)
    hex1.erase()
    
    # Ports
    s.setPoint((-L/2, 0, 0), (-1, 0, 0)) # Port 1
    s.setPoint((L/2, 0, 0), (1, 0, 0))   # Port 2
    
    return f1

OUT = JIS_100MPA_VLV_VCFL