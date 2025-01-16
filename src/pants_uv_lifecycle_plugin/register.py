from pants_uv_lifecycle_plugin import run_uv_sync, run_uv_build, uv_run_behave
from pants_uv_lifecycle_plugin.utils import rule_utils

def rules():
    return [*run_uv_sync.rules(), *run_uv_build.rules(), *rule_utils.rules(), *uv_run_behave.rules()]
