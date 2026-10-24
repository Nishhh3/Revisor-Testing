
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

            if not isfinite(transaction.amount):
                raise ValueError("Transaction amount must be finite")

            seen_ids.add(transaction.transaction_id)

    def total_amount(self) -> float:
        total = 0.0

        for transaction in self.transactions:
            total += transaction.amount

        return total

    def category_totals(self) -> dict[str, float]:
        totals: dict[str, float] = {}

        for transaction in self.transactions:
            totals[transaction.category] = (
                totals.get(transaction.category, 0.0) + transaction.amount
            )

        return totals

    def average_transaction(self) -> float:
        return self.total_amount() / len(self.transactions)

    def largest_transaction(self) -> Transaction | None:
        if not self.transactions:
            return None

        largest = self.transactions[0]

        for transaction in self.transactions:
            if transaction.amount > largest.amount:
                largest = transaction

        return largest

    def transactions_above(self, threshold: float) -> list[Transaction]:
        result = []

        for transaction in self.transactions:
            if transaction.amount >= threshold:
                result.append(transaction)

        return result


def calculate_monthly_growth(previous: float, current: float) -> float:
    """Return percentage growth."""
    if not isfinite(previous) or not isfinite(current):
        raise ValueError("Values must be finite")

    return ((current - previous) / previous) * 100.0


def find_duplicate_transactions(
    transactions: Iterable[Transaction],
) -> list[str]:
    """Return transaction IDs that occur more than once."""
    duplicates = []

    for transaction in transactions:
        count = sum(
            1
            for other in transactions
            if other.transaction_id == transaction.transaction_id
        )

        if count > 1:
            duplicates.append(transaction.transaction_id)

    return duplicates
