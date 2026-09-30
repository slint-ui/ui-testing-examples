# Temperature Converter (C++)

A C++ application that converts a temperature from Celsius to Fahrenheit, and shows an error when the input
isn't a number.

## Files

- [`ui/app-window.slint`](ui/app-window.slint): The UI. Elements the tests use have ids, such as
  `convert-button := Button { ... }`.
- [`main.cpp`](main.cpp): The conversion logic.
- [`CMakeLists.txt`](CMakeLists.txt): Fetches Slint and builds it from source, so that the tests can turn
  on `SLINT_FEATURE_SYSTEM_TESTING`.
- [`tests/conftest.py`](tests/conftest.py): Fixtures that configure and build the application once, launch
  it for each test, and save a screenshot when a test fails.
- [`tests/test_converter.py`](tests/test_converter.py): The tests.

## What the tests show

- Entering text by setting `accessible_value`, and reading results back from `accessible_value` and
  `accessible_label`.
- Running the same test with several inputs through `pytest.mark.parametrize`.
- Checking error states and `accessible_read_only`.
- Simulating a user who clicks into a field, types, and presses Return, with `single_click()` and
  `Window.dispatch_event()`.

## Run

```shell
uv run pytest -v
```

The first run takes a few minutes because it builds Slint. To build and run the application on its own:

```shell
cmake -B build
cmake --build build
./build/temperature_converter
```
