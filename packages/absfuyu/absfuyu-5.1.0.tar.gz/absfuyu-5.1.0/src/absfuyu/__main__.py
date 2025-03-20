"""
ABSFUYU
-------
COMMAND LINE INTERFACE

Version: 5.1.0
Date updated: 10/03/2025 (dd/mm/yyyy)
"""

# Library
# ---------------------------------------------------------------------------
try:
    from absfuyu.cli import cli
except ModuleNotFoundError:  # Check for `click`, `colorama`
    from absfuyu.core.dummy_cli import cli


# Function
# ---------------------------------------------------------------------------
def main() -> None:
    cli()


# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
