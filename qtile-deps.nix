{ pkgs }:
with pkgs.python312Packages;
[
  qtile-extras
  dateutils
  python-dotenv
  loguru
  httpx
  yarl
  pydantic
  pydantic-settings
]
