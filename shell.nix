{
  pkgs ? import <nixpkgs> { },
}:

with pkgs;

mkShell {

  buildInputs = [
    nano
    git
    # gnumake
    python3
    python3.pkgs.qbittorrent-api
    # python3.pkgs.requests
    # python3.pkgs.aiohttp
    # python3.pkgs.libtorrent-rasterbar
    # python3.pkgs.psutil
    # python3.pkgs.torf
    netselect
  ];
}
