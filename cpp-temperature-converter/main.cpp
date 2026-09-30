#include "app-window.h"

#include <cerrno>
#include <cstdlib>
#include <format>
#include <optional>
#include <string>

static std::optional<double> parse_number(const std::string &text)
{
    const char *begin = text.c_str();
    char *end = nullptr;
    errno = 0;
    double value = std::strtod(begin, &end);
    if (end == begin || errno == ERANGE) {
        return std::nullopt;
    }
    while (*end == ' ') {
        ++end;
    }
    if (*end != '\0') {
        return std::nullopt;
    }
    return value;
}

int main()
{
    auto app = App::create();

    app->on_convert([weak = slint::ComponentWeakHandle(app)](slint::SharedString celsius_text) {
        auto app = *weak.lock();
        if (auto celsius = parse_number(std::string(celsius_text))) {
            double fahrenheit = *celsius * 9.0 / 5.0 + 32.0;
            app->set_fahrenheit(slint::SharedString(std::format("{:g}", fahrenheit)));
            app->set_error("");
        } else {
            app->set_fahrenheit("");
            app->set_error("Please enter a number.");
        }
    });

    app->run();
}
