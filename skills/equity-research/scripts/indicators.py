#!/usr/bin/env python3
"""Technical indicators from daily price history, standard library only.

Usage: python3 indicators.py <file>

<file> is either Yahoo's chart JSON (query1.finance.yahoo.com/v8/finance/chart/
<SYMBOL>?range=1y&interval=1d) or a CSV with a header row holding date, close
and volume columns (high and low optional). Prints one line per figure:
field | value | as of <last date>.
"""
import csv
import json
import sys
from datetime import date, datetime, timedelta, timezone


def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rows = load_yahoo(text) if text.lstrip().startswith("{") else load_csv(text)
    rows = [r for r in rows if r["close"] is not None]
    rows.sort(key=lambda r: r["date"])
    if len(rows) < 35:
        sys.exit(f"need at least 35 sessions, got {len(rows)}")
    return rows


def load_yahoo(text):
    result = json.loads(text)["chart"]["result"][0]
    offset = timedelta(seconds=result["meta"].get("gmtoffset", 0))
    quote = result["indicators"]["quote"][0]
    return [
        {
            "date": (datetime.fromtimestamp(ts, timezone.utc) + offset).date(),
            "close": quote["close"][i],
            "high": quote.get("high", [None] * (i + 1))[i],
            "low": quote.get("low", [None] * (i + 1))[i],
            "volume": quote.get("volume", [None] * (i + 1))[i] or 0,
        }
        for i, ts in enumerate(result["timestamp"])
    ]


def load_csv(text):
    rows = []
    for raw in csv.DictReader(text.splitlines()):
        r = {k.strip().lower(): (v or "").strip() for k, v in raw.items() if k}
        num = lambda k: float(r[k].replace(",", "")) if r.get(k) else None
        rows.append({
            "date": date.fromisoformat(r["date"][:10]),
            "close": num("close"),
            "high": num("high"),
            "low": num("low"),
            "volume": num("volume") or 0,
        })
    return rows


def sma(values, n):
    return sum(values[-n:]) / n if len(values) >= n else None


def ema_series(values, n):
    """EMA seeded with the simple average of the first n values."""
    out = [None] * (n - 1) + [sum(values[:n]) / n]
    k = 2 / (n + 1)
    for v in values[n:]:
        out.append(v * k + out[-1] * (1 - k))
    return out


def rsi(closes, n=14):
    """RSI with Wilder smoothing; also returns the previous session's value."""
    changes = [b - a for a, b in zip(closes, closes[1:])]
    gain = sum(max(c, 0) for c in changes[:n]) / n
    loss = sum(max(-c, 0) for c in changes[:n]) / n
    values = []
    for c in changes[n:]:
        gain = (gain * (n - 1) + max(c, 0)) / n
        loss = (loss * (n - 1) + max(-c, 0)) / n
        values.append(100.0 if loss == 0 else 100 - 100 / (1 + gain / loss))
    return values[-1], values[-2]


def macd(closes, fast=12, slow=26, signal=9):
    fast_ema, slow_ema = ema_series(closes, fast), ema_series(closes, slow)
    line = [f - s for f, s in zip(fast_ema[slow - 1:], slow_ema[slow - 1:])]
    sig = ema_series(line, signal)
    return line[-1], sig[-1]


def main():
    rows = load(sys.argv[1])
    closes = [r["close"] for r in rows]
    volumes = [r["volume"] for r in rows]
    last = rows[-1]
    asof = last["date"].strftime("%d %b %Y")

    def out(field, value):
        print(f"{field} | {value} | as of {asof}")

    def price(v):
        return f"{v:.4g}" if v < 10 else f"{v:,.2f}"

    out("Close", price(last["close"]))

    year = [r for r in rows if r["date"] > last["date"] - timedelta(days=365)]
    basis = "intraday" if all(r["high"] and r["low"] for r in year) else "closing"
    hi = max((r["high"] if basis == "intraday" else r["close"]) for r in year)
    lo = min((r["low"] if basis == "intraday" else r["close"]) for r in year)
    out(f"52-week high ({basis})", f"{price(hi)} (close {last['close'] / hi - 1:+.1%} from it)")
    out(f"52-week low ({basis})", f"{price(lo)} (close {last['close'] / lo - 1:+.1%} from it)")

    recent = rows[-20:]
    out(f"20-day high ({basis})", price(max((r["high"] if basis == "intraday" else r["close"]) for r in recent)))
    out(f"20-day low ({basis})", price(min((r["low"] if basis == "intraday" else r["close"]) for r in recent)))

    for n in (20, 50, 100, 200):
        v = sma(closes, n)
        out(f"{n}-day SMA", price(v) if v else f"n/a (only {len(closes)} sessions)")

    now, prev = rsi(closes)
    out("RSI(14, Wilder)", f"{now:.1f} (previous session {prev:.1f})")

    line, sig = macd(closes)
    side = "above" if line > sig else "below"
    out("MACD(12,26,9)", f"line {line:.4g}, signal {sig:.4g}, line {side} signal")

    out("20-day average volume", f"{sma(volumes, 20):,.0f}")
    if len(volumes) >= 40:
        out("20-day average volume, 20 sessions earlier", f"{sum(volumes[-40:-20]) / 20:,.0f}")

    weeks = {}
    for r in rows:
        monday = r["date"] - timedelta(days=r["date"].weekday())
        weeks[monday] = weeks.get(monday, 0) + r["volume"]
    for monday in sorted(weeks)[-4:]:
        out(f"Volume, week of {monday.strftime('%d %b %Y')}", f"{weeks[monday]:,.0f}")


if __name__ == "__main__":
    main()
