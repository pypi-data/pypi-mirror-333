import os
from picamera2 import Picamera2
from labthings_picamera2 import recalibrate_utils

import pytest


MODEL = Picamera2.global_camera_info()[0]['Model']


def check_camera_available():
    assert len(Picamera2.global_camera_info()) >= 1


def load_default_tuning():
    fname = f"{MODEL}.json"
    return Picamera2.load_tuning_file(fname)


def generate_bad_tuning():
    default_tuning = load_default_tuning()
    bad_tuning = default_tuning.copy()
    bad_tuning["version"] = 999
    return bad_tuning


def print_tuning(read_file=False):
    key = "LIBCAMERA_RPI_TUNING_FILE"
    if key in os.environ:
        print(f"Tuning file environment variable: {os.environ[key]}")
        if read_file:
            with open(os.environ[key], "r") as f:
                print(f.read())
    else:
        print("Tuning file environment variable not set")


def _test_bad_tuning_after_good_tuning(configure):
    bad_tuning = generate_bad_tuning()
    default_tuning = load_default_tuning()
    print_tuning()
    print("opening camera with explicitly specified tuning")
    with Picamera2(tuning=default_tuning) as cam:
        print_tuning()
        if configure:
            cam.configure(cam.create_preview_configuration())
    del cam
    recalibrate_utils.recreate_camera_manager()
    print(f"Opening camera with tuning['version'] = {bad_tuning['version']}")
    with pytest.raises(IndexError):
        # The bad version should cause a problem
        cam = Picamera2(tuning=bad_tuning)
        print_tuning()
        print("Success (not expected)!")
        del cam
    recalibrate_utils.recreate_camera_manager()
    with Picamera2(tuning=default_tuning) as cam:
        # Reload the camera with working tuning, or it will stop responding
        # and fail future tests
        pass
    del cam


@pytest.mark.filterwarnings("ignore: Exception ignored")
def test_bad_tuning_after_good_tuning_noconfigure():
    _test_bad_tuning_after_good_tuning(False)


@pytest.mark.filterwarnings("ignore: Exception ignored")
def test_bad_tuning_after_good_tuning_configure():
    _test_bad_tuning_after_good_tuning(True)


@pytest.mark.filterwarnings("ignore: Exception ignored")
def test_bad_tuning_after_good_tuning_noconfigure2():
    _test_bad_tuning_after_good_tuning(False)


@pytest.mark.filterwarnings("ignore: Exception ignored")
def test_bad_tuning_after_good_tuning_configure2():
    _test_bad_tuning_after_good_tuning(True)
