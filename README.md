# .github · GS-Loft-Dev

Profilo pubblico dell'organizzazione **GS-Loft-Dev** su GitHub.

- `profile/README.md`: la pagina che si vede su [github.com/GS-Loft-Dev](https://github.com/GS-Loft-Dev).
- `profile/assets/`: i banner, chiaro e scuro (GitHub mostra quello giusto in base al tema di chi guarda).
- `_sorgente/`: logo GS·LOFT (dal sito [gsloft.it](https://www.gsloft.it)) e lo script che crea i banner.

## Rifare i banner

```bash
python3 _sorgente/make-banner.py
```

Serve Google Chrome. Lo script disegna `_sorgente/banner-light.html` e `banner-dark.html` e li salva come PNG 2560×800 in `profile/assets/`.
Colori del sito: bianco `#F8F8F8`, nero `#0C0C0C`, accento `#EAF0C2`. Carattere: Inter Tight (il sito usa Forma DJR Micro, che non è libero).

> Questo repository deve restare **pubblico**: GitHub mostra il profilo dell'organizzazione solo se `.github` è pubblico. Non metterci dati interni.
