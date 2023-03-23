from dagster import (
    repository,
    ScheduleDefinition,
    define_asset_job,
    AssetSelection,
    DefaultScheduleStatus,
)

from .assets.assets import airbyte_assets


airbyte_asset_job = define_asset_job(
    name="airbyte_asset_sync",
    selection=AssetSelection.all(),
)

airbyte_update_schedule = ScheduleDefinition(
    name="daily_airbyte_sync",
    cron_schedule="0 4 * * *",
    job=airbyte_asset_job,
    execution_timezone="UTC",
    default_status=DefaultScheduleStatus.RUNNING,
)


@repository
def airbyte_connections():
    return [airbyte_assets, airbyte_asset_job, airbyte_update_schedule]
