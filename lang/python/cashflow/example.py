from datetime import date

from matplotlib import pyplot

from cashflow import Account, DateRange, ExpenseSink, IncomeSource, Monthly, OneOff, run_events, Schedule, \
    ScheduledSaving, Weekdays, Weekly


# Schedule applies to 2022/2023 financial year.
year_begin = date(2022, 7, 1)
year_end = date(2023, 6, 30)

all_year = DateRange(year_begin, year_end)

# Declare bank accounts, investments, etc.
general_account = Account('Everyday account', liquid=True)     # Default account for income and expenses
investment_account = Account('Investment account', liquid=False)
accounts = (general_account, investment_account)

schedule = Schedule(general_account)

# Example: work paycheque of $2000 comes every month on the 15th day of month, occurring all year.
schedule.income('Work', Monthly(15, 1, all_year), 2000)
# Example: tax return of $1000 comes once on 2022/10/01
schedule.income('Tax return', OneOff(date(2022, 10, 1)), 1000)
# Example: public transport to work, occurs every weekday (Monday-Friday).
schedule.expense('Public transport', Weekdays(all_year), 6)
# Example: groceries cost $100 every week, on Saturdays.
schedule.expense('Groceries', Weekly(6, 1, all_year), 100)
schedule.expense('Car insurance', OneOff(date(2022, 7, 22)), 375)
schedule.saving('Investment', Monthly(1, 3, all_year), 1500, investment_account)
# Other occurrence types available, see classes derived from `Occurrence`.

# Timeframe in which we're doing the projection and analysis.
analysis_range = all_year

# Can leave these out to just get change in cash rather than absolute values.
initial_account_balances = {
    general_account: 2000,
    investment_account: 10000
}


# Calulcate all cash flow events in desired timeframe.
events = list(schedule.iterate(analysis_range))

# Apply the events to accounts and get a sequence of account balances.
results = run_events(analysis_range, events, accounts, initial_account_balances)
# Display the details of each event.
for log in results.event_logs:
    print(log)

# Summary of main cash flows.
total_income = sum(event.amount for event in events if isinstance(event.source, IncomeSource))
total_expenses = sum(event.amount for event in events if isinstance(event.destination, ExpenseSink))
total_savings = sum(event.amount for event in events if isinstance(event.schedule, ScheduledSaving))
print(f'Total income: ${total_income:.2f}')
print(f'Total expenses: ${total_expenses:.2f}')
print(f'Total savings: ${total_savings:.2f}')

# Plot the balance of each account over time.
for account in accounts:
    balances = [bs[account] for bs in results.account_balances]
    pyplot.plot(results.dates, balances, label=account.label)
# Plot total cash on hand over time.
cash_on_hand_series = [sum(b for a, b in bs.items() if a.liquid) for bs in results.account_balances]
pyplot.plot(results.dates, cash_on_hand_series, label='Total cash at hand')
# Plot total locked/inaccessible savings over time.
locked_savings_series = [sum(b for a, b in bs.items() if not a.liquid) for bs in results.account_balances]
pyplot.plot(results.dates, locked_savings_series, label='Total locked savings')
pyplot.title(f'Funds from {analysis_range.begin} to {analysis_range.end}')
pyplot.xlabel('Date')
pyplot.ylabel('Funds ($)')
pyplot.legend()
pyplot.tight_layout()
pyplot.show()
