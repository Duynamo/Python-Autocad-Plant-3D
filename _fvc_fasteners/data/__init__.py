import os
from .jis_b1217_dataset import JIS_B1180_METRIC_DATASET, JIS_B1217_BOLT_DATASET
from .jis_b1180_dataset import (
    JIS_B1180_BOLT_TYPES,
    JIS_B1180_PITCH_SPECS,
    JIS_B1180_HEAD_DIMENSIONS,
)

JIS_B1217_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jis_b1217.sqlite")
JIS_B1180_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jis_b1180.sqlite")
DB_PATH = JIS_B1217_DB_PATH

__all__ = [
    "DB_PATH",
    "JIS_B1217_DB_PATH",
    "JIS_B1180_DB_PATH",
    "JIS_B1180_METRIC_DATASET",
    "JIS_B1217_BOLT_DATASET",
    "JIS_B1180_BOLT_TYPES",
    "JIS_B1180_PITCH_SPECS",
    "JIS_B1180_HEAD_DIMENSIONS",
]
