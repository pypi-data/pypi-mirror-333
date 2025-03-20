# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "ListConnectionConfigsResponse",
    "ConnectorsAircallConnectorConfig",
    "ConnectorsAircallConnectorConfigConnector",
    "ConnectorsAirtableConnectorConfig",
    "ConnectorsAirtableConnectorConfigConnector",
    "ConnectorsApolloConnectorConfig",
    "ConnectorsApolloConnectorConfigConnector",
    "ConnectorsBeancountConnectorConfig",
    "ConnectorsBeancountConnectorConfigConnector",
    "ConnectorsBrexConnectorConfig",
    "ConnectorsBrexConnectorConfigConfig",
    "ConnectorsBrexConnectorConfigConfigOAuth",
    "ConnectorsBrexConnectorConfigConnector",
    "ConnectorsCodaConnectorConfig",
    "ConnectorsCodaConnectorConfigConnector",
    "ConnectorsConfluenceConnectorConfig",
    "ConnectorsConfluenceConnectorConfigConfig",
    "ConnectorsConfluenceConnectorConfigConfigOAuth",
    "ConnectorsConfluenceConnectorConfigConnector",
    "ConnectorsDiscordConnectorConfig",
    "ConnectorsDiscordConnectorConfigConfig",
    "ConnectorsDiscordConnectorConfigConfigOAuth",
    "ConnectorsDiscordConnectorConfigConnector",
    "ConnectorsFinchConnectorConfig",
    "ConnectorsFinchConnectorConfigConfig",
    "ConnectorsFinchConnectorConfigConnector",
    "ConnectorsFirebaseConnectorConfig",
    "ConnectorsFirebaseConnectorConfigConnector",
    "ConnectorsForeceiptConnectorConfig",
    "ConnectorsForeceiptConnectorConfigConnector",
    "ConnectorsGitHubConnectorConfig",
    "ConnectorsGitHubConnectorConfigConfig",
    "ConnectorsGitHubConnectorConfigConfigOAuth",
    "ConnectorsGitHubConnectorConfigConnector",
    "ConnectorsGongConnectorConfig",
    "ConnectorsGongConnectorConfigConfig",
    "ConnectorsGongConnectorConfigConfigOAuth",
    "ConnectorsGongConnectorConfigConnector",
    "ConnectorsGoogleConnectorConfig",
    "ConnectorsGoogleConnectorConfigConfig",
    "ConnectorsGoogleConnectorConfigConfigIntegrations",
    "ConnectorsGoogleConnectorConfigConfigIntegrationsCalendar",
    "ConnectorsGoogleConnectorConfigConfigIntegrationsDocs",
    "ConnectorsGoogleConnectorConfigConfigIntegrationsDrive",
    "ConnectorsGoogleConnectorConfigConfigIntegrationsGmail",
    "ConnectorsGoogleConnectorConfigConfigIntegrationsSheets",
    "ConnectorsGoogleConnectorConfigConfigIntegrationsSlides",
    "ConnectorsGoogleConnectorConfigConfigOAuth",
    "ConnectorsGoogleConnectorConfigConnector",
    "ConnectorsGreenhouseConnectorConfig",
    "ConnectorsGreenhouseConnectorConfigConnector",
    "ConnectorsHeronConnectorConfig",
    "ConnectorsHeronConnectorConfigConfig",
    "ConnectorsHeronConnectorConfigConnector",
    "ConnectorsHubspotConnectorConfig",
    "ConnectorsHubspotConnectorConfigConfig",
    "ConnectorsHubspotConnectorConfigConfigOAuth",
    "ConnectorsHubspotConnectorConfigConnector",
    "ConnectorsIntercomConnectorConfig",
    "ConnectorsIntercomConnectorConfigConfig",
    "ConnectorsIntercomConnectorConfigConfigOAuth",
    "ConnectorsIntercomConnectorConfigConnector",
    "ConnectorsJiraConnectorConfig",
    "ConnectorsJiraConnectorConfigConfig",
    "ConnectorsJiraConnectorConfigConfigOAuth",
    "ConnectorsJiraConnectorConfigConnector",
    "ConnectorsKustomerConnectorConfig",
    "ConnectorsKustomerConnectorConfigConfig",
    "ConnectorsKustomerConnectorConfigConfigOAuth",
    "ConnectorsKustomerConnectorConfigConnector",
    "ConnectorsLeverConnectorConfig",
    "ConnectorsLeverConnectorConfigConfig",
    "ConnectorsLeverConnectorConfigConfigOAuth",
    "ConnectorsLeverConnectorConfigConnector",
    "ConnectorsLinearConnectorConfig",
    "ConnectorsLinearConnectorConfigConfig",
    "ConnectorsLinearConnectorConfigConfigOAuth",
    "ConnectorsLinearConnectorConfigConnector",
    "ConnectorsLunchmoneyConnectorConfig",
    "ConnectorsLunchmoneyConnectorConfigConfig",
    "ConnectorsLunchmoneyConnectorConfigConnector",
    "ConnectorsMercuryConnectorConfig",
    "ConnectorsMercuryConnectorConfigConfig",
    "ConnectorsMercuryConnectorConfigConfigOAuth",
    "ConnectorsMercuryConnectorConfigConnector",
    "ConnectorsMergeConnectorConfig",
    "ConnectorsMergeConnectorConfigConfig",
    "ConnectorsMergeConnectorConfigConnector",
    "ConnectorsMicrosoftConnectorConfig",
    "ConnectorsMicrosoftConnectorConfigConfig",
    "ConnectorsMicrosoftConnectorConfigConfigIntegrations",
    "ConnectorsMicrosoftConnectorConfigConfigIntegrationsOutlook",
    "ConnectorsMicrosoftConnectorConfigConfigIntegrationsSharepoint",
    "ConnectorsMicrosoftConnectorConfigConfigIntegrationsTeams",
    "ConnectorsMicrosoftConnectorConfigConfigOAuth",
    "ConnectorsMicrosoftConnectorConfigConnector",
    "ConnectorsMootaConnectorConfig",
    "ConnectorsMootaConnectorConfigConfig",
    "ConnectorsMootaConnectorConfigConnector",
    "ConnectorsOnebrickConnectorConfig",
    "ConnectorsOnebrickConnectorConfigConfig",
    "ConnectorsOnebrickConnectorConfigConnector",
    "ConnectorsOutreachConnectorConfig",
    "ConnectorsOutreachConnectorConfigConfig",
    "ConnectorsOutreachConnectorConfigConfigOAuth",
    "ConnectorsOutreachConnectorConfigConnector",
    "ConnectorsPipedriveConnectorConfig",
    "ConnectorsPipedriveConnectorConfigConfig",
    "ConnectorsPipedriveConnectorConfigConfigOAuth",
    "ConnectorsPipedriveConnectorConfigConnector",
    "ConnectorsPlaidConnectorConfig",
    "ConnectorsPlaidConnectorConfigConfig",
    "ConnectorsPlaidConnectorConfigConfigCredentials",
    "ConnectorsPlaidConnectorConfigConnector",
    "ConnectorsPostgresConnectorConfig",
    "ConnectorsPostgresConnectorConfigConnector",
    "ConnectorsQboConnectorConfig",
    "ConnectorsQboConnectorConfigConfig",
    "ConnectorsQboConnectorConfigConfigOAuth",
    "ConnectorsQboConnectorConfigConnector",
    "ConnectorsRampConnectorConfig",
    "ConnectorsRampConnectorConfigConfig",
    "ConnectorsRampConnectorConfigConfigOAuth",
    "ConnectorsRampConnectorConfigConnector",
    "ConnectorsSalesforceConnectorConfig",
    "ConnectorsSalesforceConnectorConfigConfig",
    "ConnectorsSalesforceConnectorConfigConfigOAuth",
    "ConnectorsSalesforceConnectorConfigConnector",
    "ConnectorsSalesloftConnectorConfig",
    "ConnectorsSalesloftConnectorConfigConfig",
    "ConnectorsSalesloftConnectorConfigConfigOAuth",
    "ConnectorsSalesloftConnectorConfigConnector",
    "ConnectorsSaltedgeConnectorConfig",
    "ConnectorsSaltedgeConnectorConfigConfig",
    "ConnectorsSaltedgeConnectorConfigConnector",
    "ConnectorsSlackConnectorConfig",
    "ConnectorsSlackConnectorConfigConfig",
    "ConnectorsSlackConnectorConfigConfigOAuth",
    "ConnectorsSlackConnectorConfigConnector",
    "ConnectorsSplitwiseConnectorConfig",
    "ConnectorsSplitwiseConnectorConfigConnector",
    "ConnectorsStripeConnectorConfig",
    "ConnectorsStripeConnectorConfigConfig",
    "ConnectorsStripeConnectorConfigConfigOAuth",
    "ConnectorsStripeConnectorConfigConnector",
    "ConnectorsTellerConnectorConfig",
    "ConnectorsTellerConnectorConfigConfig",
    "ConnectorsTellerConnectorConfigConnector",
    "ConnectorsTogglConnectorConfig",
    "ConnectorsTogglConnectorConfigConnector",
    "ConnectorsTwentyConnectorConfig",
    "ConnectorsTwentyConnectorConfigConnector",
    "ConnectorsVenmoConnectorConfig",
    "ConnectorsVenmoConnectorConfigConfig",
    "ConnectorsVenmoConnectorConfigConfigProxy",
    "ConnectorsVenmoConnectorConfigConnector",
    "ConnectorsWiseConnectorConfig",
    "ConnectorsWiseConnectorConfigConnector",
    "ConnectorsXeroConnectorConfig",
    "ConnectorsXeroConnectorConfigConfig",
    "ConnectorsXeroConnectorConfigConfigOAuth",
    "ConnectorsXeroConnectorConfigConnector",
    "ConnectorsYodleeConnectorConfig",
    "ConnectorsYodleeConnectorConfigConfig",
    "ConnectorsYodleeConnectorConfigConfigProxy",
    "ConnectorsYodleeConnectorConfigConnector",
    "ConnectorsZohodeskConnectorConfig",
    "ConnectorsZohodeskConnectorConfigConfig",
    "ConnectorsZohodeskConnectorConfigConfigOAuth",
    "ConnectorsZohodeskConnectorConfigConnector",
    "ConnectorsGoogledriveConnectorConfig",
    "ConnectorsGoogledriveConnectorConfigConfig",
    "ConnectorsGoogledriveConnectorConfigConnector",
]


class ConnectorsAircallConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsAircallConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["aircall"]

    id: Optional[str] = None

    connector: Optional[ConnectorsAircallConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsAirtableConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsAirtableConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["airtable"]

    id: Optional[str] = None

    connector: Optional[ConnectorsAirtableConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsApolloConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsApolloConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["apollo"]

    id: Optional[str] = None

    connector: Optional[ConnectorsApolloConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsBeancountConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsBeancountConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["beancount"]

    id: Optional[str] = None

    connector: Optional[ConnectorsBeancountConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsBrexConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorsBrexConnectorConfigConfig(BaseModel):
    apikey_auth: Optional[bool] = FieldInfo(alias="apikeyAuth", default=None)
    """API key auth support"""

    oauth: Optional[ConnectorsBrexConnectorConfigConfigOAuth] = None
    """Configure oauth"""


class ConnectorsBrexConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsBrexConnectorConfig(BaseModel):
    config: ConnectorsBrexConnectorConfigConfig

    connector_name: Literal["brex"]

    id: Optional[str] = None

    connector: Optional[ConnectorsBrexConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsCodaConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsCodaConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["coda"]

    id: Optional[str] = None

    connector: Optional[ConnectorsCodaConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsConfluenceConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsConfluenceConnectorConfigConfig(BaseModel):
    oauth: ConnectorsConfluenceConnectorConfigConfigOAuth


class ConnectorsConfluenceConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsConfluenceConnectorConfig(BaseModel):
    config: ConnectorsConfluenceConnectorConfigConfig

    connector_name: Literal["confluence"]

    id: Optional[str] = None

    connector: Optional[ConnectorsConfluenceConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsDiscordConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsDiscordConnectorConfigConfig(BaseModel):
    oauth: ConnectorsDiscordConnectorConfigConfigOAuth


class ConnectorsDiscordConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsDiscordConnectorConfig(BaseModel):
    config: ConnectorsDiscordConnectorConfigConfig

    connector_name: Literal["discord"]

    id: Optional[str] = None

    connector: Optional[ConnectorsDiscordConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsFinchConnectorConfigConfig(BaseModel):
    client_id: str

    client_secret: str

    products: List[
        Literal["company", "directory", "individual", "ssn", "employment", "payment", "pay_statement", "benefits"]
    ]
    """
    Finch products to access, @see
    https://developer.tryfinch.com/api-reference/development-guides/Permissions
    """

    api_version: Optional[str] = None
    """Finch API version"""


class ConnectorsFinchConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsFinchConnectorConfig(BaseModel):
    config: ConnectorsFinchConnectorConfigConfig

    connector_name: Literal["finch"]

    id: Optional[str] = None

    connector: Optional[ConnectorsFinchConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsFirebaseConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsFirebaseConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["firebase"]

    id: Optional[str] = None

    connector: Optional[ConnectorsFirebaseConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsForeceiptConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsForeceiptConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["foreceipt"]

    id: Optional[str] = None

    connector: Optional[ConnectorsForeceiptConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsGitHubConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsGitHubConnectorConfigConfig(BaseModel):
    oauth: ConnectorsGitHubConnectorConfigConfigOAuth


class ConnectorsGitHubConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsGitHubConnectorConfig(BaseModel):
    config: ConnectorsGitHubConnectorConfigConfig

    connector_name: Literal["github"]

    id: Optional[str] = None

    connector: Optional[ConnectorsGitHubConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsGongConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsGongConnectorConfigConfig(BaseModel):
    oauth: ConnectorsGongConnectorConfigConfigOAuth


class ConnectorsGongConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsGongConnectorConfig(BaseModel):
    config: ConnectorsGongConnectorConfigConfig

    connector_name: Literal["gong"]

    id: Optional[str] = None

    connector: Optional[ConnectorsGongConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsGoogleConnectorConfigConfigIntegrationsCalendar(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """calendar specific space separated scopes"""


class ConnectorsGoogleConnectorConfigConfigIntegrationsDocs(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """docs specific space separated scopes"""


class ConnectorsGoogleConnectorConfigConfigIntegrationsDrive(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """drive specific space separated scopes"""


class ConnectorsGoogleConnectorConfigConfigIntegrationsGmail(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """gmail specific space separated scopes"""


class ConnectorsGoogleConnectorConfigConfigIntegrationsSheets(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """sheets specific space separated scopes"""


class ConnectorsGoogleConnectorConfigConfigIntegrationsSlides(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """slides specific space separated scopes"""


class ConnectorsGoogleConnectorConfigConfigIntegrations(BaseModel):
    calendar: Optional[ConnectorsGoogleConnectorConfigConfigIntegrationsCalendar] = None

    docs: Optional[ConnectorsGoogleConnectorConfigConfigIntegrationsDocs] = None

    drive: Optional[ConnectorsGoogleConnectorConfigConfigIntegrationsDrive] = None

    gmail: Optional[ConnectorsGoogleConnectorConfigConfigIntegrationsGmail] = None

    sheets: Optional[ConnectorsGoogleConnectorConfigConfigIntegrationsSheets] = None

    slides: Optional[ConnectorsGoogleConnectorConfigConfigIntegrationsSlides] = None


class ConnectorsGoogleConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None
    """global google connector space separated scopes"""


class ConnectorsGoogleConnectorConfigConfig(BaseModel):
    integrations: ConnectorsGoogleConnectorConfigConfigIntegrations

    oauth: ConnectorsGoogleConnectorConfigConfigOAuth


class ConnectorsGoogleConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsGoogleConnectorConfig(BaseModel):
    config: ConnectorsGoogleConnectorConfigConfig

    connector_name: Literal["google"]

    id: Optional[str] = None

    connector: Optional[ConnectorsGoogleConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsGreenhouseConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsGreenhouseConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["greenhouse"]

    id: Optional[str] = None

    connector: Optional[ConnectorsGreenhouseConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsHeronConnectorConfigConfig(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorsHeronConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsHeronConnectorConfig(BaseModel):
    config: ConnectorsHeronConnectorConfigConfig

    connector_name: Literal["heron"]

    id: Optional[str] = None

    connector: Optional[ConnectorsHeronConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsHubspotConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsHubspotConnectorConfigConfig(BaseModel):
    oauth: ConnectorsHubspotConnectorConfigConfigOAuth


class ConnectorsHubspotConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsHubspotConnectorConfig(BaseModel):
    config: ConnectorsHubspotConnectorConfigConfig

    connector_name: Literal["hubspot"]

    id: Optional[str] = None

    connector: Optional[ConnectorsHubspotConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsIntercomConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsIntercomConnectorConfigConfig(BaseModel):
    oauth: ConnectorsIntercomConnectorConfigConfigOAuth


class ConnectorsIntercomConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsIntercomConnectorConfig(BaseModel):
    config: ConnectorsIntercomConnectorConfigConfig

    connector_name: Literal["intercom"]

    id: Optional[str] = None

    connector: Optional[ConnectorsIntercomConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsJiraConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsJiraConnectorConfigConfig(BaseModel):
    oauth: ConnectorsJiraConnectorConfigConfigOAuth


class ConnectorsJiraConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsJiraConnectorConfig(BaseModel):
    config: ConnectorsJiraConnectorConfigConfig

    connector_name: Literal["jira"]

    id: Optional[str] = None

    connector: Optional[ConnectorsJiraConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsKustomerConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsKustomerConnectorConfigConfig(BaseModel):
    oauth: ConnectorsKustomerConnectorConfigConfigOAuth


class ConnectorsKustomerConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsKustomerConnectorConfig(BaseModel):
    config: ConnectorsKustomerConnectorConfigConfig

    connector_name: Literal["kustomer"]

    id: Optional[str] = None

    connector: Optional[ConnectorsKustomerConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsLeverConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsLeverConnectorConfigConfig(BaseModel):
    env_name: Literal["sandbox", "production"] = FieldInfo(alias="envName")

    oauth: ConnectorsLeverConnectorConfigConfigOAuth


class ConnectorsLeverConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsLeverConnectorConfig(BaseModel):
    config: ConnectorsLeverConnectorConfigConfig

    connector_name: Literal["lever"]

    id: Optional[str] = None

    connector: Optional[ConnectorsLeverConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsLinearConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsLinearConnectorConfigConfig(BaseModel):
    oauth: ConnectorsLinearConnectorConfigConfigOAuth


class ConnectorsLinearConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsLinearConnectorConfig(BaseModel):
    config: ConnectorsLinearConnectorConfigConfig

    connector_name: Literal["linear"]

    id: Optional[str] = None

    connector: Optional[ConnectorsLinearConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsLunchmoneyConnectorConfigConfig(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")


class ConnectorsLunchmoneyConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsLunchmoneyConnectorConfig(BaseModel):
    config: ConnectorsLunchmoneyConnectorConfigConfig

    connector_name: Literal["lunchmoney"]

    id: Optional[str] = None

    connector: Optional[ConnectorsLunchmoneyConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsMercuryConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorsMercuryConnectorConfigConfig(BaseModel):
    apikey_auth: Optional[bool] = FieldInfo(alias="apikeyAuth", default=None)
    """API key auth support"""

    oauth: Optional[ConnectorsMercuryConnectorConfigConfigOAuth] = None
    """Configure oauth"""


class ConnectorsMercuryConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsMercuryConnectorConfig(BaseModel):
    config: ConnectorsMercuryConnectorConfigConfig

    connector_name: Literal["mercury"]

    id: Optional[str] = None

    connector: Optional[ConnectorsMercuryConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsMergeConnectorConfigConfig(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorsMergeConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsMergeConnectorConfig(BaseModel):
    config: ConnectorsMergeConnectorConfigConfig

    connector_name: Literal["merge"]

    id: Optional[str] = None

    connector: Optional[ConnectorsMergeConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsMicrosoftConnectorConfigConfigIntegrationsOutlook(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """outlook specific space separated scopes"""


class ConnectorsMicrosoftConnectorConfigConfigIntegrationsSharepoint(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """sharepoint specific space separated scopes"""


class ConnectorsMicrosoftConnectorConfigConfigIntegrationsTeams(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """teams specific space separated scopes"""


class ConnectorsMicrosoftConnectorConfigConfigIntegrations(BaseModel):
    outlook: Optional[ConnectorsMicrosoftConnectorConfigConfigIntegrationsOutlook] = None

    sharepoint: Optional[ConnectorsMicrosoftConnectorConfigConfigIntegrationsSharepoint] = None

    teams: Optional[ConnectorsMicrosoftConnectorConfigConfigIntegrationsTeams] = None


class ConnectorsMicrosoftConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None
    """global microsoft connector space separated scopes"""


class ConnectorsMicrosoftConnectorConfigConfig(BaseModel):
    integrations: ConnectorsMicrosoftConnectorConfigConfigIntegrations

    oauth: ConnectorsMicrosoftConnectorConfigConfigOAuth


class ConnectorsMicrosoftConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsMicrosoftConnectorConfig(BaseModel):
    config: ConnectorsMicrosoftConnectorConfigConfig

    connector_name: Literal["microsoft"]

    id: Optional[str] = None

    connector: Optional[ConnectorsMicrosoftConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsMootaConnectorConfigConfig(BaseModel):
    token: str


class ConnectorsMootaConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsMootaConnectorConfig(BaseModel):
    config: ConnectorsMootaConnectorConfigConfig

    connector_name: Literal["moota"]

    id: Optional[str] = None

    connector: Optional[ConnectorsMootaConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsOnebrickConnectorConfigConfig(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")

    env_name: Literal["sandbox", "production"] = FieldInfo(alias="envName")

    public_token: str = FieldInfo(alias="publicToken")

    access_token: Optional[str] = FieldInfo(alias="accessToken", default=None)

    redirect_url: Optional[str] = FieldInfo(alias="redirectUrl", default=None)


class ConnectorsOnebrickConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsOnebrickConnectorConfig(BaseModel):
    config: ConnectorsOnebrickConnectorConfigConfig

    connector_name: Literal["onebrick"]

    id: Optional[str] = None

    connector: Optional[ConnectorsOnebrickConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsOutreachConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsOutreachConnectorConfigConfig(BaseModel):
    oauth: ConnectorsOutreachConnectorConfigConfigOAuth


class ConnectorsOutreachConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsOutreachConnectorConfig(BaseModel):
    config: ConnectorsOutreachConnectorConfigConfig

    connector_name: Literal["outreach"]

    id: Optional[str] = None

    connector: Optional[ConnectorsOutreachConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsPipedriveConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsPipedriveConnectorConfigConfig(BaseModel):
    oauth: ConnectorsPipedriveConnectorConfigConfigOAuth


class ConnectorsPipedriveConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsPipedriveConnectorConfig(BaseModel):
    config: ConnectorsPipedriveConnectorConfigConfig

    connector_name: Literal["pipedrive"]

    id: Optional[str] = None

    connector: Optional[ConnectorsPipedriveConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsPlaidConnectorConfigConfigCredentials(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorsPlaidConnectorConfigConfig(BaseModel):
    client_name: str = FieldInfo(alias="clientName")
    """
    The name of your application, as it should be displayed in Link. Maximum length
    of 30 characters. If a value longer than 30 characters is provided, Link will
    display "This Application" instead.
    """

    country_codes: List[
        Literal["US", "GB", "ES", "NL", "FR", "IE", "CA", "DE", "IT", "PL", "DK", "NO", "SE", "EE", "LT", "LV"]
    ] = FieldInfo(alias="countryCodes")

    env_name: Literal["sandbox", "development", "production"] = FieldInfo(alias="envName")

    language: Literal["en", "fr", "es", "nl", "de"]

    products: List[
        Literal[
            "assets",
            "auth",
            "balance",
            "identity",
            "investments",
            "liabilities",
            "payment_initiation",
            "identity_verification",
            "transactions",
            "credit_details",
            "income",
            "income_verification",
            "deposit_switch",
            "standing_orders",
            "transfer",
            "employment",
            "recurring_transactions",
        ]
    ]

    credentials: Optional[ConnectorsPlaidConnectorConfigConfigCredentials] = None


class ConnectorsPlaidConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsPlaidConnectorConfig(BaseModel):
    config: ConnectorsPlaidConnectorConfigConfig

    connector_name: Literal["plaid"]

    id: Optional[str] = None

    connector: Optional[ConnectorsPlaidConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsPostgresConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsPostgresConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["postgres"]

    id: Optional[str] = None

    connector: Optional[ConnectorsPostgresConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsQboConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsQboConnectorConfigConfig(BaseModel):
    env_name: Literal["sandbox", "production"] = FieldInfo(alias="envName")

    oauth: ConnectorsQboConnectorConfigConfigOAuth

    url: Optional[str] = None
    """For proxies, not typically needed"""

    verifier_token: Optional[str] = FieldInfo(alias="verifierToken", default=None)
    """For webhooks"""


class ConnectorsQboConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsQboConnectorConfig(BaseModel):
    config: ConnectorsQboConnectorConfigConfig

    connector_name: Literal["qbo"]

    id: Optional[str] = None

    connector: Optional[ConnectorsQboConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsRampConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorsRampConnectorConfigConfig(BaseModel):
    oauth: ConnectorsRampConnectorConfigConfigOAuth


class ConnectorsRampConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsRampConnectorConfig(BaseModel):
    config: ConnectorsRampConnectorConfigConfig

    connector_name: Literal["ramp"]

    id: Optional[str] = None

    connector: Optional[ConnectorsRampConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsSalesforceConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsSalesforceConnectorConfigConfig(BaseModel):
    oauth: ConnectorsSalesforceConnectorConfigConfigOAuth


class ConnectorsSalesforceConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsSalesforceConnectorConfig(BaseModel):
    config: ConnectorsSalesforceConnectorConfigConfig

    connector_name: Literal["salesforce"]

    id: Optional[str] = None

    connector: Optional[ConnectorsSalesforceConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsSalesloftConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsSalesloftConnectorConfigConfig(BaseModel):
    oauth: ConnectorsSalesloftConnectorConfigConfigOAuth


class ConnectorsSalesloftConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsSalesloftConnectorConfig(BaseModel):
    config: ConnectorsSalesloftConnectorConfigConfig

    connector_name: Literal["salesloft"]

    id: Optional[str] = None

    connector: Optional[ConnectorsSalesloftConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsSaltedgeConnectorConfigConfig(BaseModel):
    app_id: str = FieldInfo(alias="appId")

    secret: str

    url: Optional[str] = None


class ConnectorsSaltedgeConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsSaltedgeConnectorConfig(BaseModel):
    config: ConnectorsSaltedgeConnectorConfigConfig

    connector_name: Literal["saltedge"]

    id: Optional[str] = None

    connector: Optional[ConnectorsSaltedgeConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsSlackConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsSlackConnectorConfigConfig(BaseModel):
    oauth: ConnectorsSlackConnectorConfigConfigOAuth


class ConnectorsSlackConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsSlackConnectorConfig(BaseModel):
    config: ConnectorsSlackConnectorConfigConfig

    connector_name: Literal["slack"]

    id: Optional[str] = None

    connector: Optional[ConnectorsSlackConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsSplitwiseConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsSplitwiseConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["splitwise"]

    id: Optional[str] = None

    connector: Optional[ConnectorsSplitwiseConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsStripeConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorsStripeConnectorConfigConfig(BaseModel):
    apikey_auth: Optional[bool] = FieldInfo(alias="apikeyAuth", default=None)
    """API key auth support"""

    oauth: Optional[ConnectorsStripeConnectorConfigConfigOAuth] = None
    """Configure oauth"""


class ConnectorsStripeConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsStripeConnectorConfig(BaseModel):
    config: ConnectorsStripeConnectorConfigConfig

    connector_name: Literal["stripe"]

    id: Optional[str] = None

    connector: Optional[ConnectorsStripeConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsTellerConnectorConfigConfig(BaseModel):
    application_id: str = FieldInfo(alias="applicationId")

    token: Optional[str] = None


class ConnectorsTellerConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsTellerConnectorConfig(BaseModel):
    config: ConnectorsTellerConnectorConfigConfig

    connector_name: Literal["teller"]

    id: Optional[str] = None

    connector: Optional[ConnectorsTellerConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsTogglConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsTogglConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["toggl"]

    id: Optional[str] = None

    connector: Optional[ConnectorsTogglConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsTwentyConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsTwentyConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["twenty"]

    id: Optional[str] = None

    connector: Optional[ConnectorsTwentyConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsVenmoConnectorConfigConfigProxy(BaseModel):
    cert: str

    url: str


class ConnectorsVenmoConnectorConfigConfig(BaseModel):
    proxy: Optional[ConnectorsVenmoConnectorConfigConfigProxy] = None

    v1_base_url: Optional[str] = FieldInfo(alias="v1BaseURL", default=None)

    v5_base_url: Optional[str] = FieldInfo(alias="v5BaseURL", default=None)


class ConnectorsVenmoConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsVenmoConnectorConfig(BaseModel):
    config: ConnectorsVenmoConnectorConfigConfig

    connector_name: Literal["venmo"]

    id: Optional[str] = None

    connector: Optional[ConnectorsVenmoConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsWiseConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsWiseConnectorConfig(BaseModel):
    config: None

    connector_name: Literal["wise"]

    id: Optional[str] = None

    connector: Optional[ConnectorsWiseConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsXeroConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsXeroConnectorConfigConfig(BaseModel):
    oauth: ConnectorsXeroConnectorConfigConfigOAuth


class ConnectorsXeroConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsXeroConnectorConfig(BaseModel):
    config: ConnectorsXeroConnectorConfigConfig

    connector_name: Literal["xero"]

    id: Optional[str] = None

    connector: Optional[ConnectorsXeroConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsYodleeConnectorConfigConfigProxy(BaseModel):
    cert: str

    url: str


class ConnectorsYodleeConnectorConfigConfig(BaseModel):
    admin_login_name: str = FieldInfo(alias="adminLoginName")

    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")

    env_name: Literal["sandbox", "development", "production"] = FieldInfo(alias="envName")

    proxy: Optional[ConnectorsYodleeConnectorConfigConfigProxy] = None

    sandbox_login_name: Optional[str] = FieldInfo(alias="sandboxLoginName", default=None)


class ConnectorsYodleeConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsYodleeConnectorConfig(BaseModel):
    config: ConnectorsYodleeConnectorConfigConfig

    connector_name: Literal["yodlee"]

    id: Optional[str] = None

    connector: Optional[ConnectorsYodleeConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsZohodeskConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorsZohodeskConnectorConfigConfig(BaseModel):
    oauth: ConnectorsZohodeskConnectorConfigConfigOAuth


class ConnectorsZohodeskConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsZohodeskConnectorConfig(BaseModel):
    config: ConnectorsZohodeskConnectorConfigConfig

    connector_name: Literal["zohodesk"]

    id: Optional[str] = None

    connector: Optional[ConnectorsZohodeskConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorsGoogledriveConnectorConfigConfig(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[List[str]] = None


class ConnectorsGoogledriveConnectorConfigConnector(BaseModel):
    name: str

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[str]] = None

    stage: Optional[str] = None


class ConnectorsGoogledriveConnectorConfig(BaseModel):
    config: ConnectorsGoogledriveConnectorConfigConfig

    connector_name: Literal["googledrive"]

    id: Optional[str] = None

    connector: Optional[ConnectorsGoogledriveConnectorConfigConnector] = None

    created_at: Optional[str] = None

    integrations: Optional[Dict[str, Dict[str, object]]] = None

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


ListConnectionConfigsResponse: TypeAlias = Union[
    ConnectorsAircallConnectorConfig,
    ConnectorsAirtableConnectorConfig,
    ConnectorsApolloConnectorConfig,
    ConnectorsBeancountConnectorConfig,
    ConnectorsBrexConnectorConfig,
    ConnectorsCodaConnectorConfig,
    ConnectorsConfluenceConnectorConfig,
    ConnectorsDiscordConnectorConfig,
    ConnectorsFinchConnectorConfig,
    ConnectorsFirebaseConnectorConfig,
    ConnectorsForeceiptConnectorConfig,
    ConnectorsGitHubConnectorConfig,
    ConnectorsGongConnectorConfig,
    ConnectorsGoogleConnectorConfig,
    ConnectorsGreenhouseConnectorConfig,
    ConnectorsHeronConnectorConfig,
    ConnectorsHubspotConnectorConfig,
    ConnectorsIntercomConnectorConfig,
    ConnectorsJiraConnectorConfig,
    ConnectorsKustomerConnectorConfig,
    ConnectorsLeverConnectorConfig,
    ConnectorsLinearConnectorConfig,
    ConnectorsLunchmoneyConnectorConfig,
    ConnectorsMercuryConnectorConfig,
    ConnectorsMergeConnectorConfig,
    ConnectorsMicrosoftConnectorConfig,
    ConnectorsMootaConnectorConfig,
    ConnectorsOnebrickConnectorConfig,
    ConnectorsOutreachConnectorConfig,
    ConnectorsPipedriveConnectorConfig,
    ConnectorsPlaidConnectorConfig,
    ConnectorsPostgresConnectorConfig,
    ConnectorsQboConnectorConfig,
    ConnectorsRampConnectorConfig,
    ConnectorsSalesforceConnectorConfig,
    ConnectorsSalesloftConnectorConfig,
    ConnectorsSaltedgeConnectorConfig,
    ConnectorsSlackConnectorConfig,
    ConnectorsSplitwiseConnectorConfig,
    ConnectorsStripeConnectorConfig,
    ConnectorsTellerConnectorConfig,
    ConnectorsTogglConnectorConfig,
    ConnectorsTwentyConnectorConfig,
    ConnectorsVenmoConnectorConfig,
    ConnectorsWiseConnectorConfig,
    ConnectorsXeroConnectorConfig,
    ConnectorsYodleeConnectorConfig,
    ConnectorsZohodeskConnectorConfig,
    ConnectorsGoogledriveConnectorConfig,
]
