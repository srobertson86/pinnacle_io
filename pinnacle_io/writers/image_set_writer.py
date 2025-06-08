"""
Writer for Pinnacle ImageSet files.
"""

from pinnacle_io.models import ImageSet

class ImageSetWriter:
    """
    Writer for Pinnacle ImageSet files.
    """
    @staticmethod
    def write(image_set: ImageSet, path: str) -> None:
        """
        Write a Pinnacle ImageSet model to files.

        Args:
            image_set: ImageSet model
            path: Path to write the ImageSet files
        """
        raise NotImplementedError("ImageSetWriter.write is not implemented")
