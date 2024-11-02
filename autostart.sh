#!/usr/bin/env fish

greenclip daemon &
dunst &
chatterino &
nekoray &
prismatik &; echo (sleep 0.5 && prismatik --on && prismatik --on) &
