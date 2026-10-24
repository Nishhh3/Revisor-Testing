```python
"""Financial analytics utilities for calculating portfolio metrics."""

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    amount: float
    category: str


class PortfolioAnalyzer:
    """Analyze transactions and calculate portfolio statistics."""

    def __init__(self, transactions: Iterable[Transaction]):
        self.transactions = tuple(transactions)
        self._validate_transactions()

    def _validate_transactions(self) -> None:
        seen_ids = set()

        for transaction in self.transactions:
            if not transaction.transaction_id:
                raise ValueError("Transaction ID cannot be empty")

            if transaction.transaction_id in seen_ids:
                raise ValueError(
                    f"Duplicate transaction ID: {transaction.transaction_id}"
                )

            if not isfinite(transaction.amount):
                raise ValueError("Transaction amount must be finite")

            seen_ids.add(transaction.transaction_id)

    def total_amount(self) -> float:
        return sum(t.amount for t in self.transactions)

    def category_totals(self) -> dict[str, float]:
        totals: dict[str, float] = {}

        for transaction in self.transactions:
            totals[transaction.category] = (
                totals.get(transaction.category, 0.0) + transaction.amount
            )

        return totals

    def average_transaction(self) -> float:
        if not self.transactions:
            return 0.0

        return self.total_amount() / len(self.transactions)

    def largest_transaction(self) -> Transaction | None:
        if not self.transactions:
            return None

        return max(self.transactions, key=lambda t: t.amount)

    def transactions_above(self, threshold: float) -> list[Transaction]:
        return [
            transaction
            for transaction in self.transactions
            if transaction.amount > threshold
        ]


def calculate_monthly_growth(previous: float, current: float) -> float:
    """Return percentage growth; return zero when the previous value is zero."""
    if not isfinite(previous) or not isfinite(current):
        raise ValueError("Values must be finite")

    if previous == 0:
        return 0.0

    return ((current - previous) / abs(previous)) * 100.0


def find_duplicate_transactions(
    transactions: Iterable[Transaction],
) -> list[str]:
    """Return transaction IDs that occur more than once."""
    seen = set()
    duplicates = set()

    for transaction in transactions:
        if transaction.transaction_id in seen:
            duplicates.add(transaction.transaction_id)
        else:
            seen.add(transaction.transaction_id)

    return sorted(duplicates)
```
