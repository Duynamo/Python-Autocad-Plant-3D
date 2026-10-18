import os
from typing import Dict, Tuple, Optional
from ..models.dimensions import FlangeDimensions
from ..data import DB_PATH, JIS_B2220_FLANGE_DATASET

_CACHE: Dict[Tuple[str, str, str, int], FlangeDimensions] = {}

def get_flange_dimensions(
    rating: str = "10K",
    dn: int = 50,
    flange_type: str = "IT",
    standard: str = "JIS_B_2220"
) -> FlangeDimensions:
    """Truy vấn kích thước mặt bích JIS B 2220 theo Standard, Rating, DN, FlangeType.
    
    Args:
        rating: Cấp áp ('10K', '7K5', '5K', '20K')
        dn: Cỡ danh định A (10, 15, ..., 1500)
        flange_type: Loại bích ('IT', 'SOP', 'WN', 'BL')
        standard: Tiêu chuẩn bích ('JIS_B_2220'). Mặc định là 'JIS_B_2220'.
    
    Returns:
        FlangeDimensions: Đối tượng chứa đầy đủ kích thước kỹ thuật.
    """
    std_clean = standard.strip().upper()
    rating_clean = rating.strip().upper()
    type_clean = flange_type.strip().upper()
    cache_key = (std_clean, rating_clean, type_clean, dn)
    
    if cache_key in _CACHE:
        return _CACHE[cache_key]
        
    # 1. Tra cứu trực tiếp từ bộ dữ liệu thuần Python
    if cache_key in JIS_B2220_FLANGE_DATASET:
        dim = JIS_B2220_FLANGE_DATASET[cache_key]
        _CACHE[cache_key] = dim
        return dim
        
    # 2. Phương án dự phòng: Tra cứu SQLite
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT standard, rating, flange_type, dn, d, c, h, no, bolt_name, g, f, t, total_len, hub_small, hub_large, d0, pipe_od, d_bore
                FROM jis_b2220
                WHERE standard = ? AND rating = ? AND flange_type = ? AND dn = ?
            """, (std_clean, rating_clean, type_clean, dn))
            row = cur.fetchone()
            conn.close()
            
            if row:
                dim = FlangeDimensions(
                    standard=row[0],
                    rating=row[1],
                    flange_type=row[2],
                    dn=row[3],
                    d=row[4],
                    c=row[5],
                    h=row[6],
                    no=row[7],
                    bolt_name=row[8] if row[8] else "",
                    g=row[9],
                    f=row[10],
                    t=row[11],
                    total_len=row[12] if row[12] else row[11],
                    hub_small=row[13] if row[13] else 0.0,
                    hub_large=row[14] if row[14] else 0.0,
                    d0=row[15],
                    pipe_od=row[16],
                    d_bore=row[17],
                    inner_dia=row[15]
                )
                _CACHE[cache_key] = dim
                return dim
    except (ImportError, Exception):
        pass
        
    raise ValueError(
        f"[ERROR] Không tìm thấy kích thước mặt bích: Standard={std_clean}, Rating={rating_clean}, "
        f"Type={type_clean}, DN={dn}. Vui lòng kiểm tra lại data seed!"
    )
