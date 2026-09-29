"""Async API client for ARP-GAN (Bruxelles-Propreté) waste collection calendar."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)

BASE = "https://formsv2.arp-gan.eu"
CALENDAR_PAGE = f"{BASE}/CalendarV5/?Language=EN"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:155.0) Gecko/20100101 Firefox/155.0",
    "Accept": "application/json, text/plain, */*",
    "Origin": BASE,
    "Referer": CALENDAR_PAGE,
}


class BxlPropreteError(Exception):
    """Raised for address validation failures or unexpected API responses."""


class BxlPropreteAPI:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session

    async def get_calendar(
        self, street: str, number: str, zip_code: str, commune: str, lang: str = "EN"
    ) -> dict[str, Any]:
        # Step 1: resolve address to internal id
        try:
            async with self.session.get(
                f"{BASE}/StreetEngine/GetAdress.aspx",
                params={
                    "rue": street,
                    "numero": number,
                    "zip": zip_code,
                    "Lang": lang,
                    "operation": "VALIDATION",
                },
                headers=HEADERS,
            ) as r:
                r.raise_for_status()
                data = await r.json(content_type=None)
        except aiohttp.ClientError as err:
            raise BxlPropreteError(f"Network error during address lookup: {err}") from err

        if not data or data[0].get("Statut") != "OK":
            raise BxlPropreteError(f"Address not recognised by ARP-GAN: {data}")
        address_id = data[0]["Value"]

        # Step 2: fetch calendar via multipart POST (confirmed from browser capture)
        form_data = aiohttp.FormData()
        form_data.add_field("rue", street)
        form_data.add_field("numero", str(number))
        form_data.add_field("zip", str(zip_code))
        form_data.add_field("commune", commune)
        form_data.add_field("id", str(address_id))
        form_data.add_field("Lang", lang)
        form_data.add_field("operation", "VALIDATION")

        try:
            async with self.session.post(
                f"{BASE}/GetCalendarv5/GetCalendarWeb.aspx",
                data=form_data,
                headers=HEADERS,
            ) as r:
                r.raise_for_status()
                res = await r.json(content_type=None)
        except aiohttp.ClientError as err:
            raise BxlPropreteError(f"Network error fetching calendar: {err}") from err

        if not isinstance(res, dict) or "SacsVerts" not in res:
            raise BxlPropreteError(f"Unexpected ARP-GAN response, missing 'SacsVerts': {res}")
        return res
