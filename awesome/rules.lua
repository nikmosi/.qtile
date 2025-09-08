local awful = require("awful")

awful.rules.rules = {
  {
    rule = {},
    properties = {
      focus = awful.client.focus.filter,
      raise = true,
      screen = awful.screen.preferred,
    },
  },
  {
    rule_any = {
      class = {
        "pavucontrol",
        "qbittorrent",
        "float_pass",
        "ripdrag",
        "ssh-askpass",
      },
      name = {
        "branchdialog",
        "pinentry",
      },
    },
    properties = { floating = true },
  },
}

return {}
