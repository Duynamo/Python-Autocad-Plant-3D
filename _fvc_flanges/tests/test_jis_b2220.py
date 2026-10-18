import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(current_dir))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from _fvc_flanges import (
    JisB2220Flange,
    JisFlange,
    get_flange_dimensions,
    FlangeDimensions
)

def run_tests():
    print("=== KIỂM THỬ PACKAGE _FVC_FLANGES (JIS B 2220) ===")
    
    # 1. Kiểm tra truy vấn kích thước bích JIS B 2220
    test_cases = [
        ("10K", 50, "IT", 155.0, 120.0, 16.0, 4, "M16"),
        ("10K", 100, "IT", 210.0, 175.0, 18.0, 8, "M16"),
        ("10K", 200, "SOP", 330.0, 290.0, 22.0, 12, "M20"),
        ("7K5", 100, "IT", 210.0, 175.0, 20.0, 8, "M16"),
        ("7K5", 200, "SOP", 342.0, 299.0, 27.0, 8, "M16"),
    ]
    
    print("\n--- 1. Kiểm tra trường standard và kích thước bích JIS B 2220 ---")
    for rating, dn, f_type, exp_d, exp_c, exp_t, exp_no, exp_bolt in test_cases:
        dim = get_flange_dimensions(rating=rating, dn=dn, flange_type=f_type, standard="JIS_B_2220")
        assert dim.standard == "JIS_B_2220", f"Sai standard: {dim.standard}"
        assert dim.d == exp_d, f"Sai D: {dim.d} != {exp_d}"
        assert dim.c == exp_c, f"Sai C: {dim.c} != {exp_c}"
        assert dim.t == exp_t, f"Sai t: {dim.t} != {exp_t}"
        assert dim.no == exp_no, f"Sai số lỗ bu lông: {dim.no} != {exp_no}"
        assert dim.bolt_name == exp_bolt, f"Sai tên bu lông: {dim.bolt_name} != {exp_bolt}"
        print(f"[OK] {dim.standard} {dim.rating} {dim.flange_type} DN{dim.dn:3d}: D={dim.d:3.0f}mm, C={dim.c:3.0f}mm, t={dim.t:2.0f}mm, {dim.no} lỗ {dim.bolt_name}")

    # 2. Kiểm tra liên kết sang _fvc_fasteners qua thuộc tính .bolt
    print("\n--- 2. Kiểm tra liên kết tự động sang _fvc_fasteners (.bolt) ---")
    dim100 = get_flange_dimensions("10K", 100, "IT")
    from _fvc_fasteners import get_bolt_for_flange
    bolt100 = get_bolt_for_flange(rating="10K", dn=100, flange_std=dim100.standard)
    assert bolt100 is not None
    assert bolt100.standard == "JIS_B_1217"
    assert bolt100.flange_std == "JIS_B_2220"
    assert bolt100.bolt_size == "M16"
    assert bolt100.bolt_count == 8
    assert bolt100.l == 65.0
    print(f"[OK] Liên kết thành công: Bích {dim100.standard} 10K DN100 -> Bu lông {bolt100.standard} {bolt100.bolt_size} x {bolt100.bolt_count} con (l={bolt100.l}mm, tg={bolt100.tg}mm)")

    print("\n>>> TẤT CẢ TEST TRONG _FVC_FLANGES ĐÃ ĐẠT 100%! <<<")

if __name__ == "__main__":
    run_tests()
