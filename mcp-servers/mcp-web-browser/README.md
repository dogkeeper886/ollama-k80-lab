
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
    - mcp-web-browser
    - /usr/bin/python3
    - /usr/local/src/mcp-web-browser/src/mcp_web_browser/server.py
```

## Additional Notes

## Contributing

Contributions to this project are welcome! Please refer to the contributing guidelines in the repository for more information on how you can get involved.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

