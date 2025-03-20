from .han import Han


def add_rule(rule: str):
    return Han().add_rule(rule)


def to_traditional(original: str) -> str:
    return Han().to_traditional(original)
