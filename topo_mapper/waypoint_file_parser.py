import pandas as pd
from pathlib import Path


class WaypointFileParser:
    class COL:
        NAME = "NAME"
        LAT = "LATITUDE"
        LONG = "LONGITUDE"
        ALT = "ALTITUDE"
        DESC = "DESCRIPTION"

        FILE_ONLY_COLS = [LAT, LONG, ALT]
        COMPUTED_COLS = []
        ALL_COLS = FILE_ONLY_COLS + COMPUTED_COLS

    def __init__(self, filename: Path) -> None:
        self.df = pd.read_csv(filename, index_col=False, names=self.COL.FILE_ONLY_COLS)

        # TODO Extend this class for waypoint conversion as well. Lat/lon to decimal
