# Written by Reece Jones

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from itertools import count
from typing import Iterable, Literal, Mapping

from dateutil.relativedelta import relativedelta


__all__ = [
    'Account',
    'CashEndpoint',
    'CashFlowEvent',
    'DateRange',
    'ExpenseSink',
    'IncomeSource',
    'Monthly',
    'Occurrence',
    'OneOff',
    'RunEventsResult',
    'run_events',
    'Schedule',
    'ScheduledCashFlow',
    'ScheduledExpense',
    'ScheduledIncome',
    'ScheduledSaving',
    'ScheduledTransfer',
    'Weekdays',
    'Weekends',
    'Weekly'
]


@dataclass(frozen=True)
class DateRange:
    begin: date     # Inclusive.
    end: date       # Inclusive.

    def __post_init__(self) -> None:
        if self.begin > self.end:
            raise ValueError('begin must be <= end')

    def __contains__(self, d: date) -> bool:
        return self.begin <= d <= self.end


class CashEndpoint(ABC):
    """Somewhere that funds come from or go to."""

    label: str


@dataclass(frozen=True)
class IncomeSource(CashEndpoint):
    label: str


@dataclass(frozen=True)
class ExpenseSink(CashEndpoint):
    label: str


@dataclass(frozen=True)
class Account(CashEndpoint):
    label: str
    liquid: bool        # Can you immediately withdraw and use cash from this account?


@dataclass(frozen=True)
class CashFlowEvent:
    """Some event (on a specific date) that cause cash to flow from one place to another."""

    date: date
    source: CashEndpoint
    destination: CashEndpoint
    amount: float
    schedule: 'ScheduledCashFlow'


DayOfWeek = Literal[0, 1, 2, 3, 4, 5, 6]
DayOfMonth = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


class Occurrence(ABC):
    """Specification of a schedule for a series of events."""

    @abstractmethod
    def iterate(self, range: DateRange) -> Iterable[date]:
        """Iterate all event dates occurring within `range`, in chronological order."""

        raise NotImplementedError()


@dataclass(frozen=True)
class OneOff(Occurrence):
    """Event occurs exactly once, on a specified date."""

    day: date

    def iterate(self, range: DateRange) -> Iterable[date]:
        if self.day in range:
            yield self.day


@dataclass(frozen=True)
class Weekdays(Occurrence):
    """Event occurs on all Mondays to Fridays within a specified date range."""

    range: DateRange

    def iterate(self, range: DateRange) -> Iterable[date]:
        # First occurrence will be from whichever range begins later.
        occurrence = max(self.range.begin, range.begin)
        # No occurrence can be after the end of either range.
        end = min(self.range.end, range.end)
        while occurrence <= end:
            weekday = occurrence.weekday()
            # Occurs only on Monday to Friday (0 to 4).
            if weekday <= 4:
                yield occurrence
            if weekday <= 3:
                # Go from any day Monday-Thursday.
                occurrence += relativedelta(days=1)
            else:
                # Skip from any day Friday-Sunday to the next Monday.
                occurrence += relativedelta(weekday=0)


@dataclass(frozen=True)
class Weekends(Occurrence):
    """Event occurs on all Saturdays and Sundays within a specified date range."""

    range: DateRange

    def iterate(self, range: DateRange) -> Iterable[date]:
        # First occurrence will be from whichever range begins later.
        occurrence = max(self.range.begin, range.begin)
        # No occurrence can be after the end of either range.
        end = min(self.range.end, range.end)
        while occurrence <= end:
            weekday = occurrence.weekday()
            # Occurs only on Saturday and Sunday (5 and 6).
            if weekday >= 5:
                yield occurrence
            if weekday == 5:
                # Go from Saturday to Sunday.
                occurrence += relativedelta(days=1)
            else:
                # Skip from any day that's not Saturday to the next Saturday.
                occurrence += relativedelta(weekday=5)
            

@dataclass(frozen=True)
class Weekly(Occurrence):
    """Event occurs on a specified day of week every `interval` number of weeks, within a specified date range."""

    day: DayOfWeek
    interval: int
    range: DateRange

    def __post_init__(self) -> None:
        if not 0 <= self.day <= 6:
            raise ValueError('day must be in the range [0, 6]')
        if self.interval < 1:
            raise ValueError('interval must be >= 1')

    def iterate(self, range: DateRange) -> Iterable[date]:
        # Inefficient algorithm here but it probably doesn't matter.
        # Improvement would be to calculate the exact first occurrence within the requested range.

        # First possible occurrence is the next specified day of the week from the beginning of the range (could be the
        # same day).
        occurrence = self.range.begin + relativedelta(weekday=self.day)
        # No occurrence can be before the start of either range.
        begin = max(self.range.begin, range.begin)
        # No occurrence can be after the end of either range.
        end = min(self.range.end, range.end)
        while occurrence <= end:
            if occurrence >= begin:
                yield occurrence
            # Move ahead interval number of weeks, maintaining the day of week.
            occurrence += relativedelta(weeks=self.interval)


@dataclass(frozen=True)
class Monthly(Occurrence):
    """Event occurs on a specified day of month every `interval` number of months, within a specified date range."""

    day: DayOfMonth
    interval: int
    range: DateRange

    def __post_init__(self) -> None:
        if not 1 <= self.day <= 31:
            raise ValueError('day must be in the range [1, 31]')
        if self.interval < 1:
            raise ValueError('interval must be >= 1')

    def iterate(self, range: DateRange) -> Iterable[date]:
        # Inefficient algorithm here but it probably doesn't matter.
        # Improvement would be to calculate the exact first occurrence within the requested range.

        # First possible occurrence is the next specified day of the month from the beginning of the range (could be the
        # same day or in the past).
        first = self.range.begin + relativedelta(day=self.day)
        # No occurrence can be before the start of either range.
        begin = max(self.range.begin, range.begin)
        # No occurrence can be after the end of either range.
        end = min(self.range.end, range.end)
        for i in count(0):
            # Go to the specified day of month i months ahead. We must move all i months at once rather than
            # incrementally so that relativedelta will clamp days past the end of the month in the way we want. Note:
            # date(y, 5, 31) + relativedelta(months=1) + relativedelta(months=1) == date(y, 7, 30)  (not what we want)
            # date(y, 5, 31) + relativedelta(months=2) == date(y, 7, 31)
            occurrence = first + relativedelta(months=self.interval * i)
            if occurrence > end:
                break
            elif occurrence >= begin:
                yield occurrence


class ScheduledCashFlow(ABC):
    @abstractmethod
    def iterate(self, range: DateRange) -> Iterable['CashFlowEvent']:
        raise NotImplementedError()


@dataclass(frozen=True)
class ScheduledIncome(ScheduledCashFlow):
    label: str
    occurrence: Occurrence
    amount: float
    destination_account: Account    # The account into which the income is deposited.

    def iterate(self, range: DateRange) -> Iterable['CashFlowEvent']:
        return (CashFlowEvent(d, IncomeSource(self.label), self.destination_account, self.amount, self)
                for d in self.occurrence.iterate(range))


@dataclass(frozen=True)
class ScheduledExpense(ScheduledCashFlow):
    label: str
    occurrence: Occurrence
    amount: float
    source_account: Account     # The account from which the expense is withdrawn.

    def iterate(self, range: DateRange) -> Iterable['CashFlowEvent']:
        return (CashFlowEvent(d, self.source_account, ExpenseSink(self.label), self.amount, self)
                for d in self.occurrence.iterate(range))


@dataclass(frozen=True)
class ScheduledTransfer(ScheduledCashFlow):
    label: str
    occurrence: Occurrence
    amount: float
    source_account: Account         # The account from which the cash is withdrawn.
    destination_account: Account    # The account into with the cash is deposited.

    def iterate(self, range: DateRange) -> Iterable['CashFlowEvent']:
        return (CashFlowEvent(d, self.source_account, self.destination_account, self.amount, self)
                for d in self.occurrence.iterate(range))


@dataclass(frozen=True)
class ScheduledSaving(ScheduledTransfer):
    pass


class Schedule:
    """
        :param general_account: The default account for incomes and expenses.
        :param savings_account: The default account for savings.
    """
    def __init__(self, general_account: Account | None = None, savings_account: Account | None = None) -> None:
        self.general_account = general_account
        self.savings_account = savings_account
        self.all: list[ScheduledCashFlow] = []

    def income(self, label: str, occurrence: Occurrence, amount: float, account: Account | None = None) -> None:
        account = account or self.general_account
        if account is None:
            raise ValueError('Either account or general_account must be provided')
        self.all.append(ScheduledIncome(label, occurrence, amount, account))

    def expense(self, label: str, occurrence: Occurrence, amount: float, account: Account | None = None) -> None:
        account = account or self.general_account
        if account is None:
            raise ValueError('Either account or general_account must be provided')
        self.all.append(ScheduledExpense(label, occurrence, amount, account))

    def saving(self, label: str, occurrence: Occurrence, amount: float, destination_account: Account | None = None,
            source_account: Account | None = None) -> None:
        source_account = source_account or self.general_account
        if source_account is None:
            raise ValueError('Either source_account or general_account must be provided')
        destination_account = destination_account or self.savings_account
        if destination_account is None:
            raise ValueError('Either destination_account or savings_account must be provided')
        self.all.append(ScheduledSaving(label, occurrence, amount, source_account, destination_account))
    
    def transfer(self, label: str, occurrence: Occurrence, amount: float, source_account: Account,
            destination_account: Account) -> None:
        self.all.append(ScheduledTransfer(label, occurrence, amount, source_account, destination_account))

    def iterate(self, range: DateRange) -> Iterable[CashFlowEvent]:
        events = [event for sched in self.all for event in sched.iterate(range)]
        return sorted(events, key=lambda event: event.date)


@dataclass
class RunEventsResult:
    event_logs: list[str]       # Human-readable one-line description of each event.
    dates: list[date]           # Dates associated with each entry in account_balances.
    account_balances: list[dict[Account, float]]    # Account balances for each day at least one event occurred.


def run_events(timeframe: DateRange, events: Iterable[CashFlowEvent], accounts: Iterable[Account],
        initial_account_balances: Mapping[Account, float] = {}) -> RunEventsResult:
    account_balances = {account: 0.0 for account in accounts} | initial_account_balances
    event_logs: list[str] = []
    dates: list[date] = []
    account_balances_list: list[dict[Account, float]] = []

    def append_day_results(d: date) -> None:
        dates.append(d)
        account_balances_list.append(account_balances.copy())

    prev_date = timeframe.begin
    append_day_results(prev_date)
    for event in events:
        while prev_date < event.date:
            append_day_results(prev_date)
            prev_date += relativedelta(days=1)
        if isinstance(event.source, Account):
            account_balances[event.source] -= event.amount
        if isinstance(event.destination, Account):
            account_balances[event.destination] += event.amount
        event_logs.append(f'{event.date} | ${event.amount} from "{event.source.label}" to "{event.destination.label}"')
    append_day_results(prev_date)

    if prev_date != timeframe.end:
        append_day_results(timeframe.end)
    
    return RunEventsResult(event_logs, dates, account_balances_list)
