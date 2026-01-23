# Systematic Strategy Construction

## **THE COMPLETE SYSTEMATIC TRADING PIPELINE**

### **1. Universe Definition**
What assets/instruments are eligible for trading?
- Treasury futures (ZN, ZB, ZF)
- VIX futures complex
- Cryptocurrency spot/futures
- ETFs, stocks, options, etc.

**Constraints:** liquidity minimums, broker access, margin requirements

---

### **2. Data Layer**
Raw market data and reference information:
- **Market data**: OHLCV, bid/ask, order book
- **Reference data**: contract specs, expiration dates, roll schedules
- **Fundamental data**: earnings, economic releases, positioning reports
- **Alternative data**: sentiment, flows, on-chain metrics

---

### **3. Feature Engineering**
Transform raw data into meaningful variables:

**Price features:**
- Returns (log returns, simple returns)
- Moving averages (SMA, EMA, adaptive)
- Volatility (realized, implied, GARCH)
- Momentum indicators (RSI, MACD, rate-of-change)

**Structural features:**
- VIX term structure slope (M1-M2 spread)
- Treasury yield curve (2s10s, 5s30s)
- Roll yield/carry
- Basis (futures vs spot)

**Cross-sectional features:**
- Relative strength vs peers
- Factor exposures (value, momentum, quality)
- Correlation/cointegration relationships

**Statistical features:**
- Z-scores, percentile ranks
- Principal components
- Regime probabilities

**In your work:** The VIX curve slope, Treasury MA crossovers, month-end effects are all features.

---

### **4. Signal Generation**
Process features into actionable trade recommendations:

**Types of signals:**
- **Directional**: +1 (long), -1 (short), 0 (flat)
- **Continuous**: score from -1 to +1 indicating conviction
- **Target weights**: desired portfolio allocation percentages
- **Target volatility**: desired volatility contribution

**Signal examples:**
- "SMA(20) > SMA(60)" → +1 (long signal)
- Z-score of term structure → continuous signal from -2 to +2
- Momentum rank → portfolio weight proportional to rank

**Key point:** A signal is NOT yet a strategy—it's just a predictive output or target.

---

### **5. STRATEGY Level**
**A strategy is a complete, self-contained trading approach with specific objective and logic.**

**Components of a strategy:**
1. **Objective**: What is it trying to achieve? (trend capture, mean reversion, carry harvest, tail hedge)
2. **Signal logic**: How does it generate trade recommendations?
3. **Entry/exit rules**: When to establish and close positions
4. **Filters**: Under what conditions is the strategy active?
5. **Position sizing**: How much capital/risk per trade?
6. **Rebalancing rules**: How often to adjust positions?

**Examples from your PSOF:**

**BALL Strategy:**
- **Objective**: Capture Treasury futures trends
- **Signal**: MA crossover + month-end effects
- **Filters**: Trend strength threshold, regime detection
- **Sizing**: Fixed vol target per position
- **Rebalance**: Daily or at signal changes

**VIXVOL Strategy:**
- **Objective**: Harvest VIX term structure premium
- **Signal**: Front-month vs back-month spread
- **Filters**: Minimum contango, not during stress
- **Sizing**: Based on curve steepness
- **Rebalance**: Daily or at roll

**SWAN Strategy:**
- **Objective**: Tail risk protection
- **Signal**: VIX option strikes based on portfolio exposure
- **Filters**: Active during elevated vol regimes
- **Sizing**: Percentage of NAV for premium budget
- **Rebalance**: Monthly or at regime shift

Each strategy is independent and could run standalone. Each has its own P&L, Sharpe ratio, drawdown profile.

---

### **6. Filters / Regime Detection**
Conditional logic that modulates strategy behavior:

**Strategy-level filters:**
- **Participation filters**: "Only trade BALL when not in crisis regime"
- **Signal filters**: "Only take longs when overall market trend > 0"
- **Risk filters**: "Reduce size when portfolio vol > 20%"

**System-level filters:**
- **Market regime**: Risk-on vs risk-off (affects all strategies)
- **Liquidity regime**: Normal vs stressed (affects execution)
- **Volatility regime**: Low/medium/high (affects leverage)

**In your Continuum Allocator:** The regime detection (VIX slope, momentum, vol) is a filter determining UPRO vs TMF allocation.

---

### **7. SYSTEM / PORTFOLIO Level**
**A system is the overarching framework that combines multiple strategies into a unified portfolio.**

**THIS IS THE KEY DISTINCTION:**
- **Strategy** = single approach with one objective (BALL, VIXVOL, SWAN)
- **System** = portfolio of strategies with allocation rules (PSOF)

**System-level decisions:**

**A. Strategy Allocation**
How to divide capital among strategies:
- **Fixed weights**: 25% BALL, 25% LSVS, 25% SWAN, 25% VIXVOL
- **Volatility parity**: equal risk contribution from each
- **Dynamic weights**: based on regime, recent performance, correlations
- **Risk budgets**: allocate based on Sharpe ratio or expected returns

**B. Portfolio Construction**
- **Diversification**: ensure strategies aren't redundant
- **Correlation management**: adjust for changing strategy correlations
- **Capital efficiency**: use leverage/overlay strategies when appropriate
- **Notional exposure**: aggregate across strategies to manage gross/net

**C. Rebalancing**
- **Frequency**: daily, weekly, monthly
- **Triggers**: drift from target weights, regime changes, signal strength
- **Transaction cost awareness**: avoid excessive trading

**Your PSOF is a SYSTEM that combines:**
- BALL (Treasury trend)
- LSVS (likely low-vol long/short)
- SWAN (tail hedge)
- VIXVOL (term structure)

Each is a strategy; PSOF is the system managing them.

---

### **8. Risk Management**
Portfolio-wide controls (system level):

**Position limits:**
- Max gross exposure (e.g., 300% notional)
- Max net exposure (e.g., ±100%)
- Max single position (e.g., 50% of NAV)
- Concentration limits by asset class

**Volatility management:**
- Target portfolio volatility (e.g., 15% annualized)
- Dynamic leverage: scale up in low vol, down in high vol
- VaR limits, stress loss limits

**Drawdown controls:**
- Max drawdown threshold (e.g., -20%)
- Circuit breakers: reduce exposure or shut down
- Recovery protocols: how to scale back in

**Correlation/factor exposure:**
- Limit beta to SPY, aggregate bond duration
- Manage factor tilts (momentum, value, carry)

---

### **9. Execution Layer**
How signals become actual trades:

**Pre-trade:**
- **Order generation**: convert target positions to order quantities
- **Timing**: MOC, MOO, VWAP, TWAP, aggressive/passive
- **Cost estimation**: expected slippage + commissions

**Trade:**
- **Order routing**: broker selection, venue
- **Execution algorithms**: minimize market impact
- **Fills**: partial fills, cancel/replace logic

**Post-trade:**
- **Transaction cost analysis**: actual vs expected
- **Attribution**: P&L decomposition by strategy, factor, alpha/beta
- **Reconciliation**: positions vs expected, cash accounting

---

## **CONCRETE EXAMPLE: BALL Strategy in PSOF System**

Let's trace a single trade through the full pipeline:

**1. Universe:** Treasury futures (ZN, ZB, ZF)

**2. Data:** Daily OHLC for ZN from Bloomberg

**3. Features:**
- 20-day SMA of ZN close
- 60-day SMA of ZN close
- Month-end dummy (1 if within 3 days of month-end, else 0)
- 10-day realized volatility

**4. Signal:**
```
if SMA(20) > SMA(60) and month_end == 1:
    signal = +1  # Long
elif SMA(20) < SMA(60):
    signal = -1  # Short
else:
    signal = 0   # Flat
```

**5. BALL Strategy:**
- **Objective:** Capture Treasury trends with month-end boost
- **Entry:** When signal changes from 0 or -1 to +1 (or vice versa)
- **Position size:** Target 10% portfolio volatility contribution
- **Filters:**
  - Only active if VIX < 35 (not crisis mode)
  - Minimum trend strength (20MA must be >0.5% from 60MA)
- **Rebalance:** Daily

**6. System-level (PSOF):**
- BALL gets 25% of system risk budget
- System currently in "neutral" regime → full allocation
- No portfolio-level overrides active
- BALL target = 25% * portfolio vol = 3.75% vol contribution

**7. Risk Management:**
- BALL wants 50 ZN contracts for 3.75% vol
- Check: doesn't violate max 100 contract limit ✓
- Check: gross exposure still under 300% ✓
- Check: not exceeding correlation budget with other strategies ✓
- Approved: 50 contracts

**8. Execution:**
- Current position: 30 long ZN
- Target: 50 long ZN
- Order: Buy 20 ZN at market-on-close
- Expected cost: $150 slippage + $40 commission
- Fill: 20 @ 110.15 (vs 110.14 mid)
- Actual cost: $200 + $40 = $240

**9. Attribution:**
- Next day: ZN up 0.3% = ~$3,000 gain
- Less transaction cost: $240
- Net P&L: $2,760 attributed to BALL strategy

---

## **STRATEGY vs SYSTEM: The Critical Distinction**

**STRATEGY = Single coherent trading approach**
- Has ONE objective (capture trends, harvest carry, hedge tail risk)
- Generates its own signals
- Has its own entry/exit/sizing logic
- Produces independent P&L stream
- Example: "20/60 MA crossover on Treasury futures"

**SYSTEM = Portfolio management framework**
- Combines MULTIPLE strategies
- Manages capital allocation across strategies
- Handles portfolio-level risk management
- Coordinates rebalancing and execution
- Produces aggregate P&L from all strategies
- Example: "PSOF combining BALL + LSVS + SWAN + VIXVOL"

**Yes, a system is a blend of strategies**, but it's more than just mixing them—it's the architecture that determines:
- How much capital each strategy gets
- When to increase/decrease strategy allocations
- How to manage interactions (if BALL and LSVS both want to short Treasuries)
- Portfolio-level constraints (max leverage, drawdown triggers)
- Unified execution and reporting

---

## **METAPHOR: Restaurant vs Restaurant Group**

- **Strategy** = A restaurant with specific cuisine (Italian, Japanese, BBQ)
  - Each has its own menu, chef, specialty
  - Each generates its own revenue
  - Each has its own customer base

- **System** = Restaurant group managing multiple restaurants
  - Decides how much capital to invest in each concept
  - Manages shared resources (supply chain, marketing, staff)
  - Optimizes portfolio for different neighborhoods/demographics
  - Corporate oversight, consolidated financials

Your PSOF is the restaurant group. BALL, LSVS, SWAN, VIXVOL are the individual restaurants.

---

## **IN YOUR WORK**

When you're developing in Claude Code or Jupyter:

**Building a strategy:**
- Define features (VIX curve slope, MA crossovers)
- Create signal logic
- Add filters (regime detection)
- Backtest independently
- Measure standalone Sharpe, drawdown

**Building a system:**
- Combine strategies (BALL + LSVS + SWAN + VIXVOL)
- Determine allocation method (equal risk, tactical, regime-based)
- Add portfolio risk management
- Test aggregate performance
- Analyze diversification benefits, correlation structure

The pipeline clarity helps you modularize: debug strategy signal logic separately from system allocation logic separately from execution implementation.
