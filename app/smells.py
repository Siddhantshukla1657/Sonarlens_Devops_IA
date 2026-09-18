"""Seeded SonarQube Code Smells example. DEMO ONLY - do not reuse this code.

Code smells hurt maintainability, not correctness. None of the issues
below affect runtime behavior; that is the point of the demonstration.
"""


def generate_report(title, author, recipient, priority, status, due_date, category, summary):
    """SMELL: too many parameters (SonarQube rule S107).

    SonarQube's default maximum is 7; this function takes 8. A real
    refactor would bundle the fields into a dataclass or dict.
    """
    return {
        "title": title,
        "author": author,
        "recipient": recipient,
        "priority": priority,
        "status": status,
        "due_date": due_date,
        "category": category,
        "summary": summary,
    }


def classify_reading(temperature, pressure, humidity):
    """SMELL: deeply nested conditionals (SonarQube rule S3776).

    Nesting reaches four levels. Guard clauses that return early would
    flatten this into a single readable level.
    """
    if temperature is not None:
        if pressure is not None:
            if humidity is not None:
                if temperature > 30 and pressure > 1000:
                    return "hot and high pressure"
                return "nominal"
    return "incomplete reading"


def audit_task(task):
    """SMELL: dead store (SonarQube rule S1854).

    The first assignment to label is never read; it is overwritten
    before use, so the initial value is dead.
    """
    label = "unknown"
    if task.get("priority") == "high":
        label = "escalated"
    else:
        label = "standard"
    return label


class TaskScribe:
    """SMELL: class with an excessive number of methods (SonarQube rule S1448).

    SonarQube's default method-count maximum is 10; this class defines
    11. A class this broad almost always has more than one
    responsibility and should be split.
    """

    def open_session(self):
        return "session opened"

    def close_session(self):
        return "session closed"

    def log_start(self):
        return "start logged"

    def log_finish(self):
        return "finish logged"

    def format_title(self, title):
        return title.strip()

    def format_notes(self, notes):
        return notes.strip()

    def validate(self, task):
        return bool(task)

    def summarize(self, task):
        return str(task)

    def archive(self, task):
        return f"archived: {task}"

    def restore(self, task):
        return f"restored: {task}"

    def export(self, task):
        return {"task": task}
