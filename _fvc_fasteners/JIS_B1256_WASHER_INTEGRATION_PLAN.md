# KẾ HOẠCH TÍCH HỢP VÒNG ĐỆM PHẲNG THEO TIÊU CHUẨN JIS B 1256 : 2008

> **Tài liệu quy chuẩn tham chiếu**: [JIS B 1256 : 2008 (平座金 - Plain washers - Vòng đệm phẳng)](https://kikakurui.com/b1/B1256-2008-01.html)  
> **Module đích trong dự án**: `_fvc_fasteners`  
> **Ngôn ngữ thực hiện**: Python 3, SQLite3, AutoCAD Plant 3D Primitives Engine  

---

## MỤC LỤC
1. [Tổng quan về quy chuẩn JIS B 1256:2008](#1-tổng-quan-về-quy-chuẩn-jis-b-12562008)
2. [Hệ thống phân loại toàn bộ các loại vòng đệm](#2-hệ-thống-phân-loại-toàn-bộ-các-loại-vòng-đệm)
   - [Sơ đồ phân nhánh chủng loại vòng đệm](#sơ-đồ-phân-nhánh-chủng-loại-vòng-đệm)
   - [Đặc điểm 7 dòng vòng đệm phẳng theo thân tiêu chuẩn ISO](#đặc-điểm-7-dòng-vòng-đệm-phẳng-theo-thân-tiêu-chuẩn-iso)
   - [Vòng đệm vuông theo Phụ lục JA](#vòng-đệm-vuông-theo-phụ-lục-ja)
   - [Hệ truyền thống Nhật Bản (JIS B 1250: ミガキ丸 và 並丸)](#hệ-truyền-thống-nhật-bản-jis-b-1250-ミガキ丸-và-並丸)
   - [Cấp độ cứng và cơ tính vật liệu (100 HV, 200 HV, 300 HV)](#cấp-độ-cứng-và-cơ-tính-vật-liệu-100-hv-200-hv-300-hv)
3. [Hệ thống bảng đối chiếu kỹ thuật chuẩn Excel Grid](#3-hệ-thống-bảng-đối-chiếu-kỹ-thuật-chuẩn-excel-grid)
   - [Bảng 1: Phân loại 7 chủng loại vòng đệm phẳng ISO](#bảng-1-phân-loại-7-chủng-loại-vòng-đệm-phẳng-iso)
   - [Bảng 2: Thông số kích thước hình học chi tiết (d1, d2, h từ M3 đến M64)](#bảng-2-thông-số-kích-thước-hình-học-chi-tiết-d1-d2-h-từ-m3-đến-m64)
   - [Bảng 3: Đối chiếu hệ truyền thống Nhật JIS B 1250 và Phụ lục JA](#bảng-3-đối-chiếu-hệ-truyền-thống-nhật-jis-b-1250-và-phụ-lục-ja)
4. [Kế hoạch cập nhật cơ sở dữ liệu và hệ thống mã nguồn](#4-kế-hoạch-cập-nhật-cơ-sở-dữ-liệu-và-hệ-thống-mã-nguồn)
   - [Bước 1: Mô hình hóa dữ liệu (Data Modeling)](#bước-1-mô-hình-hóa-dữ-liệu-data-modeling)
   - [Bước 2: Thiết kế cơ sở dữ liệu SQLite (jis_b1256.sqlite)](#bước-2-thiết-kế-cơ-sở-dữ-liệu-sqlite-jis_b1256sqlite)
   - [Bước 3: Khởi tạo bộ dữ liệu RAM siêu tốc (jis_b1256_dataset.py)](#bước-3-khởi-tạo-bộ-dữ-liệu-ram-siêu-tốc-jis_b1256_datasetpy)
   - [Bước 4: Phát triển tầng truy vấn dữ liệu DAO (jis_b1256_reader.py)](#bước-4-phát-triển-tầng-truy-vấn-dữ-liệu-dao-jis_b1256_readerpy)
   - [Bước 5: Nâng cấp hình học 3D Solid và cụm bu lông bích](#bước-5-nâng-cấp-hình-học-3d-solid-và-cụm-bu-lông-bích)
   - [Bước 6: Kiểm thử tự động (Unit Tests & Performance Benchmark)](#bước-6-kiểm-thử-tự-động-unit-tests--performance-benchmark)

---

## 1. TỔNG QUAN VỀ QUY CHUẨN JIS B 1256:2008

Tiêu chuẩn **JIS B 1256:2008** quy định kích thước hình học, dung sai, độ cứng và đặc tính kỹ thuật của các loại **vòng đệm phẳng (Plain washers - 平座金)** dùng chung cho bu lông, vít và đai ốc làm từ thép cacbon, thép không gỉ (Inox) và kim loại màu.

### Bối cảnh và cấu trúc tiêu chuẩn:
1. **Hài hòa kỹ thuật với 7 tiêu chuẩn quốc tế ISO**:
   * Phiên bản JIS B 1256:2008 được biên dịch và đồng bộ trực tiếp từ **7 tiêu chuẩn ISO phiên bản 2000**:
     * **ISO 7089:2000**: Vòng đệm phẳng thông thường, cấp A (Normal series - Product grade A).
     * **ISO 7090:2000**: Vòng đệm phẳng thông thường vát mép, cấp A (Normal series chamfered - Product grade A).
     * **ISO 7091:2000**: Vòng đệm phẳng thông thường, cấp C (Normal series - Product grade C).
     * **ISO 7092:2000**: Vòng đệm phẳng vành nhỏ, cấp A (Small series - Product grade A).
     * **ISO 7093-1:2000**: Vòng đệm phẳng vành lớn, cấp A (Large series - Product grade A).
     * **ISO 7093-2:2000**: Vòng đệm phẳng vành lớn, cấp C (Large series - Product grade C).
     * **ISO 7094:2000**: Vòng đệm phẳng vành cực lớn, cấp C (Extra large series - Product grade C).
2. **Tách nhánh tiêu chuẩn truyền thống Nhật Bản**:
   * Tiêu chuẩn JIS B 1256:1998 trước đây gộp cả vòng đệm hệ ISO và vòng đệm truyền thống Nhật Bản. Đến bản 2008, phần vòng đệm truyền thống Nhật Bản (loại mài bóng - ミガキ丸 và loại thường - 並丸) được tách riêng thành tiêu chuẩn **JIS B 1250**, trong khi JIS B 1256 tập trung chuẩn hóa hoàn toàn theo hệ ISO.
3. **Phụ lục JA (Tham khảo - 角座金)**:
   * Giữ lại quy cách **vòng đệm vuông (Square washers)** từ JIS B 1256:1978 chuyên dùng cho kết cấu gỗ, kênh dầm thép chữ U, chữ I.

---

## 2. HỆ THỐNG PHÂN LOẠI TOÀN BỘ CÁC LOẠI VÒNG ĐỆM

### Sơ đồ phân nhánh chủng loại vòng đệm

```
JIS B 1256:2008 (Hệ thống phân loại Vòng đệm)
├── Nhóm I: Thân tiêu chuẩn chính (Hài hòa 7 tiêu chuẩn ISO)
│   ├── Dòng vành nhỏ (Small Series - d2 ≈ 1.6d ~ 1.8d)
│   │   └── 1. Vòng đệm nhỏ Cấp A (ISO 7092) [Dùng cho bu lông chìm Socket Cap]
│   ├── Dòng vành tiêu chuẩn (Normal Series - d2 ≈ 2.0d)
│   │   ├── 2. Vòng đệm thường Cấp A (ISO 7089) [MẶC ĐỊNH CHO MẶT BÍCH]
│   │   ├── 3. Vòng đệm thường vát mép Cấp A (ISO 7090) [Bu lông cường độ cao]
│   │   └── 4. Vòng đệm thường Cấp C (ISO 7091) [Cơ khí thô, giá rẻ]
│   ├── Dòng vành lớn (Large Series - d2 ≈ 3.0d)
│   │   ├── 5. Vòng đệm vành lớn Cấp A (ISO 7093-1) [Tải phân bố đều]
│   │   └── 6. Vòng đệm vành lớn Cấp C (ISO 7093-2) [Tấm mỏng, lỗ rộng]
│   └── Dòng vành cực lớn (Extra Large Series - d2 ≈ 3.5d ~ 4.0d)
│       └── 7. Vòng đệm vành cực lớn Cấp C (ISO 7094) [Kết cấu gỗ, xốp]
│
├── Nhóm II: Vòng đệm vuông theo Phụ lục JA (角座金)
│   ├── 8. Vòng đệm vuông phẳng (Square Flat Washers - Dùng cho gỗ)
│   └── 9. Vòng đệm vuông vát nghiêng (Square Taper Washers - Dùng cho dầm I, U)
│
└── Nhóm III: Hệ truyền thống Nhật Bản liên quan (JIS B 1250)
    ├── 10. Vòng đệm tròn mài bóng (ミガキ丸 - Polished Round Washer)
    └── 11. Vòng đệm tròn thông dụng (並丸 - Commercial Round Washer)
```

---

### Đặc điểm 7 dòng vòng đệm phẳng theo thân tiêu chuẩn ISO

1. **Vòng đệm nhỏ Cấp A (Small series - ISO 7092)**:
   - Đường kính ngoài d2 nhỏ gọn nhất trong các dòng đệm phẳng (d2 ≈ 1.6d ~ 1.8d).
   - Ứng dụng: Lắp vừa khít vào lỗ khoét bậc của **bu lông lục giác chìm (Socket head cap screw)** hoặc vít đầu trụ (Cheese head screw).
2. **Vòng đệm thường Cấp A (Normal series - ISO 7089)**:
   - Đường kính ngoài tiêu chuẩn d2 ≈ 2.0d, bề mặt phẳng nhẵn, dung sai chế tạo tinh (Cấp A).
   - Ứng dụng: **Vòng đệm mặc định chuẩn cho các mối nối mặt bích đường ống**, liên kết bu lông - đai ốc cấp bền 8.8 và Inox A2/A4.
3. **Vòng đệm thường vát mép Cấp A (Normal series chamfered - ISO 7090)**:
   - Kích thước cơ bản tương đương ISO 7089 nhưng có vát mép ngoài góc 30 đến 45 độ (mặt vát quay về phía đầu bu lông).
   - Ứng dụng: Dùng cho mối nối bu lông cường độ cao cấp bền 10.9; mặt vát mép giúp tránh hiện tượng cấn vào bán kính bo góc chân cổ bu lông (r).
4. **Vòng đệm thường Cấp C (Normal series - ISO 7091)**:
   - Kích thước tương tự ISO 7089 nhưng chế tạo dập thô (Cấp C, dung sai rộng), độ cứng 100 HV.
   - Ứng dụng: Kết cấu thép thông thường, phụ kiện cơ khí dân dụng dùng với bu lông cấp bền ≤ 6.8, chi phí tiết kiệm.
5. **Vòng đệm vành lớn Cấp A (Large series - ISO 7093-1)**:
   - Đường kính ngoài lớn d2 ≈ 3.0d, diện tích mặt tỳ gấp hơn 2.2 lần so với vòng đệm thường.
   - Ứng dụng: Giảm áp lực bề mặt tỳ lên các vật liệu mềm (nhôm, hợp kim đồng, tấm composite), hoặc che phủ các lỗ xỏ bu lông bị gia công quá rộng/bị khoét rãnh dài (slotted hole).
6. **Vòng đệm vành lớn Cấp C (Large series - ISO 7093-2)**:
   - Kích thước ngoài d2 ≈ 3.0d nhưng chế tạo dập thô cấp C, độ cứng 100 HV.
   - Ứng dụng: Tấm thép mỏng, vỏ máy nông nghiệp, thiết bị công nghiệp thô.
7. **Vòng đệm vành cực lớn Cấp C (Extra large series - ISO 7094)**:
   - Đường kính ngoài cực lớn d2 ≈ 3.5d ~ 4.0d, chiều dày h tăng cường từ 2 mm đến 8 mm.
   - Ứng dụng: Chuyên dùng cho ngành kết cấu gỗ (Timber constructions), liên kết xà gồ gỗ nhằm triệt tiêu hiện tượng bu lông chìm lún làm dập nát thớ gỗ.

---

### Vòng đệm vuông theo Phụ lục JA

- **Vòng đệm vuông phẳng (角座金)**: Dạng tấm vuông kích thước cạnh a x a, có lỗ tròn d1 ở tâm, chiều dày t từ 2.0 mm đến 6.0 mm. Thường dùng trong liên kết dầm gỗ, giằng cột nhà xưởng và đường ray.
- **Vòng đệm vuông vát nghiêng (テーパ座金 - Taper washer)**: Có mặt nghiêng góc 5 độ hoặc 8 độ dùng để đệm phẳng khi bắt bu lông xuyên qua cánh chữ I hoặc cánh chữ U.

---

### Hệ truyền thống Nhật Bản (JIS B 1250: ミガキ丸 và 並丸)

Trong các bản vẽ và máy móc xuất xứ nội địa Nhật Bản, các kỹ sư thường bắt gặp 2 định danh:
1. **ミガキ丸 (Vòng đệm mài bóng / Polished round)**: Đường kính ngoài nhỏ gọn, bề mặt nhẵn bóng, dung sai chính xác (tương đương cấp A).
2. **並丸 (Vòng đệm thông dụng / Commercial round)**: Đường kính ngoài rộng hơn, bề dày nhỉnh hơn, chế tạo đại trà.

---

### Cấp độ cứng và cơ tính vật liệu (100 HV, 200 HV, 300 HV)

Tiêu chuẩn JIS B 1256:2008 phân định cơ tính của vòng đệm thép theo 3 cấp độ cứng Vickers (HV):

| Cấp độ cứng | Dải độ cứng Vickers (HV) | Xử lý nhiệt | Bu lông tương thích | Ứng dụng tiêu biểu |
| :-: | :-: | :--- | :--- | :--- |
| **100 HV** | 100 ~ 200 HV | Thép cacbon không tôi (thép mềm) | Cấp bền ≤ 6.8 (4.6, 4.8, 5.8, 6.8) | Dùng cho đệm Cấp C (ISO 7091, ISO 7093-2, ISO 7094) |
| **200 HV** | 200 ~ 300 HV | Thép cacbon khử ứng suất / ram nhẹ | Cấp bền ≤ 8.8 (8.8, đai ốc cấp 8, inox A2/A4) | **Mặc định chuẩn cho mặt bích đường ống và cơ khí chính xác** |
| **300 HV** | 300 ~ 400 HV | Thép cacbon hoặc hợp kim tôi & ram | Cấp bền 10.9 (hoặc bu lông chìm cường độ cao) | Mối ghép bu lông cường độ cao, chịu tải trọng uốn/giật lớn |

* **Vật liệu thép không gỉ (Inox)**: Nhóm Austenitic A2 (SUS304) và A4 (SUS316), độ cứng tối thiểu đạt 200 HV.
* **Vật liệu kim loại màu**: Đồng thau (Brass - CuZn), Hợp kim nhôm (Al).

---

## 3. HỆ THỐNG BẢNG ĐỐI CHIẾU KỸ THUẬT CHUẨN EXCEL GRID

> 📊 **Bản bảng tính Excel kỹ thuật đã được tạo lập**:  
> Dữ liệu phân loại chi tiết đã được xuất thành bảng tính Excel chuyên nghiệp có phân màu, kẻ khung viền, tự động căn chỉnh độ rộng cột và gán bộ lọc tại:
> * File nội bộ module: [JIS_B1256_WASHER_SPECIFICATION.xlsx](file:///c:/Users/95053/Desktop/Hello%20World/Python-Autocad-Plant-3D/_fvc_fasteners/JIS_B1256_WASHER_SPECIFICATION.xlsx)
> * Thư mục Catalog dự án: [JIS_B1256_WASHER_SPECIFICATION.xlsx](file:///c:/Users/95053/Desktop/Hello%20World/Python-Autocad-Plant-3D/Excel%20Catalog/JIS_B1256_WASHER_SPECIFICATION.xlsx)

---

### BẢNG 1: PHÂN LOẠI 7 CHỦNG LOẠI VÒNG ĐỆM PHẲNG ISO

| STT | Nhóm kích thước | Tiêu chuẩn ISO | Tên tiếng Nhật chuẩn | Tên tiếng Anh kỹ thuật | Cấp SP | Cấp độ cứng (HV) | Tỷ lệ ngoài d2/d | Đặc điểm hình học vát mép | Dải cỡ ren D | Ứng dụng kỹ thuật chính |
| :-: | :--- | :-: | :--- | :--- | :-: | :-: | :-: | :--- | :-: | :--- |
| **1** | Small series (小形) | **ISO 7092** | 平座金・小形−部品等級A | Plain washers Small series Grade A | Cấp A | 200 HV / 300 HV | d2 ≈ 1.6d ~ 1.8d | Vành ngoài nhỏ gọn, phẳng không vát | M1.6 - M36 | Dùng cho bu lông chìm lục giác Socket Cap, vít đầu trụ nhỏ |
| **2** | Normal series (並形) | **ISO 7089** | 平座金・並形−部品等級A | Plain washers Normal series Grade A | Cấp A | 200 HV / 300 HV | d2 ≈ 2.0d | Vành tiêu chuẩn, phẳng không vát, dung sai tinh H13/h14 | M1.6 - M64 | **Mặc định chuẩn cho mối nối mặt bích đường ống** |
| **3** | Normal chamfered (並形面取り) | **ISO 7090** | 平座金・並形面取り−部品等級A | Plain washers Chamfered Normal Grade A | Cấp A | 200 HV / 300 HV | d2 ≈ 2.0d | Vành tiêu chuẩn, vát mép ngoài góc 30 - 45 độ | M5 - M64 | Dùng cho bu lông cấp 10.9, tránh cấn góc lượn cổ bu lông |
| **4** | Normal series (並形 Cấp C) | **ISO 7091** | 平座金・並形−部品等級C | Plain washers Normal series Grade C | Cấp C | 100 HV | d2 ≈ 2.0d | Vành tiêu chuẩn, dập phẳng thô H14/h16 | M1.6 - M64 | Kết cấu thép dân dụng, bu lông cấp bền <= 6.8 |
| **5** | Large series (大形) | **ISO 7093-1** | 平座金・大形−部品等級A | Plain washers Large series Part 1 Grade A | Cấp A | 200 HV / 300 HV | d2 ≈ 3.0d | Vành ngoài lớn, diện tích tỳ gấp 2.2 lần đệm thường | M3 - M36 | Phân bố đều lực siết lên bề mặt mềm, lỗ khoét rãnh dài |
| **6** | Large series (大形 Cấp C) | **ISO 7093-2** | 平座金・大形−部品等級C | Plain washers Large series Part 2 Grade C | Cấp C | 100 HV | d2 ≈ 3.0d | Vành ngoài lớn gia công dập phẳng thô | M3 - M36 | Kết cấu thép tấm mỏng, vỏ máy cơ khí thô |
| **7** | Extra large series (特大形) | **ISO 7094** | 平座金・特大形−部品等級C | Plain washers Extra large series Grade C | Cấp C | 100 HV | d2 ≈ 3.5d ~ 4.0d | Vành ngoài cực lớn, bề dày tăng cường (2 - 8 mm) | M5 - M36 | Chuyên dụng cho kết cấu gỗ, vật liệu composite xốp |

---

### BẢNG 2: THÔNG SỐ KÍCH THƯỚC HÌNH HỌC CHI TIẾT (d1, d2, h TỪ M3 ĐẾN M64)

*Đơn vị đo: milimet (mm)*

| Cỡ ren (D) | Đường kính trong d1 | d2 Small (ISO 7092) | h Small | d2 Normal (ISO 7089/90/91) | h Normal | d2 Large (ISO 7093) | h Large | d2 Extra Large (ISO 7094) | h Extra Large |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **M3** | 3.2 | 6.0 | 0.5 | 7.0 | 0.5 | 9.0 | 0.8 | - | - |
| **M4** | 4.3 | 8.0 | 0.5 | 9.0 | 0.8 | 12.0 | 1.0 | - | - |
| **M5** | 5.3 | 9.0 | 1.0 | 10.0 | 1.0 | 15.0 | 1.2 | 18.0 | 2.0 |
| **M6** | 6.4 | 11.0 | 1.6 | 12.0 | 1.6 | 18.0 | 1.6 | 22.0 | 2.0 |
| **M8** | 8.4 | 15.0 | 1.6 | 16.0 | 1.6 | 24.0 | 2.0 | 28.0 | 3.0 |
| **M10** | 10.5 | 18.0 | 1.6 | 20.0 | 2.0 | 30.0 | 2.5 | 34.0 | 3.0 |
| **M12** | 13.0 | 20.0 | 2.0 | 24.0 | 2.5 | 37.0 | 3.0 | 44.0 | 4.0 |
| **M14** | 15.0 | 24.0 | 2.5 | 28.0 | 2.5 | 44.0 | 3.0 | 50.0 | 4.0 |
| **M16** | 17.0 | 28.0 | 2.5 | **30.0** | **3.0** | 50.0 | 3.0 | 56.0 | 5.0 |
| **M18** | 19.0 | 30.0 | 2.5 | 34.0 | 3.0 | 56.0 | 4.0 | 60.0 | 5.0 |
| **M20** | 21.0 | 34.0 | 3.0 | **37.0** | **3.0** | 60.0 | 4.0 | 72.0 | 6.0 |
| **M22** | 23.0 | 37.0 | 3.0 | 39.0 | 3.0 | 66.0 | 5.0 | 80.0 | 6.0 |
| **M24** | 25.0 | 39.0 | 4.0 | **44.0** | **4.0** | 72.0 | 5.0 | 85.0 | 6.0 |
| **M27** | 28.0 | 44.0 | 4.0 | 50.0 | 4.0 | 85.0 | 6.0 | 98.0 | 6.0 |
| **M30** | 31.0 | 50.0 | 4.0 | **56.0** | **4.0** | 92.0 | 6.0 | 105.0 | 6.0 |
| **M33** | 34.0 | 56.0 | 5.0 | 60.0 | 5.0 | 105.0 | 6.0 | 115.0 | 8.0 |
| **M36** | 37.0 | 60.0 | 5.0 | **66.0** | **5.0** | 110.0 | 8.0 | 125.0 | 8.0 |
| **M42** | 43.0 | - | - | **78.0** | **7.0** | - | - | - | - |
| **M48** | 50.0 | - | - | **92.0** | **8.0** | - | - | - | - |
| **M56** | 58.0 | - | - | **105.0** | **9.0** | - | - | - | - |
| **M64** | 66.0 | - | - | **115.0** | **9.0** | - | - | - | - |

---

### BẢNG 3: ĐỐI CHIẾU HỆ TRUYỀN THỐNG NHẬT JIS B 1250 VÀ PHỤ LỤC JA

| Cỡ ren | Lỗ d1 | d2 Polished (ミガキ丸) | h Polished | d2 Commercial (並丸) | h Commercial | Cạnh đệm vuông a (Phụ lục JA) | Lỗ đệm vuông d1 | Dày đệm vuông t |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **M6** | 6.5 | 11.5 | 1.2 | 13.0 | 1.0 | 20.0 | 7.0 | 2.0 |
| **M8** | 8.5 | 15.5 | 1.6 | 18.0 | 1.6 | 26.0 | 9.0 | 2.3 |
| **M10** | 10.5 | 18.5 | 1.6 | 22.0 | 1.6 | 32.0 | 11.0 | 2.3 |
| **M12** | 13.0 | 21.0 | 2.0 | 26.0 | 2.3 | 40.0 | 13.5 | 3.2 |
| **M16** | 17.0 | 28.0 | 2.6 | 32.0 | 3.2 | 52.0 | 17.5 | 4.5 |
| **M20** | 21.0 | 34.0 | 3.2 | 40.0 | 3.2 | 68.0 | 22.0 | 6.0 |
| **M22** | 23.0 | 39.0 | 3.2 | 44.0 | 3.2 | 74.0 | 24.0 | 6.0 |
| **M24** | 26.0 | 44.0 | 4.0 | 48.0 | 4.0 | 80.0 | 26.0 | 6.0 |

---

## 4. KẾ HOẠCH CẬP NHẬT CƠ SỞ DỮ LIỆU VÀ HỆ THỐNG MÃ NGUỒN

### Bước 1: Mô hình hóa dữ liệu (Data Modeling)
* **File khởi tạo**: `_fvc_fasteners/models/jis_b1256_specs.py`
* **Nội dung thiết kế**:
  - `WasherDimensionSpec`: Kích thước hình học đai ốc và vòng đệm:
    - `d1`: Đường kính lỗ trong (mm).
    - `d2`: Đường kính ngoài (mm).
    - `h`: Chiều dày danh nghĩa (mm).
    - `chamfer_angle_deg`: Góc vát mép ngoài (30 - 45 độ đối với ISO 7090, 0 độ đối với phẳng).
    - `series`: Dòng series ('ISO_NORMAL_A', 'ISO_NORMAL_CHAMFERED_A', 'ISO_NORMAL_C', 'ISO_SMALL_A', 'ISO_LARGE_A', 'ISO_EXTRA_LARGE_C', 'ANNEX_JA_SQUARE').
  - `WasherTypeSpec`: Định danh 7 chủng loại ISO + 2 loại Phụ lục JA/JIS cũ.
  - `PlainWasherSpec`: Thông số đối tượng hoàn chỉnh phục vụ dựng mô hình 3D Solid và lập bảng kê BOM.
* **Cập nhật export**: Đăng ký các lớp mới vào `_fvc_fasteners/models/__init__.py`.

---

### Bước 2: Thiết kế cơ sở dữ liệu SQLite (jis_b1256.sqlite)
* **File cơ sở dữ liệu**: `_fvc_fasteners/data/jis_b1256.sqlite`
* **File script khởi tạo & nạp dữ liệu**: `_fvc_fasteners/data/jis_b1256_seed.py`
* **Lược đồ CSDL gồm 3 bảng quan hệ**:

```sql
-- 1. Bảng danh mục chủng loại vòng đệm
CREATE TABLE IF NOT EXISTS jis_b1256_washer_types (
    type_id INTEGER PRIMARY KEY,
    type_code TEXT UNIQUE NOT NULL,
    type_name_ja TEXT NOT NULL,
    type_name_en TEXT NOT NULL,
    iso_standard TEXT,
    washer_series TEXT NOT NULL,
    product_grade TEXT NOT NULL,
    is_flange_default INTEGER DEFAULT 0,
    description_vi TEXT
);

-- 2. Bảng kích thước hình học chi tiết từng cỡ ren
CREATE TABLE IF NOT EXISTS jis_b1256_dimensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series TEXT NOT NULL,
    bolt_size TEXT NOT NULL,
    nominal_dia REAL NOT NULL,
    d1_nominal REAL NOT NULL,
    d1_min REAL NOT NULL,
    d1_max REAL NOT NULL,
    d2_nominal REAL NOT NULL,
    d2_min REAL NOT NULL,
    d2_max REAL NOT NULL,
    h_nominal REAL NOT NULL,
    h_min REAL NOT NULL,
    h_max REAL NOT NULL,
    chamfer_angle_deg REAL DEFAULT 0.0,
    UNIQUE(series, bolt_size)
);

-- 3. Bảng cơ tính và cấp độ cứng
CREATE TABLE IF NOT EXISTS jis_b1256_hardness_specs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hardness_class TEXT NOT NULL,
    min_hv REAL NOT NULL,
    max_hv REAL NOT NULL,
    applicable_bolts TEXT,
    description_vi TEXT
);
```

---

### Bước 3: Khởi tạo bộ dữ liệu RAM siêu tốc (jis_b1256_dataset.py)
* **File khởi tạo**: `_fvc_fasteners/data/jis_b1256_dataset.py`
* **Nguyên lý hoạt động**:
  - Dữ liệu được biên soạn thành cấu trúc Dictionary thuần Python, nạp ngay khi khởi động ứng dụng.
  - Phục vụ truy xuất tức thời (Zero Disk-IO) khi lắp hàng ngàn vòng đệm trên toàn bộ tuyến ống của AutoCAD Plant 3D.
  - Đóng vai trò lớp dự phòng tin cậy (Fallback) khi file SQLite gặp lỗi quyền ghi hoặc bị khóa trên hệ điều hành Windows.

---

### Bước 4: Phát triển tầng truy vấn dữ liệu DAO (jis_b1256_reader.py)
* **File khởi tạo**: `_fvc_fasteners/db/jis_b1256_reader.py`
* **Cung cấp giao diện hàm tiện ích cấp cao**:
  1. `get_washer_type(type_code: str) -> Optional[WasherTypeSpec]`: Tra cứu loại vòng đệm.
  2. `get_washer_dimension(bolt_size: str, series: str = "ISO_NORMAL_A") -> Optional[WasherDimensionSpec]`: Tra cứu kích thước d1, d2, h theo cỡ bu lông và series.
  3. `get_matching_washer_for_bolt(bolt_size: str, prefer_series: str = "ISO_NORMAL_A") -> WasherDimensionSpec`: Tự động tìm vòng đệm tương thích với cỡ bu lông mặt bích JIS B 1217.
  4. `list_available_washer_types() -> List[WasherTypeSpec]`: Liệt kê các loại vòng đệm hỗ trợ.

---

### Bước 5: Nâng cấp hình học 3D Solid và cụm bu lông bích
* **Thư mục liên quan**: `_fvc_fasteners/geometry/` và `hotreload_impl.py`
* **Quy trình dựng hình học**:
  1. Tạo module dựng hình: `_fvc_fasteners/geometry/washer.py` với hàm `PlainWasher(s, bolt_size, series)`.
  2. Dựng hình học chính xác bằng các hàm nguyên sinh (`primitives.py`):
     - Tạo khối trụ tròn đường kính ngoài d2, chiều cao h.
     - Khoét rỗng lỗ tâm đường kính d1.
     - Tạo góc vát mép 30 đến 45 độ nếu chọn series vát mép (ISO 7090).
  3. Tích hợp tự động vào cụm bu lông mặt bích:
     - Tự động gắn vòng đệm dưới mũ bu lông và dưới đai ốc khi người dùng kích hoạt tùy chọn `has_washers=True` trên mặt bích JIS.

---

### Bước 6: Kiểm thử tự động (Unit Tests & Performance Benchmark)
* **File kiểm thử**: `_fvc_fasteners/tests/test_jis_b1256.py`
* **Nội dung kiểm tra**:
  1. Kiểm tra đủ 7 chủng loại vòng đệm ISO và các phân loại truyền thống.
  2. Kiểm tra độ chuẩn xác kích thước:
     - M16 Normal A (ISO 7089): d1 = 17.0 mm, d2 = 30.0 mm, h = 3.0 mm.
     - M20 Normal A (ISO 7089): d1 = 21.0 mm, d2 = 37.0 mm, h = 3.0 mm.
     - M16 Small A (ISO 7092): d1 = 17.0 mm, d2 = 28.0 mm, h = 2.5 mm.
     - M16 Large A (ISO 7093-1): d1 = 17.0 mm, d2 = 50.0 mm, h = 3.0 mm.
  3. Đo lường tốc độ truy vấn bộ nhớ RAM đảm bảo dưới 0.05 ms.
  4. Kiểm tra tính toàn vẹn của tệp cơ sở dữ liệu SQLite `jis_b1256.sqlite`.
