# Code instructions

Use Mesop, which can be found at https://github.com/mesop-dev/mesop or https://mesop-dev.github.io/mesop/, but also in the virtual environment library .venv/lib/python3.13/site-packages/mesop

## Mesop

### Code Style

*   **Comments:** Add clear and concise comments to your code to explain the purpose of functions, classes, and complex logic. This is especially important for web components and their interaction with the main Python application.

### Styling

* Styling properties like `margin` and `padding` don't accept simple string values (e.g., `"10px"`). Instead, you must use the dedicated Mesop styling objects like `me.Margin` and `me.Padding`. For example, to set a bottom margin, use `me.Style(margin=me.Margin(bottom=10))`.

### Asynchronous Operations and State Updates

* For components that need to update continuously (like a clock), the main page function (`@me.page`) must be defined as an `async` generator.
* Inside the `async` page function, you must `yield` at least once to render the initial UI before entering an infinite loop for updates.
* The `on_load` event handler is not suitable for long-running, continuously updating tasks. It should be used for initial setup and one-time actions when the page loads.

### Content Security Policy (CSP)

* If you encounter a blank page and see Content Security Policy errors in the browser console, you may need to adjust the security policy for the page. This can be done by setting the `security_policy` argument in the `@me.page` decorator. For example:

```python
@me.page(
    security_policy=me.SecurityPolicy(
        dangerously_disable_trusted_types=True
    )
)
```

*   **Connecting to External Resources (CORS):** If your application needs to connect to external domains (e.g., for streaming audio), you must explicitly allow them in the `SecurityPolicy`. Use the `allowed_connect_srcs` argument to provide a list of allowed domains.

    ```python
    @me.page(
        security_policy=me.SecurityPolicy(
            allowed_connect_srcs=[
                "'self'",
                "https://some-streaming-service.com",
            ]
        )
    )
    ```

### Web Components

*   **Defining a Web Component:** To create a web component, use the `@me.web_component` decorator on a Python function. This function should return a `me.insert_web_component` call.

    ```python
    @me.web_component(path="./my_component.js")
    def my_component(my_property: str):
      return me.insert_web_component(
        name="my-component-name",
        properties={
          "myProperty": my_property,
        },
      )
    ```

*   **Using a Web Component:** To use a web component in your page, simply call the decorated Python function.

    ```python
    import mesop as me

    @me.page(...)
    def my_page():
      my_component(my_property="hello")
    ```

*   **Security:** Mesop has a security feature that prevents you from directly setting the `src` property on a web component. If you need to pass a URL to a component, use a different property name (e.g., `stream_url`).

*   **Event Handlers:** Use `on_click` for click events, not `onclick`.

*   **Importing JavaScript Modules:** When using a JavaScript library (like `hls.js`) in your web component, make sure to import the module-compatible version. For libraries on CDNs, this often means pointing to a specific file, like `.../dist/hls.mjs`, instead of the main package URL.

    ```javascript
    // Incorrect:
    import Hls from 'https://cdn.jsdelivr.net/npm/hls.js@latest';

    // Correct:
    import Hls from 'https://cdn.jsdelivr.net/npm/hls.js@latest/dist/hls.mjs';
    ```

*   **Debugging External Data Sources:** When working with external data sources like streaming URLs, be aware that they can be unreliable and change without notice. If a stream is not working, use your browser's developer tools to check for network errors (like 404s or CORS issues) and use a web search to find alternative, more reliable URLs.