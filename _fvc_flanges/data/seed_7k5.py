import sqlite3
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "jis_b2220.sqlite")

# Bảng kích thước JIS 7.5K (0.75 MPa) thường dùng trong hệ thống van nước / tiêu chuẩn JWWA / JIS B 2062
JIS_7K5_RAW_DATA = [
    # DN,  D,    C,    h,  No, bolt,   g,    f,  t,  t_bl, T_it, a,      b,     d0
    (40,   140,  105,  19, 4,  "M16",  85,   2,  16, 16,   38,   48.6,   62,    49.1),
    (50,   155,  120,  19, 4,  "M16",  100,  2,  16, 16,   40,   60.5,   75,    61.1),
    (65,   175,  140,  19, 4,  "M16",  120,  2,  18, 18,   44,   76.3,   92,    77.1),
    (80,   185,  150,  19, 8,  "M16",  130,  2,  18, 18,   45,   89.1,   105,   90.0),
    (100,  210,  175,  19, 8,  "M16",  155,  2,  20, 20,   45,   114.3,  130,   115.4),
    (125,  250,  210,  19, 8,  "M16",  185,  2,  20, 20,   47,   139.8,  156,   141.2),
    (150,  280,  240,  19, 8,  "M16",  215,  2,  22, 22,   53,   165.2,  184,   166.6),
    (200,  342,  299,  19, 8,  "M16",  256,  3,  27, 27,   58,   216.3,  238,   218.0),
    (250,  410,  360,  23, 12, "M20",  314,  3,  29, 29,   65,   267.4,  292,   269.5),
    (300,  464,  414,  23, 12, "M20",  364,  3,  30, 30,   68,   318.5,  345,   321.0),
    (350,  510,  460,  23, 12, "M20",  414,  3,  32, 32,   79,   355.6,  388,   358.1),
    (400,  565,  515,  25, 16, "M22",  465,  3,  34, 34,   85,   406.4,  442,   409.0),
    (450,  620,  570,  25, 16, "M22",  520,  3,  36, 36,   90,   457.2,  495,   460.0),
    (500,  675,  620,  25, 16, "M22",  570,  3,  38, 38,   90,   508.0,  546,   511.0),
    (600,  795,  740,  25, 20, "M22",  680,  3,  42, 42,   112,  609.6,  648,   613.0),
]

def seed_7k5():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    records = []
    for dn, d, c, h, no, bolt, g, f, t, t_bl, T_it, a, b, d0 in JIS_7K5_RAW_DATA:
        records.append(('7K5', 'IT', dn, d, c, h, no, bolt, g, f, t, T_it, a, b, d0))
        records.append(('7K5', 'SOP', dn, d, c, h, no, bolt, g, f, t, t, 0.0, 0.0, d0))
        records.append(('7K5', 'WN', dn, d, c, h, no, bolt, g, f, t, T_it, a, b, a))
        records.append(('7K5', 'BL', dn, d, c, h, no, bolt, g, f, t_bl, t_bl, 0.0, 0.0, 0.0))

    cur.executemany("""
    INSERT OR REPLACE INTO jis_b2220 
    (rating, flange_type, dn, d, c, h, no, bolt_name, g, f, t, total_len, hub_small, hub_large, inner_dia)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM jis_b2220 WHERE rating='7K5'").fetchone()[0]
    conn.close()
    print(f"[OK] Seeded {count} records for JIS 7K5 into database.")

if __name__ == "__main__":
    seed_7k5()
