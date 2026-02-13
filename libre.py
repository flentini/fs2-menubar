"""Thin wrapper around pylibrelinkup for fetching glucose readings."""

from dataclasses import dataclass
from datetime import datetime

from pylibrelinkup import PyLibreLinkUp
from pylibrelinkup.exceptions import RedirectError


@dataclass
class GlucoseReading:
    value: int
    trend_arrow: str
    timestamp: datetime
    is_high: bool
    is_low: bool


def create_client(email: str, password: str) -> PyLibreLinkUp:
    """Authenticate with LibreLinkUp, handling region redirects."""
    client = PyLibreLinkUp(email=email, password=password)
    try:
        client.authenticate()
    except RedirectError as e:
        client = PyLibreLinkUp(email=email, password=password, api_url=e.region)
        client.authenticate()
    return client


def fetch_latest(client: PyLibreLinkUp) -> GlucoseReading:
    """Fetch the most recent glucose reading for the first linked patient."""
    patients = client.get_patients()
    if not patients:
        raise RuntimeError("No patients found in LibreLinkUp account")

    latest = client.latest(patient_identifier=patients[0])

    return GlucoseReading(
        value=int(latest.value),
        trend_arrow=latest.trend.indicator,
        timestamp=latest.timestamp,
        is_high=latest.is_high,
        is_low=latest.is_low,
    )
