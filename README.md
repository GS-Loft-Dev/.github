# .github · GS-Loft-Dev

Profilo pubblico dell'organizzazione **GS-Loft-Dev** su GitHub.

- `profile/README.md`: la pagina che si vede su [github.com/GS-Loft-Dev](https://github.com/GS-Loft-Dev).
- `profile/assets/`: le immagini animate (banner, metodo, flusso dei dati), chiare e scure: GitHub mostra quelle giuste in base al tema di chi guarda. Restano anche i banner PNG statici.
- `_sorgente/`: logo GS·LOFT (dal sito [gsloft.it](https://www.gsloft.it)) e lo script che crea i banner.

## Aggiornamento automatico

La GitHub Action `aggiorna profilo` (`.github/workflows/aggiorna-profilo.yml`) gira ogni ora, a mano da *Actions › aggiorna profilo › Run workflow*, e quando cambia qualcosa in `_sorgente/`. Esegue `_sorgente/aggiorna.py`, che:

- legge tutti i repository dell'organizzazione;
- rifà la tabella dei progetti nel README, tra `<!-- progetti:inizio -->` e `<!-- progetti:fine -->`;
- rifà banner, schema `( dev )` e *Ultimi aggiornamenti* con i dati veri;
- salva solo se è cambiato qualcosa.

Un repository nuovo compare da solo. Il gruppo viene dai suoi topic (`dashboard`, `automazioni`, `ai`, `strumenti`, `dati`, `web`) e il testo dalla descrizione su GitHub. Per scegliere gruppo e testo a mano, o per nasconderlo, si modifica `_sorgente/progetti.json` (oppure si dà al repository il topic `nascondi`). Nel profilo pubblico finiscono solo nome, gruppo, testo e data: mai commit o contenuti dei repository privati.

**Serve il segreto `ORG_READ_TOKEN`**: un token *fine-grained* con proprietario GS-Loft-Dev, accesso a *All repositories* e il solo permesso *Metadata: read*. Senza, lo script si ferma invece di togliere i privati dalla tabella.

Per aggiornare subito dopo un push in un altro repository, quel repository può inviare un `repository_dispatch` di tipo `aggiorna-profilo` a `GS-Loft-Dev/.github`.

Per provarlo in locale: `GH_TOKEN=$(gh auth token) python3 _sorgente/aggiorna.py`.

## Rifare le immagini animate

```bash
python3 _sorgente/make-anim.py
```

Crea `banner`, `metodo` e `dev` in SVG, chiari e scuri, in `profile/assets/`. Sono animati solo con SMIL e CSS, perché GitHub non esegue script nelle immagini. Il testo usa Inter Tight se è installato, altrimenti il sans-serif di sistema.

## Rifare i banner PNG

```bash
python3 _sorgente/make-banner.py
```

Serve Google Chrome. Lo script disegna `_sorgente/banner-light.html` e `banner-dark.html` e li salva come PNG 2560×800 in `profile/assets/`.
Colori del sito: bianco `#F8F8F8`, nero `#0C0C0C`, accento `#EAF0C2`. Carattere: Inter Tight (il sito usa Forma DJR Micro, che non è libero).

> Questo repository deve restare **pubblico**: GitHub mostra il profilo dell'organizzazione solo se `.github` è pubblico. Non metterci dati interni.
