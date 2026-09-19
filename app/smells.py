"""Seeded SonarQube Code Smells example. DEMO ONLY - do not reuse this code.

Code smells hurt maintainability and readability without necessarily breaking
runtime execution.
"""


def generate_report(title, author, recipient, priority, status, due_date, category, summary, notes):
    """SMELL (S107): excessive number of parameters."""
    return {
        "title": title,
        "author": author,
        "recipient": recipient,
        "priority": priority,
        "status": status,
        "due_date": due_date,
        "category": category,
        "summary": summary,
        "notes": notes,
    }


def classify_reading(temperature, pressure, humidity):
    """SMELL (S1066): nested if statements that should be merged."""
    if temperature is not None:
        if pressure is not None:
            if humidity is not None:
                if temperature > 30:
                    if pressure > 1000:
                        return "hot and high pressure"
                return "nominal"
    return "incomplete reading"


def audit_task(task, unused_context):
    """SMELL (S1854, S1481, S1172): dead stores and unused variables."""
    # S1854: initial assignment is immediately overwritten
    label = "unknown"
    # S1481: unused local variable
    unused_temporary_cache = {"timestamp": 12345}

    if task.get("priority") == "high":
        label = "escalated"
    else:
        label = "standard"
    return label


def plan_feature():
    """SMELL (S1135, S1134): TODO and FIXME tags."""
    # TODO: Implement asynchronous queue processing here
    # FIXME: Address memory consumption issue during batch processing
    return True


class TaskScribe:
    """SMELL (S1144): unused private method."""

    def __init__(self, name):
        self.name = name

    def __unused_private_helper(self):
        """S1144: class-private method never invoked."""
        return "never called"

    def format_title(self, title):
        return title.strip()
