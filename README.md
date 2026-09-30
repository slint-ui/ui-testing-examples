# Slint UI Testing Examples

Example applications built with [Slint](https://slint.dev), each with a suite of Python tests that
use [Slint UI Testing](https://testing.slint.dev/) to launch the application, find UI elements, interact with
them, and verify the results.

| Example | Language | Shows |
| --- | --- | --- |
| [`rust-todo`](rust-todo/) | Rust | Lists and `find_all`, queries by role and label, checkboxes, enabled state, tracking elements |
| [`cpp-temperature-converter`](cpp-temperature-converter/) | C++ | Text input, parametrized tests, error states, keyboard events |
| [`node-signup`](node-signup/) | Node.js | Forms, elements in `if` conditions, quitting the application |
| [`python-tip-calculator`](python-tip-calculator/) | Python | Spin boxes, increment and decrement actions, value ranges |

Each example is self-contained. Copy its directory as a starting point for your own project.

## Prerequisites

- [uv](https://docs.astral.sh/uv/), which also provides Python.
- For the Rust and C++ examples: a [Rust toolchain](https://rustup.rs/). The C++ example builds Slint from source.
- For the C++ example: [CMake](https://cmake.org/) 3.21 or newer and a C++20 compiler.
- For the Node.js example: [Node.js](https://nodejs.org/) 20 or newer.
- An access token for Slint UI Testing's package index at `testing.slint.dev`.

## Set up access to `slint-testing`

The `slint_testing` Python package is distributed through Slint's package index at `testing.slint.dev`. Give
your token to uv once per machine:

```shell
uv auth login https://testing.slint.dev/simple/ --token <TOKEN>
```

Each example's `pyproject.toml` points uv at that index for `slint-testing` only. The URL holds no token,
so it's safe to commit.

## Run the tests

```shell
cd rust-todo    # or any other example
uv run pytest -v
```

The first run builds the application, which takes a while for the C++ example because Slint gets compiled.
When a test fails, a screenshot of the window is saved in `screenshots/`.

## How it works

The application needs system testing support, which is left out of regular builds so it isn't part of
the application you ship:

- In Rust, the application's `system-testing` Cargo feature enables the `system-testing` feature of the
  `slint` crate. The tests build with that feature.
- In C++, the tests configure CMake with `-DSLINT_FEATURE_SYSTEM_TESTING=ON`.
- In Node.js, `slint-ui-dev` is a dev dependency next to `slint-ui`.
- In Python, `slint[dev]` is in the `dev` dependency group next to `slint`.

For Rust and C++, the tests also set the `SLINT_EMIT_DEBUG_INFO=1` environment variable during the build,
so that the element ids from the `.slint` files, such as `AppWindow::add-button`, are available to the tests.
Node.js and Python compile `.slint` files at run time and always keep the element ids.

`slint_testing.Application` launches the application and waits for its first window to connect back. Each test
gets a fresh instance of the application through pytest fixtures in `tests/conftest.py`.

See the [Slint UI Testing documentation](https://testing.slint.dev/) for the full API.

## Continuous integration

The [CI workflow](.github/workflows/ci.yaml) runs the tests on Linux, macOS, and Windows. It reads the token
from the `SLINT_TESTING_TOKEN` repository secret and passes it to uv through the
`UV_INDEX_SLINT_PRIVATE_USERNAME` and `UV_INDEX_SLINT_PRIVATE_PASSWORD` environment variables. On Linux, a
virtual X display lets the application show its windows.

## License

The examples are available under the [MIT license](LICENSE).
