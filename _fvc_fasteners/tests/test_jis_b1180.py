"""Unit tests cho module JIS B 1180 : 2014 trong gói _fvc_fasteners."""
import sys
import unittest

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from _fvc_fasteners.db.jis_b1180_reader import (
    get_bolt_type,
    get_head_dimension,
    get_hex_bolt,
    list_available_bolt_types,
    calculate_thread_length,
)
from _fvc_fasteners.geometry.bolt import HexBolt


class TestJisB1180(unittest.TestCase):
    def test_list_all_bolt_types(self):
        """Kiểm tra có đủ 7 loại chính + Phụ lục JA."""
        types = list_available_bolt_types()
        self.assertEqual(len(types), 8)
        codes = [t.type_code for t in types]
        self.assertIn("TYPE_1_NOMINAL_COARSE_GRADE_C", codes)
        self.assertIn("TYPE_2_NOMINAL_COARSE_GRADE_AB", codes)
        self.assertIn("TYPE_3_NOMINAL_FINE_GRADE_AB", codes)
        self.assertIn("TYPE_4_FULL_COARSE_GRADE_AB", codes)
        self.assertIn("TYPE_5_FULL_COARSE_GRADE_C", codes)
        self.assertIn("TYPE_6_FULL_FINE_GRADE_AB", codes)
        self.assertIn("TYPE_7_REDUCED_COARSE_GRADE_B", codes)
        self.assertIn("TYPE_8_ANNEX_JA_TRADITIONAL", codes)

    def test_default_flange_bolt_type(self):
        """Kiểm tra Loại 2 là mặc định cho mối nối mặt bích."""
        t2 = get_bolt_type("TYPE_2_NOMINAL_COARSE_GRADE_AB")
        self.assertIsNotNone(t2)
        self.assertTrue(t2.is_flange_default)
        self.assertEqual(t2.iso_standard, "ISO 4014")
        self.assertEqual(t2.thread_style, "NOMINAL_SHANK")
        self.assertEqual(t2.pitch_type, "COARSE")

    def test_head_dimensions_iso_grade_ab(self):
        """Kiểm tra kích thước đầu Cấp A/B (có gờ đệm dw)."""
        head_m16 = get_head_dimension("M16", "ISO_GRADE_AB")
        self.assertIsNotNone(head_m16)
        self.assertEqual(head_m16.s_nominal, 24.0)
        self.assertEqual(head_m16.k_nominal, 10.0)
        self.assertEqual(head_m16.dw_min, 22.49)
        self.assertEqual(head_m16.c_min, 0.20)
        self.assertEqual(head_m16.c_max, 0.80)
        self.assertEqual(head_m16.r_min, 0.60)

        head_m12 = get_head_dimension("M12", "ISO_GRADE_AB")
        self.assertEqual(head_m12.s_nominal, 18.0)
        self.assertEqual(head_m12.k_nominal, 7.5)

    def test_head_dimensions_grade_c(self):
        """Kiểm tra kích thước đầu Cấp C (mặt tỳ phẳng, không bắt buộc gờ dw)."""
        head_m16_c = get_head_dimension("M16", "ISO_GRADE_C")
        self.assertIsNotNone(head_m16_c)
        self.assertEqual(head_m16_c.s_nominal, 24.0)
        self.assertEqual(head_m16_c.k_nominal, 10.0)
        self.assertIsNone(head_m16_c.dw_min)
        self.assertIsNone(head_m16_c.c_min)

    def test_annex_ja_traditional_differences(self):
        """Kiểm tra điểm khác biệt giác s của Phụ lục JA (JIS truyền thống)."""
        # M10: ISO s = 16, JA s = 17
        m10_iso = get_head_dimension("M10", "ISO_GRADE_AB")
        m10_ja = get_head_dimension("M10", "ANNEX_JA")
        self.assertEqual(m10_iso.s_nominal, 16.0)
        self.assertEqual(m10_ja.s_nominal, 17.0)

        # M12: ISO s = 18, JA s = 19
        m12_iso = get_head_dimension("M12", "ISO_GRADE_AB")
        m12_ja = get_head_dimension("M12", "ANNEX_JA")
        self.assertEqual(m12_iso.s_nominal, 18.0)
        self.assertEqual(m12_ja.s_nominal, 19.0)

        # M14: ISO s = 21, JA s = 22
        m14_iso = get_head_dimension("M14", "ISO_GRADE_AB")
        m14_ja = get_head_dimension("M14", "ANNEX_JA")
        self.assertEqual(m14_iso.s_nominal, 21.0)
        self.assertEqual(m14_ja.s_nominal, 22.0)

        # M22: ISO s = 34, JA s = 32
        m22_iso = get_head_dimension("M22", "ISO_GRADE_AB")
        m22_ja = get_head_dimension("M22", "ANNEX_JA")
        self.assertEqual(m22_iso.s_nominal, 34.0)
        self.assertEqual(m22_ja.s_nominal, 32.0)

    def test_calculate_thread_length_formulas(self):
        """Kiểm tra công thức tính chiều dài ren b theo JIS B 1180."""
        # l <= 125: b = 2*d + 6 (M16 có d=16 -> b = 38)
        self.assertEqual(calculate_thread_length(65.0, 16.0, "NOMINAL_SHANK"), 38.0)
        self.assertEqual(calculate_thread_length(100.0, 16.0, "NOMINAL_SHANK"), 38.0)

        # 125 < l <= 200: b = 2*d + 12 (M16 có d=16 -> b = 44)
        self.assertEqual(calculate_thread_length(150.0, 16.0, "NOMINAL_SHANK"), 44.0)

        # l > 200: b = 2*d + 25 (M16 có d=16 -> b = 57)
        self.assertEqual(calculate_thread_length(220.0, 16.0, "NOMINAL_SHANK"), 57.0)

        # Full thread: b = l
        self.assertEqual(calculate_thread_length(65.0, 16.0, "FULL_THREAD"), 65.0)

    def test_get_hex_bolt_flange_default(self):
        """Kiểm tra tạo bu lông M16x65 cho mặt bích."""
        bolt = get_hex_bolt(bolt_size="M16", length=65.0)
        self.assertIsNotNone(bolt)
        self.assertEqual(bolt.standard, "JIS_B_1180")
        self.assertEqual(bolt.type_code, "TYPE_2_NOMINAL_COARSE_GRADE_AB")
        self.assertEqual(bolt.nominal_dia, 16.0)
        self.assertEqual(bolt.pitch, 2.0)
        self.assertEqual(bolt.length, 65.0)
        self.assertEqual(bolt.thread_length, 38.0)
        self.assertEqual(bolt.shank_length, 27.0)
        self.assertEqual(bolt.shank_dia, 16.0)
        self.assertEqual(bolt.head.s_nominal, 24.0)
        self.assertEqual(bolt.head.k_nominal, 10.0)
        self.assertEqual(bolt.head.dw_min, 22.49)

    def test_get_hex_bolt_reduced_shank(self):
        """Kiểm tra tạo bu lông thân thắt (Loại 7 - ISO 4015)."""
        bolt = get_hex_bolt(bolt_size="M16", length=65.0, type_code="TYPE_7_REDUCED_COARSE_GRADE_B")
        self.assertIsNotNone(bolt)
        self.assertEqual(bolt.type_code, "TYPE_7_REDUCED_COARSE_GRADE_B")
        # Thân thắt xấp xỉ d - 0.6495 * P = 16 - 0.6495*2 = 14.70
        self.assertEqual(bolt.shank_dia, 14.7)

    def test_hex_bolt_geometry_wrapper(self):
        """Kiểm tra gọi hàm dựng hình HexBolt ngoài AutoCAD."""
        obj = HexBolt(None, bolt_size="M20", length=80.0)
        self.assertIsNotNone(obj)
        self.assertIsNotNone(obj.spec)
        self.assertEqual(obj.spec.nominal_dia, 20.0)
        self.assertEqual(obj.spec.head.s_nominal, 30.0)
        self.assertEqual(obj.spec.head.k_nominal, 12.5)


if __name__ == "__main__":
    unittest.main()
