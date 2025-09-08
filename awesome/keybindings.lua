local gears = require("gears")
local awful = require("awful")

local mod = "Mod4"
local terminal = "kitty"

local globalkeys = gears.table.join(
  awful.key({ mod }, "Return", function() awful.spawn(terminal) end,
    { description = "open a terminal", group = "launcher" }),
  awful.key({ mod }, "h", function() awful.client.focus.bydirection("left") end,
    { description = "focus left", group = "client" }),
  awful.key({ mod }, "l", function() awful.client.focus.bydirection("right") end,
    { description = "focus right", group = "client" }),
  awful.key({ mod }, "j", function() awful.client.focus.bydirection("down") end,
    { description = "focus down", group = "client" }),
  awful.key({ mod }, "k", function() awful.client.focus.bydirection("up") end,
    { description = "focus up", group = "client" }),
  awful.key({ mod, "Shift" }, "r", awesome.restart,
    { description = "reload awesome", group = "awesome" }),
  awful.key({ mod, "Shift" }, "q", awesome.quit,
    { description = "quit awesome", group = "awesome" })
)

root.keys(globalkeys)

return {}
