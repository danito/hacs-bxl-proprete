import aiohttp

BASE = "https://formsv2.arp-gan.eu"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:155.0)",
    "Accept": "application/json, text/plain, */*",
    "Origin": BASE,
    "Referer": f"{BASE}/CalendarV5/?Language=EN",
}

class BxlPropreteAPI:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_calendar(self, street, number, zip_code, commune, lang="EN"):
        async with self.session.get(
            f"{BASE}/StreetEngine/GetAdress.aspx",
            params={"rue": street, "numero": number, "zip": zip_code, "Lang": lang, "operation": "VALIDATION"},
            headers=HEADERS,
        ) as r:
            data = await r.json()
            if not data or data[0].get("Statut") != "OK":
                raise ValueError("Address not recognized")
            address_id = data[0]["Value"]

        form_data = aiohttp.FormData()
        form_data.add_field("rue", street)
        form_data.add_field("numero", str(number))
        form_data.add_field("zip", str(zip_code))
        form_data.add_field("commune", commune)
        form_data.add_field("id", str(address_id))
        form_data.add_field("Lang", lang)
        form_data.add_field("operation", "VALIDATION")

        async with self.session.post(
            f"{BASE}/GetCalendarv5/GetCalendarWeb.aspx",
            data=form_data,
            headers=HEADERS,
        ) as r:
            res = await r.json()
            if "SacsVerts" not in res:
                raise ValueError("Unexpected response")
            return res