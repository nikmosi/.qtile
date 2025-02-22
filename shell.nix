{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages =
    with pkgs.python312Packages;
    [
      qtile
      python
    ]
    ++ import ./qtile-deps.nix { inherit pkgs; };

  shellHook = ''exec fish'';
}
