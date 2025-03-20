# RTQL8

Python library for cron parsing and description generation.

## Installation

```bash
pip install rtql8
```

## Development Installation

```bash
poetry install
```

## Usage

```python
from rtql8 import Cron

cron = Cron("* * * * *")
print(cron.description)
```

## Usage for CLI

```bash
rtql8 -e "* * * * *"

# Output
Every minute
```

Another way is using `poetry run`:

```bash
poetry run rtql8 -e "0 0 1,15 * ?"

# Output
At midnight, on 1st and 15th of the month
```

## Testing

```bash
poetry run pytest
```

or run specific test case, for example, `test_cli.py` in `test_cron.py`:

```bash
poetry run pytest tests/test_cli.py
```

or

```bash
poetry run pytest tests/test_cron.py
```

## License

MIT
