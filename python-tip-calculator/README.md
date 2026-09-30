# Tip Calculator (Python)

A tip calculator written with Slint for Python. It computes the tip and the amount per person for a bill,
a tip percentage, and the number of people who share it.

## Files

- [`app-window.slint`](app-window.slint): The UI. It calls `recalculate()` when the user accepts the bill
  amount with Return, or changes a spin box.
- [`main.py`](main.py): The calculation.
- [`pyproject.toml`](pyproject.toml): The application depends on `slint`. The `dev` dependency group, which
  uv installs by default, adds the test dependencies and `slint[dev]`. That extra provides a variant of
  the Slint binary with system testing support, which `slint` loads only when `SLINT_TEST_SERVER` is set.
- [`tests/conftest.py`](tests/conftest.py): Fixtures that launch the application for each test with the same
  Python environment as the tests, and save a screenshot when a test fails.
- [`tests/test_tip_calculator.py`](tests/test_tip_calculator.py): The tests.

## What the tests show

- Reading the range of a `SpinBox` through `accessible_value_minimum` and `accessible_value_maximum`.
- Changing values with `invoke_accessible_increment_action()` and `invoke_accessible_decrement_action()`,
  and checking that they stay within range.
- Entering text by setting `accessible_value`, then clicking into the field and pressing Return with
  `single_click()` and `Window.dispatch_event()` to accept it.
- Checking that the result only changes once the input is accepted, through `accessible_label`.

## Run

This example requires Python 3.12 or newer, which uv installs when needed.

```shell
uv run pytest -v
```

To run the application on its own, use `uv run main.py`.
