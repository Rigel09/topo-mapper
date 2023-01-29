from topo_mapper.waypoint_file_parser_google_ver import WaypointFileParserGoogle as wfpg
from topo_mapper.enums import Feature

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show
import numpy as np
import pandas as pd
import xyzservices.providers as xyz

from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
from typing import Optional


if __name__ == "__main__":
    parser = ArgumentParser("Creates a TOPO Map of a Destination given a folder")
    parser.add_argument(
        "directory",
        type=str,
        nargs="?",
        help="Folder that contains CSV files of waypoints plotted in the google map",
    )
    parser.add_argument("--trail", type=str, help="CSV file of trail waypoints")
    args = parser.parse_args()

    directory = args.directory
    if not directory:
        directory = Path("../site_info_python/bankhead/")
        print(f"Defaulting working directory to {directory}")

    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory [{directory}] doesn't exist")

    waypoint_files = [Path(x) for x in directory.glob("*")]
    print(f"Found the following files:")
    for x in waypoint_files:
        print(f"\t{x}")

    map = figure(
        title="TOPO Map", x_axis_type="mercator", y_axis_type="mercator", sizing_mode="stretch_both"
    )
    map.add_tile(xyz.USGS.USTopo, retina=True)

    data = pd.DataFrame(columns=wfpg.COL.ALL_COLS)
    opts = {"x": wfpg.COL.MERC_X, "y": wfpg.COL.MERC_Y}
    nvc = "#880e4f"  # not vistited color
    for file in waypoint_files:
        if not file.suffix not in ["csv", "xlsx"]:
            print(f"Ignoring file [{file}]")
            continue

        print(f"Loading file {file}")

        data_frame = wfpg(file).df
        data_source = ColumnDataSource(data_frame)
        opts["source"] = data_source

        fname = f"{file.stem}"
        if fname == "waterfalls_not_visited":
            map.square(**opts, color=nvc, size=9, legend_label="waterfalls not visited")
        elif fname == "waterfalls_visited":
            map.square(**opts, color="#106dc9", size=9, legend_label="waterfalls visited")
        elif fname == "cemetaries_not_visited":
            map.cross(**opts, color=nvc, size=10, legend_label="cemetaries not visited")
        elif fname == "cemetaries_visited":
            map.cross(**opts, color="black", size=10, legend_label="cemetaries visited")
        elif fname == "parking":
            map.circle(**opts, color="red", size=10, legend_label="parking")
        elif fname == "trail_junctions":
            map.circle(**opts, color="black", size=8, legend_label="trail junctions")
        elif fname == "trailheads":
            map.triangle(**opts, color="red", size=10, legend_lable="trailheads")
        elif fname == "unique_features_not_visited":
            map.star(**opts, color=nvc, size=18, legend_label="unique feature not visited")
        elif fname == "unique_features_visited":
            map.star(**opts, color="orange", size=18, legend_label="unique features visited")
        elif fname == "campsites":
            pass


    print("All files loaded")

    map.legend.click_policy = "hide"
    map.add_tools(
        HoverTool(
            tooltips=[
                ("Name", "@" + wfpg.COL.NAME),
                ("LAT", "@" + wfpg.COL.LAT),
                ("LONG", "@" + wfpg.COL.LONG),
                ("ALT", "@" + wfpg.COL.ALT),
                ("INFO", "@" + wfpg.COL.INFO),
            ]
        )
    )
    show(column(map, sizing_mode="stretch_both"))
