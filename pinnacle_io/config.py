"""
Configuration settings and constants for the pinnacle_io package.
"""
from pathlib import Path
from typing import Dict, Any

# File extensions and patterns
INSTITUTION_HEADER_FILE = ".header"
PATIENT_INFO_FILE = ".PatientInfo"
PLAN_TRIAL_FILE = "plan.Trial"
PLAN_POINTS_FILE = "plan.Points"
PLAN_ROI_FILE = "plan.roi"
PLAN_SETUP_FILE = "plan.PatientSetup"
IMAGE_INFO_FILE = ".ImageInfo"

# Temporary directory settings
DEFAULT_TEMP_DIR = Path("./tmp")
MIN_DISK_SPACE_MB = 1000  # Minimum disk space required for extraction (in MB)

# Default encoding for Pinnacle files
DEFAULT_ENCODING = "utf-8"

# Common Pinnacle file format settings
PINNACLE_INDENT = "    "  # 4 spaces
PINNACLE_NEWLINE = "\n"

# Type aliases
PinnacleData = Dict[str, Any]
