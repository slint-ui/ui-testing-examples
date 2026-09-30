import pytest
import slint_testing
from slint_testing import KeyPressedEvent, KeyReleasedEvent, PointerEventButton, keys


def find(window: slint_testing.Window, id: str) -> slint_testing.Element:
    return window.query_descendants().match_id(f"App::{id}").find_one()


@pytest.mark.parametrize(
    ("celsius", "fahrenheit"),
    [("100", "212"), ("0", "32"), ("-40", "-40"), ("37", "98.6")],
)
def test_convert(window: slint_testing.Window, celsius: str, fahrenheit: str):
    find(window, "celsius-input").accessible_value = celsius
    find(window, "convert-button").invoke_accessible_default_action()

    assert find(window, "fahrenheit-input").accessible_value == fahrenheit
    assert find(window, "error-label").accessible_label == ""


def test_fahrenheit_is_read_only(window: slint_testing.Window):
    assert find(window, "fahrenheit-input").accessible_read_only
    assert not find(window, "celsius-input").accessible_read_only


def test_invalid_input(window: slint_testing.Window):
    celsius_input = find(window, "celsius-input")
    convert_button = find(window, "convert-button")
    fahrenheit_input = find(window, "fahrenheit-input")
    error_label = find(window, "error-label")

    celsius_input.accessible_value = "hot"
    convert_button.invoke_accessible_default_action()
    assert fahrenheit_input.accessible_value == ""
    assert error_label.accessible_label == "Please enter a number."

    # A valid value afterwards clears the error again.
    celsius_input.accessible_value = "20"
    convert_button.invoke_accessible_default_action()
    assert fahrenheit_input.accessible_value == "68"
    assert error_label.accessible_label == ""


def test_type_and_press_return(window: slint_testing.Window):
    """Simulates a user clicking into the field, typing, and pressing Return."""
    celsius_input = find(window, "celsius-input")
    celsius_input.single_click(PointerEventButton.Left)

    for text in ["2", "5", keys.Return]:
        window.dispatch_event(KeyPressedEvent(text=text))
        window.dispatch_event(KeyReleasedEvent(text=text))

    assert celsius_input.accessible_value == "25"
    assert find(window, "fahrenheit-input").accessible_value == "77"
