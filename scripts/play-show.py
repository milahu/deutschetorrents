#!/usr/bin/env python3

"""
spiele eine episode einer "serie" (TV show)
mit dem "mpv" video player

damit das skript deine downloads findet:
ändere diese variablen:
- downloads_muster_liste

beispiel: south park
damit das skript andere serien spielt:
kopiere das skript zu "play-deine-serie.py"
ändere diese variablen:
- video_muster_liste
- audio_muster_liste

wenn video_muster oder audio_muster mehrere dateien findet
dann nimmt das skript die erste datei
"""



import sys, os, re, glob, shlex, subprocess



# argumente
s = int(sys.argv[1]) # season
e = int(sys.argv[2]) # episode

s0 = f"S{s:02d}" # S01
e0 = f"E{e:02d}" # E02
se0 = s0 + e0 # S01E02



# einstellungen:



# download ordner
# "~" ist dein "home" ordner, zum beispiel "/home/user" unter linux
# "/run/media/$USER/*" sind externe festplatten unter linux
downloads_muster_liste = [
    "~/Downloads",
    "~/Downloads/torrent",
    "~/Downloads/pyLoad",
    "~/torrent",
    "~/pyload",
    "~/down/torrent/done",
    "/run/media/$USER/*/torrent",
    "/run/media/$USER/*/pyload",
    # TODO hier deine download ordner
    # ...
]



# TODO hier deine muster zu dateipfaden

# video_muster ist relativ zu downloads_muster
video_muster_liste = [
    f"South.Park.Uncensored.S01-S21.720p.BluRay.x265-HETeam/{s0}/South.Park.{se0}.720p.BluRay.x265-HETeam.mkv",
]

# audio_muster ist relativ zu downloads_muster
audio_muster_liste = [
    f"South.Park.{s0}.German.*/*.{se0}.*",
]

# untertitel_muster ist relativ zum ordner von audio_pfad
untertitel_muster_liste = [
    f"*.{se0}.*",
]



video_endung_liste = ["mkv", "mp4", "avi"]

audio_endung_liste = ["mka", "m4a", "aac", "ac3", "mp3", "wav", "ogg", "opus", "dts", "flac"]
audio_endung_liste += video_endung_liste # nutze auch tonspuren in video-dateien

untertitel_endung_liste = ["srt"]



# :einstellungen



def pfad_von_muster(muster_liste):
    for muster in muster_liste:
        muster = os.path.expandvars(muster) # expand $USER
        muster = os.path.expanduser(muster) # expand ~
        for pfad in glob.glob(muster): # expand *
            yield pfad

downloads_pfad_liste = list(pfad_von_muster(downloads_muster_liste))

if len(downloads_pfad_liste) == 0:
    print("fehler: keine downloads ordner")
    sys.exit(1)

if 0:
    print("downloads_pfad_liste:")
    for downloads_pfad in downloads_pfad_liste:
        print(f"  {downloads_pfad}")

r"""
# https://stackoverflow.com/a/31142692/10440128
# a breadth-first search would be more efficient:
# split the pattern by slashes, call os.listdir on each level,
# and only descend when the dirname matches.
# then the glob pattern ** would allow recursive descending to find the next path segment.
# im pretty sure this already exists somewhere...
import fnmatch
def findfiles(dir, pattern):
    #patternregex = fnmatch.translate(pattern)
    patternregex = re.compile(pattern)
    for root, dirs, files in os.walk(dir):
        for basename in files:
            filename = os.path.join(root, basename)
            if re.search(patternregex, filename, re.IGNORECASE):
                yield filename
"""

r"""
# https://stackoverflow.com/a/56619011/10440128
def walk_with_suffixes(target, extensions):
    results = []
    for r, d, f in os.walk(target):
        for ff in f:
            for e in extensions:
                if ff.endswith(e):
                    yield os.path.join(r, ff)
                    break
"""

def finde_datei_pfad(downloads_pfad_liste, datei_muster_liste, datei_endung_liste, mehrere=False, muss_finden=True):
    liste = list(finde_datei_pfad_innen(downloads_pfad_liste, datei_muster_liste, datei_endung_liste, mehrere, muss_finden))
    if mehrere:
        return liste
    else:
        return liste[0]

def finde_datei_pfad_innen(downloads_pfad_liste, datei_muster_liste, datei_endung_liste, mehrere=False, muss_finden=True):
    for downloads_pfad in downloads_pfad_liste:
        #print(f"downloads_pfad: {downloads_pfad}")
        for datei_muster in datei_muster_liste:
            datei_muster = os.path.join(downloads_pfad, datei_muster)
            #print(f"datei_muster: {datei_muster}")
            #for datei_pfad in pfad_von_muster(datei_muster):
            for datei_pfad in glob.glob(datei_muster):
                #print(f"datei_pfad: {datei_pfad}")
                #return datei_pfad
                # python glob kann keine brace expansion a la "*.{mkv,mp4,avi}"
                # https://stackoverflow.com/questions/22996645/brace-expansion-in-python-glob
                # alternative: regex muster für den ganzen dateipfad -> "def findfiles"
                datei_pfad_lower = datei_pfad.lower()
                for datei_endung in datei_endung_liste:
                    if datei_pfad_lower.endswith("." + datei_endung):
                        yield datei_pfad
                        if not mehrere: return # stop generator
    if muss_finden:
        print(f"fehler: datei nicht gefunden: {datei_muster_liste} .{{{','.join(datei_endung_liste)}}}")
        sys.exit(1)

video_pfad = finde_datei_pfad(downloads_pfad_liste, video_muster_liste, video_endung_liste)
print(f"video_pfad: {video_pfad}")

# TODO mehrere audio dateien?
audio_pfad = finde_datei_pfad(downloads_pfad_liste, audio_muster_liste, audio_endung_liste)
print(f"audio_pfad: {audio_pfad}")

# untertitel_muster ist relativ zum ordner von audio_pfad
untertitel_pfad_liste = [os.path.dirname(audio_pfad)]
untertitel_pfad_liste = finde_datei_pfad(untertitel_pfad_liste, untertitel_muster_liste, untertitel_endung_liste, True, False)
print(f"untertitel_pfad_liste: {untertitel_pfad_liste}")

# TODO audio-video sync
# nutze die sync/*.mkv datei neben der audio datei
# zum synchronisieren mit dem video
# kann mpv dynamisches audio-delay?
# wahrscheinlich nicht, dann müssen wir die tonspur schneiden
# und eine temporäre audio datei erzeugen

# TODO mpv audio-speed-correction

args = [
    "mpv",
    video_pfad,
    "--audio-file=" + audio_pfad,
]

for untertitel_pfad in untertitel_pfad_liste:
    args.append("--sub-file=" + untertitel_pfad)

print(">", shlex.join(args))
# not working. wtf?!
#os.execlp(*args)
#os.execvp(args[0], args[1:])
subprocess.run(args)
