from topo_mapper.waypoint_file_parser import WaypointFileParser as wfp
from topo_mapper.conversions import lla2mercxya

from bokeh.driving import count
from bokeh.layouts import column, gridplot, row
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.plotting import figure, show
import numpy as np
import pandas as pd
import xyzservices.providers as xyz

from argparse import ArgumentParser
import logging
from pathlib import Path
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)

COLUMNS = ["name", "lat", "long", "type"]


if __name__ == "__main__":
    parser = ArgumentParser("Creates a TOPO Map of a Destination")
    parser.add_argument(
        "--waypoints",
        type=str,
        action="append",
        help="CSV file of waypoints, name, lat, long, alt, desc",
    )
    parser.add_argument("--trail", type=str, help="CSV file of trail waypoints")
    args = parser.parse_args()

    if not args.waypoints:
        raise RuntimeError("Waypoints are required for plotting")

    waypoint_files = [Path(x) for x in args.waypoints]

    data = pd.DataFrame(columns=COLUMNS)
    for file in waypoint_files:
        if not file.exists():
            raise FileExistsError(f"File [{file}] cannot be found")

        data = pd.concat(
            [
                data,
                pd.read_csv(
                    file, delimiter=",", header=None, index_col=False, names=COLUMNS, skiprows=1
                ),
            ],
            ignore_index=True,
        )

    logger.info("All files loaded")

    print(data)
    lla = np.ones(data.shape) * 180
    lla[:, 0] = data["lat"].to_numpy()
    lla[:, 1] = data["long"].to_numpy()
    lla = lla2mercxya(lla)
    map = figure(
        title="TOPO Map", x_axis_type="mercator", y_axis_type="mercator", sizing_mode="stretch_both"
    )
    map.add_tile(xyz.USGS.USTopo, retina=True)
    map.scatter(lla[:, 0], lla[:, 1], line_width=4, color="orange")
    show(column(map, sizing_mode="stretch_both"))
