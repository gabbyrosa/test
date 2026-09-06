#!/usr/bin/env bash
# Download the Swiss Ephemeris data files needed by the natal calculator.
# Covers 1800-2399 for the main planets, Moon, and asteroids (incl. Chiron).
set -euo pipefail

DEST="${1:-/usr/share/swisseph}"
BASE="https://raw.githubusercontent.com/aloistr/swisseph/master/ephe"

mkdir -p "$DEST"
for f in sepl_18.se1 semo_18.se1 seas_18.se1; do
  echo "Fetching $f ..."
  curl -sSL -o "$DEST/$f" "$BASE/$f"
done
echo "Swiss Ephemeris files installed in $DEST"

# Fixed-star catalogue (needed for swe.fixstar_ut)
curl -sSL -o /usr/share/swisseph/sefstars.txt \
  https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sefstars.txt
