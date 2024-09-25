#!/usr/bin/python3
import asyncio
import logging
from typing import List

from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    Footer,
    Button,
    Select,
    Static,
    Label,
    RichLog,
    Input,
)
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.events import Key

# Import your existing modules
from config import (
    username,
    client_id,
    client_secret,
    app_redirect,
    scope,
    cached_token,
    target_devices,
)
import spotipy
import nullspot
import datetime
import time
import threading
import signal

from songs import Song
from cars import Car

from songs.turnallthelightson import turnallthelightson
from songs.caramelldansen import caramelldansen
from songs.unite import unite
from songs.europapa import europapa

from cars.corsa import corsa
from cars.kiacarens import kiacarens
from cars.corsastub import corsastub
from cars.nullcar import nullcar

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__).setLevel(logging.DEBUG)
logging.getLogger("songs").setLevel(logging.DEBUG)
logging.getLogger("cars").setLevel(logging.DEBUG)

LOG = logging.getLogger(__name__)


class LightShowApp(App):
    CSS_PATH = "app.css"  # You can define styles in this CSS file
    started = reactive(False)
    song_thread : threading.Thread = None
    car : Car | None = None
    song : Song | None = None
    sp = None
    token = None
    stop_event = threading.Event()
    song_offset = "00:00.000"
    foobar = None
    target_device_id = None

    def compose(self) -> ComposeResult:
        """Compose the UI elements."""
        yield Header()
        yield Footer()

        # Create selection widgets
        self.song_select = Select(
            options=[(c.__name__, c.__name__) for c in Song.__subclasses__()],
            name="song_select",
            prompt="Select a song",
        )
        self.car_select = Select(
            options=[(c.__name__, c.__name__) for c in Car.__subclasses__()],
            name="car_select",
            prompt="Select a car",
        )
        self.device_select = Select(
            options=[(name, name) for name in list(target_devices.keys()) + ["nullspot"]],
            name="device_select",
            prompt="Select a Spotify device",
        )
        self.start_button = Button("Start Light Show", name="start_button")
        self.stop_button = Button("Stop Light Show", name="stop_button", disabled=True)
        self.status_label = Label("Welcome to the Light Show App!", name="status_label")

        # Horizontal container for start/stop buttons
        button_container = Horizontal(self.start_button, self.stop_button, id="button_container")

        # VerticalScroll for options with scrolling support
        controls = VerticalScroll(
            Vertical(
                self.song_select,
                self.car_select,
                self.device_select,
                button_container,
                self.status_label,
                id="controls",
            ),
        )

        self.rich_log = RichLog(highlight=True, markup=True, id="log")

        # Add widgets to the app
        yield Container(controls, self.rich_log)

    async def on_mount(self) -> None:
        """Called when the app is mounted."""
        await self.initialize_app()

    async def initialize_app(self):
        """Initialize Spotify connection."""
        self.log_message("Initializing Spotify connection...")
        try:
            self.token = spotipy.util.prompt_for_user_token(
                username,
                scope,
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=app_redirect,
            )
        except Exception as ex:
            LOG.info("Unable to fetch new Spotify token. Using cached token")
            self.token = cached_token

        LOG.debug(f"Used Spotify token: {self.token}")

    def log_message(self, message: str):
        """Log a message to the RichLog widget."""
        LOG.info(message)
        self.rich_log.write(message)

    async def action_start_light_show(self):
        """Start the light show."""
        song_name = self.song_select.value
        car_name = self.car_select.value
        device_name = self.device_select.value

        self.log_message(f"Selected song: {song_name}")
        self.log_message(f"Selected car: {car_name}")
        self.log_message(f"Selected device: {device_name}")

        # Initialize car
        for c in Car.__subclasses__():
            if c.__name__ == car_name:
                self.car = c()
                self.log_message(f"Initialized car: {car_name}")

        # Initialize song
        for s in Song.__subclasses__():
            if s.__name__ == song_name:
                self.song = s(self.car)
                self.log_message(f"Initialized song: {song_name}")

        # Initialize Spotify device
        if device_name == "nullspot":
            self.sp = nullspot
        else:
            self.target_device_id = target_devices[device_name]
            self.sp = None
            while self.sp is None:
                try:
                    self.sp = spotipy.Spotify(auth=self.token)
                    self.sp.current_user()
                except spotipy.exceptions.SpotifyException:
                    self.log_message("Unable to authenticate to Spotify")
                    self.token = input("Please input a valid Spotify auth token:")
                    self.sp = None

            self.log_message(f"Waiting for Spotify device {device_name} to appear...")
            device_found = False
            while not device_found:
                for device in self.sp.devices()["devices"]:
                    LOG.debug(device)
                    if device["id"] == self.target_device_id:
                        device_found = True
                        break
                time.sleep(0.5)
            self.log_message("Spotify device found.")

        # Start the car
        self.car.start()
        self.log_message("Car started.")

        # Start the song and light show in a separate thread
        self.started = True
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.status_label.update("Light show is running...")

        self.song_thread = threading.Thread(target=self.run_light_show)
        self.song_thread.start()

    def run_light_show(self):
        """Run the light show."""
        self.foobar = datetime.datetime.now()
        self.print_timestamp()

        self.log_message("Waiting for the song to finish...")

        self.song.start(self.sp, self.target_device_id, offset=self.song_offset)
        time.sleep(1)
        while self.song.wait(timeout=1):
            if not self.started:
                self.log_message("Stopping light show prematurely.")
                self.song.stop()
                break
        time.sleep(0.5)
        self.started = False
        self.log_message("Light show finished.")
        self.song.stop()
        self.car.stop()
        self.status_label.update("Light show stopped.")
        self.start_button.disabled = False
        self.stop_button.disabled = True

    def print_timestamp(self):
        """Print the current timestamp."""
        time_passed = (
            datetime.datetime.now() - self.foobar
        ) + datetime.timedelta(
            minutes=int(self.song_offset.split(":")[0]),
            seconds=float(self.song_offset.split(":")[1]),
        )
        minutes, seconds = divmod(time_passed.total_seconds(), 60)
        self.log_message(
            "{minutes:02d}:{seconds:06.3f} - Light show started.".format(
                minutes=int(minutes), seconds=seconds
            )
        )

    async def action_stop_light_show(self):
        """Stop the light show."""
        if self.started:
            self.started = False
            self.status_label.update("Stopping light show...")
            self.log_message("Stopping light show...")
            self.song.stop()
            self.car.stop()
            if self.song_thread and self.song_thread.is_alive():
                self.song_thread.join()
            self.status_label.update("Light show stopped.")
            self.start_button.disabled = False
            self.stop_button.disabled = True

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_name = event.button.name
        if button_name == "start_button":
            await self.action_start_light_show()
        elif button_name == "stop_button":
            await self.action_stop_light_show()

    async def on_key(self, event: Key) -> None:
        """Handle key presses."""
        if event.key == "ctrl+c":
            await self.action_stop_light_show()
            self.exit()

    def on_unmount(self) -> None:
        """Handle app exit."""
        if self.started:
            self.started = False
            self.song.stop()
            self.car.stop()
            if self.song_thread and self.song_thread.is_alive():
                self.song_thread.join()
            self.log_message("Application exited.")

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    def action_reset(self) -> None:
        """Reset the application to select new options."""
        self.song_select.value = None
        self.car_select.value = None
        self.device_select.value = None
        self.status_label.update("Welcome to the Light Show App!")
        self.rich_log.clear()
        self.log_message("Application reset.")

    async def action_reload(self) -> None:
        """Reload the application."""
        await self.action_stop_light_show()
        await self.initialize_app()
        self.log_message("Application reloaded.")


if __name__ == "__main__":
    LightShowApp().run()
