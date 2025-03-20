from pathlib import Path

from attr import attrib, attrs
from pref import Pref, PrefOrderedSet
from appdirs import user_data_dir

from ..__version__ import application_name, author
from pytest_fly.common.platform_info import get_performance_core_count

preferences_file_name = f"{application_name}_preferences.db"

scheduler_time_quantum_default = 1.0
refresh_rate_default = 3.0
utilization_high_threshold_default = 0.8
utilization_low_threshold_default = 0.5


@attrs
class FlyPreferences(Pref):
    window_x: int = attrib(default=-1)
    window_y: int = attrib(default=-1)
    window_width: int = attrib(default=-1)
    window_height: int = attrib(default=-1)
    verbose: bool = attrib(default=False)
    processes: int = attrib(default=get_performance_core_count())  # number of processes to use
    scheduler_time_quantum: float = attrib(default=scheduler_time_quantum_default)  # scheduler time quantum in seconds
    refresh_rate: float = attrib(default=refresh_rate_default)  # display minimum refresh rate in seconds
    utilization_high_threshold: float = attrib(default=utilization_high_threshold_default)  # above this threshold, the process is considered high utilization
    utilization_low_threshold: float = attrib(default=utilization_low_threshold_default)  # below this threshold, the process is considered low utilization
    csv_dump_path: str = attrib(default=str(Path(user_data_dir(application_name, author), f"{application_name}.csv")))


def get_pref() -> FlyPreferences:
    return FlyPreferences(application_name, author, file_name=preferences_file_name)


class PrefSplits(PrefOrderedSet):
    def __init__(self):
        super().__init__(application_name, author, "split", preferences_file_name)


def get_splits() -> PrefOrderedSet:
    return PrefSplits()
