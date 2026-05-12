def run(s, L=250.0, D=200.0, T=22.0, H=130, **kw):
# Trong script hiện tại, chưa thể sử dụng parameter H để điều chỉnh chiều cao tổng thể của van, vì phần thân chính của van được thiết kế với kích thước cố định. 
# Lý do là nếu sử dụng H để điều chỉnh chiều cao tổng thể, giá trị extrude của part1 không hiển thị đúng như mong muốn. ví dụ là dù cho có nhập H là 0 hay 100 thì giá trị được dùng để set chiều cao extrude vẫn hiển thị là 1 hằng số nào đó??????????????????
# Tuy nhiên, tôi sẽ giữ tham số H trong hàm run . nếu tìm ra cách khắc phục vấn đề này tôi sẽ cập nhật lại code sau. 

#region :deliverParams for check valve
    B = 3*D/5 #Body size

#endregion
    # 1. Left Flange
    f1 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((-L/2, 0, 0)) #type: ignore
    
    # 2. Right Flange
    f2 = CYLINDER(s, R=D/2, H=T).rotateY(90).translate((L/2-T, 0, 0)) #type: ignore
    
    # 3. Nozzles (Horizontal cylinders connecting flanges to body)
    noz_d = D * 0.5
    noz_len = (L/2 - T) - (B/2)
    noz1 = CYLINDER(s, R=noz_d/2, H=noz_len).rotateY(90).translate((-L/2+T, 0, 0)) #type: ignore
    noz2 = CYLINDER(s, R=noz_d/2, H=noz_len).rotateY(90).translate((B/2, 0, 0)) #type: ignore
    f1.uniteWith(noz1)
    f1.uniteWith(noz2)
    f1.uniteWith(f2)
    
    # 4. Central Body 
    # Using a Box for the central junction
    # body_size = 2*D/3
    # body_box = BOX(s, L=B, W=B, H=B).translate((0, 0, 0))
    RX = L-2*T - 2*noz_len
    RY = 2*B/3
    A1 = 360
    A2 = 0
    A3 = 0
    A4 = 180
    body_main = ELLIPSOIDSEGMENT(s, RX=RX, RY=RY, A1=A1, A2=A2, A3=A3, A4=A4) #type: ignore
    f1.uniteWith(body_main)
    
    # 5. Top part 1 (connect to body)

    part1 = CYLINDER(s, R = 0.8*D*0.5 , H = H-33).translate((0, 0, 0)) #type: ignore
    f1.uniteWith(part1)
    part1.erase()

    # 6. Top part 2 (top flange)
    part2 = CYLINDER(s, R=0.5*D*0.9, H =25).translate((0, 0,  H-33)) #type: ignore
    f1.uniteWith(part2)
    
    # 7. Top hexagon
    hex_L = 40
    hex_W = 8
    hex_H = 23.1
    hex1 = BOX(s, L=hex_L, W=hex_W, H=hex_H).translate((0, 0, H-33+25))              #type: ignore
    hex2 = BOX(s, L=hex_L, W=hex_W, H=hex_H).rotateZ(60).translate((0, 0, H-33+25))  #type: ignore
    hex3 = BOX(s, L=hex_L, W=hex_W, H=hex_H).rotateZ(120).translate((0, 0, H-33+25)) #type: ignore

    hex1.uniteWith(hex2)
    hex2.erase()
   
    hex1.uniteWith(hex3)
    hex3.erase()

    f1.uniteWith(hex1)

    # 8. Valve shaft 
    shaft_d = 12
    shaft_h = 20 + RY/2
    # shaft_h = 200

    shaft = CYLINDER(s, R=shaft_d/2, H=shaft_h).rotateX(90).translate((0.3*D, shaft_h, RY)) #type: ignore
    # shaft = CYLINDER(s, R=shaft_d/2, H=shaft_h).translate((0, 0, 0)) #type: ignore

    f1.uniteWith(shaft)
    shaft.erase()

    # Ports
    s.setPoint((-L/2, 0, 0), (-1, 0, 0)) # Port 1
    s.setPoint((L/2, 0, 0), (1, 0, 0))   # Port 2
    
    return f1
