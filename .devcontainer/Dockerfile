# Uses Microsoft's Python devcontainer base (has user "vscode" and Python preinstalled)
FROM mcr.microsoft.com/devcontainers/python:3.11

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Optional: set up a venv and install tools
# RUN python -m venv /workspace/.venv && \
#     /workspace/.venv/bin/pip install --upgrade pip black

# Ensure the default PATH finds python at /usr/local/bin/python in this image
