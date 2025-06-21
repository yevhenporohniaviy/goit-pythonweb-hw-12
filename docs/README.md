# Documentation

This directory contains the Sphinx documentation for the Contacts API.

## Building the Documentation

To build the documentation, you can use Docker:

```bash
# Build HTML documentation
docker-compose run --rm app sphinx-build -b html docs/source docs/build/html

# Or use make (if available)
docker-compose run --rm app make -C docs html
```

## Viewing the Documentation

After building, you can view the documentation by opening `docs/build/html/index.html` in your browser.

## Structure

- `source/` - Source files for the documentation
- `build/` - Built documentation (generated)
- `source/conf.py` - Sphinx configuration
- `source/index.rst` - Main documentation page
- `source/api.rst` - API documentation
- `source/models.rst` - Database models documentation
- `source/services.rst` - Services documentation
- `source/core.rst` - Core modules documentation

## Adding Documentation

To add documentation for new modules:

1. Add docstrings to your Python functions and classes
2. Update the appropriate `.rst` file in `source/`
3. Rebuild the documentation
