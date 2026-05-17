#region ___import Python Package
from aqa.math import *  #type: ignore
from varmain.primitiv import *  #type: ignore
from varmain.custom import *  #type: ignore
#endregion

#region __metaData
@activate (Group="Valve", TooltipShort="Gate Valve JIS7.5K",TooltipLong="Gate Valve with Handwheel",FirstPortEndtypes="FL",LengthUnit="mm",Ports="2") #type: ignore
@group("MainDimensions") #type: ignore
@param(L=LENGTH, TooltipShort="Length (Face to Face)") #type: ignore
@param(D=LENGTH, TooltipShort="Flange Diameter") #type: ignore
@param(T=LENGTH, TooltipShort="Flange Thickness") #type: ignore
@param(H=LENGTH, TooltipShort="Total Height") #type: ignore
@param(H1=LENGTH, TooltipShort="Total Height") #type: ignore
@param(D1=LENGTH, TooltipShort="Handle Diameter") #type: ignore
@param(No=INT, TooltipShort="Number of holes") #type: ignore
@param(Dh=LENGTH, TooltipShort="Bolt hole Diameter") #type: ignore
@param(PCD=LENGTH, TooltipShort="PCDA") #type: ignore

# (testacpscript "JIS_100MPA_VLV_VTFL")

def JIS_100MPA_VLV_VTFL(s, L=290.0, D=330.0, T=30.0, H=991.0, H1= 725, D1=355.0, No=12, Dh=23.0, PCD=290.0, **kw):
# Lưu ý khi move đối tượng. Mặc định khi được tạo, khố sẽ được tạo ra theo dạng đối xứng quanh gốc tọa độ (0, 0, 0). Khi move, đối tượng sẽ được dịch chuyển theo vector từ gốc đến điểm mới. Nếu muốn đối tượng nằm ở vị trí chính xác, cần tính toán vector dịch chuyển dựa trên kích thước và vị trí mong muốn của đối tượng.
    # 1. Left Flange
    f1 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((-L/2 , 0, 0)) #type: ignore

    # 2. Right Flange
    f2 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((L/2 -T , 0, 0)) #type: ignore

    # 3. Body 1 (Horizontal cylinders connecting left and right flanges)
    body1_D = D * 0.6
    body1_L = (L - 2*T ) 
    body1 = CYLINDER(s, R=body1_D/2, H=body1_L).rotateY(90).translate((-body1_L/2, 0, 0)) #type: ignore
    
    f1.uniteWith(body1)
    body1.erase()
    
    # 4. Body 2 3 4 (Phần body chứa đĩa van)
    # Chiều cao phân bổ cho phần này là H / 2  
    body2_D = D * 0.7
    body2_L = 0.4 * L
    body2 = CYLINDER(s, R=body2_D/2, H=body2_L).rotateY(90).translate((-body2_L/2, 0, 0))#type: ignore

    body4_H = 0.4 * L
    body4_L = 0.7 * D
    body4_W = H/2 - body2_D / 2  #type: ignore
    body4 = BOX(s, L=body4_L, W=body4_W, H=body4_H).rotateY(0).translate((0, 0, body4_W / 2 )) #type: ignore
    body4.uniteWith(body2)
    body2.erase()

    body3_D = D * 0.7
    body3_L = 0.4 * L
    body3 = CYLINDER(s, R=body3_D/2, H=body3_L).rotateY(90).translate((-body2_L/2, 0, H/2 - body3_D/2))#type: ignore

    body4.uniteWith(body3)
    body3.erase()
    
    f1.uniteWith(body4)
    body4.erase()


    # 5. Mặt bích thân valve
    bodyFlange_L = 0.8 * L

    bodyFlange1_D = 0.6 * L
    bodyFlange1_H = 0.8 * 2 * T
    bodyFlange1 = CYLINDER(s, R=bodyFlange1_D/2, H=bodyFlange1_H).translate((0, bodyFlange_L/3, 0.3*H)) #type: ignore
    f1.uniteWith(bodyFlange1)
    bodyFlange1.erase()

    bodyFlange2_D = 0.6 * L
    bodyFlange2_H = 0.8 * 2 * T
    bodyFlange2 = CYLINDER(s, R=bodyFlange2_D/2, H=bodyFlange2_H).translate((0, -bodyFlange_L/3, 0.3*H)) #type: ignore
    f1.uniteWith(bodyFlange2)
    bodyFlange2.erase()

    bodyFlange3_L = bodyFlange_L - bodyFlange1_D / 2
    bodyFlange3_H = 0.6 * L 
    bodyFlange3_W = 0.8 * 2 * T
    bodyFlange3 = BOX(s, L=bodyFlange3_L, W=bodyFlange3_W, H=bodyFlange3_H).translate((0, 0, 0.3*H + bodyFlange3_W/2 )) #type: ignore
    f1.uniteWith(bodyFlange3)
    bodyFlange3.erase()


    # 6. Trục tay vặn
    shaft_d = 32
    shaft_h = H-H/2 
    shaft = CYLINDER(s, R=shaft_d/2, H=shaft_h).translate((0, 0, H/2)) #type: ignore
    f1.uniteWith(shaft)
    shaft.erase()

    # 7. Tay vặn
    handwheel_d = D1
    handwheel_h = 30
    handwheel = CYLINDER(s, R=handwheel_d/2, H=handwheel_h).translate((0, 0, H1-handwheel_h/2)) #type: ignore
    f1.uniteWith(handwheel)
    # handwheel.erase()
    
    # 8. Top hexagon
    hex_L = 40
    hex_W = 40
    hex_H = 23.1
    hex1 = BOX(s, L=hex_L, W=hex_W, H=hex_H).translate((0, 0, H1 + handwheel_h/2))              #type: ignore
    hex2 = BOX(s, L=hex_L, W=hex_W, H=hex_H).rotateZ(60).translate((0, 0, H1 + handwheel_h/2))  #type: ignore
    hex3 = BOX(s, L=hex_L, W=hex_W, H=hex_H).rotateZ(120).translate((0, 0, H1 + handwheel_h/2)) #type: ignore

    hex1.uniteWith(hex2)
    hex2.erase()
   
    hex1.uniteWith(hex3)
    hex3.erase()

    f1.uniteWith(hex1)
    hex1.erase()

    # 9. Gân gia cường tay vặn
    rib1_L = 0.15 * L
    rib1_W = 20
    rib1_H = 0.45 * L
    rib1 = BOX(s, L=rib1_L, W=rib1_W, H=rib1_H).translate((0, 0, H/2 +rib1_W/2)) #type: ignore
    f1.uniteWith(rib1)
    rib1.erase() 

    rib2_L = 0.2 * L
    rib2_W = 20
    rib2_H = 0.2 * L
    rib2 = BOX(s, L=rib2_L, W=rib2_W, H=rib2_H).translate((0, 0,0.75*H  - rib2_W/2 - handwheel_h)) #type: ignore
    f1.uniteWith(rib2)
    rib2.erase() 

    rib3_L = 20
    rib3_W =  H/2 - handwheel_h
    rib3_H = 20
    rib3 = BOX(s, L=rib3_L, W=rib3_W, H=rib3_H).translate((-35, 0, H/2 +rib1_W/2 )) #type: ignore
    f1.uniteWith(rib3)
    rib3.erase()

    rib4_L = 20
    rib4_W = H/2 - handwheel_h
    rib4_H = 20
    rib4 = BOX(s, L=rib4_L, W=rib4_W, H=rib4_H).translate((35, 0, H/2 +rib1_W/2 )) #type: ignore
    f1.uniteWith(rib4)
    rib4.erase()
    
    # Ports
    s.setPoint((-L/2, 0, 0), (-1, 0, 0)) # Port 1
    s.setPoint((L/2, 0, 0), (1, 0, 0))   # Port 2
    
    return f1

OUT = JIS_100MPA_VLV_VTFL