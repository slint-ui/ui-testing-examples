import shutil
import subprocess
from collections.abc import Iterator
from pathlib import Path

import pytest
import slint_testing

PROJECT_DIR = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = PROJECT_DIR / "screenshots"


@pytest.fixture(scope="session")
def app_command() -> list[str]:
    """Installs the npm dependencies once per test session and returns the command to launch the app."""
    npm = shutil.which("npm")
    node = shutil.which("node")
    if npm is None or node is None:
        pytest.fail("Node.js and npm are required to run the tests")
    # Installs slint-ui-dev from devDependencies, which slint-ui loads when SLINT_TEST_SERVER is set.
    subprocess.run(
        [npm, "install", "--no-audit", "--no-fund"], cwd=PROJECT_DIR, check=True
    )
    return [node, str(PROJECT_DIR / "main.js")]


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    report = yield
    # Make the outcome of each phase available to fixtures, see `window` below.
    setattr(item, f"report_{report.when}", report)
    return report


@pytest.fixture
def app(app_command: list[str]) -> Iterator[slint_testing.Application]:
    """Launches a fresh instance of the application for each test."""
    with slint_testing.Application(app_command) as app:
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
