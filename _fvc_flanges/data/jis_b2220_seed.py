import sqlite3
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "jis_b2220.sqlite")
DATASET_PATH = os.path.join(DB_DIR, "jis_b2220_dataset.py")

# Bảng kích thước gốc JIS B 2220 : 2012 - 呼び圧力10K
JIS_10K_RAW_DATA = [
    # DN,  D,    C,   h,  No, bolt,   g,    f,  t,  t_bl, T_it, a(OD),  b,     d0,    d_bore
    (10,   90,   65,  15, 4,  "M12",  46,   1,  12, 12,   29,   17.3,   28,    17.8,  12.7),
    (15,   95,   70,  15, 4,  "M12",  51,   1,  12, 12,   31,   21.7,   33,    22.2,  16.1),
    (20,   100,  75,  15, 4,  "M12",  56,   1,  14, 14,   32,   27.2,   38,    27.7,  21.6),
    (25,   125,  90,  19, 4,  "M16",  67,   2,  14, 14,   36,   34.0,   47,    34.5,  27.6),
    (32,   135,  100, 19, 4,  "M16",  76,   2,  16, 16,   38,   42.7,   56,    43.2,  35.7),
    (40,   140,  105, 19, 4,  "M16",  81,   2,  16, 16,   38,   48.6,   62,    49.1,  41.6),
    (50,   155,  120, 19, 4,  "M16",  96,   2,  16, 16,   40,   60.5,   75,    61.1,  52.9),
    (65,   175,  140, 19, 4,  "M16",  116,  2,  18, 18,   44,   76.3,   92,    77.1,  67.9),
    (80,   185,  150, 19, 8,  "M16",  126,  2,  18, 18,   45,   89.1,   105,   90.0,  80.7),
    (90,   195,  160, 19, 8,  "M16",  136,  2,  18, 18,   45,   101.6,  117,   102.6, 93.2),
    (100,  210,  175, 19, 8,  "M16",  151,  2,  18, 18,   45,   114.3,  130,   115.4, 105.3),
    (125,  250,  210, 23, 8,  "M20",  182,  2,  20, 20,   47,   139.8,  156,   141.2, 130.8),
    (150,  280,  240, 23, 8,  "M20",  212,  2,  22, 22,   53,   165.2,  184,   166.6, 155.2),
    (175,  305,  265, 23, 12, "M20",  237,  2,  22, 22,   55,   190.7,  210,   192.1, 180.1),
    (200,  330,  290, 23, 12, "M20",  262,  2,  22, 22,   58,   216.3,  238,   218.0, 204.7),
    (225,  350,  310, 23, 12, "M20",  282,  2,  22, 22,   58,   241.8,  261,   243.7, 229.4),
    (250,  400,  355, 25, 12, "M22",  324,  2,  24, 24,   65,   267.4,  292,   269.5, 254.2),
    (300,  445,  400, 25, 16, "M22",  368,  3,  24, 24,   68,   318.5,  345,   321.0, 304.7),
    (350,  490,  445, 25, 16, "M22",  413,  3,  26, 26,   79,   355.6,  388,   358.1, 339.8),
    (400,  560,  510, 27, 16, "M24",  475,  3,  28, 28,   85,   406.4,  442,   409.0, 390.6),
    (450,  620,  565, 27, 20, "M24",  530,  3,  30, 30,   90,   457.2,  495,   460.0, 441.4),
    (500,  675,  620, 27, 20, "M24",  585,  3,  30, 30,   90,   508.0,  546,   511.0, 492.2),
    (550,  745,  680, 33, 20, "M30",  640,  3,  32, 34,   111,  558.8,  597,   562.0, 543.0),
    (600,  795,  730, 33, 24, "M30",  690,  3,  32, 36,   112,  609.6,  648,   613.0, 593.8),
    (650,  845,  780, 33, 24, "M30",  740,  3,  34, 38,   116,  660.4,  700,   664.0, 644.6),
    (700,  905,  840, 33, 24, "M30",  800,  3,  34, 40,   132,  711.2,  754,   715.0, 695.4),
    (750,  970,  900, 33, 24, "M30",  855,  3,  36, 44,   139,  762.0,  807,   766.0, 746.2),
    (800,  1020, 950, 33, 28, "M30",  905,  3,  36, 46,   139,  812.8,  858,   817.0, 797.0),
    (850,  1070, 1000,33, 28, "M30",  955,  3,  36, 48,   139,  863.6,  908,   868.0, 847.8),
    (900,  1120, 1050,33, 28, "M30",  1005, 3,  38, 50,   140,  914.4,  959,   919.0, 898.6),
    (1000, 1235, 1160,39, 28, "M36",  1110, 3,  40, 56,   151,  1016.0, 1065,  1021.0, 1000.2),
    (1100, 1345, 1270,39, 28, "M36",  1220, 3,  42, 62,   170,  1117.6, 1174,  1122.0, 1098.6),
    (1200, 1465, 1380,39, 32, "M36",  1325, 3,  44, 66,   182,  1219.2, 1281,  1224.0, 1200.2),
    (1350, 1630, 1540,45, 36, "M42",  1480, 3,  48, 74,   200,  1371.6, 1438,  1376.0, 1346.2),
    (1500, 1795, 1700,45, 40, "M42",  1635, 3,  50, 82,   218,  1524.0, 1598,  1529.0, 1498.6),
]

# Bảng kích thước JIS 7.5K (0.75 MPa)
JIS_7K5_RAW_DATA = [
    # DN,  D,    C,    h,  No, bolt,   g,    f,  t,  t_bl, T_it, a(OD),  b,     d0,    d_bore
    (40,   140,  105,  19, 4,  "M16",  85,   2,  16, 16,   38,   48.6,   62,    49.1,  41.6),
    (50,   155,  120,  19, 4,  "M16",  100,  2,  16, 16,   40,   60.5,   75,    61.1,  52.9),
    (65,   175,  140,  19, 4,  "M16",  120,  2,  18, 18,   44,   76.3,   92,    77.1,  67.9),
    (80,   185,  150,  19, 8,  "M16",  130,  2,  18, 18,   45,   89.1,   105,   90.0,  80.7),
    (100,  210,  175,  19, 8,  "M16",  155,  2,  20, 20,   45,   114.3,  130,   115.4, 105.3),
    (125,  250,  210,  19, 8,  "M16",  185,  2,  20, 20,   47,   139.8,  156,   141.2, 130.8),
    (150,  280,  240,  19, 8,  "M16",  215,  2,  22, 22,   53,   165.2,  184,   166.6, 155.2),
    (200,  342,  299,  19, 8,  "M16",  256,  3,  27, 27,   58,   216.3,  238,   218.0, 204.7),
    (250,  410,  360,  23, 12, "M20",  314,  3,  29, 29,   65,   267.4,  292,   269.5, 254.2),
    (300,  464,  414,  23, 12, "M20",  364,  3,  30, 30,   68,   318.5,  345,   321.0, 304.7),
    (350,  510,  460,  23, 12, "M20",  414,  3,  32, 32,   79,   355.6,  388,   358.1, 339.8),
    (400,  565,  515,  25, 16, "M22",  465,  3,  34, 34,   85,   406.4,  442,   409.0, 390.6),
    (450,  620,  570,  25, 16, "M22",  520,  3,  36, 36,   90,   457.2,  495,   460.0, 441.4),
    (500,  675,  620,  25, 16, "M22",  570,  3,  38, 38,   90,   508.0,  546,   511.0, 492.2),
    (600,  795,  740,  25, 20, "M22",  680,  3,  42, 42,   112,  609.6,  648,   613.0, 593.8),
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS jis_b2220;")
    cur.execute("""
    CREATE TABLE jis_b2220 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        standard TEXT NOT NULL DEFAULT 'JIS_B_2220',
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
        d0 REAL NOT NULL,
        pipe_od REAL NOT NULL,
        d_bore REAL NOT NULL,
        CONSTRAINT uq_flange UNIQUE (standard, rating, flange_type, dn)
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_flange_lookup ON jis_b2220(standard, rating, flange_type, dn);")
    
    records = []
    # 1. Nạp 10K
    for dn, d, c, h, no, bolt, g, f, t, t_bl, T_it, a_od, b, d0, d_bore in JIS_10K_RAW_DATA:
        records.append(('JIS_B_2220', '10K', 'IT', dn, d, c, h, no, bolt, g, f, t, T_it, a_od, b, d0, a_od, d_bore))
        records.append(('JIS_B_2220', '10K', 'SOP', dn, d, c, h, no, bolt, g, f, t, t, 0.0, 0.0, d0, a_od, d_bore))
        records.append(('JIS_B_2220', '10K', 'WN', dn, d, c, h, no, bolt, g, f, t, T_it, a_od, b, d0, a_od, d_bore))
        records.append(('JIS_B_2220', '10K', 'BL', dn, d, c, h, no, bolt, g, f, t_bl, t_bl, 0.0, 0.0, 0.0, a_od, 0.0))

    # 2. Nạp 7.5K
    for dn, d, c, h, no, bolt, g, f, t, t_bl, T_it, a_od, b, d0, d_bore in JIS_7K5_RAW_DATA:
        records.append(('JIS_B_2220', '7K5', 'IT', dn, d, c, h, no, bolt, g, f, t, T_it, a_od, b, d0, a_od, d_bore))
        records.append(('JIS_B_2220', '7K5', 'SOP', dn, d, c, h, no, bolt, g, f, t, t, 0.0, 0.0, d0, a_od, d_bore))
        records.append(('JIS_B_2220', '7K5', 'WN', dn, d, c, h, no, bolt, g, f, t, T_it, a_od, b, d0, a_od, d_bore))
        records.append(('JIS_B_2220', '7K5', 'BL', dn, d, c, h, no, bolt, g, f, t_bl, t_bl, 0.0, 0.0, 0.0, a_od, 0.0))

    cur.executemany("""
    INSERT OR REPLACE INTO jis_b2220 
    (standard, rating, flange_type, dn, d, c, h, no, bolt_name, g, f, t, total_len, hub_small, hub_large, d0, pipe_od, d_bore)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    
    conn.commit()
    conn.close()
    print(f"[OK] Database initialized successfully at: {DB_PATH}")
    print(f"[OK] Seeded {len(records)} rows for JIS B 2220 with standard='JIS_B_2220'.")
    
    generate_python_dataset(records)


def generate_python_dataset(records):
    lines = [
        "# Auto-generated from jis_b2220_seed.py. DO NOT EDIT DIRECTLY.",
        "from ..models.dimensions import FlangeDimensions",
        "",
        "# Khóa tra cứu: (standard, rating, flange_type, dn)",
        "JIS_B2220_FLANGE_DATASET = {"
    ]
    for r in records:
        key = f'("{r[0]}", "{r[1]}", "{r[2]}", {r[3]})'
        lines.append(f'    {key}: FlangeDimensions(')
        lines.append(f'        standard="{r[0]}",')
        lines.append(f'        rating="{r[1]}",')
        lines.append(f'        flange_type="{r[2]}",')
        lines.append(f'        dn={r[3]},')
        lines.append(f'        d={float(r[4])},')
        lines.append(f'        c={float(r[5])},')
        lines.append(f'        h={float(r[6])},')
        lines.append(f'        no={int(r[7])},')
        lines.append(f'        bolt_name="{r[8]}",')
        lines.append(f'        g={float(r[9])},')
        lines.append(f'        f={float(r[10])},')
        lines.append(f'        t={float(r[11])},')
        lines.append(f'        total_len={float(r[12])},')
        lines.append(f'        hub_small={float(r[13])},')
        lines.append(f'        hub_large={float(r[14])},')
        lines.append(f'        d0={float(r[15])},')
        lines.append(f'        pipe_od={float(r[16])},')
        lines.append(f'        d_bore={float(r[17])}')
        lines.append('    ),')
    lines.append("}")
    lines.append("")

    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] Generated pure-Python dataset at: {DATASET_PATH}")


if __name__ == "__main__":
    init_db()
