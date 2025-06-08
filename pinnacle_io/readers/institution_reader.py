"""
Reader for Pinnacle Institution files.
"""
from pathlib import Path
from pinnacle_io.models import Institution
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader


class InstitutionReader:
    """
    Reader for Pinnacle Institution files.
    """
    @staticmethod
    def read(institution_path: str) -> Institution:
        """
        Read a Pinnacle Institution directory and create an Institution model.
        
        Args:
            institution_path: Path to the Institution directory
            
        Returns:
            Institution model populated with data from the files
        """
        path = Path(institution_path)
        if not str(path).lower().endswith('institution'):
            path = path / 'Institution'
        
        if not path.exists():
            raise FileNotFoundError(f"Institution file not found: {path}")
        
        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            return InstitutionReader.parse_institution_content(f.readlines())
    
    @staticmethod
    def parse_institution_content(content_lines: list[str]) -> Institution:
        """
        Parse a Pinnacle Institution content string and create an Institution model.
        
        Args:
            content_lines: Pinnacle Institution content lines
            
        Returns:
            Institution model populated with data from the content
        """
        data = PinnacleFileReader.parse_key_value_content_lines(content_lines)
        institution = Institution(**data)
        return institution