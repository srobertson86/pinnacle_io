"""
Writer for Pinnacle Plan files.
"""

from pinnacle_io.models import Plan

class PlanWriter:
    """
    Writer for Pinnacle Plan files.
    """
    @staticmethod
    def write(plan: Plan, path: str) -> None:
        """
        Write a Pinnacle Plan model to files.

        Args:
            plan: Plan model
            path: Path to write the Plan files
        """
        raise NotImplementedError("PlanWriter.write is not implemented")
