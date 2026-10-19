"""Script khởi tạo CSDL SQLite và dataset Python thuần cho vòng đệm phẳng JIS B 1256 : 2008."""
import os
import sqlite3
import sys
from typing import Dict, Tuple

# Đảm bảo xuất UTF-8 trên mọi môi trường
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATA_DIR, "jis_b1256.sqlite")
DATASET_PATH = os.path.join(DATA_DIR, "jis_b1256_dataset.py")

# ==============================================================================
# 1. DANH MỤC CÁC CHỦNG LOẠI VÒNG ĐỆM PHẲNG JIS B 1256 : 2008
# ==============================================================================
# (type_id, type_code, type_name_ja, type_name_en, iso_standard, washer_series, product_grade, dimension_series, is_flange_default, description_vi)
WASHER_TYPES_DATA = [
    (
        1,
        "ISO_7089_NORMAL_GRADE_A",
        "平座金・並形−部品等級A",
        "Plain washers Normal series Grade A",
        "ISO 7089",
        "NORMAL",
        "GRADE_A",
        "ISO_NORMAL_A",
        1,
        "Vòng đệm phẳng vành tiêu chuẩn cấp A, dung sai tinh H13/h14 (Mặc định chuẩn cho mối nối mặt bích đường ống)"
    ),
    (
        2,
        "ISO_7090_NORMAL_CHAMFERED_GRADE_A",
        "平座金・並形面取り−部品等級A",
        "Plain washers Chamfered Normal series Grade A",
        "ISO 7090",
        "NORMAL_CHAMFERED",
        "GRADE_A",
        "ISO_NORMAL_CHAMFERED_A",
        0,
        "Vòng đệm phẳng vành tiêu chuẩn vát mép ngoài 30-45 độ cấp A (Dùng cho bu lông cường độ cao cấp bền 10.9, tránh cấn góc lượn cổ bu lông)"
    ),
    (
        3,
        "ISO_7091_NORMAL_GRADE_C",
        "平座金・並形−部品等級C",
        "Plain washers Normal series Grade C",
        "ISO 7091",
        "NORMAL",
        "GRADE_C",
        "ISO_NORMAL_C",
        0,
        "Vòng đệm phẳng vành tiêu chuẩn cấp C dập thô kinh tế (Dùng cho kết cấu thép dân dụng và bu lông cấp bền <= 6.8)"
    ),
    (
        4,
        "ISO_7092_SMALL_GRADE_A",
        "平座金・小形−部品等級A",
        "Plain washers Small series Grade A",
        "ISO 7092",
        "SMALL",
        "GRADE_A",
        "ISO_SMALL_A",
        0,
        "Vòng đệm phẳng vành nhỏ gọn cấp A (Dùng cho bu lông chìm lục giác Socket Head Cap Screw và vít đầu trụ cheese head)"
    ),
    (
        5,
        "ISO_7093_1_LARGE_GRADE_A",
        "平座金・大形−部品等級A",
        "Plain washers Large series Part 1 Grade A",
        "ISO 7093-1",
        "LARGE",
        "GRADE_A",
        "ISO_LARGE_A",
        0,
        "Vòng đệm phẳng vành lớn cấp A, diện tích tỳ gấp 2.2 lần loại thường (Phân bố đều lực siết trên bề mặt mềm hoặc rãnh xẻ rộng)"
    ),
    (
        6,
        "ISO_7093_2_LARGE_GRADE_C",
        "平座金・大形−部品等級C",
        "Plain washers Large series Part 2 Grade C",
        "ISO 7093-2",
        "LARGE",
        "GRADE_C",
        "ISO_LARGE_C",
        0,
        "Vòng đệm phẳng vành lớn cấp C gia công dập thô (Dùng cho thép tấm mỏng, vỏ máy cơ khí và lỗ quá khổ)"
    ),
    (
        7,
        "ISO_7094_EXTRA_LARGE_GRADE_C",
        "平座金・特大形−部品等級C",
        "Plain washers Extra large series Grade C",
        "ISO 7094",
        "EXTRA_LARGE",
        "GRADE_C",
        "ISO_EXTRA_LARGE_C",
        0,
        "Vòng đệm phẳng vành cực lớn dày cấp C (Chuyên dụng cho kết cấu gỗ Timber Structures nhằm chống lún dập thớ gỗ)"
    ),
    (
        8,
        "ANNEX_JA_SQUARE",
        "附属書JA 角座金",
        "Annex JA Square Washers",
        "ANNEX_JA",
        "SQUARE",
        "JIS_JA",
        "ANNEX_JA_SQUARE",
        0,
        "Vòng đệm vuông phụ lục JA (Dùng cho giằng cột nhà thép, liên kết dầm xà gồ gỗ và đường ray)"
    ),
    (
        9,
        "JIS_POLISHED_ROUND",
        "JIS B 1250 ミガキ丸",
        "JIS B 1250 Polished Round Washer",
        "JIS_B_1250",
        "POLISHED_ROUND",
        "JIS",
        "JIS_POLISHED_ROUND",
        0,
        "Vòng đệm tròn mài bóng hệ truyền thống Nhật Bản (Đường kính ngoài nhỏ gọn, bề mặt nhẵn bóng, dung sai tinh)"
    ),
    (
        10,
        "JIS_COMMERCIAL_ROUND",
        "JIS B 1250 並丸",
        "JIS B 1250 Commercial Round Washer",
        "JIS_B_1250",
        "COMMERCIAL_ROUND",
        "JIS",
        "JIS_COMMERCIAL_ROUND",
        0,
        "Vòng đệm tròn thông dụng hệ truyền thống Nhật Bản (Đường kính ngoài rộng, chế tạo dập phẳng đại trà)"
    ),
]

# ==============================================================================
# 2. BẢNG CƠ TÍNH VÀ CẤP ĐỘ CỨNG THEO JIS B 1256 : 2008
# ==============================================================================
# (hardness_class, min_hv, max_hv, applicable_bolts, description_vi)
HARDNESS_SPECS_DATA = [
    (
        "100_HV",
        100.0,
        200.0,
        "Cấp bền <= 6.8 (4.6, 4.8, 5.8, 6.8)",
        "Thép cacbon mềm không tôi, dùng cho đệm cấp C (ISO 7091, ISO 7093-2, ISO 7094)"
    ),
    (
        "200_HV",
        200.0,
        300.0,
        "Cấp bền <= 8.8, đai ốc cấp 8, thép không gỉ A2/A4",
        "Thép cacbon khử ứng suất hoặc Inox tôi nguội (Mặc định cho mối nối mặt bích đường ống)"
    ),
    (
        "300_HV",
        300.0,
        400.0,
        "Cấp bền 10.9 hoặc bu lông chìm cường độ cao",
        "Thép cacbon tôi và ram, dùng cho bu lông cường độ cao và đệm vát mép ISO 7090"
    ),
]

# ==============================================================================
# 3. KÍCH THƯỚC HÌNH HỌC CHI TIẾT THEO CÁC DÒNG SERIES (d1, d2, h, chamfer)
# ==============================================================================
# (series, bolt_size, nominal_dia, d1_nom, d1_min, d1_max, d2_nom, d2_min, d2_max, h_nom, h_min, h_max, chamfer_angle_deg, chamfer_c)
WASHER_DIMENSIONS_DATA = [
    # --------------------------------------------------------------------------
    # 1. ISO 7089 - NORMAL SERIES GRADE A (MẶC ĐỊNH CHO MẶT BÍCH)
    # --------------------------------------------------------------------------
    ("ISO_NORMAL_A", "M1.6", 1.6, 1.7, 1.70, 1.84, 4.0, 3.64, 4.0, 0.3, 0.25, 0.35, 0.0, None),
    ("ISO_NORMAL_A", "M2", 2.0, 2.2, 2.20, 2.34, 5.0, 4.64, 5.0, 0.3, 0.25, 0.35, 0.0, None),
    ("ISO_NORMAL_A", "M2.5", 2.5, 2.7, 2.70, 2.84, 6.0, 5.64, 6.0, 0.5, 0.45, 0.55, 0.0, None),
    ("ISO_NORMAL_A", "M3", 3.0, 3.2, 3.20, 3.38, 7.0, 6.64, 7.0, 0.5, 0.45, 0.55, 0.0, None),
    ("ISO_NORMAL_A", "M4", 4.0, 4.3, 4.30, 4.48, 9.0, 8.64, 9.0, 0.8, 0.70, 0.90, 0.0, None),
    ("ISO_NORMAL_A", "M5", 5.0, 5.3, 5.30, 5.48, 10.0, 9.64, 10.0, 1.0, 0.90, 1.10, 0.0, None),
    ("ISO_NORMAL_A", "M6", 6.0, 6.4, 6.40, 6.62, 12.0, 11.57, 12.0, 1.6, 1.40, 1.80, 0.0, None),
    ("ISO_NORMAL_A", "M8", 8.0, 8.4, 8.40, 8.62, 16.0, 15.57, 16.0, 1.6, 1.40, 1.80, 0.0, None),
    ("ISO_NORMAL_A", "M10", 10.0, 10.5, 10.50, 10.77, 20.0, 19.48, 20.0, 2.0, 1.80, 2.20, 0.0, None),
    ("ISO_NORMAL_A", "M12", 12.0, 13.0, 13.00, 13.27, 24.0, 23.48, 24.0, 2.5, 2.30, 2.70, 0.0, None),
    ("ISO_NORMAL_A", "M14", 14.0, 15.0, 15.00, 15.27, 28.0, 27.48, 28.0, 2.5, 2.30, 2.70, 0.0, None),
    ("ISO_NORMAL_A", "M16", 16.0, 17.0, 17.00, 17.27, 30.0, 29.48, 30.0, 3.0, 2.70, 3.30, 0.0, None),
    ("ISO_NORMAL_A", "M18", 18.0, 19.0, 19.00, 19.33, 34.0, 33.38, 34.0, 3.0, 2.70, 3.30, 0.0, None),
    ("ISO_NORMAL_A", "M20", 20.0, 21.0, 21.00, 21.33, 37.0, 36.38, 37.0, 3.0, 2.70, 3.30, 0.0, None),
    ("ISO_NORMAL_A", "M22", 22.0, 23.0, 23.00, 23.33, 39.0, 38.38, 39.0, 3.0, 2.70, 3.30, 0.0, None),
    ("ISO_NORMAL_A", "M24", 24.0, 25.0, 25.00, 25.33, 44.0, 43.38, 44.0, 4.0, 3.70, 4.30, 0.0, None),
    ("ISO_NORMAL_A", "M27", 27.0, 28.0, 28.00, 28.33, 50.0, 49.38, 50.0, 4.0, 3.70, 4.30, 0.0, None),
    ("ISO_NORMAL_A", "M30", 30.0, 31.0, 31.00, 31.39, 56.0, 55.26, 56.0, 4.0, 3.70, 4.30, 0.0, None),
    ("ISO_NORMAL_A", "M33", 33.0, 34.0, 34.00, 34.39, 60.0, 59.26, 60.0, 5.0, 4.40, 5.60, 0.0, None),
    ("ISO_NORMAL_A", "M36", 36.0, 37.0, 37.00, 37.39, 66.0, 65.26, 66.0, 5.0, 4.40, 5.60, 0.0, None),
    ("ISO_NORMAL_A", "M39", 39.0, 40.0, 40.00, 40.39, 72.0, 71.26, 72.0, 6.0, 5.40, 6.60, 0.0, None),
    ("ISO_NORMAL_A", "M42", 42.0, 43.0, 43.00, 43.39, 78.0, 77.26, 78.0, 7.0, 6.00, 8.00, 0.0, None),
    ("ISO_NORMAL_A", "M45", 45.0, 46.0, 46.00, 46.39, 85.0, 83.60, 85.0, 7.0, 6.00, 8.00, 0.0, None),
    ("ISO_NORMAL_A", "M48", 48.0, 50.0, 50.00, 50.39, 92.0, 90.60, 92.0, 8.0, 7.00, 9.00, 0.0, None),
    ("ISO_NORMAL_A", "M52", 52.0, 54.0, 54.00, 54.46, 98.0, 96.60, 98.0, 8.0, 7.00, 9.00, 0.0, None),
    ("ISO_NORMAL_A", "M56", 56.0, 58.0, 58.00, 58.46, 105.0, 103.60, 105.0, 9.0, 8.00, 10.00, 0.0, None),
    ("ISO_NORMAL_A", "M60", 60.0, 62.0, 62.00, 62.46, 110.0, 108.60, 110.0, 9.0, 8.00, 10.00, 0.0, None),
    ("ISO_NORMAL_A", "M64", 64.0, 66.0, 66.00, 66.46, 115.0, 113.60, 115.0, 9.0, 8.00, 10.00, 0.0, None),

    # --------------------------------------------------------------------------
    # 2. ISO 7090 - NORMAL SERIES CHAMFERED GRADE A (VÁT MÉP 30 - 45 ĐỘ)
    # --------------------------------------------------------------------------
    ("ISO_NORMAL_CHAMFERED_A", "M5", 5.0, 5.3, 5.30, 5.48, 10.0, 9.64, 10.0, 1.0, 0.90, 1.10, 45.0, 0.5),
    ("ISO_NORMAL_CHAMFERED_A", "M6", 6.0, 6.4, 6.40, 6.62, 12.0, 11.57, 12.0, 1.6, 1.40, 1.80, 45.0, 0.6),
    ("ISO_NORMAL_CHAMFERED_A", "M8", 8.0, 8.4, 8.40, 8.62, 16.0, 15.57, 16.0, 1.6, 1.40, 1.80, 45.0, 0.8),
    ("ISO_NORMAL_CHAMFERED_A", "M10", 10.0, 10.5, 10.50, 10.77, 20.0, 19.48, 20.0, 2.0, 1.80, 2.20, 45.0, 1.0),
    ("ISO_NORMAL_CHAMFERED_A", "M12", 12.0, 13.0, 13.00, 13.27, 24.0, 23.48, 24.0, 2.5, 2.30, 2.70, 45.0, 1.2),
    ("ISO_NORMAL_CHAMFERED_A", "M14", 14.0, 15.0, 15.00, 15.27, 28.0, 27.48, 28.0, 2.5, 2.30, 2.70, 45.0, 1.2),
    ("ISO_NORMAL_CHAMFERED_A", "M16", 16.0, 17.0, 17.00, 17.27, 30.0, 29.48, 30.0, 3.0, 2.70, 3.30, 45.0, 1.5),
    ("ISO_NORMAL_CHAMFERED_A", "M18", 18.0, 19.0, 19.00, 19.33, 34.0, 33.38, 34.0, 3.0, 2.70, 3.30, 45.0, 1.5),
    ("ISO_NORMAL_CHAMFERED_A", "M20", 20.0, 21.0, 21.00, 21.33, 37.0, 36.38, 37.0, 3.0, 2.70, 3.30, 45.0, 1.5),
    ("ISO_NORMAL_CHAMFERED_A", "M22", 22.0, 23.0, 23.00, 23.33, 39.0, 38.38, 39.0, 3.0, 2.70, 3.30, 45.0, 1.5),
    ("ISO_NORMAL_CHAMFERED_A", "M24", 24.0, 25.0, 25.00, 25.33, 44.0, 43.38, 44.0, 4.0, 3.70, 4.30, 45.0, 2.0),
    ("ISO_NORMAL_CHAMFERED_A", "M27", 27.0, 28.0, 28.00, 28.33, 50.0, 49.38, 50.0, 4.0, 3.70, 4.30, 45.0, 2.0),
    ("ISO_NORMAL_CHAMFERED_A", "M30", 30.0, 31.0, 31.00, 31.39, 56.0, 55.26, 56.0, 4.0, 3.70, 4.30, 45.0, 2.0),
    ("ISO_NORMAL_CHAMFERED_A", "M33", 33.0, 34.0, 34.00, 34.39, 60.0, 59.26, 60.0, 5.0, 4.40, 5.60, 45.0, 2.5),
    ("ISO_NORMAL_CHAMFERED_A", "M36", 36.0, 37.0, 37.00, 37.39, 66.0, 65.26, 66.0, 5.0, 4.40, 5.60, 45.0, 2.5),
    ("ISO_NORMAL_CHAMFERED_A", "M39", 39.0, 40.0, 40.00, 40.39, 72.0, 71.26, 72.0, 6.0, 5.40, 6.60, 45.0, 2.5),
    ("ISO_NORMAL_CHAMFERED_A", "M42", 42.0, 43.0, 43.00, 43.39, 78.0, 77.26, 78.0, 7.0, 6.00, 8.00, 45.0, 3.0),
    ("ISO_NORMAL_CHAMFERED_A", "M45", 45.0, 46.0, 46.00, 46.39, 85.0, 83.60, 85.0, 7.0, 6.00, 8.00, 45.0, 3.0),
    ("ISO_NORMAL_CHAMFERED_A", "M48", 48.0, 50.0, 50.00, 50.39, 92.0, 90.60, 92.0, 8.0, 7.00, 9.00, 45.0, 3.0),
    ("ISO_NORMAL_CHAMFERED_A", "M52", 52.0, 54.0, 54.00, 54.46, 98.0, 96.60, 98.0, 8.0, 7.00, 9.00, 45.0, 3.0),
    ("ISO_NORMAL_CHAMFERED_A", "M56", 56.0, 58.0, 58.00, 58.46, 105.0, 103.60, 105.0, 9.0, 8.00, 10.00, 45.0, 3.5),
    ("ISO_NORMAL_CHAMFERED_A", "M60", 60.0, 62.0, 62.00, 62.46, 110.0, 108.60, 110.0, 9.0, 8.00, 10.00, 45.0, 3.5),
    ("ISO_NORMAL_CHAMFERED_A", "M64", 64.0, 66.0, 66.00, 66.46, 115.0, 113.60, 115.0, 9.0, 8.00, 10.00, 45.0, 3.5),

    # --------------------------------------------------------------------------
    # 3. ISO 7091 - NORMAL SERIES GRADE C (DẬP PHẲNG THÔ)
    # --------------------------------------------------------------------------
    ("ISO_NORMAL_C", "M1.6", 1.6, 1.7, 1.70, 1.95, 4.0, 3.25, 4.0, 0.3, 0.20, 0.40, 0.0, None),
    ("ISO_NORMAL_C", "M2", 2.0, 2.2, 2.20, 2.45, 5.0, 4.25, 5.0, 0.3, 0.20, 0.40, 0.0, None),
    ("ISO_NORMAL_C", "M2.5", 2.5, 2.7, 2.70, 2.95, 6.0, 5.25, 6.0, 0.5, 0.38, 0.62, 0.0, None),
    ("ISO_NORMAL_C", "M3", 3.0, 3.2, 3.20, 3.45, 7.0, 6.25, 7.0, 0.5, 0.38, 0.62, 0.0, None),
    ("ISO_NORMAL_C", "M4", 4.0, 4.3, 4.30, 4.60, 9.0, 8.10, 9.0, 0.8, 0.60, 1.00, 0.0, None),
    ("ISO_NORMAL_C", "M5", 5.0, 5.3, 5.30, 5.60, 10.0, 9.10, 10.0, 1.0, 0.80, 1.20, 0.0, None),
    ("ISO_NORMAL_C", "M6", 6.0, 6.4, 6.40, 6.76, 12.0, 10.90, 12.0, 1.6, 1.30, 1.90, 0.0, None),
    ("ISO_NORMAL_C", "M8", 8.0, 8.4, 8.40, 8.76, 16.0, 14.90, 16.0, 1.6, 1.30, 1.90, 0.0, None),
    ("ISO_NORMAL_C", "M10", 10.0, 10.5, 10.50, 10.93, 20.0, 18.70, 20.0, 2.0, 1.70, 2.30, 0.0, None),
    ("ISO_NORMAL_C", "M12", 12.0, 13.0, 13.00, 13.43, 24.0, 22.70, 24.0, 2.5, 2.10, 2.90, 0.0, None),
    ("ISO_NORMAL_C", "M14", 14.0, 15.0, 15.00, 15.43, 28.0, 26.70, 28.0, 2.5, 2.10, 2.90, 0.0, None),
    ("ISO_NORMAL_C", "M16", 16.0, 17.0, 17.00, 17.43, 30.0, 28.70, 30.0, 3.0, 2.50, 3.50, 0.0, None),
    ("ISO_NORMAL_C", "M18", 18.0, 19.0, 19.00, 19.52, 34.0, 32.40, 34.0, 3.0, 2.50, 3.50, 0.0, None),
    ("ISO_NORMAL_C", "M20", 20.0, 21.0, 21.00, 21.52, 37.0, 35.40, 37.0, 3.0, 2.50, 3.50, 0.0, None),
    ("ISO_NORMAL_C", "M22", 22.0, 23.0, 23.00, 23.52, 39.0, 37.40, 39.0, 3.0, 2.50, 3.50, 0.0, None),
    ("ISO_NORMAL_C", "M24", 24.0, 25.0, 25.00, 25.52, 44.0, 42.40, 44.0, 4.0, 3.40, 4.60, 0.0, None),
    ("ISO_NORMAL_C", "M27", 27.0, 28.0, 28.00, 28.52, 50.0, 48.40, 50.0, 4.0, 3.40, 4.60, 0.0, None),
    ("ISO_NORMAL_C", "M30", 30.0, 31.0, 31.00, 31.62, 56.0, 54.10, 56.0, 4.0, 3.40, 4.60, 0.0, None),
    ("ISO_NORMAL_C", "M33", 33.0, 34.0, 34.00, 34.62, 60.0, 58.10, 60.0, 5.0, 4.20, 5.80, 0.0, None),
    ("ISO_NORMAL_C", "M36", 36.0, 37.0, 37.00, 37.62, 66.0, 64.10, 66.0, 5.0, 4.20, 5.80, 0.0, None),
    ("ISO_NORMAL_C", "M39", 39.0, 40.0, 40.00, 40.62, 72.0, 70.10, 72.0, 6.0, 5.10, 6.90, 0.0, None),
    ("ISO_NORMAL_C", "M42", 42.0, 43.0, 43.00, 43.62, 78.0, 76.10, 78.0, 7.0, 5.80, 8.20, 0.0, None),
    ("ISO_NORMAL_C", "M45", 45.0, 46.0, 46.00, 46.62, 85.0, 82.80, 85.0, 7.0, 5.80, 8.20, 0.0, None),
    ("ISO_NORMAL_C", "M48", 48.0, 50.0, 50.00, 50.62, 92.0, 89.80, 92.0, 8.0, 6.80, 9.20, 0.0, None),
    ("ISO_NORMAL_C", "M52", 52.0, 54.0, 54.00, 54.74, 98.0, 95.80, 98.0, 8.0, 6.80, 9.20, 0.0, None),
    ("ISO_NORMAL_C", "M56", 56.0, 58.0, 58.00, 58.74, 105.0, 102.80, 105.0, 9.0, 7.60, 10.40, 0.0, None),
    ("ISO_NORMAL_C", "M60", 60.0, 62.0, 62.00, 62.74, 110.0, 107.80, 110.0, 9.0, 7.60, 10.40, 0.0, None),
    ("ISO_NORMAL_C", "M64", 64.0, 66.0, 66.00, 66.74, 115.0, 112.80, 115.0, 9.0, 7.60, 10.40, 0.0, None),

    # --------------------------------------------------------------------------
    # 4. ISO 7092 - SMALL SERIES GRADE A (VÀNH NHỎ CHO BU LÔNG CHÌM)
    # --------------------------------------------------------------------------
    ("ISO_SMALL_A", "M1.6", 1.6, 1.7, 1.70, 1.84, 3.0, 2.75, 3.0, 0.3, 0.25, 0.35, 0.0, None),
    ("ISO_SMALL_A", "M2", 2.0, 2.2, 2.20, 2.34, 4.0, 3.70, 4.0, 0.3, 0.25, 0.35, 0.0, None),
    ("ISO_SMALL_A", "M2.5", 2.5, 2.7, 2.70, 2.84, 5.0, 4.70, 5.0, 0.5, 0.45, 0.55, 0.0, None),
    ("ISO_SMALL_A", "M3", 3.0, 3.2, 3.20, 3.38, 6.0, 5.70, 6.0, 0.5, 0.45, 0.55, 0.0, None),
    ("ISO_SMALL_A", "M3.5", 3.5, 3.7, 3.70, 3.88, 7.0, 6.64, 7.0, 0.5, 0.45, 0.55, 0.0, None),
    ("ISO_SMALL_A", "M4", 4.0, 4.3, 4.30, 4.48, 8.0, 7.64, 8.0, 0.5, 0.45, 0.55, 0.0, None),
    ("ISO_SMALL_A", "M5", 5.0, 5.3, 5.30, 5.48, 9.0, 8.64, 9.0, 1.0, 0.90, 1.10, 0.0, None),
    ("ISO_SMALL_A", "M6", 6.0, 6.4, 6.40, 6.62, 11.0, 10.57, 11.0, 1.6, 1.40, 1.80, 0.0, None),
    ("ISO_SMALL_A", "M8", 8.0, 8.4, 8.40, 8.62, 15.0, 14.57, 15.0, 1.6, 1.40, 1.80, 0.0, None),
    ("ISO_SMALL_A", "M10", 10.0, 10.5, 10.50, 10.77, 18.0, 17.57, 18.0, 1.6, 1.40, 1.80, 0.0, None),
    ("ISO_SMALL_A", "M12", 12.0, 13.0, 13.00, 13.27, 20.0, 19.48, 20.0, 2.0, 1.80, 2.20, 0.0, None),
    ("ISO_SMALL_A", "M14", 14.0, 15.0, 15.00, 15.27, 24.0, 23.48, 24.0, 2.5, 2.30, 2.70, 0.0, None),
    ("ISO_SMALL_A", "M16", 16.0, 17.0, 17.00, 17.27, 28.0, 27.48, 28.0, 2.5, 2.30, 2.70, 0.0, None),
    ("ISO_SMALL_A", "M18", 18.0, 19.0, 19.00, 19.33, 30.0, 29.48, 30.0, 2.5, 2.30, 2.70, 0.0, None),
    ("ISO_SMALL_A", "M20", 20.0, 21.0, 21.00, 21.33, 34.0, 33.38, 34.0, 3.0, 2.70, 3.30, 0.0, None),
    ("ISO_SMALL_A", "M22", 22.0, 23.0, 23.00, 23.33, 37.0, 36.38, 37.0, 3.0, 2.70, 3.30, 0.0, None),
    ("ISO_SMALL_A", "M24", 24.0, 25.0, 25.00, 25.33, 39.0, 38.38, 39.0, 4.0, 3.70, 4.30, 0.0, None),
    ("ISO_SMALL_A", "M27", 27.0, 28.0, 28.00, 28.33, 44.0, 43.38, 44.0, 4.0, 3.70, 4.30, 0.0, None),
    ("ISO_SMALL_A", "M30", 30.0, 31.0, 31.00, 31.39, 50.0, 49.38, 50.0, 4.0, 3.70, 4.30, 0.0, None),
    ("ISO_SMALL_A", "M33", 33.0, 34.0, 34.00, 34.39, 56.0, 55.26, 56.0, 5.0, 4.40, 5.60, 0.0, None),
    ("ISO_SMALL_A", "M36", 36.0, 37.0, 37.00, 37.39, 60.0, 59.26, 60.0, 5.0, 4.40, 5.60, 0.0, None),

    # --------------------------------------------------------------------------
    # 5. ISO 7093-1 - LARGE SERIES GRADE A (VÀNH LỚN CẤP A)
    # --------------------------------------------------------------------------
    ("ISO_LARGE_A", "M3", 3.0, 3.2, 3.20, 3.38, 9.0, 8.64, 9.0, 0.8, 0.70, 0.90, 0.0, None),
    ("ISO_LARGE_A", "M3.5", 3.5, 3.7, 3.70, 3.88, 11.0, 10.57, 11.0, 0.8, 0.70, 0.90, 0.0, None),
    ("ISO_LARGE_A", "M4", 4.0, 4.3, 4.30, 4.48, 12.0, 11.57, 12.0, 1.0, 0.90, 1.10, 0.0, None),
    ("ISO_LARGE_A", "M5", 5.0, 5.3, 5.30, 5.48, 15.0, 14.57, 15.0, 1.2, 1.00, 1.40, 0.0, None),
    ("ISO_LARGE_A", "M6", 6.0, 6.4, 6.40, 6.62, 18.0, 17.57, 18.0, 1.6, 1.40, 1.80, 0.0, None),
    ("ISO_LARGE_A", "M7", 7.0, 7.4, 7.40, 7.62, 22.0, 21.48, 22.0, 2.0, 1.80, 2.20, 0.0, None),
    ("ISO_LARGE_A", "M8", 8.0, 8.4, 8.40, 8.62, 24.0, 23.48, 24.0, 2.0, 1.80, 2.20, 0.0, None),
    ("ISO_LARGE_A", "M10", 10.0, 10.5, 10.50, 10.77, 30.0, 29.48, 30.0, 2.5, 2.30, 2.70, 0.0, None),
    ("ISO_LARGE_A", "M12", 12.0, 13.0, 13.00, 13.27, 37.0, 36.38, 37.0, 3.0, 2.70, 3.30, 0.0, None),
    ("ISO_LARGE_A", "M14", 14.0, 15.0, 15.00, 15.27, 44.0, 43.38, 44.0, 3.0, 2.70, 3.30, 0.0, None),
    ("ISO_LARGE_A", "M16", 16.0, 17.0, 17.00, 17.27, 50.0, 49.38, 50.0, 3.0, 2.70, 3.30, 0.0, None),
    ("ISO_LARGE_A", "M18", 18.0, 19.0, 19.00, 19.33, 56.0, 55.26, 56.0, 4.0, 3.70, 4.30, 0.0, None),
    ("ISO_LARGE_A", "M20", 20.0, 21.0, 21.00, 21.33, 60.0, 59.26, 60.0, 4.0, 3.70, 4.30, 0.0, None),
    ("ISO_LARGE_A", "M22", 22.0, 23.0, 23.00, 23.33, 66.0, 65.26, 66.0, 5.0, 4.40, 5.60, 0.0, None),
    ("ISO_LARGE_A", "M24", 24.0, 25.0, 25.00, 25.33, 72.0, 71.26, 72.0, 5.0, 4.40, 5.60, 0.0, None),
    ("ISO_LARGE_A", "M27", 27.0, 28.0, 28.00, 28.33, 85.0, 83.60, 85.0, 6.0, 5.40, 6.60, 0.0, None),
    ("ISO_LARGE_A", "M30", 30.0, 31.0, 31.00, 31.39, 92.0, 90.60, 92.0, 6.0, 5.40, 6.60, 0.0, None),
    ("ISO_LARGE_A", "M33", 33.0, 34.0, 34.00, 34.39, 105.0, 103.60, 105.0, 6.0, 5.40, 6.60, 0.0, None),
    ("ISO_LARGE_A", "M36", 36.0, 37.0, 37.00, 37.39, 110.0, 108.60, 110.0, 8.0, 7.00, 9.00, 0.0, None),

    # --------------------------------------------------------------------------
    # 6. ISO 7093-2 - LARGE SERIES GRADE C (VÀNH LỚN CẤP C)
    # --------------------------------------------------------------------------
    ("ISO_LARGE_C", "M3", 3.0, 3.2, 3.20, 3.45, 9.0, 8.10, 9.0, 0.8, 0.60, 1.00, 0.0, None),
    ("ISO_LARGE_C", "M3.5", 3.5, 3.7, 3.70, 3.95, 11.0, 9.90, 11.0, 0.8, 0.60, 1.00, 0.0, None),
    ("ISO_LARGE_C", "M4", 4.0, 4.3, 4.30, 4.60, 12.0, 10.90, 12.0, 1.0, 0.80, 1.20, 0.0, None),
    ("ISO_LARGE_C", "M5", 5.0, 5.3, 5.30, 5.60, 15.0, 13.90, 15.0, 1.2, 0.90, 1.50, 0.0, None),
    ("ISO_LARGE_C", "M6", 6.0, 6.4, 6.40, 6.76, 18.0, 16.90, 18.0, 1.6, 1.30, 1.90, 0.0, None),
    ("ISO_LARGE_C", "M7", 7.0, 7.4, 7.40, 7.76, 22.0, 20.70, 22.0, 2.0, 1.70, 2.30, 0.0, None),
    ("ISO_LARGE_C", "M8", 8.0, 8.4, 8.40, 8.76, 24.0, 22.70, 24.0, 2.0, 1.70, 2.30, 0.0, None),
    ("ISO_LARGE_C", "M10", 10.0, 10.5, 10.50, 10.93, 30.0, 28.70, 30.0, 2.5, 2.10, 2.90, 0.0, None),
    ("ISO_LARGE_C", "M12", 12.0, 13.0, 13.00, 13.43, 37.0, 35.40, 37.0, 3.0, 2.50, 3.50, 0.0, None),
    ("ISO_LARGE_C", "M14", 14.0, 15.0, 15.00, 15.43, 44.0, 42.40, 44.0, 3.0, 2.50, 3.50, 0.0, None),
    ("ISO_LARGE_C", "M16", 16.0, 17.0, 17.00, 17.43, 50.0, 48.40, 50.0, 3.0, 2.50, 3.50, 0.0, None),
    ("ISO_LARGE_C", "M18", 18.0, 19.0, 19.00, 19.52, 56.0, 54.10, 56.0, 4.0, 3.40, 4.60, 0.0, None),
    ("ISO_LARGE_C", "M20", 20.0, 21.0, 21.00, 21.52, 60.0, 58.10, 60.0, 4.0, 3.40, 4.60, 0.0, None),
    ("ISO_LARGE_C", "M22", 22.0, 23.0, 23.00, 23.52, 66.0, 64.10, 66.0, 5.0, 4.20, 5.80, 0.0, None),
    ("ISO_LARGE_C", "M24", 24.0, 25.0, 25.00, 25.52, 72.0, 70.10, 72.0, 5.0, 4.20, 5.80, 0.0, None),
    ("ISO_LARGE_C", "M27", 27.0, 28.0, 28.00, 28.52, 85.0, 82.80, 85.0, 6.0, 5.10, 6.90, 0.0, None),
    ("ISO_LARGE_C", "M30", 30.0, 31.0, 31.00, 31.62, 92.0, 89.80, 92.0, 6.0, 5.10, 6.90, 0.0, None),
    ("ISO_LARGE_C", "M33", 33.0, 34.0, 34.00, 34.62, 105.0, 102.80, 105.0, 6.0, 5.10, 6.90, 0.0, None),
    ("ISO_LARGE_C", "M36", 36.0, 37.0, 37.00, 37.62, 110.0, 107.80, 110.0, 8.0, 6.80, 9.20, 0.0, None),

    # --------------------------------------------------------------------------
    # 7. ISO 7094 - EXTRA LARGE SERIES GRADE C (VÀNH CỰC LỚN CHO KẾT CẤU GỖ)
    # --------------------------------------------------------------------------
    ("ISO_EXTRA_LARGE_C", "M5", 5.0, 5.5, 5.50, 5.80, 18.0, 16.90, 18.0, 2.0, 1.70, 2.30, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M6", 6.0, 6.6, 6.60, 6.96, 22.0, 20.70, 22.0, 2.0, 1.70, 2.30, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M8", 8.0, 9.0, 9.00, 9.36, 28.0, 26.70, 28.0, 3.0, 2.50, 3.50, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M10", 10.0, 11.0, 11.00, 11.43, 34.0, 32.40, 34.0, 3.0, 2.50, 3.50, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M12", 12.0, 13.5, 13.50, 13.93, 44.0, 42.40, 44.0, 4.0, 3.40, 4.60, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M14", 14.0, 15.5, 15.50, 15.93, 50.0, 48.40, 50.0, 4.0, 3.40, 4.60, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M16", 16.0, 17.5, 17.50, 17.93, 56.0, 54.10, 56.0, 5.0, 4.20, 5.80, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M18", 18.0, 20.0, 20.00, 20.52, 60.0, 58.10, 60.0, 5.0, 4.20, 5.80, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M20", 20.0, 22.0, 22.00, 22.52, 72.0, 70.10, 72.0, 6.0, 5.10, 6.90, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M22", 22.0, 24.0, 24.00, 24.52, 80.0, 78.10, 80.0, 6.0, 5.10, 6.90, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M24", 24.0, 26.0, 26.00, 26.52, 85.0, 82.80, 85.0, 6.0, 5.10, 6.90, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M27", 27.0, 30.0, 30.00, 30.52, 98.0, 95.80, 98.0, 6.0, 5.10, 6.90, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M30", 30.0, 33.0, 33.00, 33.62, 105.0, 102.80, 105.0, 6.0, 5.10, 6.90, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M33", 33.0, 36.0, 36.00, 36.62, 115.0, 112.80, 115.0, 8.0, 6.80, 9.20, 0.0, None),
    ("ISO_EXTRA_LARGE_C", "M36", 36.0, 39.0, 39.00, 39.62, 125.0, 122.80, 125.0, 8.0, 6.80, 9.20, 0.0, None),

    # --------------------------------------------------------------------------
    # 8. ANNEX JA - SQUARE WASHERS (VÒNG ĐỆM VUÔNG - d2 ở đây là kích thước cạnh a)
    # --------------------------------------------------------------------------
    ("ANNEX_JA_SQUARE", "M6", 6.0, 7.0, 7.0, 7.4, 20.0, 19.2, 20.8, 2.0, 1.7, 2.3, 0.0, None),
    ("ANNEX_JA_SQUARE", "M8", 8.0, 9.0, 9.0, 9.4, 26.0, 25.0, 27.0, 2.3, 2.0, 2.6, 0.0, None),
    ("ANNEX_JA_SQUARE", "M10", 10.0, 11.0, 11.0, 11.5, 32.0, 31.0, 33.0, 2.3, 2.0, 2.6, 0.0, None),
    ("ANNEX_JA_SQUARE", "M12", 12.0, 13.5, 13.5, 14.1, 40.0, 38.5, 41.5, 3.2, 2.8, 3.6, 0.0, None),
    ("ANNEX_JA_SQUARE", "M16", 16.0, 17.5, 17.5, 18.2, 52.0, 50.0, 54.0, 4.5, 4.0, 5.0, 0.0, None),
    ("ANNEX_JA_SQUARE", "M20", 20.0, 22.0, 22.0, 22.8, 68.0, 66.0, 70.0, 6.0, 5.3, 6.7, 0.0, None),
    ("ANNEX_JA_SQUARE", "M22", 22.0, 24.0, 24.0, 24.8, 74.0, 72.0, 76.0, 6.0, 5.3, 6.7, 0.0, None),
    ("ANNEX_JA_SQUARE", "M24", 24.0, 26.0, 26.0, 26.8, 80.0, 78.0, 82.0, 6.0, 5.3, 6.7, 0.0, None),

    # --------------------------------------------------------------------------
    # 9. JIS B 1250 - POLISHED ROUND (VÒNG ĐỆM TRÒN MÀI BÓNG ミガキ丸)
    # --------------------------------------------------------------------------
    ("JIS_POLISHED_ROUND", "M6", 6.0, 6.5, 6.5, 6.8, 11.5, 11.0, 11.5, 1.2, 1.0, 1.4, 0.0, None),
    ("JIS_POLISHED_ROUND", "M8", 8.0, 8.5, 8.5, 8.8, 15.5, 15.0, 15.5, 1.6, 1.4, 1.8, 0.0, None),
    ("JIS_POLISHED_ROUND", "M10", 10.0, 10.5, 10.5, 10.9, 18.5, 18.0, 18.5, 1.6, 1.4, 1.8, 0.0, None),
    ("JIS_POLISHED_ROUND", "M12", 12.0, 13.0, 13.0, 13.4, 21.0, 20.4, 21.0, 2.0, 1.8, 2.2, 0.0, None),
    ("JIS_POLISHED_ROUND", "M16", 16.0, 17.0, 17.0, 17.4, 28.0, 27.4, 28.0, 2.6, 2.3, 2.9, 0.0, None),
    ("JIS_POLISHED_ROUND", "M20", 20.0, 21.0, 21.0, 21.5, 34.0, 33.3, 34.0, 3.2, 2.8, 3.6, 0.0, None),
    ("JIS_POLISHED_ROUND", "M22", 22.0, 23.0, 23.0, 23.5, 39.0, 38.3, 39.0, 3.2, 2.8, 3.6, 0.0, None),
    ("JIS_POLISHED_ROUND", "M24", 24.0, 26.0, 26.0, 26.5, 44.0, 43.3, 44.0, 4.0, 3.5, 4.5, 0.0, None),

    # --------------------------------------------------------------------------
    # 10. JIS B 1250 - COMMERCIAL ROUND (VÒNG ĐỆM TRÒN THÔNG DỤNG 並丸)
    # --------------------------------------------------------------------------
    ("JIS_COMMERCIAL_ROUND", "M6", 6.0, 6.5, 6.5, 6.9, 13.0, 12.0, 13.0, 1.0, 0.8, 1.2, 0.0, None),
    ("JIS_COMMERCIAL_ROUND", "M8", 8.0, 8.5, 8.5, 8.9, 18.0, 17.0, 18.0, 1.6, 1.3, 1.9, 0.0, None),
    ("JIS_COMMERCIAL_ROUND", "M10", 10.0, 10.5, 10.5, 11.0, 22.0, 21.0, 22.0, 1.6, 1.3, 1.9, 0.0, None),
    ("JIS_COMMERCIAL_ROUND", "M12", 12.0, 13.0, 13.0, 13.5, 26.0, 25.0, 26.0, 2.3, 1.9, 2.7, 0.0, None),
    ("JIS_COMMERCIAL_ROUND", "M16", 16.0, 17.0, 17.0, 17.5, 32.0, 30.8, 32.0, 3.2, 2.7, 3.7, 0.0, None),
    ("JIS_COMMERCIAL_ROUND", "M20", 20.0, 21.0, 21.0, 21.6, 40.0, 38.8, 40.0, 3.2, 2.7, 3.7, 0.0, None),
    ("JIS_COMMERCIAL_ROUND", "M22", 22.0, 23.0, 23.0, 23.6, 44.0, 42.8, 44.0, 3.2, 2.7, 3.7, 0.0, None),
    ("JIS_COMMERCIAL_ROUND", "M24", 24.0, 26.0, 26.0, 26.6, 48.0, 46.8, 48.0, 4.0, 3.4, 4.6, 0.0, None),
]


# ==============================================================================
# 4. HÀM TẠO VÀ NẠP CSDL SQLITE (jis_b1256.sqlite)
# ==============================================================================
def create_and_seed_sqlite():
    """Khởi tạo cấu trúc và nạp toàn bộ dữ liệu vào SQLite."""
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Bảng 1: Danh mục chủng loại vòng đệm
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jis_b1256_washer_types (
            type_id INTEGER PRIMARY KEY,
            type_code TEXT UNIQUE NOT NULL,
            type_name_ja TEXT NOT NULL,
            type_name_en TEXT NOT NULL,
            iso_standard TEXT,
            washer_series TEXT NOT NULL,
            product_grade TEXT NOT NULL,
            dimension_series TEXT NOT NULL,
            is_flange_default INTEGER DEFAULT 0,
            description_vi TEXT
        )
    """)

    # Bảng 2: Kích thước chi tiết
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jis_b1256_washer_dimensions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            standard TEXT NOT NULL DEFAULT 'JIS_B_1256',
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
            chamfer_c REAL,
            UNIQUE(series, bolt_size)
        )
    """)

    # Bảng 3: Cơ tính và cấp độ cứng
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jis_b1256_hardness_specs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hardness_class TEXT UNIQUE NOT NULL,
            min_hv REAL NOT NULL,
            max_hv REAL NOT NULL,
            applicable_bolts TEXT,
            description_vi TEXT
        )
    """)

    # Nạp dữ liệu chủng loại
    cur.executemany("""
        INSERT INTO jis_b1256_washer_types (
            type_id, type_code, type_name_ja, type_name_en, iso_standard,
            washer_series, product_grade, dimension_series, is_flange_default, description_vi
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, WASHER_TYPES_DATA)

    # Nạp dữ liệu kích thước
    dim_rows_with_std = []
    for d in WASHER_DIMENSIONS_DATA:
        # (series, bolt_size, nominal_dia, d1_nom, d1_min, d1_max, d2_nom, d2_min, d2_max, h_nom, h_min, h_max, chamfer_angle_deg, chamfer_c)
        dim_rows_with_std.append(("JIS_B_1256", *d))

    cur.executemany("""
        INSERT INTO jis_b1256_washer_dimensions (
            standard, series, bolt_size, nominal_dia,
            d1_nominal, d1_min, d1_max,
            d2_nominal, d2_min, d2_max,
            h_nominal, h_min, h_max,
            chamfer_angle_deg, chamfer_c
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, dim_rows_with_std)

    # Nạp dữ liệu cơ tính
    cur.executemany("""
        INSERT INTO jis_b1256_hardness_specs (
            hardness_class, min_hv, max_hv, applicable_bolts, description_vi
        ) VALUES (?, ?, ?, ?, ?)
    """, HARDNESS_SPECS_DATA)

    # Tạo chỉ mục
    cur.execute("CREATE INDEX IF NOT EXISTS idx_b1256_dim ON jis_b1256_washer_dimensions(series, bolt_size)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_b1256_types ON jis_b1256_washer_types(type_code)")

    conn.commit()
    conn.close()
    print(f"-> Tạo thành công CSDL SQLite: {DB_PATH}")


# ==============================================================================
# 5. HÀM TẠO DATASET PYTHON THUẦN (ZERO-IO CACHE TRONG RAM)
# ==============================================================================
def generate_python_dataset():
    """Tạo file Python thuần chứa dữ liệu tĩnh phục vụ tra cứu RAM tức thời."""
    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        f.write('"""Bộ dữ liệu tĩnh chuẩn JIS B 1256 : 2008 cho AutoCAD Plant 3D (Không phụ thuộc SQLite)."""\n')
        f.write("from ..models.jis_b1256_specs import WasherDimensionSpec, WasherTypeSpec\n\n")

        # 1. Danh mục chủng loại
        f.write("# Danh mục 10 chủng loại vòng đệm trong JIS B 1256 : 2008 & hệ liên quan\n")
        f.write("JIS_B1256_WASHER_TYPES = {\n")
        for item in WASHER_TYPES_DATA:
            t_id, t_code, t_ja, t_en, iso, series, grade, dim_ser, def_flg, desc = item
            f.write(f'    "{t_code}": WasherTypeSpec(\n')
            f.write('        standard="JIS_B_1256",\n')
            f.write(f"        type_id={t_id},\n")
            f.write(f'        type_code="{t_code}",\n')
            f.write(f'        type_name_ja="{t_ja}",\n')
            f.write(f'        type_name_en="{t_en}",\n')
            f.write(f'        iso_standard="{iso}",\n')
            f.write(f'        washer_series="{series}",\n')
            f.write(f'        product_grade="{grade}",\n')
            f.write(f'        dimension_series="{dim_ser}",\n')
            f.write(f"        is_flange_default={bool(def_flg)},\n")
            f.write(f'        description_vi="{desc}"\n')
            f.write("    ),\n")
        f.write("}\n\n")

        # 2. Cấp độ cứng
        f.write("# Bảng cấp độ cứng Vickers và bu lông tương ứng\n")
        f.write("JIS_B1256_HARDNESS_SPECS = {\n")
        for h_cls, min_hv, max_hv, b_appl, desc in HARDNESS_SPECS_DATA:
            f.write(f'    "{h_cls}": {{\n')
            f.write(f'        "hardness_class": "{h_cls}",\n')
            f.write(f'        "min_hv": {min_hv},\n')
            f.write(f'        "max_hv": {max_hv},\n')
            f.write(f'        "applicable_bolts": "{b_appl}",\n')
            f.write(f'        "description_vi": "{desc}",\n')
            f.write("    },\n")
        f.write("}\n\n")

        # 3. Kích thước chi tiết
        f.write("# Kích thước hình học chi tiết từng cỡ ren theo series\n")
        f.write("JIS_B1256_WASHER_DIMENSIONS = {\n")
        for dim in WASHER_DIMENSIONS_DATA:
            ser, sz, nom_d, d1_n, d1_min, d1_max, d2_n, d2_min, d2_max, h_n, h_min, h_max, c_ang, c_c = dim
            c_c_val = f"{c_c}" if c_c is not None else "None"
            f.write(f'    ("{ser}", "{sz}"): WasherDimensionSpec(\n')
            f.write('        standard="JIS_B_1256",\n')
            f.write(f'        series="{ser}",\n')
            f.write(f'        bolt_size="{sz}",\n')
            f.write(f"        nominal_dia={nom_d},\n")
            f.write(f"        d1_nominal={d1_n},\n")
            f.write(f"        d1_min={d1_min},\n")
            f.write(f"        d1_max={d1_max},\n")
            f.write(f"        d2_nominal={d2_n},\n")
            f.write(f"        d2_min={d2_min},\n")
            f.write(f"        d2_max={d2_max},\n")
            f.write(f"        h_nominal={h_n},\n")
            f.write(f"        h_min={h_min},\n")
            f.write(f"        h_max={h_max},\n")
            f.write(f"        chamfer_angle_deg={c_ang},\n")
            f.write(f"        chamfer_c={c_c_val}\n")
            f.write("    ),\n")
        f.write("}\n")

    print(f"-> Tạo thành công dataset Python: {DATASET_PATH}")


if __name__ == "__main__":
    create_and_seed_sqlite()
    generate_python_dataset()
    print("=== HOÀN TẤT TÍCH HỢP CƠ SỞ DỮ LIỆU JIS B 1256 ===")
