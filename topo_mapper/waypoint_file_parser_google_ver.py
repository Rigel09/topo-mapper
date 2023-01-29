from topo_mapper.conversions import lla2mercxya
from topo_mapper.enums import Feature, stringToFeature


import numpy as np
import pandas as pd
from pathlib import Path


def apply_glyph_url(feature_type: str) -> str:
    if feature_type == Feature.FALLS.name:
        return "https://raw.githubusercontent.com/Rigel09/topo-mapper/main/glyphs/waterfall-icon-png.jpg"
    elif feature_type == Feature.PARKING.name:
        return "https://raw.githubusercontent.com/Rigel09/topo-mapper/main/glyphs/parking.png"


class WaypointFileParserGoogle:
    class COL:
        NAME = "NAME"
        LAT = "LATITUDE"
        LONG = "LONGITUDE"
        ALT = "ALTITUDE"
        MERC_X = "MERCATOR_X_COORD"
        MERC_Y = "MERCATOR_Y_COORD"
        INFO = "INFO"
        GLYPH_URL = "GLYPH_URL"

        FILE_ONLY_COLS = [NAME, LAT, LONG, INFO]
        COMPUTED_COLS = [ALT, MERC_X, MERC_Y, GLYPH_URL]
        ALL_COLS = FILE_ONLY_COLS + COMPUTED_COLS

    def __init__(self, filename: Path) -> None:
        if filename.suffix == "csv":
            self.df = pd.read_csv(
                filename, index_col=False, names=self.COL.FILE_ONLY_COLS, header=None, skiprows=1
            )
        else:
            self.df = pd.read_excel(
                filename, index_col=False, names=self.COL.FILE_ONLY_COLS, header=None, skiprows=1
            )
        self._feature: Feature = None

        fname = f"{filename.stem}"
        if "falls" in fname:
            self._feature = Feature.FALLS
        elif "parking" in fname:
            self._feature = Feature.PARKING
        elif "head" in fname:
            self._feature = Feature.TRAIL_HEAD
        elif "unique" in fname:
            self._feature = Feature.UNIQUE_FEATURE
        elif "junction" in fname:
            self._feature = Feature.TRAIL_JUNCTION

        for col in self.COL.COMPUTED_COLS:
            self.df[col] = 0

        self.df[self.COL.GLYPH_URL] = apply_glyph_url(self._feature)

        lla = np.ones((self.df.shape[0], 3))
        lla[:, 0] = self.df[self.COL.LAT].to_numpy()
        lla[:, 1] = self.df[self.COL.LONG].to_numpy()
        lla[:, 2] = self.df[self.COL.ALT].to_numpy()
        xya = lla2mercxya(lla)
        self.df[self.COL.MERC_X] = xya[:, 0]
        self.df[self.COL.MERC_Y] = xya[:, 1]
