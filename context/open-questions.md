# Open Questions

Questions, decisions, or items that need follow-up.

---

## ~~Slack Bot Setup~~ RESOLVED

**Issue:** Can't send DMs to bot - "Sending messages to this app has been turned off"

**Resolution:** Bot started working overnight on 2026-01-23. Root cause unknown but issue resolved.

**Enhancement Added:** Updated bot to accept unstructured messages. Can now send any text and it will be captured as "raw" type for review during check-in.

## Flow Trade System - Research Process

**Challenge:** So many levers to pull on this project - having trouble figuring out where to start and how to confirm that research being done is reliable and accurate.

**Core Question:** What's the right process from idea generation to thoroughly vetted tradable strategy?

**Specific Problem:** Can't trust that backtests are being done correctly. This is where it's falling down.

**Considerations:**
- Need systematic approach to evaluate which levers to pull first
- Need validation framework to ensure research is reliable
- Need backtest verification methodology - how to know if the backtest implementation is correct?
- Project is highest-importance but complexity is causing paralysis

**Specific Validation Issue - Futures Return Methodology:**
- Historically used percent returns for backtesting, but this may not apply to futures
- In futures: every point of change = same dollar P&L regardless of asset price (e.g., 1 tick in ZN is always worth $15.625 regardless of whether ZN is at 110 or 120)
- Percent returns assume proportional P&L to price level, which doesn't match futures mechanics
- Need to confirm proper return calculation method for futures backtesting framework
- **Impact:** If using wrong return methodology, all historical backtest results could be invalid

