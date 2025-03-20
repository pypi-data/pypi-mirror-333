# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ClientCreateMagicLinkParams"]


class ClientCreateMagicLinkParams(TypedDict, total=False):
    connection_id: str
    """The specific connection id to load"""

    connector_names: List[
        Literal[
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
    ]
    """Filter integrations by connector names"""

    redirect_url: str
    """Where to send user to after connect / if they press back button"""

    theme: Literal["light", "dark"]
    """Magic Link display theme"""

    validity_in_seconds: float
    """How long the magic link will be valid for (in seconds) before it expires"""

    view: Literal["manage", "manage-deeplink", "add", "add-deeplink"]
    """Magic Link tab view to load in the connect magic link"""
