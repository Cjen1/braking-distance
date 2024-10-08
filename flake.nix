{
  description = "Basic python flake";

  inputs = { 
    flake-utils.url = "github:numtide/flake-utils"; 
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, flake-utils, nixpkgs }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3.withPackages (pypkgs: [
            pypkgs.numpy
            pypkgs.scipy
            pypkgs.sympy
            pypkgs.seaborn
            pypkgs.pandas
          ]);
      in {
        packages = { };
        devShell = pkgs.mkShell {
          inputsFrom = [ ];
          buildInputs = [ python ];
        };
      });
}
