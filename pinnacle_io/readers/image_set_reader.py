"""
Reader for Pinnacle ImageSet files.
"""

from pathlib import Path
import numpy as np
from pinnacle_io.models import ImageSet, ImageInfo
from pinnacle_io.readers.pinnacle_file_reader import PinnacleFileReader


class ImageSetReader:
    """
    Reader for Pinnacle ImageSet files.

    This class provides methods for reading ImageSet files and creating models from the data in the files.
    """

    @staticmethod
    def read_header(image_header_path: str) -> ImageSet:
        """
        Read a Pinnacle ImageSet header file and create an ImageSet model. 
        The ImageInfoList is also read from the ImageInfo file.

        Args:
            image_header_path: /Path/to/ImageSet_# (the .header extension is optional)

        Returns:
            ImageSet model populated with data from the file
        """
        path = Path(image_header_path)
        if not str(path).lower().endswith(".header"):
            path = path.with_suffix(".header")

        if not path.exists():
            raise FileNotFoundError(f"ImageSet header file not found: {path}")

        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            image_set = ImageSetReader.parse_header_content(f.readlines())
        
        image_set.image_info_list = ImageSetReader.read_image_info(str(path.with_suffix(".ImageInfo")))
        return image_set

    @staticmethod
    def parse_header_content(content_lines: list[str]) -> ImageSet:
        """
        Parse a Pinnacle ImageSet header content string and create an ImageSet model. 
        The ImageInfoList is not parsed.

        Args:
            content_lines: Pinnacle ImageSet header content lines

        Returns:
            ImageSet model populated with data from the content
        """
        data = PinnacleFileReader.parse_key_value_content_lines(content_lines)
        image_set = ImageSet(**data)
        return image_set

    @staticmethod
    def read_image_info(path: str) -> list[ImageInfo]:
        """
        Read a Pinnacle ImageSet info file and create an ImageInfo model.

        Args:
            path: /Path/to/ImageSet_# (the .ImageInfo extension is optional)

        Returns:
            List of ImageInfo models populated with data from the file
        """
        path = Path(path)
        if not str(path).lower().endswith(".ImageInfo"):
            path = path.with_suffix(".ImageInfo")

        if not path.exists():
            raise FileNotFoundError(f"ImageSet info file not found: {path}")

        with open(path, 'r', encoding='latin1', errors='ignore') as f:
            return ImageSetReader.parse_image_info_content(f.readlines())

    @staticmethod
    def parse_image_info_content(content_lines: list[str]) -> list[ImageInfo]:
        """Parse a Pinnacle ImageSet info content string and create an ImageInfo model.

        Args:
            content_lines: Pinnacle ImageSet info content lines

        Returns:
            List of ImageInfo models populated with data from the content
        """
        data = PinnacleFileReader.parse_key_value_content_lines(content_lines)
        image_info_list = [
            ImageInfo(**image_info) for image_info in data.get("ImageInfoList", {})
        ]
        return image_info_list

    @staticmethod
    def read_image_set(path: str, image_set: ImageSet = None) -> ImageSet:
        """Read a Pinnacle ImageSet file and create an ImageSet model.

        Args:
            path: /Path/to/ImageSet_# (the .img extension is optional)

        Returns:
            ImageSet model populated with data from the file
        """
        path = Path(path)
        if not str(path).lower().endswith(".img"):
            path = path.with_suffix(".img")

        if not path.exists():
            raise FileNotFoundError(f"ImageSet file not found: {path}")

        if image_set is None:
            image_set = ImageSetReader.read_header(path.with_suffix(".header")) # Replaces the suffix

        with open(path, "rb") as f:
            binary_data = f.read()
            pixel_data = np.frombuffer(binary_data, dtype=np.uint16).reshape(
                image_set.z_dim, image_set.y_dim, image_set.x_dim
            )

        image_set.pixel_data = pixel_data
        return image_set
