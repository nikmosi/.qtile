local awful = require("awful")

local function watch(cmd, timeout, widget, callback)
  awful.widget.watch(cmd, timeout, function(w, stdout)
    callback(w, stdout)
  end, widget)
  return widget
end

return watch
