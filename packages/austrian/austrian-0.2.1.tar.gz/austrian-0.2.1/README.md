# Austrian 
Ідея і стартова реалізація завдячує роботі `d3m0`.

Бібліотека для перетворення повнотекстової назви або коментаря до об'єкта на код sidc стандарту app6d

## Як працювати зараз?

Запускає
```
from austrian import UnitDesignator

UnitDesignator.calculate_icon("танк")
//'30062000001103000000'
```        

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management.

### Installation

1. Install Poetry (if not already installed):
   ```
   pip install poetry
   ```

2. Install dependencies:
   ```
   poetry install
   ```

3. Activate the virtual environment:
   ```
   poetry shell
   ```

### Testing

Run tests with pytest:
```
poetry run pytest
```

### CI/CD

This project uses GitHub Actions for continuous integration and deployment. The workflow:

1. Runs tests on pull requests and pushes to main and develop branches
2. When manually triggered with a version number, builds and publishes the package to PyPI        