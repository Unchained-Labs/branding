# Regenerates assets/logo/png. Invoked by `make png`.
# The SVGs are the source of truth; everything under assets/logo/png is generated.
set -eu
cd "$(dirname "$0")/.."
apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq --no-install-recommends librsvg2-bin >/dev/null 2>&1
out=assets/logo/png; mkdir -p "$out"

# Square marks. 16 is the documented minimum; 512 covers a store/social tile.
for src in mark-accent mark-dark mark-paper favicon; do
  for size in 16 32 48 64 128 180 256 512 1024; do
    rsvg-convert -w "$size" -h "$size" "assets/logo/$src.svg" -o "$out/$src-${size}.png"
  done
done

# Lockups scale by HEIGHT so the aspect ratio is never guessed.
for src in lockup-horizontal lockup-horizontal-dark lockup-stacked lockup-stacked-dark; do
  for h in 32 64 128 256 512; do
    rsvg-convert -h "$h" "assets/logo/$src.svg" -o "$out/$src-h${h}.png"
  done
done

# mark-mono is currentColor. A PNG cannot inherit anything, so rendering it
# as-is silently produces black and half the reason mono exists disappears.
# Emit BOTH inks explicitly instead, named so the choice is visible.
for ink in black white; do
  sed "s/currentColor/$ink/g" assets/logo/mark-mono.svg > /tmp/mono-$ink.svg
  for size in 16 32 64 128 256 512; do
    rsvg-convert -w "$size" -h "$size" /tmp/mono-$ink.svg -o "$out/mark-mono-$ink-${size}.png"
  done
done
ls -1 "$out" | wc -l
