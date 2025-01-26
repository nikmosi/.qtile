#!/usr/bin/env bash

chatterino &
ayugram-desktop &
nekoray &
tmux start-server &
prismatik &; echo (sleep 0.5 && prismatik --on && prismatik --on) &
