# Dieter Rams-Inspired Internet Radio Clock

This project is a web-based clock and internet radio player with a minimalist design inspired by the industrial designer Dieter Rams. It is built using the [Mesop](https://google.github.io/mesop/) Python framework and demonstrates how to integrate custom web components for rich, interactive user experiences.

## Features

*   **Real-time Clock:** A large, clear digital clock that updates every second.
*   **Internet Radio Player:** A simple interface to play pre-defined and custom internet radio streams.
*   **Custom Stream Support:** Add your own radio stations by providing a name and a stream URL.
*   **Minimalist Design:** A clean, uncluttered interface inspired by the design principles of Dieter Rams.

## How to Run

1.  **Install Dependencies:** Make sure you have Python and `uv` installed. Then, install the project dependencies:

    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Run the Application:** Start the Mesop development server:

    ```bash
    mesop main.py
    ```

3.  **Open in Browser:** Open your web browser and navigate to the URL provided in the terminal (usually `http://localhost:32123`).

## Architecture

This application is built with a combination of Python and JavaScript, leveraging the strengths of each for a robust and interactive experience.

### Mesop (Python)

The core application logic, state management, and UI layout are all handled by the Mesop framework in Python (`main.py`). Mesop allows for a declarative, component-based approach to building web UIs entirely in Python.

### Web Components (JavaScript)

For features that require real-time, client-side updates or specialized browser APIs, we use custom web components built with the [Lit](https://lit.dev/) library.

*   **`clock.js`:** This component (`<rams-clock>`) displays the current time and uses JavaScript's `setInterval` to update itself every second. This is more efficient than sending updates from the Python server for every tick of the clock.

*   **`smart_player.js`:** This component (`<smart-player>`) is responsible for playing the audio streams. It's a "smart" player because it can handle both HLS streams (like `.m3u8`) and direct audio streams (like `.mp3` and `.aac`). It uses the `hls.js` library to handle HLS streams and falls back to the native HTML `<audio>` element for direct streams.

This hybrid approach allows us to build a powerful, interactive application while keeping the Python code clean and focused on the core application logic.


# Disclaimer

This is not an official or supported Google project.

