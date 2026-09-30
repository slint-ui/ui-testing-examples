from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

import slint

ui = slint.load_file(Path(__file__).parent / "app-window.slint")


def format_amount(amount: Decimal) -> str:
    return str(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


class App(ui.AppWindow):
    def __init__(self):
        super().__init__()
        self.recalculate()

    @slint.callback
    def recalculate(self):
        try:
            bill = Decimal(self.bill or "0")
        except InvalidOperation:
            bill = Decimal(0)
        tip = bill * self.tip_percent / 100
        self.tip_amount = format_amount(tip)
        self.total_per_person = format_amount((bill + tip) / self.people)


if __name__ == "__main__":
    App().run()
