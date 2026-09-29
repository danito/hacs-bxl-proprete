# Bruxelles Propreté — Home Assistant integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Home Assistant custom integration for the [ARP-GAN / Bruxelles-Propreté](https://www.arp-gan.be) waste collection calendar, for Brussels-Capital communes served by that backend (Forest/Vorst, Ixelles, Molenbeek, etc.).

## Entities

| Entity | Description |
|---|---|
| `sensor.next_green_bag_collection` | Date of the next garden-waste (sacs verts / groene zakken) pickup |
| `sensor.next_bag_collection` | Date of the next recurring blue/yellow/white/orange bag pickup |

Both sensors expose `days_until` (integer) and `human_readable` ("today", "tomorrow", "in N days") attributes, as well as upcoming date lists and the full weekly schedule.

## Installation via HACS

1. HACS → ⋮ → **Custom repositories** → add `https://github.com/danito/hacs-bxl-proprete`, category **Integration**.
2. Install **Bruxelles Propreté**, restart Home Assistant.
3. **Settings → Devices & Services → Add Integration** → search **Bruxelles Propreté**.
4. Enter your street name (no number), house number, postal code, and commune.

## Manual installation

Copy `custom_components/bxl_proprete/` into `<config>/custom_components/` and restart Home Assistant.

## Notes

### desc_ramassage day offset

The ARP-GAN API's `desc_ramassage` field (the per-weekday text schedule) has a confirmed upstream bug: its day labels are consistently **one day later** than the actual pickup day shown in ARP-GAN's own calendar graphic and verified against real household collection days. The `SacsVerts` green-bag dates are **not** affected. This integration corrects for this with `DESC_RAMASSAGE_DAY_OFFSET = -1` in `const.py`.

### The `img_ramassage` field

The API also returns an `img_ramassage` URL (a JPG/PDF). This integration ignores it — it's an image, not structured data. The `desc_ramassage` text (with the offset correction applied) and `SacsVerts` dates are used instead.
