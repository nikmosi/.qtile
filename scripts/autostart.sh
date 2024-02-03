#!/usr/bin/env bash

wired &
greenclip daemon &
setxkbmap -layout us,ru
for id in $(xinput list | grep "pointer" | cut -d '=' -f 2 | cut -f 1); do xinput --set-prop $id 'libinput Accel Profile Enabled' 0, 1; done
chatterino &
