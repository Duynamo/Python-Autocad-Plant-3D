# KẾ HOẠCH TÍCH HỢP GIOĂNG ĐỆM MẶT BÍCH THEO TIÊU CHUẨN JIS B 2404 : 2018

> **Tài liệu quy chuẩn tham chiếu**: [JIS B 2404 : 2018 (管フランジ用ガスケットの寸法 - Dimensions of gaskets for use with pipe flanges)](https://kikakurui.com/b2/B2404-2018-01.html)  
> **Các tiêu chuẩn mặt bích áp dụng**: JIS B 2220 (Thép), JIS B 2239 (Gang), JIS B 2240 (Đồng), JIS B 2241 (Nhôm)  
> **Module triển khai**: `_fvc_fasteners` (hoặc `_fvc_gaskets`)  
> **Ngôn ngữ thực hiện**: Python 3, SQLite3, AutoCAD Plant 3D Primitives Engine  

---

## MỤC LỤC
1. [Tổng quan về tiêu chuẩn JIS B 2404:2018](#1-tổng-quan-về-tiêu-chuẩn-jis-b-24042018)
2. [Hệ thống phân loại toàn bộ các loại Gasket trong tiêu chuẩn](#2-hệ-thống-phân-loại-toàn-bộ-các-loại-gasket-trong-tiêu-chuẩn)
   - [Sơ đồ phân nhánh 3 họ Gasket chính](#sơ-đồ-phân-nhánh-3-họ-gasket-chính)
   - [Họ 1: Gioăng tấm đệm (シートガスケット - Sheet Gaskets)](#họ-1-gioăng-tấm-đệm-シートガスケット---sheet-gaskets)
   - [Họ 2: Gioăng bọc màng PTFE (ふっ素樹脂ジャケットガスケット - PTFE Jacketed Gaskets)](#họ-2-gioăng-bọc-màng-ptfe-ふっ素樹脂ジャケットガスケット---ptfe-jacketed-gaskets)
   - [Họ 3: Gioăng kim loại quấn xoắn (うず巻形ガスケット - Spiral Wound Gaskets)](#họ-3-gioăng-kim-loại-quấn-xoắn-うず巻形ガスケット---spiral-wound-gaskets)
   - [Phụ lục A: Gioăng cho mặt bích áp lực siêu thấp 2K](#phụ-lục-a-gioăng-cho-mặt-bích-áp-lực-siêu-thấp-2k)
3. [Bảng đối chiếu và so sánh toàn diện các loại Gasket JIS B 2404](#3-bảng-đối-chiếu-và-so-sánh-toàn-diện-các-loại-gasket-jis-b-2404)
   - [Bảng 1: Bảng so sánh tổng hợp 3 họ Gasket theo kết cấu và phạm vi áp dụng](#bảng-1-bảng-so-sánh-tổng-hợp-3-họ-gasket-theo-kết-cấu-và-phạm-vi-áp-dụng)
   - [Bảng 2: Ma trận phối ghép Gasket theo kiểu bề mặt bích (Facing Compatibility)](#bảng-2-ma-trận-phối-ghép-gasket-theo-kiểu-bề-mặt-bích-facing-compatibility)
   - [Bảng 3: Ma trận phối ghép Gasket theo vật liệu mặt bích (JIS B 2220 / 2239 / 2240 / 2241)](#bảng-3-ma-trận-phối-ghép-gasket-theo-vật-liệu-mặt-bích-jis-b-2220--2239--2240--2241)
   - [Bảng 4: Bảng tra cứu chiều dày danh định và dung sai kích thước](#bảng-4-bảng-tra-cứu-chiều-dày-danh-định-và-dung-sai-kích-thước)
4. [Kế hoạch cập nhật cơ sở dữ liệu và hệ thống mã nguồn](#4-kế-hoạch-cập-nhật-cơ-sở-dữ-liệu-và-hệ-thống-mã-nguồn)
   - [Bước 1: Mô hình hóa dữ liệu (Pydantic / Dataclasses Models)](#bước-1-mô-hình-hóa-dữ-liệu-pydantic--dataclasses-models)
   - [Bước 2: Thiết kế cơ sở dữ liệu SQLite (`jis_b2404.sqlite`)](#bước-2-thiết-kế-cơ-sở-dữ-liệu-sqlite-jis_b2404sqlite)
   - [Bước 3: Xây dựng bộ Dataset RAM thuần Python (`jis_b2404_dataset.py`)](#bước-3-xây-dựng-bộ-dataset-ram-thuần-python-jis_b2404_datasetpy)
   - [Bước 4: Phát triển tầng truy vấn thông minh DAO (`jis_b2404_reader.py`)](#bước-4-phát-triển-tầng-truy-vấn-thông-minh-dao-jis_b2404_readerpy)
   - [Bước 5: Nâng cấp hình học 3D Solid đa biến thể (`geometry/gasket.py`)](#bước-5-nâng-cấp-hình-học-3d-solid-đa-biến-thể-geometrygasketpy)
   - [Bước 6: Tích hợp vào Cụm kết nối mặt bích (`hotreload_impl.py`)](#bước-6-tích-hợp-vào-cụm-kết-nối-mặt-bích-hotreload_implpy)
   - [Bước 7: Kiểm thử tự động (Unit Tests & Performance Benchmarks)](#bước-7-kiểm-thử-tự-động-unit-tests--performance-benchmarks)

---

## 1. TỔNG QUAN VỀ TIÊU CHUẨN JIS B 2404:2018

Tiêu chuẩn **JIS B 2404 : 2018** mang tên chính thức là **管フランジ用ガスケットの寸法 (Dimensions of gaskets for use with pipe flanges)** do Hiệp hội Kỹ sư Cơ khí Nhật Bản (JSME) và Hiệp hội Tiêu chuẩn Nhật Bản (JSA) biên soạn, được Bộ Kinh tế, Thương mại và Công nghiệp Nhật Bản (METI) ban hành thay thế cho phiên bản trước đó là JIS B 2404:2006.

### Lịch sử và bối cảnh quy chuẩn:
1. **Nguồn gốc phát triển**: Tiêu chuẩn xuất phát từ năm 1967 ban đầu chỉ quy định cho gioăng kim loại quấn xoắn (*うず巻形ガスケット*). Đến năm 1999, tiêu chuẩn được cải cách toàn diện để tích hợp toàn bộ các dòng gioăng tấm đệm (Sheet gasket), gioăng bọc màng PTFE và gioăng quấn xoắn dùng chung cho toàn bộ ngành đường ống Nhật Bản.
2. **Hệ mặt bích tương thích**: Khác với hệ tiêu chuẩn quốc tế ISO (ISO 7005-1/2/3) hay ASME B16.5 / B16.20, JIS B 2404 được thiết kế chuẩn xác tuyệt đối để ăn khớp hoàn hảo với 4 bộ tiêu chuẩn mặt bích của Nhật Bản:
   * **JIS B 2220**: Mặt bích thép đường ống (Steel pipe flanges) - Phổ biến nhất.
   * **JIS B 2239**: Mặt bích gang đúc (Cast iron pipe flanges).
   * **JIS B 2240**: Mặt bích hợp kim đồng (Copper alloy pipe flanges).
   * **JIS B 2241**: Mặt bích hợp kim nhôm (Aluminium alloy pipe flanges).
3. **Phạm vi quy định**: Tiêu chuẩn quy định **kích thước hình học (Dimensions)**, **kiểu hình dáng (Shapes)** và **nguyên tắc phối ghép (Combinations)** giữa loại gioăng với bề mặt bích (Flange facings: Phẳng - FF, Gờ nổi - RF, Lồi lõm - MF, Rãnh - TG). Tiêu chuẩn không quy định thành phần công thức vật liệu chế tạo mà dẫn chiếu tới các tiêu chuẩn vật liệu chuyên ngành (như JIS R 3453 cho joint sheet, JIS K 6885 cho PTFE...).

---

## 2. HỆ THỐNG PHÂN LOẠI TOÀN BỘ CÁC LOẠI GASKET TRONG TIÊU CHUẨN

Theo **Bảng 1 (表1)** của JIS B 2404:2018, hệ thống gioăng được phân nhánh thành **3 họ chính**, bao gồm **14 phân nhánh vật liệu và kết cấu**:

### Sơ đồ phân nhánh 3 họ Gasket chính

```
JIS B 2404:2018 (Phân loại Gioăng mặt bích)
│
├── 1. シートガスケット (Họ I: Gioăng tấm đệm - Sheet Gaskets)
│   ├── Dạng hình học:
│   │   ├── 全面形ガスケット (Full-Face Gasket / FF): Có đục lỗ bu lông, che kín toàn bộ mặt bích
│   │   └── リングガスケット (Ring Gasket / RF / IBC): Dạng vành tròn trơn, lọt trong vòng chia bu lông
│   └── 7 Loại vật liệu chế tạo chuẩn hóa:
│       ├── (1) ゴムシート (Cao su tấm / 布入り có sợi vải gia cường)
│       ├── (2) ジョイントシート (Tấm đệm sợi nén Non-Asbestos Joint Sheet)
│       ├── (3) ふっ素樹脂切削シート (Tấm PTFE tiện cắt từ khối - Cut PTFE)
│       ├── (4) ふっ素樹脂延伸シート (Tấm PTFE giãn nở đa chiều - ePTFE)
│       ├── (5) ふっ素樹脂延伸シート高密度品 (Tấm ePTFE mật độ cao - High-density ePTFE)
│       ├── (6) 充塡材入りふっ素樹脂圧延シート (Tấm PTFE cán có chất độn - Filled PTFE)
│       └── (7) 膨張黒鉛シート (Tấm than chì Graphite giãn nở / 金属補強品 có cốt thép)
│
├── 2. ふっ素樹脂ジャケットガスケット (Họ II: Gioăng bọc màng PTFE - PTFE Jacketed Gaskets)
│   ├── Cấu tạo: Lõi mềm (Joint sheet / Cao su) + Lớp áo bảo vệ bên ngoài bằng màng PTFE nguyên chất
│   └── 3 Kiểu gia công màng bọc:
│       ├── (1) 切込み被覆 (S形 - Slit Type): Xẻ rãnh từ vành ngoài lồng lõi vào (Cỡ nhỏ - vừa: DN 15A ~ 300A)
│       ├── (2) くり抜き被覆 (M形 - Milled Type / Chữ U liền): Phay khoét lòng máng mép trong, chống đọng dịch
│       └── (3) 融着被覆 (F形 - Welded / Fused Type): Hàn nhiệt mép màng PTFE kín tuyệt đối (Cỡ lớn: DN 350A ~ 600A+)
│
├── 3. うず巻形ガスケット (Họ III: Gioăng kim loại quấn xoắn - Spiral Wound Gaskets / SWG)
│   ├── Cấu tạo: Dải kim loại hình V quấn xoắn xen kẽ dải đệm phi kim (Graphite / PTFE / Non-asbestos)
│   └── 4 Kiểu kết cấu vành dẫn hướng:
│       ├── (1) 基本形 (Basic Type - SW): Chỉ có dải quấn, dùng cho bích rãnh đực-cái và rãnh kín (TG / MF)
│       ├── (2) 内輪付き (With Inner Ring - SWI): Có vành kim loại bên trong chống móp vặn ("菊形変形")
│       ├── (3) 外輪付き (With Outer Ring - SWC): Có vành kim loại ngoài để định tâm vòng bu lông (Dùng cho RF)
│       └── (4) 内外輪付き (With Inner & Outer Ring - SWIC): Có cả 2 vành (Bắt buộc cho áp cao 16K~63K RF)
│
└── 4. 附属書A (Phụ lục A: Gioăng tấm cho mặt bích áp lực siêu thấp 2K - JIS B 2220 Annex E)
```

---

### Họ 1: Gioăng tấm đệm (シートガスケット - Sheet Gaskets)

* **Bản chất**: Cắt từ các tấm vật liệu phi kim hoặc bán kim phẳng đồng đều.
* **Hai dạng định hình**:
  1. **全面形 (Full-Face Gasket)**: Có đường kính ngoài bằng đường kính ngoài mặt bích ($D$), được đục đầy đủ số lỗ bu lông ($n$ lỗ, đường kính $h$, nằm trên đường tròn chia $C$). Thường dùng cho mặt bích phẳng (Flat Face - FF), bích gang (JIS B 2239), bích đồng, bích nhôm hoặc bích tấm hàn trượt SOP/BL cỡ lớn (5K $\ge$ 400A, 10K $\ge$ 250A) để hạn chế mô-men uốn gây nứt vành bích.
  2. **リング (Ring Gasket / Inside Bolt Circle)**: Chỉ gồm vành khăn tròn giới hạn bởi đường kính trong $d_1$ và đường kính ngoài $D_3$, nằm lọt trọn bên trong vòng tròn chia bu lông (PCD). Dùng cho bích gờ nổi (Raised Face - RF), bích lồi lõm (Male-Female) và bích rãnh (Tongue-and-Groove).
* **Quy chuẩn độ dày (Bảng 11 & Bảng 12)**:
  * Chiều dày danh định tiêu chuẩn: **0.5, 0.8, 1.0, 1.5, 2.0, 3.0 mm**.
  * Trong ứng dụng đường ống bích tiêu chuẩn công nghiệp (5K ~ 30K), chiều dày thông dụng nhất là **1.5 mm** và **3.0 mm**.

---

### Họ 2: Gioăng bọc màng PTFE (ふっ素樹脂ジャケットガスケット - PTFE Jacketed Gaskets)

* **Bản chất**: Kết hợp tính năng đàn hồi, chịu nén của vật liệu lõi (Core - thường là Joint Sheet không amiăng) với tính năng kháng hóa chất trơ tuyệt đối của màng bọc PTFE dày từ 0.4 mm đến 0.8 mm.
* **Ba kiểu kết cấu màng bọc**:
  * **S-Type (切込み被覆 - Slit jacket)**: Màng PTFE được rạch lưỡi dao từ ngoài mép biên vào giữa để lồng lõi đệm. Gia công nhanh, giá thành tối ưu cho dải cỡ từ 15A đến 300A.
  * **M-Type (くり抜き被覆 - Milled/Machined U-jacket)**: Màng PTFE được tiện rãnh chữ U liền khối nguyên tấm ở mép trong. Mép trong trơn láng 100%, ngăn ngừa đọng lưu chất, tuyệt đối sạch sẽ trong ngành hóa chất siêu tinh khiết, dược phẩm và thực phẩm.
  * **F-Type (融着被覆 - Fused/Welded jacket)**: Ghép 2 tấm màng PTFE và hàn nhiệt nóng chảy mép mép ngoài/trong. Chuyên dụng cho các đường ống đường kính lớn từ 350A đến 600A+.
* **Phạm vi áp dụng (Bảng 13 & 14)**:
  * Áp lực: 5K, 10K, 10K mỏng (cho cả mặt bích FF và RF); 16K, 20K (cho bích RF).

---

### Họ 3: Gioăng kim loại quấn xoắn (うず巻形ガスケット - Spiral Wound Gaskets)

* **Bản chất**: Dải lá thép không gỉ cán nguội định hình gân chữ V (V-shaped hoop - SUS304, SUS316, SUS316L...) được quấn tròn đồng tâm, ép xen kẽ với dải đệm phi kim làm kín (Filler tape: Than chì mềm Expanded Graphite, hạt nhựa PTFE hoặc sợi vô cơ chịu nhiệt).
* **Bốn biến thể kết cấu dẫn hướng**:
  1. **Loại cơ bản (基本形 - Basic Type)**: Không vành dẫn hướng. Chiều dày dải quấn tiêu chuẩn là 3.2 mm hoặc 4.5 mm. Chỉ dùng trong các hốc bích khép kín (bích rãnh âm dương Tongue-and-Groove hoặc hốc lồi lõm Male-Female).
  2. **Loại có vòng trong (内輪付き - With Inner Ring)**: Thêm vành thép đặc bên trong dải quấn. Vành trong ngăn dải quấn bị nén quá mức và chống hiện tượng bung mép trong ("菊形変形" - biến dạng cánh cúc) làm tắc nghẽn dòng chảy.
  3. **Loại có vòng ngoài (外輪付き - With Outer Ring / Centering Ring)**: Thêm vành thép định tâm bên ngoài dải quấn. Đường kính ngoài của vành khớp vừa khít với vòng cắm bu lông, giúp căn tâm tự động khi lắp ghép trên bích phẳng hoặc gờ nâng (RF).
  4. **Loại có cả vòng trong và vòng ngoài (内外輪付き - With Inner and Outer Rings)**: Cấu trúc hoàn hảo và an toàn nhất của dòng gioăng quấn xoắn. Vành ngoài định tâm chính xác, vành trong chống biến dạng bung dải quấn. Bắt buộc sử dụng cho cấp áp suất cao (16K, 20K, 30K, 40K, 63K) khi dùng đệm than chì Graphite hoặc PTFE trên bích RF.

---

## 3. BẢNG ĐỐI CHIẾU VÀ SO SÁNH TOÀN DIỆN CÁC LOẠI GASKET JIS B 2404

### Bảng 1: Bảng so sánh tổng hợp 3 họ Gasket theo kết cấu và phạm vi áp dụng

| Tiêu chí so sánh | Họ I: Gioăng tấm đệm (Sheet Gasket) | Họ II: Gioăng bọc PTFE (PTFE Jacketed) | Họ III: Gioăng quấn xoắn (Spiral Wound) |
| :--- | :--- | :--- | :--- |
| **Tên tiếng Nhật** | シートガスケット | ふっ素樹脂ジャケットガスケット | うず巻形ガスケット |
| **Vật liệu cấu tạo** | Cao su, Joint sheet, PTFE cắt/giãn nở, Graphite | Lõi Joint sheet + Vỏ bọc màng PTFE nguyên chất | Lá thép V (SUS304/316) + Filler (Graphite/PTFE) + Vành thép |
| **Dạng kết cấu** | • Toàn mặt (全面形 - Full Face)<br>• Vành trong (リング - Ring) | • Xẻ rãnh (S-Type - 切込み)<br>• Phay chữ U (M-Type - くり抜き)<br>• Hàn nhiệt (F-Type - 融着) | • Cơ bản (基本形 - Không vành)<br>• Có vành trong (内輪)<br>• Có vành ngoài (外輪)<br>• Có cả vành trong & ngoài (内外輪) |
| **Dải áp suất (Rating)** | 2K, 5K, 10K, 16K, 20K, 30K | 5K, 10K, 16K, 20K | 10K, 16K, 20K, 30K, 40K, 63K |
| **Dải cỡ danh định (DN)** | DN 10A – DN 1500A (Bảng 6 – 10) | DN 15A – DN 600A (Bảng 13 – 14) | DN 10A – DN 600A (Bảng 15 – 26) |
| **Độ dày tiêu chuẩn (t)** | 0.5, 0.8, 1.0, **1.5**, 2.0, **3.0 mm** | Thường 2.0 mm, 3.0 mm | Thân quấn: **4.5 mm** (hoặc 3.2 mm)<br>Vành dẫn hướng: **3.0 mm** |
| **Loại mặt bích thích hợp** | • Mặt phẳng (FF)<br>• Gờ nổi (RF)<br>• Lồi - Lõm (MF)<br>• Rãnh âm dương (TG) | • Mặt phẳng (FF)<br>• Gờ nổi (RF) | • Gờ nổi (RF): Cần vành ngoài/trong<br>• Lồi - Lõm (MF): Cơ bản / Vành trong<br>• Rãnh âm dương (TG): Loại cơ bản |
| **Khả năng chịu nhiệt** | -50°C đến 150°C (Cao su / PTFE)<br>Đến 400°C (Graphite có cốt kim loại) | -50°C đến 150°C (Giới hạn bởi màng bọc nhựa PTFE) | -200°C đến 600°C (Với Filler Graphite & Thép SUS316L) |
| **Đặc tính nổi bật** | Giá thành rẻ, dễ cắt dập tại chỗ, độ đàn hồi tốt ở áp thấp | Kháng axit, kiềm mạnh, bề mặt siêu sạch, không gây nhiễm bẩn | Chịu áp lực cực cao, chống rung động, chống rão đàn hồi, tự bù nhiệt |

---

### Bảng 2: Ma trận phối ghép Gasket theo kiểu bề mặt bích (Facing Compatibility)

*(Trích xuất chuẩn hóa từ Điều 5: Bảng 3, Bảng 4, Bảng 5 của JIS B 2404:2018)*

| Kiểu bề mặt bích (Flange Facing) | Dạng Gasket cho phép | Loại Gasket tương thích khuyến nghị | Cấp áp suất tương thích (Rating) | Ghi chú kỹ thuật tiêu chuẩn |
| :--- | :--- | :--- | :--- | :--- |
| **Mặt phẳng (Flat Face - 全面座)** | **全面形 (Full-Face)** | • Cao su tấm (布入りゴム)<br>• Joint Sheet<br>• PTFE tấm (cắt / ePTFE)<br>• Graphite có cốt | 2K, 5K, 10K, 10K mỏng, 16K | • Bu lông xuyên qua gioăng giúp giữ cố định.<br>• Bắt buộc dùng cho bích SOP/BL 5K $\ge$400A và 10K $\ge$250A. |
| **Gờ nâng (Raised Face - 平面座)** | **リング (Ring Gasket)** | • Joint Sheet, ePTFE, Graphite<br>• PTFE Jacketed (S, M, F) | 5K, 10K, 16K, 20K, 30K | • Vành ngoài $D_3$ lọt khít trong các lỗ bu lông để tự định tâm. |
| **Gờ nâng (Raised Face - 平面座)** | **うず巻形 (Spiral Wound)** | • Loại có vành ngoài (外輪)<br>• Loại có cả vành trong & ngoài (内外輪) | 10K, 16K, 20K, 30K, 40K, 63K | • Bắt buộc dùng vành ngoài để căn tâm.<br>• Áp $\ge$ 16K khuyến nghị dùng内外輪 chống bung mép trong. |
| **Lồi - Lõm (Male - Female / はめ込み形)** | **リング (Ring Gasket)** | • Joint Sheet, PTFE, Graphite | 10K, 16K, 20K, 30K, 40K, 63K | • Gioăng lọt trọn vào lòng hốc âm (Female recess). |
| **Lồi - Lõm (Male - Female / はめ込み形)** | **うず巻形 (Spiral Wound)** | • Loại cơ bản (基本形)<br>• Loại có vành trong (内輪付き) | 10K, 16K, 20K, 30K, 40K, 63K | • Không cần vành ngoài vì thành hốc bích đã có chức năng căn tâm. |
| **Rãnh âm - dương (Tongue & Groove / 溝形)** | **リング (Ring Gasket)** | • Joint Sheet, PTFE, Graphite | 10K, 16K, 20K, 30K, 40K, 63K | • Bề rộng gioăng hẹp, lắp kín trong rãnh rãnh âm. |
| **Rãnh âm - dương (Tongue & Groove / 溝形)** | **うず巻形 (Spiral Wound)** | • Loại cơ bản (基本形 - Không vành) | 10K, 16K, 20K, 30K, 40K, 63K | • Độ kín khít cao nhất, chống thổi bay đệm ở áp siêu cao. |

---

### Bảng 3: Ma trận phối ghép Gasket theo vật liệu mặt bích (JIS B 2220 / 2239 / 2240 / 2241)

*(Trích xuất từ Bảng 2 của JIS B 2404:2018)*

| Tiêu chuẩn mặt bích | Vật liệu chế tạo bích | Sheet Gasket (Cao su / Joint Sheet) | PTFE Jacketed Gasket | Spiral Wound Gasket (Quấn xoắn kim loại) | Lưu ý kỹ thuật |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **JIS B 2220** | Thép cacbon, thép không gỉ (Steel) | **○ (Tốt)** | **○ (Tốt)** | **○ (Tốt)** | Thép chịu lực kéo/siết cao, tương thích toàn bộ các loại gioăng kể cả gioăng kim loại cứng. |
| **JIS B 2239** | Gang xám, gang dẻo (Cast Iron) | **○ (Tốt)** | **- (Hạn chế)** | **- (Không khuyên dùng)** | Gang có độ bền kéo và độ dẻo thấp. Tránh dùng gioăng quấn xoắn đòi hỏi lực siết bu lông quá lớn dễ làm nứt vỡ bích gang. Ưu tiên đệm cao su hoặc Joint sheet mềm. |
| **JIS B 2240** | Hợp kim đồng (Copper Alloy) | **○ (Tốt)** | **○ (Tốt)** | **- (Không khuyên dùng)** | Bích đồng mềm, dùng gioăng tấm mềm hoặc gioăng bọc PTFE chịu ăn mòn nước biển. |
| **JIS B 2241** | Hợp kim nhôm (Aluminium Alloy) | **○ (Tốt)** | **○ (Tốt)** | **- (Không khuyên dùng)** | Bích nhôm dễ trầy xước và giới hạn lực siết, chỉ áp dụng đệm cao su mềm hoặc màng PTFE đàn hồi cao. |

---

### Bảng 4: Bảng tra cứu chiều dày danh định và dung sai kích thước

*(Trích xuất từ Bảng 11, Bảng 12 và quy định dung sai chế tạo JIS B 2404)*

| Dòng Gasket | Chiều dày danh định tiêu chuẩn ($t$) | Dung sai chiều dày ($\Delta t$) | Dung sai đường kính ngoài ($\Delta D$) | Dung sai đường kính trong ($\Delta d_1$) |
| :--- | :--- | :--- | :--- | :--- |
| **Sheet Gasket (Cao su / Joint Sheet)** | 0.5, 0.8, 1.0, 1.5, 2.0, 3.0 mm | $\pm 0.15 \sim \pm 0.25$ mm | DN $\le 300$: $\pm 1.5$ mm<br>DN $350 \sim 600$: $\pm 2.0$ mm<br>DN $> 600$: $\pm 3.0$ mm | DN $\le 300$: $\pm 1.5$ mm<br>DN $350 \sim 600$: $\pm 2.0$ mm<br>DN $> 600$: $\pm 3.0$ mm |
| **PTFE Jacketed Gasket** | Thường 2.0 mm hoặc 3.0 mm | $\pm 0.3$ mm | $\pm 1.5$ mm | $\pm 1.5$ mm |
| **Spiral Wound Gasket (Phần thân quấn)** | **4.5 mm** (mặc định)<br>hoặc 3.2 mm (cỡ nhỏ) | $+0.4 / -0.2$ mm | Dải quấn $d_3$: $\pm 0.8$ mm | Dải quấn $d_2$: $\pm 0.4$ mm |
| **Spiral Wound Gasket (Vành ngoài / Vành trong)** | **3.0 mm** (hoặc 2.0 mm) | $\pm 0.2$ mm | Vành ngoài $d_4$: $\pm 0.8$ mm | Vành trong $d_1$: $\pm 0.8$ mm |

---

## 4. KẾ HOẠCH CẬP NHẬT CƠ SỞ DỮ LIỆU VÀ HỆ THỐNG MÃ NGUỒN

Để đưa toàn bộ tiêu chuẩn JIS B 2404:2018 vào hệ sinh thái CAD/Python hiện tại của dự án (tương tự như `_fvc_flanges` và `_fvc_fasteners`), chúng ta xây dựng lộ trình thực thi chuẩn hóa 7 bước:

```
LỘ TRÌNH 7 BƯỚC TÍCH HỢP JIS B 2404:2018
├── Bước 1: Data Modeling (Khai báo Typed Models cho 3 họ Gasket)
├── Bước 2: SQLite Schema & Storage (jis_b2404.sqlite)
├── Bước 3: In-Memory Dataset (jis_b2404_dataset.py)
├── Bước 4: Smart DAO Query Engine (jis_b2404_reader.py)
├── Bước 5: 3D Solid Geometry Builder (geometry/gasket.py)
├── Bước 6: Integration into Hotreload Assembly (hotreload_impl.py)
└── Bước 7: Unit Testing & Performance Verification (test_jis_b2404.py)
```

---

### Bước 1: Mô hình hóa dữ liệu (Pydantic / Dataclasses Models)
* **Vị trí file**: `_fvc_fasteners/models/jis_b2404_specs.py`
* **Nội dung thiết kế**: Khai báo các cấu trúc dữ liệu hình học mạnh:
  ```python
  from dataclasses import dataclass
  from typing import Optional, List

  @dataclass(frozen=True)
  class SheetGasketSpec:
      """Thông số kích thước gioăng tấm phẳng (Bảng 6 - 10)"""
      standard: str              # 'JIS_B_2404'
      rating: str                # '2K', '5K', '10K', '16K', '20K', '30K'
      dn: int                    # Cỡ danh định mm (10, 15, ..., 1500)
      shape: str                 # 'FULL_FACE' hoặc 'RING'
      facing: str                # 'FF', 'RF', 'MF', 'TG'
      d1: float                  # Đường kính trong gioăng (mm)
      d2: float                  # Đường kính ngoài gioăng (mm)
      c: Optional[float] = None  # PCD vòng tròn chia bu lông (cho Full-face)
      h: Optional[float] = None  # Đường kính lỗ bu lông (cho Full-face)
      no: Optional[int] = None   # Số lỗ bu lông (cho Full-face)
      nominal_thickness: float = 3.0  # 1.5, 3.0 mm

  @dataclass(frozen=True)
  class PtfeJacketGasketSpec:
      """Thông số gioăng bọc màng PTFE (Bảng 13 - 14)"""
      standard: str
      rating: str
      dn: int
      jacket_type: str           # 'S' (Slit), 'M' (Milled), 'F' (Fused)
      d1: float                  # Đường kính trong (mm)
      d2: float                  # Đường kính ngoài (mm)
      nominal_thickness: float = 3.0

  @dataclass(frozen=True)
  class SpiralWoundGasketSpec:
      """Thông số gioăng kim loại quấn xoắn SWG (Bảng 15 - 26)"""
      standard: str
      rating: str
      dn: int
      construction: str          # 'BASIC', 'INNER_RING', 'OUTER_RING', 'INNER_OUTER_RING'
      facing: str                # 'RF', 'MF', 'TG'
      d1: Optional[float]        # Đường kính trong vành trong (Inner Ring ID)
      d2: float                  # Đường kính trong thân quấn (Winding ID)
      d3: float                  # Đường kính ngoài thân quấn (Winding OD)
      d4: Optional[float]        # Đường kính ngoài vành ngoài (Outer Ring OD)
      t_winding: float = 4.5     # Chiều dày thân quấn
      t_ring: float = 3.0        # Chiều dày vành dẫn hướng
  ```

---

### Bước 2: Thiết kế cơ sở dữ liệu SQLite (`jis_b2404.sqlite`)
* **Vị trí file**: `_fvc_fasteners/data/jis_b2404.sqlite`
* **Cấu trúc bảng**:
  1. `sheet_gaskets`: Chứa dữ liệu toàn bộ Bảng 6, 7, 8 (Full-Face) và Bảng 9, 10 (Ring Gasket).
  2. `ptfe_jacket_gaskets`: Chứa dữ liệu Bảng 13, 14 cho 3 kiểu S, M, F.
  3. `spiral_wound_gaskets`: Chứa dữ liệu Bảng 15 đến Bảng 26 với đầy đủ 4 đường kính $d_1, d_2, d_3, d_4$.
* **Đánh chỉ mục (Indexing)**:
  `CREATE INDEX idx_sheet ON sheet_gaskets (rating, dn, shape, facing);`  
  `CREATE INDEX idx_swg ON spiral_wound_gaskets (rating, dn, construction, facing);`

---

### Bước 3: Xây dựng bộ Dataset RAM thuần Python (`jis_b2404_dataset.py`)
* **Mục đích**: Tương tự như `jis_b1180_dataset.py`, `jis_b1181_dataset.py` và `jis_b1256_dataset.py`, dữ liệu được biên dịch sẵn thành từ điển hằng số `tuple` / `dict` tĩnh trong RAM.
* **Hiệu năng**: Tốc độ tra cứu đạt **< 0.001 ms (dưới 1 microsecond)**, loại bỏ hoàn toàn độ trễ I/O đọc ổ cứng khi AutoCAD Plant 3D render hàng trăm mặt bích cùng lúc.

---

### Bước 4: Phát triển tầng truy vấn thông minh DAO (`jis_b2404_reader.py`)
* **Vị trí file**: `_fvc_fasteners/db/jis_b2404_reader.py`
* **Giao diện API cấp cao**:
  ```python
  def get_sheet_gasket_dimension(rating: str, dn: int, shape: str = "RING", facing: str = "RF", thickness: float = 3.0) -> Optional[SheetGasketSpec]:
      """Tra cứu kích thước gioăng tấm đệm JIS B 2404"""
      ...

  def get_spiral_wound_gasket_dimension(rating: str, dn: int, construction: str = "INNER_OUTER_RING", facing: str = "RF") -> Optional[SpiralWoundGasketSpec]:
      """Tra cứu kích thước gioăng kim loại quấn xoắn JIS B 2404"""
      ...

  def get_auto_gasket_for_flange(rating: str, dn: int, flange_facing: str = "RF", gasket_family: str = "SHEET") -> Optional[GasketSpec]:
      """Tự động chọn kích thước gioăng tối ưu tương thích hoàn toàn với mặt bích JIS B 2220"""
      ...
  ```

---

### Bước 5: Nâng cấp hình học 3D Solid đa biến thể (`geometry/gasket.py`)
* **Hiện trạng**: [gasket.py](file:///c:/Users/Laptop/OneDrive/Desktop/Hello%20World/Python-Autocad-Plant-3D/_fvc_fasteners/geometry/gasket.py) hiện tại chỉ dựng một hình trụ rỗng đơn giản từ đường kính ngoài `od` và đường kính trong `id_`.
* **Nâng cấp**:
  1. **Dựng Full-Face Gasket**:
     * Khối đĩa trụ tròn đường kính ngoài $D$, khoét lỗ tâm $d_1$.
     * Tự động đục $n$ lỗ bu lông đường kính $h$ phân bố đều quanh đường tròn chia $C$.
  2. **Dựng Spiral Wound Gasket (LOD cao)**:
     * Dựng thân quấn (Winding): Hình trụ dày 4.5 mm từ $d_2$ đến $d_3$.
     * Dựng vành ngoài (Outer Ring): Vành thép dày 3.0 mm từ $d_3$ đến $d_4$.
     * Dựng vành trong (Inner Ring): Vành thép dày 3.0 mm từ $d_1$ đến $d_2$.
     * Hợp nhất 3 phần lại thành 1 Solid chuẩn xác về trực quan kỹ thuật.

---

### Bước 6: Tích hợp vào Cụm kết nối mặt bích (`hotreload_impl.py`)
* **Cơ chế nhận diện tự động thông minh (Smart Inference Engine - Cách 1)**:
  Tự động suy luận loại gioăng tối ưu dựa trên thông số bích mà người dùng không cần nhập tay:
  1. **Quy tắc bề mặt & áp suất**:
     * Bích phẳng `FF` -> Tự chọn `FULL_FACE_SHEET` (có đục $n$ lỗ bu lông).
     * Bích gờ `RF` áp thấp $\le 10K$ -> Tự chọn `RING_SHEET` ($D_3$ lọt lòng bu lông).
     * Bích gờ `RF` áp cao $\ge 16K$ -> Tự chọn `SPIRAL_WOUND` (`内外輪 - SWIC`).
     * Bích rãnh âm dương `TG` / Lồi lõm `MF` -> Tự chọn `SPIRAL_WOUND` cơ bản hoặc có vành trong.
  2. **Quy tắc chống ăn mòn điện hóa khi lệch vật liệu (Dissimilar Metal Detection - Cách 1)**:
     * Tự động so sánh: `if flange1.material != flange2.material:` (ví dụ bích Thép nối với bích Inox SUS304/SUS316, hoặc Thép nối Đồng):
     * **Kích hoạt tự động cụm cách điện (Dielectric Flange Insulation Kit)**:
       * Gioăng chuyển thành gioăng cách điện (GRE G10 / PTFE).
       * Tự động bổ sung **ống lót cách điện (Insulating Sleeves)** bọc quanh thân bu lông chống chạm lỗ bích.
       * Tự động bổ sung **vòng đệm cách điện kép (Double Insulating Washers)** đặt dưới từng đai ốc và mũ bu lông.

* **Code tích hợp vào hàm `run`**:
  ```python
  # Tự động nhận diện toàn bộ theo JIS B 2404 & Vật liệu bích:
  gasket_spec = get_auto_gasket_for_flange(
      rating=TEST_RATING, 
      dn=TEST_DN, 
      flange1=flange1, 
      flange2=flange2
  )
  gasket = Gasket(s, spec=gasket_spec)
  ```

---

### Bước 7: Kiểm thử tự động (Unit Tests & Performance Benchmarks)
* Xây dựng file `_fvc_fasteners/tests/test_jis_b2404.py`:
  1. Kiểm thử tính toàn vẹn của dữ liệu: Kiểm tra dải DN từ 10A đến 1500A cho toàn bộ 5K, 10K, 16K, 20K, 30K, 40K, 63K.
  2. Kiểm thử dung sai: Đảm bảo $d_1 < d_2$ và vành ngoài vừa khít trong vòng bu lông ($D_3 < C - h$).
  3. Đo benchmark thời gian truy vấn bộ nhớ: Cam kết thời gian đáp ứng dưới **0.001 ms**.
