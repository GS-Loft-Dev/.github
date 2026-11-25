# Aggiorna il profilo dell'organizzazione con i repository veri di GS-Loft-Dev.
# Uso: GH_TOKEN=... python3 _sorgente/aggiorna.py
#
# 1. legge da GitHub tutti i repository dell'organizzazione (servono i permessi per vedere anche i privati)
# 2. li unisce a _sorgente/progetti.json (gruppo e testo scelti a mano; i nuovi entrano da soli)
# 3. riscrive la tabella dei progetti nel README, tra i segnaposto <!-- progetti:inizio --> e <!-- progetti:fine -->
# 4. salva _sorgente/dati.json e rifà le immagini animate (make-anim.py), che leggono quei dati
#
# Nel profilo pubblico finiscono solo nome, gruppo, testo e data dell'ultimo aggiornamento:
# mai messaggi dei commit o contenuto dei repository privati.
import datetime, json, os, pathlib, re, subprocess, sys, urllib.request

ORG = "GS-Loft-Dev"
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_sorgente"
README = ROOT / "profile" / "README.md"
CONF = json.loads((SRC / "progetti.json").read_text())
TOPIC_GRUPPO = {"dashboard": "Dashboard", "automazioni": "Automazioni", "automazione": "Automazioni", "bot": "Automazioni", "ai": "AI",
                "strumenti": "Strumenti", "tool": "Strumenti", "dati": "Dati", "data": "Dati", "datamanagement": "Dati", "web": "Web", "sito": "Web"}
MESI = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]


def api(path):
    token = os.environ.get("ORG_READ_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    out, url = [], f"https://api.github.com{path}"
    while url:
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "gsloft-profilo"})
        if token: req.add_header("Authorization", "Bearer " + token)
        with urllib.request.urlopen(req, timeout=30) as r:
            out += json.load(r)
            nxt = re.search(r'<([^>]+)>;\s*rel="next"', r.headers.get("Link", ""))
            url = nxt.group(1) if nxt else None
    return out


def data_it(iso):
    d = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return f"{d.day} {MESI[d.month - 1]} {d.year}"


def raccogli():
    repos = api(f"/orgs/{ORG}/repos?type=all&per_page=100&sort=pushed")
    if not any(r["private"] for r in repos):
        # senza permessi sui privati la tabella perderebbe quasi tutti i progetti: meglio fermarsi che cancellarli
        tok = os.environ.get("ORG_READ_TOKEN") or ""
        tipo = "fine-grained" if tok.startswith("github_pat_") else "classico" if tok.startswith("ghp_") else "assente" if not tok else "altro"
        sys.exit(f"nessun repository privato visibile ({len(repos)} pubblici, token {tipo}): serve un token che li legga "
                 "(segreto ORG_READ_TOKEN, con accesso ai repository privati di GS-Loft-Dev). Non cambio niente.")
    adesso = datetime.datetime.now(datetime.timezone.utc)
    nascosti = set(CONF.get("nascondi", []))
    progetti = []
    for r in repos:
        topics = r.get("topics") or []
        if r["archived"] or r["name"] in nascosti or "nascondi" in topics:
            continue
        man = CONF["progetti"].get(r["name"], {})
        gruppo = man.get("gruppo") or next((TOPIC_GRUPPO[t] for t in topics if t in TOPIC_GRUPPO), None) or "Altro"
        testo = man.get("testo") or (r.get("description") or "").strip() or "In sviluppo"
        creato = datetime.datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
        progetti.append({
            "nome": r["name"], "gruppo": gruppo, "testo": testo, "privato": r["private"],
            "url": None if r["private"] else r["html_url"], "lingua": r.get("language") or "",
            "aggiornato": r["pushed_at"], "aggiornato_it": data_it(r["pushed_at"]),
            "nuovo": (adesso - creato).days <= 30 and r["name"] not in CONF["progetti"],
        })
    ordine = {g: i for i, g in enumerate(CONF["gruppi"])}
    progetti.sort(key=lambda p: (ordine.get(p["gruppo"], 99), -datetime.datetime.fromisoformat(p["aggiornato"].replace("Z", "+00:00")).timestamp()))
    ultimo = max(progetti, key=lambda p: p["aggiornato"]) if progetti else None
    return {"progetti": progetti, "totale": len(progetti), "privati": sum(p["privato"] for p in progetti),
            "ultimo": ultimo and {"nome": ultimo["nome"], "data": ultimo["aggiornato_it"]}}


def tabella(dati):
    righe = ["| | Progetto | Cosa fa | Aggiornato |", "|:--|:--|:--|:--|"]
    prec = None
    for p in dati["progetti"]:
        g = f"**{p['gruppo']}**" if p["gruppo"] != prec else ""
        prec = p["gruppo"]
        nome = f"[`{p['nome']}`]({p['url']})" if p["url"] else f"`{p['nome']}`"
        if p["nuovo"]: nome += " <sup>nuovo</sup>"
        testo = p["testo"].replace("|", "\\|")
        righe.append(f"| {g} | {nome} | {testo} | {p['aggiornato_it']} |")
    privati = dati["privati"]
    nota = (f"<sub>{dati['totale']} progetti, {privati} privati: li vedono solo i membri dell'organizzazione. "
            f"Elenco aggiornato da solo da una GitHub Action.</sub>")
    return "\n".join(righe) + "\n\n" + nota


def main():
    dati = raccogli()
    (SRC / "dati.json").write_text(json.dumps(dati, ensure_ascii=False, indent=2) + "\n")
    testo = README.read_text()
    blocco = f"<!-- progetti:inizio -->\n{tabella(dati)}\n<!-- progetti:fine -->"
    nuovo, n = re.subn(r"<!-- progetti:inizio -->.*?<!-- progetti:fine -->", blocco, testo, flags=re.S)
    if not n: sys.exit("nel README mancano i segnaposto <!-- progetti:inizio --> e <!-- progetti:fine -->")
    README.write_text(nuovo)
    subprocess.run([sys.executable, str(SRC / "make-anim.py")], check=True)
    print(f"{dati['totale']} progetti, ultimo aggiornamento: {dati['ultimo']}")


if __name__ == "__main__":
    main()
