# Changelog

## v2.0 (2026-05-20)

### Architecture
- Modular project structure under `src/` with clean separation of concerns
- v1.0 preserved in `project.py` for CS50P submission compliance
- `run.py` as v2.0 entry point

### Themes
- **Vaporwave** (new, replaces Pastel): Neon pink/cyan/purple palette, retro sunset card back, 18 flat-style symbols (statue, palm tree, dolphin, floppy disk, cassette, CRT monitor, etc.)
- **Cyberpunk**: Redesigned card back with symmetrical hexagonal chip and radiating circuit traces; 18 geometric icons (credits, data chip, energy core, hacking, vector blade, firewall, augment, neural AI, toxin, drone, etc.)
- **Nature**: Redesigned card back with symmetrical Tree of Life and ornate vine border; 18 detailed nature illustrations (oak leaf, mushroom, acorn, butterfly, bloom, pine tree, berries, bird, fern, snail, feather, sunflower, ladybug, maple leaf, dragonfly, tulip, owl, rose); forest green UI palette with leaf vein background texture

### Features
- Programmatic sound effects (flip, match, mismatch, victory) generated via `wave`+`math` stdlib, played with `pygame.mixer`
- PIL-generated playing cards with theme-specific back patterns and custom illustrations
- Roman numeral card numbering (I–XVIII)
- Minimal card face border design with index marks
- Exit button during gameplay with confirmation dialog
- Leaderboard system with persistent JSON storage, tracks best scores per theme × difficulty

### Files
- `src/game_logic.py` — Pure game logic functions
- `src/themes.py` — Theme definitions, difficulties, Roman numeral converter
- `src/sound.py` — Sound generation and playback
- `src/card_renderer.py` — PIL-based card image rendering
- `src/symbols/nature.py` — 18 nature illustration functions
- `src/symbols/cyberpunk.py` — 18 cyberpunk icon functions
- `src/symbols/vaporwave.py` — 18 vaporwave symbol functions
- `src/gui/app.py` — Main application class
- `src/gui/menu.py` — Menu frame with leaderboard
- `src/gui/game.py` — Game board frame with exit confirmation
- `src/gui/victory.py` — Victory screen with score recording
- `src/leaderboard.py` — Score persistence
- `run.py` — v2.0 launch script
- `requirements-v2.txt` — Dependencies (customtkinter, pygame, Pillow)

## v1.0 (2026-05-15)

### Initial Release
- Single-file implementation in `project.py` for CS50P final project
- 3 themes (Pastel, Cyberpunk, Nature) with color-switching
- 3 difficulty levels (4×4, 4×6, 6×6)
- Emoji-based card content
- Move counter, timer, scoring system
- 17 pytest tests covering 4 core logic functions
