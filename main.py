# main.py - The core of the Dieter Rams-inspired Internet Radio Clock

import mesop as me

# A dictionary of pre-defined radio stations.
# Note: These URLs can be unreliable and may change without notice.
RADIO_STATIONS = {
    "WNYC": "https://am820.wnyc.org/wnycam-mp3",
    "KCRW": "https://streams.kcrw.com/kcrw_mp3",
    "BBC Radio 1": "http://as-hls-ww-live.akamaized.net/pool_01505109/live/ww/bbc_radio_one/bbc_radio_one.isml/bbc_radio_one-audio%3d96000.norewind.m3u8",
}

# Defines the clock web component, linking it to the clock.js file.
@me.web_component(path="./clock.js")
def clock_component():
  """Inserts the rams-clock web component into the page."""
  return me.insert_web_component(name="rams-clock")

# Defines the smart audio player web component, linking it to the smart_player.js file.
@me.web_component(path="./smart_player.js")
def smart_player_component(stream_url: str, playing: bool):
  """Inserts the smart-player web component into the page."""
  return me.insert_web_component(
    name="smart-player",
    properties={
      "stream_url": stream_url,
      "playing": playing,
    },
  )

# Defines the application's state.
# This class holds all the data that can change over time.
@me.stateclass
class State:
    selected_station: str
    is_playing: bool
    custom_station_name: str
    custom_station_url: str
    custom_stations: dict[str, str]

# Event handler for the play/pause button.
def play_pause(e: me.ClickEvent):
    """Toggles the play/pause state of the radio."""
    state = me.state(State)
    state.is_playing = not state.is_playing
    yield

# Event handler for selecting a radio station.
def select_station(e: me.ClickEvent):
    """Changes the selected radio station."""
    state = me.state(State)
    state.selected_station = e.key
    state.is_playing = True  # Auto-play when a new station is selected
    yield

def on_custom_station_name_input(e: me.InputEvent):
    """Updates the custom station name in the state."""
    state = me.state(State)
    state.custom_station_name = e.value
    yield

def on_custom_station_url_input(e: me.InputEvent):
    """Updates the custom station URL in the state."""
    state = me.state(State)
    state.custom_station_url = e.value
    yield

def on_add_custom_station(e: me.ClickEvent):
    """Adds a new custom station to the list."""
    state = me.state(State)
    if state.custom_station_name and state.custom_station_url:
        state.custom_stations[state.custom_station_name] = state.custom_station_url
        state.custom_station_name = ""
        state.custom_station_url = ""
        yield


# Defines the main page of the application.
@me.page(
    title="Internet Radio Clock",
    # The security policy is crucial for allowing the app to connect to external
    # streaming URLs and load scripts from CDNs.
    security_policy=me.SecurityPolicy(
        dangerously_disable_trusted_types=True,
        allowed_script_srcs=["https://cdn.jsdelivr.net"],
        allowed_connect_srcs=[
            "'self'",
            "https://am820.wnyc.org",
            "https://streams.kcrw.com",
            "http://as-hls-ww-live.akamaized.net",
        ],
    ),
)
def page():
    """Renders the main page of the application."""
    state = me.state(State)
    # Initialize the state on the first load.
    if state.selected_station is None:
        state.selected_station = "WNYC"
        state.is_playing = False

    # Main container for the entire application.
    with me.box(style=main_container_style()):
        # Display the clock component.
        clock_component()

        # Container for the radio player UI.
        with me.box(style=radio_container_style()):
            me.text("Radio", style=radio_title_style())
            # Iterate over the pre-defined stations and create a button for each.
            for station_name, stream_url in RADIO_STATIONS.items():
                with me.box(
                    key=station_name,
                    on_click=select_station,
                    style=radio_station_style(
                        is_selected=state.selected_station == station_name
                    ),
                ):
                    me.text(station_name)
            # Iterate over the custom stations and create a button for each.
            for station_name, stream_url in state.custom_stations.items():
                with me.box(
                    key=station_name,
                    on_click=select_station,
                    style=radio_station_style(
                        is_selected=state.selected_station == station_name
                    ),
                ):
                    me.text(station_name)

            # UI for the play/pause button and the "Now Playing" text.
            with me.box(style=controls_style()):
                me.button(
                    "Pause" if state.is_playing else "Play",
                    on_click=play_pause,
                    type="flat",
                )
            if state.is_playing:
                me.text(f"Now Playing: {state.selected_station}", style=now_playing_style())

            # Form for adding a new custom station.
            with me.box(style=custom_station_form_style()):
                me.input(
                    label="Station Name",
                    on_input=on_custom_station_name_input,
                    style=me.Style(width="100%"),
                )
                me.input(
                    label="Stream URL",
                    on_input=on_custom_station_url_input,
                    style=me.Style(width="100%"),
                )
                me.button(
                    "Add Station",
                    on_click=on_add_custom_station,
                    type="flat",
                )

        # The smart player component is only added to the page when a station is playing.
        if state.is_playing:
            all_stations = {**RADIO_STATIONS, **state.custom_stations}
            smart_player_component(
                stream_url=all_stations[state.selected_station],
                playing=state.is_playing,
            )

# The following functions define the styling for the different UI elements.

def main_container_style():
    return me.Style(
        background="#f0f0f0",
        color="#333",
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
        height="100vh",
        font_family="Helvetica, Arial, sans-serif",
    )

def radio_container_style():
    return me.Style(
        margin=me.Margin(top=40),
        padding=me.Padding.all(20),
        border=me.Border.all(me.BorderSide(width=1, style="solid", color="#ccc")),
        border_radius=10,
        background="#e0e0e0",
        width=300,
    )

def radio_title_style():
    return me.Style(
        font_size="1.5rem",
        font_weight="bold",
        margin=me.Margin(bottom=10),
    )

def radio_station_style(is_selected: bool):
    style = me.Style(
        padding=me.Padding.all(10),
        cursor="pointer",
        border_radius=5,
        margin=me.Margin(bottom=5),
    )
    if is_selected:
        style.background = "#ffde00"  # Muted yellow accent
        style.color = "#000"
    return style

def controls_style():
    return me.Style(
        margin=me.Margin(top=20),
        display="flex",
        justify_content="center",
    )

def now_playing_style():
    return me.Style(
        margin=me.Margin(top=10),
        font_size="0.8rem",
        color="#666",
    )

def custom_station_form_style():
    return me.Style(
        margin=me.Margin(top=20),
        display="flex",
        flex_direction="column",
        gap=10,
    )