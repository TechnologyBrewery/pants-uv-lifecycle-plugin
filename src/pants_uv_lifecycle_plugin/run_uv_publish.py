from pants.engine.env_vars import EnvironmentVars
from pants.engine.goal import Goal, GoalSubsystem
from pants.option.option_types import StrOption, StrListOption
from pants.engine.process import InteractiveProcess, InteractiveProcessResult
from pants.engine.rules import goal_rule, collect_rules, Get, Effect
from pants_uv_lifecycle_plugin.utils.rule_utils import (
    PathEnvVariableRequest,
    PyprojectTomlFileTargets,
    PyprojectTomlDirs,
)
import logging
from fnmatch import fnmatch

logger = logging.getLogger("uv_publish_logger")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


class UvPublishSubsystem(GoalSubsystem):
    name = "uv-publish"
    help = "Run `uv publish`."

    token = StrOption(
        help="Authentication token.",
        default=None,
    )
    url = StrOption(
        help="URL to publish to.",
        default=None,
    )

    ignore_dirs = StrListOption(
        help="List of directories to ignore when running `uv publish`.", default=[]
    )


class UvPublishGoal(Goal):
    subsystem_cls = UvPublishSubsystem
    environment_behavior = Goal.EnvironmentBehavior.LOCAL_ONLY


@goal_rule(desc="run `uv publish`")
async def run_uv_build_on_pyproject_directories(
    subsystem: UvPublishSubsystem,
    py_targets: PyprojectTomlFileTargets,
) -> UvPublishGoal:
    process_result_codes = []
    publish_url = subsystem.options.url
    token = subsystem.options.token
    ignore_dirs = subsystem.options.ignore_dirs

    path_environment_variable = await Get(EnvironmentVars, PathEnvVariableRequest())

    pyproject_toml_dirs = await Get(
        PyprojectTomlDirs, PyprojectTomlFileTargets, py_targets
    )
    for pyproject_toml_dir in pyproject_toml_dirs.paths:
        if not any(fnmatch(pyproject_toml_dir, pattern) for pattern in ignore_dirs):
            logger.info(f"Running `uv publish` on {pyproject_toml_dir} directory")

            argv = ["uv", "publish", "--project", pyproject_toml_dir]

            if publish_url:
                argv.extend(["--publish-url", publish_url])

            if token:
                argv.extend(["--token", token])

            interactive_process_result = await Effect(
                InteractiveProcessResult,
                InteractiveProcess(
                    env=path_environment_variable,
                    argv=argv,
                    description=f"run `uv publish` in {pyproject_toml_dir} directory",
                    run_in_workspace=True,
                ),
            )
            process_result_codes.append(interactive_process_result.exit_code)

            logger.info(f"`uv publish` completed for {pyproject_toml_dir}")

        else:
            logger.info(
                f"Skipping publishing for {pyproject_toml_dir}, because it matches an ignore pattern."
            )

    logger.info("`uv publish` completed for all pyproject.toml-based projects.")

    return UvPublishGoal(exit_code=max(process_result_codes))


def rules():
    return collect_rules()
