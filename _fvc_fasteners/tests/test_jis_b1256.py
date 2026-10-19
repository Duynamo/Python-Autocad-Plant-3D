"""Unit tests toàn diện cho module vòng đệm phẳng JIS B 1256 : 2008 trong gói _fvc_fasteners."""
import os
import sqlite3
import sys
import time
import unittest

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from _fvc_fasteners.models.jis_b1256_specs import WasherDimensionSpec, WasherTypeSpec, PlainWasherSpec
from _fvc_fasteners.db.jis_b1256_reader import (
    get_washer_type,
    list_available_washer_types,
    get_washer_dimension,
    list_available_washer_sizes,
    get_hardness_spec,
    get_plain_washer,
    get_matching_washer_for_bolt,
)
from _fvc_fasteners.data.jis_b1256_seed import DB_PATH
from _fvc_fasteners.geometry.washer import PlainWasher, SquareWasher


class TestJisB1256(unittest.TestCase):
    """Bộ kiểm thử tính toàn vẹn dữ liệu, kích thước hình học và hiệu năng của JIS B 1256."""

    def test_list_all_10_washer_types(self):
        """Kiểm tra có đầy đủ 10 chủng loại vòng đệm (7 ISO + 1 Phụ lục JA + 2 JIS B 1250 cũ)."""
        types = list_available_washer_types()
        self.assertEqual(len(types), 10, "Phải có chính xác 10 chủng loại vòng đệm theo JIS B 1256 & JIS B 1250")
        
        codes = [t.type_code for t in types]
        expected_codes = [
            "ISO_7089_NORMAL_GRADE_A",
            "ISO_7090_NORMAL_CHAMFERED_GRADE_A",
            "ISO_7091_NORMAL_GRADE_C",
            "ISO_7092_SMALL_GRADE_A",
            "ISO_7093_1_LARGE_GRADE_A",
            "ISO_7093_2_LARGE_GRADE_C",
            "ISO_7094_EXTRA_LARGE_GRADE_C",
            "ANNEX_JA_SQUARE",
            "JIS_POLISHED_ROUND",
            "JIS_COMMERCIAL_ROUND",
        ]
        for ec in expected_codes:
            self.assertIn(ec, codes, f"Mã loại {ec} phải tồn tại trong danh mục")

    def test_default_flange_washer_type(self):
        """Kiểm tra vòng đệm thường cấp A (ISO 7089) là mặc định cho mặt bích đường ống."""
        t1 = get_washer_type("ISO_7089_NORMAL_GRADE_A")
        self.assertIsNotNone(t1)
        self.assertTrue(t1.is_flange_default)
        self.assertEqual(t1.iso_standard, "ISO 7089")
        self.assertEqual(t1.washer_series, "NORMAL")
        self.assertEqual(t1.product_grade, "GRADE_A")
        self.assertEqual(t1.dimension_series, "ISO_NORMAL_A")

    def test_iso_normal_series_grade_a_dimensions(self):
        """Kiểm tra kích thước vòng đệm thường cấp A (ISO 7089) theo Bảng 7 tiêu chuẩn."""
        # Kiểm tra M16: d1=17.0, d2=30.0, h=3.0
        m16 = get_washer_dimension("M16", "ISO_NORMAL_A")
        self.assertIsNotNone(m16)
        self.assertEqual(m16.d1_nominal, 17.0, "M16 phải có d1 = 17.0 mm")
        self.assertEqual(m16.d1_min, 17.0)
        self.assertEqual(m16.d1_max, 17.27)
        self.assertEqual(m16.d2_nominal, 30.0, "M16 phải có d2 = 30.0 mm")
        self.assertEqual(m16.d2_max, 30.0)
        self.assertEqual(m16.d2_min, 29.48)
        self.assertEqual(m16.h_nominal, 3.0, "M16 phải có h = 3.0 mm")
        self.assertEqual(m16.h_min, 2.7)
        self.assertEqual(m16.h_max, 3.3)

        # Kiểm tra M20: d1=21.0, d2=37.0, h=3.0
        m20 = get_washer_dimension("M20", "ISO_NORMAL_A")
        self.assertIsNotNone(m20)
        self.assertEqual(m20.d1_nominal, 21.0)
        self.assertEqual(m20.d2_nominal, 37.0)
        self.assertEqual(m20.h_nominal, 3.0)

        # Kiểm tra M24: d1=25.0, d2=44.0, h=4.0
        m24 = get_washer_dimension("M24", "ISO_NORMAL_A")
        self.assertIsNotNone(m24)
        self.assertEqual(m24.d1_nominal, 25.0)
        self.assertEqual(m24.d2_nominal, 44.0)
        self.assertEqual(m24.h_nominal, 4.0)

        # Kiểm tra M30: d1=31.0, d2=56.0, h=4.0
        m30 = get_washer_dimension("M30", "ISO_NORMAL_A")
        self.assertIsNotNone(m30)
        self.assertEqual(m30.d1_nominal, 31.0)
        self.assertEqual(m30.d2_nominal, 56.0)
        self.assertEqual(m30.h_nominal, 4.0)

        # Kiểm tra M36: d1=37.0, d2=66.0, h=5.0
        m36 = get_washer_dimension("M36", "ISO_NORMAL_A")
        self.assertIsNotNone(m36)
        self.assertEqual(m36.d1_nominal, 37.0)
        self.assertEqual(m36.d2_nominal, 66.0)
        self.assertEqual(m36.h_nominal, 5.0)

        # Kiểm tra M42: d1=43.0, d2=78.0, h=7.0
        m42 = get_washer_dimension("M42", "ISO_NORMAL_A")
        self.assertIsNotNone(m42)
        self.assertEqual(m42.d1_nominal, 43.0)
        self.assertEqual(m42.d2_nominal, 78.0)
        self.assertEqual(m42.h_nominal, 7.0)

        # Kiểm tra M64: d1=66.0, d2=115.0, h=9.0
        m64 = get_washer_dimension("M64", "ISO_NORMAL_A")
        self.assertIsNotNone(m64)
        self.assertEqual(m64.d1_nominal, 66.0)
        self.assertEqual(m64.d2_nominal, 115.0)
        self.assertEqual(m64.h_nominal, 9.0)

    def test_iso_normal_chamfered_grade_a(self):
        """Kiểm tra vòng đệm thường vát mép ngoài (ISO 7090) góc 45 độ."""
        m16_ch = get_washer_dimension("M16", "ISO_NORMAL_CHAMFERED_A")
        self.assertIsNotNone(m16_ch)
        self.assertEqual(m16_ch.d1_nominal, 17.0)
        self.assertEqual(m16_ch.d2_nominal, 30.0)
        self.assertEqual(m16_ch.h_nominal, 3.0)
        self.assertEqual(m16_ch.chamfer_angle_deg, 45.0)
        self.assertEqual(m16_ch.chamfer_c, 1.5, "M16 vát mép c = 1.5 mm")

        m20_ch = get_washer_dimension("M20", "ISO_NORMAL_CHAMFERED_A")
        self.assertEqual(m20_ch.chamfer_c, 1.5)

    def test_iso_small_series_dimensions(self):
        """Kiểm tra vòng đệm vành nhỏ (ISO 7092) d2 nhỏ hơn vòng đệm thường."""
        m16_small = get_washer_dimension("M16", "ISO_SMALL_A")
        m16_normal = get_washer_dimension("M16", "ISO_NORMAL_A")
        self.assertIsNotNone(m16_small)
        self.assertEqual(m16_small.d1_nominal, 17.0)
        self.assertEqual(m16_small.d2_nominal, 28.0, "M16 Small có d2 = 28 mm")
        self.assertEqual(m16_small.h_nominal, 2.5)
        self.assertLess(m16_small.d2_nominal, m16_normal.d2_nominal, "Vành nhỏ phải có d2 nhỏ hơn vành thường")

    def test_iso_large_series_dimensions(self):
        """Kiểm tra vòng đệm vành lớn (ISO 7093-1) d2 gấp ~ 3d."""
        m16_large = get_washer_dimension("M16", "ISO_LARGE_A")
        m16_normal = get_washer_dimension("M16", "ISO_NORMAL_A")
        self.assertIsNotNone(m16_large)
        self.assertEqual(m16_large.d1_nominal, 17.0)
        self.assertEqual(m16_large.d2_nominal, 50.0, "M16 Large có d2 = 50 mm")
        self.assertEqual(m16_large.h_nominal, 3.0)
        self.assertGreater(m16_large.d2_nominal, m16_normal.d2_nominal, "Vành lớn phải có d2 lớn hơn vành thường")

    def test_iso_extra_large_series_dimensions(self):
        """Kiểm tra vòng đệm vành cực lớn dày (ISO 7094) dùng cho kết cấu gỗ."""
        m16_xl = get_washer_dimension("M16", "ISO_EXTRA_LARGE_C")
        self.assertIsNotNone(m16_xl)
        self.assertEqual(m16_xl.d1_nominal, 17.5)
        self.assertEqual(m16_xl.d2_nominal, 56.0, "M16 Extra Large có d2 = 56 mm")
        self.assertEqual(m16_xl.h_nominal, 5.0, "M16 Extra Large phải dày 5.0 mm")

    def test_annex_ja_square_washers(self):
        """Kiểm tra kích thước đệm vuông phụ lục JA (角座金)."""
        sq_m16 = get_washer_dimension("M16", "ANNEX_JA_SQUARE")
        self.assertIsNotNone(sq_m16)
        self.assertEqual(sq_m16.d1_nominal, 17.5)
        self.assertEqual(sq_m16.d2_nominal, 52.0, "Cạnh đệm vuông M16 a = 52 mm")
        self.assertEqual(sq_m16.h_nominal, 4.5, "Độ dày đệm vuông M16 t = 4.5 mm")

        sq_m20 = get_washer_dimension("M20", "ANNEX_JA_SQUARE")
        self.assertEqual(sq_m20.d2_nominal, 68.0, "Cạnh đệm vuông M20 a = 68 mm")
        self.assertEqual(sq_m20.h_nominal, 6.0)

    def test_traditional_japanese_washers(self):
        """Kiểm tra vòng đệm truyền thống Nhật Bản JIS B 1250 (ミガキ丸 và 並丸)."""
        migaki_m16 = get_washer_dimension("M16", "JIS_POLISHED_ROUND")
        self.assertIsNotNone(migaki_m16)
        self.assertEqual(migaki_m16.d1_nominal, 17.0)
        self.assertEqual(migaki_m16.d2_nominal, 28.0, "M16 ミガキ丸 d2 = 28 mm")
        self.assertEqual(migaki_m16.h_nominal, 2.6)

        nami_m16 = get_washer_dimension("M16", "JIS_COMMERCIAL_ROUND")
        self.assertIsNotNone(nami_m16)
        self.assertEqual(nami_m16.d1_nominal, 17.0)
        self.assertEqual(nami_m16.d2_nominal, 32.0, "M16 並丸 d2 = 32 mm")
        self.assertEqual(nami_m16.h_nominal, 3.2)

    def test_hardness_classes(self):
        """Kiểm tra các cấp độ cứng 100 HV, 200 HV, 300 HV."""
        h100 = get_hardness_spec("100_HV")
        self.assertIsNotNone(h100)
        self.assertEqual(h100["min_hv"], 100.0)

        h200 = get_hardness_spec("200_HV")
        self.assertIsNotNone(h200)
        self.assertEqual(h200["min_hv"], 200.0)
        self.assertIn("mặt bích", h200["description_vi"])

        h300 = get_hardness_spec("300_HV")
        self.assertIsNotNone(h300)
        self.assertEqual(h300["min_hv"], 300.0)

    def test_get_plain_washer_bom_spec(self):
        """Kiểm tra khởi tạo đối tượng PlainWasherSpec hoàn chỉnh phục vụ BOM."""
        washer_obj = get_plain_washer("M16", "ISO_NORMAL_A", "200_HV", "CARBON_STEEL")
        self.assertIsNotNone(washer_obj)
        self.assertEqual(washer_obj.bolt_size, "M16")
        self.assertEqual(washer_obj.hardness_class, "200_HV")
        self.assertEqual(washer_obj.material, "CARBON_STEEL")
        self.assertIn("JIS B 1256", washer_obj.full_designation)
        self.assertIn("M16", washer_obj.full_designation)

    def test_matching_washer_for_bolt(self):
        """Kiểm tra tự động tìm vòng đệm tương thích và khả năng fallback."""
        w_m16 = get_matching_washer_for_bolt("M16")
        self.assertEqual(w_m16.d2_nominal, 30.0)
        self.assertEqual(w_m16.h_nominal, 3.0)

        # Cỡ đặc biệt tự động tính toán
        w_special = get_matching_washer_for_bolt("M72")
        self.assertIsNotNone(w_special)
        self.assertEqual(w_special.bolt_size, "M72")
        self.assertGreater(w_special.d2_nominal, 72.0)

    def test_geometry_3d_washer_creation(self):
        """Kiểm tra khởi tạo mô hình 3D Solid PlainWasher và SquareWasher không phát sinh lỗi."""
        washer_3d = PlainWasher(None, bolt_size="M16", series="ISO_NORMAL_A", has_hole=True)
        self.assertIsNotNone(washer_3d)
        self.assertEqual(washer_3d.spec.d2_nominal, 30.0)
        self.assertEqual(washer_3d.spec.h_nominal, 3.0)

        sq_3d = SquareWasher(None, bolt_size="M16", has_hole=True)
        self.assertIsNotNone(sq_3d)
        self.assertEqual(sq_3d.spec.d2_nominal, 52.0)
        self.assertEqual(sq_3d.spec.h_nominal, 4.5)

    def test_sqlite_database_integrity(self):
        """Kiểm tra tính toàn vẹn của tệp SQLite jis_b1256.sqlite trên đĩa."""
        self.assertTrue(os.path.exists(DB_PATH), f"File SQLite phải tồn tại tại: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM jis_b1256_washer_types")
        self.assertEqual(cur.fetchone()[0], 10, "CSDL SQLite phải chứa 10 chủng loại vòng đệm")

        cur.execute("SELECT COUNT(*) FROM jis_b1256_washer_dimensions")
        self.assertEqual(cur.fetchone()[0], 177, "CSDL SQLite phải chứa 177 bản ghi kích thước")

        cur.execute("SELECT COUNT(*) FROM jis_b1256_hardness_specs")
        self.assertEqual(cur.fetchone()[0], 3, "CSDL SQLite phải chứa 3 bản ghi cấp độ cứng")

        conn.close()

    def test_query_performance_benchmark(self):
        """Đo lường hiệu năng truy vấn trong RAM phải đạt dưới 0.05 ms (50 µs)."""
        # Warmup
        get_washer_dimension("M16", "ISO_NORMAL_A")

        iterations = 10000
        start_time = time.perf_counter()
        for _ in range(iterations):
            get_washer_dimension("M16", "ISO_NORMAL_A")
            get_washer_dimension("M20", "ISO_NORMAL_CHAMFERED_A")
            get_washer_dimension("M16", "ANNEX_JA_SQUARE")
        elapsed = time.perf_counter() - start_time

        avg_time_per_query_ms = (elapsed / (iterations * 3)) * 1000.0
        print(f"\n[Benchmark JIS B 1256] Thời gian trung bình 1 lần truy vấn: {avg_time_per_query_ms:.6f} ms")
        self.assertLess(avg_time_per_query_ms, 0.05, "Thời gian truy vấn RAM trung bình phải dưới 0.05 ms")


if __name__ == "__main__":
    unittest.main(verbosity=2)
