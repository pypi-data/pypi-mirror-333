import time
import statistics
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any, Callable

import asyncio
from functools import wraps


class TimTheEnchanterReportFormat(Enum):
    """Enum for different report formats."""

    CHRONOLOGICAL = "chronological"  # Ordered by insertion time
    BY_PROCESS = "by_process"  # Ordered by process name and insertion time
    AGGREGATE = "aggregate"  # Aggregated by process name with statistics


@dataclass
class TimTheEnchanterTimingEvent:
    """Class to store timing information for a single event."""

    process_name: str
    duration: float  # Duration in seconds
    timestamp: datetime
    metadata: Optional[Dict] = None


class TimTheEnchanter:
    """Performance tracking service for measuring execution times."""

    _instance = None
    _initialized = False

    def __new__(cls):
        """Singleton pattern to ensure only one tracker exists."""
        if cls._instance is None:
            cls._instance = super(TimTheEnchanter, cls).__new__(cls)
            cls._instance._sessions = {}
            cls._instance._active_session = None
            # Default to disabled for safety
            cls._instance._enabled = False
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the performance tracker if not already initialized."""
        if not self._initialized:
            self._initialized = True

    def configure(
        self, enabled: Optional[bool] = None, reset_sessions: bool = False
    ) -> "TimTheEnchanter":
        """Configure the performance tracker with the provided settings.

        Args:
            enabled: Whether tracking should be enabled. If None, keeps current setting.
            reset_sessions: Whether to clear all existing sessions.

        Returns:
            The performance tracker instance (self) for method chaining.
        """
        # Only update if explicitly requested
        if enabled is not None:
            previous_state = self._enabled
            self._enabled = enabled
            print(
                f"Performance tracking configured: {previous_state} -> {self._enabled}"
            )

        if reset_sessions:
            self._sessions = {}
            self._active_session = None

        return self

    @classmethod
    def create(cls, enabled: bool = True) -> "TimTheEnchanter":
        """Factory method to create/get and configure the performance tracker.

        This is the recommended way to get a configured tracker instance.

        Args:
            enabled: Whether performance tracking should be enabled

        Returns:
            Configured TimTheEnchanter instance

        Example:
            tracker = TimTheEnchanter.create(enabled=True)
        """
        instance = cls()
        instance.configure(enabled=enabled)
        return instance

    @property
    def enabled(self) -> bool:
        """Get whether performance tracking is enabled."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set whether performance tracking is enabled."""
        self._enabled = value

    def enable(self) -> None:
        """Enable performance tracking."""
        self._enabled = True

    def disable(self) -> None:
        """Disable performance tracking."""
        self._enabled = False

    def start_session(self, session_name: str) -> "TimTheEnchanter":
        """Start a new recording session.

        Args:
            session_name: A unique name for the session

        Returns:
            The performance tracker instance (self) for method chaining.
        """
        if not self._enabled:
            return self  # No-op when disabled, but still return self for chaining

        if session_name in self._sessions:
            raise ValueError(f"Session '{session_name}' already exists")

        self._sessions[session_name] = []
        self._active_session = session_name

        return self

    def end_session(self) -> "TimTheEnchanter":
        """End the current recording session.

        Returns:
            The performance tracker instance (self) for method chaining.
        """
        if not self._enabled:
            return self  # No-op when disabled, but still return self for chaining

        self._active_session = None

        return self

    def record(
        self, process_name: str, duration: float, metadata: Optional[Dict] = None
    ) -> "TimTheEnchanter":
        """Record a timing event for a process.

        Args:
            process_name: Name of the process being timed
            duration: Duration of the process in seconds
            metadata: Optional metadata for the event

        Returns:
            The performance tracker instance (self) for method chaining.
        """
        if not self._enabled:
            return self  # No-op when disabled, but still return self for chaining

        if not self._active_session:
            raise RuntimeError("No active session. Call start_session() first.")

        event = TimTheEnchanterTimingEvent(
            process_name=process_name,
            duration=duration,
            timestamp=datetime.now(),
            metadata=metadata,
        )

        self._sessions[self._active_session].append(event)

        return self

    @contextmanager
    def time_process(self, process_name: str, metadata: Optional[Dict] = None):
        """Context manager for timing a process.

        Args:
            process_name: Name of the process being timed
            metadata: Optional metadata for the event

        Example:
            with tim_the_enchanter.time_process("database_query"):
                result = db.query()
        """
        if not self._enabled:
            # Fast no-op path when disabled
            yield
            return

        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.record(process_name, duration, metadata)

    def time_function(self, process_name: Optional[str] = None):
        """Decorator for timing a function.

        Args:
            process_name: Optional name override. If None, uses function name

        Example:
            @tim_the_enchanter.time_function()
            def my_function():
                pass
        """

        def decorator(func):
            @wraps(func)
            def wrapped(*args, **kwargs):
                if not self._enabled:
                    # Fast path when disabled - just call the function
                    return func(*args, **kwargs)

                name = process_name or func.__name__
                with self.time_process(name):
                    return func(*args, **kwargs)

            return wrapped

        return decorator

    def time_async_function(self, process_name: Optional[str] = None):
        """Decorator for timing an async function.

        Args:
            process_name: Optional name override. If None, uses function name

        Example:
            @tim_the_enchanter.time_async_function()
            async def my_async_function():
                pass
        """

        def decorator(func):
            @wraps(func)
            async def wrapped(*args, **kwargs):
                if not self._enabled:
                    # Fast path when disabled - just call the function
                    return await func(*args, **kwargs)

                name = process_name or func.__name__
                start_time = time.time()
                try:
                    return await func(*args, **kwargs)
                finally:
                    duration = time.time() - start_time
                    self.record(name, duration)

            return wrapped

        return decorator

    def get_session_events(
        self, session_name: Optional[str] = None
    ) -> List[TimTheEnchanterTimingEvent]:
        """Get all events for a session.

        Args:
            session_name: Name of the session. If None, uses active session.

        Returns:
            List of TimTheEnchanterTimingEvent objects for the session
        """
        if not self._enabled:
            return []  # Return empty list when disabled

        session = session_name or self._active_session
        if not session:
            raise RuntimeError("No active session and no session name provided.")

        if session not in self._sessions:
            raise ValueError(f"Session '{session}' does not exist")

        return self._sessions[session]

    def report(
        self,
        format: Union[
            TimTheEnchanterReportFormat, str
        ] = TimTheEnchanterReportFormat.CHRONOLOGICAL,
        session_name: Optional[str] = None,
        include_metadata: bool = False,
    ) -> Dict:
        """Generate a report for the specified session.

        Args:
            format: Report format (chronological, by_process, or aggregate)
            session_name: Name of the session. If None, uses active session.
            include_metadata: Whether to include metadata in the report

        Returns:
            Dictionary with the report data
        """
        if not self._enabled:
            return {
                "format": "disabled",
                "session": session_name or self._active_session or "unknown",
                "events": [],
                "message": "Performance tracking is disabled",
            }

        session = session_name or self._active_session
        if not session:
            raise RuntimeError("No active session and no session name provided.")

        if session not in self._sessions:
            raise ValueError(f"Session '{session}' does not exist")

        events = self._sessions[session]

        if isinstance(format, str):
            try:
                format = TimTheEnchanterReportFormat(format)
            except ValueError:
                valid_formats = [e.value for e in TimTheEnchanterReportFormat]
                raise ValueError(
                    f"Invalid format '{format}'. Valid formats are: {valid_formats}"
                )

        if format == TimTheEnchanterReportFormat.CHRONOLOGICAL:
            # Sort by timestamp
            sorted_events = sorted(events, key=lambda e: e.timestamp)
            result = {
                "format": "chronological",
                "session": session,
                "events": [
                    self._event_to_dict(e, include_metadata) for e in sorted_events
                ],
            }

        elif format == TimTheEnchanterReportFormat.BY_PROCESS:
            # Group by process name, then sort by timestamp
            by_process = defaultdict(list)
            for event in events:
                by_process[event.process_name].append(event)

            for process, process_events in by_process.items():
                by_process[process] = sorted(process_events, key=lambda e: e.timestamp)

            result = {
                "format": "by_process",
                "session": session,
                "processes": {
                    process: [
                        self._event_to_dict(e, include_metadata) for e in process_events
                    ]
                    for process, process_events in by_process.items()
                },
            }

        elif format == TimTheEnchanterReportFormat.AGGREGATE:
            # Aggregate statistics by process
            by_process = defaultdict(list)
            for event in events:
                by_process[event.process_name].append(event.duration)

            aggregates = {}
            for process, durations in by_process.items():
                aggregates[process] = {
                    "count": len(durations),
                    "total_time": sum(durations),
                    "avg_time": sum(durations) / len(durations),
                    "min_time": min(durations),
                    "max_time": max(durations),
                    "median_time": statistics.median(durations),
                    "stdev": statistics.stdev(durations) if len(durations) > 1 else 0,
                }

            result = {
                "format": "aggregate",
                "session": session,
                "aggregates": aggregates,
            }

        return result

    def print_report(
        self,
        format: Union[
            TimTheEnchanterReportFormat, str
        ] = TimTheEnchanterReportFormat.CHRONOLOGICAL,
        session_name: Optional[str] = None,
        include_metadata: bool = False,
    ) -> "TimTheEnchanter":
        """Print a formatted report to the console as a table.

        Args:
            format: Report format (chronological, by_process, or aggregate)
            session_name: Name of the session. If None, uses active session.
            include_metadata: Whether to include metadata in the report

        Returns:
            The performance tracker instance (self) for method chaining.
        """
        # Debug output to show the current state
        if not self._enabled:
            # When disabled, print nothing and just return
            return self

        report_data = self.report(format, session_name, include_metadata)

        print(
            f"\n===== ✨ Tim The Enchanter Performance Report ✨ {report_data['session']} ====="
        )
        print(f"Format: {report_data['format']}")

        if report_data["format"] == "chronological":
            # Define column widths for the table
            col_widths = {
                "index": 5,
                "process_name": 40,
                "duration": 12,
                "timestamp": 26,
            }

            # Print table header
            header = (
                f"{'#':^{col_widths['index']}} | "
                f"{'Process Name':{col_widths['process_name']}} | "
                f"{'Duration (s)':^{col_widths['duration']}} | "
                f"{'Timestamp':{col_widths['timestamp']}}"
            )
            print(f"\n{header}")
            print("-" * (sum(col_widths.values()) + len(col_widths) * 3 - 1))

            # Print each row
            for i, event in enumerate(report_data["events"], 1):
                row = (
                    f"{i:^{col_widths['index']}} | "
                    f"{event['process_name']:{col_widths['process_name']}} | "
                    f"{event['duration']:{col_widths['duration']}.6f} | "
                    f"{event['timestamp']:{col_widths['timestamp']}}"
                )
                print(row)

                # Print metadata if included
                if include_metadata and event.get("metadata"):
                    metadata_str = str(event["metadata"])
                    # If metadata is long, truncate it
                    if len(metadata_str) > sum(col_widths.values()):
                        metadata_str = (
                            metadata_str[: sum(col_widths.values()) - 10] + "..."
                        )
                    print(f"{'':{col_widths['index']}} | Metadata: {metadata_str}")
                    print("-" * (sum(col_widths.values()) + len(col_widths) * 3 - 1))

        elif report_data["format"] == "by_process":
            # For by_process, we'll create a table per process
            for process, events in report_data["processes"].items():
                print(f"\n{process} ({len(events)} events):")

                # Define column widths
                col_widths = {"index": 5, "duration": 12, "timestamp": 26}

                # Print table header
                header = (
                    f"{'#':^{col_widths['index']}} | "
                    f"{'Duration (s)':^{col_widths['duration']}} | "
                    f"{'Timestamp':{col_widths['timestamp']}}"
                )
                print(f"{header}")
                print("-" * (sum(col_widths.values()) + len(col_widths) * 3 - 1))

                # Print each row
                for i, event in enumerate(events, 1):
                    row = (
                        f"{i:^{col_widths['index']}} | "
                        f"{event['duration']:{col_widths['duration']}.6f} | "
                        f"{event['timestamp']:{col_widths['timestamp']}}"
                    )
                    print(row)

                    # Print metadata if included
                    if include_metadata and event.get("metadata"):
                        metadata_str = str(event["metadata"])
                        # If metadata is long, truncate it
                        if len(metadata_str) > sum(col_widths.values()):
                            metadata_str = (
                                metadata_str[: sum(col_widths.values()) - 10] + "..."
                            )
                        print(f"{'':{col_widths['index']}} | Metadata: {metadata_str}")
                        print(
                            "-" * (sum(col_widths.values()) + len(col_widths) * 3 - 1)
                        )

        elif report_data["format"] == "aggregate":
            # Define column widths for the table
            col_widths = {
                "process_name": 40,
                "count": 8,
                "total": 12,
                "avg": 12,
                "min": 12,
                "max": 12,
                "median": 12,
                "stdev": 12,
            }

            # Print table header
            header = (
                f"{'Process Name':{col_widths['process_name']}} | "
                f"{'Count':^{col_widths['count']}} | "
                f"{'Total (s)':^{col_widths['total']}} | "
                f"{'Avg (s)':^{col_widths['avg']}} | "
                f"{'Min (s)':^{col_widths['min']}} | "
                f"{'Max (s)':^{col_widths['max']}} | "
                f"{'Median (s)':^{col_widths['median']}} | "
                f"{'StdDev (s)':^{col_widths['stdev']}}"
            )
            print(f"\n{header}")
            print("-" * (sum(col_widths.values()) + len(col_widths) * 3 - 1))

            # Sort processes by total time (descending)
            sorted_processes = sorted(
                report_data["aggregates"].items(),
                key=lambda x: x[1]["total_time"],
                reverse=True,
            )

            # Print each row
            for process, stats in sorted_processes:
                row = (
                    f"{process:{col_widths['process_name']}} | "
                    f"{stats['count']:^{col_widths['count']}} | "
                    f"{stats['total_time']:{col_widths['total']}.6f} | "
                    f"{stats['avg_time']:{col_widths['avg']}.6f} | "
                    f"{stats['min_time']:{col_widths['min']}.6f} | "
                    f"{stats['max_time']:{col_widths['max']}.6f} | "
                    f"{stats['median_time']:{col_widths['median']}.6f} | "
                    f"{stats['stdev']:{col_widths['stdev']}.6f}"
                )
                print(row)

        print("\n" + "=" * 80 + "\n")
        return self

    def reset_session(self, session_name: Optional[str] = None) -> "TimTheEnchanter":
        """Reset a session, clearing all recorded events.

        Args:
            session_name: Name of the session. If None, uses active session.

        Returns:
            The performance tracker instance (self) for method chaining.
        """
        if not self._enabled:
            return self  # No-op when disabled, but still return self for chaining

        session = session_name or self._active_session
        if not session:
            raise RuntimeError("No active session and no session name provided.")

        if session not in self._sessions:
            raise ValueError(f"Session '{session}' does not exist")

        self._sessions[session] = []
        return self

    def delete_session(self, session_name: str) -> "TimTheEnchanter":
        """Delete a session.

        Args:
            session_name: Name of the session to delete.

        Returns:
            The performance tracker instance (self) for method chaining.
        """
        if not self._enabled:
            return self  # No-op when disabled, but still return self for chaining

        if session_name not in self._sessions:
            raise ValueError(f"Session '{session_name}' does not exist")

        if self._active_session == session_name:
            self._active_session = None

        del self._sessions[session_name]
        return self

    def _event_to_dict(
        self, event: TimTheEnchanterTimingEvent, include_metadata: bool = False
    ) -> Dict:
        """Convert a TimTheEnchanterTimingEvent to a dictionary.

        Args:
            event: The TimTheEnchanterTimingEvent to convert
            include_metadata: Whether to include metadata

        Returns:
            Dictionary representation of the event
        """
        result = {
            "process_name": event.process_name,
            "duration": event.duration,
            "timestamp": event.timestamp.isoformat(),
        }

        if include_metadata and event.metadata:
            result["metadata"] = event.metadata

        return result


# Create singleton instance for direct import
tim_the_enchanter = TimTheEnchanter()


# Example usage:
"""
# Get a configured instance via the factory method (recommended)
tracker = TimTheEnchanter.create(enabled=True)  # or enabled=False to disable

# Method 1: Configure an existing instance
tracker = TimTheEnchanter().configure(enabled=True)

# Method 2: Use the factory method (recommended approach)
tracker = TimTheEnchanter.create(enabled=not is_production)

# Start tracking a session
tracker.start_session("my_api_request")

# Track a block of code with a context manager
with tracker.time_process("data_processing"):
    # Your code here
    process_data()

# Track a function with a decorator
@tracker.time_function()
def calculate_results():
    # Function code
    pass

# Track an async function
@tracker.time_async_function()
async def fetch_data():
    # Async function code
    pass

# Manual tracking
start_time = time.time()
# ... do something ...
duration = time.time() - start_time
tracker.record("manual_operation", duration)

# Method chaining with fluent interface
(TimTheEnchanter()
    .configure(enabled=True)
    .start_session("api_request")
    .record("initialization", 0.05)
    .print_report(TimTheEnchanterReportFormat.CHRONOLOGICAL)
    .end_session()
)

# Runtime enabling/disabling
tracker.disable()  # Temporarily disable tracking
expensive_operation()  # Not tracked
tracker.enable()   # Re-enable tracking

# Generate reports
tracker.print_report(TimTheEnchanterReportFormat.CHRONOLOGICAL)  # Time-ordered events
tracker.print_report(TimTheEnchanterReportFormat.BY_PROCESS)     # Grouped by process name
tracker.print_report(TimTheEnchanterReportFormat.AGGREGATE)      # Statistical summary

# End the session
tracker.end_session()
"""
