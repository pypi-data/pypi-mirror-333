#!/usr/bin/env python
"""
Simple example of using the progress tracking system.
"""

import asyncio
import logging

from laneswap.core.progress import get_tracker, with_async_progress_tracking

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simple_progress")

@with_async_progress_tracking()
async def simple_task(iterations: int = 5):
    """A simple task that demonstrates progress tracking."""
    tracker = get_tracker()
    execution_id = asyncio.current_task().get_name()

    logger.info("Starting task with execution ID: %s", execution_id)

    for i in range(iterations):
        # Update progress
        progress_pct = (i / iterations) * 100
        await tracker.update_progress(
            execution_id=execution_id,
            step=f"Step {i+1}/{iterations}",
            progress=progress_pct
        )

        # Simulate work
        logger.info("Working on step %s/%s...", i+1, iterations)
        await asyncio.sleep(1)

    # Final progress update
    await tracker.update_progress(
        execution_id=execution_id,
        step="Completed",
        progress=100
    )

    logger.info("Task completed successfully")
    return "Success"

async def main():
    """Run the example."""
    logger.info("Starting simple progress tracking example")

    # Run the task
    result = await simple_task(iterations=5)

    logger.info("Task result: %s", result)

    # Get execution statistics
    tracker = get_tracker()
    executions = tracker.get_all_executions()

    logger.info("Tracked %s executions", len(executions))
    for exec_id, exec_data in executions.items():
        logger.info("Execution %s: %s in %s", exec_id, exec_data['status'], exec_data.get('duration', 'N/A'))

if __name__ == "__main__":
    asyncio.run(main())
