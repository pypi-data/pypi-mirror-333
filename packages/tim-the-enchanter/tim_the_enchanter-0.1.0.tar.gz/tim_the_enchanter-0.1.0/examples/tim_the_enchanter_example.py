import asyncio
import time
from tim_the_enchanter import (
    tim_the_enchanter,
    TimTheEnchanterReportFormat,
)


async def demonstrate_basic_usage():
    """Show basic usage of the performance tracker."""
    # Start a new session
    tim_the_enchanter.start_session("demo_session")

    # Manual timing
    start = time.time()
    await asyncio.sleep(0.1)  # Simulate some work
    end = time.time()
    tim_the_enchanter.record("manual_process", end - start)

    # Using context manager
    with tim_the_enchanter.time_process("context_manager_process"):
        await asyncio.sleep(0.2)  # Simulate some work

    # Using decorator for sync function
    @tim_the_enchanter.time_function()
    def sync_function():
        time.sleep(0.15)  # Simulate some work

    sync_function()

    # Using decorator for async function
    @tim_the_enchanter.time_async_function()
    async def async_function():
        await asyncio.sleep(0.25)  # Simulate some work

    await async_function()

    # Print reports in different formats
    print("\n=== Chronological Report ===")
    tim_the_enchanter.print_report(TimTheEnchanterReportFormat.CHRONOLOGICAL)

    print("\n=== By Process Report ===")
    tim_the_enchanter.print_report(TimTheEnchanterReportFormat.BY_PROCESS)

    print("\n=== Aggregate Report ===")
    tim_the_enchanter.print_report(TimTheEnchanterReportFormat.AGGREGATE)

    # End the session
    tim_the_enchanter.end_session()


async def demonstrate_real_world_usage():
    """Demonstrate how to use the performance tracker in a real-world scenario."""
    # Start a session for tracking a request
    tim_the_enchanter.start_session("document_processing")

    # Simulate document parsing
    with tim_the_enchanter.time_process("document_parsing", {"doc_size": "2MB"}):
        await asyncio.sleep(0.3)  # Simulate parsing work

    # Simulate text embedding in multiple batches
    for i in range(3):
        with tim_the_enchanter.time_process(
            "text_embedding", {"batch": i, "model": "text-embedding-3-small"}
        ):
            # Different batches might take different times
            await asyncio.sleep(0.1 + (i * 0.05))

    # Simulate LLM processing
    with tim_the_enchanter.time_process("llm_processing", {"model": "gpt-4"}):
        await asyncio.sleep(0.5)  # LLMs typically take longer

    # Simulate database operations
    with tim_the_enchanter.time_process("database_operations"):
        for i in range(2):
            with tim_the_enchanter.time_process(
                "db_query", {"query_type": "vector_search"}
            ):
                await asyncio.sleep(0.1)

    # Generate an aggregate report
    tim_the_enchanter.print_report(TimTheEnchanterReportFormat.AGGREGATE)

    # End the session
    tim_the_enchanter.end_session()


async def main():
    await demonstrate_basic_usage()
    print("\n" + "=" * 50 + "\n")
    await demonstrate_real_world_usage()


if __name__ == "__main__":
    asyncio.run(main())
