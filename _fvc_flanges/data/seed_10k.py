import sqlite3
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "jis_b2220.sqlite")

# Bảng kích thước gốc từ Tiêu chuẩn JIS B 2220 : 2012, 表15 - 呼び圧力10Kフランジの寸法
# Cấu trúc: (DN, D, C, h, No, bolt_name, g, f, t, t_bl, T_it, a, b, d0)
JIS_10K_RAW_DATA = [
    # DN,  D,    C,   h,  No, bolt,   g,    f,  t,  t_bl, T_it, a,      b,     d0
    (10,   90,   65,  15, 4,  "M12",  46,   1,  12, 12,   29,   17.3,   28,    17.8),
    (15,   95,   70,  15, 4,  "M12",  51,   1,  12, 12,   31,   21.7,   33,    22.2),
    (20,   100,  75,  15, 4,  "M12",  56,   1,  14, 14,   32,   27.2,   38,    27.7),
    (25,   125,  90,  19, 4,  "M16",  67,   2,  14, 14,   36,   34.0,   47,    34.5),
    (32,   135,  100, 19, 4,  "M16",  76,   2,  16, 16,   38,   42.7,   56,    43.2),
    (40,   140,  105, 19, 4,  "M16",  81,   2,  16, 16,   38,   48.6,   62,    49.1),
    (50,   155,  120, 19, 4,  "M16",  96,   2,  16, 16,   40,   60.5,   75,    61.1),
    (65,   175,  140, 19, 4,  "M16",  116,  2,  18, 18,   44,   76.3,   92,    77.1),
    (80,   185,  150, 19, 8,  "M16",  126,  2,  18, 18,   45,   89.1,   105,   90.0),
    (90,   195,  160, 19, 8,  "M16",  136,  2,  18, 18,   45,   101.6,  117,   102.6),
    (100,  210,  175, 19, 8,  "M16",  151,  2,  18, 18,   45,   114.3,  130,   115.4),
    (125,  250,  210, 23, 8,  "M20",  182,  2,  20, 20,   47,   139.8,  156,   141.2),
    (150,  280,  240, 23, 8,  "M20",  212,  2,  22, 22,   53,   165.2,  184,   166.6),
    (175,  305,  265, 23, 12, "M20",  237,  2,  22, 22,   55,   190.7,  210,   192.1),
    (200,  330,  290, 23, 12, "M20",  262,  2,  22, 22,   58,   216.3,  238,   218.0),
    (225,  350,  310, 23, 12, "M20",  282,  2,  22, 22,   58,   241.8,  261,   243.7),
    (250,  400,  355, 25, 12, "M22",  324,  2,  24, 24,   65,   267.4,  292,   269.5),
    (300,  445,  400, 25, 16, "M22",  368,  3,  24, 24,   68,   318.5,  345,   321.0),
    (350,  490,  445, 25, 16, "M22",  413,  3,  26, 26,   79,   355.6,  388,   358.1),
    (400,  560,  510, 27, 16, "M24",  475,  3,  28, 28,   85,   406.4,  442,   409.0),
    (450,  620,  565, 27, 20, "M24",  530,  3,  30, 30,   90,   457.2,  495,   460.0),
    (500,  675,  620, 27, 20, "M24",  585,  3,  30, 30,   90,   508.0,  546,   511.0),
    (550,  745,  680, 33, 20, "M30",  640,  3,  32, 34,   111,  558.8,  597,   562.0),
    (600,  795,  730, 33, 24, "M30",  690,  3,  32, 36,   112,  609.6,  648,   613.0),
    (650,  845,  780, 33, 24, "M30",  740,  3,  34, 38,   116,  660.4,  700,   664.0),
    (700,  905,  840, 33, 24, "M30",  800,  3,  34, 40,   132,  711.2,  754,   715.0),
    (750,  970,  900, 33, 24, "M30",  855,  3,  36, 44,   139,  762.0,  807,   766.0),
    (800,  1020, 950, 33, 28, "M30",  905,  3,  36, 46,   139,  812.8,  858,   817.0),
    (850,  1070, 1000,33, 28, "M30",  955,  3,  36, 48,   139,  863.6,  908,   868.0),
    (900,  1120, 1050,33, 28, "M30",  1005, 3,  38, 50,   140,  914.4,  959,   919.0),
    (1000, 1235, 1160,39, 28, "M36",  1110, 3,  40, 56,   151,  1016.0, 1065,  1021.0),
    (1100, 1345, 1270,39, 28, "M36",  1220, 3,  42, 62,   170,  1117.6, 1174,  1122.0),
    (1200, 1465, 1380,39, 32, "M36",  1325, 3,  44, 66,   182,  1219.2, 1281,  1224.0),
    (1350, 1630, 1540,45, 36, "M42",  1480, 3,  48, 74,   200,  1371.6, 1438,  1376.0),
    (1500, 1795, 1700,45, 40, "M42",  1635, 3,  50, 82,   218,  1524.0, 1598,  1529.0),
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jis_b2220 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating TEXT NOT NULL,
        flange_type TEXT NOT NULL,
        dn INTEGER NOT NULL,
        d REAL NOT NULL,
        c REAL NOT NULL,
        h REAL NOT NULL,
        no INTEGER NOT NULL,
        bolt_name TEXT,
        g REAL DEFAULT 0.0,
        f REAL DEFAULT 0.0,
        t REAL NOT NULL,
        total_len REAL,
        hub_small REAL,
        hub_large REAL,
        inner_dia REAL,
        CONSTRAINT uq_flange UNIQUE (rating, flange_type, dn)
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_flange_lookup ON jis_b2220(rating, flange_type, dn);")
    
    records = []
    for dn, d, c, h, no, bolt, g, f, t, t_bl, T_it, a, b, d0 in JIS_10K_RAW_DATA:
        # 1. Loại IT (Integral - dùng cho Van / Accessories / Thiết bị có cổ bích đúc liền)
        records.append(('10K', 'IT', dn, d, c, h, no, bolt, g, f, t, T_it, a, b, d0))
        
        # 2. Loại SOP (Slip-On Plate - Bích phẳng hàn trượt)
        records.append(('10K', 'SOP', dn, d, c, h, no, bolt, g, f, t, t, 0.0, 0.0, d0))

        # 3. Loại WN (Welding Neck - Bích hàn cổ cao)
        records.append(('10K', 'WN', dn, d, c, h, no, bolt, g, f, t, T_it, a, b, a))

        # 4. Loại BL (Blind - Bích mù, không lỗ khoét tâm, độ dày t_bl)
        records.append(('10K', 'BL', dn, d, c, h, no, bolt, g, f, t_bl, t_bl, 0.0, 0.0, 0.0))

    cur.executemany("""
    INSERT OR REPLACE INTO jis_b2220 
    (rating, flange_type, dn, d, c, h, no, bolt_name, g, f, t, total_len, hub_small, hub_large, inner_dia)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    
    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM jis_b2220 WHERE rating='10K'").fetchone()[0]
    conn.close()
    print(f"[OK] Database initialized successfully at: {DB_PATH}")
    print(f"[OK] Total 10K flange records seeded: {count} rows (across IT, SOP, WN, BL for 35 nominal diameters).")

if __name__ == "__main__":
    init_db()
