import { useCallback, useState, useEffect } from "react";
import Calendar from "react-calendar";
import CurrencyInput from "./CurrencyInput";
import "react-calendar/dist/Calendar.css";
import "./App.css";

// VITE_API_URL for actual deployment only
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const RECURRING_OPTIONS = [
  { value: "One Time", label: "One time" },
  { value: "Daily", label: "Daily" },
  { value: "Weekly", label: "Weekly" },
  { value: "Monthly", label: "Monthly" },
  { value: "Yearly", label: "Yearly" },
];

const EMPTY_FORM = {
  name: "",
  amount: "",
  date: "",
  recurring_freq: "One Time",
};

// ===========================================================================
// HELPER FUNCTIONS
// ===========================================================================

function todayMonthString() {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
}

function toDateKey(date) {
  const d = String(date.getDate()).padStart(2, "0");
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const y = date.getFullYear();
  return `${d}-${m}-${y}`;
}

function getCurrencySymbol(currencyCode) {
  const parts = new Intl.NumberFormat(undefined, {
    style: "currency",
    currency: currencyCode,
  }).formatToParts(0);

  return parts.find((part) => part.type === "currency")?.value ?? currencyCode;
}

function formatAmount(
  amount,
  currencyCode = "USD",
  includePositiveSign = false,
) {
  const sign = amount < 0 ? "-" : includePositiveSign ? "+" : "";
  const symbol = getCurrencySymbol(currencyCode);
  return `${sign}${symbol}${Math.abs(amount).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function isNegativeBalance(amount) {
  return amount < 0 ? { id: "negative-balance" } : {};
}

// ===========================================================================
// COMPONENTS
// ===========================================================================

export default function App() {
  // Transactions loaded from DB
  const [transactions, setTransactions] = useState([]);
  const [txLoading, setTxLoading] = useState(true);
  const [txError, setTxError] = useState(null);

  // Currency code
  const [currency, setCurrency] = useState("USD");

  // Add-transaction form state
  const [form, setForm] = useState(EMPTY_FORM);
  const [addLoading, setAddLoading] = useState(false);
  const [addError, setAddError] = useState(null);

  // Update-transaction form state
  const [updateForm, setUpdateForm] = useState(EMPTY_FORM);
  const [updateLoading, setUpdateLoading] = useState(false);
  const [updateError, setUpdateError] = useState(null);

  // Forecast parameters & result
  const [startingBalance, setStartingBalance] = useState(0);
  const [currentMonth, setCurrentMonth] = useState(todayMonthString());

  const [forecast, setForecast] = useState(null);
  const [forecastLoading, setForecastLoading] = useState(false);
  const [forecastError, setForecastError] = useState(null);

  // Calendar active start date
  const [calendarActiveStartDate, setCalendarActiveStartDate] = useState(
    new Date(),
  );

  // ===========================================================================
  // VALIDATION HELPERS
  // ===========================================================================
  const isValidStartingBalance = () => {
    return !isNaN(Number(startingBalance));
  };

  const isValidMonthString = (monthString) => {
    return (
      typeof monthString === "string" &&
      monthString.match(/^\d{4}-\d{2}$/) &&
      Number(monthString.split("-")[1]) <= 12 &&
      Number(monthString.split("-")[1]) >= 1
    );
  };

  const isReadyToForecast = () => {
    return (
      isValidStartingBalance() &&
      isValidMonthString(currentMonth) &&
      transactions.length > 0 &&
      !forecastLoading &&
      !txLoading &&
      !addLoading
    );
  };

  // ===========================================================================
  // FETCH ALL TRANSACTIONS
  // ===========================================================================

  const fetchTransactions = useCallback(async () => {
    setTxLoading(true);
    setTxError(null);

    try {
      const res = await fetch(`${API_URL}/api/transaction/all`);
      if (!res.ok)
        throw new Error(`GET /api/transaction/all returned ${res.status}`);
      setTransactions(await res.json());
    } catch (err) {
      setTxError(err.message || "Could not load transactions");
    } finally {
      setTxLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  // ===========================================================================
  // TRANSACTION OPERATIONS
  // ===========================================================================

  async function addTransaction(e) {
    // Ensure transaction form is filled in
    e.preventDefault();
    if (!form.name || !form.amount || !form.date) return;

    setAddLoading(true);
    setAddError(null);
    try {
      const res = await fetch(`${API_URL}/api/transaction`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name,
          amount: Number(form.amount),
          date: form.date,
          recurring_freq: form.recurring_freq,
        }),
      });
      if (!res.ok)
        throw new Error(`POST /api/transaction/ returned ${res.status}`);

      // Add created transaction
      const createdTransaction = await res.json();
      setTransactions((prev) => [...prev, createdTransaction]);

      // Empty the transaction form
      setForm(EMPTY_FORM);

      // Invalidate stale forecast
      setForecast(null);
    } catch (err) {
      setAddError(err.message || "Failed to add transaction");
    } finally {
      setAddLoading(false);
    }
  }

  async function deleteTransaction(tr_id) {
    try {
      const res = await fetch(`${API_URL}/api/transaction/${tr_id}`, {
        method: "DELETE",
      });
      if (!res.ok)
        throw new Error(`DELETE /api/transaction/ returned ${res.status}`);

      // Remove the chosen transaction from transactions via filter
      setTransactions((prev) => prev.filter((tr) => tr.tr_id !== tr_id));

      // Invalidate stale forecast
      setForecast(null);
    } catch (err) {
      alert(`Could not delete transaction: ${err.message || "Unknown error"}`);
    }
  }

  // Not used for now
  // TODO: Implement in the future
  async function updateTransaction(tr_id) {
    setUpdateLoading(true);
    setUpdateError(null);

    try {
      const res = await fetch(`${API_URL}/api/transaction/${tr_id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: updateForm.name,
          amount: Number(updateForm.amount),
          date: updateForm.date,
          recurring_freq: updateForm.recurring_freq,
        }),
      });
      if (!res.ok)
        throw new Error(
          `PATCH /api/transaction/${tr_id} returned ${res.status}`,
        );

      // Replace the updated transaction in the list
      const updatedTransaction = await res.json();
      setTransactions((prev) =>
        prev.map((tr) => (tr.tr_id === tr_id ? updatedTransaction : tr)),
      );

      // Invalidate stale forecast
      setForecast(null);
    } catch (err) {
      setUpdateError(err.message || "Failed to update transaction");
    } finally {
      setUpdateLoading(false);
    }
  }

  // ===========================================================================
  // RUN FORECAST
  // ===========================================================================
  async function runForecast() {
    setForecastLoading(true);
    setForecastError(null);

    try {
      const res = await fetch(`${API_URL}/api/forecast`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          starting_balance: Number(startingBalance),
          transactions: transactions,
          month: currentMonth,
        }),
      });
      if (!res.ok) throw new Error(`POST /api/forecast returned ${res.status}`);
      const data = await res.json();
      setForecast(data);
    } catch (err) {
      setForecastError(err.message || "Failed to reach the forecast API");
    } finally {
      setForecastLoading(false);
    }
  }

  // ===========================================================================
  // CALENDAR HELPERS
  // ===========================================================================

  function getHeatmapClass(balance, lowest, highest) {
    if (lowest === undefined || highest === undefined || highest === lowest) {
      return "heatmap-10";
    }
    const ratio = Math.max(
      0,
      Math.min(1, (balance - lowest) / (highest - lowest)),
    );
    const index = Math.round(ratio * 10);
    return `heatmap-${index}`;
  }

  function tileClassName({ date, view }) {
    if (view !== "month" || !forecast) return null;
    const balance = forecast.balances[toDateKey(date)];
    if (balance === undefined) return null;
    return getHeatmapClass(
      balance,
      forecast.lowest_balance,
      forecast.highest_balance,
    );
  }

  function tileContent({ date, view }) {
    if (view !== "month" || !forecast) return null;
    const balance = forecast.balances[toDateKey(date)];
    if (balance === undefined) return null;
    return (
      <div className="day-tile" {...isNegativeBalance(balance)}>
        {formatAmount(balance, currency)}
      </div>
    );
  }

  const handleCurrentMonthChange = (e) => {
    const value = e.target.value;
    setCurrentMonth(value);

    // Expecting format like "2026-08" (YYYY-MM)
    if (isValidMonthString(value)) {
      const parsed = new Date(`${value}-01T00:00:00`);
      setCalendarActiveStartDate(parsed);
    }
  };

  // ===========================================================================
  // RENDER
  // ===========================================================================

  return (
    <div className="app">
      <header className="app-header">
        <h1>ForeCashier</h1>
        <p>Project your balance across the month and spot tight days early.</p>
      </header>

      <div className="layout">
        {/* -- Left panel -- */}
        <section className="panel">
          <h2>Setup</h2>

          <label className="field">
            Currency
            <CurrencyInput
              value={currency}
              onChange={setCurrency}
            ></CurrencyInput>
          </label>

          <label className="field">
            Starting balance ({currency})
            <input
              id="starting-balance"
              type="number"
              value={startingBalance}
              onChange={(e) => setStartingBalance(e.target.value)}
            />
          </label>
          {!isValidStartingBalance() && (
            <p className="error">Invalid starting balance</p>
          )}

          <label className="field">
            Month (YYYY-MM, e.g. 2026-08)
            <input
              id="forecast-month"
              type="month"
              value={currentMonth}
              onChange={(e) => {
                handleCurrentMonthChange(e);
                setForecast(null);
              }}
            />
          </label>
          {!isValidMonthString(currentMonth) && (
            <p className="error">Invalid month string (Must be YYYY-MM)</p>
          )}

          {/* -- Transaction list -- */}
          <h3>Transactions</h3>

          {txLoading && <p className="muted-text">Loading</p>}
          {txError && <p className="error">{txError}</p>}
          {!txLoading && transactions.length === 0 && (
            <p className="muted-text">No transactions yet. Add one below.</p>
          )}

          <ul className="transaction-list">
            {transactions.map((t) => (
              <li key={t.tr_id} className={t.amount < 0 ? "expense" : "income"}>
                <div className="name-val">
                  <span className="name">{t.name}</span>
                  <span className="amount">
                    {formatAmount(t.amount, currency, true)}
                  </span>
                </div>
                <span className="date">
                  {t.date} · {t.recurring_freq}
                </span>
                <button
                  className="delete-button"
                  onClick={() => deleteTransaction(t.tr_id)}
                  aria-label={`Remove ${t.name}`}
                  title="Remove"
                >
                  ×
                </button>
              </li>
            ))}
          </ul>

          {/* -- Add form -- */}
          <h3>Add Transaction</h3>
          <form className="add-form" onSubmit={addTransaction}>
            <input
              id="tx-name"
              placeholder="Name (e.g. Rent)"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
            <input
              type="number"
              step="0.01"
              placeholder="Amount  (+ income / - expense)"
              value={form.amount}
              onChange={(e) => setForm({ ...form, amount: e.target.value })}
              required
            />
            <input
              type="date"
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              required
            />
            <select
              value={form.recurring_freq}
              onChange={(e) =>
                setForm({ ...form, recurring_freq: e.target.value })
              }
            >
              {RECURRING_OPTIONS.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
            <button
              id="add-transaction-btn"
              type="submit"
              disabled={addLoading}
            >
              {addLoading ? "Adding..." : "Add transaction"}
            </button>
          </form>

          {addError && <p className="error">{addError}</p>}

          {/* -- Run forecast -- */}
          <button
            id="run-forecast-btn"
            className="run-forecast"
            onClick={runForecast}
            disabled={!isReadyToForecast()}
          >
            {forecastLoading ? "Calculating..." : "Run forecast"}
          </button>

          {forecastError && <p className="error">{forecastError}</p>}

          {forecast && (
            <p className="summary">
              Lowest projected balance:{" "}
              <strong {...isNegativeBalance(forecast.lowest_balance)}>
                {formatAmount(forecast.lowest_balance, currency)}
              </strong>{" "}
              on {forecast.lowest_balance_date}
            </p>
          )}
        </section>

        {/* -- Right panel -- */}
        <section className="panel calendar-panel">
          <h2>Calendar</h2>

          {!forecast && (
            <p className="muted-text calendar-hint">
              Set up your transactions and click <strong>Run forecast</strong>{" "}
              to see daily balances on the calendar.
            </p>
          )}

          {forecast && (
            <div className="heatmap-legend">
              <span className="legend-label">
                {formatAmount(forecast.lowest_balance, currency)} (Low)
              </span>
              <div className="heatmap-gradient-bar" />
              <span className="legend-label">
                {formatAmount(forecast.highest_balance, currency)} (High)
              </span>
            </div>
          )}

          <br />

          <Calendar
            calendarType="gregory"
            tileClassName={tileClassName}
            tileContent={tileContent}
            activeStartDate={calendarActiveStartDate}
            onActiveStartDateChange={({ activeStartDate }) =>
              setActiveStartDate(activeStartDate)
            }
            showNavigation={true}
            showNeighboringMonth={false}
            view="month"
          />
        </section>
      </div>
    </div>
  );
}
