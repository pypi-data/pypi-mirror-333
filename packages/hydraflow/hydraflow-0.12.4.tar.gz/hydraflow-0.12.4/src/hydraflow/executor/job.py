"""Job execution and argument handling for HydraFlow.

This module provides functionality for executing jobs in HydraFlow, including:

- Argument parsing and expansion for job steps
- Batch processing of Hydra configurations
- Execution of jobs via shell commands or Python functions

The module supports two execution modes:

1. Shell command execution
2. Python function calls

Each job can consist of multiple steps, and each step can have its own
arguments and configurations that will be expanded into multiple runs.
"""

from __future__ import annotations

import importlib
import shlex
import subprocess
import sys
from subprocess import CalledProcessError
from typing import TYPE_CHECKING

import ulid

from .parser import collect, expand

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .conf import Job


def iter_args(batch: str, args: str) -> Iterator[list[str]]:
    """Iterate over combinations generated from parsed arguments.

    Generate all possible combinations of arguments by parsing and
    expanding each one, yielding them as an iterator.

    Args:
        batch (str): The batch to parse.
        args (str): The arguments to parse.

    Yields:
        list[str]: a list of the parsed argument combinations.

    """
    args_ = collect(args)

    for batch_ in expand(batch):
        yield [*batch_, *args_]


def iter_batches(job: Job) -> Iterator[list[str]]:
    """Generate Hydra application arguments for a job.

    This function generates a list of Hydra application arguments
    for a given job, including the job name and the root directory
    for the sweep.

    Args:
        job (Job): The job to generate the Hydra configuration for.

    Returns:
        list[str]: A list of Hydra configuration strings.

    """
    job_name = f"hydra.job.name={job.name}"
    job_configs = shlex.split(job.with_)

    for step in job.steps:
        configs = shlex.split(step.with_) or job_configs

        for args in iter_args(step.batch, step.args):
            sweep_dir = f"hydra.sweep.dir=multirun/{ulid.ULID()}"
            yield ["--multirun", *args, job_name, sweep_dir, *configs]


def multirun(job: Job) -> None:
    """Execute multiple runs of a job using either shell commands or Python functions.

    This function processes a job configuration and executes it in one of two modes:

    1. Shell command mode (job.run): Executes shell commands with the generated
       arguments
    2. Python function mode (job.call): Calls a Python function with the generated
       arguments

    Args:
        job (Job): The job configuration containing run parameters and steps.

    Raises:
        RuntimeError: If a shell command fails or if a function call encounters
            an error.
        ValueError: If the Python function path is invalid or the function cannot
            be imported.

    """
    it = iter_batches(job)

    if job.run:
        base_cmds = shlex.split(job.run)
        if base_cmds[0] == "python" and sys.platform == "win32":
            base_cmds[0] = sys.executable

        for args in it:
            cmds = [*base_cmds, *args]
            try:
                subprocess.run(cmds, check=True)
            except CalledProcessError as e:
                msg = f"Command failed with exit code {e.returncode}"
                raise RuntimeError(msg) from e

    elif job.call:
        call_name, *base_args = shlex.split(job.call)

        if "." not in call_name:
            msg = f"Invalid function path: {call_name}."
            msg += " Expected format: 'package.module.function'"
            raise ValueError(msg)

        try:
            module_name, func_name = call_name.rsplit(".", 1)
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
        except (ImportError, AttributeError, ModuleNotFoundError) as e:
            msg = f"Failed to import or find function: {call_name}"
            raise ValueError(msg) from e

        for args in it:
            try:
                func([*base_args, *args])
            except Exception as e:  # noqa: PERF203
                msg = f"Function call '{job.call}' failed with args: {args}"
                raise RuntimeError(msg) from e


def to_text(job: Job) -> str:
    """Convert the job configuration to a string.

    This function returns the job configuration for a given job.

    Args:
        job (Job): The job configuration to show.

    Returns:
        str: The job configuration.

    """
    text = ""

    it = iter_batches(job)

    if job.run:
        base_cmds = shlex.split(job.run)
        for args in it:
            cmds = " ".join([*base_cmds, *args])
            text += f"{cmds}\n"

    elif job.call:
        text = f"call: {job.call}\n"
        for args in it:
            text += f"args: {args}\n"

    return text.rstrip()
