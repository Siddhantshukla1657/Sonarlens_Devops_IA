"""Seeded SonarQube Bugs example. DEMO ONLY - do not reuse this code.

Every defect in this file is intentional. The bugs here are logic
defects SonarQube classifies as Bugs: they break correctness at runtime
rather than security or maintainability.
"""


def average_score(total, count):
    """BUG: division with no zero check.

    count comes straight from the caller with no guard, so count == 0
    raises ZeroDivisionError at runtime. A correct version would reject
    non-positive counts before dividing.
    """
    return total / count


def get_item(items, index):
    """BUG: off-by-one boundary check.

    The guard uses ">" where it needs ">=", so index == len(items)
    passes the check and items[index] then raises IndexError. The
    /tasks/<idx> endpoint in main.py routes through this function, so
    requesting the index one past the last task fails with a 500.
    """
    if index > len(items):
        raise IndexError("task index out of range")
    return items[index]


def print_value(value):
    """BUG: possible null dereference (SonarQube rule S2259).

    When value is None the branch below only prints a note and falls
    through, so value.upper() dereferences None and crashes. A correct
    version would return right after handling the None case.
    """
    if value is None:
        print("nothing to describe")
    print(value.upper())


def normalize_titles(titles):
    """BUG: ignored return value (SonarQube rule S2201).

    sorted() has no side effects, so calling it as a statement does
    nothing; the caller still receives the unsorted list.
    """
    sorted(titles)
    return titles
