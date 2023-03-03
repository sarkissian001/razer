from asynctest import TestCase, patch, CoroutineMock

from src.razer.Enums.airbyte_connector_types import ConnectionType
from src.razer.airbyte_base.airbyte_base import AirByteBase


class TestAirByteBase(TestCase):
    def setUp(self) -> None:
        self.airbyte_base = AirByteBase()

        self.workspace_data = {
            "workspaces": [
                {
                    "anonymousDataCollection": False,
                    "customerId": "c77527b6-d856-405d-b6ba-e2d365beeddf",
                    "defaultGeography": "auto",
                    "displaySetupWizard": True,
                    "email": "fake@outlook.com",
                    "initialSetupComplete": True,
                    "name": "500f6675-e1a7-4408-b736-f69d15871b6f",
                    "news": False,
                    "notifications": [],
                    "securityUpdates": False,
                    "slug": "500f6675-e1a7-4408-b736-f69d15871b6f",
                    "workspaceId": "500f6675-e1a7-4408-b736-f69d15871b6f",
                },
                {
                    "anonymousDataCollection": False,
                    "customerId": "18734b39-02e1-46a7-bfa5-4d71fc8e255d",
                    "defaultGeography": "auto",
                    "displaySetupWizard": True,
                    "email": "fake@outlook.com",
                    "initialSetupComplete": True,
                    "name": "COCA COLA",
                    "news": False,
                    "notifications": [],
                    "securityUpdates": False,
                    "slug": "coca-cola",
                    "webhookConfigs": [],
                    "workspaceId": "64f6cbaf-6fea-4b52-ae96-9431c2ce5a1e",
                },
                {
                    "anonymousDataCollection": False,
                    "customerId": "5eb92cdf-1ab6-44f6-ba6d-fac34eca3b1c",
                    "defaultGeography": "auto",
                    "displaySetupWizard": False,
                    "email": "myworkspace@email.com",
                    "initialSetupComplete": False,
                    "name": "MY WORKSPACE",
                    "news": False,
                    "notifications": [],
                    "securityUpdates": False,
                    "slug": "my-workspace",
                    "webhookConfigs": [],
                    "workspaceId": "5ddf3514-9024-4cad-aa1b-915141498842",
                },
                {
                    "anonymousDataCollection": False,
                    "customerId": "93c4cb25-d50d-4a63-9533-28b0b84363db",
                    "defaultGeography": "auto",
                    "displaySetupWizard": False,
                    "email": "myworkspace@email.com",
                    "initialSetupComplete": False,
                    "name": "OSCAR",
                    "news": False,
                    "notifications": [],
                    "securityUpdates": False,
                    "slug": "oscar",
                    "webhookConfigs": [],
                    "workspaceId": "70fe5210-adc3-4fd7-b4ff-86248360e04e",
                },
                {
                    "anonymousDataCollection": False,
                    "customerId": "3cdf15da-feb5-4110-8258-a831b8fe3432",
                    "defaultGeography": "auto",
                    "displaySetupWizard": True,
                    "email": "fake@outlook.com",
                    "initialSetupComplete": True,
                    "name": "Pepsi COLA",
                    "news": False,
                    "notifications": [],
                    "securityUpdates": True,
                    "slug": "pepsi-cola",
                    "webhookConfigs": [],
                    "workspaceId": "ca50d19c-052e-45d8-9f62-ac428f68e2ae",
                },
            ]
        }

    @patch("src.razer.airbyte_base.airbyte_base.aiohttp.ClientSession.post")
    async def test_get_workspaces(self, mock_session):
        mock_session.return_value.__aenter__.return_value.json = CoroutineMock(
            side_effect=[self.workspace_data]
        )

        actual_response = await self.airbyte_base.get_workspaces()

        self.assertEqual(actual_response, self.workspace_data)

        assert mock_session.call_count == 1

        mock_session.assert_called_once_with(
            "http://localhost:8000/api/v1/workspaces/list",
            headers={"Content-Type": "application/json"},
        )

    @patch("src.razer.airbyte_base.airbyte_base.AirByteBase.get_workspaces")
    async def test_get_workspace_ids(self, mock_ws):
        mock_ws.return_value = self.workspace_data

        expected_ws_ids = [
            "500f6675-e1a7-4408-b736-f69d15871b6f",
            "64f6cbaf-6fea-4b52-ae96-9431c2ce5a1e",
            "5ddf3514-9024-4cad-aa1b-915141498842",
            "70fe5210-adc3-4fd7-b4ff-86248360e04e",
            "ca50d19c-052e-45d8-9f62-ac428f68e2ae",
        ]

        actual_response = await self.airbyte_base.get_workspace_ids()

        self.assertEqual(actual_response, expected_ws_ids)

    @patch("src.razer.airbyte_base.airbyte_base.aiohttp.ClientSession.post")
    async def test_create_workspace(self, mock_session):
        expected = {
            "anonymousDataCollection": False,
            "customerId": "54213afa-7e14-4865-85fb-79fe44cd2144",
            "defaultGeography": "auto",
            "displaySetupWizard": False,
            "email": "amazon@email.com",
            "initialSetupComplete": False,
            "name": "AMAZON",
            "news": False,
            "notifications": [],
            "securityUpdates": False,
            "slug": "amazon",
            "webhookConfigs": [],
            "workspaceId": "b018b3bd-803c-43e8-8813-95d2749d1b63",
        }

        mock_session.return_value.__aenter__.return_value.json = CoroutineMock(
            side_effect=[expected]
        )

        actual_response = await self.airbyte_base.create_workspace()

        print(actual_response)

        self.assertEqual(actual_response, expected)

        assert mock_session.call_count == 1

        mock_session.assert_called_once_with(
            "http://localhost:8000/api/v1/workspaces/create",
            headers={"Content-Type": "application/json"},
            json={},
        )

    @patch("src.razer.airbyte_base.airbyte_base.AirByteBase.get_workspaces")
    async def test_get_customer_id(self, mock_ws):
        mock_ws.return_value = self.workspace_data

        ws_id = "500f6675-e1a7-4408-b736-f69d15871b6f"
        expected_customer_id = "c77527b6-d856-405d-b6ba-e2d365beeddf"

        actual_response = await self.airbyte_base.get_customer_id(workspace_id=ws_id)

        self.assertEqual(actual_response, expected_customer_id)

    @patch("src.razer.airbyte_base.airbyte_base.aiohttp.ClientSession.post")
    async def test_get_workspace_connections(self, mock_session):
        expected_data = {
            "connections": [
                {
                    "connectionId": "186a8381-9930-4000-8f34-08c1d1ea5d01",
                    "name": "string",
                    "namespaceDefinition": "source",
                    "namespaceFormat": "fake format ",
                    "prefix": "string",
                    "sourceId": "186a8381-9930-4000-8670-6a79352df601",
                    "destinationId": "186a8381-9930-4000-80eb-86535fc09018",
                    "operationIds": ["186a8381-9930-4000-8d17-6cf719072101"],
                    "syncCatalog": {
                        "streams": [
                            {
                                "stream": {
                                    "name": "string",
                                    "jsonSchema": {},
                                    "supportedSyncModes": ["full_refresh"],
                                    "sourceDefinedCursor": False,
                                    "defaultCursorField": ["string"],
                                    "sourceDefinedPrimaryKey": [["string"]],
                                    "namespace": "string",
                                },
                                "config": {
                                    "syncMode": "full_refresh",
                                    "cursorField": ["string"],
                                    "destinationSyncMode": "append",
                                    "primaryKey": [["string"]],
                                    "aliasName": "string",
                                    "selected": False,
                                    "suggested": False,
                                    "fieldSelectionEnabled": False,
                                    "selectedFields": [{"fieldPath": ["string"]}],
                                },
                            }
                        ]
                    },
                    "schedule": {"units": 0, "timeUnit": "minutes"},
                    "scheduleType": "manual",
                    "scheduleData": {
                        "basicSchedule": {"timeUnit": "minutes", "units": 0},
                        "cron": {
                            "cronExpression": "string",
                            "cronTimeZone": "string",
                        },
                    },
                    "status": "active",
                    "resourceRequirements": {
                        "cpu_request": "string",
                        "cpu_limit": "string",
                        "memory_request": "string",
                        "memory_limit": "string",
                    },
                    "sourceCatalogId": "186a8381-9930-4000-8cd7-68e25498d201",
                    "geography": "auto",
                    "breakingChange": False,
                    "notifySchemaChanges": False,
                    "nonBreakingChangesPreference": "ignore",
                }
            ]
        }

        mock_session.return_value.__aenter__.return_value.json = CoroutineMock(
            side_effect=[expected_data]
        )

        expected_customer_id = "186a8381-9930-4000-8f34-08c1d1ea5d01"

        actual_response = await self.airbyte_base.get_workspace_connections(
            workspace_id="500f6675-e1a7-4408-b736-f69d15871b6f"
        )

        self.assertEqual(actual_response[0], expected_customer_id)

        assert mock_session.call_count == 1

        mock_session.assert_called_once_with(
            url="http://localhost:8000/api/v1/connections/list",
            headers={"Content-Type": "application/json"},
            json={"workspaceId": "500f6675-e1a7-4408-b736-f69d15871b6f"},
        )

    @patch("src.razer.airbyte_base.airbyte_base.aiohttp.ClientSession.post")
    async def test_sync_custom_connector(self, mock_session):
        expected_data = {
            "dockerImageTag": "latest",
            "dockerRepository": "myuser/source-some-api",
            "documentationUrl": "docs",
            "name": "My Source",
            "protocolVersion": "0.2.0",
            "releaseStage": "custom",
            "sourceDefinitionId": "9c5a0609-0b17-4a14-b766-e4e155dfbae6",
        }

        mock_session.return_value.__aenter__.return_value.json = CoroutineMock(
            side_effect=[expected_data]
        )

        actual_response = await self.airbyte_base.sync_custom_connector(
            workspace_id="500f6675-e1a7-4408-b736-f69d15871b6f",
            connection_name="My Source",
            repository_url="myuser/source-some-api",
            image_tag="latest",
            connector_type=ConnectionType.SOURCE,
            documentation_url="docs",
        )

        self.assertEqual(actual_response, expected_data)

        assert mock_session.call_count == 1

        mock_session.assert_called_once_with(
            "http://localhost:8000/api/v1/source_definitions/create_custom",
            headers={"Content-Type": "application/json"},
            json={
                "workspaceId": "500f6675-e1a7-4408-b736-f69d15871b6f",
                "sourceDefinition": {
                    "name": "My Source",
                    "documentationUrl": "docs",
                    "dockerRepository": "myuser/source-some-api",
                    "dockerImageTag": "latest",
                },
            },
            timeout=300,
        )
