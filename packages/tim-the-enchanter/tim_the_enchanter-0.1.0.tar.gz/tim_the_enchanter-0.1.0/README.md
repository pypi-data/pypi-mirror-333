# ✨ Tim The Enchanter ✨

A lightweight, flexible performance tracking library for Python applications. Easily measure and analyze execution times of your functions, code blocks, and processes.

## Features

- ✅ **Zero dependencies** - Just Python standard library
- ✅ **Minimal overhead** - Designed to be lightweight
- ✅ **Multiple reporting formats** - Chronological, by-process, and aggregated statistics
- ✅ **Flexible configuration** - Enable/disable via arguments or environment variables
- ✅ **Method chaining** - Fluent interface for concise code
- ✅ **Context managers & decorators** - Multiple ways to instrument your code
- ✅ **Support for async functions** - Works with asyncio
- ✅ **Metadata support** - Add context to your timing events

## Installation

```bash
pip install tim-the-enchanter
```

## Basic Usage

```python
from tim_the_enchanter import TimTheEnchanter, TimTheEnchanterReportFormat

# Get a configured instance
tracker = TimTheEnchanter.create(enabled=True)

# Start tracking a session
tracker.start_session("my_api_request")

# Track a block of code
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

# Generate reports
tracker.print_report(TimTheEnchanterReportFormat.CHRONOLOGICAL)  # Time-ordered events
tracker.print_report(TimTheEnchanterReportFormat.BY_PROCESS)     # Grouped by process name
tracker.print_report(TimTheEnchanterReportFormat.AGGREGATE)      # Statistical summary

# End the session
tracker.end_session()
```

## Configuration Options

There are multiple ways to configure the performance tracker:

### 1. Factory Method (Recommended)

```python
# Simple way to create and configure in one step
tracker = TimTheEnchanter.create(enabled=not is_production)
```

### 2. Direct Configuration

```python
# Import the singleton instance
from tim_the_enchanter import tim_the_enchanter as tracker
# Configure the singleton instance
tracker.configure(enabled=True, reset_sessions=False)
```

## Method Chaining

The tracker supports a fluent interface for concise code:

```python
# Chain multiple operations
(TimTheEnchanter()
    .configure(enabled=True)
    .start_session("api_request")
    .record("initialization", 0.05)
    .print_report(TimTheEnchanterReportFormat.CHRONOLOGICAL)
    .end_session()
)
```

## Runtime Toggling

You can enable or disable tracking at runtime:

```python
# Disable during specific operations
tracker.disable()
compute_expensive_operation()  # Not tracked
tracker.enable()
```
## Session Management

```python
# Create and manage multiple sessions
tracker.start_session("session1")
# ... operations ...
tracker.end_session()

tracker.start_session("session2")
# ... more operations ...
tracker.print_report(format=TimTheEnchanterReportFormat.AGGREGATE, session_name="session2")
tracker.end_session()
```

## Metadata Support

```python
# Add contextual information to timing events
with tracker.time_process("database_query", metadata={"table": "users", "filters": {"active": True}}):
    # Your code here
    pass
```

## Performance Considerations

The tracker is designed to be lightweight, but for production environments, you may want to disable it:

```python
# In your application startup code
is_production = os.environ.get("ENV") == "production"
tracker = TimTheEnchanter.create(enabled=not is_production)
```

When disabled, all tracking operations become no-ops with minimal overhead. 
