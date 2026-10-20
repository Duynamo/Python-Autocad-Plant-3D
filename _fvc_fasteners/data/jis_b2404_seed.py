"""Script khởi tạo CSDL SQLite jis_b2404.sqlite cho tiêu chuẩn gioăng mặt bích JIS B 2404 : 2018."""
import os
import sqlite3
import sys

# Đảm bảo xuất UTF-8
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATA_DIR, "jis_b2404.sqlite")

from jis_b2404_dataset import (
    SHEET_GASKET_D1,
    RING_GASKET_D3,
    SPIRAL_WOUND_DIMENSIONS,
)

# Tra cứu kích thước bích JIS B 2220 cho Full-Face
try:
    from _fvc_flanges import get_flange_dimensions
except ImportError:
    # Nếu chạy độc lập trong thư mục data
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from _fvc_flanges import get_flange_dimensions


def seed_database():
    """Tạo bảng và nạp dữ liệu vào SQLite database jis_b2404.sqlite."""
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Bảng Sheet Gaskets (Gioăng tấm đệm phẳng)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sheet_gaskets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        standard TEXT NOT NULL,
        rating TEXT NOT NULL,
        dn INTEGER NOT NULL,
        shape TEXT NOT NULL,
        facing TEXT NOT NULL,
        d1 REAL NOT NULL,
        d2 REAL NOT NULL,
        c REAL,
        h REAL,
        no INTEGER,
        nominal_thickness REAL NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sheet ON sheet_gaskets (rating, dn, shape, facing);")

    # 2. Bảng Spiral Wound Gaskets (Gioăng quấn xoắn kim loại)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS spiral_wound_gaskets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        standard TEXT NOT NULL,
        rating TEXT NOT NULL,
        dn INTEGER NOT NULL,
        construction TEXT NOT NULL,
        facing TEXT NOT NULL,
        d1 REAL,
        d2 REAL NOT NULL,
        d3 REAL NOT NULL,
        d4 REAL,
        t_winding REAL NOT NULL,
        t_ring REAL NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_swg ON spiral_wound_gaskets (rating, dn, construction, facing);")

    # 3. Nạp dữ liệu Ring Gaskets (Bảng 9)
    sheet_rows = []
    for (rating, dn), d3 in RING_GASKET_D3.items():
        d1 = SHEET_GASKET_D1.get(dn, float(dn))
        sheet_rows.append((
            "JIS_B_2404", rating, dn, "RING", "RF", d1, d3, None, None, None, 3.0
        ))

    # 4. Nạp dữ liệu Full-Face Gaskets (Bảng 6, 7, 8)
    for rating in ["5K", "10K", "16K"]:
        for dn, d1 in SHEET_GASKET_D1.items():
            flange_dim = None
            for ft in ["SOP", "IT", "WN", "BL"]:
                try:
                    flange_dim = get_flange_dimensions(rating=rating, dn=dn, flange_type=ft)
                    if flange_dim:
                        break
                except Exception:
                    continue
            if flange_dim:
                d2 = flange_dim.d
                c = flange_dim.c
                h = flange_dim.h
                no = flange_dim.no
                sheet_rows.append((
                    "JIS_B_2404", rating, dn, "FULL_FACE", "FF", d1, d2, c, h, no, 3.0
                ))

    cur.executemany("""
    INSERT INTO sheet_gaskets (
        standard, rating, dn, shape, facing, d1, d2, c, h, no, nominal_thickness
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, sheet_rows)

    # 5. Nạp dữ liệu Spiral Wound Gaskets (Bảng 15 - 23)
    swg_rows = []
    for (rating, dn), (d1_in, d2_in, d3_out, d4_out) in SPIRAL_WOUND_DIMENSIONS.items():
        # Dạng có cả 2 vành (INNER_OUTER_RING)
        swg_rows.append((
            "JIS_B_2404", rating, dn, "INNER_OUTER_RING", "RF",
            d1_in, d2_in, d3_out, d4_out, 4.5, 3.0
        ))
        # Dạng chỉ có vành ngoài (OUTER_RING)
        swg_rows.append((
            "JIS_B_2404", rating, dn, "OUTER_RING", "RF",
            None, d2_in, d3_out, d4_out, 4.5, 3.0
        ))
        # Dạng cơ bản (BASIC)
        swg_rows.append((
            "JIS_B_2404", rating, dn, "BASIC", "TG",
            None, d2_in, d3_out, None, 4.5, 3.0
        ))

    cur.executemany("""
    INSERT INTO spiral_wound_gaskets (
        standard, rating, dn, construction, facing, d1, d2, d3, d4, t_winding, t_ring
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, swg_rows)

    conn.commit()
    conn.close()
    print(f"Khởi tạo thành công database: {DB_PATH}")
    print(f" - Sheet Gasket rows: {len(sheet_rows)}")
    print(f" - Spiral Wound Gasket rows: {len(swg_rows)}")


if __name__ == "__main__":
    seed_database()
