# vc-screenscribe — Ścieżka repo / debug i przykłady

## Ścieżka repo / debug

Kanoniczne repo upstream:

- [vetcoders/Screenscribe](https://github.com/vetcoders/Screenscribe)

Gdy potrzebna jest praca z repo, preferuj bieżący checkout screenscribe, jeśli użytkownik
już go otworzył. Nie zakładaj stałej lokalnej ścieżki. Jeśli żaden checkout nie jest
otwarty, odwołaj się do domyślnego repo powyżej i wspomnij o lokalnej ścieżce dopiero, gdy
faktycznie jest znana.

Wejdź do repo tylko wtedy, gdy:

- brakuje CLI lub jest zepsute
- potrzebny jest debug providera/configu/runtime'u
- użytkownik chce pracy nad samym screenscribe

Wtedy preferuj:

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe review /absolute/path/to/video.mov
```

### Review

Pojedyncze wideo:

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe review /absolute/path/to/video.mov
```

Batch:

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe review /path/video1.mov /path/video2.mov -o /absolute/output/dir
```

Przydatne flagi:

- `--keywords-only`
- `--estimate`
- `--dry-run`
- `--no-vision`
- `--resume`
- `--lang en`
- `-o /path/output`

### Preprocess

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe preprocess /absolute/path/to/video.mov
```

Przydatne flagi:

- `--no-audio`
- `--force`
- `--lang en`
- `-o /path/output`

### Transcribe

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe transcribe /absolute/path/to/video.mov -o /absolute/path/to/transcript.txt
```

### Interaktywny serwer Analyze

Preferowane:

```bash
cd /path/to/Screenscribe
make analyze VIDEO=/absolute/path/to/video.mov PORT=8766
```

### Bezpieczne komendy triażu

Używaj ich tylko, jeśli normalna ścieżka `screenscribe review ...` lub `screenscribe preprocess ...` zawiodła:

```bash
screenscribe review --help
screenscribe preprocess --help
screenscribe version
ffmpeg -version
test -f ~/.config/screenscribe/config.env && echo CONFIG_OK || echo CONFIG_MISSING
```

## Przykłady

**Przykład 1**
Wejście: „Przeleć mi ten review.mov i wypluj JSON + markdown z bugami."
Działanie: uruchom `screenscribe review /absolute/path/to/review.mov`, zwróć katalog wyjściowy i kluczowe findingi.

**Przykład 2**
Wejście: „Mam video, ale chcę tylko transcript, timestampy i pack dla agenta."
Działanie: uruchom `screenscribe preprocess /absolute/path/to/video.mov`, zwróć katalog bundle'a i listę artefaktów.

**Przykład 3**
Wejście: „W repo https://github.com/vetcoders/Screenscribe coś popsuliśmy w HTML Pro."
Działanie: potraktuj to jako pracę z repo, użyj natywnych komend repo i bramek jakości, a nie zwykłego przebiegu review.
