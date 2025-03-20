# OpenAI WebSearch MCP Servr

This MCP server provides access to OpenAI's websearch functionality through the Model Context Protocol. It allows AI assistants to search the web during conversations with users, providing up-to-date information that may not be available in the assistant's training data. The server can be installed and configured for use with Claude.app or Zed editor.

### Available Tools

- `web_search` - Call openai websearch as tool.
  - Required arguments:
    - `type` (string): web_search_preview
    - `search_context_size` (string): High level guidance for the amount of context window space to use for the search. One of low, medium, or high. medium is the default.
    - `user_location` (object or null)
      - `type` (string): The type of location > approximation. Always approximate.
      - `city` (string): Free text input for the city of the user, e.g. San Francisco.
      - `country` (string): The two-letter ISO country code of the user, e.g. US.
      - `region` (string): Free text input for the region of the user, e.g. California.
      - `timezone` (string): The IANA timezone of the user, e.g. America/Los_Angeles.

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *openai-websearch-mcp*.

### Using PIP

Alternatively you can install `openai-websearch-mcp` via pip:

```bash
pip install openai-websearch-mcp
```

After installation, you can run it as a script using:

```bash
python -m openai-websearch-mcp
```

## Configuration

### Configure for Claude.app

!!!can using command auto update configure file
```bash
uv run --with openai-websearch-mcp openai-websearch-mcp-install
```

Add to your Claude settings:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "openai-websearch-mcp": {
    "command": "uvx",
    "args": ["openai-websearch-mcp"],
    "env": {
        "OPENAI_API_KEY": "your-api-key-here"
    }
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "openai-websearch-mcp": {
    "command": "python",
    "args": ["-m", "openai_websearch_mcp"],
    "env": {
        "OPENAI_API_KEY": "your-api-key-here"
    }
  }
}
```
</details>

### Configure for Zed

Add to your Zed settings.json:

<details>
<summary>Using uvx</summary>

```json
"context_servers": [
  "openai-websearch-mcp": {
    "command": "uvx",
    "args": ["openai-websearch-mcp"],
    "env": {
        "OPENAI_API_KEY": "your-api-key-here"
    }
  }
],
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"context_servers": {
  "openai-websearch-mcp": {
    "command": "python",
    "args": ["-m", "openai_websearch_mcp"],
    "env": {
        "OPENAI_API_KEY": "your-api-key-here"
    }
  }
},
```
</details>


## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```bash
npx @modelcontextprotocol/inspector uvx openai-websearch-mcp
```
