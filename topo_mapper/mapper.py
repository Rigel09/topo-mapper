from topo_mapper.waypoint_file_parser import WaypointFileParser as wfp
from topo_mapper.conversions import lla2mercxya
from topo_mapper.enums import Feature

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool
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

    data = pd.DataFrame(columns=wfp.COL.ALL_COLS)
    for file in waypoint_files:
        if not file.exists():
            raise FileExistsError(f"File [{file}] cannot be found")

        data = pd.concat(
            [
                data,
                wfp(file).df,
            ],
            ignore_index=True,
        )

    logger.info("All files loaded")
    source = ColumnDataSource(data)
    print(data)
    map = figure(
        title="TOPO Map", x_axis_type="mercator", y_axis_type="mercator", sizing_mode="stretch_both"
    )
    map.add_tile(xyz.USGS.USTopo, retina=True)

    waterfall_source = ColumnDataSource(data[data[wfp.COL.FEATURE_TYPE_STR] == Feature.FALLS.name])
    parking_source = ColumnDataSource(data[data[wfp.COL.FEATURE_TYPE_STR] == Feature.PARKING.name])
    trail_junc_source = ColumnDataSource(
        data[data[wfp.COL.FEATURE_TYPE_STR] == Feature.TRAIL_JUNCTION.name]
    )
    trail_head_source = ColumnDataSource(
        data[data[wfp.COL.FEATURE_TYPE_STR] == Feature.TRAIL_HEAD.name]
    )
    uniquq_feature_source = ColumnDataSource(
        data[data[wfp.COL.FEATURE_TYPE_STR] == Feature.UNIQUE_FEATURE.name]
    )
    print(waterfall_source)
    map.image_url(
        url=wfp.COL.GLYPH_URL,
        x=wfp.COL.MERC_X,
        y=wfp.COL.MERC_Y,
        w=25,
        h=25,
        w_units="screen",
        h_units="screen",
        anchor="bottom_left",
        source=waterfall_source,
        legend_label="Waterfalls",
    )
    map.image_url(
        url=wfp.COL.GLYPH_URL,
        x=wfp.COL.MERC_X,
        y=wfp.COL.MERC_Y,
        w=15,
        h=15,
        w_units="screen",
        h_units="screen",
        anchor="bottom_left",
        source=parking_source,
        legend_label="Parking",
    )
    map.square(
        x=wfp.COL.MERC_X,
        y=wfp.COL.MERC_Y,
        size=9,
        color="black",
        legend_label="Trail Junction",
        source=trail_junc_source,
    )
    map.star(
        x=wfp.COL.MERC_X,
        y=wfp.COL.MERC_Y,
        size=18,
        color="orange",
        legend_label="Unique Feature",
        source=uniquq_feature_source,
    )
    map.scatter(
        x=wfp.COL.MERC_X,
        y=wfp.COL.MERC_Y,
        color="red",
        size=10,
        legend_label="Trailhead",
        source=trail_head_source,
    )
    map.legend.click_policy = "hide"
    map.add_tools(
        HoverTool(
            tooltips=[
                ("Name", "@" + wfp.COL.NAME),
                ("LAT", "@" + wfp.COL.LAT),
                ("LONG", "@" + wfp.COL.LONG),
                ("ALT", "@" + wfp.COL.ALT),
                ("Feature Type", "@" + wfp.COL.FEATURE_TYPE_STR),
                ("DESC", "@" + wfp.COL.DESC),
            ]
        )
    )
    show(column(map, sizing_mode="stretch_both"))
