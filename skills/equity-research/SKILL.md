---
name: equity-research
description: "Equity research report on a listed stock. Use when the user names a ticker or company and asks for an analysis or valuation, a buy/sell/hold call, or a price target."
---

# Equity Research

Produce one report per stock, built from live web research (searches and page fetches) and written in the exact structure under [Output format](#output-format). Every figure in the report is **sourced**: it came from a page fetched or searched this run, carries its timeframe (YoY, QoQ, TTM, FY, as-of date), and links to an entry in the report's Sources list. From step 1 on, keep a **fact sheet** in your working notes: one line per figure with value, timeframe, source URL, and source date. A field with no sourced figure says so plainly, naming what was checked ("Not available: no listed options on SGX; checked SGX derivatives, broker sites"). A **proxy** may fill the gap only when labelled as one ("Proxy: US ADR options show...").

Several tickers in one request: one report per ticker. Where subagents are available, dispatch one per ticker with this skill, so each researches in a clean context; otherwise run the full sequence for each in turn.

The `reports/` folder (prior-report lookup in step 1, save in step 5) applies only where a persistent working directory exists; elsewhere skip the lookup and present the report in chat only.

## Steps

### 1. Resolve the counter

Pin down before any analysis:

- Ticker code as the exchange lists it (e.g. `D05`, `0700`, `SHEL`, `AAPL`)
- Company name
- Exchange operator acronym (SGX, LSE, HKEX, NYSE, NASDAQ, ...)
- Counter currency: the currency this line trades in. Some stocks trade on several counters (SGX SGD/USD, HKEX HKD/RMB, ADR vs home listing); take the one the user named, else the primary counter, and say which.
- Reporting currency of the company's financial statements, which may differ (RMB for many HKEX names, USD for many LSE and some SGX names)
- Current price, with date and time quoted

If the ticker is ambiguous, ask the user which listing. Then read the market notes for the exchange: [`markets/sgx.md`](markets/sgx.md), [`markets/lse.md`](markets/lse.md), [`markets/hkex.md`](markets/hkex.md), [`markets/us.md`](markets/us.md), or [`markets/other.md`](markets/other.md) for any other exchange.

Check `reports/` in the current directory for earlier reports on this ticker; if one exists, read the most recent.

Done when all six facts are on the fact sheet, the market notes are read, and any prior report is read.

### 2. Research

Run all three search passes, using the sources the market notes name, adding each figure to the fact sheet. Prefer the latest reported period for financials and data no older than 30 days for price, technicals, options, and consensus targets; note the date wherever a figure is older.

1. **Financial performance**: latest results (revenue, growth YoY and QoQ or HoH, gross/operating/net margins, EPS vs consensus), segment or business KPIs, management guidance, analyst consensus rating and price targets with firm names and dates.
2. **Market positioning**: 3-5 peers chosen by business, wherever listed, including at least one from the same exchange when one exists. P/E, P/S, EV/EBITDA, or sector-appropriate multiples (P/B and ROE for banks, P/NAV and DPU yield for REITs). Market share, sector ETF or index performance, competitive developments.
3. **Advanced intelligence**: 52-week range, support/resistance, moving averages, RSI, volume trend; options put/call ratio, implied volatility, unusual activity; insider buys/sells with names and amounts; buyback programmes; institutional ownership changes; short interest; regulatory or legal matters; ESG issues material to institutional holders.

Done when every placeholder in the output format maps to a fact-sheet line, a labelled proxy, or a recorded "not available" with what was checked.

### 3. Derive the call

- **Horizon**: 12 months unless the user asked for another.
- **Scenario targets**: bull, base, bear prices, each tied to a specific assumption (a multiple on a forward earnings figure, a DCF driver, a NAV discount). Where the reporting currency differs from the counter currency, state the FX rate used and its date.
- **Probability weights** summing to 100%.
- **Price target** = the probability-weighted value of the three scenarios, rounded sensibly. Upside/downside % = target / current price - 1.
- **Rating**: BUY above +15% upside, SELL below -10%, HOLD between. Deviate only with the reason stated in the Executive Summary (e.g. HOLD despite +20% upside on binary regulatory risk).
- **Position sizing**: a range as % of a diversified equity portfolio with no other single name above 10%, justified by beta, volatility, or liquidity. State that assumption in a short clause.

Done when the weighted value, the headline target, and the upside % agree arithmetically.

### 4. Write the report

Fill the [Output format](#output-format) exactly: same headings, same order, same bold labels, nothing before or after it.

- **Currency**: write every amount with its ISO currency code (SGD 0.82, HKD 385.20, USD 212.40; LSE prices in pence, e.g. 1,245p), since web chat renders text between two dollar signs as LaTeX math. Share prices and targets in the counter currency, filling the template's `[CCY]`; financials in the reporting currency (GBP 1.2bn, USD 4.5bn, RMB 30bn).
- **Citations**: numbered markers `[n]` pointing into `## SOURCES`; one marker covers a sentence whose figures share a source. Each source line: title, publisher, date, URL.
- **Prior report**: if step 1 found one, end the Executive Summary with the `Changes since` line: previous rating, target, and what moved the thesis. Omit the line otherwise.

### 5. Check, save, and present

Confirm each, fixing the draft until all hold:

- Every figure is **sourced**, its `[n]` marker resolving to a Sources entry.
- No `[placeholder]` text remains; gaps read as "not available" statements or labelled proxies.
- Probability weights sum to 100% and reproduce the headline target.
- Upside % matches the target and the quoted current price.
- Price currency matches the header's counter throughout, every amount written with its currency code; any mixed-currency valuation names its FX rate.

Then save to `reports/<TICKER>-<YYYY-MM-DD>.md` in the current directory (create `reports/` if needed; a same-day re-run overwrites), and show the report in chat.

## Output format

```markdown
# **[TICKER CODE] - ENHANCED EQUITY RESEARCH**
### [TICKER NAME] | [Exchange operator acronym, e.g. NYSE, SGX]-Listed | [Counter currency, e.g. SGD, HKD, GBX] Counter
> *Analysis Date: [Current date in DD MMM YYYY] | Analyst: LLM-Generated Research | For Educational Purposes Only*

## EXECUTIVE SUMMARY
**[BUY/SELL/HOLD]** with [CCY] [X] price target ([X]% upside/downside) over [timeframe]. [Key catalyst and investment thesis in 1-2 sentences]. [Risk-reward ratio description].
**Changes since [DD MMM YYYY]**: [Previous rating and target → current; what changed the thesis].

## FUNDAMENTAL ANALYSIS
**Recent Financial Metrics**: [Specific revenue growth %, margins, key business KPIs with exact numbers and timeframes]

**Peer Comparison**: [Valuation multiples vs competitors with specific P/E, P/S ratios and company names]

**Forward Outlook**: [Management guidance, analyst consensus, growth projections with specific numbers]

## CATALYST ANALYSIS
**Near-term (0-6 months)**: [Specific upcoming events with dates - earnings, product launches, regulatory decisions]
**Medium-term (6-24 months)**: [Strategic initiatives, market expansion, competitive positioning changes]
**Event-driven**: [M&A potential, index inclusion, spin-offs, special dividends]

## VALUATION & PRICE TARGETS
Current consensus: [CCY] [X] (range [CCY] [low]-[high]). Bull case [CCY] [X] assumes [specific scenario]. Base case [CCY] [X] reflects [scenario]. Bear case [CCY] [X] on [risk scenario]. Probability weighting: [X]%/[Y]%/[Z]%.

## RISK ASSESSMENT
**Company risks**: [Specific business risks - competitive threats, regulatory issues, operational challenges]
**Macro risks**: [Interest rate sensitivity, economic cycle impact, sector rotation effects]
**Position sizing**: [X]%-[Y]% allocation based on [volatility/beta/risk factors]. **ESG considerations**: [If material to institutional ownership].

## TECHNICAL CONTEXT & OPTIONS INTELLIGENCE
[Current price vs 52-week range]. [Key support/resistance levels]. [Recent volume patterns]. **Options flow**: [Put/call ratios, unusual activity, implied volatility trends]. [Momentum indicators and trend analysis].

## MARKET POSITIONING
**Sector Performance**: [Stock performance vs sector ETF and broader market with specific %]. [Rotation trends affecting the position]. [Relative strength analysis].

## INSIDER SIGNALS
[Recent insider buying/selling with specific values and executives]. [Share buyback programs]. [Institutional ownership changes]. [Pattern analysis of insider behavior].

## SOURCES
[n]. [Title] - [Publisher], [DD MMM YYYY]. [URL]
```
