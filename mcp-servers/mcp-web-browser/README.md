
# MCP Web Browser Docker Container

This Docker container sets up an environment to run the `mcp-web-browser` application, which is designed to extract information from web pages using Playwright and other Python libraries.

## Getting Started

### Prerequisites

- Docker installed on your machine.

### Usage

For the MCP server setup using Visual Studio Code's Continue plugin.

```yml
mcpServers:
  - name: mcp-web-browser
    command: docker
    args:
    - run
    - -i
    - --rm
    - dogkeeper886/mcp-web-browser:latest
    - /usr/bin/python3
    - /usr/local/src/mcp-web-browser/src/mcp_web_browser/server.py
```

## Contributing

Contributions to this project are welcome! If you have any issues or would like to contribute, please feel free to open an issue on the [GitHub repository](https://github.com/dogkeeper886/mcp-web-browser).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

