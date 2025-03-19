from dataclasses import dataclass


@dataclass
class DataExport:
    name: str
    title: str
    description: str


DATA_EXPORT_CATALOG = [
    DataExport(
        name="ALL_MONITORS",
        title="All monitors",
        description="All monitors with aggregated properties, excluding deleted monitors.",
    ),
]
