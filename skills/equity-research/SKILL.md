---
name: equity-research
description: "Equity research report on a listed stock. Use when the user names a ticker or company and asks for an analysis or valuation, a buy/sell/hold call, or a price target."
---

# Equity Research

Produce one report per stock, built from live web research (searches and page fetches) and written in the exact structure under [Output format](#output-format). Every figure in the report is **sourced**: it came from a page fetched or searched this run, carries its timeframe (YoY, QoQ, TTM, FY, as-of date), and links to an entry in the report's Sources list. From step 1 on, keep a **fact sheet** in your working notes: one line per figure with value, timeframe, source URL, and source date. A field with no sourced figure says so plainly, naming what was checked ("Not available: no listed options on SGX; checked SGX derivatives, broker sites"). A **proxy** may fill the gap only when labelled as one ("Proxy: US ADR options show...").

**Fan out** independent work: issue independent searches and fetches together in one turn, and where you can dispatch subagents, send independent tasks to them all at once rather than one after another. Only the steps themselves are sequential.

Several tickers in one request: one report per ticker. Where you can dispatch subagents, dispatch one per ticker with this skill in a single turn, so each researches in a clean context; otherwise run the full sequence for each in turn.

The `reports/` folder (prior-report lookup in step 1, save in step 5) applies only where a persistent working directory exists; elsewhere skip the lookup and present the report in chat only.

## Steps

### 1. Resolve the counter

Pin down before any analysis, fanning out the price lookup, the listing lookups, and the `reports/` check:

- Ticker code as the exchange lists it (e.g. `D05`, `0700`, `SHEL`, `AAPL`)
- Company name
- Exchange operator acronym (SGX, LSE, HKEX, NYSE, NASDAQ, ...)
- Counter currency: the currency this line trades in. Some stocks trade on several counters (SGX SGD/USD, HKEX HKD/RMB, ADR vs home listing); take the one the user named, else the primary counter, and say which.
- Reporting currency of the company's financial statements, which may differ (RMB for many HKEX names, USD for many LSE and some SGX names)
- Current price, with date and time quoted

If the ticker is ambiguous, ask the user which listing. Then read the market notes for the exchange: [`markets/sgx.md`](markets/sgx.md), [`markets/lse.md`](markets/lse.md), [`markets/hkex.md`](markets/hkex.md), [`markets/us.md`](markets/us.md), or [`markets/other.md`](markets/other.md) for any other exchange. If the counter is an ETF, unit trust, or other listed fund, also read [`funds.md`](funds.md).

Check `reports/` in the current directory for earlier reports on this ticker; if one exists, read the most recent.

Done when all six facts are on the fact sheet, the market notes (and `funds.md` for a fund) are read, and any prior report is read.

### 2. Research

Run all three search passes below concurrently, using the sources the market notes name. Prefer the latest reported period for financials and data no older than 30 days for price, technicals, options, and consensus targets; note the date wherever a figure is older.

1. **Financial performance**: latest results (revenue, growth YoY and QoQ or HoH, gross/operating/net margins, EPS vs consensus), segment or business KPIs, management guidance, analyst consensus rating and price targets with firm names and dates.
2. **Market positioning**: 3-5 peers chosen by business, wherever listed, including at least one from the same exchange when one exists. P/E, P/S, EV/EBITDA, or sector-appropriate multiples (P/B and ROE for banks, P/NAV and DPU yield for REITs). Market share, sector ETF or index performance, competitive developments.
3. **Advanced intelligence**: 52-week range, support/resistance, moving averages, RSI, volume trend; options put/call ratio, implied volatility, unusual activity; insider buys/sells with names and amounts; buyback programmes; institutional ownership changes; short interest; regulatory or legal matters; ESG issues material to institutional holders.

- **Technicals**: where you can run code, compute the indicators from a year of daily prices with the script in [`technicals.md`](technicals.md); its lines become fact-sheet lines cited to the price-history source as "computed from", and support and resistance are your judgement from them. Without code execution, read the indicators from a vendor page and name its settings where stated ("RSI(14) 46.7 per Investing.com").
- **With subagents**: dispatch one per pass in a single turn. Brief each with the six counter facts, the market notes file path, its pass's list, the freshness rule above, and the fact-sheet line format, plus the Technicals bullet and the `technicals.md` path for pass 3; ask it to fan out its own searches and return fact-sheet lines plus "not available" entries naming what was checked.
- **Without**: run the passes yourself, fanning out each pass's searches and fetches.

Merge every return into the fact sheet. Where passes report one figure with different values, keep the more recent, more primary source. Then fan out follow-up searches for any remaining gaps.

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
- **Lean prose**: figures live in tables; prose carries the reasoning. The Executive Summary thesis is at most 2 sentences and 4 figures, with the detail left to the sections below.
- **Citations**: numbered markers `[n]` pointing into `## SOURCES`; one marker covers a sentence whose figures share a source, and a table row carries its markers in the `Src` column (`[3][7]` for several). A sentence restating a table's figures names the table ("the peer table") and carries no markers, since the table's `Src` column already does. A sentence carries at most 3 markers; past that, split it or keep the primary sources. Each source line: title, publisher, date, URL.
- **Key-figures table**: Recent Financial Metrics is a `Metric | Value | Period | Src` table of up to 8 rows, a change written inside its Value cell (`USD 4.5bn (+12% YoY)`), then one sentence on what the figures say.
- **Peer table**: the subject in bold as the first row, then the 3-5 peers, then a bold `Peer median` row taken over the available figures. The first column holds a short name of 20 characters or fewer with the ticker (`Lion-Phillip S-REIT (CLR)`); the footnote names a peer's exchange where it differs from the subject's. At most 5 metric columns plus `Src`, following the sector: the template's default; banks `P/E | P/B | ROE | Div yield`; REITs `P/NAV | DPU yield | Gearing`. P/E and EV/EBITDA each use one basis down the column, forward if every row has it, else trailing, named in the header (`P/E (fwd)`). An unsourced cell reads `n/a`, with the footnote naming what was checked.
- **Catalyst table**: a bold group row per horizon, Near-term (0-6m), Medium-term (6-24m), Event-driven, then one row per catalyst, dated rows by date then undated. Every horizon has at least one row; an empty one reads "None identified: checked [sources]". The Catalyst cell adds what the timeline label lacks (context, the holding's weight) in 15 words or fewer. Impact opens with ▲ Positive, ▼ Negative, or ◆ Binary.
- **Catalyst timeline**: a plain-text block above the catalyst table, one line per row that has a date or period, sorted by start: the date padded to a fixed width, the row's impact symbol, a label of 40 characters or fewer. Undated rows stay in the table only; with no dated rows, omit the block.
- **Paragraphs**: each bold-labelled point opens its own paragraph, with a blank line before the next, as in the template.
- **Prior report**: if step 1 found one, end the Executive Summary with the `Changes since` line: previous rating, target, and what moved the thesis. Omit the line otherwise.

### 5. Check, save, and present

Confirm each, fixing the draft until all hold:

- Every figure is **sourced**, its `[n]` marker resolving to a Sources entry.
- No `[placeholder]` text remains; gaps read as "not available" statements or labelled proxies.
- Probability weights sum to 100% and reproduce the headline target; the valuation table's weighted row matches it.
- The catalyst timeline lists exactly the table's dated rows, with the same dates and impact symbols.
- The peer median row and the takeaway's premium/discount follow from the table's own figures.
- Upside % matches the target and the quoted current price.
- Price currency matches the header's counter throughout, every amount written with its currency code; any mixed-currency valuation names its FX rate.

Then save to `reports/<TICKER>-<YYYY-MM-DD>.md` in the current directory (create `reports/` if needed; a same-day re-run overwrites), and show the report in chat.

## Output format

````markdown
# **[TICKER CODE] - ENHANCED EQUITY RESEARCH**
### [TICKER NAME] | [Exchange operator acronym, e.g. NYSE, SGX]-Listed | [Counter currency, e.g. SGD, HKD, GBX] Counter
> *Analysis Date: [Current date in DD MMM YYYY] | Analyst: LLM-Generated Research | For informational and educational purposes only. This is not financial advice. Please do your own research and speak with a certified advisor before investing.*

## EXECUTIVE SUMMARY
**[BUY/SELL/HOLD] with [CCY] [X] price target ([X]% upside/downside) over [timeframe].**

[Key catalyst and investment thesis, with the risk-reward, in at most 2 sentences and 4 figures].

**Changes since [DD MMM YYYY]**: [Previous rating and target → current; what changed the thesis].

## FUNDAMENTAL ANALYSIS
**Recent Financial Metrics**:

| Metric | Value | Period | Src |
| --- | --- | --- | --- |
| Revenue | [CCY] [X]bn ([+/-X]% YoY) | [FY/1H/Q YYYY] | [n] |
| Operating margin | [X]% ([+/-X]pp YoY) | [Period] | [n] |
| Net margin | [X]% | [Period] | [n] |
| EPS vs consensus | [CCY] [X] vs [CCY] [X] | [Period] | [n] |
| [Key business KPI] | [Value] | [Period] | [n] |

[One sentence on what the figures say].

**Peer Comparison**:

| Company | Mkt cap (USD) | P/E ([fwd/ttm]) | EV/EBITDA ([fwd/ttm]) | P/S | Src |
| --- | --- | --- | --- | --- | --- |
| **[Short name] ([Ticker])** | **[X]bn** | **[X]x** | **[X]x** | **[X]x** | [n] |
| [Short name] ([Ticker]) | [X]bn | [X]x | [X]x | [X]x | [n] |
| **Peer median** | **[X]bn** | **[X]x** | **[X]x** | **[X]x** | |

*Market caps converted at FX rates as of [DD MMM YYYY]. [Exchanges that differ from the subject's]. [Each n/a: what was checked].*

[Premium/discount to the peer median on the key multiple, and why].

**Forward Outlook**: [Management guidance, analyst consensus, growth projections with specific numbers]

## CATALYST ANALYSIS

```
[Mon YYYY]   [▲/▼/◆]  [Short catalyst label]
[H2 YYYY]    [▲/▼/◆]  [Short catalyst label]
```

| Catalyst | Timing | Expected impact | Src |
| --- | --- | --- | --- |
| **Near-term (0-6m)** | | | |
| [Earnings, product launch, regulatory decision] | [DD MMM YYYY or period] | [▲ Positive / ▼ Negative / ◆ Binary]: [few words] | [n] |
| **Medium-term (6-24m)** | | | |
| [Strategic initiative, market expansion, competitive shift] | [Period] | [Impact] | [n] |
| **Event-driven** | | | |
| [M&A, index inclusion, spin-off, special dividend] | [Period or undated] | [Impact] | [n] |

## VALUATION & PRICE TARGETS
Current consensus: [CCY] [X] (range [CCY] [low]-[high]) [n].

| Scenario | Price ([CCY]) | Key assumption | Probability | Src |
| --- | --- | --- | --- | --- |
| Bull | [X] | [Specific scenario: multiple on forward figure, DCF driver, NAV discount] | [X]% | [n] |
| Base | [X] | [Scenario] | [Y]% | [n] |
| Bear | [X] | [Risk scenario] | [Z]% | [n] |
| **Probability-weighted target** | **[X]** | | **100%** | |

*[FX rate and date, where the valuation mixes currencies].*

## RISK ASSESSMENT
**Company risks**: [Specific business risks - competitive threats, regulatory issues, operational challenges]

**Macro risks**: [Interest rate sensitivity, economic cycle impact, sector rotation effects]

**Position sizing**: [X]%-[Y]% allocation based on [volatility/beta/risk factors].

**ESG considerations**: [If material to institutional ownership].

## TECHNICAL CONTEXT & OPTIONS INTELLIGENCE
**Price action**: [Current price vs 52-week range]. [Key support/resistance levels]. [Moving averages].

**Momentum & volume**: [RSI and other momentum indicators, trend]. [Recent volume patterns].

**Options flow**: [Put/call ratios, unusual activity, implied volatility trends].

## MARKET POSITIONING
**Sector performance**: [Stock performance vs sector ETF and broader market with specific %].

**Rotation & relative strength**: [Rotation trends affecting the position]. [Relative strength analysis].

## INSIDER SIGNALS
**Insider dealings**: [Recent insider buying/selling with specific values and executives]. [Pattern across them].

**Buybacks**: [Share buyback programme and progress against its mandate].

**Institutional ownership**: [Notable institutional ownership changes].

## SOURCES
[n]. [Title] - [Publisher], [DD MMM YYYY]. [URL]
````
