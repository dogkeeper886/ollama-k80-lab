# ===== Stage 1: Build the source code =====
FROM dogkeeper886/ollama37-builder AS builder

# Copy source code and build
RUN cd /usr/local/src \
    && git clone https://github.com/dogkeeper886/ollama37 \
    && cd ollama37 \
    && CC=/usr/local/bin/gcc CXX=/usr/local/bin/g++ cmake -B build \
    && CC=/usr/local/bin/gcc CXX=/usr/local/bin/g++ cmake --build build \
    && go build -o ollama .

# ===== Stage 2: Runtime image =====
FROM rockylinux/rockylinux:9

# Copy only the built binary and any needed assets from the builder stage
COPY --from=builder /usr/local/src/ollama37 /usr/local/src/ollama37

# Set environment variables
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV NVIDIA_VISIBLE_DEVICES=all
ENV OLLAMA_HOST=0.0.0.0:11434

# Expose port
EXPOSE 11434

# Set entrypoint and command
ENTRYPOINT ["/usr/local/src/ollama37/ollama"]
CMD ["serve"]
