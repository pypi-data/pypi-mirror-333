"""lighthousellmm Client."""

from importlib import metadata
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from lighthousellmm._expect import expect
    from lighthousellmm.async_client import AsyncClient
    from lighthousellmm.client import Client
    from lighthousellmm.evaluation import aevaluate, evaluate
    from lighthousellmm.evaluation.evaluator import EvaluationResult, RunEvaluator
    from lighthousellmm.run_helpers import (
        get_current_run_tree,
        get_tracing_context,
        trace,
        traceable,
        tracing_context,
    )
    from lighthousellmm.run_trees import RunTree
    from lighthousellmm.testing._internal import test, unit
    from lighthousellmm.utils import (
        ContextThreadPoolExecutor,
    )

# Avoid calling into importlib on every call to __version__
version = ""
try:
    version = metadata.version(__package__)
except metadata.PackageNotFoundError:
    pass


def __getattr__(name: str) -> Any:
    if name == "__version__":
        return version
    elif name == "Client":
        from lighthousellmm.client import Client

        return Client
    elif name == "AsyncClient":
        from lighthousellmm.async_client import AsyncClient

        return AsyncClient
    elif name == "RunTree":
        from lighthousellmm.run_trees import RunTree

        return RunTree
    elif name == "EvaluationResult":
        from lighthousellmm.evaluation.evaluator import EvaluationResult

        return EvaluationResult
    elif name == "RunEvaluator":
        from lighthousellmm.evaluation.evaluator import RunEvaluator

        return RunEvaluator
    elif name == "trace":
        from lighthousellmm.run_helpers import trace

        return trace
    elif name == "traceable":
        from lighthousellmm.run_helpers import traceable

        return traceable

    elif name == "test":
        from lighthousellmm.testing._internal import test

        return test

    elif name == "expect":
        from lighthousellmm._expect import expect

        return expect
    elif name == "evaluate":
        from lighthousellmm.evaluation import evaluate

        return evaluate

    elif name == "evaluate_existing":
        from lighthousellmm.evaluation import evaluate_existing

        return evaluate_existing
    elif name == "aevaluate":
        from lighthousellmm.evaluation import aevaluate

        return aevaluate
    elif name == "aevaluate_existing":
        from lighthousellmm.evaluation import aevaluate_existing

        return aevaluate_existing
    elif name == "tracing_context":
        from lighthousellmm.run_helpers import tracing_context

        return tracing_context

    elif name == "get_tracing_context":
        from lighthousellmm.run_helpers import get_tracing_context

        return get_tracing_context

    elif name == "get_current_run_tree":
        from lighthousellmm.run_helpers import get_current_run_tree

        return get_current_run_tree

    elif name == "unit":
        from lighthousellmm.testing._internal import unit

        return unit
    elif name == "ContextThreadPoolExecutor":
        from lighthousellmm.utils import (
            ContextThreadPoolExecutor,
        )

        return ContextThreadPoolExecutor

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Client",
    "RunTree",
    "__version__",
    "EvaluationResult",
    "RunEvaluator",
    "anonymizer",
    "traceable",
    "trace",
    "unit",
    "test",
    "expect",
    "evaluate",
    "aevaluate",
    "tracing_context",
    "get_tracing_context",
    "get_current_run_tree",
    "ContextThreadPoolExecutor",
    "AsyncClient",
]
