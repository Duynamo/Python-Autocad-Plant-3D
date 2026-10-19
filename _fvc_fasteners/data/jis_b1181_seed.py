"""Script khởi tạo CSDL SQLite và dataset Python thuần cho đai ốc lục giác JIS B 1181 : 2014."""
import os
import sqlite3
import sys
from typing import Dict, Tuple

# Đảm bảo xuất UTF-8 trên mọi môi trường
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATA_DIR, "jis_b1181.sqlite")
DATASET_PATH = os.path.join(DATA_DIR, "jis_b1181_dataset.py")

# ==============================================================================
# 1. DANH MỤC 12 CHỦNG LOẠI ĐAI ỐC CHUẨN THEO JIS B 1181 : 2014
# ==============================================================================
# (type_id, type_code, type_name_ja, type_name_en, iso_standard, nut_style, pitch_type, product_grade, dimension_series, is_flange_default, description_vi)
NUT_TYPES_DATA = [
    (
        1,
        "ISO_4032_STYLE_1_COARSE",
        "六角ナット−スタイル1 (並目)",
        "Hexagon regular nut (Style 1) Coarse",
        "ISO 4032",
        "STYLE_1",
        "COARSE",
        "GRADE_AB",
        "ISO_STYLE_1",
        1,
        "Đai ốc lục giác tiêu chuẩn Style 1 ren thô, cấp A & B có gờ đệm (Mặc định chuẩn cho mặt bích đường ống)"
    ),
    (
        2,
        "ISO_8673_STYLE_1_FINE",
        "六角ナット−スタイル1 (細目)",
        "Hexagon regular nut (Style 1) Fine",
        "ISO 8673",
        "STYLE_1",
        "FINE",
        "GRADE_AB",
        "ISO_STYLE_1",
        0,
        "Đai ốc lục giác tiêu chuẩn Style 1 ren mịn, cấp A & B có gờ đệm (Chống rung lắc nới lỏng, chỉnh định chính xác)"
    ),
    (
        3,
        "ISO_4034_STYLE_1_GRADE_C",
        "六角ナット−C (並目)",
        "Hexagon nut Product Grade C",
        "ISO 4034",
        "STYLE_1",
        "COARSE",
        "GRADE_C",
        "ISO_GRADE_C",
        0,
        "Đai ốc lục giác ren thô cấp C thương mại (Mặt tỳ phẳng tự nhiên, kết cấu thép nhà xưởng kinh tế)"
    ),
    (
        4,
        "ISO_4033_STYLE_2_COARSE",
        "六角ナット−スタイル2 (並目)",
        "Hexagon high nut (Style 2) Coarse",
        "ISO 4033",
        "STYLE_2",
        "COARSE",
        "GRADE_AB",
        "ISO_STYLE_2",
        0,
        "Đai ốc lục giác dày Style 2 ren thô (Thành cao m ≈ 1.0d, chịu tải trọng chứng minh Proof Load lớn, cấp bền 9, 12)"
    ),
    (
        5,
        "ISO_8674_STYLE_2_FINE",
        "六角ナット−スタイル2 (細目)",
        "Hexagon high nut (Style 2) Fine",
        "ISO 8674",
        "STYLE_2",
        "FINE",
        "GRADE_AB",
        "ISO_STYLE_2",
        0,
        "Đai ốc lục giác dày Style 2 ren mịn (Thành cao ren mịn chịu tải cực hạn và chống rung lắc)"
    ),
    (
        6,
        "ISO_4035_STYLE_0_THIN_COARSE",
        "六角低ナット−両面取り (並目)",
        "Hexagon thin nut chamfered Coarse",
        "ISO 4035",
        "STYLE_0_THIN",
        "COARSE",
        "GRADE_AB",
        "ISO_STYLE_0_THIN",
        0,
        "Đai ốc lục giác mỏng Style 0 vát mép 2 mặt ren thô (m ≈ 0.5d, dùng làm đai ốc khóa chống tuột Jam Nut / Lock Nut)"
    ),
    (
        7,
        "ISO_8675_STYLE_0_THIN_FINE",
        "六角低ナット−両面取り (細目)",
        "Hexagon thin nut chamfered Fine",
        "ISO 8675",
        "STYLE_0_THIN",
        "FINE",
        "GRADE_AB",
        "ISO_STYLE_0_THIN",
        0,
        "Đai ốc lục giác mỏng Style 0 vát mép 2 mặt ren mịn (Dùng làm đai ốc hãm trong không gian giới hạn chiều trục)"
    ),
    (
        8,
        "ISO_4036_STYLE_0_UNCHAMFERED",
        "六角低ナット−面取りなし",
        "Hexagon thin nut unchamfered",
        "ISO 4036",
        "STYLE_0_THIN",
        "COARSE",
        "GRADE_B",
        "ISO_STYLE_0_UNCHAMFERED",
        0,
        "Đai ốc lục giác mỏng không vát mép (Mép dập phẳng vuông, dùng cho thiết bị điện tử, cơ cấu phụ lực nhẹ M1.6 - M10)"
    ),
    (
        9,
        "JA_TYPE_1_REGULAR",
        "附属書JA 六角ナット 1種",
        "JIS Annex JA Nut Type 1",
        "ANNEX_JA",
        "ANNEX_JA",
        "COARSE_AND_FINE",
        "JIS_JA",
        "ANNEX_JA_REGULAR",
        0,
        "Đai ốc lục giác hệ truyền thống Nhật Bản Loại 1 (Vát mép 1 mặt, mặt đáy phẳng tỳ sát, thông dụng nội địa Nhật)"
    ),
    (
        10,
        "JA_TYPE_2_REGULAR",
        "附属書JA 六角ナット 2種",
        "JIS Annex JA Nut Type 2",
        "ANNEX_JA",
        "ANNEX_JA",
        "COARSE_AND_FINE",
        "JIS_JA",
        "ANNEX_JA_REGULAR",
        0,
        "Đai ốc lục giác hệ truyền thống Nhật Bản Loại 2 (Vát mép 2 mặt đối xứng, thuận tiện cấp liệu và lắp ráp tự động)"
    ),
    (
        11,
        "JA_TYPE_3_THIN",
        "附属書JA 六角低ナット 3種",
        "JIS Annex JA Thin Nut Type 3",
        "ANNEX_JA",
        "ANNEX_JA",
        "COARSE_AND_FINE",
        "JIS_JA",
        "ANNEX_JA_THIN",
        0,
        "Đai ốc lục giác mỏng hệ truyền thống Nhật Bản Loại 3 (m ≈ 0.5d - 0.6d, chuyên làm đai ốc khóa chống nới lỏng)"
    ),
    (
        12,
        "JA_TYPE_4_WASHER_FACE",
        "附属書JA 六角ナット 4種",
        "JIS Annex JA Nut Type 4",
        "ANNEX_JA",
        "ANNEX_JA",
        "COARSE_AND_FINE",
        "JIS_JA",
        "ANNEX_JA_REGULAR",
        0,
        "Đai ốc lục giác hệ truyền thống Nhật Bản Loại 4 (Vát mép 1 mặt, mặt kia có gờ đệm tròn/lõm thay thế vòng đệm phẳng)"
    ),
]

# ==============================================================================
# 2. BƯỚC REN CHUẨN JIS B 1181 (COARSE VÀ FINE)
# ==============================================================================
PITCH_DATA = {
    "M1.6": (1.6, 0.35, None),
    "M2": (2.0, 0.4, None),
    "M2.5": (2.5, 0.45, None),
    "M3": (3.0, 0.5, None),
    "M4": (4.0, 0.7, None),
    "M5": (5.0, 0.8, None),
    "M6": (6.0, 1.0, 0.75),
    "M8": (8.0, 1.25, 1.0),
    "M10": (10.0, 1.5, 1.25),
    "M12": (12.0, 1.75, 1.25),
    "M14": (14.0, 2.0, 1.5),
    "M16": (16.0, 2.0, 1.5),
    "M18": (18.0, 2.5, 1.5),
    "M20": (20.0, 2.5, 1.5),
    "M22": (22.0, 2.5, 1.5),
    "M24": (24.0, 3.0, 2.0),
    "M27": (27.0, 3.0, 2.0),
    "M30": (30.0, 3.5, 2.0),
    "M30x3": (30.0, 3.0, 3.0),
    "M33": (33.0, 3.5, 2.0),
    "M36": (36.0, 4.0, 3.0),
    "M36x3": (36.0, 3.0, 3.0),
    "M39": (39.0, 4.0, 3.0),
    "M39x3": (39.0, 3.0, 3.0),
    "M42": (42.0, 4.5, 3.0),
    "M42x3": (42.0, 3.0, 3.0),
    "M45": (45.0, 4.5, 3.0),
    "M48": (48.0, 5.0, 3.0),
    "M48x3": (48.0, 3.0, 3.0),
    "M52": (52.0, 5.0, 3.0),
    "M56": (56.0, 5.5, 4.0),
    "M56x4": (56.0, 4.0, 4.0),
    "M60": (60.0, 5.5, 4.0),
    "M64": (64.0, 6.0, 4.0),
    "M64x4": (64.0, 4.0, 4.0),
}

# ==============================================================================
# 3. KÍCH THƯỚC HÌNH HỌC ĐAI ỐC CHI TIẾT THEO TIÊU CHUẨN JIS B 1181 : 2014
# ==============================================================================
# (series, nut_size, nominal_dia, pitch, s_nominal, s_min, s_max, m_nominal, m_min, m_max, e_min, dw_min, da_min, da_max, chamfer_angle_deg, chamfer_sides)
NUT_DIMENSIONS_DATA = [
    # -------------------------------------------------------------------------
    # A. ISO STYLE 1 (ISO 4032 / ISO 8673 - Tiêu chuẩn cơ bản, mặc định bích)
    # -------------------------------------------------------------------------
    ("ISO_STYLE_1", "M1.6", 1.6, 0.35, 3.2, 3.02, 3.2, 1.3, 1.05, 1.3, 3.41, 2.4, 1.6, 1.84, 30.0, 2),
    ("ISO_STYLE_1", "M2", 2.0, 0.4, 4.0, 3.82, 4.0, 1.6, 1.35, 1.6, 4.32, 3.1, 2.0, 2.3, 30.0, 2),
    ("ISO_STYLE_1", "M2.5", 2.5, 0.45, 5.0, 4.82, 5.0, 2.0, 1.75, 2.0, 5.45, 4.1, 2.5, 2.9, 30.0, 2),
    ("ISO_STYLE_1", "M3", 3.0, 0.5, 5.5, 5.32, 5.5, 2.4, 2.15, 2.4, 6.01, 4.6, 3.0, 3.45, 30.0, 2),
    ("ISO_STYLE_1", "M4", 4.0, 0.7, 7.0, 6.78, 7.0, 3.2, 2.9, 3.2, 7.66, 5.9, 4.0, 4.6, 30.0, 2),
    ("ISO_STYLE_1", "M5", 5.0, 0.8, 8.0, 7.78, 8.0, 4.7, 4.4, 4.7, 8.79, 6.9, 5.0, 5.75, 30.0, 2),
    ("ISO_STYLE_1", "M6", 6.0, 1.0, 10.0, 9.78, 10.0, 5.2, 4.9, 5.2, 11.05, 8.9, 6.0, 6.75, 30.0, 2),
    ("ISO_STYLE_1", "M8", 8.0, 1.25, 13.0, 12.73, 13.0, 6.8, 6.44, 6.8, 14.38, 11.6, 8.0, 8.75, 30.0, 2),
    ("ISO_STYLE_1", "M10", 10.0, 1.5, 16.0, 15.73, 16.0, 8.4, 8.04, 8.4, 17.77, 14.6, 10.0, 10.8, 30.0, 2),
    ("ISO_STYLE_1", "M12", 12.0, 1.75, 18.0, 17.73, 18.0, 10.8, 10.37, 10.8, 20.03, 16.6, 12.0, 13.0, 30.0, 2),
    ("ISO_STYLE_1", "M14", 14.0, 2.0, 21.0, 20.67, 21.0, 12.8, 12.1, 12.8, 23.36, 19.6, 14.0, 15.1, 30.0, 2),
    ("ISO_STYLE_1", "M16", 16.0, 2.0, 24.0, 23.67, 24.0, 14.8, 14.1, 14.8, 26.75, 22.5, 16.0, 17.3, 30.0, 2),
    ("ISO_STYLE_1", "M18", 18.0, 2.5, 27.0, 26.16, 27.0, 15.8, 15.1, 15.8, 29.56, 24.9, 18.0, 19.5, 30.0, 2),
    ("ISO_STYLE_1", "M20", 20.0, 2.5, 30.0, 29.16, 30.0, 18.0, 16.9, 18.0, 32.95, 27.7, 20.0, 21.6, 30.0, 2),
    ("ISO_STYLE_1", "M22", 22.0, 2.5, 34.0, 33.0, 34.0, 19.4, 18.1, 19.4, 37.29, 31.4, 22.0, 23.7, 30.0, 2),
    ("ISO_STYLE_1", "M24", 24.0, 3.0, 36.0, 35.0, 36.0, 21.5, 20.2, 21.5, 39.55, 33.2, 24.0, 25.9, 30.0, 2),
    ("ISO_STYLE_1", "M27", 27.0, 3.0, 41.0, 40.0, 41.0, 23.8, 22.5, 23.8, 45.20, 38.0, 27.0, 29.1, 30.0, 2),
    ("ISO_STYLE_1", "M30", 30.0, 3.5, 46.0, 45.0, 46.0, 25.6, 24.3, 25.6, 50.85, 42.8, 30.0, 32.4, 30.0, 2),
    ("ISO_STYLE_1", "M30x3", 30.0, 3.0, 46.0, 45.0, 46.0, 25.6, 24.3, 25.6, 50.85, 42.8, 30.0, 32.4, 30.0, 2),
    ("ISO_STYLE_1", "M33", 33.0, 3.5, 50.0, 49.0, 50.0, 28.7, 27.4, 28.7, 55.37, 46.6, 33.0, 35.6, 30.0, 2),
    ("ISO_STYLE_1", "M36", 36.0, 4.0, 55.0, 53.8, 55.0, 31.0, 29.4, 31.0, 60.79, 51.1, 36.0, 38.9, 30.0, 2),
    ("ISO_STYLE_1", "M36x3", 36.0, 3.0, 55.0, 53.8, 55.0, 31.0, 29.4, 31.0, 60.79, 51.1, 36.0, 38.9, 30.0, 2),
    ("ISO_STYLE_1", "M39", 39.0, 4.0, 60.0, 58.8, 60.0, 33.4, 31.8, 33.4, 66.44, 55.9, 39.0, 42.1, 30.0, 2),
    ("ISO_STYLE_1", "M39x3", 39.0, 3.0, 60.0, 58.8, 60.0, 33.4, 31.8, 33.4, 66.44, 55.9, 39.0, 42.1, 30.0, 2),
    ("ISO_STYLE_1", "M42", 42.0, 4.5, 65.0, 63.1, 65.0, 34.0, 32.4, 34.0, 71.30, 60.0, 42.0, 45.4, 30.0, 2),
    ("ISO_STYLE_1", "M42x3", 42.0, 3.0, 65.0, 63.1, 65.0, 34.0, 32.4, 34.0, 71.30, 60.0, 42.0, 45.4, 30.0, 2),
    ("ISO_STYLE_1", "M45", 45.0, 4.5, 70.0, 68.1, 70.0, 36.0, 34.4, 36.0, 76.95, 64.7, 45.0, 48.6, 30.0, 2),
    ("ISO_STYLE_1", "M48", 48.0, 5.0, 75.0, 73.1, 75.0, 38.0, 36.4, 38.0, 82.60, 69.4, 48.0, 51.8, 30.0, 2),
    ("ISO_STYLE_1", "M48x3", 48.0, 3.0, 75.0, 73.1, 75.0, 38.0, 36.4, 38.0, 82.60, 69.4, 48.0, 51.8, 30.0, 2),
    ("ISO_STYLE_1", "M52", 52.0, 5.0, 80.0, 78.1, 80.0, 42.0, 40.4, 42.0, 88.25, 74.2, 52.0, 56.2, 30.0, 2),
    ("ISO_STYLE_1", "M56", 56.0, 5.5, 85.0, 82.8, 85.0, 45.0, 43.4, 45.0, 93.56, 78.7, 56.0, 60.5, 30.0, 2),
    ("ISO_STYLE_1", "M56x4", 56.0, 4.0, 85.0, 82.8, 85.0, 45.0, 43.4, 45.0, 93.56, 78.7, 56.0, 60.5, 30.0, 2),
    ("ISO_STYLE_1", "M60", 60.0, 5.5, 90.0, 87.8, 90.0, 48.0, 46.4, 48.0, 99.21, 83.4, 60.0, 64.8, 30.0, 2),
    ("ISO_STYLE_1", "M64", 64.0, 6.0, 95.0, 92.8, 95.0, 51.0, 49.1, 51.0, 104.86, 88.2, 64.0, 69.1, 30.0, 2),
    ("ISO_STYLE_1", "M64x4", 64.0, 4.0, 95.0, 92.8, 95.0, 51.0, 49.1, 51.0, 104.86, 88.2, 64.0, 69.1, 30.0, 2),

    # -------------------------------------------------------------------------
    # B. ISO STYLE 2 (ISO 4033 / ISO 8674 - Đai ốc dày / thành cao chịu tải lớn)
    # -------------------------------------------------------------------------
    ("ISO_STYLE_2", "M5", 5.0, 0.8, 8.0, 7.78, 8.0, 5.1, 4.8, 5.1, 8.79, 6.9, 5.0, 5.75, 30.0, 2),
    ("ISO_STYLE_2", "M6", 6.0, 1.0, 10.0, 9.78, 10.0, 5.7, 5.4, 5.7, 11.05, 8.9, 6.0, 6.75, 30.0, 2),
    ("ISO_STYLE_2", "M8", 8.0, 1.25, 13.0, 12.73, 13.0, 7.5, 7.14, 7.5, 14.38, 11.6, 8.0, 8.75, 30.0, 2),
    ("ISO_STYLE_2", "M10", 10.0, 1.5, 16.0, 15.73, 16.0, 9.3, 8.94, 9.3, 17.77, 14.6, 10.0, 10.8, 30.0, 2),
    ("ISO_STYLE_2", "M12", 12.0, 1.75, 18.0, 17.73, 18.0, 12.0, 11.57, 12.0, 20.03, 16.6, 12.0, 13.0, 30.0, 2),
    ("ISO_STYLE_2", "M14", 14.0, 2.0, 21.0, 20.67, 21.0, 14.1, 13.4, 14.1, 23.36, 19.6, 14.0, 15.1, 30.0, 2),
    ("ISO_STYLE_2", "M16", 16.0, 2.0, 24.0, 23.67, 24.0, 16.4, 15.7, 16.4, 26.75, 22.5, 16.0, 17.3, 30.0, 2),
    ("ISO_STYLE_2", "M18", 18.0, 2.5, 27.0, 26.16, 27.0, 17.6, 16.9, 17.6, 29.56, 24.9, 18.0, 19.5, 30.0, 2),
    ("ISO_STYLE_2", "M20", 20.0, 2.5, 30.0, 29.16, 30.0, 20.3, 19.0, 20.3, 32.95, 27.7, 20.0, 21.6, 30.0, 2),
    ("ISO_STYLE_2", "M22", 22.0, 2.5, 34.0, 33.0, 34.0, 21.8, 20.5, 21.8, 37.29, 31.4, 22.0, 23.7, 30.0, 2),
    ("ISO_STYLE_2", "M24", 24.0, 3.0, 36.0, 35.0, 36.0, 23.9, 22.6, 23.9, 39.55, 33.2, 24.0, 25.9, 30.0, 2),
    ("ISO_STYLE_2", "M27", 27.0, 3.0, 41.0, 40.0, 41.0, 26.7, 25.4, 26.7, 45.20, 38.0, 27.0, 29.1, 30.0, 2),
    ("ISO_STYLE_2", "M30", 30.0, 3.5, 46.0, 45.0, 46.0, 28.6, 27.3, 28.6, 50.85, 42.8, 30.0, 32.4, 30.0, 2),
    ("ISO_STYLE_2", "M30x3", 30.0, 3.0, 46.0, 45.0, 46.0, 28.6, 27.3, 28.6, 50.85, 42.8, 30.0, 32.4, 30.0, 2),
    ("ISO_STYLE_2", "M33", 33.0, 3.5, 50.0, 49.0, 50.0, 32.5, 31.2, 32.5, 55.37, 46.6, 33.0, 35.6, 30.0, 2),
    ("ISO_STYLE_2", "M36", 36.0, 4.0, 55.0, 53.8, 55.0, 34.7, 33.1, 34.7, 60.79, 51.1, 36.0, 38.9, 30.0, 2),
    ("ISO_STYLE_2", "M36x3", 36.0, 3.0, 55.0, 53.8, 55.0, 34.7, 33.1, 34.7, 60.79, 51.1, 36.0, 38.9, 30.0, 2),
    ("ISO_STYLE_2", "M39", 39.0, 4.0, 60.0, 58.8, 60.0, 37.5, 35.9, 37.5, 66.44, 55.9, 39.0, 42.1, 30.0, 2),

    # -------------------------------------------------------------------------
    # C. ISO STYLE 0 (ISO 4035 / ISO 8675 - Đai ốc mỏng / đai ốc hãm)
    # -------------------------------------------------------------------------
    ("ISO_STYLE_0_THIN", "M1.6", 1.6, 0.35, 3.2, 3.02, 3.2, 1.0, 0.75, 1.0, 3.41, 2.4, 1.6, 1.84, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M2", 2.0, 0.4, 4.0, 3.82, 4.0, 1.2, 0.95, 1.2, 4.32, 3.1, 2.0, 2.3, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M2.5", 2.5, 0.45, 5.0, 4.82, 5.0, 1.6, 1.35, 1.6, 5.45, 4.1, 2.5, 2.9, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M3", 3.0, 0.5, 5.5, 5.32, 5.5, 1.8, 1.55, 1.8, 6.01, 4.6, 3.0, 3.45, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M4", 4.0, 0.7, 7.0, 6.78, 7.0, 2.2, 1.95, 2.2, 7.66, 5.9, 4.0, 4.6, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M5", 5.0, 0.8, 8.0, 7.78, 8.0, 2.7, 2.45, 2.7, 8.79, 6.9, 5.0, 5.75, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M6", 6.0, 1.0, 10.0, 9.78, 10.0, 3.2, 2.9, 3.2, 11.05, 8.9, 6.0, 6.75, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M8", 8.0, 1.25, 13.0, 12.73, 13.0, 4.0, 3.7, 4.0, 14.38, 11.6, 8.0, 8.75, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M10", 10.0, 1.5, 16.0, 15.73, 16.0, 5.0, 4.7, 5.0, 17.77, 14.6, 10.0, 10.8, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M12", 12.0, 1.75, 18.0, 17.73, 18.0, 6.0, 5.7, 6.0, 20.03, 16.6, 12.0, 13.0, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M14", 14.0, 2.0, 21.0, 20.67, 21.0, 7.0, 6.42, 7.0, 23.36, 19.6, 14.0, 15.1, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M16", 16.0, 2.0, 24.0, 23.67, 24.0, 8.0, 7.42, 8.0, 26.75, 22.5, 16.0, 17.3, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M18", 18.0, 2.5, 27.0, 26.16, 27.0, 9.0, 8.42, 9.0, 29.56, 24.9, 18.0, 19.5, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M20", 20.0, 2.5, 30.0, 29.16, 30.0, 10.0, 9.1, 10.0, 32.95, 27.7, 20.0, 21.6, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M22", 22.0, 2.5, 34.0, 33.0, 34.0, 11.0, 9.9, 11.0, 37.29, 31.4, 22.0, 23.7, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M24", 24.0, 3.0, 36.0, 35.0, 36.0, 12.0, 10.9, 12.0, 39.55, 33.2, 24.0, 25.9, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M27", 27.0, 3.0, 41.0, 40.0, 41.0, 13.5, 12.4, 13.5, 45.20, 38.0, 27.0, 29.1, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M30", 30.0, 3.5, 46.0, 45.0, 46.0, 15.0, 13.9, 15.0, 50.85, 42.8, 30.0, 32.4, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M30x3", 30.0, 3.0, 46.0, 45.0, 46.0, 15.0, 13.9, 15.0, 50.85, 42.8, 30.0, 32.4, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M36", 36.0, 4.0, 55.0, 53.8, 55.0, 18.0, 16.9, 18.0, 60.79, 51.1, 36.0, 38.9, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M36x3", 36.0, 3.0, 55.0, 53.8, 55.0, 18.0, 16.9, 18.0, 60.79, 51.1, 36.0, 38.9, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M42", 42.0, 4.5, 65.0, 63.1, 65.0, 21.0, 19.7, 21.0, 71.30, 60.0, 42.0, 45.4, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M48", 48.0, 5.0, 75.0, 73.1, 75.0, 24.0, 22.7, 24.0, 82.60, 69.4, 48.0, 51.8, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M56", 56.0, 5.5, 85.0, 82.8, 85.0, 28.0, 26.7, 28.0, 93.56, 78.7, 56.0, 60.5, 30.0, 2),
    ("ISO_STYLE_0_THIN", "M64", 64.0, 6.0, 95.0, 92.8, 95.0, 32.0, 30.4, 32.0, 104.86, 88.2, 64.0, 69.1, 30.0, 2),

    # -------------------------------------------------------------------------
    # D. ISO GRADE C (ISO 4034 - Đai ốc thô không có gờ đệm dw)
    # -------------------------------------------------------------------------
    ("ISO_GRADE_C", "M5", 5.0, 0.8, 8.0, 7.64, 8.0, 4.7, 4.22, 5.18, 8.63, None, 5.0, 5.75, 30.0, 2),
    ("ISO_GRADE_C", "M6", 6.0, 1.0, 10.0, 9.64, 10.0, 5.2, 4.72, 5.68, 10.89, None, 6.0, 6.75, 30.0, 2),
    ("ISO_GRADE_C", "M8", 8.0, 1.25, 13.0, 12.57, 13.0, 6.8, 6.18, 7.42, 14.20, None, 8.0, 8.75, 30.0, 2),
    ("ISO_GRADE_C", "M10", 10.0, 1.5, 16.0, 15.57, 16.0, 8.4, 7.78, 9.02, 17.59, None, 10.0, 10.8, 30.0, 2),
    ("ISO_GRADE_C", "M12", 12.0, 1.75, 18.0, 17.57, 18.0, 10.8, 10.1, 11.5, 19.85, None, 12.0, 13.0, 30.0, 2),
    ("ISO_GRADE_C", "M14", 14.0, 2.0, 21.0, 20.16, 21.0, 12.8, 11.96, 13.64, 22.78, None, 14.0, 15.1, 30.0, 2),
    ("ISO_GRADE_C", "M16", 16.0, 2.0, 24.0, 23.16, 24.0, 14.8, 13.96, 15.64, 26.17, None, 16.0, 17.3, 30.0, 2),
    ("ISO_GRADE_C", "M18", 18.0, 2.5, 27.0, 26.16, 27.0, 15.8, 14.96, 16.64, 29.56, None, 18.0, 19.5, 30.0, 2),
    ("ISO_GRADE_C", "M20", 20.0, 2.5, 30.0, 29.16, 30.0, 18.0, 16.9, 19.1, 32.95, None, 20.0, 21.6, 30.0, 2),
    ("ISO_GRADE_C", "M22", 22.0, 2.5, 34.0, 33.0, 34.0, 19.4, 18.1, 20.7, 37.29, None, 22.0, 23.7, 30.0, 2),
    ("ISO_GRADE_C", "M24", 24.0, 3.0, 36.0, 35.0, 36.0, 21.5, 20.2, 22.8, 39.55, None, 24.0, 25.9, 30.0, 2),
    ("ISO_GRADE_C", "M27", 27.0, 3.0, 41.0, 40.0, 41.0, 23.8, 22.5, 25.1, 45.20, None, 27.0, 29.1, 30.0, 2),
    ("ISO_GRADE_C", "M30", 30.0, 3.5, 46.0, 45.0, 46.0, 25.6, 24.3, 26.9, 50.85, None, 30.0, 32.4, 30.0, 2),
    ("ISO_GRADE_C", "M36", 36.0, 4.0, 55.0, 53.8, 55.0, 31.0, 29.4, 32.6, 60.79, None, 36.0, 38.9, 30.0, 2),
    ("ISO_GRADE_C", "M42", 42.0, 4.5, 65.0, 63.1, 65.0, 34.0, 32.4, 35.6, 71.30, None, 42.0, 45.4, 30.0, 2),
    ("ISO_GRADE_C", "M48", 48.0, 5.0, 75.0, 73.1, 75.0, 38.0, 36.4, 39.6, 82.60, None, 48.0, 51.8, 30.0, 2),
    ("ISO_GRADE_C", "M56", 56.0, 5.5, 85.0, 82.8, 85.0, 45.0, 43.4, 46.6, 93.56, None, 56.0, 60.5, 30.0, 2),
    ("ISO_GRADE_C", "M64", 64.0, 6.0, 95.0, 92.8, 95.0, 51.0, 49.1, 52.9, 104.86, None, 64.0, 69.1, 30.0, 2),

    # -------------------------------------------------------------------------
    # E. ANNEX JA REGULAR (Phụ lục JA truyền thống Nhật Bản: M10=17, M12=19, M14=22, M22=32)
    # -------------------------------------------------------------------------
    ("ANNEX_JA_REGULAR", "M6", 6.0, 1.0, 10.0, 9.78, 10.0, 5.0, 4.7, 5.0, 11.05, 8.9, 6.0, 6.75, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M8", 8.0, 1.25, 13.0, 12.73, 13.0, 6.5, 6.14, 6.5, 14.38, 11.6, 8.0, 8.75, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M10", 10.0, 1.5, 17.0, 16.73, 17.0, 8.0, 7.64, 8.0, 18.90, 15.5, 10.0, 10.8, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M12", 12.0, 1.75, 19.0, 18.67, 19.0, 10.0, 9.64, 10.0, 21.10, 17.5, 12.0, 13.0, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M14", 14.0, 2.0, 22.0, 21.67, 22.0, 11.0, 10.57, 11.0, 24.49, 20.5, 14.0, 15.1, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M16", 16.0, 2.0, 24.0, 23.67, 24.0, 13.0, 12.57, 13.0, 26.75, 22.5, 16.0, 17.3, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M18", 18.0, 2.5, 27.0, 26.16, 27.0, 15.0, 14.3, 15.0, 29.56, 24.9, 18.0, 19.5, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M20", 20.0, 2.5, 30.0, 29.16, 30.0, 16.0, 15.3, 16.0, 32.95, 27.7, 20.0, 21.6, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M22", 22.0, 2.5, 32.0, 31.0, 32.0, 18.0, 17.3, 18.0, 35.03, 29.5, 22.0, 23.7, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M24", 24.0, 3.0, 36.0, 35.0, 36.0, 19.0, 18.1, 19.0, 39.55, 33.2, 24.0, 25.9, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M27", 27.0, 3.0, 41.0, 40.0, 41.0, 22.0, 21.0, 22.0, 45.20, 38.0, 27.0, 29.1, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M30", 30.0, 3.5, 46.0, 45.0, 46.0, 24.0, 23.0, 24.0, 50.85, 42.8, 30.0, 32.4, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M30x3", 30.0, 3.0, 46.0, 45.0, 46.0, 24.0, 23.0, 24.0, 50.85, 42.8, 30.0, 32.4, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M33", 33.0, 3.5, 50.0, 49.0, 50.0, 26.0, 25.0, 26.0, 55.37, 46.6, 33.0, 35.6, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M36", 36.0, 4.0, 55.0, 53.8, 55.0, 29.0, 27.7, 29.0, 60.79, 51.1, 36.0, 38.9, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M36x3", 36.0, 3.0, 55.0, 53.8, 55.0, 29.0, 27.7, 29.0, 60.79, 51.1, 36.0, 38.9, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M42", 42.0, 4.5, 65.0, 63.1, 65.0, 34.0, 32.4, 34.0, 71.30, 60.0, 42.0, 45.4, 30.0, 1),
    ("ANNEX_JA_REGULAR", "M48", 48.0, 5.0, 75.0, 73.1, 75.0, 38.0, 36.4, 38.0, 82.60, 69.4, 48.0, 51.8, 30.0, 1),

    # -------------------------------------------------------------------------
    # F. ANNEX JA THIN (Phụ lục JA Loại 3 - Đai ốc mỏng truyền thống m ≈ 0.6d)
    # -------------------------------------------------------------------------
    ("ANNEX_JA_THIN", "M6", 6.0, 1.0, 10.0, 9.78, 10.0, 3.6, 3.3, 3.6, 11.05, 8.9, 6.0, 6.75, 30.0, 2),
    ("ANNEX_JA_THIN", "M8", 8.0, 1.25, 13.0, 12.73, 13.0, 5.0, 4.7, 5.0, 14.38, 11.6, 8.0, 8.75, 30.0, 2),
    ("ANNEX_JA_THIN", "M10", 10.0, 1.5, 17.0, 16.73, 17.0, 6.0, 5.7, 6.0, 18.90, 15.5, 10.0, 10.8, 30.0, 2),
    ("ANNEX_JA_THIN", "M12", 12.0, 1.75, 19.0, 18.67, 19.0, 7.0, 6.64, 7.0, 21.10, 17.5, 12.0, 13.0, 30.0, 2),
    ("ANNEX_JA_THIN", "M14", 14.0, 2.0, 22.0, 21.67, 22.0, 8.0, 7.64, 8.0, 24.49, 20.5, 14.0, 15.1, 30.0, 2),
    ("ANNEX_JA_THIN", "M16", 16.0, 2.0, 24.0, 23.67, 24.0, 10.0, 9.64, 10.0, 26.75, 22.5, 16.0, 17.3, 30.0, 2),
    ("ANNEX_JA_THIN", "M18", 18.0, 2.5, 27.0, 26.16, 27.0, 11.0, 10.57, 11.0, 29.56, 24.9, 18.0, 19.5, 30.0, 2),
    ("ANNEX_JA_THIN", "M20", 20.0, 2.5, 30.0, 29.16, 30.0, 12.0, 11.57, 12.0, 32.95, 27.7, 20.0, 21.6, 30.0, 2),
    ("ANNEX_JA_THIN", "M22", 22.0, 2.5, 32.0, 31.0, 32.0, 13.0, 12.57, 13.0, 35.03, 29.5, 22.0, 23.7, 30.0, 2),
    ("ANNEX_JA_THIN", "M24", 24.0, 3.0, 36.0, 35.0, 36.0, 14.0, 13.4, 14.0, 39.55, 33.2, 24.0, 25.9, 30.0, 2),
    ("ANNEX_JA_THIN", "M27", 27.0, 3.0, 41.0, 40.0, 41.0, 16.0, 15.3, 16.0, 45.20, 38.0, 27.0, 29.1, 30.0, 2),
    ("ANNEX_JA_THIN", "M30", 30.0, 3.5, 46.0, 45.0, 46.0, 18.0, 17.3, 18.0, 50.85, 42.8, 30.0, 32.4, 30.0, 2),
    ("ANNEX_JA_THIN", "M30x3", 30.0, 3.0, 46.0, 45.0, 46.0, 18.0, 17.3, 18.0, 50.85, 42.8, 30.0, 32.4, 30.0, 2),
    ("ANNEX_JA_THIN", "M36", 36.0, 4.0, 55.0, 53.8, 55.0, 21.0, 20.0, 21.0, 60.79, 51.1, 36.0, 38.9, 30.0, 2),
    ("ANNEX_JA_THIN", "M42", 42.0, 4.5, 65.0, 63.1, 65.0, 25.0, 24.0, 25.0, 71.30, 60.0, 42.0, 45.4, 30.0, 2),

    # -------------------------------------------------------------------------
    # G. ANNEX JA SMALL (Phụ lục JA 小形 - Giác cờ-lê nhỏ hơn thông thường)
    # -------------------------------------------------------------------------
    ("ANNEX_JA_SMALL", "M8", 8.0, 1.25, 12.0, 11.73, 12.0, 6.5, 6.14, 6.5, 13.28, 10.6, 8.0, 8.75, 30.0, 1),
    ("ANNEX_JA_SMALL", "M10", 10.0, 1.5, 14.0, 13.73, 14.0, 8.0, 7.64, 8.0, 15.51, 12.5, 10.0, 10.8, 30.0, 1),
    ("ANNEX_JA_SMALL", "M12", 12.0, 1.75, 17.0, 16.73, 17.0, 10.0, 9.64, 10.0, 18.90, 15.5, 12.0, 13.0, 30.0, 1),
    ("ANNEX_JA_SMALL", "M14", 14.0, 2.0, 19.0, 18.67, 19.0, 11.0, 10.57, 11.0, 21.10, 17.5, 14.0, 15.1, 30.0, 1),
    ("ANNEX_JA_SMALL", "M16", 16.0, 2.0, 22.0, 21.67, 22.0, 13.0, 12.57, 13.0, 24.49, 20.5, 16.0, 17.3, 30.0, 1),
    ("ANNEX_JA_SMALL", "M20", 20.0, 2.5, 27.0, 26.16, 27.0, 16.0, 15.3, 16.0, 29.56, 24.9, 20.0, 21.6, 30.0, 1),
    ("ANNEX_JA_SMALL", "M24", 24.0, 3.0, 32.0, 31.0, 32.0, 19.0, 18.1, 19.0, 35.03, 29.5, 24.0, 25.9, 30.0, 1),
    ("ANNEX_JA_SMALL", "M30", 30.0, 3.5, 41.0, 40.0, 41.0, 24.0, 23.0, 24.0, 45.20, 38.0, 30.0, 32.4, 30.0, 1),
    ("ANNEX_JA_SMALL", "M36", 36.0, 4.0, 50.0, 49.0, 50.0, 29.0, 27.7, 29.0, 55.37, 46.6, 36.0, 38.9, 30.0, 1),
]

# ==============================================================================
# 4. HÀM TẠO VÀ SEED CƠ SỞ DỮ LIỆU SQLITE
# ==============================================================================
def create_and_seed_sqlite():
    """Khởi tạo cấu trúc bảng SQLite và nạp toàn bộ dữ liệu JIS B 1181."""
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Bảng 1: Danh mục chủng loại nut
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jis_b1181_nut_types (
            type_id INTEGER PRIMARY KEY,
            type_code TEXT UNIQUE NOT NULL,
            type_name_ja TEXT NOT NULL,
            type_name_en TEXT NOT NULL,
            iso_standard TEXT,
            nut_style TEXT NOT NULL,
            pitch_type TEXT NOT NULL,
            product_grade TEXT NOT NULL,
            dimension_series TEXT NOT NULL,
            is_flange_default INTEGER DEFAULT 0,
            description_vi TEXT
        )
    """)

    # Bảng 2: Kích thước hình học đai ốc
    cur.execute("""
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
            chamfer_angle_deg REAL DEFAULT 30.0,
            chamfer_sides INTEGER DEFAULT 2,
            UNIQUE(series, nut_size)
        )
    """)

    # Bảng 3: Bước ren
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jis_b1181_pitch_specs (
            nut_size TEXT PRIMARY KEY,
            nominal_dia REAL NOT NULL,
            pitch_coarse REAL NOT NULL,
            pitch_fine REAL
        )
    """)

    # Bảng 4: Cấp bền cơ tính
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jis_b1181_materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            standard_system TEXT NOT NULL,
            material_group TEXT NOT NULL,
            property_class TEXT NOT NULL,
            proof_stress_mpa REAL,
            description_vi TEXT
        )
    """)

    # Nạp Bảng 1: Nut types
    cur.executemany("""
        INSERT INTO jis_b1181_nut_types
        (type_id, type_code, type_name_ja, type_name_en, iso_standard, nut_style, pitch_type, product_grade, dimension_series, is_flange_default, description_vi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, NUT_TYPES_DATA)

    # Nạp Bảng 2: Nut dimensions
    cur.executemany("""
        INSERT INTO jis_b1181_nut_dimensions
        (series, nut_size, nominal_dia, pitch, s_nominal, s_min, s_max, m_nominal, m_min, m_max, e_min, dw_min, da_min, da_max, chamfer_angle_deg, chamfer_sides)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, NUT_DIMENSIONS_DATA)

    # Nạp Bảng 3: Pitches
    pitch_rows = [(k, v[0], v[1], v[2]) for k, v in PITCH_DATA.items()]
    cur.executemany("""
        INSERT INTO jis_b1181_pitch_specs (nut_size, nominal_dia, pitch_coarse, pitch_fine)
        VALUES (?, ?, ?, ?)
    """, pitch_rows)

    # Nạp Bảng 4: Cơ tính vật liệu
    materials_data = [
        ("ISO_898_2", "STEEL", "6", 600.0, "Thép cacbon cấp bền 6, dùng với bu lông 6.8"),
        ("ISO_898_2", "STEEL", "8", 800.0, "Thép cacbon cấp bền 8, dùng với bu lông 8.8 (Mặc định cho đường ống công nghiệp)"),
        ("ISO_898_2", "STEEL", "10", 1000.0, "Thép hợp kim xử lý nhiệt cấp bền 10, dùng với bu lông 10.9"),
        ("ISO_898_2", "STEEL", "12", 1200.0, "Thép hợp kim tôi ram cấp bền 12, dùng với bu lông 12.9"),
        ("JIS_ANNEX_JB", "STEEL", "4T", 400.0, "Thép hệ truyền thống Nhật 4T"),
        ("JIS_ANNEX_JB", "STEEL", "5T", 500.0, "Thép hệ truyền thống Nhật 5T"),
        ("JIS_ANNEX_JB", "STEEL", "6T", 600.0, "Thép hệ truyền thống Nhật 6T"),
        ("JIS_ANNEX_JB", "STEEL", "8T", 800.0, "Thép hệ truyền thống Nhật 8T"),
        ("JIS_ANNEX_JB", "STEEL", "10T", 1000.0, "Thép hệ truyền thống Nhật 10T"),
        ("ISO_3506_2", "STAINLESS", "A2-70", 700.0, "Inox SUS304 tôi nguội cấp 70"),
        ("ISO_3506_2", "STAINLESS", "A4-70", 700.0, "Inox SUS316 kháng axit cấp 70"),
    ]
    cur.executemany("""
        INSERT INTO jis_b1181_materials (standard_system, material_group, property_class, proof_stress_mpa, description_vi)
        VALUES (?, ?, ?, ?, ?)
    """, materials_data)

    # Tạo chỉ mục tối ưu truy vấn
    cur.execute("CREATE INDEX IF NOT EXISTS idx_b1181_dim ON jis_b1181_nut_dimensions(series, nut_size)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_b1181_types ON jis_b1181_nut_types(type_code)")

    conn.commit()
    conn.close()
    print(f"-> Tạo thành công CSDL SQLite: {DB_PATH}")


# ==============================================================================
# 5. HÀM TẠO DATASET PYTHON THUẦN (ZERO-IO CACHE TRONG RAM)
# ==============================================================================
def generate_python_dataset():
    """Tạo file Python thuần chứa dữ liệu tĩnh dạng Dictionary phục vụ tra cứu RAM."""
    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        f.write('"""Bộ dữ liệu tĩnh chuẩn JIS B 1181 : 2014 cho AutoCAD Plant 3D (Không phụ thuộc SQLite)."""\n')
        f.write("from ..models.jis_b1181_specs import NutDimensionSpec, NutTypeSpec\n\n")

        # 1. Ghi danh mục chủng loại
        f.write("# Danh mục 12 chủng loại đai ốc trong JIS B 1181 : 2014\n")
        f.write("JIS_B1181_NUT_TYPES = {\n")
        for item in NUT_TYPES_DATA:
            t_id, t_code, t_ja, t_en, iso, style, p_type, grade, dim_ser, def_flg, desc = item
            f.write(f'    "{t_code}": NutTypeSpec(\n')
            f.write('        standard="JIS_B_1181",\n')
            f.write(f"        type_id={t_id},\n")
            f.write(f'        type_code="{t_code}",\n')
            f.write(f'        type_name_ja="{t_ja}",\n')
            f.write(f'        type_name_en="{t_en}",\n')
            f.write(f'        iso_standard="{iso}",\n')
            f.write(f'        nut_style="{style}",\n')
            f.write(f'        pitch_type="{p_type}",\n')
            f.write(f'        product_grade="{grade}",\n')
            f.write(f'        dimension_series="{dim_ser}",\n')
            f.write(f"        is_flange_default={bool(def_flg)},\n")
            f.write(f'        description_vi="{desc}"\n')
            f.write("    ),\n")
        f.write("}\n\n")

        # 2. Ghi thông số bước ren
        f.write("# Bước ren thô và mịn theo cỡ đai ốc\n")
        f.write("JIS_B1181_PITCH_SPECS = {\n")
        for size, (d, pc, pf) in PITCH_DATA.items():
            pf_val = f"{pf}" if pf is not None else "None"
            f.write(f'    "{size}": {{"nominal_dia": {d}, "pitch_coarse": {pc}, "pitch_fine": {pf_val}}},\n')
        f.write("}\n\n")

        # 3. Ghi kích thước hình học chi tiết
        f.write("# Kích thước hình học đai ốc theo họ series và cỡ ren\n")
        f.write("JIS_B1181_NUT_DIMENSIONS = {\n")
        for dim in NUT_DIMENSIONS_DATA:
            ser, sz, d, p, sn, smin, smax, mn, mmin, mmax, emin, dw, damin, damax, c_ang, c_sides = dim
            dw_val = f"{dw}" if dw is not None else "None"
            damin_val = f"{damin}" if damin is not None else "None"
            damax_val = f"{damax}" if damax is not None else "None"
            f.write(f'    ("{ser}", "{sz}"): NutDimensionSpec(\n')
            f.write('        standard="JIS_B_1181",\n')
            f.write(f'        series="{ser}",\n')
            f.write(f'        nut_size="{sz}",\n')
            f.write(f"        nominal_dia={d},\n")
            f.write(f"        pitch={p},\n")
            f.write(f"        s_nominal={sn},\n")
            f.write(f"        s_min={smin},\n")
            f.write(f"        s_max={smax},\n")
            f.write(f"        m_nominal={mn},\n")
            f.write(f"        m_min={mmin},\n")
            f.write(f"        m_max={mmax},\n")
            f.write(f"        e_min={emin},\n")
            f.write(f"        dw_min={dw_val},\n")
            f.write(f"        da_min={damin_val},\n")
            f.write(f"        da_max={damax_val},\n")
            f.write(f"        chamfer_angle_deg={c_ang},\n")
            f.write(f"        chamfer_sides={c_sides}\n")
            f.write("    ),\n")
        f.write("}\n")

    print(f"-> Tạo thành công dataset Python: {DATASET_PATH}")


if __name__ == "__main__":
    create_and_seed_sqlite()
    generate_python_dataset()
    print("=== HOÀN TẤT TÍCH HỢP CƠ SỞ DỮ LIỆU JIS B 1181 ===")
