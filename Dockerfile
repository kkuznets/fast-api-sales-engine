FROM ghcr.io/astral-sh/uv:0.5.26-python3.13-bookworm

# Copy the project into the image
ADD . /code

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /code
RUN uv sync --frozen

# Expose the port the app runs on
EXPOSE 8000