{
  description = "An example project.";

  inputs.pre-commit-hooks.url = "github:cachix/git-hooks.nix";

  outputs =
    { self, nixpkgs, ... }@inputs:
    let
      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;

    in
    {
      checks = forAllSystems (system: {
        pre-commit-check = inputs.pre-commit-hooks.lib.${system}.run {
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
      });

      devShells = forAllSystems (
        system:
        let
          pkgs = import nixpkgs {
            system = system;
          };
        in
        {
          default = nixpkgs.legacyPackages.${system}.mkShell {
            packages =
              with pkgs;
              with python312Packages;
              [ qtile ]
              ++ import ./qtile-deps.nix {
                inherit pkgs;
              };
            buildInputs = self.checks.${system}.pre-commit-check.enabledPackages;
            shellHook = ''
              ${self.checks.${system}.pre-commit-check.shellHook}
              exec fish
            '';
          };
        }
      );
    };
}
