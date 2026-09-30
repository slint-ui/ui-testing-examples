import * as slint from "slint-ui";

const ui = slint.loadFile(new URL("ui/app-window.slint", import.meta.url));
const app = new ui.AppWindow();

function validate(email, password) {
    if (!/^[^@\s]+@[^@\s]+$/.test(email)) {
        return "Please enter a valid email address.";
    }
    if (password.length < 8) {
        return "The password must be at least 8 characters long.";
    }
    return "";
}

app.sign_up = (email, password) => {
    const error = validate(email.trim(), password);
    app.error = error;
    if (error === "") {
        app.signed_up_email = email.trim();
    }
};

app.quit = () => {
    slint.quitEventLoop();
};

await app.run();
