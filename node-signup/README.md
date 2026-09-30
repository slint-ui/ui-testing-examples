# Sign-Up Form (Node.js)

A sign-up form written in JavaScript with Slint for Node.js. It checks the email address and password, requires
accepting the terms of service, and replaces the form with a welcome screen after signing up.

## Files

- [`ui/app-window.slint`](ui/app-window.slint): The UI. The form and the welcome screen are in `if`
  conditions, so their elements are created and destroyed as the application switches between them.
- [`main.js`](main.js): The validation logic.
- [`package.json`](package.json): Depends on `slint-ui`, and on `slint-ui-dev` as a dev dependency.
  `slint-ui-dev` provides a variant of the Slint binary with system testing support, which `slint-ui` loads
  only when `SLINT_TEST_SERVER` is set. A production install with `npm install --omit=dev` leaves it out.
- [`tests/conftest.py`](tests/conftest.py): Fixtures that run `npm install` once, launch the application for
  each test, and save a screenshot when a test fails.
- [`tests/test_signup.py`](tests/test_signup.py): The tests.

## What the tests show

- Enabling a button through a checkbox, with `invoke_accessible_default_action()` and `single_click()`.
- Checking error messages through `accessible_label`.
- Following elements that appear and disappear with `tracking()` queries, and checking
  `is_valid` once an element is gone.
- Quitting the application from the UI and checking its exit code with `Application.wait()`.

## Run

This example requires [Node.js](https://nodejs.org/) 20 or newer.

```shell
uv run pytest -v
```

To run the application on its own:

```shell
npm install
npm start
```
