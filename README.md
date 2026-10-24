# equity-research

An agent skill, `equity-research`, that writes institutional-style equity research reports on listed stocks. Name a ticker and ask for an analysis, rating, price target or buy/sell/hold call. The skill researches the stock live on the web and writes a structured report in which every figure is cited.

> Reports are LLM-generated and for educational purposes only. They are not investment advice.

## What a report contains

Each report follows a fixed structure:

- **Executive summary**: BUY / HOLD / SELL rating, a 12-month price target and the upside or downside %
- **Fundamental analysis**: a key-figures table of recent financials, a peer valuation table (sector-specific multiples, with a peer median row), guidance and consensus
- **Catalysts**: a plain-text timeline of dated catalysts, then a table of near-term, medium-term and event-driven catalysts with timing and expected impact (▲ positive, ▼ negative, ◆ binary)
- **Valuation**: a table of bull, base and bear targets, each tied to a stated assumption, with probability weights that reproduce the headline target
- **Risk assessment**: company and macro risks, position sizing, ESG where material
- **Technicals and options**: 52-week range, support and resistance, momentum, put/call ratio, implied volatility
- **Market positioning and insider signals**: performance against the sector, insider dealings, buybacks, institutional ownership
- **Sources**: a numbered list; every `[n]` marker in the report points into it

Every figure carries its timeframe and a citation. When a figure can't be found, the report says what was checked instead of estimating it. Proxies (e.g. US ADR options data for a Hong Kong listing) are used only when labelled as proxies.

The rating follows from the target: BUY above +15% upside, SELL below −10%, HOLD in between. Any deviation must be explained in the executive summary.

## Supported markets

Each exchange has its own notes covering where filings are announced, how often companies report, how insider dealings are disclosed, the currency conventions and the benchmark indices:

| Exchange | Notes |
| --- | --- |
| SGX | [`markets/sgx.md`](skills/equity-research/markets/sgx.md) |
| LSE | [`markets/lse.md`](skills/equity-research/markets/lse.md) |
| HKEX | [`markets/hkex.md`](skills/equity-research/markets/hkex.md) |
| NYSE / NASDAQ | [`markets/us.md`](skills/equity-research/markets/us.md) |
| Anything else | [`markets/other.md`](skills/equity-research/markets/other.md): a checklist for working out these facts for an unfamiliar exchange |

ETFs, unit trusts and other listed funds get their own [notes](skills/equity-research/funds.md): fund-level metrics (NAV, TER, tracking, distributions), fund peers, and fund flows in place of insider dealings.

The skill handles stocks that trade on more than one counter (SGX SGD/USD, HKEX HKD/RMB, ADR vs home listing) and companies that report in a different currency from the one their shares trade in.

## Install

The skill needs web search and web fetch tools.

**Coding agents (Claude Code and others)**: install with the [`skills`](https://github.com/vercel-labs/skills) CLI (Node.js 22.20+):

```sh
npx skills add shadowandy/equity-research
```

The skill installs into the current project; add `-g` to make it available in every project.

**claude.ai and gemini.google.com**: download [`equity-research.zip`](https://github.com/shadowandy/equity-research/releases/latest/download/equity-research.zip) and upload it in the Skills settings (claude.ai) or when creating a skill (Gemini web app or Mac app). The link always points at the [latest release](https://github.com/shadowandy/equity-research/releases/latest).

## Usage

```
Analyse D05
Give me a buy/sell/hold call on 0700 with a price target
Evaluate SHEL and AAPL
```

Research runs in parallel where the agent allows it: one subagent per ticker, and within each report the financial, positioning and technical/insider search passes run at the same time. Agents without subagents still batch independent searches together.

When a request names several tickers, the skill writes one report per ticker. Each report is saved to `reports/<TICKER>-<YYYY-MM-DD>.md` in the current directory and also shown in chat. If an earlier report on the same ticker exists, the new report says what changed in the rating, the target and the reasoning behind them.

`reports/` is git-ignored in this repo.

## Releasing

Every push to `main` that changes `skills/equity-research/` publishes a new release automatically. The [release workflow](.github/workflows/release-skill.yml) bumps the patch version (`v1.0.0` → `v1.0.1`), checks that the `SKILL.md` header is valid YAML, and attaches `equity-research.zip` (the `equity-research/` skill folder at the zip root), which both claude.ai and gemini.google.com accept.

To pick a different version (e.g. a minor or major bump), push the tag yourself or run the workflow from the Actions tab and enter a tag:

```sh
git tag v1.1.0
git push origin v1.1.0
```

## Repository layout

```
skills/equity-research/   the skill (SKILL.md, per-market notes, fund notes)
.github/workflows/        release packaging
docs/agents/              conventions for agents working on this repo
AGENTS.md                 agent instructions
```
