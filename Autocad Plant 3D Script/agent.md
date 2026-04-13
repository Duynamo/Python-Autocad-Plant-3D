# Hướng dẫn Lập trình Tiêu chuẩn AutoCAD Plant 3D (Agent Coding Guide)

Tài liệu này được tổng hợp từ **Lib.py** và tài liệu **PD4214-L**, định nghĩa các quy tắc và thư viện hàm chuẩn để phát triển Custom Scripts cho AutoCAD Plant 3D.

---

## 1. Nguyên tắc Dựng hình Cơ bản
- **Bản chất**: Script là generator dùng để tạo khối hình học solid nằm trong một AutoCAD Block.
- **Điểm kết nối (Ports)**: Là yếu tố quan trọng nhất để linh kiện tự động bắt dính vào đường ống. Mỗi Port cần có: **Vị trí (Position)** và **Vector hướng (Direction)**.
- **Đơn vị**: Luôn kiểm tra `LengthUnit` ("mm" ) trong `@activate`.
- **Hiệu suất**: Phải giải phóng bộ nhớ bằng lệnh `.erase()` ngay sau khi thực hiện các phép toán Boolean (`uniteWith`, `subtractFrom`, `intersectWith`).

---

## 2. Thư viện Khối cơ bản (Geometric Primitives)

| Hàm | Thông số chính | Điểm gốc (Base Point) |
| :--- | :--- | :--- |
| **BOX** | `L` (Dài), `W` (Rộng), `H` (Cao) | Trọng tâm khối |
| **CYLINDER** | `R` (Bán kính), `H` (Cao), `O` (Lỗ rỗng) | Tâm mặt đáy |
| **CONE** | `R1` (Đáy dưới), `R2` (Đáy trên), `H`, `E` (Lệch tâm) | Tâm mặt đáy dưới |
| **ARC3D** | `D` (Bán kính ống), `R` (Bán kính uốn), `A` (Góc) | Giao điểm đường tâm 2 đầu |
| **PYRAMID** | `L`, `W` (Đáy), `H` (Khối cụt), `HT` (Tổng cao) | Tâm hình chữ nhật đáy |
| **ROUNDRECT** | `L`, `W` (Đáy), `H`, `R2` (Kính đỉnh), `E` (Lệch) | Tâm hình chữ nhật đáy |
| **TORUS** | `R1` (Bán kính ngoài), `R2` (Bán kính ống) | Giao điểm đường tâm 2 đầu |

---

## 3. Kỹ thuật Hiệu chỉnh & Truy vấn Nâng cao

### Phép toán Boolean & Di chuyển
- **Hợp nhất**: `o0.uniteWith(o1)` sau đó `o1.erase()`.
- **Trừ khối**: `o0.subtractFrom(o2)` sau đó `o2.erase()`.
- **Xoay**: `.rotateX(angle)`, `.rotateY(angle)`, `.rotateZ(angle)` (đơn vị: độ).
- **Ma trận**: Sử dụng `.setTransformationMatrix(mtx)` để xử lý các phép dời hình phức tạp.

### Truy vấn thông tin
- **Lấy tham số**: `obj.parameters()` trả về dict chứa các kích thước đã tính toán (ví dụ: `vT["H"]`).
- **Kế thừa Port**: Sử dụng `obj.pointAt(index)` và `obj.directionAt(index)` để lấy thông số Port của khối con gán cho khối chính.

---

## 4. Metadata & Đăng ký (Workflow)

### Quy tắc Metadata
1. **@activate**: Luôn ở hàng đầu tiên. Chứa `Group`, `Tooltip`, `LengthUnit`.
2. **@group**: Phân nhóm tham số cho giao diện người dùng.
3. **@param**: Định nghĩa kiểu dữ liệu (`LENGTH`, `ANGLE`, `ENUM`). Sử dụng `Ask4Dist=True` nếu muốn cho phép click chọn khoảng cách trên màn hình.

### Quy trình Đăng ký & Test
1. Đặt file `.py` vào thư mục `CustomScripts` trong đường dẫn Content.
2. Lệnh đăng ký: `PLANTREGISTERCUSTOMSCRIPTS`.
3. Lệnh test: `(arxload "PnP3dACPAdapter.arx")` sau đó `(TESTACPSCRIPT "TênScript")`.
4. Ảnh xem trước: Lệnh `PlantSnapShot`, đặt tên `[ScriptName]_200.png` (64, 32).

---

## 5. Ví dụ Cấu trúc Chuẩn (CPMB Reference)
```python
def CPMB(s, L=54.0, B=22.0, D1=220.0, D2=114.3, **kw):
    O = CON_OF_DIV(D2)/2.0
    # Tạo nhánh, xoay và dời hình
    o1 = CYLINDER(s, R=D2/2.0, H=L-B, O=O).rotateY(90).translate((B, 0, 0))
    # Tạo gốc
    o0 = CYLINDER(s, R=D1/2.0, H=B, O=O).rotateY(90)
    # Hợp nhất và xóa khối phụ
    o0.uniteWith(o1)
    o1.erase()
    # Định nghĩa port chuẩn
    s.setPoint((0, 0, 0), (-1, 0, 0))
    s.setPoint((L, 0, 0), (1, 0, 0))
```
