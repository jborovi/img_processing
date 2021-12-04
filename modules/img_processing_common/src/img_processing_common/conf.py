"""
Shared variables used across the project
"""

import os

DATA_PROCESS = os.path.join(
    os.getenv("SHARED_VOLUME", "/tmp/images"),
    os.getenv("DIR_PROCESS", "process"),
)
DATA_DONE = os.path.join(
    os.getenv("SHARED_VOLUME", "/tmp/images"),
    os.getenv("DIR_DONE", "done"),
)
