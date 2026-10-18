import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thư mục gốc dự án
current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(current_dir))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from _fvc_fasteners import (
    get_bolt_for_flange,
    get_metric_bolt_spec,
    MetricBoltSpec,
    FlangeBoltSelection
)

def run_tests():
    print("=== KIỂM THỬ PACKAGE _FVC_FASTENERS (JIS B 1217 : 2018) ===")
    
    # 1. Kiểm tra bảng metric_bolt_standards (JIS B 1180 / 1181)
    print("\n--- 1. Kiểm tra quy cách hình học Bu-lông hệ Mét (JIS B 1180 / 1181) ---")
    sizes_to_test = ["M10", "M12", "M16", "M20", "M22", "M24", "M30", "M30x3", "M36", "M36x3", "M42", "M42x3"]
    for sz in sizes_to_test:
        spec = get_metric_bolt_spec(sz)
        assert spec is not None, f"Không tìm thấy spec cho {sz}"
        assert spec.standard == "JIS_B_1180"
        print(f"[OK] {spec.standard} {sz}: Dia={spec.nominal_dia}mm, Pitch={spec.pitch}mm, Giác s={spec.s}mm, Ê-cu m={spec.m}mm, Mũ k={spec.k}mm")

    # 2. Kiểm tra bảng tra Bu-lông Mặt bích theo từng cấp áp (JIS B 1217 : 2018)
    print("\n--- 2. Kiểm tra bảng tra Bu-lông Mặt bích theo từng cấp áp (JIS B 1217 : 2018) ---")
    test_cases = [
        ("5K", 50, "M12", 4, 52.0, 70.0, 3.0),
        ("5K", 100, "M16", 8, 61.0, 84.0, 3.0),
        ("10K", 50, "M16", 4, 61.0, 84.0, 3.0),
        ("10K", 100, "M16", 8, 65.0, 88.0, 3.0),
        ("10K", 200, "M20", 12, 79.0, 107.0, 3.0),
        ("10K_THIN", 100, "M12", 8, 56.0, 74.0, 3.0),
        ("16K", 50, "M16", 8, 61.0, 84.0, 3.0),
        ("16K", 100, "M20", 8, 79.0, 107.0, 3.0),
        ("20K", 50, "M16", 8, 66.0, 89.0, 4.5),
        ("20K", 100, "M20", 8, 85.0, 113.0, 4.5),
        ("30K", 100, "M22", 8, 102.0, 131.0, 4.5),
        ("40K", 100, "M22", 8, 110.0, 139.0, 4.5),
        ("63K", 100, "M24", 8, 130.0, 164.0, 4.5),
        ("63K", 400, "M42x3", 16, 235.0, 281.0, 4.5),
    ]

    for rating, dn, exp_bolt, exp_count, exp_l, exp_lt, exp_tg in test_cases:
        bolt_sel = get_bolt_for_flange(rating=rating, dn=dn, flange_std="JIS_B_2220")
        assert bolt_sel is not None, f"Không tìm thấy bu-lông cho ({rating}, DN{dn})"
        assert bolt_sel.standard == "JIS_B_1217"
        assert bolt_sel.flange_std == "JIS_B_2220"
        assert bolt_sel.bolt_size == exp_bolt
        assert bolt_sel.bolt_count == exp_count
        assert bolt_sel.l == exp_l
        assert bolt_sel.lt == exp_lt
        assert bolt_sel.tg == exp_tg
        print(f"[OK] {bolt_sel.standard} | Bích {bolt_sel.flange_std} {rating} DN{dn:4d}: Bu-lông {bolt_sel.bolt_size} x {bolt_sel.bolt_count:2d} | l={bolt_sel.l:3.0f}mm, lt={bolt_sel.lt:3.0f}mm, tg={bolt_sel.tg:3.1f}mm")

    print("\n>>> TẤT CẢ TEST TRONG _FVC_FASTENERS ĐÃ ĐẠT 100%! <<<")

if __name__ == "__main__":
    run_tests()
