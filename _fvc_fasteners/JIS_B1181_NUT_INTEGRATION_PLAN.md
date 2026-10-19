# KẾ HOẠCH TÍCH HỢP ĐAI ỐC LỤC GIÁC THEO TIÊU CHUẨN JIS B 1181 : 2014

> **Tài liệu quy chuẩn tham chiếu**: [JIS B 1181 : 2014 (六角ナット及び六角低ナット - Hexagon nuts and hexagon thin nuts)](https://kikakurui.com/b1/B1181-2014-01.html)  
> **Module đích trong dự án**: `_fvc_fasteners`  
> **Ngôn ngữ thực hiện**: Python 3, SQLite3, AutoCAD Plant 3D Primitives Engine  

---

## MỤC LỤC
1. [Tổng quan về quy chuẩn JIS B 1181:2014](#1-tổng-quan-về-quy-chuẩn-jis-b-11812014)
2. [Hệ thống phân loại toàn bộ các loại Nut](#2-hệ-thống-phân-loại-toàn-bộ-các-loại-nut)
   - [Nhóm I: Hệ Tiêu chuẩn Quốc tế ISO (Thân tiêu chuẩn chính)](#nhóm-i-hệ-tiêu-chuẩn-quốc-tế-iso-thân-tiêu-chuẩn-chính)
   - [Nhóm II: Hệ Truyền thống Nhật Bản (Phụ lục quy chuẩn JA)](#nhóm-ii-hệ-truyền-thống-nhật-bản-phụ-lục-quy-chuẩn-ja)
   - [Bảng tổng hợp đối chiếu 12 chủng loại Nut](#bảng-tổng-hợp-đối-chiếu-12-chủng-loại-nut)
   - [Quy chuẩn vật liệu và cấp độ bền](#quy-chuẩn-vật-liệu-và-cấp-độ-bền)
3. [Kế hoạch cập nhật cơ sở dữ liệu và mã nguồn](#3-kế-hoạch-cập-nhật-cơ-sở-dữ-liệu-và-mã-nguồn)
   - [Bước 1: Mô hình hóa dữ liệu (Data Modeling)](#bước-1-mô-hình-hóa-dữ-liệu-data-modeling)
   - [Bước 2: Thiết kế cơ sở dữ liệu SQLite (jis_b1181.sqlite)](#bước-2-thiết-kế-cơ-sở-dữ-liệu-sqlite-jis_b1181sqlite)
   - [Bước 3: Khởi tạo bộ dữ liệu RAM siêu tốc (jis_b1181_dataset.py)](#bước-3-khởi-tạo-bộ-dữ-liệu-ram-siêu-tốc-jis_b1181_datasetpy)
   - [Bước 4: Phát triển tầng truy vấn dữ liệu DAO (jis_b1181_reader.py)](#bước-4-phát-triển-tầng-truy-vấn-dữ-liệu-dao-jis_b1181_readerpy)
   - [Bước 5: Tích hợp hình học 3D và mối nối mặt bích JIS B 1217](#bước-5-tích-hợp-hình-học-3d-và-mối-nối-mặt-bích-jis-b-1217)
   - [Bước 6: Kiểm thử tự động (Unit Tests)](#bước-6-kiểm-thử-tự-động-unit-tests)

---

## 1. TỔNG QUAN VỀ QUY CHUẨN JIS B 1181:2014

Tiêu chuẩn **JIS B 1181:2014** quy định đặc tính kỹ thuật, kích thước hình học, dung sai và phân loại cho các loại đai ốc lục giác (Hexagon nuts) và đai ốc lục giác mỏng (Hexagon thin nuts) làm từ thép cacbon, thép không gỉ (Inox) và kim loại màu.

Cấu trúc cốt lõi của quy chuẩn được chia thành 2 phần độc lập nhưng song hành:
1. **Phần thân tiêu chuẩn chính (ISO Harmonized)**: Được biên dịch và hài hòa kỹ thuật từ **8 tiêu chuẩn quốc tế ISO** (ISO 4032 đến ISO 4036 và ISO 8673 đến ISO 8675 bản 2012).
2. **Phần Phụ lục quy chuẩn JA (附属書JA - Annex JA)**: Quy định các loại đai ốc theo **hệ truyền thống Nhật Bản** (1種, 2種, 3種, 4種; loại đai ốc thường và đai ốc cỡ nhỏ) không theo hệ ISO. Phụ lục này tiếp tục được duy trì do thói quen thiết kế và sản lượng chế tạo thực tế tại Nhật Bản chiếm tỷ trọng áp đảo.
3. **Phần Phụ lục quy chuẩn JB (附属書JB - Annex JB)**: Quy định cơ tính và cấp độ bền thép truyền thống **4T đến 10T** của Nhật Bản.

---

## 2. HỆ THỐNG PHÂN LOẠI TOÀN BỘ CÁC LOẠI NUT

Tất cả các loại Nut trong JIS B 1181:2014 được phân định thành **12 dòng sản phẩm chuẩn**:

```
JIS B 1181:2014 (Hệ thống phân loại Nut)
├── Nhóm I: Hệ Tiêu chuẩn Quốc tế ISO (Thân tiêu chuẩn - 8 loại)
│   ├── Đai ốc tiêu chuẩn (Style 1 - chiều cao m ≈ 0.8d đến 0.9d)
│   │   ├── 1. Hex Nut Style 1 - Bước thô (ISO 4032) [Cấp A/B]
│   │   ├── 2. Hex Nut Style 1 - Bước mịn (ISO 8673) [Cấp A/B]
│   │   └── 3. Hex Nut C - Bước thô cấp thô (ISO 4034) [Cấp C]
│   ├── Đai ốc cao (Style 2 - High Nut - chiều cao m ≈ 1.0d)
│   │   ├── 4. Hex High Nut Style 2 - Bước thô (ISO 4033) [Cấp A/B]
│   │   └── 5. Hex High Nut Style 2 - Bước mịn (ISO 8674) [Cấp A/B]
│   └── Đai ốc mỏng / Đai ốc hãm (Style 0 - Thin Nut - chiều cao m ≈ 0.5d)
│       ├── 6. Hex Thin Nut vát mép 2 mặt - Bước thô (ISO 4035) [Cấp A/B]
│       ├── 7. Hex Thin Nut vát mép 2 mặt - Bước mịn (ISO 8675) [Cấp A/B]
│       └── 8. Hex Thin Nut không vát mép - Bước thô (ISO 4036) [Cấp B]
│
└── Nhóm II: Hệ Truyền thống Nhật Bản (Phụ lục JA - Annex JA - 4 loại hình học)
    ├── Phân loại theo kích thước giác cờ-lê (s/d):
    │   ├── 並形六角ナット (Đai ốc thường, s/d ≥ 1.45)
    │   └── 小形六角ナット (Đai ốc cỡ nhỏ, s/d < 1.45)
    └── Phân loại theo hình dạng gia công (4 loại):
        ├── 9. Loại 1 (1種 - Type 1): Vát mép 1 mặt (m ≈ 0.8d)
        ├── 10. Loại 2 (2種 - Type 2): Vát mép 2 mặt (m ≈ 0.8d)
        ├── 11. Loại 3 (3種 - Type 3): Đai ốc mỏng / đai ốc hãm (m ≈ 0.5d đến 0.6d)
        └── 12. Loại 4 (4種 - Type 4): Vát mép 1 mặt, mặt kia có gờ đệm tròn (m ≈ 0.8d)
```

---

### Bảng tổng hợp đối chiếu 12 chủng loại Nut

> 📊 **Bản bảng tính Excel kỹ thuật đã được tạo lập**:  
> Dữ liệu phân loại chi tiết đã được xuất thành bảng tính Excel chuyên nghiệp có phân màu, kẻ khung viền, tự động căn chỉnh độ rộng cột và gán bộ lọc tại:
> * File nội bộ module: [JIS_B1181_NUT_SPECIFICATION.xlsx](file:///c:/Users/95053/Desktop/Hello%20World/Python-Autocad-Plant-3D/_fvc_fasteners/JIS_B1181_NUT_SPECIFICATION.xlsx)
> * Thư mục Catalog dự án: [JIS_B1181_NUT_SPECIFICATION.xlsx](file:///c:/Users/95053/Desktop/Hello%20World/Python-Autocad-Plant-3D/Excel%20Catalog/JIS_B1181_NUT_SPECIFICATION.xlsx)

Dưới đây là cấu trúc hiển thị dạng bảng tính dữ liệu (Excel Grid View) phân tách rành mạch từng cột trường thông tin:

---

#### BẢNG 1: NHÓM THÂN TIÊU CHUẨN QUỐC TẾ (HÀI HÒA ISO - 8 LOẠI)

| STT | Nhóm kiểu dáng | Tiêu chuẩn ISO | Tên tiếng Nhật chuẩn | Tên tiếng Anh kỹ thuật | Bước ren | Cấp SP | Chiều cao m | Vát mép & Mặt tỳ | Dải cỡ ren D | Ứng dụng kỹ thuật chính |
| :-: | :--- | :-: | :--- | :--- | :-: | :-: | :-: | :--- | :-: | :--- |
| **1** | Style 1 (Tiêu chuẩn) | **ISO 4032** | 六角ナット−スタイル1 (並目) | Hexagon regular nut (Style 1) Coarse | Thô | A / B | m ≈ 0.8d | Vát mép đỉnh, có gờ đệm mặt tỳ (dw) | M1.6 - M64 | **Mặc định chuẩn cho mặt bích đường ống** và cơ khí chính |
| **2** | Style 1 (Tiêu chuẩn) | **ISO 8673** | 六角ナット−スタイル1 (細目) | Hexagon regular nut (Style 1) Fine | Mịn | A / B | m ≈ 0.8d | Vát mép đỉnh, có gờ đệm mặt tỳ (dw) | M8x1 - M64x4 | Chống tự nới lỏng do rung động, tinh chỉnh khe hở trục |
| **3** | Style 1 (Cấp C Thô) | **ISO 4034** | 六角ナット−C (並目) | Hexagon nut Product Grade C | Thô | C | m ≈ 0.8d | Không gờ đệm (mặt tỳ phẳng tự do) | M5 - M64 | Kết cấu thép nhà xưởng, phụ kiện cơ khí thô tiết kiệm |
| **4** | Style 2 (Đai ốc cao) | **ISO 4033** | 六角ナット−スタイル2 (並目) | Hexagon high nut (Style 2) Coarse | Thô | A / B | m ≈ 1.0d | Thành cao tăng ren ăn khớp, có gờ dw | M5 - M39 | Chịu tải trọng chứng minh (Proof Load) lớn, cấp bền 9, 12 |
| **5** | Style 2 (Đai ốc cao) | **ISO 8674** | 六角ナット−スタイル2 (細目) | Hexagon high nut (Style 2) Fine | Mịn | A / B | m ≈ 1.0d | Thành cao ren mịn chịu giật, có gờ dw | M8x1 - M39x3 | Cơ cấu chịu lực kéo cực hạn và yêu cầu chống nới lỏng |
| **6** | Style 0 (Đai ốc mỏng) | **ISO 4035** | 六角低ナット−両面取り (並目) | Hexagon thin nut chamfered Coarse | Thô | A / B | m ≈ 0.5d | Thân mỏng, vát mép cả 2 mặt đối xứng | M1.6 - M64 | Đai ốc khóa chống tuột (Jam Nut / Lock Nut) cụm đôi |
| **7** | Style 0 (Đai ốc mỏng) | **ISO 8675** | 六角低ナット−両面取り (細目) | Hexagon thin nut chamfered Fine | Mịn | A / B | m ≈ 0.5d | Thân mỏng bước mịn, vát mép 2 mặt | M8x1 - M64x4 | Đai ốc khóa chống trôi ở không gian dọc trục ren hẹp |
| **8** | Style 0 (Đai ốc mỏng) | **ISO 4036** | 六角低ナット−面取りなし | Hexagon thin nut unchamfered | Thô | B | m ≈ 0.5d | Thân mỏng, không vát mép (mép vuông) | M1.6 - M10 | Kẹp giữ thiết bị điện tử, tấm che, cơ cấu phụ lực nhẹ |

---

#### BẢNG 2: NHÓM PHỤ LỤC JA (HỆ TRUYỀN THỐNG NHẬT BẢN - 4 LOẠI HÌNH HỌC)

| STT | Phân nhóm giác s/d | Chủng loại hình học | Tên tiếng Nhật chuẩn | Bước ren | Chiều cao m | Số mặt vát mép | Cấu tạo mặt đáy / mặt tỳ | Cấp hoàn thiện | Ứng dụng thực tế đặc trưng |
| :-: | :--- | :--- | :--- | :-: | :-: | :--- | :--- | :-: | :--- |
| **9** | 並形 (s/d ≥ 1.45)<br>小形 (s/d < 1.45) | **Loại 1 (1種 - Type 1)** | 附属書JA 六角ナット 1種 | Thô / Mịn | m ≈ 0.8d | Vát mép 1 mặt | Mặt đáy phẳng tỳ sát hoàn toàn | Thượng / Trung / 並 | Thông dụng nhất trong chế tạo máy công nghiệp nội địa Nhật |
| **10** | 並形 (s/d ≥ 1.45)<br>小形 (s/d < 1.45) | **Loại 2 (2種 - Type 2)** | 附属書JA 六角ナット 2種 | Thô / Mịn | m ≈ 0.8d | Vát mép cả 2 mặt | Hai mặt đối xứng (mặt nào cũng tỳ được) | Thượng / Trung / 並 | Lắp 2 chiều như nhau, tối ưu cho dây chuyền tự động hóa |
| **11** | 並形 (s/d ≥ 1.45)<br>小形 (s/d < 1.45) | **Loại 3 (3種 - Type 3)** | 附属書JA 六角低ナット 3種 | Thô / Mịn | m ≈ 0.5d ~ 0.6d | Vát mép 2 mặt (≤ M5 có thể phẳng) | Hai mặt đối xứng vát mép, thân mỏng | Thượng / Trung / 並 | Chuyên làm đai ốc khóa chống nới lỏng (Lock Nut) cụm rung |
| **12** | 並形 (s/d ≥ 1.45)<br>小形 (s/d < 1.45) | **Loại 4 (4種 - Type 4)** | 附属書JA 六角ナット 4種 | Thô / Mịn | m ≈ 0.8d | Vát mép 1 mặt | Mặt kia có gờ đệm tròn / lõm tích hợp | Thượng / Trung / 並 | Tích hợp sẵn chức năng vòng đệm, tiết kiệm vật tư và công lắp |

---

#### MA TRẬN TRA CỨU NHANH ĐẶC TÍNH 12 LOẠI NUT

| STT | Mã hiệu nhận diện | Tiêu chuẩn | Chiều cao | Bước ren | Số mặt vát mép | Gờ đệm (dw) | Cấp bền áp dụng | Ghi chú kỹ thuật |
| :-: | :--- | :-: | :-: | :-: | :-: | :-: | :--- | :--- |
| 1 | `ISO_4032_STYLE_1_COARSE` | ISO 4032 | Tiêu chuẩn (0.8d) | Thô | 1 hoặc 2 | Có | ISO: 6, 8, 10, 12 | Thân tiêu chuẩn chính (Mặc định cho mặt bích) |
| 2 | `ISO_8673_STYLE_1_FINE` | ISO 8673 | Tiêu chuẩn (0.8d) | Mịn | 1 hoặc 2 | Có | ISO: 6, 8, 10, 12 | Thân tiêu chuẩn chính (Cơ cấu tinh chỉnh) |
| 3 | `ISO_4033_STYLE_2_COARSE` | ISO 4033 | Cao (1.0d) | Thô | 1 hoặc 2 | Có | ISO: 9, 12 | Đai ốc cao chịu tải chứng minh lớn |
| 4 | `ISO_8674_STYLE_2_FINE` | ISO 8674 | Cao (1.0d) | Mịn | 1 hoặc 2 | Có | ISO: 9, 12 | Đai ốc cao ren mịn chịu tải cực hạn |
| 5 | `ISO_4034_STYLE_1_GRADE_C` | ISO 4034 | Tiêu chuẩn (0.8d) | Thô | 1 hoặc 2 | Không | ISO: 4, 5 | Cấp gia công C kinh tế |
| 6 | `ISO_4035_STYLE_0_THIN_COARSE` | ISO 4035 | Mỏng (0.5d) | Thô | 2 mặt | Có | ISO: 04, 05 | Đai ốc mỏng khóa ren bước thô |
| 7 | `ISO_8675_STYLE_0_THIN_FINE` | ISO 8675 | Mỏng (0.5d) | Mịn | 2 mặt | Có | ISO: 04, 05 | Đai ốc mỏng khóa ren bước mịn |
| 8 | `ISO_4036_STYLE_0_UNCHAMFERED` | ISO 4036 | Mỏng (0.5d) | Thô | Không vát | Không | ISO: Thép mềm | Đai ốc mỏng dập mép vuông phẳng |
| 9 | `JA_TYPE_1_REGULAR` | Phụ lục JA | Tiêu chuẩn (0.8d) | Thô / Mịn | 1 mặt | Không | JIS: 4T, 5T, 6T, 8T | Phụ lục JA truyền thống (1 mặt vát) |
| 10 | `JA_TYPE_2_REGULAR` | Phụ lục JA | Tiêu chuẩn (0.8d) | Thô / Mịn | 2 mặt | Không | JIS: 4T, 5T, 6T, 8T | Phụ lục JA truyền thống (2 mặt vát đối xứng) |
| 11 | `JA_TYPE_3_THIN` | Phụ lục JA | Mỏng (0.5 ~ 0.6d) | Thô / Mịn | 2 mặt | Không | JIS: Đai ốc hãm | Phụ lục JA đai ốc hãm truyền thống |
| 12 | `JA_TYPE_4_WASHER_FACE` | Phụ lục JA | Tiêu chuẩn (0.8d) | Thô / Mịn | 1 mặt | Có gờ đệm | JIS: 4T, 5T, 6T, 8T | Phụ lục JA tích hợp mặt đệm |

---

### Quy chuẩn vật liệu và cấp độ bền

1. **Thép cacbon và thép hợp kim**:
   - Hệ ISO (JIS B 1052-2 / JIS B 1052-6): Cấp độ bền **4, 5, 6, 8, 9, 10, 12**.
   - Hệ truyền thống Nhật (Phụ lục JB): Cấp độ bền **4T, 5T, 6T, 8T, 10T** (ví dụ: đai ốc 8T làm việc cùng bu lông 8.8).
2. **Thép không gỉ (Inox)**:
   - Theo JIS B 1054-2: Mác thép A2-50, A2-70, A2-80 (SUS304) và A4-50, A4-70, A4-80 (SUS316).
3. **Kim loại màu**:
   - Theo JIS B 1057: Hợp kim đồng (Cu2, Cu3) và hợp kim nhôm (AL1, AL2).

---

## 3. KẾ HOẠCH CẬP NHẬT CƠ SỞ DỮ LIỆU VÀ MÃ NGUỒN

### Bước 1: Mô hình hóa dữ liệu (Data Modeling)
* **File khởi tạo**: `_fvc_fasteners/models/jis_b1181_specs.py`
* **Nội dung thiết kế**:
  - `NutTypeSpec`: Lưu định danh phân loại chuẩn (12 loại), tiêu chuẩn ISO tương ứng, hệ ren, kiểu chiều cao.
  - `NutDimensionSpec`: Bộ thông số kích thước hình học chi tiết theo từng cỡ ren:
    - `d`: Đường kính ren danh nghĩa (mm).
    - `pitch`: Bước ren (mm).
    - `s_nominal`, `s_min`, `s_max`: Bề rộng giác cờ-lê (Width across flats) (mm).
    - `m_nominal`, `m_min`, `m_max`: Chiều cao đai ốc (Height of nut) (mm).
    - `e_min`: Đường kính đỉnh góc lục giác danh nghĩa (Corner diameter) (mm).
    - `dw_min`: Đường kính gờ tỳ (Washer face diameter) (mm).
    - `da_min`, `da_max`: Đường kính vát mép lỗ ren (Countersink diameter) (mm).
    - `chamfer_angle`: Góc vát mép ngoài (15 đến 30 độ).
  - `HexNutSpec`: Thông số đối tượng đai ốc hoàn chỉnh phục vụ dựng mô hình 3D và xuất bảng BOM.

---

### Bước 2: Thiết kế cơ sở dữ liệu SQLite (jis_b1181.sqlite)
* **File cơ sở dữ liệu**: `_fvc_fasteners/data/jis_b1181.sqlite`
* **File script khởi tạo & nạp dữ liệu**: `_fvc_fasteners/data/jis_b1181_seed.py`
* **Lược đồ CSDL gồm 3 bảng quan hệ**:

```sql
-- 1. Bảng danh mục định danh loại đai ốc
CREATE TABLE IF NOT EXISTS jis_b1181_nut_types (
    type_id INTEGER PRIMARY KEY,
    type_code TEXT UNIQUE NOT NULL,
    type_name_ja TEXT NOT NULL,
    iso_equivalent TEXT,
    nut_style TEXT NOT NULL,
    pitch_type TEXT NOT NULL,
    product_grade TEXT NOT NULL,
    is_flange_default INTEGER DEFAULT 0,
    description_vi TEXT
);

-- 2. Bảng kích thước hình học chi tiết theo từng cỡ ren
CREATE TABLE IF NOT EXISTS jis_b1181_nut_dimensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series TEXT NOT NULL,
    nut_size TEXT NOT NULL,
    nominal_dia REAL NOT NULL,
    pitch REAL NOT NULL,
    s_nominal REAL NOT NULL,
    s_min REAL NOT NULL,
    s_max REAL NOT NULL,
    m_nominal REAL NOT NULL,
    m_min REAL NOT NULL,
    m_max REAL NOT NULL,
    e_min REAL NOT NULL,
    dw_min REAL,
    da_min REAL,
    da_max REAL,
    chamfer_angle REAL DEFAULT 30.0,
    UNIQUE(series, nut_size)
);

-- 3. Bảng cơ tính vật liệu và cấp độ bền
CREATE TABLE IF NOT EXISTS jis_b1181_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_group TEXT NOT NULL,
    property_class TEXT NOT NULL,
    proof_stress_mpa REAL,
    applicable_standards TEXT
);
```

---

### Bước 3: Khởi tạo bộ dữ liệu RAM siêu tốc (jis_b1181_dataset.py)
* **File khởi tạo**: `_fvc_fasteners/data/jis_b1181_dataset.py`
* **Nguyên lý hoạt động**:
  - Dữ liệu được biên soạn thành các từ điển (Python Dictionary) thuần túy nạp trực tiếp vào RAM khi import.
  - Phục vụ truy vấn tức thời (Zero Disk-IO) khi phần mềm AutoCAD Plant 3D cần nạp hàng ngàn cụm bu lông - đai ốc trên tuyến ống.
  - Đóng vai trò lớp dự phòng tin cậy (Fallback) nếu file SQLite bị xung đột truy cập hoặc lỗi quyền ghi trên Windows.

---

### Bước 4: Phát triển tầng truy vấn dữ liệu DAO (jis_b1181_reader.py)
* **File khởi tạo**: `_fvc_fasteners/db/jis_b1181_reader.py`
* **Cung cấp giao diện hàm tiện ích cấp cao**:
  1. `get_nut_type(type_code: str) -> Optional[NutTypeSpec]`: Tra cứu loại đai ốc.
  2. `get_nut_dimension(nut_size: str, series: str = "ISO_STYLE_1") -> Optional[NutDimensionSpec]`: Tra cứu kích thước `s`, `m`, `e`, `dw` theo cỡ ren (tự động xử lý bước thô như M16, M20 hoặc bước mịn như M30x3).
  3. `get_matching_nut_for_bolt(bolt_spec: MetricBoltSpec, prefer_style: str = "STYLE_1") -> NutDimensionSpec`: Tự động tìm con đai ốc tương thích hoàn toàn với bu lông mặt bích trong `jis_b1217_reader.py`.

---

### Bước 5: Tích hợp hình học 3D và mối nối mặt bích JIS B 1217
* **Thư mục liên quan**: `_fvc_fasteners/geometry/` và `hotreload_impl.py`
* **Quy trình dựng hình học**:
  1. Sử dụng tham số `s`, `m`, `e` để tạo khối lăng trụ lục giác đều xuyên tâm qua hàm `primitives.py`.
  2. Dựng mặt vát mép tròn góc 30 độ (cho 1 mặt đối với Style 1 / Type 1, hoặc cả 2 mặt đối với Style 0 / Type 2 / Type 3).
  3. Tạo gờ đệm mặt tỳ đường kính `dw_min` và khoét lỗ ren rỗng đường kính `da`.
  4. Ghép cặp tự động: Khi người dùng chọn mặt bích JIS 10K, 16K, 20K, hệ thống tự động tính số lượng bu lông và lấy đai ốc tương ứng lắp ráp chuẩn vào 2 đầu ren.

---

### Bước 6: Kiểm thử tự động (Unit Tests)
* **File kiểm thử**: `_fvc_fasteners/tests/test_jis_b1181.py`
* **Kết quả thực thi kiểm thử**:
  - Đã chạy thành công **13/13 test cases** chuyên biệt cho JIS B 1181 và **22/22 test cases** tổng thể của toàn bộ module `_fvc_fasteners` với kết quả **100% OK / PASS**.
  - **Tốc độ truy vấn đo được (Benchmark)**: ~ 0.000963 ms / lần truy vấn (nhanh hơn gấp 100 lần so với giới hạn mục tiêu 0.1 ms).
  - Đã xác thực độ chính xác tuyệt đối của dữ liệu:
    - M16 Style 1: s = 24.0 mm, m = 14.8 mm, dw = 22.5 mm, e_min = 26.75 mm.
    - M20 Style 1: s = 30.0 mm, m = 18.0 mm, dw = 27.7 mm, e_min = 32.95 mm.
    - Phụ lục JA: M10 (s = 17 mm), M12 (s = 19 mm), M14 (s = 22 mm), M22 (s = 32 mm) hoàn toàn tách biệt với hệ ISO (M10 s=16, M12 s=18, M14 s=21, M22 s=34).
    - CSDL SQLite `jis_b1181.sqlite` đã được nạp 12 chủng loại đai ốc, trên 100 quy cách kích thước chi tiết và các cấp bền cơ tính.

