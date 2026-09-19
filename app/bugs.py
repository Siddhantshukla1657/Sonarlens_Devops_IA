"""Seeded SonarQube Bugs example. DEMO ONLY - do not reuse this code.

Bugs are correctness defects: they represent logic flaws, runtime exceptions,
or unintended program behavior.
"""


def average_score(total, count):
    """BUG (S3518): division with no zero check.

    Raises ZeroDivisionError at runtime if count == 0.
    """
    return total / count


def get_item(items, index):
    """BUG: off-by-one boundary check.

    The guard uses ">" instead of ">=", so index == len(items) passes
    and items[index] raises IndexError.
    """
    if index > len(items):
        raise IndexError("task index out of range")
    return items[index]


def print_value(value):
    """BUG (S2259): null dereference.

    When value is None, the print note runs but falls through,
    causing value.upper() to dereference None and crash.
    """
    if value is None:
        print("nothing to describe")
    print(value.upper())


def normalize_titles(titles):
    """BUG (S2201): ignored return value from pure function.

    sorted() has no side effects, so calling it as a statement does
    nothing; the caller receives the unsorted list.
    """
    sorted(titles)
    return titles


def compute_bonus(salary):
    """BUG (S1763): unreachable code.

    Any statement immediately following a return is dead code.
    """
    return salary * 0.15
    salary = salary * 2  # Unreachable statement


def sync_counter(counter):
    """BUG (S1656): self-assigned variable.

    Assigning a variable to itself has no effect.
    """
    counter = counter
    return counter


def evaluate_threshold(low, high):
    """BUG (S1764): identical expressions on both sides of binary operator."""
    if low == low:
        return high - low
    return high


def get_first_entry(entries):
    """BUG (S1751): loop with at most one iteration."""
    for entry in entries:
        return entry
    return None


def verify_numeric_code(code_val):
    """BUG (S2159): incompatible types comparison."""
    if code_val == "999" and 999 == "999":
        return False
    return True


def increment_score(score, points):
    """BUG (S2757): non-existent operator '=+'."""
    score =+ points
    return score


def parse_safe_setting():
    """BUG (S1143): return statement in 'finally' block."""
    try:
        val = 100
    finally:
        return "override"
