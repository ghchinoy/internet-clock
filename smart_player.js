// smart_player.js - A Lit web component that can play both HLS and direct audio streams.

import { LitElement, html } from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';
import Hls from 'https://cdn.jsdelivr.net/npm/hls.js@latest/dist/hls.mjs';

class SmartPlayer extends LitElement {
  // Define the component's properties.
  static properties = {
    stream_url: { type: String },
    playing: { type: Boolean },
  };

  // Initialize the component's state and the HLS.js instance.
  constructor() {
    super();
    this.playing = false;
    this.hls = new Hls();
  }

  // This function is called whenever the component's properties change.
  updated(changedProperties) {
    // If the stream URL has changed, load the new stream.
    if (changedProperties.has('stream_url')) {
      this.loadStream();
    }
    // If the playing state has changed, toggle the audio playback.
    if (changedProperties.has('playing')) {
      this.togglePlay();
    }
  }

  // This function determines whether to use HLS.js or the native audio element.
  loadStream() {
    const audio = this.shadowRoot.querySelector('audio');
    const streamUrl = this.stream_url;

    // If the stream URL ends with .m3u8, use HLS.js.
    if (streamUrl.endsWith('.m3u8')) {
      if (Hls.isSupported()) {
        console.log('HLS stream detected. Loading with hls.js:', streamUrl);
        this.hls.loadSource(streamUrl);
        this.hls.attachMedia(audio);
      } else {
        console.error('HLS is not supported in this browser.');
      }
    } else {
      // Otherwise, use the native audio element.
      console.log('Direct stream detected. Loading with native audio:', streamUrl);
      audio.src = streamUrl;
    }
  }

  // This function plays or pauses the audio.
  togglePlay() {
    const audio = this.shadowRoot.querySelector('audio');
    if (this.playing) {
      console.log('Playing audio');
      audio.play().catch(e => console.error('Error playing audio:', e));
    } else {
      console.log('Pausing audio');
      audio.pause();
    }
  }

  // Render the component's HTML template.
  render() {
    return html`<audio controls></audio>`;
  }
}

// Define the custom element for the smart player.
customElements.define('smart-player', SmartPlayer);