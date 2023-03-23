from dagster_airbyte import airbyte_resource
from dagster_dbt import dbt_cli_resource

from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module, AssetSelection,
)

from . import assets


# my_job = define_asset_job("sync_addresses", selection=AssetSelection.all())
# schedule = ScheduleDefinition(job=my_job, cron_schedule="*/1 * * * *")

# defs = Definitions(
#     assets=[airbyte_assets],
#     jobs=[my_job],
#     schedules=[schedule],
# )

defs = Definitions(
    assets=load_assets_from_package_module(assets),
    schedules=[
        # update all assets once a day
        ScheduleDefinition(
            job=define_asset_job("sync_addresses", selection=AssetSelection.all()),
            cron_schedule="*/1 * * * *"
        ),
    ],
)