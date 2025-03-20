import pathlib
import httpx
import pytest
from sqlalchemy.sql import ColumnElement
from sqlmodel.sql.expression import SelectOfScalar
from sqlmodel import select
from doplaydo.dodata_core.models import Cell, Project, DeviceData, Device, Die, Wafer
import doplaydo.dodata as dd
from tqdm.auto import tqdm

module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent
notebooks_path = repo_path / "notebooks"
wafer_id = "6d4c615ff105"
spirals_data = notebooks_path / "spirals" / wafer_id

if __name__ == "__main__":
    spectrum_measurement_type = dd.api.device_data.PlottingKwargs(
        x_name="wavelength",
        y_name="output_power",
        x_col="wavelength",
        y_col=["output_power"],  # can also be a string for a single value
        # y_col="output_power",
    )

    MEASUREMENTS_PATH = spirals_data
    PROJECT_ID = "spirals"
    data_files = list(MEASUREMENTS_PATH.glob("**/data.json"))
    project_ids = []
    device_ids = []
    die_xs = []
    die_ys = []
    wafer_ids = []
    plotting_kwargs = []
    data_types = []
    die_ids = []

    for path in data_files:
        device_id = path.parts[-2]
        die_id = path.parts[-3]
        die_x, die_y = die_id.split("_")
        wafer_id = path.parts[-4]

        device_ids.append(device_id)
        die_ids.append(die_id)
        die_xs.append(die_x)
        die_ys.append(die_y)
        wafer_ids.append(wafer_id)
        plotting_kwargs.append(spectrum_measurement_type)
        project_ids.append(PROJECT_ID)
        data_types.append("measurement")

    die_set = set(die_ids)
    wafer_set = set(wafer_ids)
    database_dies = []
    widths_um = [0.3, 0.5, 0.8]

    for wafer in wafer_set:
        for die_id in tqdm(die_set):
            die_x, die_y = die_id.split("_")
            for width_um in widths_um:
                r = dd.analysis.trigger_die(
                    project_id=PROJECT_ID,
                    wafer_id=wafer,
                    die_x=die_x,
                    die_y=die_y,
                    analysis_function_id="loss_cutback",
                    parameters={"width_um": width_um},
                )
                if r.status_code != 200:
                    raise httpx.HTTPError(r.text)
