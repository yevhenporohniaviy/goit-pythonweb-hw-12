#!/bin/bash

# Build Sphinx documentation
echo "Building Sphinx documentation..."

# Create build directory if it doesn't exist
mkdir -p docs/build

# Build HTML documentation
sphinx-build -b html docs/source docs/build/html

echo "Documentation built successfully!"
echo "You can view it by opening docs/build/html/index.html in your browser." 