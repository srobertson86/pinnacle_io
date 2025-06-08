"""
Writer for Pinnacle Institution files.
"""
from pinnacle_io.models import Institution

class InstitutionWriter:
    """
    Writer for Pinnacle Institution files.
    """
    @staticmethod
    def write(institution: Institution, path: str) -> None:
        """
        Write a Pinnacle Institution model to files.
        
        Args:
            institution: Institution model
            path: Path to write the Institution files
        """
        raise NotImplementedError("InstitutionWriter.write is not implemented")
    