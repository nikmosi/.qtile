{ config, pkgs, ... }:
{
  home.file.".local/bin/awesome-disk" = {
    source = ./scripts/awesome-disk;
    executable = true;
  };

  xdg.configFile."awesome".source = ./awesome;
}
