from collections import deque
from dataclasses import dataclass
from typing import Dict, Deque
import time

@dataclass
class PricePoint:
    timestamp: float
    usdt: float
    eur: float

class PriceTracker:
    def __init__(self, threshold_pct: float, window_min: float):
        self.threshold_pct = threshold_pct
        self.window_sec = window_min * 60
        self._history: Dict[str, Deque[PricePoint]] = {}

    def record(self, symbol: str, prices: dict) -> None:
        if symbol not in self._history:
            self._history[symbol] = deque()
        self._history[symbol].append(
            PricePoint(timestamp=time.time(), usdt=prices["usdt"], eur=prices["eur"])
        )
        self._evict_old(symbol)

    def _evict_old(self, symbol: str) -> None:
        cutoff = time.time() - self.window_sec
        dq = self._history[symbol]
        while dq and dq[0].timestamp < cutoff:
            dq.popleft()

    def get_snapshot(self, symbol: str, day_open: float) -> dict:
        dq = self._history.get(symbol)
        if not dq:
            return {"symbol": symbol, "usdt": 0.0, "eur": 0.0,
                    "change_day_pct": 0.0, "change_spike_pct": 0.0, "spike_alert": False}

        latest = dq[-1]
        oldest = dq[0]

        change_day_pct = ((latest.usdt - day_open) / day_open * 100) if day_open else 0.0
        change_spike_pct = (
            (latest.usdt - oldest.usdt) / oldest.usdt * 100
            if oldest.usdt else 0.0
        )

        return {
            "symbol": symbol,
            "usdt": latest.usdt,
            "eur": latest.eur,
            "change_day_pct": round(change_day_pct, 2),
            "change_spike_pct": round(change_spike_pct, 2),
            "spike_alert": abs(change_spike_pct) >= self.threshold_pct,
        }
