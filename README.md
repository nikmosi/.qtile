# Awesome WM migration

This repository contains an Awesome WM configuration generated from an existing
Qtile setup.  The configuration is intended to be used on NixOS via flakes and
Home Manager.

## Installation

```sh
nix flake check    # optional, runs linters
home-manager switch --flake .#your-username
```

## Widget mapping

| Qtile widget | Awesome equivalent |
|--------------|-------------------|
| `CurrentLayoutIcon` | `awful.widget.layoutbox` |
| `GroupBox` | `awful.widget.taglist` |
| `Prompt` | `awful.widget.prompt` |
| `WindowName` | `awful.widget.tasklist` |
| `Chord` | _not implemented_ |
| `cSysTray` | `wibox.widget.systray` |
| `Wireguard` | `awesome-wireguard` (CLI script) |
| `CheckUpdates` | `awesome-updates` (CLI script) |
| `WakaTime` | `awesome-wakatime` (CLI script) |
| `OpenWeatherMap` | `awesome-weather` (CLI script) |
| `InfoAirQualitiIndex` | `awesome-airquality` (CLI script) |
| `Memory` | `awesome-memory` (CLI script) |
| `CDF` | `awesome-disk` (CLI script) |
| `PulseVolume` | `awesome-volume` (CLI script) |
| `NextFormatsClock` | `wibox.widget.textclock` |
| `KblEmoji` | `wibox.widget.keyboardlayout` |

## Keybindings

| Keys | Action |
|------|--------|
| `Mod4+Return` | Launch terminal |
| `Mod4+h/j/k/l` | Focus clients |
| `Mod4+Shift+r` | Reload Awesome |
| `Mod4+Shift+q` | Quit Awesome |

## Troubleshooting

Run `awesome --replace` from a TTY to check for errors.

## Migration report

The bar layout, basic keybindings and disk widget are implemented.  Other
Qtile-specific widgets are represented by placeholders that expect external
CLI scripts.
