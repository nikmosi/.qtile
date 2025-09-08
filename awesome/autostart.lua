local awful = require("awful")

local commands = {
  "chatterino",
  "hyperhdr --desktop",
  "ayugram-desktop",
  "hiddify",
  "firefox",
  "easyeffects",
  "prismatik && sleep 0.5 && prismatik --on && prismatik --on",
}

for _, cmd in ipairs(commands) do
  awful.spawn.once(cmd, {})
end

return {}
