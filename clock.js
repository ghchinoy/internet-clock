// clock.js - A simple Lit web component for displaying the current time.

import { LitElement, html, css } from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class RamsClock extends LitElement {
  // Define the component's properties.
  static properties = {
    time: { type: String },
  };

  // Define the component's styles.
  static styles = css`
    :host {
      display: block;
      font-family: Helvetica, Arial, sans-serif;
      font-size: 12rem;
      font-weight: bold;
      letter-spacing: -5px;
      color: #333;
    }
  `;

  // Initialize the component's state.
  constructor() {
    super();
    this.time = new Date().toLocaleTimeString('en-US', { hour12: false });
  }

  // Set up a timer to update the time every second when the component is added to the page.
  connectedCallback() {
    super.connectedCallback();
    this.timerID = setInterval(() => {
      this.time = new Date().toLocaleTimeString('en-US', { hour12: false });
    }, 1000);
  }

  // Clean up the timer when the component is removed from the page.
  disconnectedCallback() {
    super.disconnectedCallback();
    clearInterval(this.timerID);
  }

  // Render the component's HTML template.
  render() {
    return html`${this.time}`;
  }
}

// Define the custom element for the clock.
customElements.define('rams-clock', RamsClock);