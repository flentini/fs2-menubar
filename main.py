"""FreeStyle Libre 2+ macOS menu bar app."""

import os
import threading

import rumps
from dotenv import load_dotenv

from libre import create_client, fetch_latest, GlucoseReading

load_dotenv()

POLL_INTERVAL = 60  # seconds


class GlucoseApp(rumps.App):
    def __init__(self):
        super().__init__("--", quit_button=None)

        self.last_update_item = rumps.MenuItem("Last update: --")
        self.last_update_item.set_callback(None)
        self.status_item = rumps.MenuItem("")
        self.status_item.set_callback(None)
        self.status_item.hide()

        self.menu = [
            self.last_update_item,
            self.status_item,
            None,  # separator
            rumps.MenuItem("Refresh Now", callback=self.on_refresh),
            None,  # separator
            rumps.MenuItem("Quit", callback=rumps.quit_application),
        ]

        self.client = None
        self._notified_high = False
        self._notified_low = False

    def _init_client(self):
        email = os.getenv("LIBRE_USERNAME")
        password = os.getenv("LIBRE_PASSWORD")
        if not email or not password:
            rumps.alert(
                "Missing credentials",
                "Set LIBRE_USERNAME and LIBRE_PASSWORD in .env",
            )
            rumps.quit_application()
            return
        try:
            self.client = create_client(email, password)
        except Exception as e:
            self.title = "⚠ --"
            self.last_update_item.title = f"Auth error: {e}"

    def _update_display(self, reading: GlucoseReading):
        self.title = f"{reading.value} {reading.trend_arrow}"
        self.last_update_item.title = (
            f"Last update: {reading.timestamp.strftime('%H:%M')}"
        )

        if reading.is_high:
            self.status_item.title = "⚠ HIGH"
            self.status_item.show()
        elif reading.is_low:
            self.status_item.title = "⚠ LOW"
            self.status_item.show()
        else:
            self.status_item.hide()

        # Notifications for high/low, once per episode
        if reading.is_high and not self._notified_high:
            rumps.notification(
                "High Glucose",
                f"{reading.value} mg/dL",
                f"Glucose is high ({reading.value} {reading.trend_arrow})",
            )
            self._notified_high = True
        elif not reading.is_high:
            self._notified_high = False

        if reading.is_low and not self._notified_low:
            rumps.notification(
                "Low Glucose",
                f"{reading.value} mg/dL",
                f"Glucose is low ({reading.value} {reading.trend_arrow})",
            )
            self._notified_low = True
        elif not reading.is_low:
            self._notified_low = False

    def _do_fetch(self):
        if self.client is None:
            return
        try:
            reading = fetch_latest(self.client)
            self._update_display(reading)
        except Exception as e:
            self.title = "⚠ --"
            self.last_update_item.title = f"Error: {e}"

    @rumps.timer(POLL_INTERVAL)
    def poll(self, _):
        threading.Thread(target=self._do_fetch, daemon=True).start()

    def on_refresh(self, _):
        threading.Thread(target=self._do_fetch, daemon=True).start()

    @rumps.events.before_start
    def setup(self):
        self._init_client()


if __name__ == "__main__":
    GlucoseApp().run()
