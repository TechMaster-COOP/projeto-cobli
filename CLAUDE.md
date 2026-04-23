# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
# Activate the virtual environment first
.venv\Scripts\activate  # Windows

# Run the Streamlit dashboard
streamlit run app.py
```

There is no build step, test suite, or linter configured.

## GitHub Repository

Repositório: **https://github.com/TechMaster-COOP/projeto-cobli**

### Auto-sync com GitHub

Um hook `PostToolUse` em `.claude/settings.json` faz commit e push automático após cada edição de arquivo (ferramentas `Edit`, `Write`, `NotebookEdit`). O commit usa a mensagem `auto: update via Claude Code [timestamp]`.

O hook só faz commit quando há alterações reais (`git status --porcelain`). Para que o hook esteja ativo em uma nova sessão do Claude Code, abra `/hooks` uma vez após iniciar a sessão (recarrega as configurações).

Para commitar manualmente:
```powershell
git add -A
git commit -m "sua mensagem"
git push
```

## Architecture

This is a **Streamlit financial dashboard** that displays real-time and historical stock prices for Petrobras (PETR4.SA), Itaú Unibanco (ITUB4.SA), and Nvidia (NVDA). All UI labels are in Portuguese.

**Data flow:**
1. `app.py` orchestrates the page — reads user controls from `components/sidebar.py`, fetches data via `data/fetcher.py`, renders a tab per stock, and renders a cross-stock comparison at the bottom.
2. `data/fetcher.py` wraps `yfinance` with a `@st.cache_data(ttl=300)` decorator so API calls are cached for 5 minutes.
3. `charts/` — four Plotly chart modules (`price_chart`, `volume_chart`, `return_chart`, `comparison_chart`), all using the `plotly_dark` template.
4. `components/metric_card.py` — renders four KPI tiles per stock (price, market cap, 52-week high/low) plus a live market-open indicator.
5. `utils/formatters.py` — currency formatting (R$ BRL / US$ USD), large-number abbreviation (T/B/M/K), and percentage formatting.

**Configuration** (`config.py`):
- `TICKERS` — symbol → label + chart color
- `PERIODS` — period key → human label + yfinance interval
- `CURRENCY_MAP` — symbol → "BRL" or "USD"
- `AUTO_REFRESH_SECONDS = 300`

All configuration (tickers, colors, periods) lives in `config.py`. Adding a new stock means updating `TICKERS` and `CURRENCY_MAP` there; no other files need changing unless a new chart type is required.
