"""Bộ kiểm thử đơn vị tự động (Unit Tests) cho tiêu chuẩn gioăng mặt bích JIS B 2404 : 2018."""
import sys
import time
import unittest

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from _fvc_fasteners import (
    Gasket,
    get_sheet_gasket_dimension,
    get_spiral_wound_gasket_dimension,
    get_auto_gasket_for_flange,
)


class TestJisB2404(unittest.TestCase):
    """Kiểm thử tính toàn vẹn dữ liệu và bộ máy suy luận thông minh JIS B 2404."""

    def test_sheet_gasket_ring_lookup(self):
        """Kiểm tra tra cứu gioăng tấm dạng vành (Ring Gasket)."""
        # 10K DN100: d1=115, D3=159
        g_10k = get_sheet_gasket_dimension("10K", 100, shape="RING", facing="RF")
        self.assertIsNotNone(g_10k)
        self.assertEqual(g_10k.d1, 115.0)
        self.assertEqual(g_10k.d2, 159.0)

        # 20K DN200: d1=218, D3=280
        g_20k = get_sheet_gasket_dimension("20K", 200, shape="RING", facing="RF")
        self.assertIsNotNone(g_20k)
        self.assertEqual(g_20k.d1, 218.0)
        self.assertEqual(g_20k.d2, 280.0)

    def test_spiral_wound_lookup(self):
        """Kiểm tra tra cứu gioăng quấn xoắn SWG JIS B 2404."""
        # 20K DN100 SWG: d1=107, d2=116, d3=127, d4=165
        swg = get_spiral_wound_gasket_dimension("20K", 100, construction="INNER_OUTER_RING")
        self.assertIsNotNone(swg)
        self.assertEqual(swg.d1, 107.0)
        self.assertEqual(swg.d2, 116.0)
        self.assertEqual(swg.d3, 127.0)
        self.assertEqual(swg.d4, 165.0)
        self.assertEqual(swg.t_winding, 4.5)
        self.assertEqual(swg.t_ring, 3.0)

    def test_auto_inference_smart(self):
        """Kiểm tra bộ máy suy luận tự động thông minh theo áp suất và bề mặt bích."""
        # 1. Bích 10K gờ nâng RF -> Tự chọn Sheet Ring
        g1 = get_auto_gasket_for_flange(rating="10K", dn=100, facing="RF")
        self.assertEqual(g1.family, "SHEET")
        self.assertEqual(g1.shape_code, "RING")
        self.assertEqual(g1.d_inner, 115.0)
        self.assertEqual(g1.d_outer, 159.0)

        # 2. Bích 20K áp cao gờ nâng RF -> Tự chọn Spiral Wound SWIC
        g2 = get_auto_gasket_for_flange(rating="20K", dn=100, facing="RF")
        self.assertEqual(g2.family, "SPIRAL_WOUND")
        self.assertEqual(g2.shape_code, "SWIC")
        self.assertEqual(g2.thickness, 4.5)
        self.assertEqual(g2.d1_inner_ring, 107.0)
        self.assertEqual(g2.d4_outer_ring, 165.0)

        # 3. Bích mặt phẳng FF -> Tự chọn Full-Face
        g3 = get_auto_gasket_for_flange(rating="10K", dn=100, facing="FF")
        self.assertEqual(g3.family, "SHEET")
        self.assertEqual(g3.shape_code, "FULL_FACE")
        self.assertIsNotNone(g3.pcd)
        self.assertIsNotNone(g3.hole_count)

    def test_galvanic_dissimilar_metal_detection(self):
        """Kiểm tra CƠ CHẾ CÁCH 1: Tự động phát hiện lệch kim loại và kích hoạt Flange Insulation Kit."""
        # Trường hợp 1: Thép carbon nối với Inox SUS304
        g_diff = get_auto_gasket_for_flange(
            rating="10K",
            dn=100,
            facing="RF",
            flange1_material="CARBON_STEEL",
            flange2_material="SUS304"
        )
        self.assertTrue(g_diff.is_insulating)
        self.assertEqual(g_diff.family, "INSULATING_KIT")
        self.assertEqual(g_diff.gasket_material, "G10_EPOXY_GLASS")

        # Trường hợp 2: Cùng vật liệu Thép carbon
        g_same = get_auto_gasket_for_flange(
            rating="10K",
            dn=100,
            facing="RF",
            flange1_material="CARBON_STEEL",
            flange2_material="CARBON_STEEL"
        )
        self.assertFalse(g_same.is_insulating)
        self.assertEqual(g_same.family, "SHEET")

    def test_3d_geometry_creation(self):
        """Kiểm tra khởi tạo đối tượng 3D Solid Gasket."""
        class MockSubpart:
            pass

        s = MockSubpart()

        # Tạo gioăng tự động
        g_obj = Gasket(s, rating="10K", dn=100, facing="RF")
        self.assertIsNotNone(g_obj)
        self.assertEqual(g_obj.od, 159.0)
        self.assertEqual(g_obj.id, 115.0)

        # Tạo gioăng cách điện (Cách 1)
        g_ins = Gasket(
            s,
            rating="10K",
            dn=100,
            flange1_material="CARBON_STEEL",
            flange2_material="SUS316"
        )
        self.assertTrue(g_ins.is_insulating)

    def test_benchmark_query_time(self):
        """Đo benchmark thời gian tra cứu bộ nhớ (yêu cầu < 0.001 ms / query)."""
        n_queries = 10000
        start = time.perf_counter()
        for _ in range(n_queries):
            get_auto_gasket_for_flange(rating="10K", dn=100, facing="RF")
        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / n_queries) * 1000.0

        print(f"\n[Benchmark JIS B 2404] Thời gian trung bình 1 lần truy vấn: {avg_ms:.6f} ms")
        self.assertLess(avg_ms, 0.05)


if __name__ == "__main__":
    unittest.main()
