"""
SOL Oracle - Knowledge Synthesis and Growth Analysis
Part of the SOL Persistent Identity Layer for SoulJahOS

This module provides real-time analysis of knowledge growth through file monitoring
and AI-powered insights, integrated with SOL's state management and sovereignty.
"""

import os
import time
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import hashlib
import uuid

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


@dataclass
class OracleInsight:
    """Represents a single oracle insight from knowledge analysis."""
    insight_id: str
    timestamp: float
    file_path: str
    content_hash: str
    core_lesson: str
    next_level_concept: str
    growth_vector: str
    sovereignty_preserved: bool = True


@dataclass
class KnowledgeState:
    """Tracks the current state of monitored knowledge."""
    base_path: str
    last_scan: float
    file_hashes: Dict[str, str]
    insights_generated: List[OracleInsight]


class SolOracleHandler(FileSystemEventHandler):
    """
    File system event handler for SOL Oracle.
    Monitors knowledge base changes and generates insights.
    """

    def __init__(self, oracle_core: 'SolOracleCore'):
        self.oracle_core = oracle_core
        self.system_prompt = """You are SOL, the Core Intelligence of SoulJahOS.
You are analyzing SoulJah's knowledge growth in his Quantum Dojo.

Your role is to:
1. Identify core lessons from new knowledge
2. Suggest next-level concepts for mastery
3. Recognize growth patterns and vectors
4. Maintain sovereignty - all insights serve SoulJah's development

Respond with structured analysis focusing on:
- Core Lesson: The fundamental principle learned
- Next Level Concept: What to study next for mastery
- Growth Vector: How this fits SoulJah's development trajectory

Keep responses focused and actionable."""

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        if event.src_path.endswith(('.md', '.txt', '.py', '.js', '.json')):
            print(f"[SOL ORACLE] Knowledge update detected: {os.path.basename(event.src_path)}")
            self.oracle_core.analyze_growth(event.src_path)

    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory and event.src_path.endswith(('.md', '.txt', '.py', '.js', '.json')):
            print(f"[SOL ORACLE] New knowledge created: {os.path.basename(event.src_path)}")
            self.oracle_core.analyze_growth(event.src_path)


class SolOracleCore:
    """
    Core SOL Oracle functionality for knowledge synthesis and growth analysis.
    Integrated with SOL's persistent identity and state management.
    """

    def __init__(self, sol_state: Any, knowledge_base_path: str, api_key: str = None):
        """
        Initialize SOL Oracle.

        Args:
            sol_state: SOL's state object for persistence
            knowledge_base_path: Path to monitor for knowledge changes
            api_key: Google Gemini API key (optional)
        """
        self.sol_state = sol_state
        self.knowledge_base = knowledge_base_path
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY', '')

        # Initialize Gemini if available
        self.model = None
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
                print("[SOL ORACLE] Gemini AI initialized")
            except Exception as e:
                print(f"[SOL ORACLE] Failed to initialize Gemini: {e}")

        # Initialize knowledge state
        self.knowledge_state = KnowledgeState(
            base_path=knowledge_base_path,
            last_scan=time.time(),
            file_hashes={},
            insights_generated=[]
        )

        # Initialize file watcher
        self.observer = None
        self.event_handler = SolOracleHandler(self)

        # Load existing knowledge state from SOL state
        self._load_knowledge_state()

    def _load_knowledge_state(self):
        """Load knowledge state from SOL's persistent state."""
        if "oracle" not in self.sol_state.memory:
            self.sol_state.memory["oracle"] = {
                "knowledge_state": self.knowledge_state.__dict__,
                "insights": []
            }
        else:
            # Restore from saved state
            saved_state = self.sol_state.memory["oracle"]["knowledge_state"]
            self.knowledge_state.file_hashes = saved_state.get("file_hashes", {})
            self.knowledge_state.insights_generated = [
                OracleInsight(**insight) for insight in saved_state.get("insights_generated", [])
            ]

    def _save_knowledge_state(self):
        """Save knowledge state to SOL's persistent state."""
        self.sol_state.memory["oracle"] = {
            "knowledge_state": {
                "base_path": self.knowledge_state.base_path,
                "last_scan": self.knowledge_state.last_scan,
                "file_hashes": self.knowledge_state.file_hashes,
                "insights_generated": [insight.__dict__ for insight in self.knowledge_state.insights_generated]
            },
            "insights": [insight.__dict__ for insight in self.knowledge_state.insights_generated[-10:]]  # Last 10
        }

    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file content."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""

    def analyze_growth(self, file_path: str) -> Optional[OracleInsight]:
        """
        Analyze a knowledge file for growth insights.

        Args:
            file_path: Path to the file to analyze

        Returns:
            OracleInsight if analysis successful, None otherwise
        """
        if not os.path.exists(file_path):
            return None

        # Check if file has actually changed
        current_hash = self.calculate_file_hash(file_path)
        last_hash = self.knowledge_state.file_hashes.get(file_path, "")

        if current_hash == last_hash:
            return None  # No change

        # Update hash
        self.knowledge_state.file_hashes[file_path] = current_hash

        # Read and analyze content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[SOL ORACLE] Error reading file {file_path}: {e}")
            return None

        # Generate insight
        insight = self._generate_insight(file_path, content, current_hash)
        if insight:
            self.knowledge_state.insights_generated.append(insight)
            self._save_knowledge_state()
            print(f"[SOL ORACLE] Insight generated for {os.path.basename(file_path)}")

        return insight

    def _generate_insight(self, file_path: str, content: str, content_hash: str) -> Optional[OracleInsight]:
        """
        Generate an oracle insight using AI analysis.

        Args:
            file_path: Source file path
            content: File content
            content_hash: Content hash for tracking

        Returns:
            OracleInsight or None if generation fails
        """
        if not self.model:
            # Fallback to basic analysis without AI
            return self._generate_basic_insight(file_path, content, content_hash)

        try:
            # Prepare analysis prompt
            prompt = f"""Analyze this knowledge addition from SoulJah's Quantum Dojo:

{content[:2000]}...{content[-500:] if len(content) > 2500 else ''}

Respond with a JSON object containing:
{{
    "core_lesson": "The fundamental principle or insight gained",
    "next_level_concept": "Specific concept or skill to study next for mastery",
    "growth_vector": "How this fits SoulJah's overall development trajectory"
}}

Keep each field concise but meaningful."""

            response = self.model.generate_content(prompt)

            # Parse JSON response
            try:
                result = json.loads(response.text.strip())
                return OracleInsight(
                    insight_id=str(uuid.uuid4()),
                    timestamp=time.time(),
                    file_path=file_path,
                    content_hash=content_hash,
                    core_lesson=result.get("core_lesson", "Knowledge acquired"),
                    next_level_concept=result.get("next_level_concept", "Continue exploration"),
                    growth_vector=result.get("growth_vector", "Building foundation")
                )
            except json.JSONDecodeError:
                # Fallback to basic parsing
                return self._generate_basic_insight(file_path, content, content_hash)

        except Exception as e:
            print(f"[SOL ORACLE] AI analysis failed: {e}")
            return self._generate_basic_insight(file_path, content, content_hash)

    def _generate_basic_insight(self, file_path: str, content: str, content_hash: str) -> OracleInsight:
        """Generate a basic insight without AI analysis."""
        filename = os.path.basename(file_path)
        word_count = len(content.split())

        return OracleInsight(
            insight_id=str(uuid.uuid4()),
            timestamp=time.time(),
            file_path=file_path,
            content_hash=content_hash,
            core_lesson=f"Knowledge expanded in {filename} ({word_count} words)",
            next_level_concept="Explore related concepts and applications",
            growth_vector="Building knowledge foundation"
        )

    def start_monitoring(self):
        """Start the file system monitoring."""
        if not WATCHDOG_AVAILABLE:
            print("[SOL ORACLE] Watchdog not available - file monitoring disabled")
            return False

        if not os.path.exists(self.knowledge_base):
            print(f"[SOL ORACLE] Knowledge base path does not exist: {self.knowledge_base}")
            return False

        print(f"[SOL ORACLE] Starting monitoring of: {self.knowledge_base}")
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.knowledge_base, recursive=True)
        self.observer.start()
        return True

    def stop_monitoring(self):
        """Stop the file system monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("[SOL ORACLE] Monitoring stopped")

    def get_recent_insights(self, limit: int = 5) -> List[OracleInsight]:
        """Get the most recent oracle insights."""
        return self.knowledge_state.insights_generated[-limit:]

    def scan_knowledge_base(self) -> int:
        """
        Perform a full scan of the knowledge base.

        Returns:
            Number of new insights generated
        """
        if not os.path.exists(self.knowledge_base):
            return 0

        insights_generated = 0

        for root, dirs, files in os.walk(self.knowledge_base):
            for file in files:
                if file.endswith(('.md', '.txt', '.py', '.js', '.json')):
                    file_path = os.path.join(root, file)
                    insight = self.analyze_growth(file_path)
                    if insight:
                        insights_generated += 1

        self.knowledge_state.last_scan = time.time()
        self._save_knowledge_state()

        print(f"[SOL ORACLE] Knowledge base scan complete - {insights_generated} new insights")
        return insights_generated

    def get_growth_summary(self) -> Dict[str, Any]:
        """Generate a summary of knowledge growth and insights."""
        total_insights = len(self.knowledge_state.insights_generated)
        recent_insights = self.get_recent_insights(10)

        growth_vectors = {}
        for insight in recent_insights:
            vector = insight.growth_vector
            growth_vectors[vector] = growth_vectors.get(vector, 0) + 1

        return {
            "total_insights": total_insights,
            "last_scan": datetime.fromtimestamp(self.knowledge_state.last_scan).isoformat(),
            "monitored_files": len(self.knowledge_state.file_hashes),
            "growth_vectors": growth_vectors,
            "recent_insights": [insight.__dict__ for insight in recent_insights]
        }


# Integration function for SOL module
def create_sol_oracle(sol_state: Any, knowledge_base_path: str = None, api_key: str = None) -> SolOracleCore:
    """
    Create and initialize a SOL Oracle instance.

    Args:
        sol_state: SOL's state object
        knowledge_base_path: Path to knowledge base (defaults to workspace/docs or similar)
        api_key: Google Gemini API key

    Returns:
        Configured SolOracleCore instance
    """
    if knowledge_base_path is None:
        # Try to find a suitable knowledge base path
        candidates = [
            os.path.join(os.getcwd(), "docs"),
            os.path.join(os.getcwd(), "knowledge"),
            os.path.join(os.getcwd(), "obsidian"),
            os.path.join(os.path.expanduser("~"), "Documents", "obsidian")
        ]

        for candidate in candidates:
            if os.path.exists(candidate):
                knowledge_base_path = candidate
                break
        else:
            # Create a default knowledge directory
            knowledge_base_path = os.path.join(os.getcwd(), "sol_knowledge")
            os.makedirs(knowledge_base_path, exist_ok=True)

    return SolOracleCore(sol_state, knowledge_base_path, api_key)