"""Constants for the Bruxelles Propreté waste collection integration."""

DOMAIN = "bxl_proprete"

CONF_STREET = "street"
CONF_NUMBER = "number"
CONF_ZIP = "zip"
CONF_COMMUNE = "commune"

DEFAULT_SCAN_INTERVAL_HOURS = 12

DAY_NAME_TO_WEEKDAY = {
    "lundi": 0,
    "mardi": 1,
    "mercredi": 2,
    "jeudi": 3,
    "vendredi": 4,
    "samedi": 5,
    "dimanche": 6,
}

# Upstream ARP-GAN bug: desc_ramassage day labels are consistently one day
# later than the actual pickup day shown in their own calendar graphic and
# confirmed against real household collection days. SacsVerts (green bag
# dates) is NOT affected — those are plain ISO dates and are correct.
# Subtract this offset from the desc_ramassage weekday to get the true day.
# Set to 0 if a future ARP-GAN fix removes the offset.
DESC_RAMASSAGE_DAY_OFFSET = -1
