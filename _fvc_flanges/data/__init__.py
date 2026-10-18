import os
from .jis_b2220_dataset import JIS_B2220_FLANGE_DATASET

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jis_b2220.sqlite")

__all__ = ["DB_PATH", "JIS_B2220_FLANGE_DATASET"]
