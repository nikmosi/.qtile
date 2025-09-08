-- AwesomeWM configuration generated from Qtile config
pcall(require, "luarocks.loader")

local gears = require("gears")
local awful = require("awful")
require("awful.autofocus")
local wibox = require("wibox")
local beautiful = require("beautiful")

beautiful.init(require("theme"))

require("keybindings")
require("rules")
require("autostart")

awful.layout.layouts = {
  awful.layout.suit.tile,
  awful.layout.suit.max,
}

local disk_widget = require("widgets.disk")

awful.screen.connect_for_each_screen(function(s)
  awful.tag({ "1", "2", "3", "4", "5", "6", "7", "8", "9" }, s, awful.layout.layouts[1])

  s.mypromptbox = awful.widget.prompt()
  s.mylayoutbox = awful.widget.layoutbox(s)
  s.mylayoutbox:buttons(gears.table.join(
    awful.button({}, 1, function() awful.layout.inc(1) end),
    awful.button({}, 3, function() awful.layout.inc(-1) end)
  ))

  s.mytaglist = awful.widget.taglist {
    screen = s,
    filter = awful.widget.taglist.filter.all,
  }

  s.mytasklist = awful.widget.tasklist {
    screen = s,
    filter = awful.widget.tasklist.filter.currenttags,
  }

  s.mywibox = awful.wibar { position = "top", screen = s }

  s.mywibox:setup {
    layout = wibox.layout.align.horizontal,
    { layout = wibox.layout.fixed.horizontal, s.mytaglist, s.mypromptbox },
    s.mytasklist,
    { layout = wibox.layout.fixed.horizontal, disk_widget(), wibox.widget.textclock() },
  }
end)

return {}
