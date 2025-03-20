from uphy.device import api
from functools import partial
from rich.live import Live
from rich.table import Table
from contextlib import contextmanager


@contextmanager
def gui(device: api.Device):
    def signals_table(signals: dict[str, api.Signal]):
        signals_table = Table(show_header=False, expand=True, box=None)
        signals_table.add_column("Signal", width=25)
        signals_table.add_column("Value", width=5)
        signals_table.add_column("Index", width=5)
        for signal in signals.values():
            if signal.values_len > 1:
                for ix, value in enumerate(signal.values):
                    signals_table.add_row(
                        signal.name, f"[{ix}]", str(value) if value is not None else "NONE"
                    )
            else:
                value = signal.values[0]
                signals_table.add_row(
                    signal.name, "", str(value) if value is not None else "NONE"
                )
        return signals_table

    def slots_table(device: api.Device):
        table = Table(show_lines=True)
        table.add_column("Slot")
        table.add_column("Inputs")
        table.add_column("Outputs")

        for slot in device.slots.values():
            table.add_row(
                slot.name, signals_table(slot.inputs), signals_table(slot.outputs)
            )

        return table

    with Live(
        get_renderable=partial(slots_table, device), refresh_per_second=4
    ):

        def _render(*, status=""):
            pass

        yield _render
