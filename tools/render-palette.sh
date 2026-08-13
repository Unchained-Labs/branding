set -eu
cd "$(dirname "$0")/.."
apt-get update -qq >/dev/null 2>&1
apt-get install -y -qq --no-install-recommends librsvg2-bin fonts-dejavu-core >/dev/null 2>&1
rsvg-convert -w 1200 assets/palette/tokens.svg -o assets/palette/tokens.png
ls -la assets/palette/tokens.png
