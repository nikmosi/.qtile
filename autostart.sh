#!/usr/bin/env bash

chatterino &
nekoray &
prismatik &; echo (sleep 0.5 && prismatik --on && prismatik --on) &
tmux start-server &
