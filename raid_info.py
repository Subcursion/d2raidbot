class Raid:
    def __init__(
        self,
        name: str,
        description: str = None,
        color: int = 0x00,
        logo_url: str = None,
        aliases: list = [],
    ):
        if name is None or len(name) == 0:
            raise ValueError("The raid name must not be none or empty")
        self.name = name
        self.description = description or ""
        self.color = color or 0x000000
        self.logo_url = logo_url or ""
        self.aliases = aliases or []


raids = [
    # Raid("Leviathan"),
    Raid(
        "Last Wish",
        description="The opportunity of a lifetime",
        aliases=["lw", "wish"],
        logo_url="https://destiny.wiki.gallery/images/5/55/Dreaming_Raid.jpg",
        color=0x461D23,
    ),
    # Raid("Scourge of the Past", aliases=["scourge"]),
    # Raid("Crown of Sorrow", aliases=["crown", "cos"]),
    Raid(
        "Garden of Salvation",
        description="The garden calls out to you",
        aliases=["garden", "gos"],
        logo_url=(
            "https://destiny.wiki.gallery/images/thumb/a/a7/VexSalvationGarden2.jpg/1600px-Vex"
            "SalvationGarden2.jpg"
        ),
        color=0x62937E,
    ),
    Raid(
        "Deep Stone Crypt",
        description="The chains of legacy must be broken",
        aliases=["dsc", "crypt"],
        logo_url="https://destiny.wiki.gallery/images/1/12/DSCRaidInfobox.jpg",
        color=0xC67848,
    ),
    Raid(
        "Vault of Glass",
        description="Beneath Venus, evil stirs...",
        aliases=["vog", "vault"],
        logo_url="https://destiny.wiki.gallery/images/6/6c/Destiny-VaultOfGlass-Screen.jpg",
        color=0x90ADB9,
    ),
    Raid(
        "Vow of the Disciple",
        description="The desciple beckons...",
        aliases=["votd", "vow"],
        logo_url=(
            "https://destiny.wiki.gallery/images/thumb/0/0e/Vow_of_the_Disciple.jpg/1600px-"
            "Vow_of_the_Disciple.jpg"
        ),
        color=0x5A6032,
    ),
    Raid(
        "King's Fall",
        description="Long live the King...",
        aliases=["kf"],
        logo_url="https://destiny.wiki.gallery/images/1/12/KingsFallArt.jpg",
        color=0x3D100A,
    ),
    Raid(
        "Root of Nightmares",
        description="A sinister threat has taken root.",
        aliases=["ron", "root"],
        logo_url=(
            "https://destiny.wiki.gallery/images/thumb/d/d7/Root_of_Nightmares.jpg"
            "/1600px-Root_of_Nightmares.jpg"
        ),
        color=0x553947,
    ),
]
