# Bruxelles Propreté — Home Assistant integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Home Assistant custom integration for the [ARP-GAN / Bruxelles-Propreté](https://www.arp-gan.be) waste collection calendar, for Brussels-Capital communes served by that backend (Forest/Vorst, Ixelles, Molenbeek, etc.).

## Entities

| Entity | Description |
|---|---|
| `sensor.next_green_bag_collection` | Date of the next garden-waste (sacs verts / groene zakken) pickup |
| `sensor.next_bag_collection` | Date of the next recurring blue/yellow/white bag pickup |

Both sensors expose these attributes:

| Attribute | Description |
|---|---|
| `days_until` | Days until the collection (integer) |
| `human_readable` | "today", "tomorrow" or "in N days" |
| `put_out_date` | Day the bags go out: the evening before for weekly bags (18:00–24:00), the same morning for green bags (05:00–12:00) |
| `bag_colors` | Bag colours for that collection, e.g. `["YELLOW", "WHITE"]` |

`sensor.next_bag_collection` also has `description` and the full `weekly_schedule`; `sensor.next_green_bag_collection` has the `upcoming_dates` list.

## Installation via HACS

1. HACS → ⋮ → **Custom repositories** → add `https://github.com/danito/hacs-bxl-proprete`, category **Integration**.
2. Install **Bruxelles Propreté**, restart Home Assistant.
3. **Settings → Devices & Services → Add Integration** → search **Bruxelles Propreté**.
4. Enter your street name (no number), house number, postal code, and commune.

## Manual installation

Copy `custom_components/bxl_proprete/` into `<config>/custom_components/` and restart Home Assistant.

## Notes

### Collection day vs. put-out day

The ARP-GAN API's `desc_ramassage` field (the per-weekday text schedule) is keyed by **collection** day, and its text tells you to put the bags out the evening before: `"jeudi": "Thursday, Put out your bags YELLOW,WHITE between 6 pm and 12 pm"` means out on Wednesday 18:00–24:00, collected Thursday. ARP-GAN's calendar graphic shows the **put-out** day (Wednesday), which is why it looks one day earlier than the text.

Up to 1.1.1 this integration shifted the weekly schedule one day earlier, so `sensor.next_bag_collection` actually gave the put-out day. Since 1.2.0 its state is the collection day and the put-out day is in the `put_out_date` attribute.

The `SacsVerts` green-bag dates are collection days; according to the calendar graphic green bags go out the same morning (05:00–12:00), so their `put_out_date` is the same day.

Orange (food waste) bags appear on the calendar graphic but not in `desc_ramassage`, so this integration does not report them.

### The `img_ramassage` field

The API also returns an `img_ramassage` URL (a JPG/PDF). This integration ignores it — it's an image, not structured data. The `desc_ramassage` text and `SacsVerts` dates are used instead.
