FROM python:3.11-slim

LABEL org.opencontainers.image.title="sovereign-xml-compiler"
LABEL org.opencontainers.image.description="XML→SVG compiler and constraint graph pipeline"
LABEL org.opencontainers.image.authors="Ahmad Ali Parr × SnapKitty"
LABEL org.opencontainers.image.source="https://github.com/SNAPKITTYWEST/sovereign-xml-compiler"

WORKDIR /app
COPY . .

# Run tests to verify the image is healthy
RUN python test_compilers.py

# Default: serve the browser UI
EXPOSE 8000
CMD ["python", "-m", "http.server", "8000", "--directory", "."]
