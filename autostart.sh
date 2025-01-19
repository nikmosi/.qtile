#!/usr/bin/env fish

chatterino &
nekoray &
prismatik &; echo (sleep 0.5 && prismatik --on && prismatik --on) &
