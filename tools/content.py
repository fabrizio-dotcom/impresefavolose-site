"""All words on the Imprese Favolose site, in Italian (primary) and English (mirror).
Every change is made in both languages. tools/build.py turns this into HTML.

DRAFT lists questions for Fabrizio. They show on the preview in a box and make
tools/check.py fail, so nothing with an open question can be merged. Remove a
question only when Fabrizio has answered it."""

EMAIL = "info@impresefavolose.it"
FAB_CAMPAIGNS = "https://fabcampaigns.com"
SMART_MOUNTAINS = "https://smartmountains.net"

# Page key -> file path per language. Changing paths needs Fabrizio's approval (see CLAUDE.md).
PATHS = {
    "home": {"it": "index.html", "en": "en/index.html"},
    "programme": {"it": "programma.html", "en": "en/programme.html"},
    "ventures": {"it": "imprese.html", "en": "en/ventures.html"},
}

UI = {
    "it": {
        "nav": [("home", "Home"), ("programme", "Il programma"), ("ventures", "Le imprese")],
        "switch": "English", "switch_lang": "en",
        "skip": "Vai al contenuto",
        "draft_title": "Bozza: domande per Fabrizio",
        "draft_intro": "Da chiudere prima della pubblicazione:",
        "footer": "Imprese Favolose · Validazione del concept e incubazione",
        "footer_by": "Un’iniziativa sostenuta da",
        "contact": "Scrivici",
    },
    "en": {
        "nav": [("home", "Home"), ("programme", "The programme"), ("ventures", "Ventures")],
        "switch": "Italiano", "switch_lang": "it",
        "skip": "Skip to content",
        "draft_title": "Draft: questions for Fabrizio",
        "draft_intro": "To close before publishing:",
        "footer": "Imprese Favolose · Concept validation and incubation",
        "footer_by": "An initiative supported by",
        "contact": "Write to us",
    },
}

# ---------------------------------------------------------------- Home
HOME = {
    "it": {
        "title": "Imprese Favolose · Validazione del concept e incubazione",
        "desc": "Validiamo e incubiamo imprese nate dai problemi reali della montagna, fino a quando sono pronte per un primo pilota.",
        "eyebrow": "Validazione del concept e incubazione",
        "h1": "Imprese nate dai problemi veri della montagna",
        "lead": "Accompagniamo idee e team nella fase più fragile. Prima verifichiamo che il problema esista, che la soluzione regga e che il team la possa portare avanti. Poi incubiamo i concept che superano la prova, fino a quando sono pronti per un primo pilota sul campo.",
        "cta": [("programme", "Il programma"), ("ventures", "Le imprese")],
        "sections": [
            ("Il problema", [
                "In montagna i problemi sono concreti: versanti che si muovono, acqua da gestire, infrastrutture da monitorare, patrimonio da recuperare. Le competenze tecniche per affrontarli spesso ci sono già, nelle aziende e nelle persone delle valli.",
                "Quello che manca è il passaggio da un’idea promettente a un’impresa su cui qualcuno può investire tempo e denaro. Senza quel passaggio molte idee si fermano a metà, oppure partono senza le basi per crescere.",
            ]),
        ],
        "cards_title": "Cosa facciamo",
        "cards": [
            ("Fase 1", "Validazione del concept", "Mettiamo alla prova il problema, la soluzione e il team. Il risultato è una decisione chiara: andare avanti, cambiare rotta o fermarsi."),
            ("Fase 2", "Incubazione", "Per i concept validati: modello di business, struttura, governance e partner, fino a un’impresa pronta per il suo primo pilota."),
        ],
        "model_title": "Crescere in montagna, lavorare con la pianura",
        "model": [
            "In montagna ci sono le competenze tecniche e la capacità di esecuzione. Le imprese che validiamo crescono lì, insieme alle persone del territorio, e servono clienti e attraggono talenti dal Triveneto e dall’Emilia.",
            "Lavoriamo con le valli alpine e con le città di Padova, Treviso, Vicenza, Verona e Bologna.",
        ],
        "principles_title": "Come scegliamo",
        "principles": [
            ("Radici nel territorio", "Un legame operativo reale con la montagna. Il territorio è la fonte del problema e il primo banco di prova della soluzione."),
            ("Ambizione oltre la valle", "Acqua, rischio climatico e tenuta delle infrastrutture sono problemi alpini con una rilevanza molto più ampia. Cerchiamo soluzioni che possano crescere oltre il mercato locale."),
            ("Disponibilità a costruire insieme", "Lavoriamo dentro l’impresa, accanto ai fondatori. Serve un team pronto a mettere in discussione le proprie ipotesi."),
        ],
        "callout_title": "Hai un’idea nata da un problema di montagna?",
        "callout": "Non abbiamo bandi aperti. Se hai un’idea e un team in fase iniziale, scrivici due righe sul problema, sulla soluzione e su chi la porta avanti.",
    },
    "en": {
        "title": "Imprese Favolose · Concept validation and incubation",
        "desc": "We validate and incubate ventures born from real mountain problems, until they are ready for a first pilot.",
        "eyebrow": "Concept validation and incubation",
        "h1": "Ventures born from real mountain problems",
        "lead": "We work with ideas and teams at their most fragile stage. First we test that the problem exists, that the solution holds and that the team can carry it. Then we incubate the concepts that pass, until they are ready for a first pilot in the field.",
        "cta": [("programme", "The programme"), ("ventures", "Ventures")],
        "sections": [
            ("The problem", [
                "Mountain problems are concrete: slopes that move, water to manage, infrastructure to monitor, heritage to recover. The technical skills to tackle them are often already there, in the valleys’ companies and people.",
                "What is missing is the step from a promising idea to a venture someone can invest time and money in. Without that step many ideas stall halfway, or start without the foundations to grow.",
            ]),
        ],
        "cards_title": "What we do",
        "cards": [
            ("Phase 1", "Concept validation", "We test the problem, the solution and the team. The outcome is a clear decision: go ahead, change course or stop."),
            ("Phase 2", "Incubation", "For validated concepts: business model, structure, governance and partners, until the venture is ready for its first pilot."),
        ],
        "model_title": "Grow in the mountains, work with the plains",
        "model": [
            "The mountains have the technical skills and the capacity to execute. The ventures we validate grow there, with the people of the territory, and serve clients and attract talent from the Triveneto and Emilia.",
            "We work with the Alpine valleys and with the cities of Padova, Treviso, Vicenza, Verona and Bologna.",
        ],
        "principles_title": "How we choose",
        "principles": [
            ("Rooted in the territory", "A real operational link to the mountains. The territory is where the problem comes from and the first place the solution is tested."),
            ("Ambition beyond the valley", "Water, climate risk and infrastructure resilience are Alpine problems with much wider relevance. We look for solutions that can grow beyond the local market."),
            ("Ready to build together", "We work inside the venture, alongside the founders. That needs a team willing to challenge its own assumptions."),
        ],
        "callout_title": "Have an idea born from a mountain problem?",
        "callout": "We are not running open calls. If you have an early-stage idea and team, write us a few lines about the problem, the solution and who is behind it.",
    },
    "draft": [
        "Geography: the draft names Padova, Treviso, Vicenza, Verona and Bologna and no longer names Belluno as the base. OK to publish the cities?",
        "The ‘grow in the mountains, work with the plains’ section follows your Luxottica-model idea without naming Luxottica. Keep it unnamed, or name it?",
        "Partners: the draft names no partner organisations (the live site names Centro Consorzi as co-developer). Which partners, if any, appear publicly?",
    ],
}

# ---------------------------------------------------------------- Programme
PROGRAMME = {
    "it": {
        "title": "Il programma · Imprese Favolose",
        "desc": "Due fasi, validazione del concept e incubazione, ognuna chiusa da una decisione esplicita.",
        "h1": "Il programma",
        "sub": "Due fasi, ognuna chiusa da una decisione esplicita. Lavoriamo prima del pilota, dove una buona verifica costa poco e vale molto.",
        "phases": [
            ("Fase 1 · Gate 1", "Validazione del concept", [
                "Il problema territoriale è reale, e qualcuno lo sente abbastanza da voler pagare per risolverlo?",
                "L’approccio tecnico regge alla prova di chi conosce il campo?",
                "Il team è in grado di eseguire, o sa chi gli manca?",
            ], "Al Gate 1 cerchiamo una convinzione fondata. La trazione si misura più avanti. La decisione è una di tre: avanti, cambiare rotta, fermarsi."),
            ("Fase 2 · Gate 2", "Incubazione", [
                "Modello di business e ipotesi da verificare sul campo.",
                "Struttura societaria e governance adatte a ricevere partner e investitori.",
                "Partner tecnici e territoriali per il pilota.",
                "Piano del pilota: dove, con chi, quali dati raccogliere.",
            ], "Il Gate 2 chiude l’incubazione: l’impresa ha partner, sito, piano e governance per partire con il suo primo pilota."),
        ],
        "after_title": "Dopo il Gate 2",
        "after": "Il pilota e la crescita sono dell’impresa, con i suoi partner e investitori. Imprese Favolose può restare al suo fianco come advisor o nel consiglio.",
        "gov_title": "Governance dal primo giorno",
        "gov_lead": "Ogni gate è una decisione vera, presa con criteri noti in anticipo e documentata.",
        "gov": [
            ("Conflitti di interesse", "Chi valuta un’impresa non ne trae un vantaggio commerciale. I possibili conflitti vengono dichiarati e gestiti con un quadro di valutazione scritto."),
            ("Riservatezza", "Le informazioni dei fondatori restano protette. Regole di separazione tra i partner (Chinese wall) impediscono di usarle a proprio vantaggio."),
            ("Ruoli chiari", "Fab Campaigns Ltd sostiene Imprese Favolose come advisor e nella governance, senza ruoli esecutivi nelle imprese."),
        ],
        "callout_title": "Vuoi capire se la tua idea è pronta per il Gate 1?",
        "callout": "Scrivici due righe sul problema, sulla soluzione e sul team. Ti diciamo se e come possiamo aiutarti.",
    },
    "en": {
        "title": "The programme · Imprese Favolose",
        "desc": "Two phases, concept validation and incubation, each closed by an explicit decision.",
        "h1": "The programme",
        "sub": "Two phases, each closed by an explicit decision. We work before the pilot, where a good test costs little and is worth a lot.",
        "phases": [
            ("Phase 1 · Gate 1", "Concept validation", [
                "Is the territorial problem real, and does someone feel it enough to pay for a solution?",
                "Does the technical approach hold up with people who know the field?",
                "Can the team execute, or does it know who it is missing?",
            ], "At Gate 1 we look for grounded conviction. Traction is measured later. The decision is one of three: go ahead, change course, stop."),
            ("Phase 2 · Gate 2", "Incubation", [
                "Business model and assumptions to test in the field.",
                "Company structure and governance ready for partners and investors.",
                "Technical and territorial partners for the pilot.",
                "Pilot plan: where, with whom, which data to collect.",
            ], "Gate 2 closes incubation: the venture has the partners, site, plan and governance to start its first pilot."),
        ],
        "after_title": "After Gate 2",
        "after": "The pilot and the growth belong to the venture, with its own partners and investors. Imprese Favolose can stay alongside as an advisor or on the board.",
        "gov_title": "Governance from day one",
        "gov_lead": "Every gate is a real decision, taken against criteria known in advance, and written down.",
        "gov": [
            ("Conflicts of interest", "Whoever assesses a venture gains no commercial advantage from it. Possible conflicts are declared and managed through a written assessment framework."),
            ("Confidentiality", "Founders’ information stays protected. Separation rules between partners (Chinese walls) stop anyone using it for their own advantage."),
            ("Clear roles", "Fab Campaigns Ltd supports Imprese Favolose as an advisor and in its governance, with no executive roles in the ventures."),
        ],
        "callout_title": "Want to know if your idea is ready for Gate 1?",
        "callout": "Write us a few lines about the problem, the solution and the team. We will tell you whether and how we can help.",
    },
    "draft": [
        "Gates: the live site has three (concept validation, pilot deployment, scale readiness). The draft keeps two, Gate 1 concept validation and Gate 2 ready for pilot, and leaves the pilot and scale to the venture. Confirm?",
        "Removed from the public site: the shareholder percentages and the 5% work-for-equity stake. Do any equity terms go back on, once verified?",
        "Fab Campaigns’ role is written as ‘advisor and governance, no executive roles’, and Imprese Favolose ‘can stay as advisor or on the board’ after Gate 2. Right wording?",
    ],
}

# ---------------------------------------------------------------- Ventures
VENTURES = {
    "it": {
        "title": "Le imprese · Imprese Favolose",
        "desc": "Le prime idee con cui Imprese Favolose mette alla prova il proprio metodo.",
        "h1": "Le imprese",
        "sub": "Le prime idee con cui mettiamo alla prova il metodo. Ognuna parte da un problema concreto della montagna.",
        "ventures": [
            ("Intelligenza ambientale", "Smart Mountains",
             "Monitoraggio, modelli predittivi e supporto alle decisioni per chi gestisce infrastrutture, reti e protezione civile in montagna. Il metodo nasce e si prova sul campo in Valtellina e nelle Dolomiti.",
             (SMART_MOUNTAINS, "smartmountains.net")),
            ("Patrimonio culturale e naturale", "Valle I.",
             "Un’esperienza multisensoriale nelle gallerie allagate di una storica miniera delle Dolomiti, tra patrimonio industriale, scienza ambientale e tecnologie immersive. In fase di studio di fattibilità.",
             None),
        ],
        "callout_title": "Conosci un’idea che dovrebbe essere qui?",
        "callout": "Non abbiamo bandi aperti. Se hai radici in montagna e un problema che vale la pena risolvere, scrivici.",
    },
    "en": {
        "title": "Ventures · Imprese Favolose",
        "desc": "The first ideas Imprese Favolose is using to test its method.",
        "h1": "Ventures",
        "sub": "The first ideas we are using to test the method. Each one starts from a concrete mountain problem.",
        "ventures": [
            ("Environmental intelligence", "Smart Mountains",
             "Monitoring, predictive modelling and decision support for those who manage infrastructure, networks and civil protection in the mountains. The method was born, and is tested in the field, in Valtellina and the Dolomites.",
             (SMART_MOUNTAINS, "smartmountains.net")),
            ("Cultural and natural heritage", "Valle I.",
             "A multi-sensory experience in the flooded tunnels of a historic Dolomites mine, combining industrial heritage, environmental science and immersive technology. At feasibility stage.",
             None),
        ],
        "callout_title": "Know an idea that belongs here?",
        "callout": "We are not running open calls. If you have roots in the mountains and a problem worth solving, write to us.",
    },
    "draft": [
        "Smart Mountains: keep it listed, and with this description? The draft drops the ‘seed round summer 2026’ line and the planned pilots abroad.",
        "Valle I.: still active, and is ‘at feasibility stage’ right? The draft drops the tunnel length and the four-party joint venture detail.",
        "You mentioned startups and scale-ups of your own to add. Which ones, and in what words?",
    ],
}

NOTFOUND = {
    "title": "Pagina non trovata · Imprese Favolose",
    "h1": "Pagina non trovata",
    "sub_it": "Questa pagina non esiste, o si è spostata con il nuovo sito.",
    "sub_en": "This page does not exist, or it moved when the site was rebuilt.",
}

# Site-wide questions shown on the home page draft box.
SITE_DRAFT = [
    "Italian is now the main language (at impresefavolose.it/) with English under /en/. The live site is English first. OK?",
    "Footer: ‘An initiative supported by Fab Campaigns Ltd’. Is that the right public wording for who stands behind Imprese Favolose?",
]
