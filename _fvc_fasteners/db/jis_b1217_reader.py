import os
from typing import Dict, Tuple, Optional
from ..models.jis_b1217_specs import MetricBoltSpec, FlangeBoltSelection
from ..data import DB_PATH, JIS_B1180_METRIC_DATASET, JIS_B1217_BOLT_DATASET

_BOLT_CACHE: Dict[Tuple[str, str, int], FlangeBoltSelection] = {}
_SPEC_CACHE: Dict[str, MetricBoltSpec] = {}

def get_bolt_for_flange(
    rating: str = "10K",
    dn: int = 50,
    flange_std: str = "JIS_B_2220"
) -> Optional[FlangeBoltSelection]:
    """Truy vấn thông số bu-lông chuẩn cho mặt bích theo JIS B 1217 : 2018.
    
    Args:
        rating: Cấp áp lực ('5K', '10K', '10K_THIN', '16K', '20K', '30K', '40K', '63K')
        dn: Cỡ danh định A (10, 15, ..., 1500)
        flange_std: Tiêu chuẩn bích kết nối ('JIS_B_2220' hoặc 'JIS_B_2239'). Mặc định là 'JIS_B_2220'.
        
    Returns:
        FlangeBoltSelection: Cỡ ren, số lượng, chiều dài l, b, lt, bt, bề dày gioăng tg.
    """
    rating_clean = rating.strip().upper()
    std_clean = flange_std.strip().upper()
    cache_key = (std_clean, rating_clean, dn)
    
    if cache_key in _BOLT_CACHE:
        return _BOLT_CACHE[cache_key]
        
    # 1. Tra cứu từ bộ dữ liệu thuần Python
    if cache_key in JIS_B1217_BOLT_DATASET:
        selection = JIS_B1217_BOLT_DATASET[cache_key]
        _BOLT_CACHE[cache_key] = selection
        return selection
        
    # 2. Dự phòng: Tra cứu từ SQLite nếu có
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT standard, flange_std, rating, dn, bolt_size, bolt_count, l, b, lt, bt, tg
                FROM jis_b1217_flange_bolts
                WHERE flange_std = ? AND rating = ? AND dn = ?
            """, (std_clean, rating_clean, dn))
            row = cur.fetchone()
            conn.close()
            if row:
                selection = FlangeBoltSelection(
                    standard=row[0],
                    flange_std=row[1],
                    rating=row[2],
                    dn=row[3],
                    bolt_size=row[4],
                    bolt_count=row[5],
                    l=row[6],
                    b=row[7],
                    lt=row[8],
                    bt=row[9],
                    tg=row[10]
                )
                _BOLT_CACHE[cache_key] = selection
                return selection
    except Exception:
        pass
        
    return None


def get_metric_bolt_spec(size: str = "M16") -> Optional[MetricBoltSpec]:
    """Truy vấn quy cách hình học bu-lông lục giác & đai ốc JIS B 1180 / 1181.
    
    Args:
        size: Ký hiệu ren ('M10', 'M12', 'M16', 'M20', 'M22', 'M24', 'M30', 'M30x3'...)
        
    Returns:
        MetricBoltSpec: Bước ren, bề rộng giác s, chiều cao ê-cu m, chiều cao mũ k.
    """
    size_clean = size.strip().upper().replace("X", "x")
    
    if size_clean in _SPEC_CACHE:
        return _SPEC_CACHE[size_clean]
        
    # 1. Tra cứu thuần Python
    if size_clean in JIS_B1180_METRIC_DATASET:
        spec = JIS_B1180_METRIC_DATASET[size_clean]
        _SPEC_CACHE[size_clean] = spec
        return spec
        
    # 2. Dự phòng SQLite
    try:
        import sqlite3
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT standard, size, nominal_dia, pitch, s, e, m, k, washer_t, washer_od
                FROM metric_bolt_standards
                WHERE size = ?
            """, (size_clean,))
            row = cur.fetchone()
            conn.close()
            if row:
                spec = MetricBoltSpec(
                    standard=row[0],
                    size=row[1],
                    nominal_dia=row[2],
                    pitch=row[3],
                    s=row[4],
                    e=row[5],
                    m=row[6],
                    k=row[7],
                    washer_t=row[8],
                    washer_od=row[9]
                )
                _SPEC_CACHE[size_clean] = spec
                return spec
    except Exception:
        pass
        
    return None
