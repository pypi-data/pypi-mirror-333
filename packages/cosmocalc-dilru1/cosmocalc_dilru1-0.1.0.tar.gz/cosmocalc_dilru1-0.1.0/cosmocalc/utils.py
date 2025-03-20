# cosmocalc/utils.py

def parse_float(value):
    """Converts value to float if possible, else raises ValueError."""
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Cannot convert {value} to float.")
