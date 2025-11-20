from datetime import datetime, timedelta
from html.parser import endtagfind
from skyfield.api import EarthSatellite, load, wgs84
import json

ELEVATION_MIN_DEG = 10
STEP_SECONDS = 30

def next_overflight_times(project):
    config = json.load(open(f"acquisition_forecaster/projects/{project}/input/config.json"))
    tle_path = f"acquisition_forecaster/projects/{project}/input/tle"
    with open(tle_path, "r") as f:
        tle_lines = [line.strip() for line in f.readlines() if line.strip()]
    if len(tle_lines) < 2:
        raise ValueError("TLE file must contain at least two non-empty lines")

    ts = load.timescale()
    sat = EarthSatellite(tle_lines[0], tle_lines[1], "SAT", ts)
    observer = wgs84.latlon(config["POINT"][1], config["POINT"][0], 0.0)

    start_utc = datetime.strptime(config["START_DATE"], "%Y-%m-%d")
    end_utc = datetime.strptime(config["END_DATE"], "%Y-%m-%d") + timedelta(days=1)
    t = start_utc
    while t < end_utc:
        # current altitude
        tf = ts.utc(t.year, t.month, t.day, t.hour, t.minute, t.second)
        alt_now = (sat - observer).at(tf).altaz()[0].degrees

        # next step
        t_next = t + timedelta(seconds=STEP_SECONDS)
        if t_next > end_utc:
            t_next = end_utc

        tf_next = ts.utc(t_next.year, t_next.month, t_next.day,
                         t_next.hour, t_next.minute, t_next.second)
        alt_next = (sat - observer).at(tf_next).altaz()[0].degrees

        # Look for crossing from below -> above
        if alt_now < ELEVATION_MIN_DEG <= alt_next:
            # Linear interpolation between t and t_next
            frac = (ELEVATION_MIN_DEG - alt_now) / (alt_next - alt_now)
            dt_sec = (t_next - t).total_seconds()
            t_cross = t + timedelta(seconds=frac * dt_sec)
            return t_cross  # naive UTC datetime

        t = t_next

    return None


# Example usage:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Estimate next satellite pass time")
    parser.add_argument("--project", type=str, required=True, help="Project name")
    args = parser.parse_args()

    ts_over = next_overflight_times(args.project)

    print(f"Next overflight above {ELEVATION_MIN_DEG}°:", ts_over, "UTC")
