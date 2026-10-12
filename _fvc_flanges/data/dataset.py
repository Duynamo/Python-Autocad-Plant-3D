from ..models.dimensions import FlangeDimensions

# Bộ dữ liệu JIS B 2220 tích hợp sẵn trong bộ nhớ (không phụ thuộc sqlite3 DLL)
FLANGE_DATASET = {
    ('10K', 'BL', 10): FlangeDimensions(
        rating='10K', flange_type='BL', dn=10,
        d=90.0, c=65.0, h=15.0, no=4, bolt_name='M12',
        g=46.0, f=1.0, t=12.0, total_len=12.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=17.3, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 15): FlangeDimensions(
        rating='10K', flange_type='BL', dn=15,
        d=95.0, c=70.0, h=15.0, no=4, bolt_name='M12',
        g=51.0, f=1.0, t=12.0, total_len=12.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=21.7, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 20): FlangeDimensions(
        rating='10K', flange_type='BL', dn=20,
        d=100.0, c=75.0, h=15.0, no=4, bolt_name='M12',
        g=56.0, f=1.0, t=14.0, total_len=14.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=27.2, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 25): FlangeDimensions(
        rating='10K', flange_type='BL', dn=25,
        d=125.0, c=90.0, h=19.0, no=4, bolt_name='M16',
        g=67.0, f=2.0, t=14.0, total_len=14.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=34.0, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 32): FlangeDimensions(
        rating='10K', flange_type='BL', dn=32,
        d=135.0, c=100.0, h=19.0, no=4, bolt_name='M16',
        g=76.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=42.7, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 40): FlangeDimensions(
        rating='10K', flange_type='BL', dn=40,
        d=140.0, c=105.0, h=19.0, no=4, bolt_name='M16',
        g=81.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=48.6, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 50): FlangeDimensions(
        rating='10K', flange_type='BL', dn=50,
        d=155.0, c=120.0, h=19.0, no=4, bolt_name='M16',
        g=96.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=60.5, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 65): FlangeDimensions(
        rating='10K', flange_type='BL', dn=65,
        d=175.0, c=140.0, h=19.0, no=4, bolt_name='M16',
        g=116.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=76.3, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 80): FlangeDimensions(
        rating='10K', flange_type='BL', dn=80,
        d=185.0, c=150.0, h=19.0, no=8, bolt_name='M16',
        g=126.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=89.1, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 90): FlangeDimensions(
        rating='10K', flange_type='BL', dn=90,
        d=195.0, c=160.0, h=19.0, no=8, bolt_name='M16',
        g=136.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=101.6, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 100): FlangeDimensions(
        rating='10K', flange_type='BL', dn=100,
        d=210.0, c=175.0, h=19.0, no=8, bolt_name='M16',
        g=151.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=114.3, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 125): FlangeDimensions(
        rating='10K', flange_type='BL', dn=125,
        d=250.0, c=210.0, h=23.0, no=8, bolt_name='M20',
        g=182.0, f=2.0, t=20.0, total_len=20.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=139.8, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 150): FlangeDimensions(
        rating='10K', flange_type='BL', dn=150,
        d=280.0, c=240.0, h=23.0, no=8, bolt_name='M20',
        g=212.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=165.2, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 175): FlangeDimensions(
        rating='10K', flange_type='BL', dn=175,
        d=305.0, c=265.0, h=23.0, no=12, bolt_name='M20',
        g=237.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=190.7, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 200): FlangeDimensions(
        rating='10K', flange_type='BL', dn=200,
        d=330.0, c=290.0, h=23.0, no=12, bolt_name='M20',
        g=262.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=216.3, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 225): FlangeDimensions(
        rating='10K', flange_type='BL', dn=225,
        d=350.0, c=310.0, h=23.0, no=12, bolt_name='M20',
        g=282.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=241.8, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 250): FlangeDimensions(
        rating='10K', flange_type='BL', dn=250,
        d=400.0, c=355.0, h=25.0, no=12, bolt_name='M22',
        g=324.0, f=2.0, t=24.0, total_len=24.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=267.4, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 300): FlangeDimensions(
        rating='10K', flange_type='BL', dn=300,
        d=445.0, c=400.0, h=25.0, no=16, bolt_name='M22',
        g=368.0, f=3.0, t=24.0, total_len=24.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=318.5, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 350): FlangeDimensions(
        rating='10K', flange_type='BL', dn=350,
        d=490.0, c=445.0, h=25.0, no=16, bolt_name='M22',
        g=413.0, f=3.0, t=26.0, total_len=26.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=355.6, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 400): FlangeDimensions(
        rating='10K', flange_type='BL', dn=400,
        d=560.0, c=510.0, h=27.0, no=16, bolt_name='M24',
        g=475.0, f=3.0, t=28.0, total_len=28.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=406.4, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 450): FlangeDimensions(
        rating='10K', flange_type='BL', dn=450,
        d=620.0, c=565.0, h=27.0, no=20, bolt_name='M24',
        g=530.0, f=3.0, t=30.0, total_len=30.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=457.2, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 500): FlangeDimensions(
        rating='10K', flange_type='BL', dn=500,
        d=675.0, c=620.0, h=27.0, no=20, bolt_name='M24',
        g=585.0, f=3.0, t=30.0, total_len=30.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=508.0, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 550): FlangeDimensions(
        rating='10K', flange_type='BL', dn=550,
        d=745.0, c=680.0, h=33.0, no=20, bolt_name='M30',
        g=640.0, f=3.0, t=34.0, total_len=34.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=558.8, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 600): FlangeDimensions(
        rating='10K', flange_type='BL', dn=600,
        d=795.0, c=730.0, h=33.0, no=24, bolt_name='M30',
        g=690.0, f=3.0, t=36.0, total_len=36.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=609.6, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 650): FlangeDimensions(
        rating='10K', flange_type='BL', dn=650,
        d=845.0, c=780.0, h=33.0, no=24, bolt_name='M30',
        g=740.0, f=3.0, t=38.0, total_len=38.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=660.4, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 700): FlangeDimensions(
        rating='10K', flange_type='BL', dn=700,
        d=905.0, c=840.0, h=33.0, no=24, bolt_name='M30',
        g=800.0, f=3.0, t=40.0, total_len=40.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=711.2, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 750): FlangeDimensions(
        rating='10K', flange_type='BL', dn=750,
        d=970.0, c=900.0, h=33.0, no=24, bolt_name='M30',
        g=855.0, f=3.0, t=44.0, total_len=44.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=762.0, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 800): FlangeDimensions(
        rating='10K', flange_type='BL', dn=800,
        d=1020.0, c=950.0, h=33.0, no=28, bolt_name='M30',
        g=905.0, f=3.0, t=46.0, total_len=46.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=812.8, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 850): FlangeDimensions(
        rating='10K', flange_type='BL', dn=850,
        d=1070.0, c=1000.0, h=33.0, no=28, bolt_name='M30',
        g=955.0, f=3.0, t=48.0, total_len=48.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=863.6, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 900): FlangeDimensions(
        rating='10K', flange_type='BL', dn=900,
        d=1120.0, c=1050.0, h=33.0, no=28, bolt_name='M30',
        g=1005.0, f=3.0, t=50.0, total_len=50.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=914.4, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 1000): FlangeDimensions(
        rating='10K', flange_type='BL', dn=1000,
        d=1235.0, c=1160.0, h=39.0, no=28, bolt_name='M36',
        g=1110.0, f=3.0, t=56.0, total_len=56.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=1016.0, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 1100): FlangeDimensions(
        rating='10K', flange_type='BL', dn=1100,
        d=1345.0, c=1270.0, h=39.0, no=28, bolt_name='M36',
        g=1220.0, f=3.0, t=62.0, total_len=62.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=1117.6, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 1200): FlangeDimensions(
        rating='10K', flange_type='BL', dn=1200,
        d=1465.0, c=1380.0, h=39.0, no=32, bolt_name='M36',
        g=1325.0, f=3.0, t=66.0, total_len=66.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=1219.2, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 1350): FlangeDimensions(
        rating='10K', flange_type='BL', dn=1350,
        d=1630.0, c=1540.0, h=45.0, no=36, bolt_name='M42',
        g=1480.0, f=3.0, t=74.0, total_len=74.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=1371.6, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'BL', 1500): FlangeDimensions(
        rating='10K', flange_type='BL', dn=1500,
        d=1795.0, c=1700.0, h=45.0, no=40, bolt_name='M42',
        g=1635.0, f=3.0, t=82.0, total_len=82.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=1524.0, d_bore=0.0, inner_dia=0.0
    ),
    ('10K', 'IT', 10): FlangeDimensions(
        rating='10K', flange_type='IT', dn=10,
        d=90.0, c=65.0, h=15.0, no=4, bolt_name='M12',
        g=46.0, f=1.0, t=12.0, total_len=29.0,
        hub_small=17.3, hub_large=28.0,
        d0=17.8, pipe_od=17.3, d_bore=12.7, inner_dia=17.8
    ),
    ('10K', 'IT', 15): FlangeDimensions(
        rating='10K', flange_type='IT', dn=15,
        d=95.0, c=70.0, h=15.0, no=4, bolt_name='M12',
        g=51.0, f=1.0, t=12.0, total_len=31.0,
        hub_small=21.7, hub_large=33.0,
        d0=22.2, pipe_od=21.7, d_bore=16.1, inner_dia=22.2
    ),
    ('10K', 'IT', 20): FlangeDimensions(
        rating='10K', flange_type='IT', dn=20,
        d=100.0, c=75.0, h=15.0, no=4, bolt_name='M12',
        g=56.0, f=1.0, t=14.0, total_len=32.0,
        hub_small=27.2, hub_large=38.0,
        d0=27.7, pipe_od=27.2, d_bore=21.6, inner_dia=27.7
    ),
    ('10K', 'IT', 25): FlangeDimensions(
        rating='10K', flange_type='IT', dn=25,
        d=125.0, c=90.0, h=19.0, no=4, bolt_name='M16',
        g=67.0, f=2.0, t=14.0, total_len=36.0,
        hub_small=34.0, hub_large=47.0,
        d0=34.5, pipe_od=34.0, d_bore=27.6, inner_dia=34.5
    ),
    ('10K', 'IT', 32): FlangeDimensions(
        rating='10K', flange_type='IT', dn=32,
        d=135.0, c=100.0, h=19.0, no=4, bolt_name='M16',
        g=76.0, f=2.0, t=16.0, total_len=38.0,
        hub_small=42.7, hub_large=56.0,
        d0=43.2, pipe_od=42.7, d_bore=35.7, inner_dia=43.2
    ),
    ('10K', 'IT', 40): FlangeDimensions(
        rating='10K', flange_type='IT', dn=40,
        d=140.0, c=105.0, h=19.0, no=4, bolt_name='M16',
        g=81.0, f=2.0, t=16.0, total_len=38.0,
        hub_small=48.6, hub_large=62.0,
        d0=49.1, pipe_od=48.6, d_bore=41.6, inner_dia=49.1
    ),
    ('10K', 'IT', 50): FlangeDimensions(
        rating='10K', flange_type='IT', dn=50,
        d=155.0, c=120.0, h=19.0, no=4, bolt_name='M16',
        g=96.0, f=2.0, t=16.0, total_len=40.0,
        hub_small=60.5, hub_large=75.0,
        d0=61.1, pipe_od=60.5, d_bore=52.9, inner_dia=61.1
    ),
    ('10K', 'IT', 65): FlangeDimensions(
        rating='10K', flange_type='IT', dn=65,
        d=175.0, c=140.0, h=19.0, no=4, bolt_name='M16',
        g=116.0, f=2.0, t=18.0, total_len=44.0,
        hub_small=76.3, hub_large=92.0,
        d0=77.1, pipe_od=76.3, d_bore=67.9, inner_dia=77.1
    ),
    ('10K', 'IT', 80): FlangeDimensions(
        rating='10K', flange_type='IT', dn=80,
        d=185.0, c=150.0, h=19.0, no=8, bolt_name='M16',
        g=126.0, f=2.0, t=18.0, total_len=45.0,
        hub_small=89.1, hub_large=105.0,
        d0=90.0, pipe_od=89.1, d_bore=80.7, inner_dia=90.0
    ),
    ('10K', 'IT', 90): FlangeDimensions(
        rating='10K', flange_type='IT', dn=90,
        d=195.0, c=160.0, h=19.0, no=8, bolt_name='M16',
        g=136.0, f=2.0, t=18.0, total_len=45.0,
        hub_small=101.6, hub_large=117.0,
        d0=102.6, pipe_od=101.6, d_bore=93.2, inner_dia=102.6
    ),
    ('10K', 'IT', 100): FlangeDimensions(
        rating='10K', flange_type='IT', dn=100,
        d=210.0, c=175.0, h=19.0, no=8, bolt_name='M16',
        g=151.0, f=2.0, t=18.0, total_len=45.0,
        hub_small=114.3, hub_large=130.0,
        d0=115.4, pipe_od=114.3, d_bore=105.3, inner_dia=115.4
    ),
    ('10K', 'IT', 125): FlangeDimensions(
        rating='10K', flange_type='IT', dn=125,
        d=250.0, c=210.0, h=23.0, no=8, bolt_name='M20',
        g=182.0, f=2.0, t=20.0, total_len=47.0,
        hub_small=139.8, hub_large=156.0,
        d0=141.2, pipe_od=139.8, d_bore=130.8, inner_dia=141.2
    ),
    ('10K', 'IT', 150): FlangeDimensions(
        rating='10K', flange_type='IT', dn=150,
        d=280.0, c=240.0, h=23.0, no=8, bolt_name='M20',
        g=212.0, f=2.0, t=22.0, total_len=53.0,
        hub_small=165.2, hub_large=184.0,
        d0=166.6, pipe_od=165.2, d_bore=155.2, inner_dia=166.6
    ),
    ('10K', 'IT', 175): FlangeDimensions(
        rating='10K', flange_type='IT', dn=175,
        d=305.0, c=265.0, h=23.0, no=12, bolt_name='M20',
        g=237.0, f=2.0, t=22.0, total_len=55.0,
        hub_small=190.7, hub_large=210.0,
        d0=192.1, pipe_od=190.7, d_bore=180.1, inner_dia=192.1
    ),
    ('10K', 'IT', 200): FlangeDimensions(
        rating='10K', flange_type='IT', dn=200,
        d=330.0, c=290.0, h=23.0, no=12, bolt_name='M20',
        g=262.0, f=2.0, t=22.0, total_len=58.0,
        hub_small=216.3, hub_large=238.0,
        d0=218.0, pipe_od=216.3, d_bore=204.7, inner_dia=218.0
    ),
    ('10K', 'IT', 225): FlangeDimensions(
        rating='10K', flange_type='IT', dn=225,
        d=350.0, c=310.0, h=23.0, no=12, bolt_name='M20',
        g=282.0, f=2.0, t=22.0, total_len=58.0,
        hub_small=241.8, hub_large=261.0,
        d0=243.7, pipe_od=241.8, d_bore=229.4, inner_dia=243.7
    ),
    ('10K', 'IT', 250): FlangeDimensions(
        rating='10K', flange_type='IT', dn=250,
        d=400.0, c=355.0, h=25.0, no=12, bolt_name='M22',
        g=324.0, f=2.0, t=24.0, total_len=65.0,
        hub_small=267.4, hub_large=292.0,
        d0=269.5, pipe_od=267.4, d_bore=254.2, inner_dia=269.5
    ),
    ('10K', 'IT', 300): FlangeDimensions(
        rating='10K', flange_type='IT', dn=300,
        d=445.0, c=400.0, h=25.0, no=16, bolt_name='M22',
        g=368.0, f=3.0, t=24.0, total_len=68.0,
        hub_small=318.5, hub_large=345.0,
        d0=321.0, pipe_od=318.5, d_bore=304.7, inner_dia=321.0
    ),
    ('10K', 'IT', 350): FlangeDimensions(
        rating='10K', flange_type='IT', dn=350,
        d=490.0, c=445.0, h=25.0, no=16, bolt_name='M22',
        g=413.0, f=3.0, t=26.0, total_len=79.0,
        hub_small=355.6, hub_large=388.0,
        d0=358.1, pipe_od=355.6, d_bore=339.8, inner_dia=358.1
    ),
    ('10K', 'IT', 400): FlangeDimensions(
        rating='10K', flange_type='IT', dn=400,
        d=560.0, c=510.0, h=27.0, no=16, bolt_name='M24',
        g=475.0, f=3.0, t=28.0, total_len=85.0,
        hub_small=406.4, hub_large=442.0,
        d0=409.0, pipe_od=406.4, d_bore=390.6, inner_dia=409.0
    ),
    ('10K', 'IT', 450): FlangeDimensions(
        rating='10K', flange_type='IT', dn=450,
        d=620.0, c=565.0, h=27.0, no=20, bolt_name='M24',
        g=530.0, f=3.0, t=30.0, total_len=90.0,
        hub_small=457.2, hub_large=495.0,
        d0=460.0, pipe_od=457.2, d_bore=441.4, inner_dia=460.0
    ),
    ('10K', 'IT', 500): FlangeDimensions(
        rating='10K', flange_type='IT', dn=500,
        d=675.0, c=620.0, h=27.0, no=20, bolt_name='M24',
        g=585.0, f=3.0, t=30.0, total_len=90.0,
        hub_small=508.0, hub_large=546.0,
        d0=511.0, pipe_od=508.0, d_bore=492.2, inner_dia=511.0
    ),
    ('10K', 'IT', 550): FlangeDimensions(
        rating='10K', flange_type='IT', dn=550,
        d=745.0, c=680.0, h=33.0, no=20, bolt_name='M30',
        g=640.0, f=3.0, t=32.0, total_len=111.0,
        hub_small=558.8, hub_large=597.0,
        d0=562.0, pipe_od=558.8, d_bore=543.0, inner_dia=562.0
    ),
    ('10K', 'IT', 600): FlangeDimensions(
        rating='10K', flange_type='IT', dn=600,
        d=795.0, c=730.0, h=33.0, no=24, bolt_name='M30',
        g=690.0, f=3.0, t=32.0, total_len=112.0,
        hub_small=609.6, hub_large=648.0,
        d0=613.0, pipe_od=609.6, d_bore=593.8, inner_dia=613.0
    ),
    ('10K', 'IT', 650): FlangeDimensions(
        rating='10K', flange_type='IT', dn=650,
        d=845.0, c=780.0, h=33.0, no=24, bolt_name='M30',
        g=740.0, f=3.0, t=34.0, total_len=116.0,
        hub_small=660.4, hub_large=700.0,
        d0=664.0, pipe_od=660.4, d_bore=644.6, inner_dia=664.0
    ),
    ('10K', 'IT', 700): FlangeDimensions(
        rating='10K', flange_type='IT', dn=700,
        d=905.0, c=840.0, h=33.0, no=24, bolt_name='M30',
        g=800.0, f=3.0, t=34.0, total_len=132.0,
        hub_small=711.2, hub_large=754.0,
        d0=715.0, pipe_od=711.2, d_bore=695.4, inner_dia=715.0
    ),
    ('10K', 'IT', 750): FlangeDimensions(
        rating='10K', flange_type='IT', dn=750,
        d=970.0, c=900.0, h=33.0, no=24, bolt_name='M30',
        g=855.0, f=3.0, t=36.0, total_len=139.0,
        hub_small=762.0, hub_large=807.0,
        d0=766.0, pipe_od=762.0, d_bore=746.2, inner_dia=766.0
    ),
    ('10K', 'IT', 800): FlangeDimensions(
        rating='10K', flange_type='IT', dn=800,
        d=1020.0, c=950.0, h=33.0, no=28, bolt_name='M30',
        g=905.0, f=3.0, t=36.0, total_len=139.0,
        hub_small=812.8, hub_large=858.0,
        d0=817.0, pipe_od=812.8, d_bore=797.0, inner_dia=817.0
    ),
    ('10K', 'IT', 850): FlangeDimensions(
        rating='10K', flange_type='IT', dn=850,
        d=1070.0, c=1000.0, h=33.0, no=28, bolt_name='M30',
        g=955.0, f=3.0, t=36.0, total_len=139.0,
        hub_small=863.6, hub_large=908.0,
        d0=868.0, pipe_od=863.6, d_bore=847.8, inner_dia=868.0
    ),
    ('10K', 'IT', 900): FlangeDimensions(
        rating='10K', flange_type='IT', dn=900,
        d=1120.0, c=1050.0, h=33.0, no=28, bolt_name='M30',
        g=1005.0, f=3.0, t=38.0, total_len=140.0,
        hub_small=914.4, hub_large=959.0,
        d0=919.0, pipe_od=914.4, d_bore=898.6, inner_dia=919.0
    ),
    ('10K', 'IT', 1000): FlangeDimensions(
        rating='10K', flange_type='IT', dn=1000,
        d=1235.0, c=1160.0, h=39.0, no=28, bolt_name='M36',
        g=1110.0, f=3.0, t=40.0, total_len=151.0,
        hub_small=1016.0, hub_large=1065.0,
        d0=1021.0, pipe_od=1016.0, d_bore=1000.2, inner_dia=1021.0
    ),
    ('10K', 'IT', 1100): FlangeDimensions(
        rating='10K', flange_type='IT', dn=1100,
        d=1345.0, c=1270.0, h=39.0, no=28, bolt_name='M36',
        g=1220.0, f=3.0, t=42.0, total_len=170.0,
        hub_small=1117.6, hub_large=1174.0,
        d0=1122.0, pipe_od=1117.6, d_bore=1098.6, inner_dia=1122.0
    ),
    ('10K', 'IT', 1200): FlangeDimensions(
        rating='10K', flange_type='IT', dn=1200,
        d=1465.0, c=1380.0, h=39.0, no=32, bolt_name='M36',
        g=1325.0, f=3.0, t=44.0, total_len=182.0,
        hub_small=1219.2, hub_large=1281.0,
        d0=1224.0, pipe_od=1219.2, d_bore=1200.2, inner_dia=1224.0
    ),
    ('10K', 'IT', 1350): FlangeDimensions(
        rating='10K', flange_type='IT', dn=1350,
        d=1630.0, c=1540.0, h=45.0, no=36, bolt_name='M42',
        g=1480.0, f=3.0, t=48.0, total_len=200.0,
        hub_small=1371.6, hub_large=1438.0,
        d0=1376.0, pipe_od=1371.6, d_bore=1346.2, inner_dia=1376.0
    ),
    ('10K', 'IT', 1500): FlangeDimensions(
        rating='10K', flange_type='IT', dn=1500,
        d=1795.0, c=1700.0, h=45.0, no=40, bolt_name='M42',
        g=1635.0, f=3.0, t=50.0, total_len=218.0,
        hub_small=1524.0, hub_large=1598.0,
        d0=1529.0, pipe_od=1524.0, d_bore=1498.6, inner_dia=1529.0
    ),
    ('10K', 'SOP', 10): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=10,
        d=90.0, c=65.0, h=15.0, no=4, bolt_name='M12',
        g=46.0, f=1.0, t=12.0, total_len=12.0,
        hub_small=0.0, hub_large=0.0,
        d0=17.8, pipe_od=17.3, d_bore=12.7, inner_dia=17.8
    ),
    ('10K', 'SOP', 15): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=15,
        d=95.0, c=70.0, h=15.0, no=4, bolt_name='M12',
        g=51.0, f=1.0, t=12.0, total_len=12.0,
        hub_small=0.0, hub_large=0.0,
        d0=22.2, pipe_od=21.7, d_bore=16.1, inner_dia=22.2
    ),
    ('10K', 'SOP', 20): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=20,
        d=100.0, c=75.0, h=15.0, no=4, bolt_name='M12',
        g=56.0, f=1.0, t=14.0, total_len=14.0,
        hub_small=0.0, hub_large=0.0,
        d0=27.7, pipe_od=27.2, d_bore=21.6, inner_dia=27.7
    ),
    ('10K', 'SOP', 25): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=25,
        d=125.0, c=90.0, h=19.0, no=4, bolt_name='M16',
        g=67.0, f=2.0, t=14.0, total_len=14.0,
        hub_small=0.0, hub_large=0.0,
        d0=34.5, pipe_od=34.0, d_bore=27.6, inner_dia=34.5
    ),
    ('10K', 'SOP', 32): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=32,
        d=135.0, c=100.0, h=19.0, no=4, bolt_name='M16',
        g=76.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=43.2, pipe_od=42.7, d_bore=35.7, inner_dia=43.2
    ),
    ('10K', 'SOP', 40): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=40,
        d=140.0, c=105.0, h=19.0, no=4, bolt_name='M16',
        g=81.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=49.1, pipe_od=48.6, d_bore=41.6, inner_dia=49.1
    ),
    ('10K', 'SOP', 50): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=50,
        d=155.0, c=120.0, h=19.0, no=4, bolt_name='M16',
        g=96.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=61.1, pipe_od=60.5, d_bore=52.9, inner_dia=61.1
    ),
    ('10K', 'SOP', 65): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=65,
        d=175.0, c=140.0, h=19.0, no=4, bolt_name='M16',
        g=116.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=77.1, pipe_od=76.3, d_bore=67.9, inner_dia=77.1
    ),
    ('10K', 'SOP', 80): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=80,
        d=185.0, c=150.0, h=19.0, no=8, bolt_name='M16',
        g=126.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=90.0, pipe_od=89.1, d_bore=80.7, inner_dia=90.0
    ),
    ('10K', 'SOP', 90): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=90,
        d=195.0, c=160.0, h=19.0, no=8, bolt_name='M16',
        g=136.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=102.6, pipe_od=101.6, d_bore=93.2, inner_dia=102.6
    ),
    ('10K', 'SOP', 100): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=100,
        d=210.0, c=175.0, h=19.0, no=8, bolt_name='M16',
        g=151.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=115.4, pipe_od=114.3, d_bore=105.3, inner_dia=115.4
    ),
    ('10K', 'SOP', 125): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=125,
        d=250.0, c=210.0, h=23.0, no=8, bolt_name='M20',
        g=182.0, f=2.0, t=20.0, total_len=20.0,
        hub_small=0.0, hub_large=0.0,
        d0=141.2, pipe_od=139.8, d_bore=130.8, inner_dia=141.2
    ),
    ('10K', 'SOP', 150): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=150,
        d=280.0, c=240.0, h=23.0, no=8, bolt_name='M20',
        g=212.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=166.6, pipe_od=165.2, d_bore=155.2, inner_dia=166.6
    ),
    ('10K', 'SOP', 175): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=175,
        d=305.0, c=265.0, h=23.0, no=12, bolt_name='M20',
        g=237.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=192.1, pipe_od=190.7, d_bore=180.1, inner_dia=192.1
    ),
    ('10K', 'SOP', 200): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=200,
        d=330.0, c=290.0, h=23.0, no=12, bolt_name='M20',
        g=262.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=218.0, pipe_od=216.3, d_bore=204.7, inner_dia=218.0
    ),
    ('10K', 'SOP', 225): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=225,
        d=350.0, c=310.0, h=23.0, no=12, bolt_name='M20',
        g=282.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=243.7, pipe_od=241.8, d_bore=229.4, inner_dia=243.7
    ),
    ('10K', 'SOP', 250): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=250,
        d=400.0, c=355.0, h=25.0, no=12, bolt_name='M22',
        g=324.0, f=2.0, t=24.0, total_len=24.0,
        hub_small=0.0, hub_large=0.0,
        d0=269.5, pipe_od=267.4, d_bore=254.2, inner_dia=269.5
    ),
    ('10K', 'SOP', 300): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=300,
        d=445.0, c=400.0, h=25.0, no=16, bolt_name='M22',
        g=368.0, f=3.0, t=24.0, total_len=24.0,
        hub_small=0.0, hub_large=0.0,
        d0=321.0, pipe_od=318.5, d_bore=304.7, inner_dia=321.0
    ),
    ('10K', 'SOP', 350): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=350,
        d=490.0, c=445.0, h=25.0, no=16, bolt_name='M22',
        g=413.0, f=3.0, t=26.0, total_len=26.0,
        hub_small=0.0, hub_large=0.0,
        d0=358.1, pipe_od=355.6, d_bore=339.8, inner_dia=358.1
    ),
    ('10K', 'SOP', 400): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=400,
        d=560.0, c=510.0, h=27.0, no=16, bolt_name='M24',
        g=475.0, f=3.0, t=28.0, total_len=28.0,
        hub_small=0.0, hub_large=0.0,
        d0=409.0, pipe_od=406.4, d_bore=390.6, inner_dia=409.0
    ),
    ('10K', 'SOP', 450): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=450,
        d=620.0, c=565.0, h=27.0, no=20, bolt_name='M24',
        g=530.0, f=3.0, t=30.0, total_len=30.0,
        hub_small=0.0, hub_large=0.0,
        d0=460.0, pipe_od=457.2, d_bore=441.4, inner_dia=460.0
    ),
    ('10K', 'SOP', 500): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=500,
        d=675.0, c=620.0, h=27.0, no=20, bolt_name='M24',
        g=585.0, f=3.0, t=30.0, total_len=30.0,
        hub_small=0.0, hub_large=0.0,
        d0=511.0, pipe_od=508.0, d_bore=492.2, inner_dia=511.0
    ),
    ('10K', 'SOP', 550): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=550,
        d=745.0, c=680.0, h=33.0, no=20, bolt_name='M30',
        g=640.0, f=3.0, t=32.0, total_len=32.0,
        hub_small=0.0, hub_large=0.0,
        d0=562.0, pipe_od=558.8, d_bore=543.0, inner_dia=562.0
    ),
    ('10K', 'SOP', 600): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=600,
        d=795.0, c=730.0, h=33.0, no=24, bolt_name='M30',
        g=690.0, f=3.0, t=32.0, total_len=32.0,
        hub_small=0.0, hub_large=0.0,
        d0=613.0, pipe_od=609.6, d_bore=593.8, inner_dia=613.0
    ),
    ('10K', 'SOP', 650): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=650,
        d=845.0, c=780.0, h=33.0, no=24, bolt_name='M30',
        g=740.0, f=3.0, t=34.0, total_len=34.0,
        hub_small=0.0, hub_large=0.0,
        d0=664.0, pipe_od=660.4, d_bore=644.6, inner_dia=664.0
    ),
    ('10K', 'SOP', 700): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=700,
        d=905.0, c=840.0, h=33.0, no=24, bolt_name='M30',
        g=800.0, f=3.0, t=34.0, total_len=34.0,
        hub_small=0.0, hub_large=0.0,
        d0=715.0, pipe_od=711.2, d_bore=695.4, inner_dia=715.0
    ),
    ('10K', 'SOP', 750): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=750,
        d=970.0, c=900.0, h=33.0, no=24, bolt_name='M30',
        g=855.0, f=3.0, t=36.0, total_len=36.0,
        hub_small=0.0, hub_large=0.0,
        d0=766.0, pipe_od=762.0, d_bore=746.2, inner_dia=766.0
    ),
    ('10K', 'SOP', 800): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=800,
        d=1020.0, c=950.0, h=33.0, no=28, bolt_name='M30',
        g=905.0, f=3.0, t=36.0, total_len=36.0,
        hub_small=0.0, hub_large=0.0,
        d0=817.0, pipe_od=812.8, d_bore=797.0, inner_dia=817.0
    ),
    ('10K', 'SOP', 850): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=850,
        d=1070.0, c=1000.0, h=33.0, no=28, bolt_name='M30',
        g=955.0, f=3.0, t=36.0, total_len=36.0,
        hub_small=0.0, hub_large=0.0,
        d0=868.0, pipe_od=863.6, d_bore=847.8, inner_dia=868.0
    ),
    ('10K', 'SOP', 900): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=900,
        d=1120.0, c=1050.0, h=33.0, no=28, bolt_name='M30',
        g=1005.0, f=3.0, t=38.0, total_len=38.0,
        hub_small=0.0, hub_large=0.0,
        d0=919.0, pipe_od=914.4, d_bore=898.6, inner_dia=919.0
    ),
    ('10K', 'SOP', 1000): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=1000,
        d=1235.0, c=1160.0, h=39.0, no=28, bolt_name='M36',
        g=1110.0, f=3.0, t=40.0, total_len=40.0,
        hub_small=0.0, hub_large=0.0,
        d0=1021.0, pipe_od=1016.0, d_bore=1000.2, inner_dia=1021.0
    ),
    ('10K', 'SOP', 1100): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=1100,
        d=1345.0, c=1270.0, h=39.0, no=28, bolt_name='M36',
        g=1220.0, f=3.0, t=42.0, total_len=42.0,
        hub_small=0.0, hub_large=0.0,
        d0=1122.0, pipe_od=1117.6, d_bore=1098.6, inner_dia=1122.0
    ),
    ('10K', 'SOP', 1200): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=1200,
        d=1465.0, c=1380.0, h=39.0, no=32, bolt_name='M36',
        g=1325.0, f=3.0, t=44.0, total_len=44.0,
        hub_small=0.0, hub_large=0.0,
        d0=1224.0, pipe_od=1219.2, d_bore=1200.2, inner_dia=1224.0
    ),
    ('10K', 'SOP', 1350): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=1350,
        d=1630.0, c=1540.0, h=45.0, no=36, bolt_name='M42',
        g=1480.0, f=3.0, t=48.0, total_len=48.0,
        hub_small=0.0, hub_large=0.0,
        d0=1376.0, pipe_od=1371.6, d_bore=1346.2, inner_dia=1376.0
    ),
    ('10K', 'SOP', 1500): FlangeDimensions(
        rating='10K', flange_type='SOP', dn=1500,
        d=1795.0, c=1700.0, h=45.0, no=40, bolt_name='M42',
        g=1635.0, f=3.0, t=50.0, total_len=50.0,
        hub_small=0.0, hub_large=0.0,
        d0=1529.0, pipe_od=1524.0, d_bore=1498.6, inner_dia=1529.0
    ),
    ('10K', 'WN', 10): FlangeDimensions(
        rating='10K', flange_type='WN', dn=10,
        d=90.0, c=65.0, h=15.0, no=4, bolt_name='M12',
        g=46.0, f=1.0, t=12.0, total_len=29.0,
        hub_small=17.3, hub_large=28.0,
        d0=17.8, pipe_od=17.3, d_bore=12.7, inner_dia=17.8
    ),
    ('10K', 'WN', 15): FlangeDimensions(
        rating='10K', flange_type='WN', dn=15,
        d=95.0, c=70.0, h=15.0, no=4, bolt_name='M12',
        g=51.0, f=1.0, t=12.0, total_len=31.0,
        hub_small=21.7, hub_large=33.0,
        d0=22.2, pipe_od=21.7, d_bore=16.1, inner_dia=22.2
    ),
    ('10K', 'WN', 20): FlangeDimensions(
        rating='10K', flange_type='WN', dn=20,
        d=100.0, c=75.0, h=15.0, no=4, bolt_name='M12',
        g=56.0, f=1.0, t=14.0, total_len=32.0,
        hub_small=27.2, hub_large=38.0,
        d0=27.7, pipe_od=27.2, d_bore=21.6, inner_dia=27.7
    ),
    ('10K', 'WN', 25): FlangeDimensions(
        rating='10K', flange_type='WN', dn=25,
        d=125.0, c=90.0, h=19.0, no=4, bolt_name='M16',
        g=67.0, f=2.0, t=14.0, total_len=36.0,
        hub_small=34.0, hub_large=47.0,
        d0=34.5, pipe_od=34.0, d_bore=27.6, inner_dia=34.5
    ),
    ('10K', 'WN', 32): FlangeDimensions(
        rating='10K', flange_type='WN', dn=32,
        d=135.0, c=100.0, h=19.0, no=4, bolt_name='M16',
        g=76.0, f=2.0, t=16.0, total_len=38.0,
        hub_small=42.7, hub_large=56.0,
        d0=43.2, pipe_od=42.7, d_bore=35.7, inner_dia=43.2
    ),
    ('10K', 'WN', 40): FlangeDimensions(
        rating='10K', flange_type='WN', dn=40,
        d=140.0, c=105.0, h=19.0, no=4, bolt_name='M16',
        g=81.0, f=2.0, t=16.0, total_len=38.0,
        hub_small=48.6, hub_large=62.0,
        d0=49.1, pipe_od=48.6, d_bore=41.6, inner_dia=49.1
    ),
    ('10K', 'WN', 50): FlangeDimensions(
        rating='10K', flange_type='WN', dn=50,
        d=155.0, c=120.0, h=19.0, no=4, bolt_name='M16',
        g=96.0, f=2.0, t=16.0, total_len=40.0,
        hub_small=60.5, hub_large=75.0,
        d0=61.1, pipe_od=60.5, d_bore=52.9, inner_dia=61.1
    ),
    ('10K', 'WN', 65): FlangeDimensions(
        rating='10K', flange_type='WN', dn=65,
        d=175.0, c=140.0, h=19.0, no=4, bolt_name='M16',
        g=116.0, f=2.0, t=18.0, total_len=44.0,
        hub_small=76.3, hub_large=92.0,
        d0=77.1, pipe_od=76.3, d_bore=67.9, inner_dia=77.1
    ),
    ('10K', 'WN', 80): FlangeDimensions(
        rating='10K', flange_type='WN', dn=80,
        d=185.0, c=150.0, h=19.0, no=8, bolt_name='M16',
        g=126.0, f=2.0, t=18.0, total_len=45.0,
        hub_small=89.1, hub_large=105.0,
        d0=90.0, pipe_od=89.1, d_bore=80.7, inner_dia=90.0
    ),
    ('10K', 'WN', 90): FlangeDimensions(
        rating='10K', flange_type='WN', dn=90,
        d=195.0, c=160.0, h=19.0, no=8, bolt_name='M16',
        g=136.0, f=2.0, t=18.0, total_len=45.0,
        hub_small=101.6, hub_large=117.0,
        d0=102.6, pipe_od=101.6, d_bore=93.2, inner_dia=102.6
    ),
    ('10K', 'WN', 100): FlangeDimensions(
        rating='10K', flange_type='WN', dn=100,
        d=210.0, c=175.0, h=19.0, no=8, bolt_name='M16',
        g=151.0, f=2.0, t=18.0, total_len=45.0,
        hub_small=114.3, hub_large=130.0,
        d0=115.4, pipe_od=114.3, d_bore=105.3, inner_dia=115.4
    ),
    ('10K', 'WN', 125): FlangeDimensions(
        rating='10K', flange_type='WN', dn=125,
        d=250.0, c=210.0, h=23.0, no=8, bolt_name='M20',
        g=182.0, f=2.0, t=20.0, total_len=47.0,
        hub_small=139.8, hub_large=156.0,
        d0=141.2, pipe_od=139.8, d_bore=130.8, inner_dia=141.2
    ),
    ('10K', 'WN', 150): FlangeDimensions(
        rating='10K', flange_type='WN', dn=150,
        d=280.0, c=240.0, h=23.0, no=8, bolt_name='M20',
        g=212.0, f=2.0, t=22.0, total_len=53.0,
        hub_small=165.2, hub_large=184.0,
        d0=166.6, pipe_od=165.2, d_bore=155.2, inner_dia=166.6
    ),
    ('10K', 'WN', 175): FlangeDimensions(
        rating='10K', flange_type='WN', dn=175,
        d=305.0, c=265.0, h=23.0, no=12, bolt_name='M20',
        g=237.0, f=2.0, t=22.0, total_len=55.0,
        hub_small=190.7, hub_large=210.0,
        d0=192.1, pipe_od=190.7, d_bore=180.1, inner_dia=192.1
    ),
    ('10K', 'WN', 200): FlangeDimensions(
        rating='10K', flange_type='WN', dn=200,
        d=330.0, c=290.0, h=23.0, no=12, bolt_name='M20',
        g=262.0, f=2.0, t=22.0, total_len=58.0,
        hub_small=216.3, hub_large=238.0,
        d0=218.0, pipe_od=216.3, d_bore=204.7, inner_dia=218.0
    ),
    ('10K', 'WN', 225): FlangeDimensions(
        rating='10K', flange_type='WN', dn=225,
        d=350.0, c=310.0, h=23.0, no=12, bolt_name='M20',
        g=282.0, f=2.0, t=22.0, total_len=58.0,
        hub_small=241.8, hub_large=261.0,
        d0=243.7, pipe_od=241.8, d_bore=229.4, inner_dia=243.7
    ),
    ('10K', 'WN', 250): FlangeDimensions(
        rating='10K', flange_type='WN', dn=250,
        d=400.0, c=355.0, h=25.0, no=12, bolt_name='M22',
        g=324.0, f=2.0, t=24.0, total_len=65.0,
        hub_small=267.4, hub_large=292.0,
        d0=269.5, pipe_od=267.4, d_bore=254.2, inner_dia=269.5
    ),
    ('10K', 'WN', 300): FlangeDimensions(
        rating='10K', flange_type='WN', dn=300,
        d=445.0, c=400.0, h=25.0, no=16, bolt_name='M22',
        g=368.0, f=3.0, t=24.0, total_len=68.0,
        hub_small=318.5, hub_large=345.0,
        d0=321.0, pipe_od=318.5, d_bore=304.7, inner_dia=321.0
    ),
    ('10K', 'WN', 350): FlangeDimensions(
        rating='10K', flange_type='WN', dn=350,
        d=490.0, c=445.0, h=25.0, no=16, bolt_name='M22',
        g=413.0, f=3.0, t=26.0, total_len=79.0,
        hub_small=355.6, hub_large=388.0,
        d0=358.1, pipe_od=355.6, d_bore=339.8, inner_dia=358.1
    ),
    ('10K', 'WN', 400): FlangeDimensions(
        rating='10K', flange_type='WN', dn=400,
        d=560.0, c=510.0, h=27.0, no=16, bolt_name='M24',
        g=475.0, f=3.0, t=28.0, total_len=85.0,
        hub_small=406.4, hub_large=442.0,
        d0=409.0, pipe_od=406.4, d_bore=390.6, inner_dia=409.0
    ),
    ('10K', 'WN', 450): FlangeDimensions(
        rating='10K', flange_type='WN', dn=450,
        d=620.0, c=565.0, h=27.0, no=20, bolt_name='M24',
        g=530.0, f=3.0, t=30.0, total_len=90.0,
        hub_small=457.2, hub_large=495.0,
        d0=460.0, pipe_od=457.2, d_bore=441.4, inner_dia=460.0
    ),
    ('10K', 'WN', 500): FlangeDimensions(
        rating='10K', flange_type='WN', dn=500,
        d=675.0, c=620.0, h=27.0, no=20, bolt_name='M24',
        g=585.0, f=3.0, t=30.0, total_len=90.0,
        hub_small=508.0, hub_large=546.0,
        d0=511.0, pipe_od=508.0, d_bore=492.2, inner_dia=511.0
    ),
    ('10K', 'WN', 550): FlangeDimensions(
        rating='10K', flange_type='WN', dn=550,
        d=745.0, c=680.0, h=33.0, no=20, bolt_name='M30',
        g=640.0, f=3.0, t=32.0, total_len=111.0,
        hub_small=558.8, hub_large=597.0,
        d0=562.0, pipe_od=558.8, d_bore=543.0, inner_dia=562.0
    ),
    ('10K', 'WN', 600): FlangeDimensions(
        rating='10K', flange_type='WN', dn=600,
        d=795.0, c=730.0, h=33.0, no=24, bolt_name='M30',
        g=690.0, f=3.0, t=32.0, total_len=112.0,
        hub_small=609.6, hub_large=648.0,
        d0=613.0, pipe_od=609.6, d_bore=593.8, inner_dia=613.0
    ),
    ('10K', 'WN', 650): FlangeDimensions(
        rating='10K', flange_type='WN', dn=650,
        d=845.0, c=780.0, h=33.0, no=24, bolt_name='M30',
        g=740.0, f=3.0, t=34.0, total_len=116.0,
        hub_small=660.4, hub_large=700.0,
        d0=664.0, pipe_od=660.4, d_bore=644.6, inner_dia=664.0
    ),
    ('10K', 'WN', 700): FlangeDimensions(
        rating='10K', flange_type='WN', dn=700,
        d=905.0, c=840.0, h=33.0, no=24, bolt_name='M30',
        g=800.0, f=3.0, t=34.0, total_len=132.0,
        hub_small=711.2, hub_large=754.0,
        d0=715.0, pipe_od=711.2, d_bore=695.4, inner_dia=715.0
    ),
    ('10K', 'WN', 750): FlangeDimensions(
        rating='10K', flange_type='WN', dn=750,
        d=970.0, c=900.0, h=33.0, no=24, bolt_name='M30',
        g=855.0, f=3.0, t=36.0, total_len=139.0,
        hub_small=762.0, hub_large=807.0,
        d0=766.0, pipe_od=762.0, d_bore=746.2, inner_dia=766.0
    ),
    ('10K', 'WN', 800): FlangeDimensions(
        rating='10K', flange_type='WN', dn=800,
        d=1020.0, c=950.0, h=33.0, no=28, bolt_name='M30',
        g=905.0, f=3.0, t=36.0, total_len=139.0,
        hub_small=812.8, hub_large=858.0,
        d0=817.0, pipe_od=812.8, d_bore=797.0, inner_dia=817.0
    ),
    ('10K', 'WN', 850): FlangeDimensions(
        rating='10K', flange_type='WN', dn=850,
        d=1070.0, c=1000.0, h=33.0, no=28, bolt_name='M30',
        g=955.0, f=3.0, t=36.0, total_len=139.0,
        hub_small=863.6, hub_large=908.0,
        d0=868.0, pipe_od=863.6, d_bore=847.8, inner_dia=868.0
    ),
    ('10K', 'WN', 900): FlangeDimensions(
        rating='10K', flange_type='WN', dn=900,
        d=1120.0, c=1050.0, h=33.0, no=28, bolt_name='M30',
        g=1005.0, f=3.0, t=38.0, total_len=140.0,
        hub_small=914.4, hub_large=959.0,
        d0=919.0, pipe_od=914.4, d_bore=898.6, inner_dia=919.0
    ),
    ('10K', 'WN', 1000): FlangeDimensions(
        rating='10K', flange_type='WN', dn=1000,
        d=1235.0, c=1160.0, h=39.0, no=28, bolt_name='M36',
        g=1110.0, f=3.0, t=40.0, total_len=151.0,
        hub_small=1016.0, hub_large=1065.0,
        d0=1021.0, pipe_od=1016.0, d_bore=1000.2, inner_dia=1021.0
    ),
    ('10K', 'WN', 1100): FlangeDimensions(
        rating='10K', flange_type='WN', dn=1100,
        d=1345.0, c=1270.0, h=39.0, no=28, bolt_name='M36',
        g=1220.0, f=3.0, t=42.0, total_len=170.0,
        hub_small=1117.6, hub_large=1174.0,
        d0=1122.0, pipe_od=1117.6, d_bore=1098.6, inner_dia=1122.0
    ),
    ('10K', 'WN', 1200): FlangeDimensions(
        rating='10K', flange_type='WN', dn=1200,
        d=1465.0, c=1380.0, h=39.0, no=32, bolt_name='M36',
        g=1325.0, f=3.0, t=44.0, total_len=182.0,
        hub_small=1219.2, hub_large=1281.0,
        d0=1224.0, pipe_od=1219.2, d_bore=1200.2, inner_dia=1224.0
    ),
    ('10K', 'WN', 1350): FlangeDimensions(
        rating='10K', flange_type='WN', dn=1350,
        d=1630.0, c=1540.0, h=45.0, no=36, bolt_name='M42',
        g=1480.0, f=3.0, t=48.0, total_len=200.0,
        hub_small=1371.6, hub_large=1438.0,
        d0=1376.0, pipe_od=1371.6, d_bore=1346.2, inner_dia=1376.0
    ),
    ('10K', 'WN', 1500): FlangeDimensions(
        rating='10K', flange_type='WN', dn=1500,
        d=1795.0, c=1700.0, h=45.0, no=40, bolt_name='M42',
        g=1635.0, f=3.0, t=50.0, total_len=218.0,
        hub_small=1524.0, hub_large=1598.0,
        d0=1529.0, pipe_od=1524.0, d_bore=1498.6, inner_dia=1529.0
    ),
    ('7K5', 'BL', 40): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=40,
        d=140.0, c=105.0, h=19.0, no=4, bolt_name='M16',
        g=85.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=48.6, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 50): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=50,
        d=155.0, c=120.0, h=19.0, no=4, bolt_name='M16',
        g=100.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=60.5, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 65): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=65,
        d=175.0, c=140.0, h=19.0, no=4, bolt_name='M16',
        g=120.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=76.3, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 80): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=80,
        d=185.0, c=150.0, h=19.0, no=8, bolt_name='M16',
        g=130.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=89.1, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 100): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=100,
        d=210.0, c=175.0, h=19.0, no=8, bolt_name='M16',
        g=155.0, f=2.0, t=20.0, total_len=20.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=114.3, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 125): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=125,
        d=250.0, c=210.0, h=19.0, no=8, bolt_name='M16',
        g=185.0, f=2.0, t=20.0, total_len=20.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=139.8, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 150): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=150,
        d=280.0, c=240.0, h=19.0, no=8, bolt_name='M16',
        g=215.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=165.2, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 200): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=200,
        d=342.0, c=299.0, h=19.0, no=8, bolt_name='M16',
        g=256.0, f=3.0, t=27.0, total_len=27.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=216.3, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 250): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=250,
        d=410.0, c=360.0, h=23.0, no=12, bolt_name='M20',
        g=314.0, f=3.0, t=29.0, total_len=29.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=267.4, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 300): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=300,
        d=464.0, c=414.0, h=23.0, no=12, bolt_name='M20',
        g=364.0, f=3.0, t=30.0, total_len=30.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=318.5, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 350): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=350,
        d=510.0, c=460.0, h=23.0, no=12, bolt_name='M20',
        g=414.0, f=3.0, t=32.0, total_len=32.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=355.6, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 400): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=400,
        d=565.0, c=515.0, h=25.0, no=16, bolt_name='M22',
        g=465.0, f=3.0, t=34.0, total_len=34.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=406.4, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 450): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=450,
        d=620.0, c=570.0, h=25.0, no=16, bolt_name='M22',
        g=520.0, f=3.0, t=36.0, total_len=36.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=457.2, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 500): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=500,
        d=675.0, c=620.0, h=25.0, no=16, bolt_name='M22',
        g=570.0, f=3.0, t=38.0, total_len=38.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=508.0, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'BL', 600): FlangeDimensions(
        rating='7K5', flange_type='BL', dn=600,
        d=795.0, c=740.0, h=25.0, no=20, bolt_name='M22',
        g=680.0, f=3.0, t=42.0, total_len=42.0,
        hub_small=0.0, hub_large=0.0,
        d0=0.0, pipe_od=609.6, d_bore=0.0, inner_dia=0.0
    ),
    ('7K5', 'IT', 40): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=40,
        d=140.0, c=105.0, h=19.0, no=4, bolt_name='M16',
        g=85.0, f=2.0, t=16.0, total_len=38.0,
        hub_small=48.6, hub_large=62.0,
        d0=49.1, pipe_od=48.6, d_bore=41.6, inner_dia=49.1
    ),
    ('7K5', 'IT', 50): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=50,
        d=155.0, c=120.0, h=19.0, no=4, bolt_name='M16',
        g=100.0, f=2.0, t=16.0, total_len=40.0,
        hub_small=60.5, hub_large=75.0,
        d0=61.1, pipe_od=60.5, d_bore=52.9, inner_dia=61.1
    ),
    ('7K5', 'IT', 65): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=65,
        d=175.0, c=140.0, h=19.0, no=4, bolt_name='M16',
        g=120.0, f=2.0, t=18.0, total_len=44.0,
        hub_small=76.3, hub_large=92.0,
        d0=77.1, pipe_od=76.3, d_bore=67.9, inner_dia=77.1
    ),
    ('7K5', 'IT', 80): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=80,
        d=185.0, c=150.0, h=19.0, no=8, bolt_name='M16',
        g=130.0, f=2.0, t=18.0, total_len=45.0,
        hub_small=89.1, hub_large=105.0,
        d0=90.0, pipe_od=89.1, d_bore=80.7, inner_dia=90.0
    ),
    ('7K5', 'IT', 100): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=100,
        d=210.0, c=175.0, h=19.0, no=8, bolt_name='M16',
        g=155.0, f=2.0, t=20.0, total_len=45.0,
        hub_small=114.3, hub_large=130.0,
        d0=115.4, pipe_od=114.3, d_bore=105.3, inner_dia=115.4
    ),
    ('7K5', 'IT', 125): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=125,
        d=250.0, c=210.0, h=19.0, no=8, bolt_name='M16',
        g=185.0, f=2.0, t=20.0, total_len=47.0,
        hub_small=139.8, hub_large=156.0,
        d0=141.2, pipe_od=139.8, d_bore=130.8, inner_dia=141.2
    ),
    ('7K5', 'IT', 150): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=150,
        d=280.0, c=240.0, h=19.0, no=8, bolt_name='M16',
        g=215.0, f=2.0, t=22.0, total_len=53.0,
        hub_small=165.2, hub_large=184.0,
        d0=166.6, pipe_od=165.2, d_bore=155.2, inner_dia=166.6
    ),
    ('7K5', 'IT', 200): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=200,
        d=342.0, c=299.0, h=19.0, no=8, bolt_name='M16',
        g=256.0, f=3.0, t=27.0, total_len=58.0,
        hub_small=216.3, hub_large=238.0,
        d0=218.0, pipe_od=216.3, d_bore=204.7, inner_dia=218.0
    ),
    ('7K5', 'IT', 250): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=250,
        d=410.0, c=360.0, h=23.0, no=12, bolt_name='M20',
        g=314.0, f=3.0, t=29.0, total_len=65.0,
        hub_small=267.4, hub_large=292.0,
        d0=269.5, pipe_od=267.4, d_bore=254.2, inner_dia=269.5
    ),
    ('7K5', 'IT', 300): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=300,
        d=464.0, c=414.0, h=23.0, no=12, bolt_name='M20',
        g=364.0, f=3.0, t=30.0, total_len=68.0,
        hub_small=318.5, hub_large=345.0,
        d0=321.0, pipe_od=318.5, d_bore=304.7, inner_dia=321.0
    ),
    ('7K5', 'IT', 350): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=350,
        d=510.0, c=460.0, h=23.0, no=12, bolt_name='M20',
        g=414.0, f=3.0, t=32.0, total_len=79.0,
        hub_small=355.6, hub_large=388.0,
        d0=358.1, pipe_od=355.6, d_bore=339.8, inner_dia=358.1
    ),
    ('7K5', 'IT', 400): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=400,
        d=565.0, c=515.0, h=25.0, no=16, bolt_name='M22',
        g=465.0, f=3.0, t=34.0, total_len=85.0,
        hub_small=406.4, hub_large=442.0,
        d0=409.0, pipe_od=406.4, d_bore=390.6, inner_dia=409.0
    ),
    ('7K5', 'IT', 450): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=450,
        d=620.0, c=570.0, h=25.0, no=16, bolt_name='M22',
        g=520.0, f=3.0, t=36.0, total_len=90.0,
        hub_small=457.2, hub_large=495.0,
        d0=460.0, pipe_od=457.2, d_bore=441.4, inner_dia=460.0
    ),
    ('7K5', 'IT', 500): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=500,
        d=675.0, c=620.0, h=25.0, no=16, bolt_name='M22',
        g=570.0, f=3.0, t=38.0, total_len=90.0,
        hub_small=508.0, hub_large=546.0,
        d0=511.0, pipe_od=508.0, d_bore=492.2, inner_dia=511.0
    ),
    ('7K5', 'IT', 600): FlangeDimensions(
        rating='7K5', flange_type='IT', dn=600,
        d=795.0, c=740.0, h=25.0, no=20, bolt_name='M22',
        g=680.0, f=3.0, t=42.0, total_len=112.0,
        hub_small=609.6, hub_large=648.0,
        d0=613.0, pipe_od=609.6, d_bore=593.8, inner_dia=613.0
    ),
    ('7K5', 'SOP', 40): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=40,
        d=140.0, c=105.0, h=19.0, no=4, bolt_name='M16',
        g=85.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=49.1, pipe_od=48.6, d_bore=41.6, inner_dia=49.1
    ),
    ('7K5', 'SOP', 50): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=50,
        d=155.0, c=120.0, h=19.0, no=4, bolt_name='M16',
        g=100.0, f=2.0, t=16.0, total_len=16.0,
        hub_small=0.0, hub_large=0.0,
        d0=61.1, pipe_od=60.5, d_bore=52.9, inner_dia=61.1
    ),
    ('7K5', 'SOP', 65): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=65,
        d=175.0, c=140.0, h=19.0, no=4, bolt_name='M16',
        g=120.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=77.1, pipe_od=76.3, d_bore=67.9, inner_dia=77.1
    ),
    ('7K5', 'SOP', 80): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=80,
        d=185.0, c=150.0, h=19.0, no=8, bolt_name='M16',
        g=130.0, f=2.0, t=18.0, total_len=18.0,
        hub_small=0.0, hub_large=0.0,
        d0=90.0, pipe_od=89.1, d_bore=80.7, inner_dia=90.0
    ),
    ('7K5', 'SOP', 100): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=100,
        d=210.0, c=175.0, h=19.0, no=8, bolt_name='M16',
        g=155.0, f=2.0, t=20.0, total_len=20.0,
        hub_small=0.0, hub_large=0.0,
        d0=115.4, pipe_od=114.3, d_bore=105.3, inner_dia=115.4
    ),
    ('7K5', 'SOP', 125): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=125,
        d=250.0, c=210.0, h=19.0, no=8, bolt_name='M16',
        g=185.0, f=2.0, t=20.0, total_len=20.0,
        hub_small=0.0, hub_large=0.0,
        d0=141.2, pipe_od=139.8, d_bore=130.8, inner_dia=141.2
    ),
    ('7K5', 'SOP', 150): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=150,
        d=280.0, c=240.0, h=19.0, no=8, bolt_name='M16',
        g=215.0, f=2.0, t=22.0, total_len=22.0,
        hub_small=0.0, hub_large=0.0,
        d0=166.6, pipe_od=165.2, d_bore=155.2, inner_dia=166.6
    ),
    ('7K5', 'SOP', 200): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=200,
        d=342.0, c=299.0, h=19.0, no=8, bolt_name='M16',
        g=256.0, f=3.0, t=27.0, total_len=27.0,
        hub_small=0.0, hub_large=0.0,
        d0=218.0, pipe_od=216.3, d_bore=204.7, inner_dia=218.0
    ),
    ('7K5', 'SOP', 250): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=250,
        d=410.0, c=360.0, h=23.0, no=12, bolt_name='M20',
        g=314.0, f=3.0, t=29.0, total_len=29.0,
        hub_small=0.0, hub_large=0.0,
        d0=269.5, pipe_od=267.4, d_bore=254.2, inner_dia=269.5
    ),
    ('7K5', 'SOP', 300): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=300,
        d=464.0, c=414.0, h=23.0, no=12, bolt_name='M20',
        g=364.0, f=3.0, t=30.0, total_len=30.0,
        hub_small=0.0, hub_large=0.0,
        d0=321.0, pipe_od=318.5, d_bore=304.7, inner_dia=321.0
    ),
    ('7K5', 'SOP', 350): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=350,
        d=510.0, c=460.0, h=23.0, no=12, bolt_name='M20',
        g=414.0, f=3.0, t=32.0, total_len=32.0,
        hub_small=0.0, hub_large=0.0,
        d0=358.1, pipe_od=355.6, d_bore=339.8, inner_dia=358.1
    ),
    ('7K5', 'SOP', 400): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=400,
        d=565.0, c=515.0, h=25.0, no=16, bolt_name='M22',
        g=465.0, f=3.0, t=34.0, total_len=34.0,
        hub_small=0.0, hub_large=0.0,
        d0=409.0, pipe_od=406.4, d_bore=390.6, inner_dia=409.0
    ),
    ('7K5', 'SOP', 450): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=450,
        d=620.0, c=570.0, h=25.0, no=16, bolt_name='M22',
        g=520.0, f=3.0, t=36.0, total_len=36.0,
        hub_small=0.0, hub_large=0.0,
        d0=460.0, pipe_od=457.2, d_bore=441.4, inner_dia=460.0
    ),
    ('7K5', 'SOP', 500): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=500,
        d=675.0, c=620.0, h=25.0, no=16, bolt_name='M22',
        g=570.0, f=3.0, t=38.0, total_len=38.0,
        hub_small=0.0, hub_large=0.0,
        d0=511.0, pipe_od=508.0, d_bore=492.2, inner_dia=511.0
    ),
    ('7K5', 'SOP', 600): FlangeDimensions(
        rating='7K5', flange_type='SOP', dn=600,
        d=795.0, c=740.0, h=25.0, no=20, bolt_name='M22',
        g=680.0, f=3.0, t=42.0, total_len=42.0,
        hub_small=0.0, hub_large=0.0,
        d0=613.0, pipe_od=609.6, d_bore=593.8, inner_dia=613.0
    ),
    ('7K5', 'WN', 40): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=40,
        d=140.0, c=105.0, h=19.0, no=4, bolt_name='M16',
        g=85.0, f=2.0, t=16.0, total_len=38.0,
        hub_small=48.6, hub_large=62.0,
        d0=49.1, pipe_od=48.6, d_bore=41.6, inner_dia=49.1
    ),
    ('7K5', 'WN', 50): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=50,
        d=155.0, c=120.0, h=19.0, no=4, bolt_name='M16',
        g=100.0, f=2.0, t=16.0, total_len=40.0,
        hub_small=60.5, hub_large=75.0,
        d0=61.1, pipe_od=60.5, d_bore=52.9, inner_dia=61.1
    ),
    ('7K5', 'WN', 65): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=65,
        d=175.0, c=140.0, h=19.0, no=4, bolt_name='M16',
        g=120.0, f=2.0, t=18.0, total_len=44.0,
        hub_small=76.3, hub_large=92.0,
        d0=77.1, pipe_od=76.3, d_bore=67.9, inner_dia=77.1
    ),
    ('7K5', 'WN', 80): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=80,
        d=185.0, c=150.0, h=19.0, no=8, bolt_name='M16',
        g=130.0, f=2.0, t=18.0, total_len=45.0,
        hub_small=89.1, hub_large=105.0,
        d0=90.0, pipe_od=89.1, d_bore=80.7, inner_dia=90.0
    ),
    ('7K5', 'WN', 100): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=100,
        d=210.0, c=175.0, h=19.0, no=8, bolt_name='M16',
        g=155.0, f=2.0, t=20.0, total_len=45.0,
        hub_small=114.3, hub_large=130.0,
        d0=115.4, pipe_od=114.3, d_bore=105.3, inner_dia=115.4
    ),
    ('7K5', 'WN', 125): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=125,
        d=250.0, c=210.0, h=19.0, no=8, bolt_name='M16',
        g=185.0, f=2.0, t=20.0, total_len=47.0,
        hub_small=139.8, hub_large=156.0,
        d0=141.2, pipe_od=139.8, d_bore=130.8, inner_dia=141.2
    ),
    ('7K5', 'WN', 150): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=150,
        d=280.0, c=240.0, h=19.0, no=8, bolt_name='M16',
        g=215.0, f=2.0, t=22.0, total_len=53.0,
        hub_small=165.2, hub_large=184.0,
        d0=166.6, pipe_od=165.2, d_bore=155.2, inner_dia=166.6
    ),
    ('7K5', 'WN', 200): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=200,
        d=342.0, c=299.0, h=19.0, no=8, bolt_name='M16',
        g=256.0, f=3.0, t=27.0, total_len=58.0,
        hub_small=216.3, hub_large=238.0,
        d0=218.0, pipe_od=216.3, d_bore=204.7, inner_dia=218.0
    ),
    ('7K5', 'WN', 250): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=250,
        d=410.0, c=360.0, h=23.0, no=12, bolt_name='M20',
        g=314.0, f=3.0, t=29.0, total_len=65.0,
        hub_small=267.4, hub_large=292.0,
        d0=269.5, pipe_od=267.4, d_bore=254.2, inner_dia=269.5
    ),
    ('7K5', 'WN', 300): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=300,
        d=464.0, c=414.0, h=23.0, no=12, bolt_name='M20',
        g=364.0, f=3.0, t=30.0, total_len=68.0,
        hub_small=318.5, hub_large=345.0,
        d0=321.0, pipe_od=318.5, d_bore=304.7, inner_dia=321.0
    ),
    ('7K5', 'WN', 350): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=350,
        d=510.0, c=460.0, h=23.0, no=12, bolt_name='M20',
        g=414.0, f=3.0, t=32.0, total_len=79.0,
        hub_small=355.6, hub_large=388.0,
        d0=358.1, pipe_od=355.6, d_bore=339.8, inner_dia=358.1
    ),
    ('7K5', 'WN', 400): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=400,
        d=565.0, c=515.0, h=25.0, no=16, bolt_name='M22',
        g=465.0, f=3.0, t=34.0, total_len=85.0,
        hub_small=406.4, hub_large=442.0,
        d0=409.0, pipe_od=406.4, d_bore=390.6, inner_dia=409.0
    ),
    ('7K5', 'WN', 450): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=450,
        d=620.0, c=570.0, h=25.0, no=16, bolt_name='M22',
        g=520.0, f=3.0, t=36.0, total_len=90.0,
        hub_small=457.2, hub_large=495.0,
        d0=460.0, pipe_od=457.2, d_bore=441.4, inner_dia=460.0
    ),
    ('7K5', 'WN', 500): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=500,
        d=675.0, c=620.0, h=25.0, no=16, bolt_name='M22',
        g=570.0, f=3.0, t=38.0, total_len=90.0,
        hub_small=508.0, hub_large=546.0,
        d0=511.0, pipe_od=508.0, d_bore=492.2, inner_dia=511.0
    ),
    ('7K5', 'WN', 600): FlangeDimensions(
        rating='7K5', flange_type='WN', dn=600,
        d=795.0, c=740.0, h=25.0, no=20, bolt_name='M22',
        g=680.0, f=3.0, t=42.0, total_len=112.0,
        hub_small=609.6, hub_large=648.0,
        d0=613.0, pipe_od=609.6, d_bore=593.8, inner_dia=613.0
    ),
}
