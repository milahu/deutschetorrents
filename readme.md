# deutschetorrents

deutsche torrents sind tot... es lebe deutschetorrents

meine mudder is so alt, die kennt noch
[torrent.to](https://www.handelszeitung.ch/unternehmen/torrentto-betreiber-wandert-hinter-gitter)

ernsthaft: die deutsche torrent szene ist sowas von im arsch

zu viele menschen haben angst vor "abmahnungen"...  
aber diese angst ist falsch, siehe [abmahnungen.txt](abmahnungen.txt)

unsere welt geht eeh unter, also lass uns noch paar filme schaun, und uns schlau fühlen...

wer trotzdem immer noch angst hat,
der kann [torrent über I2P](https://geti2p.net/en/docs/applications/bittorrent) machen,  
immer noch besser als geld zahlen für rapidgator.net oder VPN



## torrents

- [magnets.txt](magnets.txt)
- [magnets.rss](magnets.rss)



## mirrors

github löscht repos bei DMCA takedown requests, deswegen mirrors im darknet

und im darknet braucht man keine email zum registrieren

- [github.com](https://github.com/milahu/deutschetorrents)
- [darktea.onion](http://it7otdanqu7ktntxzm427cba6i53w6wlanlh23v5i3siqmos47pzhvyd.onion/milahu/deutschetorrents)
- [righttoprivacy.onion](http://gg6zxtreajiijztyy5g6bt5o6l3qu32nrg7eulyemlhxwwl6enk6ghad.onion/milahu/deutschetorrents)



### git clone

```sh
# github.com
git clone https://github.com/milahu/deutschetorrents

# darktea.onion
git -c remote.origin.proxy=socks5h://127.0.0.1:9050 clone \
  http://it7otdanqu7ktntxzm427cba6i53w6wlanlh23v5i3siqmos47pzhvyd.onion/milahu/deutschetorrents
cd deutschetorrents
git config --add remote.origin.proxy socks5h://127.0.0.1:9050

# righttoprivacy.onion
git -c remote.origin.proxy=socks5h://127.0.0.1:9050 clone \
  http://gg6zxtreajiijztyy5g6bt5o6l3qu32nrg7eulyemlhxwwl6enk6ghad.onion/milahu/deutschetorrents
cd deutschetorrents
git config --add remote.origin.proxy socks5h://127.0.0.1:9050
```



### git remote add

```
git remote add github.com https://github.com/milahu/deutschetorrents

git remote add darktea.onion \
  http://it7otdanqu7ktntxzm427cba6i53w6wlanlh23v5i3siqmos47pzhvyd.onion/milahu/deutschetorrents
git config --add remote.darktea.onion.proxy socks5h://127.0.0.1:9050

git remote add righttoprivacy.onion \
  http://gg6zxtreajiijztyy5g6bt5o6l3qu32nrg7eulyemlhxwwl6enk6ghad.onion/milahu/deutschetorrents
git config --add remote.righttoprivacy.onion.proxy socks5h://127.0.0.1:9050
```



### tor hidden services

verbindungen zu `.onion` domains erfordern einen laufenden tor client,
der einen socks5 proxy auf `127.0.0.1:9050` anbietet

normalerweise als system-weiter tor service,
gestartet mit `sudo systemctl start tor` auf linux,
oder `tor.exe --service start` auf windows

siehe auch

- https://www.torproject.org/
- https://community.torproject.org/onion-services/setup/install/
- https://askubuntu.com/questions/6522/how-to-install-tor



## archiv

- [archive.org](https://web.archive.org/web/*/https://github.com/milahu/deutschetorrents)
- [archive.is](https://archive.is/2u9Gb)
