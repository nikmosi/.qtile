#!/usr/bin/env bash

greenclip daemon &
# setxkbmap -option 'grp:alt_shift_toggle' -layout us,ru -option ctrl:nocaps
# for id in $(xinput list | grep "pointer" | cut -d '=' -f 2 | cut -f 1); do xinput --set-prop $id 'libinput Accel Profile Enabled' 0, 1; done
chatterino &
nekoray &
(prismatik && sleep 4 && prismatik --on && prismatik --on) &
