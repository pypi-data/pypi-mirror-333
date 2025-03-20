
from src.tecton_gen_ai.api import Agent

from tools import list_workspaces, list_feature_services, tecton_cli_help, tecton_cli_execute, get_feature_view_configuration, get_feature_service_configuration

DIAGONISTICS_KNOWLEDGE = """
# Batch Features

## Missing Data
Tecton silently ignores all rows that don’t fall into the materialization window.

### Common gotchas:
- Using `context.end_time` as the materialization run’s feature timestamp, and forgetting to subtract a millisecond.

## Inefficient Backfills
Not filtering the upstream data source(s) properly by the materialization run’s time window.

### Common gotchas:
- Failing to use `FilteredSource`.
- Failing to make the onboarded data source “filter-able”.

Using incremental backfills when you don’t need to.

### Common gotchas:
- Implemented a custom aggregation that can really be expressed using Tecton’s aggregation engine.
- Setting `incremental_backfill` to `True` when the transformation is a simple row-level transformation.

## Inefficient Provisioning
Not properly provisioning the compute infrastructure.

### Common gotchas:
- Provisioning too little memory.
- Provisioning too much memory.
- Provisioning not enough cores.

## Inefficient Compute Mode
Picking a suboptimal compute engine.

### Common gotchas:
- Using Python mode when Pandas should be used.
- Using Pandas mode when SparkSQL or SnowflakeSQL should be used.

---

# Streaming Features

## Inefficient Stream Processing
- Using continuous when `stream_tiling` should be used (to write less data to the online store).

## Staler-than-expected Streaming Features
- Using continuous Spark streaming features when continuous Rift features should be used.
- Using tiled streaming features when continuous should be used.
- Using `StreamIngest v1` instead of `StreamIngest v2`.

## Inefficient Provisioning
Under or over-provisioned resources.

## Inefficient Choice of Streaming Features
Using streaming features when batch processing is good enough.

### Common gotchas:
- Using streaming features for features that don’t decay or change quickly.

---

# Realtime Features

## Inefficient Compute
- Using Pandas mode when Python should be used.
- Using Python mode when Calculation features should be used.
- Using real-time computed features when features should be precomputed (e.g., using last-n + RTFV when you can just aggregate in a streaming feature).

## Inefficient Provisioning

### Common gotchas:
- `FeatureServer` (or `TSG`) is not properly statically provisioned.
- `FeatureServer` (or `TSG`) uses static provisioning but should use autoscaling.

---

# Training Data Generation

## Slow Training Data Generation

### Common gotchas:
- Failure to provision the job with enough memory.
- Failure to provision the job with enough nodes (if it can easily be parallelized).
- Failure to materialize features to the offline store.
- Having unnecessarily high TTL.
- Having unnecessarily large time windows.
- Using local mode when you should use remote dataset generation

---

# Real-Time Serving

## Expensive Online Store
Choosing Dynamo when Redis should be used.

### Common gotchas:
- Extremely write-heavy workloads.

Choosing Redis when Dynamo should be used.

### Common gotchas:
- Extremely low-read intense workloads.

## Expensive Online Store for Backfills

### Common gotchas:
- Failure to use bulk-import with Dynamo.

## High Read-Time Latencies / Expensive Online Compute

### Common gotchas:
- Time window is too long and compaction is disabled.
"""

def sys_prompt() -> str:
    return f"""
You are a helpful assistant that can help diagnose performance issues and answer questions about how to optimize performance.

Use the following knowledge base to help you answer the question. If this doesn't help, try to find more information in the documentation.
If the user is asking about a specific FeatureView or FeatureService, retrieve the object, inspect it and use it to make a better diagnosis.

{DIAGONISTICS_KNOWLEDGE}

The output should be a detailed explanation of the issue and the steps you can take to fix it. Include a link to relevant documentation whenever possible.
"""

def _make_agent(doc_retriever: Agent) -> Agent:
    return Agent(
        name="diagnostics_agent",
        description="""An agent that can help you diagnose performance issues and answer questions about how to optimize performance

Args:

    - query: A detailed summary of the issue the user is experiencing or the question they're asking. Include any previous context as relevant.

Returns:

    Returns an explanation of what the user can do to fix the issue or it may contain follow up questions

Note:

    - You must pass the agent response to the user. You must not call the agent multiple times.
""",
        prompt=sys_prompt,
        tools=[
            doc_retriever,
            list_workspaces,
            list_feature_services,
            get_feature_service_configuration,
            get_feature_view_configuration,
            tecton_cli_help,
            tecton_cli_execute,
        ],
    )
