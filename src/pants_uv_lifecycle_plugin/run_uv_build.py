from pants.engine.env_vars import EnvironmentVars
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.process import InteractiveProcess, InteractiveProcessResult
from pants.engine.rules import goal_rule, collect_rules, Get, Effect
from pants_uv_lifecycle_plugin.utils.rule_utils import (
    PathEnvVariableRequest,
    PyprojectTomlFileTargets,
    PyprojectTomlDirs,
)
import logging

logger = logging.getLogger("uv_build_logger")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


class UvBuildSubsystem(GoalSubsystem):
    name = "uv-build"
    help = "Run `uv build`."


class UvBuildGoal(Goal):
    subsystem_cls = UvBuildSubsystem
    environment_behavior = Goal.EnvironmentBehavior.LOCAL_ONLY


@goal_rule(desc="run `uv build`")
async def run_uv_build_on_pyproject_directories(
    py_targets: PyprojectTomlFileTargets,
) -> UvBuildGoal:
    process_result_codes = []

    path_environment_variable = await Get(EnvironmentVars, PathEnvVariableRequest())

    pyproject_toml_dirs = await Get(
        PyprojectTomlDirs, PyprojectTomlFileTargets, py_targets
    )

    for pyproject_toml_dir in pyproject_toml_dirs.paths:
        logger.info(f"Running `uv build` on {pyproject_toml_dir} directory")

        interactive_process_result = await Effect(
            InteractiveProcessResult,
            InteractiveProcess(
                env=path_environment_variable,
                argv=["uv", "build", "--project", pyproject_toml_dir],
                description=f"run `uv build` in {pyproject_toml_dir} directory",
                run_in_workspace=True,
            ),
        )
        process_result_codes.append(interactive_process_result.exit_code)

        logger.info(f"`uv build` completed for {pyproject_toml_dir}")

    logger.info("`uv build` completed for all pyproject.toml-based projects.")

    return UvBuildGoal(exit_code=max(process_result_codes))


def rules():
    return collect_rules()
