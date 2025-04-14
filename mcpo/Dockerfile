# Use a Rocky Linux 9 base image
FROM rockylinux/rockylinux:9

# Update the system packages
RUN dnf -y update\
&& dnf -y install python3.11 python3.11-pip nodejs git

# Install uvx and mcpo using pip
RUN pip3.11 install uvx mcpo

# Clone the servers repository from GitHub
RUN cd /usr/local/src && git clone https://github.com/modelcontextprotocol/servers.git

# Copy the configuration file
COPY config.json /root/config.json

# Expose the 8000 TCP port
EXPOSE 8000

# Set the entrypoint to run the mcpo executable
ENTRYPOINT ["mcpo"]

# Set the default command to run mcpo with the config file
CMD ["--config", "/root/config.json"]


