# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["ClientListConnectionConfigsParams"]


class ClientListConnectionConfigsParams(TypedDict, total=False):
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

    expand: str

    limit: int
    """Limit the number of items returned"""

    offset: int
    """Offset the items returned"""
