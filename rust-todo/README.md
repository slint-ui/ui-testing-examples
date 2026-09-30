# To-Do List (Rust)

A to-do list written in Rust, with a text field and button to add items, a `ListView` of checkboxes, and a
button to clear completed items.

## Files

- [`ui/app-window.slint`](ui/app-window.slint): The UI. Elements the tests use have ids, such as
  `add-button := Button { ... }`.
- [`src/main.rs`](src/main.rs): The application logic, which keeps the items in a `VecModel`.
- [`Cargo.toml`](Cargo.toml): Declares a `system-testing` feature that forwards to the `slint` crate.
- [`tests/conftest.py`](tests/conftest.py): Fixtures that build the application once, launch it for each
  test, and save a screenshot when a test fails.
- [`tests/test_todo.py`](tests/test_todo.py): The tests.

## What the tests show

- Finding elements by id with `match_id("AppWindow::add-button")`, and by accessible role with
  `match_accessible_role(...)`, then picking one of them by its `accessible_label`.
- Finding all rows of a list with `find_all()`.
- Entering text by setting `accessible_value`, and clicking buttons with `invoke_accessible_default_action()`.
- Clicking with the mouse through `single_click()`.
- Checking `accessible_checked`, `accessible_enabled`, and `accessible_placeholder_text`.
- Following an element across model changes with a `tracking()` query.

## Run

```shell
uv run pytest -v
```

To run the application on its own, use `cargo run`.
