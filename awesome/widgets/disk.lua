local wibox = require("wibox")
local watch = require("lib.watch")

return function()
  local widget = wibox.widget.textbox()
  watch("awesome-disk --once", 60, widget, function(w, stdout)
    local pct = stdout:match('"percent":%s*(%d+)') or "0"
    w.text = string.format(" %s%%", pct)
  end)
  return widget
end
