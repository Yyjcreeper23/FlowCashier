import React from "react";
import "./App.css";

const CURRENCIES = [
  "USD",
  "MYR",
  "EUR",
  "SGD",
  "GBP",
  "CAD",
  "AUD",
  "NZD",
  "JPY",
  "CNY",
];

const CurrencyInput = ({ value, onChange }) => (
  <div className="field">
    <select
      name="currency"
      id="currency-select"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    >
      {CURRENCIES.map((code) => (
        <option key={code} value={code}>
          {code}
        </option>
      ))}
    </select>
  </div>
);

export default CurrencyInput;
