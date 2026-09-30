import slint_testing
from slint_testing import PointerEventButton


def query(window: slint_testing.Window, id: str) -> slint_testing.ElementQuery:
    return window.query_descendants().match_id(f"AppWindow::{id}")


def fill_in(window: slint_testing.Window, email: str, password: str):
    query(window, "email-input").find_one().accessible_value = email
    query(window, "password-input").find_one().accessible_value = password
    query(window, "accept-terms").find_one().single_click(PointerEventButton.Left)


def test_terms_must_be_accepted(window: slint_testing.Window):
    accept_terms = query(window, "accept-terms").find_one()
    sign_up_button = query(window, "sign-up-button").find_one()

    assert not accept_terms.accessible_checked
    assert not sign_up_button.accessible_enabled

    accept_terms.invoke_accessible_default_action()
    assert accept_terms.accessible_checked
    assert sign_up_button.accessible_enabled


def test_invalid_email(window: slint_testing.Window):
    fill_in(window, "not an email", "correct horse")
    query(window, "sign-up-button").find_one().invoke_accessible_default_action()

    assert query(window, "error-label").find_one().accessible_label == (
        "Please enter a valid email address."
    )
    assert query(window, "welcome-label").find_first() is None


def test_short_password(window: slint_testing.Window):
    fill_in(window, "ada@example.com", "secret")
    query(window, "sign-up-button").find_one().invoke_accessible_default_action()

    assert query(window, "error-label").find_one().accessible_label == (
        "The password must be at least 8 characters long."
    )


def test_sign_up_and_quit(app: slint_testing.Application, window: slint_testing.Window):
    # The form and the welcome screen are in `if` conditions in the .slint file, so their elements are
    # created and destroyed as the app switches between them. Tracking elements follow those changes.
    sign_up_button = query(window, "sign-up-button").tracking().find_one()
    welcome_label = query(window, "welcome-label").tracking().find_first()
    assert welcome_label is None

    fill_in(window, "ada@example.com", "correct horse")
    sign_up_button.single_click(PointerEventButton.Left)

    assert not sign_up_button.is_valid
    welcome_label = query(window, "welcome-label").tracking().find_one()
    assert welcome_label.accessible_label == "Welcome, ada@example.com!"

    query(window, "quit-button").find_one().invoke_accessible_default_action()
    assert app.wait(timeout=10) == 0
