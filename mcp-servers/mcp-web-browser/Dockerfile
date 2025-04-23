FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts and set the timezone.
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Taipei

# Updates the package lists and upgrades existing packages.
# Installs Python 3, pip, and git.
# Installs the mcp and playwright Python packages.
# Installs dependencies for Playwright.
# Installs Playwright browsers.
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3 python3-pip git \
    && pip3 install mcp playwright \
    && playwright install-deps \
    && playwright install

# Set the working directory to /usr/local/src.
WORKDIR /usr/local/src

# Clones the mcp-web-browser repository from GitHub.
RUN git clone https://github.com/random-robbie/mcp-web-browser

# Specifies the command to run when the container starts, which is the server.py script.
CMD [ "/usr/bin/python3", "/usr/local/src/mcp-web-browser/src/mcp_web_browser/server.py" ]
