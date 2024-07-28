"""
Constants for the scraper
"""

ALLOWED_BROKERAGE = {"prodaja", "oddaja", "nakup", "najem"}

ALLOWED_REGIONS = {
    "ljubljana-mesto",
    "ljubljana-okolica",
    "juzna-primorska",
    "severna-primorska",
    "notranjska",
    "savinska",
    "gorenjska",
    "koroska",
    "podravska",
    "posavska",
    "pomurska",
}

ALLOWED_SUBREGIONS = {
    "ljubljana-mesto": [
        "ljubljana-bezigrad",
        "ljubljana-center",
        "ljubljana-moste-polje",
        "ljubljana-siska",
        "ljubljana-vic-rudnik",
    ],
    "ljubljana-okolica": [
        "domzale",
        "grosuplje",
        "kamnik",
        "litija",
        "ljubljana-jugozahodni-del-vic-rudnik",
        "ljubljana-severovzhodni-del-bezigrad",
        "ljubljana-severozahodni-del-siska",
        "ljubljana-vzhodni-del-moste-polje",
        "logatec",
        "vrhnika",
    ],
    "notranjska": ["cerknica", "ilirska-bistrica", "postojna"],
    "dolenjska": ["crnomelj", "kocevje", "metlika", "novo-mesto", "ribnica", "trebnje"],
    "gorenjska": ["jesenice", "kranj", "radovljica", "skofja-loka", "trzic"],
    "severna-primorska": ["ajdovscina", "idrija", "nova-gorica", "tolmin"],
    "juzna-primorska": ["izola", "koper", "piran", "sezana"],
    "savinjska": [
        "celje",
        "lasko",
        "mozirje",
        "slovenske-konjice",
        "sentjur",
        "smarje-pri-jelsah",
        "velenje",
        "zalec",
    ],
    "podravska": [
        "lenart",
        "maribor",
        "ormoz",
        "pesnica",
        "ptuj",
        "ruse",
        "slovenska-bistrica",
    ],
}

ALLOWED_PROPERTY_TYPES = {
    "stanovanje",
    "hisa",
    "vikend",
    "posest",
    "poslovni-prostor",
    "garaza",
    "pocitniski-objekt",
}
