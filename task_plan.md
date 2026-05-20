# Vaporwave Theme — Task Plan

## Goal
Replace "Pastel" theme with "Vaporwave" (蒸汽波) theme in Memory Match v2.0.

## Phases

### Phase 1: Theme Config
- [ ] Update THEMES dict: rename "Pastel" → "Vaporwave", neon colors (pink/cyan/purple/blue)
- [ ] Update DIFFICULTIES if needed

### Phase 2: Card Back
- [ ] Sunset gradient + palm silhouette + grid floor on card back
- [ ] Pattern name: "vaporwave"

### Phase 3: Card Face Symbols (18 icons)
- [ ] Greek statue bust, Palm tree, Dolphin, Floppy disk
- [ ] Sunset circle, Grid floor, Geometric mountain, Crystal/gem
- [ ] Cassette tape, Neon triangle, Cherry blossom, Synthwave
- [ ] Lightning bolt, CRT monitor, Yin-yang, Retro phone
- [ ] Diamond, Star

### Phase 4: UI
- [ ] Title font: retro computer style (try PixelifySans or similar from canvas-fonts)
- [ ] Neon glow effect on title

### Phase 5: Integration
- [ ] Update card_renderer.py for vaporwave card back pattern
- [ ] Update symbols/__init__.py to include vaporwave
- [ ] Run tests, verify rendering
