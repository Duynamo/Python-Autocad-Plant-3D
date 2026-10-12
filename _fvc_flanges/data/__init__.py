import os
from .dataset import FLANGE_DATASET

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jis_b2220.sqlite")

__all__ = ["DB_PATH", "FLANGE_DATASET"]
