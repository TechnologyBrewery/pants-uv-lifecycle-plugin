from pants.engine.rules import goal_rule, collect_rules, Get, Effect
from pants.engine.process import InteractiveProcess, InteractiveProcessResult
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.env_vars import EnvironmentVars, EnvironmentVarsRequest
from pants.engine.fs import Paths, PathGlobs
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
async def run_uv_sync_on_pyproject_directories() -> UvSyncGoal:
    path_environment_variable = await Get(
            EnvironmentVars, EnvironmentVarsRequest(["PATH"])
        )
    
    # A Snapshot allows access to the relative directory paths of the given files
    pyproject_toml_paths = await Get(Paths, PathGlobs(["**/pyproject.toml"]))

    process_result_codes = []
    for pyproject_toml_filepath in pyproject_toml_paths.files:
        pyproject_toml_parent_dir = pyproject_toml_filepath.rsplit('/', maxsplit=1)[0]
        logger.info(f"Running `uv sync` on {pyproject_toml_parent_dir}...")

        interactive_process_result = await Effect(
            InteractiveProcessResult, 
            InteractiveProcess(
                env=path_environment_variable, 
                argv=["uv", "sync", "--project", pyproject_toml_filepath],
                description=f"run `uv sync` in {pyproject_toml_parent_dir}.", 
                run_in_workspace=True,
            )
        )
        
        process_result_codes.append(interactive_process_result.exit_code)

        logger.info(f"`uv sync` successfully completed for {pyproject_toml_parent_dir}.")
    
    logger.info(f"`uv sync` successfully completed for all pyproject.toml-based projects.")
    
    return UvSyncGoal(exit_code=max(process_result_codes))
  
def rules():
    return collect_rules()