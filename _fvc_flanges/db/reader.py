import os
from typing import Dict, Tuple, Optional
from ..models.dimensions import FlangeDimensions
from ..data import DB_PATH, FLANGE_DATASET

_CACHE: Dict[Tuple[str, str, int], FlangeDimensions] = {}

def get_flange_dimensions(rating: str = "10K", dn: int = 50, flange_type: str = "IT") -> FlangeDimensions:
    """Truy vấn kích thước mặt bích JIS B 2220 theo Rating, DN, FlangeType.
    
    Args:
        rating: Cấp áp ('10K', '7K5', '5K', '20K')
        dn: Cỡ danh định A (10, 15, ..., 1500)
        flange_type: Loại bích ('IT', 'SOP', 'WN', 'BL')
    
    Returns:
        FlangeDimensions: Đối tượng chứa đầy đủ kích thước kỹ thuật.
    """
    rating_clean = rating.strip().upper()
    type_clean = flange_type.strip().upper()
    cache_key = (rating_clean, type_clean, dn)
    
    if cache_key in _CACHE:
        return _CACHE[cache_key]
        
    # 1. Tra cứu trực tiếp từ bộ dữ liệu thuần Python (Hoạt động tốt trong AutoCAD Plant 3D khi không có module _sqlite3)
    if cache_key in FLANGE_DATASET:
        dim = FLANGE_DATASET[cache_key]
        _CACHE[cache_key] = dim
        return dim
        
    # 2. Phương án dự phòng: Tra cứu SQLite nếu môi trường có sẵn module sqlite3 và file database tồn tại
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT rating, flange_type, dn, d, c, h, no, bolt_name, g, f, t, total_len, hub_small, hub_large, d0, pipe_od, d_bore
                FROM jis_b2220
                WHERE rating = ? AND flange_type = ? AND dn = ?
            """, (rating_clean, type_clean, dn))
            row = cur.fetchone()
            conn.close()
            
            if row:
                dim = FlangeDimensions(
                    rating=row[0],
                    flange_type=row[1],
                    dn=row[2],
                    d=row[3],
                    c=row[4],
                    h=row[5],
                    no=row[6],
                    bolt_name=row[7] if row[7] else "",
                    g=row[8],
                    f=row[9],
                    t=row[10],
                    total_len=row[11] if row[11] else row[10],
                    hub_small=row[12] if row[12] else 0.0,
                    hub_large=row[13] if row[13] else 0.0,
                    d0=row[14],
                    pipe_od=row[15],
                    d_bore=row[16],
                    inner_dia=row[14]
                )
                _CACHE[cache_key] = dim
                return dim
    except (ImportError, Exception):
        pass
        
    raise ValueError(
        f"Không tìm thấy thông số bích JIS B 2220 cho: Rating='{rating}', Type='{flange_type}', DN={dn}."
    )

