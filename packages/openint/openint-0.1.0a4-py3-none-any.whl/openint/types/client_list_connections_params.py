# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ClientListConnectionsParams"]


class ClientListConnectionsParams(TypedDict, total=False):
    connector_config_id: str
    """The id of the connector config, starts with `ccfg_`"""

    connector_name: Literal[
        "aircall",
        "airtable",
        "apollo",
        "beancount",
        "brex",
        "coda",
        "confluence",
        "discord",
        "finch",
        "firebase",
        "foreceipt",
        "github",
        "gong",
        "google",
        "greenhouse",
        "heron",
        "hubspot",
        "intercom",
        "jira",
        "kustomer",
        "lever",
        "linear",
        "lunchmoney",
        "merge",
        "microsoft",
        "moota",
        "onebrick",
        "outreach",
        "pipedrive",
        "plaid",
        "qbo",
        "ramp",
        "salesforce",
        "salesloft",
        "saltedge",
        "slack",
        "splitwise",
        "stripe",
        "teller",
        "toggl",
        "twenty",
        "wise",
        "xero",
        "yodlee",
        "zohodesk",
        "googledrive",
    ]
    """The name of the connector"""

    customer_id: str
    """The id of the customer in your application.

    Ensure it is unique for that customer.
    """

    expand: List[Literal["connector", "enabled_integrations"]]

    include_secrets: Literal["none", "basic", "all"]
    """Controls secret inclusion: none (default), basic (auth only), or all secrets"""

    limit: int
    """Limit the number of items returned"""

    offset: int
    """Offset the items returned"""
