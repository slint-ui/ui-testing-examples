import slint_testing
from slint_testing import KeyPressedEvent, KeyReleasedEvent, PointerEventButton, keys


def find(window: slint_testing.Window, id: str) -> slint_testing.Element:
    return window.query_descendants().match_id(f"AppWindow::{id}").find_one()


def press_return(window: slint_testing.Window):
    window.dispatch_event(KeyPressedEvent(text=keys.Return))
    window.dispatch_event(KeyReleasedEvent(text=keys.Return))


def enter_bill(window: slint_testing.Window, amount: str):
    """Enters the bill amount and accepts it with Return, like a user would."""
    bill_input = find(window, "bill-input")
    bill_input.accessible_value = amount
    bill_input.single_click(PointerEventButton.Left)
    press_return(window)


def test_defaults(window: slint_testing.Window):
    tip_input = find(window, "tip-input")
    assert tip_input.accessible_value == "15"
    assert tip_input.accessible_value_minimum == 0
    assert tip_input.accessible_value_maximum == 30

    people_input = find(window, "people-input")
    assert people_input.accessible_value == "1"
    assert people_input.accessible_value_minimum == 1

    assert find(window, "tip-label").accessible_label == "0.00"
    assert find(window, "total-label").accessible_label == "0.00"


def test_calculate(window: slint_testing.Window):
    enter_bill(window, "80")

    assert find(window, "tip-label").accessible_label == "12.00"
    assert find(window, "total-label").accessible_label == "92.00"


def test_split_between_people(window: slint_testing.Window):
    enter_bill(window, "100")
    people_input = find(window, "people-input")
    total_label = find(window, "total-label")

    people_input.invoke_accessible_increment_action()
    people_input.invoke_accessible_increment_action()
    assert people_input.accessible_value == "3"
    # 115 split three ways, rounded to cents.
    assert total_label.accessible_label == "38.33"

    people_input.invoke_accessible_decrement_action()
    assert total_label.accessible_label == "57.50"


def test_tip_stays_within_range(window: slint_testing.Window):
    tip_input = find(window, "tip-input")

    for _ in range(20):
        tip_input.invoke_accessible_increment_action()
    assert tip_input.accessible_value == "30"

    for _ in range(40):
        tip_input.invoke_accessible_decrement_action()
    assert tip_input.accessible_value == "0"


def test_bill_is_used_once_accepted(window: slint_testing.Window):
    bill_input = find(window, "bill-input")
    total_label = find(window, "total-label")

    # Typing alone doesn't change the result yet.
    bill_input.accessible_value = "80"
    assert total_label.accessible_label == "0.00"

    bill_input.single_click(PointerEventButton.Left)
    press_return(window)
    assert total_label.accessible_label == "92.00"


def test_invalid_bill(window: slint_testing.Window):
    enter_bill(window, "80")
    assert find(window, "total-label").accessible_label == "92.00"

    # A bill that isn't a number counts as zero.
    enter_bill(window, "lots")

    assert find(window, "tip-label").accessible_label == "0.00"
    assert find(window, "total-label").accessible_label == "0.00"
