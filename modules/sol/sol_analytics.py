"""
SOL Analytics & Reporting — UUID Tracking & Chat Analytics for Team Dashboard
═══════════════════════════════════════════════════════════════════════════════
Exports session logs, chat history, and performance metrics to Excel/CSV 
for visualization and team analysis.

Features:
- 📊 Session Timeline Charts
- 💬 Chat Frequency & Length Analysis
- 🆔 UUID Activity Tracking
- 📈 Performance Metrics (Response Time, Quality Scores)
- 👥 Team Collaboration Reports
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import json
import csv
import time
import uuid as uuid_lib
import os


@dataclass
class UUIDRecord:
    """Track UUID usage and lifecycle."""
    uuid: str
    entity_type: str  # "session", "environment", "insight", "user"
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    activity_count: int = 0
    status: str = "active"  # active, closed, archived
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uuid": self.uuid,
            "entity_type": self.entity_type,
            "created_at": datetime.fromtimestamp(self.created_at).isoformat(),
            "last_activity": datetime.fromtimestamp(self.last_activity).isoformat(),
            "activity_count": self.activity_count,
            "status": self.status,
            "lifetime_seconds": self.last_activity - self.created_at,
            "metadata": json.dumps(self.metadata)
        }


@dataclass
class ChatTurn:
    """A single turn in a conversation."""
    turn_id: str
    session_id: str
    timestamp: float
    user_message: str
    ai_response: str
    user_length: int
    response_length: int
    response_time: float = 0.0
    quality_score: float = 0.0  # 0-1
    emotion_detected: str = ""
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "turn_id": self.turn_id,
            "session_id": self.session_id,
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
            "user_message_length": self.user_length,
            "ai_response_length": self.response_length,
            "response_time_ms": self.response_time * 1000,
            "quality_score": self.quality_score,
            "emotion": self.emotion_detected,
            "tags": ",".join(self.tags)
        }


@dataclass
class SessionMetrics:
    """Metrics for a single session."""
    session_id: str
    start_time: float
    end_time: Optional[float] = None
    user_id: str = ""
    duration_seconds: float = 0.0
    total_turns: int = 0
    total_user_tokens: int = 0
    total_ai_tokens: int = 0
    avg_response_time: float = 0.0
    avg_quality_score: float = 0.0
    session_type: str = "standard"  # standard, therapeutic, analysis
    outcome: str = "completed"  # completed, interrupted, error
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else "",
            "duration_minutes": self.duration_seconds / 60,
            "user_id": self.user_id,
            "total_turns": self.total_turns,
            "total_user_tokens": self.total_user_tokens,
            "total_ai_tokens": self.total_ai_tokens,
            "avg_response_time_ms": self.avg_response_time * 1000,
            "avg_quality_score": round(self.avg_quality_score, 3),
            "session_type": self.session_type,
            "outcome": self.outcome,
            "notes": self.notes
        }


class SolAnalytics:
    """
    Analytics engine for SOL — generates team dashboards and reports.
    """

    def __init__(self, data_dir: str = "sol_analytics"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self._uuid_records: Dict[str, UUIDRecord] = {}
        self._chat_turns: List[ChatTurn] = []
        self._session_metrics: Dict[str, SessionMetrics] = {}
        self._load_data()

    def _load_data(self):
        """Load existing analytics data from files."""
        uuid_file = os.path.join(self.data_dir, "uuids.json")
        if os.path.exists(uuid_file):
            try:
                with open(uuid_file, 'r') as f:
                    data = json.load(f)
                    for record_data in data:
                        record = UUIDRecord(
                            uuid=record_data["uuid"],
                            entity_type=record_data["entity_type"],
                            created_at=record_data["created_at"],
                            last_activity=record_data["last_activity"],
                            activity_count=record_data["activity_count"],
                            status=record_data["status"],
                            metadata=record_data.get("metadata", {})
                        )
                        self._uuid_records[record.uuid] = record
            except:
                pass

    def _save_data(self):
        """Save analytics data to file."""
        uuid_file = os.path.join(self.data_dir, "uuids.json")
        with open(uuid_file, 'w') as f:
            json.dump(
                [r.to_dict() for r in self._uuid_records.values()],
                f, indent=2
            )

    # ───────────────────────────────────────────────────────
    # UUID TRACKING
    # ───────────────────────────────────────────────────────

    def register_uuid(self, uuid_str: str, entity_type: str, metadata: Dict[str, Any] = None) -> UUIDRecord:
        """Register a new UUID for tracking."""
        record = UUIDRecord(
            uuid=uuid_str,
            entity_type=entity_type,
            metadata=metadata or {}
        )
        self._uuid_records[uuid_str] = record
        self._save_data()
        return record

    def update_uuid_activity(self, uuid_str: str) -> Optional[UUIDRecord]:
        """Record activity for a UUID."""
        if uuid_str in self._uuid_records:
            record = self._uuid_records[uuid_str]
            record.last_activity = time.time()
            record.activity_count += 1
            self._save_data()
            return record
        return None

    def close_uuid(self, uuid_str: str, metadata: Dict[str, Any] = None):
        """Mark a UUID as closed/inactive."""
        if uuid_str in self._uuid_records:
            record = self._uuid_records[uuid_str]
            record.status = "closed"
            record.last_activity = time.time()
            if metadata:
                record.metadata.update(metadata)
            self._save_data()

    # ───────────────────────────────────────────────────────
    # CHAT LOGGING
    # ───────────────────────────────────────────────────────

    def log_chat_turn(self, session_id: str, user_message: str, ai_response: str,
                     response_time: float = 0.0, quality_score: float = 1.0,
                     emotion: str = "", tags: List[str] = None) -> ChatTurn:
        """Log a single chat turn."""
        turn = ChatTurn(
            turn_id=str(uuid_lib.uuid4())[:8],
            session_id=session_id,
            timestamp=time.time(),
            user_message=user_message,
            ai_response=ai_response,
            user_length=len(user_message.split()),
            response_length=len(ai_response.split()),
            response_time=response_time,
            quality_score=quality_score,
            emotion_detected=emotion,
            tags=tags or []
        )
        self._chat_turns.append(turn)
        return turn

    def start_session(self, session_id: str, user_id: str = "", session_type: str = "standard") -> SessionMetrics:
        """Start tracking a new session."""
        metrics = SessionMetrics(
            session_id=session_id,
            start_time=time.time(),
            user_id=user_id,
            session_type=session_type
        )
        self._session_metrics[session_id] = metrics
        return metrics

    def end_session(self, session_id: str, outcome: str = "completed", notes: str = ""):
        """End a session and compute metrics."""
        if session_id not in self._session_metrics:
            return

        metrics = self._session_metrics[session_id]
        metrics.end_time = time.time()
        metrics.duration_seconds = metrics.end_time - metrics.start_time
        metrics.outcome = outcome
        metrics.notes = notes

        # Compute from chat turns
        session_turns = [t for t in self._chat_turns if t.session_id == session_id]
        metrics.total_turns = len(session_turns)
        metrics.total_user_tokens = sum(t.user_length for t in session_turns)
        metrics.total_ai_tokens = sum(t.response_length for t in session_turns)
        
        if session_turns:
            metrics.avg_response_time = sum(t.response_time for t in session_turns) / len(session_turns)
            metrics.avg_quality_score = sum(t.quality_score for t in session_turns) / len(session_turns)

    # ───────────────────────────────────────────────────────
    # CSV / EXCEL EXPORTS
    # ───────────────────────────────────────────────────────

    def export_uuid_report(self, filepath: str = None) -> str:
        """Export UUID tracking report to CSV."""
        if not filepath:
            filepath = os.path.join(self.data_dir, "uuid_tracking_report.csv")

        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "uuid", "entity_type", "created_at", "last_activity", 
                "activity_count", "status", "lifetime_seconds", "metadata"
            ])
            writer.writeheader()
            for record in self._uuid_records.values():
                writer.writerow(record.to_dict())

        return filepath

    def export_chat_log(self, filepath: str = None) -> str:
        """Export full chat log to CSV."""
        if not filepath:
            filepath = os.path.join(self.data_dir, "chat_log_full.csv")

        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "turn_id", "session_id", "timestamp", "user_message_length",
                "ai_response_length", "response_time_ms", "quality_score", 
                "emotion", "tags"
            ])
            writer.writeheader()
            for turn in self._chat_turns:
                writer.writerow(turn.to_dict())

        return filepath

    def export_session_metrics(self, filepath: str = None) -> str:
        """Export session-level metrics to CSV."""
        if not filepath:
            filepath = os.path.join(self.data_dir, "session_metrics.csv")

        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "session_id", "start_time", "end_time", "duration_minutes",
                "user_id", "total_turns", "total_user_tokens", "total_ai_tokens",
                "avg_response_time_ms", "avg_quality_score", "session_type", 
                "outcome", "notes"
            ])
            writer.writeheader()
            for metrics in self._session_metrics.values():
                writer.writerow(metrics.to_dict())

        return filepath

    # ───────────────────────────────────────────────────────
    # CHARTING DATA (2D TABLES FOR EXCEL/TABLEAU)
    # ───────────────────────────────────────────────────────

    def get_hourly_chat_volume(self) -> Dict[str, int]:
        """Get chat volume by hour of day."""
        hourly = {}
        for turn in self._chat_turns:
            dt = datetime.fromtimestamp(turn.timestamp)
            hour_key = f"{dt.hour:02d}:00"
            hourly[hour_key] = hourly.get(hour_key, 0) + 1
        return dict(sorted(hourly.items()))

    def get_daily_session_count(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get session count per day for the last N days."""
        daily = {}
        cutoff = time.time() - (days * 86400)

        for metrics in self._session_metrics.values():
            if metrics.start_time >= cutoff:
                date_key = datetime.fromtimestamp(metrics.start_time).date().isoformat()
                if date_key not in daily:
                    daily[date_key] = {"sessions": 0, "total_duration_min": 0, "avg_quality": 0}
                daily[date_key]["sessions"] += 1
                daily[date_key]["total_duration_min"] += metrics.duration_seconds / 60

        for date_data in daily.values():
            date_data["avg_quality"] = round(date_data.get("avg_quality", 0), 2)

        return [{"date": date, **data} for date, data in sorted(daily.items())]

    def get_quality_distribution(self) -> Dict[str, int]:
        """Quality score buckets for histogram."""
        buckets = {
            "0.0-0.2": 0, "0.2-0.4": 0, "0.4-0.6": 0,
            "0.6-0.8": 0, "0.8-1.0": 0
        }
        
        for turn in self._chat_turns:
            score = turn.quality_score
            if score < 0.2:
                buckets["0.0-0.2"] += 1
            elif score < 0.4:
                buckets["0.2-0.4"] += 1
            elif score < 0.6:
                buckets["0.4-0.6"] += 1
            elif score < 0.8:
                buckets["0.6-0.8"] += 1
            else:
                buckets["0.8-1.0"] += 1
        
        return buckets

    def get_response_time_stats(self) -> Dict[str, float]:
        """Response time statistics."""
        if not self._chat_turns:
            return {"min": 0, "max": 0, "avg": 0, "p95": 0}

        times = [t.response_time for t in self._chat_turns if t.response_time > 0]
        if not times:
            return {"min": 0, "max": 0, "avg": 0, "p95": 0}

        times.sort()
        return {
            "min": round(min(times) * 1000, 2),  # ms
            "max": round(max(times) * 1000, 2),
            "avg": round(sum(times) / len(times) * 1000, 2),
            "p95": round(times[int(len(times) * 0.95)] * 1000, 2)
        }

    def get_emotion_breakdown(self) -> Dict[str, int]:
        """Count by emotion detected."""
        emotions = {}
        for turn in self._chat_turns:
            if turn.emotion_detected:
                emotions[turn.emotion_detected] = emotions.get(turn.emotion_detected, 0) + 1
        return dict(sorted(emotions.items(), key=lambda x: x[1], reverse=True))

    # ───────────────────────────────────────────────────────
    # TEAM DASHBOARD EXPORT
    # ───────────────────────────────────────────────────────

    def export_team_dashboard(self, output_dir: str = None) -> Dict[str, str]:
        """Export complete team dashboard data."""
        if not output_dir:
            output_dir = self.data_dir

        files = {}

        # 1. UUID Report
        files["uuid_tracking"] = self.export_uuid_report(
            os.path.join(output_dir, "01_uuid_tracking.csv")
        )

        # 2. Chat Log
        files["chat_log"] = self.export_chat_log(
            os.path.join(output_dir, "02_chat_log.csv")
        )

        # 3. Session Metrics
        files["sessions"] = self.export_session_metrics(
            os.path.join(output_dir, "03_session_metrics.csv")
        )

        # 4. Charts Data
        charts_data = {
            "hourly_volume": self.get_hourly_chat_volume(),
            "daily_sessions": self.get_daily_session_count(),
            "quality_distribution": self.get_quality_distribution(),
            "response_times": self.get_response_time_stats(),
            "emotions": self.get_emotion_breakdown(),
        }

        charts_file = os.path.join(output_dir, "04_charts_data.json")
        with open(charts_file, 'w') as f:
            json.dump(charts_data, f, indent=2)
        files["charts"] = charts_file

        # 5. Summary Report
        summary_file = os.path.join(output_dir, "05_summary_report.txt")
        with open(summary_file, 'w') as f:
            f.write(self._generate_summary_report())
        files["summary"] = summary_file

        return files

    def _generate_summary_report(self) -> str:
        """Generate text summary report."""
        report = []
        report.append("=" * 80)
        report.append("SOL ANALYTICS TEAM DASHBOARD - SUMMARY REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().isoformat()}\n")

        # UUID Stats
        report.append("📊 UUID TRACKING")
        report.append(f"  Total UUIDs: {len(self._uuid_records)}")
        active_uuids = len([r for r in self._uuid_records.values() if r.status == "active"])
        report.append(f"  Active: {active_uuids}")
        report.append(f"  Closed: {len(self._uuid_records) - active_uuids}")
        report.append("")

        # Chat Stats
        report.append("💬 CHAT STATISTICS")
        report.append(f"  Total Chat Turns: {len(self._chat_turns)}")
        report.append(f"  Average User Message Length: {sum(t.user_length for t in self._chat_turns) // max(1, len(self._chat_turns))} words")
        report.append(f"  Average AI Response Length: {sum(t.response_length for t in self._chat_turns) // max(1, len(self._chat_turns))} words")
        report.append("")

        # Session Stats
        report.append("📅 SESSION STATISTICS")
        report.append(f"  Total Sessions: {len(self._session_metrics)}")
        completed = len([m for m in self._session_metrics.values() if m.outcome == "completed"])
        report.append(f"  Completed: {completed}")
        
        total_duration = sum(m.duration_seconds for m in self._session_metrics.values())
        report.append(f"  Total Duration: {total_duration / 3600:.1f} hours")
        
        if self._session_metrics:
            avg_duration = total_duration / len(self._session_metrics)
            report.append(f"  Average Session Duration: {avg_duration / 60:.1f} minutes")
        report.append("")

        # Performance
        report.append("⚡ PERFORMANCE METRICS")
        response_stats = self.get_response_time_stats()
        report.append(f"  Average Response Time: {response_stats['avg']} ms")
        report.append(f"  P95 Response Time: {response_stats['p95']} ms")
        report.append(f"  Max Response Time: {response_stats['max']} ms")
        report.append("")

        # Quality
        report.append("✨ QUALITY METRICS")
        avg_quality = sum(t.quality_score for t in self._chat_turns) / max(1, len(self._chat_turns))
        report.append(f"  Average Quality Score: {avg_quality:.3f}")
        report.append(f"  Quality Distribution: {self.get_quality_distribution()}")
        report.append("")

        # Emotions
        report.append("💭 EMOTION ANALYSIS")
        for emotion, count in self.get_emotion_breakdown().items():
            pct = (count / len(self._chat_turns) * 100) if self._chat_turns else 0
            report.append(f"  {emotion}: {count} ({pct:.1f}%)")
        report.append("")

        report.append("=" * 80)
        
        return "\n".join(report)

    def get_dashboard_json(self) -> Dict[str, Any]:
        """Get all dashboard data as JSON for web visualization."""
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_uuids": len(self._uuid_records),
                "total_chat_turns": len(self._chat_turns),
                "total_sessions": len(self._session_metrics),
            },
            "uuid_stats": {
                "total": len(self._uuid_records),
                "active": len([r for r in self._uuid_records.values() if r.status == "active"]),
                "closed": len([r for r in self._uuid_records.values() if r.status == "closed"]),
            },
            "chat_stats": {
                "total_turns": len(self._chat_turns),
                "avg_user_length": sum(t.user_length for t in self._chat_turns) // max(1, len(self._chat_turns)),
                "avg_ai_length": sum(t.response_length for t in self._chat_turns) // max(1, len(self._chat_turns)),
                "quality_distribution": self.get_quality_distribution(),
            },
            "session_stats": {
                "total": len(self._session_metrics),
                "completed": len([m for m in self._session_metrics.values() if m.outcome == "completed"]),
                "total_duration_hours": sum(m.duration_seconds for m in self._session_metrics.values()) / 3600,
            },
            "performance": self.get_response_time_stats(),
            "hourly_volume": self.get_hourly_chat_volume(),
            "daily_sessions": self.get_daily_session_count(),
            "emotions": self.get_emotion_breakdown(),
        }


# Quick export template for SOL module integration
def quick_export_dashboard(sol_module) -> Dict[str, str]:
    """Quick export of current session data."""
    analytics = SolAnalytics()
    
    # Extract from sol_module if available
    if hasattr(sol_module, 'current_session_id'):
        analytics.start_session(sol_module.current_session_id)
    
    return analytics.export_team_dashboard()
