#!/bin/sh
TOKEN="5684e685-a737-496c-86b7-77a65253e6ad"

wakatime_today="$(curl -sf --header "Authorization: Basic $(echo "$TOKEN" | base64)" https://wakatime.com/api/v1/users/current/status_bar/today | jq -r '.data.grand_total.text')"

if [ -n "$wakatime_today" ]; then
    echo " $wakatime_today"
else
    echo ""
fi
