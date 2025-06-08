"""
This module provides enumerations for representing patient position and setup information.
"""

from enum import Enum

# Patient Position Enumeration
class PatientPositionEnum(str, Enum):
    """
    Enumeration of patient position codes used in Pinnacle.

    Supine: On back
    Prone: On front
    DecubitusRight: Right side down
    DecubitusLeft: Left side down
    UNKNOWN: Unknown position
    """

    Supine = "On back (supine)"
    Prone = "On front (prone)" 
    DecubitusRight = "Right side down"
    DecubitusLeft = "Left side down"
    Unknown = "Unknown"


class PatientOrientationEnum(str, Enum):
    """
    Enumeration of patient orientation codes used in Pinnacle.

    HeadFirst: Head First Into Scanner
    FeetFirst: Feet First Into Scanner
    UNKNOWN: Unknown orientation
    """

    HeadFirst = "Head First Into Scanner"
    FeetFirst = "Feet First Into Scanner"
    Unknown = "Unknown"


class TableMotionEnum(str, Enum):
    """
    Enumeration of table motion codes used in DICOM.

    IntoScanner: Table Moves Into Scanner 
    OutOfScanner: Table Moves Out Of Scanner
    UNKNOWN: Unknown table motion

    TODO: Verify the Pinnacle OutOfScanner string
    """

    IntoScanner = "Table Moves Into Scanner"
    OutOfScanner = "Table Moves Out Of Scanner"
    Unknown = "Unknown"


class PatientSetupEnum(str, Enum):
    """
    Enumeration of patient setup codes used in DICOM.

    HFS: Head First-Supine
    HFP: Head First-Prone
    FFS: Feet First-Supine
    FFP: Feet First-Prone
    HFDR: Head First-Decubitus Right
    HFDL: Head First-Decubitus Left
    FFDR: Feet First-Decubitus Right
    FFDL: Feet First-Decubitus Left
    UNKNOWN: Unknown setup
    """

    HFS = "HFS"  # Head First-Supine
    HFP = "HFP"  # Head First-Prone
    FFS = "FFS"  # Feet First-Supine
    FFP = "FFP"  # Feet First-Prone
    HFDR = "HFDR"  # Head First-Decubitus Right
    HFDL = "HFDL"  # Head First-Decubitus Left
    FFDR = "FFDR"  # Feet First-Decubitus Right
    FFDL = "FFDL"  # Feet First-Decubitus Left
    Unknown = "Unknown"  # Unknown setup

    @classmethod
    def from_orientation_and_position(
        cls, orientation: PatientOrientationEnum, position: PatientPositionEnum
    ) -> "PatientSetupEnum":
        """
        Create a PatientSetupEnum instance from orientation and position strings.

        Args:
            orientation: Orientation enumeration
            position: Position enumeration

        Returns:
            PatientSetupEnum instance.
        """

        orientation_tag = {
            PatientOrientationEnum.HeadFirst: "HF",
            PatientOrientationEnum.FeetFirst: "FF",
        }.get(orientation, "")

        position_tag = {
            PatientPositionEnum.Supine: "S",
            PatientPositionEnum.Prone: "P",
            PatientPositionEnum.DecubitusRight: "DR",
            PatientPositionEnum.DecubitusLeft: "DL",
        }.get(position, "")

        if orientation_tag and position_tag:
            return cls(orientation_tag + position_tag)
        
        return cls.Unknown
