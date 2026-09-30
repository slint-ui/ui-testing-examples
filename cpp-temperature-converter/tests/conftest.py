import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest
import slint_testing

PROJECT_DIR = Path(__file__).resolve().parent.parent
BUILD_DIR = PROJECT_DIR / "build"
SCREENSHOT_DIR = PROJECT_DIR / "screenshots"


@pytest.fixture(scope="session")
def app_binary() -> Path:
    """Configures and builds the application once per test session, with system testing enabled."""
    env = os.environ.copy()
    # The Slint compiler must emit debug info for element ids to be visible to the tests.
    env["SLINT_EMIT_DEBUG_INFO"] = "1"
    subprocess.run(
        [
            "cmake",
            "-B",
            str(BUILD_DIR),
            "-DCMAKE_BUILD_TYPE=Debug",
            "-DSLINT_FEATURE_SYSTEM_TESTING=ON",
        ],
        cwd=PROJECT_DIR,
        env=env,
        check=True,
    )
    subprocess.run(
        ["cmake", "--build", str(BUILD_DIR), "--config", "Debug"],
        cwd=PROJECT_DIR,
        env=env,
        check=True,
    )
    exe = (
        "temperature_converter.exe"
        if sys.platform == "win32"
        else "temperature_converter"
    )
    # Multi-config generators, such as Visual Studio, place the binary in a per-configuration directory.
    for candidate in [BUILD_DIR / exe, BUILD_DIR / "Debug" / exe]:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not find {exe} in {BUILD_DIR}")


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    report = yield
    # Make the outcome of each phase available to fixtures, see `window` below.
    setattr(item, f"report_{report.when}", report)
    return report


@pytest.fixture
def app(app_binary: Path) -> Iterator[slint_testing.Application]:
    """Launches a fresh instance of the application for each test."""
    with slint_testing.Application([str(app_binary)]) as app:
        yield app


@pytest.fixture
def window(
    app: slint_testing.Application, request: pytest.FixtureRequest
) -> Iterator[slint_testing.Window]:
    window = app.first_window
    assert window is not None
    yield window

    # Keep a screenshot of the window when a test failed, to help with debugging.
    report = getattr(request.node, "report_call", None)
    if report is not None and report.failed:
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        path = SCREENSHOT_DIR / f"{request.node.name}.png"
        try:
            path.write_bytes(window.grab_window_as_png())
        except slint_testing.RequestError as error:
            print(f"Could not grab a screenshot: {error}")
