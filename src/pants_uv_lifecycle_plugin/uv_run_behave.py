from pants.engine.rules import goal_rule, collect_rules, Get, Effect
from pants.engine.process import InteractiveProcess, InteractiveProcessResult
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.env_vars import EnvironmentVars
from pants_uv_lifecycle_plugin.utils.rule_utils import (
    PathEnvVariableRequest,
    FeatureFileTargets,
    FeatureFilepaths
)
import logging
from pathlib import Path

logger = logging.getLogger("uv_run_behave_logger")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

BEHAVE_DIRECTORY_PATH = 'tests/features'

class UvRunBehaveSubsystem(GoalSubsystem):
    name = "uv-run-behave"
    help = "Run `uv run behave`."

class UvRunBehaveGoal(Goal):
    subsystem_cls = UvRunBehaveSubsystem
    environment_behavior = Goal.EnvironmentBehavior.LOCAL_ONLY

@goal_rule(desc="run `uv run behave`")
async def uv_run_behave_on_pyproject_modules(feature_file_targets: FeatureFileTargets) -> UvRunBehaveGoal:
    path_environment_variable = await Get(EnvironmentVars, PathEnvVariableRequest())
    
    feature_filepaths = await Get(FeatureFilepaths, FeatureFileTargets, feature_file_targets)

    process_result_codes = []
    for feature_filepath in feature_filepaths:
        module_dir = Path(feature_filepath).parent.parent.parent.as_posix()
        logger.info(f"Running `uv run behave` on {module_dir} module...")

        interactive_process_result = await Effect(
            InteractiveProcessResult, 
            InteractiveProcess(
                env=path_environment_variable, 
                argv=["uv", "--directory", module_dir, "run", "behave", BEHAVE_DIRECTORY_PATH],
                description=f"run `uv run behave` in {module_dir} module.", 
                run_in_workspace=True,
            )
        )
        
        process_result_codes.append(interactive_process_result.exit_code)

        logger.info(f"`uv run behave` successfully completed for {module_dir} module.")
    
    logger.info(f"`uv run behave` successfully completed for all modules with behave tests.")
    
    return UvRunBehaveGoal(exit_code=max(process_result_codes))
  
def rules():
    return collect_rules()