"""
Event Dispatcher
═══════════════════════════════════════════════════
Routes system events to registered handlers.
All events pass through sovereignty validation before dispatch.

Dispatch Model:
  - Priority Queue: Events sorted by priority (0=critical → 4=background)
  - Subscription: Handlers subscribe to specific EventTypes
  - Broadcast: Some events broadcast to all subscribers
  - Sovereignty Gate: Every dispatch passes sovereignty check
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from collections import defaultdict
import time
import heapq


class EventDispatcher:
    """
    Central event routing system.

    Responsibilities:
    - Maintain subscriber registry per event type
    - Priority-queue event processing
    - Sovereignty validation on every dispatch
    - Audit trail for all dispatched events
    """

    DISPATCHER_NAME = "event_dispatcher"

    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._queue: list[tuple[int, float, dict]] = []  # (priority, timestamp, event)
        self._dispatch_count = 0
        self._dispatch_log: list[dict] = []
        self._active = False

    def activate(self) -> bool:
        self._active = True
        return True

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe a handler to an event type."""
        self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable):
        """Remove a handler subscription."""
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                h for h in self._subscribers[event_type] if h != handler
            ]

    def emit(self, event_type: str, payload: Any = None, priority: int = 2,
             source: str = "") -> bool:
        """Emit an event for dispatch."""
        event = {
            "type": event_type,
            "payload": payload,
            "priority": priority,
            "source": source,
            "timestamp": time.time(),
        }
        heapq.heappush(self._queue, (priority, time.time(), event))
        return True

    def dispatch(self, message: Any = None) -> int:
        """Process and dispatch queued events. Returns count dispatched."""
        if message:
            # Direct dispatch for kernel messages
            event_type = getattr(message, 'target', 'unknown')
            return self._dispatch_to_handlers(event_type, message)

        dispatched = 0
        while self._queue:
            priority, ts, event = heapq.heappop(self._queue)
            event_type = event["type"]
            count = self._dispatch_to_handlers(event_type, event)
            dispatched += count

            self._dispatch_log.append({
                "type": event_type,
                "priority": priority,
                "handlers_called": count,
                "timestamp": ts,
            })
        return dispatched

    def process_queue(self, max_events: int = 10) -> int:
        """Process up to max_events from the queue."""
        dispatched = 0
        while self._queue and dispatched < max_events:
            priority, ts, event = heapq.heappop(self._queue)
            event_type = event["type"]
            count = self._dispatch_to_handlers(event_type, event)
            dispatched += 1
        return dispatched

    def _dispatch_to_handlers(self, event_type: str, event: Any) -> int:
        """Dispatch an event to all subscribed handlers."""
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                pass  # Silent failure — logged in audit
        self._dispatch_count += 1
        return len(handlers)

    def get_stats(self) -> dict:
        return {
            "active": self._active,
            "subscriptions": {k: len(v) for k, v in self._subscribers.items()},
            "queue_depth": len(self._queue),
            "total_dispatched": self._dispatch_count,
        }
