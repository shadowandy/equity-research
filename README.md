# stock-evaluation

An agent skill, `equity-research`, that writes institutional-style equity research reports on listed stocks. Name a ticker and ask for an analysis, rating, price target or buy/sell/hold call. The skill researches the stock live on the web and writes a structured report in which every figure is cited.

> Reports are LLM-generated and for educational purposes only. They are not investment advice.

## What a report contains

Each report follows a fixed structure:

- **Executive summary**: BUY / HOLD / SELL rating, a 12-month price target and the upside or downside %
- **Fundamental analysis**: recent financials, peer valuation multiples, guidance and consensus
- **Catalysts**: near-term, medium-term and event-driven
- **Valuation**: bull, base and bear targets, each tied to a stated assumption, with probability weights that reproduce the headline target
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

The skill handles stocks that trade on more than one counter (SGX SGD/USD, HKEX HKD/RMB, ADR vs home listing) and companies that report in a different currency from the one their shares trade in.

## Install

The skill needs web search and web fetch tools.

**Claude Code**: copy the skill folder into your personal or project skills directory:

```sh
git clone https://github.com/shadowandy/stock-evaluation.git
cp -r stock-evaluation/skills/equity-research ~/.claude/skills/
```

**Claude apps**: download `equity-research-<version>.zip` from the [latest release](https://github.com/shadowandy/stock-evaluation/releases/latest) and upload it in the Skills settings.

## Usage

```
Analyse D05
Give me a buy/sell/hold call on 0700 with a price target
Evaluate SHEL and AAPL
```

When a request names several tickers, the skill writes one report per ticker. Each report is saved to `reports/<TICKER>-<YYYY-MM-DD>.md` in the current directory and also shown in chat. If an earlier report on the same ticker exists, the new report says what changed in the rating, the target and the reasoning behind them.

`reports/` is git-ignored in this repo.

## Releasing

The [release workflow](.github/workflows/release-skill.yml) runs when a `v*` tag is pushed:

```sh
git tag v1.0.0
git push origin v1.0.0
```

It checks that the `SKILL.md` header is valid YAML, zips `skills/equity-research/` (with the `equity-research/` folder at the top of the archive) and attaches the zip to a GitHub release for that tag. It can also be run by hand from the Actions tab.

## Repository layout

```
skills/equity-research/   the skill (SKILL.md and per-market notes)
.github/workflows/        release packaging
docs/agents/              conventions for agents working on this repo
AGENTS.md                 agent instructions
```
