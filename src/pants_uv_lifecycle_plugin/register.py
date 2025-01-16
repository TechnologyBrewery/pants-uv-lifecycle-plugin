from pants_uv_lifecycle_plugin import run_uv_sync


def rules():
    return [*run_uv_sync.rules()]
