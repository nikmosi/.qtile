{
  description = "An example project.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    pre-commit-hooks.url = "github:cachix/git-hooks.nix";
    flake-utils.url = "github:numtide/flake-utils";
    home-manager.url = "github:nix-community/home-manager";
  };

  outputs =
    {
      self,
      nixpkgs,
      pre-commit-hooks,
      flake-utils,
      home-manager,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (system: {
      checks = {
        pre-commit-check = pre-commit-hooks.lib.${system}.run {
          src = ./.;
          hooks = {
            isort.enable = true;
            ruff.enable = true;
            ruff-format.enable = true;
            end-of-file-fixer.enable = true;
            check-added-large-files.enable = true;
            trim-trailing-whitespace.enable = true;
            check-yaml.enable = true;
            fix-byte-order-marker.enable = true;
            trufflehog = {
              enable = true;
              stages = [ "pre-push" ];
            };
          };
        };
      };

      devShells =
        let
          pkgs = import nixpkgs { inherit system; };
          qtileDeps = import ./qtile-deps.nix { inherit pkgs; };
        in
        {
          default = pkgs.mkShell {
            name = "qtile";
            packages = [
              pkgs.python312Packages.qtile
            ] ++ qtileDeps;

            buildInputs = self.checks.${system}.pre-commit-check.enabledPackages;

            shellHook = ''
              ${self.checks.${system}.pre-commit-check.shellHook}
              exec nu
            '';
          };
        };
    }) // {
      homeManagerModules = {
        awesome = import ./homeManagerModule.nix;
      };
    };
}
