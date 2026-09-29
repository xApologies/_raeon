from collections import Counter

DECK_SIZE = 60
COPY_LIMITS = {
    "FIELD_GENERATOR": 2,
    "UTILITY": 3,
    "PRIME_FIELD": 1,  # identity uniqueness; exact relation to draw deck remains OPEN
}

def validate_deck(card_rows: list[dict], require_exact_size: bool = True) -> list[str]:
    """Validate only currently established structural limits.

    card_rows entries: {"card_id": "...", "class": "..."}
    Does NOT enforce a class ratio.
    """
    errors = []
    if require_exact_size and len(card_rows) != DECK_SIZE:
        errors.append(f"deck must contain exactly {DECK_SIZE} cards")
    counts = Counter(row["card_id"] for row in card_rows)
    class_by_id = {row["card_id"]: row["class"] for row in card_rows}
    for cid, n in counts.items():
        cls = class_by_id[cid]
        limit = COPY_LIMITS[cls]
        if n > limit:
            errors.append(f"{cid}: {n} copies exceeds {limit}")
    return errors
