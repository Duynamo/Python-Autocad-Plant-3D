"""Unit tests toàn diện cho module đai ốc JIS B 1181 : 2014 trong gói _fvc_fasteners."""
import os
import sqlite3
import sys
import time
import unittest

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from _fvc_fasteners.models.jis_b1181_specs import NutDimensionSpec, NutTypeSpec, HexNutSpec
from _fvc_fasteners.db.jis_b1181_reader import (
    get_nut_type,
    list_available_nut_types,
    get_nut_dimension,
    list_available_nut_sizes,
    get_hex_nut,
    get_matching_nut_for_bolt,
)
from _fvc_fasteners.data.jis_b1181_seed import DB_PATH
from _fvc_fasteners.geometry.nut import HexNut


class TestJisB1181(unittest.TestCase):
    """Bộ kiểm thử tính toàn vẹn dữ liệu, kích thước hình học và hiệu năng của JIS B 1181."""

    def test_list_all_12_nut_types(self):
        """Kiểm tra có đầy đủ 12 chủng loại đai ốc (8 ISO + 4 Phụ lục JA)."""
        types = list_available_nut_types()
        self.assertEqual(len(types), 12, "Phải có chính xác 12 chủng loại đai ốc theo JIS B 1181 : 2014")
        
        codes = [t.type_code for t in types]
        expected_codes = [
            "ISO_4032_STYLE_1_COARSE",
            "ISO_8673_STYLE_1_FINE",
            "ISO_4034_STYLE_1_GRADE_C",
            "ISO_4033_STYLE_2_COARSE",
            "ISO_8674_STYLE_2_FINE",
            "ISO_4035_STYLE_0_THIN_COARSE",
            "ISO_8675_STYLE_0_THIN_FINE",
            "ISO_4036_STYLE_0_UNCHAMFERED",
            "JA_TYPE_1_REGULAR",
            "JA_TYPE_2_REGULAR",
            "JA_TYPE_3_THIN",
            "JA_TYPE_4_WASHER_FACE",
        ]
        for ec in expected_codes:
            self.assertIn(ec, codes, f"Mã loại {ec} phải tồn tại trong danh mục")

    def test_default_flange_nut_type(self):
        """Kiểm tra đai ốc Style 1 Coarse (ISO 4032) là mặc định cho mặt bích."""
        t1 = get_nut_type("ISO_4032_STYLE_1_COARSE")
        self.assertIsNotNone(t1)
        self.assertTrue(t1.is_flange_default)
        self.assertEqual(t1.iso_standard, "ISO 4032")
        self.assertEqual(t1.nut_style, "STYLE_1")
        self.assertEqual(t1.pitch_type, "COARSE")
        self.assertEqual(t1.dimension_series, "ISO_STYLE_1")

    def test_style_1_dimensions_iso_grade_ab(self):
        """Kiểm tra kích thước đai ốc Style 1 (ISO 4032) theo Bảng 3 tiêu chuẩn."""
        # Kiểm tra M16
        m16 = get_nut_dimension("M16", "ISO_STYLE_1")
        self.assertIsNotNone(m16)
        self.assertEqual(m16.s_nominal, 24.0, "M16 phải có giác s = 24 mm")
        self.assertEqual(m16.s_max, 24.0)
        self.assertEqual(m16.s_min, 23.67)
        self.assertEqual(m16.m_nominal, 14.8, "M16 Style 1 phải có chiều cao m = 14.8 mm")
        self.assertEqual(m16.m_max, 14.8)
        self.assertEqual(m16.m_min, 14.1)
        self.assertEqual(m16.dw_min, 22.5, "M16 Style 1 phải có gờ đệm dw_min = 22.5 mm")
        self.assertEqual(m16.e_min, 26.75)
        self.assertEqual(m16.nominal_dia, 16.0)
        self.assertEqual(m16.pitch, 2.0)

        # Kiểm tra M20
        m20 = get_nut_dimension("M20", "ISO_STYLE_1")
        self.assertIsNotNone(m20)
        self.assertEqual(m20.s_nominal, 30.0, "M20 phải có giác s = 30 mm")
        self.assertEqual(m20.m_nominal, 18.0, "M20 Style 1 phải có m = 18.0 mm")
        self.assertEqual(m20.dw_min, 27.7)

        # Kiểm tra M12 (Lưu ý: ISO 4032 quy định s=18 mm, khác với JIS cũ s=19 mm)
        m12 = get_nut_dimension("M12", "ISO_STYLE_1")
        self.assertIsNotNone(m12)
        self.assertEqual(m12.s_nominal, 18.0, "ISO 4032 quy định M12 có giác s = 18 mm")
        self.assertEqual(m12.m_nominal, 10.8)

    def test_style_2_high_nut_dimensions(self):
        """Kiểm tra đai ốc dày Style 2 (ISO 4033) có m ≈ 1.0d lớn hơn Style 1."""
        m16_style1 = get_nut_dimension("M16", "ISO_STYLE_1")
        m16_style2 = get_nut_dimension("M16", "ISO_STYLE_2")
        self.assertIsNotNone(m16_style2)
        self.assertEqual(m16_style2.s_nominal, 24.0)
        self.assertEqual(m16_style2.m_nominal, 16.4, "M16 Style 2 phải có m = 16.4 mm")
        self.assertGreater(m16_style2.m_nominal, m16_style1.m_nominal, "Style 2 phải cao hơn Style 1")

        m20_style2 = get_nut_dimension("M20", "ISO_STYLE_2")
        self.assertEqual(m20_style2.m_nominal, 20.3, "M20 Style 2 phải có m = 20.3 mm")

    def test_style_0_thin_nut_dimensions(self):
        """Kiểm tra đai ốc mỏng Style 0 (ISO 4035) có m ≈ 0.5d và vát mép 2 mặt."""
        m16_thin = get_nut_dimension("M16", "ISO_STYLE_0_THIN")
        self.assertIsNotNone(m16_thin)
        self.assertEqual(m16_thin.s_nominal, 24.0)
        self.assertEqual(m16_thin.m_nominal, 8.0, "M16 Style 0 phải có m = 8.0 mm")
        self.assertEqual(m16_thin.chamfer_sides, 2, "Style 0 phải vát mép 2 mặt")

        m20_thin = get_nut_dimension("M20", "ISO_STYLE_0_THIN")
        self.assertEqual(m20_thin.m_nominal, 10.0, "M20 Style 0 phải có m = 10.0 mm")

    def test_grade_c_dimensions(self):
        """Kiểm tra đai ốc Cấp C (ISO 4034) không có gờ đệm dw."""
        m16_c = get_nut_dimension("M16", "ISO_GRADE_C")
        self.assertIsNotNone(m16_c)
        self.assertEqual(m16_c.s_nominal, 24.0)
        self.assertEqual(m16_c.m_nominal, 14.8)
        self.assertIsNone(m16_c.dw_min, "Đai ốc cấp C không tiện gờ đệm mặt tỳ nên dw_min = None")

    def test_annex_ja_regular_traditional_sizes(self):
        """Kiểm tra đai ốc hệ truyền thống Nhật Bản (Phụ lục JA): M10=17, M12=19, M14=22, M22=32."""
        ja_m10 = get_nut_dimension("M10", "ANNEX_JA_REGULAR")
        self.assertIsNotNone(ja_m10)
        self.assertEqual(ja_m10.s_nominal, 17.0, "JIS Annex JA quy định M10 giác s = 17 mm (khác ISO s=16)")
        self.assertEqual(ja_m10.m_nominal, 8.0)

        ja_m12 = get_nut_dimension("M12", "ANNEX_JA_REGULAR")
        self.assertIsNotNone(ja_m12)
        self.assertEqual(ja_m12.s_nominal, 19.0, "JIS Annex JA quy định M12 giác s = 19 mm (khác ISO s=18)")
        self.assertEqual(ja_m12.m_nominal, 10.0)

        ja_m14 = get_nut_dimension("M14", "ANNEX_JA_REGULAR")
        self.assertEqual(ja_m14.s_nominal, 22.0, "JIS Annex JA M14 giác s = 22 mm (khác ISO s=21)")

        ja_m22 = get_nut_dimension("M22", "ANNEX_JA_REGULAR")
        self.assertEqual(ja_m22.s_nominal, 32.0, "JIS Annex JA M22 giác s = 32 mm (khác ISO s=34)")

    def test_annex_ja_small_series(self):
        """Kiểm tra đai ốc cỡ nhỏ (小形) trong Phụ lục JA."""
        small_m10 = get_nut_dimension("M10", "ANNEX_JA_SMALL")
        self.assertIsNotNone(small_m10)
        self.assertEqual(small_m10.s_nominal, 14.0, "Đai ốc nhỏ M10 có giác s = 14 mm")

        small_m12 = get_nut_dimension("M12", "ANNEX_JA_SMALL")
        self.assertEqual(small_m12.s_nominal, 17.0, "Đai ốc nhỏ M12 có giác s = 17 mm")

        small_m16 = get_nut_dimension("M16", "ANNEX_JA_SMALL")
        self.assertEqual(small_m16.s_nominal, 22.0, "Đai ốc nhỏ M16 có giác s = 22 mm")

    def test_matching_nut_for_bolt(self):
        """Kiểm tra hàm tự động tìm đai ốc ghép cặp tương thích với bu lông mặt bích."""
        nut_m16 = get_matching_nut_for_bolt("M16", prefer_style="STYLE_1")
        self.assertIsNotNone(nut_m16)
        self.assertEqual(nut_m16.s_nominal, 24.0)
        self.assertEqual(nut_m16.m_nominal, 14.8)

        # Thử bước ren mịn M30x3
        nut_m30x3 = get_matching_nut_for_bolt("M30x3", prefer_style="STYLE_1")
        self.assertIsNotNone(nut_m30x3)
        self.assertEqual(nut_m30x3.s_nominal, 46.0)
        self.assertEqual(nut_m30x3.pitch, 3.0)

        # Ghép cặp đai ốc dày Style 2
        nut_m20_s2 = get_matching_nut_for_bolt("M20", prefer_style="STYLE_2")
        self.assertEqual(nut_m20_s2.m_nominal, 20.3)

    def test_get_hex_nut_bom_spec(self):
        """Kiểm tra khởi tạo đối tượng HexNutSpec hoàn chỉnh phục vụ BOM."""
        nut_obj = get_hex_nut("M16", "ISO_4032_STYLE_1_COARSE", "STEEL_CLASS_8")
        self.assertIsNotNone(nut_obj)
        self.assertEqual(nut_obj.nut_size, "M16")
        self.assertEqual(nut_obj.material, "STEEL_CLASS_8")
        self.assertIn("ISO 4032", nut_obj.full_designation)
        self.assertIn("M16", nut_obj.full_designation)

    def test_geometry_3d_nut_creation(self):
        """Kiểm tra hàm tạo hình học 3D Solid HexNut tương thích không lỗi."""
        # Dùng container mock None
        nut_3d = HexNut(None, bolt_size="M16", series="ISO_STYLE_1", has_hole=True)
        self.assertIsNotNone(nut_3d)
        self.assertEqual(nut_3d.spec.s, 24.0)
        self.assertEqual(nut_3d.spec.m, 14.8)
        self.assertEqual(nut_3d.spec.nominal_dia, 16.0)

    def test_sqlite_database_integrity(self):
        """Kiểm tra tính toàn vẹn của CSDL SQLite trên đĩa."""
        self.assertTrue(os.path.exists(DB_PATH), f"File SQLite phải tồn tại tại: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Kiểm tra bảng nut types
        cur.execute("SELECT COUNT(*) FROM jis_b1181_nut_types")
        count_types = cur.fetchone()[0]
        self.assertEqual(count_types, 12, "CSDL SQLite phải chứa 12 bản ghi types")

        # Kiểm tra bảng dimensions
        cur.execute("SELECT COUNT(*) FROM jis_b1181_nut_dimensions")
        count_dims = cur.fetchone()[0]
        self.assertGreater(count_dims, 100, "CSDL SQLite phải chứa trên 100 dòng kích thước chi tiết")

        # Kiểm tra bảng materials
        cur.execute("SELECT COUNT(*) FROM jis_b1181_materials")
        count_mats = cur.fetchone()[0]
        self.assertGreaterEqual(count_mats, 10, "CSDL SQLite phải chứa danh mục cơ tính vật liệu")

        conn.close()

    def test_query_performance_benchmark(self):
        """Đo lường hiệu năng truy vấn trong RAM phải đạt dưới 0.1 ms (100 µs)."""
        # Warmup
        get_nut_dimension("M16", "ISO_STYLE_1")
        
        # Test 10,000 lần truy vấn lặp
        iterations = 10000
        start_time = time.perf_counter()
        for _ in range(iterations):
            get_nut_dimension("M20", "ISO_STYLE_1")
            get_nut_dimension("M24", "ISO_STYLE_2")
            get_nut_dimension("M12", "ANNEX_JA_REGULAR")
        elapsed = time.perf_counter() - start_time
        
        avg_time_per_query_ms = (elapsed / (iterations * 3)) * 1000.0
        print(f"\n[Benchmark JIS B 1181] Thời gian trung bình 1 lần truy vấn: {avg_time_per_query_ms:.6f} ms")
        self.assertLess(avg_time_per_query_ms, 0.05, "Thời gian truy vấn RAM trung bình phải dưới 0.05 ms")


if __name__ == "__main__":
    unittest.main(verbosity=2)
