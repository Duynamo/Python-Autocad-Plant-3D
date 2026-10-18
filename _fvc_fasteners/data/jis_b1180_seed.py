"""Script khởi tạo CSDL SQLite và dataset Python thuần cho JIS B 1180 : 2014."""
import os
import sqlite3
import sys

# Đảm bảo UTF-8
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATA_DIR, "jis_b1180.sqlite")
DATASET_PATH = os.path.join(DATA_DIR, "jis_b1180_dataset.py")

# ==============================================================================
# 1. DANH MỤC 7 LOẠI BU LÔNG CHÍNH + PHỤ LỤC JA THEO JIS B 1180 : 2014
# ==============================================================================
# (type_id, type_code, type_name_ja, iso_standard, thread_style, pitch_type, head_series, is_flange_default, description_vi)
BOLT_TYPES_DATA = [
    (
        1,
        "TYPE_1_NOMINAL_COARSE_GRADE_C",
        "呼び径六角ボルト−並目ねじ−部品等級C",
        "ISO 4016",
        "NOMINAL_SHANK",
        "COARSE",
        "ISO_GRADE_C",
        0,
        "Bu lông ren lửng thân danh nghĩa, bước thô, cấp C thương mại (mặt tỳ phẳng tự do)"
    ),
    (
        2,
        "TYPE_2_NOMINAL_COARSE_GRADE_AB",
        "呼び径六角ボルト−並目ねじ−部品等級A及びB",
        "ISO 4014",
        "NOMINAL_SHANK",
        "COARSE",
        "ISO_GRADE_AB",
        1,
        "Bu lông ren lửng thân danh nghĩa, bước thô, cấp A & B có gờ đệm (Mặc định cho Mặt bích đường ống)"
    ),
    (
        3,
        "TYPE_3_NOMINAL_FINE_GRADE_AB",
        "呼び径六角ボルト−細目ねじ−部品等級A及びB",
        "ISO 8765",
        "NOMINAL_SHANK",
        "FINE",
        "ISO_GRADE_AB",
        0,
        "Bu lông ren lửng thân danh nghĩa, bước mịn, cấp A & B có gờ đệm (Cơ khí chính xác)"
    ),
    (
        4,
        "TYPE_4_FULL_COARSE_GRADE_AB",
        "全ねじ六角ボルト−並目ねじ−部品等級A及びB",
        "ISO 4017",
        "FULL_THREAD",
        "COARSE",
        "ISO_GRADE_AB",
        0,
        "Bu lông ren suốt toàn thân, bước thô, cấp A & B có gờ đệm (Dùng cho lỗ ren kín đáy / van bướm wafer/lug)"
    ),
    (
        5,
        "TYPE_5_FULL_COARSE_GRADE_C",
        "全ねじ六角ボルト−並目ねじ−部品等級C",
        "ISO 4018",
        "FULL_THREAD",
        "COARSE",
        "ISO_GRADE_C",
        0,
        "Bu lông ren suốt toàn thân, bước thô, cấp C thương mại (không bắt buộc gờ đệm)"
    ),
    (
        6,
        "TYPE_6_FULL_FINE_GRADE_AB",
        "全ねじ六角ボルト−細目ねじ−部品等級A及びB",
        "ISO 8676",
        "FULL_THREAD",
        "FINE",
        "ISO_GRADE_AB",
        0,
        "Bu lông ren suốt toàn thân, bước mịn, cấp A & B có gờ đệm"
    ),
    (
        7,
        "TYPE_7_REDUCED_COARSE_GRADE_B",
        "有効径六角ボルト−並目ねじ−部品等級B",
        "ISO 4015",
        "REDUCED_SHANK",
        "COARSE",
        "ISO_GRADE_AB",
        0,
        "Bu lông thân thắt (đường kính trung bình ds ~ d2), bước thô, cấp B"
    ),
    (
        8,
        "TYPE_8_ANNEX_JA_TRADITIONAL",
        "附属書JA ISOによらない六角ボルト",
        "JIS B 1180 Annex JA",
        "NOMINAL_SHANK",
        "COARSE",
        "ANNEX_JA",
        0,
        "Bu lông lục giác hệ truyền thống Nhật Bản (M10 giác 17, M12 giác 19, M14 giác 22, M22 giác 32)"
    ),
]

# ==============================================================================
# 2. THÔNG SỐ BƯỚC REN (PITCH SPECS)
# ==============================================================================
# (bolt_size, nominal_dia, pitch_coarse, pitch_fine)
PITCH_SPECS_DATA = [
    ("M1.6", 1.6, 0.35, None),
    ("M2", 2.0, 0.40, None),
    ("M2.5", 2.5, 0.45, None),
    ("M3", 3.0, 0.50, None),
    ("M4", 4.0, 0.70, None),
    ("M5", 5.0, 0.80, None),
    ("M6", 6.0, 1.00, 0.75),
    ("M8", 8.0, 1.25, 1.00),
    ("M10", 10.0, 1.50, 1.25),
    ("M12", 12.0, 1.75, 1.25),
    ("M14", 14.0, 2.00, 1.50),
    ("M16", 16.0, 2.00, 1.50),
    ("M18", 18.0, 2.50, 1.50),
    ("M20", 20.0, 2.50, 1.50),
    ("M22", 22.0, 2.50, 1.50),
    ("M24", 24.0, 3.00, 2.00),
    ("M27", 27.0, 3.00, 2.00),
    ("M30", 30.0, 3.50, 2.00),
    ("M30x3", 30.0, 3.00, 3.00),  # Bước ren đặc thù trong JIS B 1217 cho áp lực cao
    ("M33", 33.0, 3.50, 2.00),
    ("M36", 36.0, 4.00, 3.00),
    ("M36x3", 36.0, 3.00, 3.00),
    ("M39", 39.0, 4.00, 3.00),
    ("M42", 42.0, 4.50, 3.00),
    ("M42x3", 42.0, 3.00, 3.00),
    ("M45", 45.0, 4.50, 3.00),
    ("M48", 48.0, 5.00, 3.00),
    ("M48x3", 48.0, 3.00, 3.00),
    ("M52", 52.0, 5.00, 3.00),
    ("M56", 56.0, 5.50, 4.00),
    ("M56x4", 56.0, 4.00, 4.00),
    ("M60", 60.0, 5.50, 4.00),
    ("M64", 64.0, 6.00, 4.00),
    ("M64x4", 64.0, 4.00, 4.00),
]

# ==============================================================================
# 3. KÍCH THƯỚC ĐẦU LỤC GIÁC (HEAD DIMENSIONS)
# ==============================================================================
# (series, bolt_size, s_nominal, s_min, s_max, k_nominal, k_min, k_max, e_min, dw_min, c_min, c_max, r_min, chamfer_angle_deg)
HEAD_DIMENSIONS_DATA = [
    # -------------------------------------------------------------------------
    # ISO_GRADE_AB: Cấp A & B (Bảng 3 & 4 JIS B 1180 / ISO 4014) - Có gờ đệm dw
    # -------------------------------------------------------------------------
    ("ISO_GRADE_AB", "M6", 10.0, 9.78, 10.0, 4.0, 3.85, 4.15, 11.05, 8.88, 0.15, 0.50, 0.25, 30.0),
    ("ISO_GRADE_AB", "M8", 13.0, 12.73, 13.0, 5.3, 5.15, 5.45, 14.38, 11.63, 0.15, 0.60, 0.40, 30.0),
    ("ISO_GRADE_AB", "M10", 16.0, 15.73, 16.0, 6.4, 6.22, 6.58, 17.77, 14.63, 0.15, 0.60, 0.40, 30.0),
    ("ISO_GRADE_AB", "M12", 18.0, 17.73, 18.0, 7.5, 7.32, 7.68, 20.03, 16.63, 0.15, 0.60, 0.60, 30.0),
    ("ISO_GRADE_AB", "M14", 21.0, 20.67, 21.0, 8.8, 8.62, 8.98, 23.36, 19.64, 0.15, 0.60, 0.60, 30.0),
    ("ISO_GRADE_AB", "M16", 24.0, 23.67, 24.0, 10.0, 9.82, 10.18, 26.75, 22.49, 0.20, 0.80, 0.60, 30.0),
    ("ISO_GRADE_AB", "M18", 27.0, 26.16, 27.0, 11.5, 11.28, 11.72, 30.14, 25.34, 0.20, 0.80, 0.60, 30.0),
    ("ISO_GRADE_AB", "M20", 30.0, 29.67, 30.0, 12.5, 12.285, 12.715, 33.53, 28.19, 0.20, 0.80, 0.80, 30.0),
    ("ISO_GRADE_AB", "M22", 34.0, 33.38, 34.0, 14.0, 13.785, 14.215, 37.71, 31.71, 0.20, 0.80, 0.80, 30.0),
    ("ISO_GRADE_AB", "M24", 36.0, 35.38, 36.0, 15.0, 14.785, 15.215, 39.98, 33.61, 0.20, 0.80, 0.80, 30.0),
    ("ISO_GRADE_AB", "M27", 41.0, 40.00, 41.0, 17.0, 16.65, 17.35, 45.20, 38.00, 0.20, 0.80, 1.00, 30.0),
    ("ISO_GRADE_AB", "M30", 46.0, 45.00, 46.0, 18.7, 18.28, 19.12, 50.85, 42.75, 0.20, 0.80, 1.00, 30.0),
    ("ISO_GRADE_AB", "M30x3", 46.0, 45.00, 46.0, 18.7, 18.28, 19.12, 50.85, 42.75, 0.20, 0.80, 1.00, 30.0),
    ("ISO_GRADE_AB", "M33", 50.0, 49.00, 50.0, 21.0, 20.58, 21.42, 55.37, 46.55, 0.20, 0.80, 1.00, 30.0),
    ("ISO_GRADE_AB", "M36", 55.0, 53.80, 55.0, 22.5, 22.08, 22.92, 60.79, 51.11, 0.20, 0.80, 1.00, 30.0),
    ("ISO_GRADE_AB", "M36x3", 55.0, 53.80, 55.0, 22.5, 22.08, 22.92, 60.79, 51.11, 0.20, 0.80, 1.00, 30.0),
    ("ISO_GRADE_AB", "M39", 60.0, 58.80, 60.0, 25.0, 24.58, 25.42, 66.44, 55.86, 0.20, 0.80, 1.00, 30.0),
    ("ISO_GRADE_AB", "M42", 65.0, 63.10, 65.0, 26.0, 25.58, 26.42, 71.30, 59.95, 0.30, 1.00, 1.20, 30.0),
    ("ISO_GRADE_AB", "M42x3", 65.0, 63.10, 65.0, 26.0, 25.58, 26.42, 71.30, 59.95, 0.30, 1.00, 1.20, 30.0),
    ("ISO_GRADE_AB", "M45", 70.0, 68.10, 70.0, 28.0, 27.58, 28.42, 76.95, 64.70, 0.30, 1.00, 1.20, 30.0),
    ("ISO_GRADE_AB", "M48", 75.0, 73.10, 75.0, 30.0, 29.58, 30.42, 82.60, 69.45, 0.30, 1.00, 1.60, 30.0),
    ("ISO_GRADE_AB", "M48x3", 75.0, 73.10, 75.0, 30.0, 29.58, 30.42, 82.60, 69.45, 0.30, 1.00, 1.60, 30.0),
    ("ISO_GRADE_AB", "M52", 80.0, 78.10, 80.0, 33.0, 32.50, 33.50, 88.71, 74.20, 0.30, 1.00, 1.60, 30.0),
    ("ISO_GRADE_AB", "M56", 85.0, 82.80, 85.0, 35.0, 34.50, 35.50, 93.56, 78.66, 0.30, 1.00, 2.00, 30.0),
    ("ISO_GRADE_AB", "M56x4", 85.0, 82.80, 85.0, 35.0, 34.50, 35.50, 93.56, 78.66, 0.30, 1.00, 2.00, 30.0),
    ("ISO_GRADE_AB", "M60", 90.0, 87.80, 90.0, 38.0, 37.50, 38.50, 99.21, 83.40, 0.30, 1.00, 2.00, 30.0),
    ("ISO_GRADE_AB", "M64", 95.0, 92.80, 95.0, 40.0, 39.50, 40.50, 104.86, 88.16, 0.30, 1.00, 2.00, 30.0),
    ("ISO_GRADE_AB", "M64x4", 95.0, 92.80, 95.0, 40.0, 39.50, 40.50, 104.86, 88.16, 0.30, 1.00, 2.00, 30.0),

    # -------------------------------------------------------------------------
    # ISO_GRADE_C: Cấp C (Bảng 7 & 8 JIS B 1180 / ISO 4016) - Mặt tỳ phẳng tự do
    # -------------------------------------------------------------------------
    ("ISO_GRADE_C", "M6", 10.0, 9.42, 10.0, 4.0, 3.625, 4.375, 10.89, None, None, None, 0.25, 30.0),
    ("ISO_GRADE_C", "M8", 13.0, 12.30, 13.0, 5.3, 4.875, 5.725, 14.20, None, None, None, 0.40, 30.0),
    ("ISO_GRADE_C", "M10", 16.0, 15.30, 16.0, 6.4, 5.95, 6.85, 17.59, None, None, None, 0.40, 30.0),
    ("ISO_GRADE_C", "M12", 18.0, 17.30, 18.0, 7.5, 7.05, 7.95, 19.85, None, None, None, 0.60, 30.0),
    ("ISO_GRADE_C", "M14", 21.0, 20.16, 21.0, 8.8, 8.30, 9.30, 22.78, None, None, None, 0.60, 30.0),
    ("ISO_GRADE_C", "M16", 24.0, 23.16, 24.0, 10.0, 9.50, 10.50, 26.17, None, None, None, 0.60, 30.0),
    ("ISO_GRADE_C", "M20", 30.0, 29.16, 30.0, 12.5, 11.90, 13.10, 32.95, None, None, None, 0.80, 30.0),
    ("ISO_GRADE_C", "M24", 36.0, 35.00, 36.0, 15.0, 14.35, 15.65, 39.55, None, None, None, 0.80, 30.0),
    ("ISO_GRADE_C", "M30", 46.0, 45.00, 46.0, 18.7, 17.90, 19.50, 50.85, None, None, None, 1.00, 30.0),
    ("ISO_GRADE_C", "M36", 55.0, 53.80, 55.0, 22.5, 21.70, 23.30, 60.79, None, None, None, 1.00, 30.0),
    ("ISO_GRADE_C", "M42", 65.0, 63.10, 65.0, 26.0, 25.20, 26.80, 71.30, None, None, None, 1.20, 30.0),
    ("ISO_GRADE_C", "M48", 75.0, 73.10, 75.0, 30.0, 29.20, 30.80, 82.60, None, None, None, 1.60, 30.0),
    ("ISO_GRADE_C", "M56", 85.0, 82.80, 85.0, 35.0, 34.00, 36.00, 93.56, None, None, None, 2.00, 30.0),
    ("ISO_GRADE_C", "M64", 95.0, 92.80, 95.0, 40.0, 39.00, 41.00, 104.86, None, None, None, 2.00, 30.0),

    # -------------------------------------------------------------------------
    # ANNEX_JA: Phụ lục JA (JIS truyền thống / 旧JIS) - Khác biệt s ở M10, 12, 14, 22
    # -------------------------------------------------------------------------
    ("ANNEX_JA", "M6", 10.0, 9.78, 10.0, 4.0, 3.85, 4.15, 11.05, 8.88, 0.15, 0.50, 0.25, 30.0),
    ("ANNEX_JA", "M8", 13.0, 12.73, 13.0, 5.3, 5.15, 5.45, 14.38, 11.63, 0.15, 0.60, 0.40, 30.0),
    ("ANNEX_JA", "M10", 17.0, 16.73, 17.0, 6.4, 6.22, 6.58, 18.90, 15.60, 0.15, 0.60, 0.40, 30.0),  # Giác 17
    ("ANNEX_JA", "M12", 19.0, 18.67, 19.0, 8.0, 7.82, 8.18, 21.10, 17.60, 0.15, 0.60, 0.60, 30.0),  # Giác 19, k=8.0
    ("ANNEX_JA", "M14", 22.0, 21.67, 22.0, 9.0, 8.82, 9.18, 24.49, 20.60, 0.15, 0.60, 0.60, 30.0),  # Giác 22
    ("ANNEX_JA", "M16", 24.0, 23.67, 24.0, 10.0, 9.82, 10.18, 26.75, 22.49, 0.20, 0.80, 0.60, 30.0),
    ("ANNEX_JA", "M18", 27.0, 26.16, 27.0, 12.0, 11.75, 12.25, 30.14, 25.34, 0.20, 0.80, 0.60, 30.0),
    ("ANNEX_JA", "M20", 30.0, 29.67, 30.0, 13.0, 12.75, 13.25, 33.53, 28.19, 0.20, 0.80, 0.80, 30.0),
    ("ANNEX_JA", "M22", 32.0, 31.38, 32.0, 14.0, 13.75, 14.25, 35.72, 30.00, 0.20, 0.80, 0.80, 30.0),  # Giác 32
    ("ANNEX_JA", "M24", 36.0, 35.38, 36.0, 15.0, 14.75, 15.25, 39.98, 33.61, 0.20, 0.80, 0.80, 30.0),
    ("ANNEX_JA", "M27", 41.0, 40.00, 41.0, 17.0, 16.65, 17.35, 45.20, 38.00, 0.20, 0.80, 1.00, 30.0),
    ("ANNEX_JA", "M30", 46.0, 45.00, 46.0, 19.0, 18.55, 19.45, 50.85, 42.75, 0.20, 0.80, 1.00, 30.0),
    ("ANNEX_JA", "M30x3", 46.0, 45.00, 46.0, 19.0, 18.55, 19.45, 50.85, 42.75, 0.20, 0.80, 1.00, 30.0),
    ("ANNEX_JA", "M36", 55.0, 53.80, 55.0, 23.0, 22.50, 23.50, 60.79, 51.11, 0.20, 0.80, 1.00, 30.0),
    ("ANNEX_JA", "M36x3", 55.0, 53.80, 55.0, 23.0, 22.50, 23.50, 60.79, 51.11, 0.20, 0.80, 1.00, 30.0),
]


def seed_database(db_path: str = DB_PATH):
    """Tạo các bảng và nạp dữ liệu JIS B 1180 vào file SQLite."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Bảng jis_b1180_bolt_types
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jis_b1180_bolt_types (
            type_id INTEGER PRIMARY KEY,
            standard TEXT NOT NULL DEFAULT 'JIS_B_1180',
            type_code TEXT NOT NULL UNIQUE,
            type_name_ja TEXT NOT NULL,
            iso_standard TEXT NOT NULL,
            thread_style TEXT NOT NULL,
            pitch_type TEXT NOT NULL,
            head_series TEXT NOT NULL,
            is_flange_default INTEGER NOT NULL DEFAULT 0,
            description_vi TEXT NOT NULL
        );
    """)

    for row in BOLT_TYPES_DATA:
        cur.execute("""
            INSERT INTO jis_b1180_bolt_types 
            (type_id, standard, type_code, type_name_ja, iso_standard, thread_style, pitch_type, head_series, is_flange_default, description_vi)
            VALUES (?, 'JIS_B_1180', ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)

    # 2. Bảng jis_b1180_pitch_specs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jis_b1180_pitch_specs (
            bolt_size TEXT PRIMARY KEY,
            standard TEXT NOT NULL DEFAULT 'JIS_B_1180',
            nominal_dia REAL NOT NULL,
            pitch_coarse REAL NOT NULL,
            pitch_fine REAL
        );
    """)

    for row in PITCH_SPECS_DATA:
        cur.execute("""
            INSERT INTO jis_b1180_pitch_specs 
            (bolt_size, standard, nominal_dia, pitch_coarse, pitch_fine)
            VALUES (?, 'JIS_B_1180', ?, ?, ?)
        """, row)

    # 3. Bảng jis_b1180_head_dimensions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jis_b1180_head_dimensions (
            series TEXT NOT NULL,
            bolt_size TEXT NOT NULL,
            standard TEXT NOT NULL DEFAULT 'JIS_B_1180',
            s_nominal REAL NOT NULL,
            s_min REAL NOT NULL,
            s_max REAL NOT NULL,
            k_nominal REAL NOT NULL,
            k_min REAL NOT NULL,
            k_max REAL NOT NULL,
            e_min REAL NOT NULL,
            dw_min REAL,
            c_min REAL,
            c_max REAL,
            r_min REAL NOT NULL,
            chamfer_angle_deg REAL NOT NULL DEFAULT 30.0,
            PRIMARY KEY (series, bolt_size)
        );
    """)

    for row in HEAD_DIMENSIONS_DATA:
        cur.execute("""
            INSERT INTO jis_b1180_head_dimensions
            (series, bolt_size, standard, s_nominal, s_min, s_max, k_nominal, k_min, k_max, e_min, dw_min, c_min, c_max, r_min, chamfer_angle_deg)
            VALUES (?, ?, 'JIS_B_1180', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)

    conn.commit()
    conn.close()
    print(f" Đã nạp thành công CSDL SQLite JIS B 1180 tại: {db_path}")


def export_dataset(dataset_path: str = DATASET_PATH):
    """Xuất bộ dữ liệu tĩnh Python thuần túy vào file jis_b1180_dataset.py."""
    with open(dataset_path, "w", encoding="utf-8") as f:
        f.write('"""Bộ dữ liệu tĩnh chuẩn JIS B 1180 : 2014 cho AutoCAD Plant 3D (Không phụ thuộc SQLite)."""\n')
        f.write("from ..models.jis_b1180_specs import HexHeadSpec, BoltTypeSpec\n\n")

        # 1. BOLT TYPES
        f.write("# Danh mục các loại bu lông trong JIS B 1180 : 2014\n")
        f.write("JIS_B1180_BOLT_TYPES = {\n")
        for row in BOLT_TYPES_DATA:
            f.write(f'    "{row[1]}": BoltTypeSpec(\n')
            f.write('        standard="JIS_B_1180",\n')
            f.write(f"        type_id={row[0]},\n")
            f.write(f'        type_code="{row[1]}",\n')
            f.write(f'        type_name_ja="{row[2]}",\n')
            f.write(f'        iso_standard="{row[3]}",\n')
            f.write(f'        thread_style="{row[4]}",\n')
            f.write(f'        pitch_type="{row[5]}",\n')
            f.write(f'        head_series="{row[6]}",\n')
            f.write(f"        is_flange_default={bool(row[7])},\n")
            f.write(f'        description_vi="{row[8]}"\n')
            f.write("    ),\n")
        f.write("}\n\n")

        # 2. PITCH SPECS
        f.write("# Bước ren thô và mịn theo cỡ bu lông\n")
        f.write("JIS_B1180_PITCH_SPECS = {\n")
        for row in PITCH_SPECS_DATA:
            fine_val = f"{row[3]}" if row[3] is not None else "None"
            f.write(f'    "{row[0]}": {{"nominal_dia": {row[1]}, "pitch_coarse": {row[2]}, "pitch_fine": {fine_val}}},\n')
        f.write("}\n\n")

        # 3. HEAD DIMENSIONS
        f.write("# Kích thước đầu lục giác theo họ series và cỡ bu lông\n")
        f.write("JIS_B1180_HEAD_DIMENSIONS = {\n")
        for row in HEAD_DIMENSIONS_DATA:
            dw_val = f"{row[9]}" if row[9] is not None else "None"
            c_min_val = f"{row[10]}" if row[10] is not None else "None"
            c_max_val = f"{row[11]}" if row[11] is not None else "None"
            f.write(f'    ("{row[0]}", "{row[1]}"): HexHeadSpec(\n')
            f.write('        standard="JIS_B_1180",\n')
            f.write(f'        series="{row[0]}",\n')
            f.write(f'        bolt_size="{row[1]}",\n')
            f.write(f"        s_nominal={row[2]},\n")
            f.write(f"        s_min={row[3]},\n")
            f.write(f"        s_max={row[4]},\n")
            f.write(f"        k_nominal={row[5]},\n")
            f.write(f"        k_min={row[6]},\n")
            f.write(f"        k_max={row[7]},\n")
            f.write(f"        e_min={row[8]},\n")
            f.write(f"        dw_min={dw_val},\n")
            f.write(f"        c_min={c_min_val},\n")
            f.write(f"        c_max={c_max_val},\n")
            f.write(f"        r_min={row[12]},\n")
            f.write(f"        chamfer_angle_deg={row[13]}\n")
            f.write("    ),\n")
        f.write("}\n")

    print(f" Đã xuất thành công pure-Python dataset tại: {dataset_path}")


if __name__ == "__main__":
    seed_database()
    export_dataset()
