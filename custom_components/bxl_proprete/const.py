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

# desc_ramassage is keyed by collection day; its text says to put the bags out
# the evening before (e.g. "jeudi": "Thursday, Put out your bags YELLOW,WHITE
# between 6 pm and 12 pm" -> out Wednesday 18:00-24:00, collected Thursday).
# ARP-GAN's calendar graphic shows the put-out day, which is why it looks one
# day earlier than the desc_ramassage labels.
WEEKLY_PUT_OUT_DAYS_BEFORE = 1

# SacsVerts dates are collection days too, but the calendar graphic shows green
# bags go out the same morning (05:00-12:00).
GREEN_PUT_OUT_DAYS_BEFORE = 0

# Bag colour words in desc_ramassage, normalised to English
BAG_COLORS = {
    "BLUE": "BLUE", "BLEU": "BLUE", "BLAUW": "BLUE",
    "WHITE": "WHITE", "BLANC": "WHITE", "WIT": "WHITE",
    "YELLOW": "YELLOW", "JAUNE": "YELLOW", "GEEL": "YELLOW",
    "ORANGE": "ORANGE", "ORANJE": "ORANGE",
    "GREEN": "GREEN", "VERT": "GREEN", "GROEN": "GREEN",
}
