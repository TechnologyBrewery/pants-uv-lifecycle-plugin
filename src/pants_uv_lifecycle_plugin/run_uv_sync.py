from pathlib import Path
from pants.engine.rules import goal_rule, collect_rules, Get, Effect
from pants.engine.process import InteractiveProcess, InteractiveProcessResult
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.env_vars import EnvironmentVars
from pants_uv_lifecycle_plugin.utils.rule_utils import (
    PathEnvVariableRequest,
    PyprojectTomlFileTargets,
    PyprojectTomlFilepaths,
)
import logging

logger = logging.getLogger("uv_sync_logger")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


class UvSyncSubsystem(GoalSubsystem):
    name = "uv-sync"
    help = "Run `uv sync`."


class UvSyncGoal(Goal):
    subsystem_cls = UvSyncSubsystem
    environment_behavior = Goal.EnvironmentBehavior.LOCAL_ONLY


@goal_rule(desc="run `uv sync`")
async def run_uv_sync_on_pyproject_directories(
    py_targets: PyprojectTomlFileTargets,
) -> UvSyncGoal:
    process_result_codes = []

    path_environment_variable = await Get(EnvironmentVars, PathEnvVariableRequest())

    pyproject_toml_filepaths = await Get(
        PyprojectTomlFilepaths, PyprojectTomlFileTargets, py_targets
    )

    for pyproject_toml_filepath in pyproject_toml_filepaths.paths:
        pyproject_toml_dir = str(Path(pyproject_toml_filepath).parent)

        logger.info(f"Running `uv sync` on {pyproject_toml_dir} directory")

        interactive_process_result = await Effect(
            InteractiveProcessResult,
            InteractiveProcess(
                env=path_environment_variable,
                argv=[
                    "uv",
                    "sync",
                    "--project",
                    pyproject_toml_filepath,
                    "--no-config",
                ],
                description=f"run `uv sync` in {pyproject_toml_dir} directory",
                run_in_workspace=True,
            ),
        )
        process_result_codes.append(interactive_process_result.exit_code)

        logger.info(f"`uv sync` completed for {pyproject_toml_dir}")

    logger.info("`uv sync` completed for all pyproject.toml-based projects.")

    return UvSyncGoal(exit_code=max(process_result_codes))


def rules():
    return collect_rules()
