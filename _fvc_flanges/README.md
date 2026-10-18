# Thư Viện _fvc_flanges — JIS B 2220 / JIS B 2062 Cho AutoCAD Plant 3D

## 1. Giới thiệu tổng quan

`_fvc_flanges` là thư viện Python chuyên dụng được thiết kế riêng cho **AutoCAD Plant 3D**, cung cấp giải pháp dựng hình Solid 3D tham số hóa (parametric 3D modeling) cho các loại mặt bích tiêu chuẩn công nghiệp Nhật Bản **JIS B 2220** và **JIS B 2062**.

Thư viện giúp chuẩn hóa việc tạo hình mặt bích cho cả hai bài toán:

1. **Dựng mặt bích độc lập (Standalone Piping Flange):** Bích nối ống như SOP, WN, BL... với đầy đủ lỗ bu lông, lỗ khoét trong và gờ Raised Face.
2. **Dựng bích đúc liền thân thiết bị/van (Integral Flange - IT):** Dùng làm đầu nối cho các loại van (Gate Valve, Check Valve, Ball Valve...) hoặc phụ kiện đường ống.

---

## 2. Cấu trúc thư mục module

```text
_fvc_flanges/
├── __init__.py           # Export các API chính: JisFlange, JisFlangeObject, get_flange_dimensions, FlangeDimensions
├── jis_flange.py         # Factory function JisFlange() & Wrapper class JisFlangeObject (hỗ trợ method chaining)
├── README.md             # Tài liệu kỹ thuật chi tiết này
├── models/
│   ├── __init__.py
│   └── dimensions.py     # Data model FlangeDimensions (dataclass chứa đầy đủ thông số kỹ thuật JIS)
├── db/
│   ├── __init__.py
│   └── reader.py         # Module truy vấn kích thước (O(1) In-Memory Lookup + SQLite Fallback)
├── data/
│   ├── __init__.py
│   ├── dataset.py        # Bộ dữ liệu thuần Python (200 records 10K & 7K5), không phụ thuộc external C DLL
│   ├── jis_b2220.sqlite  # Cơ sở dữ liệu SQLite gốc
│   ├── seed_10k.py       # Script nạp dữ liệu JIS 10K
│   └── seed_7k5.py       # Script nạp dữ liệu JIS 7.5K
└── geometry/
    ├── __init__.py
    └── builder.py        # Core dựng hình Solid 3D (CYLINDER, CONE, Boolean Operations)
```

---

## 3. Các tiêu chuẩn và chủng loại bích hỗ trợ

### 3.1. Cấp áp suất (Pressure Rating)

* **`10K`** (1.0 MPa): Cỡ danh định từ **DN10 đến DN1500** (35 dải kích thước tiêu chuẩn).
* **`7K5`** (0.75 MPa): Cỡ danh định từ **DN40 đến DN600** (15 dải kích thước tiêu chuẩn).
* *(Dễ dàng mở rộng thêm 5K, 16K, 20K, 30K thông qua seed file)*.

### 3.2. Chủng loại mặt bích (Flange Types)

| Mã loại         | Tên tiêu chuẩn | Mô tả công dụng                                | Đặc điểm hình học                                                                              |
| :---------------- | :---------------- | :------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| **`IT`**  | Integral          | Bích đúc liền trên thân van hoặc thiết bị | Có cổ côn (Hub) nối liền vào thân van/vỏ bơm                                                |
| **`SOP`** | Slip-On Plate     | Bích phẳng hàn trượt dạng tấm               | Khoét rỗng lỗ tâm$d_0$ để lồng ống thép vào hàn góc                                    |
| **`WN`**  | Welding Neck      | Bích hàn cổ cao giáp mối                      | Có cổ côn vát mép, đường kính trong lòng ống$d_{\text{bore}}$, mép ngoài $pipe\_od$ |
| **`BL`**  | Blind             | Bích mù / Bích đặc bịt kín đầu ống       | Không khoét lỗ tâm ($d_0 = 0$), độ dày tiêu chuẩn $t_{\text{bl}}$                       |

---

## 4. Nguyên lý hình học & Hệ tọa độ chuẩn trong AutoCAD Plant 3D

### 4.1. Quy chuẩn chiều dày mặt bích JIS B 2220

Theo tiêu chuẩn Nhật Bản JIS B 2220:

* **$t$**: Tổng chiều dày danh định của bích — **đã bao gồm chiều cao gờ nâng $f$**.
* **$\text{base\_t} = t - f$**: Chiều dày của vành đĩa ngoài (phần không có gờ nâng).
* **$f$**: Chiều cao gờ Raised Face (RF) (thường là $1\text{ mm}$ với DN nhỏ, $2\text{ mm}$ với DN trung bình, $3\text{ mm}$ với DN lớn).
* **$g$**: Đường kính gờ Raised Face.
* **$D$**: Đường kính ngoài của mặt bích.
* **$C$ (PCD)**: Đường kính vòng tròn chia tâm các lỗ bu lông.
* **$h$ / $N$**: Đường kính lỗ bu lông và số lượng lỗ bu lông.

### 4.2. Hệ tọa độ cục bộ (Local Coordinate System)

Trong engine AutoCAD Plant 3D (`varmain.primitiv`), khối `CYLINDER` và `CONE` có đáy nằm tại $Z = 0$ và chiều cao hướng dọc trục $+Z$.

`_fvc_flanges` định vị hình khối như sau:

1. **Mặt sau bích (Back face):** Cố định tại **$Z = 0$**.
2. **Vành đĩa chính (Main Disc):**
   * Bắt đầu từ $Z = 0$ đến $Z = \text{base\_t}$.
   * Bán kính: $R = D / 2$.
3. **Gờ Raised Face (RF):**
   * Đặt tiếp nối ngay trên vành đĩa chính, từ $Z = \text{base\_t}$ đến $Z = t$.
   * Bán kính: $R = g / 2$.
   * Nhô cao đúng $f\text{ mm}$, giật cấp vào trong tạo bậc thang rõ nét.
4. **Cổ bích (Hub) (nếu `has_hub=True`):**
   * Đáy lớn ($b$) tiếp xúc mặt sau bích tại $Z = 0$.
   * Đáy nhỏ ($a$) vươn ngược về phía âm trục Z: từ $Z = -(\text{total\_len} - t)$ đến $Z = 0$.
5. **Khoét rỗng lỗ tâm (Bore):**
   * Trục cắt dọc tâm Z từ $Z = -(\text{hub\_h} + 5)$ xuyên suốt qua $Z = t + 5$.
   * Đường kính cắt: $d_0$ (đối với SOP) hoặc $d_{\text{bore}}$ (đối với WN/IT).
6. **Đục lỗ bu lông (Bolt Holes):**
   * Các khối trụ đường kính $h$ phân bố đều theo góc $\theta = \frac{2\pi \cdot i}{N}$ trên bán kính $C/2$.
   * Cắt xuyên suốt vành bích từ $Z = -5$ đến $Z = t + 5$.

```text
                  +Z (Trục dòng chảy / Hướng kết nối)
                   ▲
                   │       ┌─────────┐  ◄── Mặt gờ RF (Z = t), Đường kính g
                   │  ┌────┘         └────┐
  Vành bích ngoài  │  │   (Lỗ bu lông h)  │ ◄── Vành bích chính (Z = base_t), Đường kính D
 (Chiều dày base_t)│  │   │     │         │
                   └──┼───┼─────┼─────────┼──► X, Y
                      │   │  ▲  │         │  ◄── Mặt sau bích (Z = 0)
                      │   │  │  │         │
                      └───┘  │  └─────────┘
                             │
                      Lỗ khoét tâm d0
```

### 4.3. Cổng kết nối (Ports)

* **Port 1 (Mặt tiếp xúc gioăng RF):** Tọa độ `(0, 0, dim.t)`, Vector hướng `(0, 0, 1)`.
* **Port 2 (Mặt sau nối ống/hàn):** Tọa độ `(0, 0, -hub_h)` (hoặc `(0, 0, 0)` nếu không có cổ côn), Vector hướng `(0, 0, -1)`.

---

## 5. Kiến trúc truy vấn dữ liệu (Data Access Layer)

AutoCAD Plant 3D tích hợp môi trường Python rút gọn (*embedded runtime*) và **không đính kèm file binary `_sqlite3.pyd`**. Do đó, việc gọi trực tiếp `import sqlite3` trong Plant 3D sẽ gây lỗi `ModuleNotFoundError: No module named '_sqlite3'`.

Để giải quyết triệt để vấn đề này, kiến trúc dữ liệu của `_fvc_flanges` được thiết kế 2 tầng:

1. **Tầng 1 (Primary - In-Memory Dataset):**
   * File `data/dataset.py` lưu trữ sẵn toàn bộ 200 bản ghi bích chuẩn dưới dạng Dictionary Python thuần túy.
   * Tra cứu tức thời theo khóa `(rating, flange_type, dn)` với độ phức tạp **$O(1)$**, không tốn I/O đĩa và **hoàn toàn không phụ thuộc vào bất kỳ DLL nào**.
2. **Tầng 2 (Fallback - SQLite Dynamic):**
   * Khi cần tra cứu bản ghi tùy biến ngoài danh mục mặc định, `db/reader.py` sẽ thử kết nối `jis_b2220.sqlite` trong khối an toàn `try...except ImportError`.

---

## 6. Hướng dẫn sử dụng API

### 6.1. Khởi tạo mặt bích qua hàm `JisFlange`

```python
from _fvc_flanges import JisFlange

flange = JisFlange(
    s=s,                # Subpart container của Plant 3D (bắt buộc)
    rating="10K",       # Cấp áp: '10K', '7K5' (mặc định '10K')
    dn=100,             # Cỡ danh định: 10, 15, ..., 1500 (mặc định 50)
    flange_type="SOP",  # Loại bích: 'IT', 'SOP', 'WN', 'BL' (mặc định 'IT')
    has_holes=True,     # True: đục lỗ bu lông (LOD cao) | False: bích trơn (nhẹ model)
    has_rf=True,        # True: có gờ nổi Raised Face | False: mặt phẳng FF
    has_hub=False,      # True: có cổ côn bích (cho IT, WN) | False: bích phẳng
    has_bore=True       # True: khoét rỗng lỗ tâm | False: bích đặc
)
```

### 6.2. Wrapper Class `JisFlangeObject` & Chaining Methods

Đối tượng trả về `JisFlangeObject` hỗ trợ gọi chuỗi phương thức (*method chaining*) để dịch chuyển và xoay không gian linh hoạt:

* `.rotateX(deg)`: Xoay quanh trục X.
* `.rotateY(deg)`: Xoay quanh trục Y.
* `.rotateZ(deg)`: Xoay quanh trục Z.
* `.translate((x, y, z))` hoặc `.move((x, y, z))`: Dịch chuyển theo vector.
* `.uniteWith(other)`: Gộp khối `other` vào bích và tự động giải phóng (`erase`) đối tượng `other`.
* `.subtractFrom(other)`: Cắt trừ khối `other`.
* `.unwrap()`: **Lấy đối tượng hình học gốc** để trả về cho engine AutoCAD Plant 3D.
* `.dim`: Truy cập thông số kích thước kỹ thuật ([FlangeDimensions](<file:///c:/Users/Laptop/OneDrive/Desktop/Hello%20World/Python-Autocad-Plant-3D/_fvc_flanges/models/dimensions.py>)).

---

## 7. Các kịch bản ứng dụng mẫu

### 7.1. Kịch bản 1: Test mặt bích đơn lẻ (Hot Reload trong AutoCAD)

Viết trong file `hotreload_impl.py`:

```python
import sys, os

# Đảm bảo đường dẫn và tự động reload cache
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

for mod_name in list(sys.modules.keys()):
    if mod_name.startswith('_fvc_flanges'):
        del sys.modules[mod_name]

from _fvc_flanges import JisFlange

def run(s, **kw):
    flange = JisFlange(
        s=s,
        rating="10K",
        dn=200,
        flange_type="SOP",
        has_holes=True,
        has_rf=True,
        has_bore=True
    )
    dim = flange.dim

    # Thiết lập Port cho AutoCAD Plant 3D
    s.setPoint((0, 0, dim.t), (0, 0, 1))   # Cổng 1: Mặt RF
    s.setPoint((0, 0, 0), (0, 0, -1))       # Cổng 2: Mặt sau

    return flange.unwrap()
```

### 7.2. Kịch bản 2: Tích hợp vào hai đầu van (Valve Assembly)

Khi gắn bích vào thân van (dọc trục X từ $-L/2$ đến $+L/2$):

```python
from _fvc_flanges import JisFlange

def build_valve(s, L=300.0, DN=100, **kw):
    # 1. Bích trái (Port 1 ở -L/2, mặt RF quay sang hướng -X)
    f_left = JisFlange(s, rating="10K", dn=DN, flange_type="IT", has_rf=True, has_holes=True)
    f_left.rotateY(-90).translate((-L/2 + f_left.dim.t, 0, 0))

    # 2. Bích phải (Port 2 ở +L/2, mặt RF quay sang hướng +X)
    f_right = JisFlange(s, rating="10K", dn=DN, flange_type="IT", has_rf=True, has_holes=True)
    f_right.rotateY(90).translate((L/2 - f_right.dim.t, 0, 0))

    # 3. Gộp bích phải vào bích trái
    f_left.uniteWith(f_right)

    # 4. Tiếp tục dựng thân van (body) và gộp vào f_left...
    # ...
  
    # 5. Cài đặt ports hai đầu van
    s.setPoint((-L/2, 0, 0), (-1, 0, 0))
    s.setPoint((L/2, 0, 0), (1, 0, 0))

    return f_left.unwrap()
```

---

## 8. Hướng dẫn mở rộng thêm dữ liệu (Add new Rating/Standard)

Khi cần bổ sung thêm cấp áp mới (ví dụ: `5K` hoặc `20K`):

1. Thêm mảng dữ liệu thô vào file `data/seed_<rating>.py` theo cấu trúc:
   ```python
   # (DN, D, C, h, No, bolt_name, g, f, t, t_bl, T_it, a_OD, b, d0, d_bore)
   ```
2. Chạy file seed để cập nhật cơ sở dữ liệu `data/jis_b2220.sqlite`.
3. Cập nhật hoặc xuất lại từ điển vào `data/dataset.py` để sử dụng ngay trong AutoCAD Plant 3D mà không gặp lỗi thiếu DLL SQLite.
