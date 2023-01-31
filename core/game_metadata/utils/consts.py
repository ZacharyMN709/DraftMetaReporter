"""
Contains constants about magic cards and arena ranks.

Key things outlined are:
 - Card Templating (Split, Adventure, etc.)
 - Card Rarity (Rarity list, Aliases, Indexes for sorting)
 - Types (Supertypes, Types, and Subtypes, split by Type)
 - Arena Ranks (Bronze - Mythic)
"""

from typing import Union, Literal
from enum import Flag, auto

# Arena Rank Consts
RANKS = ['None', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Mythic']


# region Rarity
RARITIES: set[str] = {'C', 'U', 'R', 'M'}

RARITY_ALIASES: dict[str, str] = {
    'common': "C",
    'uncommon': "U",
    'rare': "R",
    'mythic': "M",
    # TODO: See if there's a better way to handle this.
    'basic': "C"  # This comes from arena, for common lands in draft packs.
}

RARITY_INDEXES: dict[str, int] = {
    "C": 0,
    "U": 1,
    "R": 2,
    "M": 3,
}
# endregion Rarity


# region Typing
# https://mtg.fandom.com/wiki/Supertype
SUPERTYPES: set[str] = {"Basic", "Legendary", "Snow", "World", "Host"}
TYPES: set[str] = {"Land", "Creature", "Artifact", "Enchantment", "Planeswalker", "Instant", "Sorcery", "Tribal"}

LAND_SUBTYPES: set[str] = {
    "Plains", "Island", "Swamp", "Mountain", "Forest",
    "Desert", "Gate", "Lair", "Locus", "Sphere",
    "Urza's", "Mine", "Power-Plant", "Tower"
}

CREATURE_SUBTYPES: set[str] = {
     "Advisor", "Aetherborn", "Ally", "Angel", "Antelope", "Ape", "Archer", "Archon", "Army",
     "Artificer", "Assassin", "Assembly-Worker", "Atog", "Aurochs", "Avatar", "Azra", "Badger",
     "Barbarian", "Bard", "Basilisk", "Bat", "Bear", "Beast", "Beeble", "Beholder", "Berserker",
     "Bird", "Blinkmoth", "Boar", "Bringer", "Brushwagg", "Camarid", "Camel", "Caribou", "Carrier",
     "Cat", "Centaur", "Cephalid", "Chimera", "Citizen", "Cleric", "Cockatrice", "Construct", "Coward",
     "Crab", "Crocodile", "Cyclops", "Dauthi", "Demigod", "Demon", "Deserter", "Devil", "Dinosaur",
     "Djinn", "Dog", "Dragon", "Drake", "Dreadnought", "Drone", "Druid", "Dryad", "Dwarf", "Efreet",
     "Egg", "Elder", "Eldrazi", "Elemental", "Elephant", "Elf", "Elk", "Eye", "Faerie", "Ferret",
     "Fish", "Flagbearer", "Fox", "Fractal", "Frog", "Fungus", "Gargoyle", "Germ", "Giant", "Gith", "Gnoll",
     "Gnome", "Goat", "Goblin", "God", "Golem", "Gorgon", "Graveborn", "Gremlin", "Griffin", "Hag",
     "Halfling", "Hamster", "Harpy", "Hellion", "Hippo", "Hippogriff", "Homarid", "Homunculus",
     "Horror", "Horse", "Human", "Hydra", "Hyena", "Illusion", "Imp", "Incarnation", "Inkling",
     "Insect", "Jackal", "Jellyfish", "Juggernaut", "Kavu", "Kirin", "Kithkin", "Knight", "Kobold",
     "Kor", "Kraken", "Lamia", "Lammasu", "Leech", "Leviathan", "Lhurgoyf", "Licid", "Lizard",
     "Manticore", "Masticore", "Mercenary", "Merfolk", "Metathran", "Minion", "Minotaur", "Mite", "Mole",
     "Monger", "Mongoose", "Monk", "Monkey", "Moonfolk", "Mouse", "Mutant", "Myr", "Mystic", "Naga",
     "Nautilus", "Nephilim", "Nightmare", "Nightstalker", "Ninja", "Noble", "Noggle", "Nomad", "Nymph",
     "Octopus", "Ogre", "Ooze", "Orb", "Orc", "Orgg", "Otter", "Ouphe", "Ox", "Oyster", "Pangolin",
     "Peasant", "Pegasus", "Pentavite", "Pest", "Phelddagrif", "Phoenix", "Phyrexian", "Pilot",
     "Pincher", "Pirate", "Plant", "Praetor", "Prism", "Processor", "Rabbit", "Raccoon", "Ranger",
     "Rat", "Rebel", "Reflection", "Rhino", "Rigger", "Rogue", "Sable", "Salamander", "Samurai",
     "Sand", "Saproling", "Satyr", "Scarecrow", "Scion", "Scorpion", "Scout", "Sculpture", "Serf",
     "Serpent", "Servo", "Shade", "Shaman", "Shapeshifter", "Shark", "Sheep", "Siren", "Skeleton",
     "Slith", "Sliver", "Slug", "Snake", "Soldier", "Soltari", "Spawn", "Specter", "Spellshaper",
     "Sphinx", "Spider", "Spike", "Spirit", "Splinter", "Sponge", "Squid", "Squirrel", "Starfish",
     "Surrakar", "Survivor", "Tentacle", "Tetravite", "Thalakos", "Thopter", "Thrull", "Tiefling",
     "Treefolk", "Trilobite", "Triskelavite", "Troll", "Turtle", "Unicorn", "Vampire", "Vedalken",
     "Viashino", "Volver", "Wall", "Walrus", "Warlock", "Warrior", "Weird", "Werewolf", "Whale",
     "Wizard", "Wolf", "Wolverine", "Wombat", "Worm", "Wraith", "Wurm", "Yeti", "Zombie", "Zubera"
}

ARTIFACT_SUBTYPES: set[str] = {
    "Blood", "Clue", "Contraption", "Equipment", "Food",
    "Gold", "Fortification", "Powerstone", "Treasure", "Vehicle"
}

ENCHANTMENT_SUBTYPES: set[str] = {
    "Aura", "Cartouche", "Curse", "Rune", "Background", "Class", "Saga", "Shard", "Shrine"
}

PLANESWALKER_SUBTYPES: set[str] = {
    "Ajani", "Aminatou", "Angrath", "Arlinn", "Ashiok", "Bahamut", "Basri", "Bolas", "Calix",
    "Chandra", "Dack", "Dakkon", "Daretti", "Davriel", "Dihada", "Domri", "Dovin", "Ellywick",
    "Elspeth", "Estrid", "Freyalise", "Garruk", "Gideon", "Grist", "Huatli", "Jace", "Jaya",
    "Jeska", "Kaito", "Karn", "Kasmina", "Kaya", "Kiora", "Koth", "Liliana", "Lolth", "Lukka",
    "Minsc", "Mordenkainen", "Nahiri", "Narset", "Niko", "Nissa", "Nixilis", "Oko", "Ral", "Rowan",
    "Saheeli", "Samut", "Sarkhan", "Serra", "Sorin", "Szat", "Tamiyo", "Tasha", "Teferi", "Teyo",
    "Tezzeret", "Tibalt", "Tyvar", "Ugin", "Urza", "Venser", "Vivien", "Vraska", "Will", "Windgrace",
    "Wrenn", "Xenagos", "Yanggu", "Yanling", "Zariel"
}

INSTANT_SUBTYPES: set[str] = {"Adventure", "Arcane", "Trap"}

SORCERY_SUBTYPES: set[str] = {"Adventure", "Arcane", "Lesson"}

SUBTYPES: set[str] = LAND_SUBTYPES | CREATURE_SUBTYPES | ARTIFACT_SUBTYPES | ENCHANTMENT_SUBTYPES | \
                     PLANESWALKER_SUBTYPES | INSTANT_SUBTYPES | SORCERY_SUBTYPES

SUBTYPE_DICT: dict[str, set[str]] = {
    "Land": LAND_SUBTYPES,
    "Creature": CREATURE_SUBTYPES,
    "Artifact": ARTIFACT_SUBTYPES,
    "Enchantment": ENCHANTMENT_SUBTYPES,
    "Planeswalker": PLANESWALKER_SUBTYPES,
    "Instant": INSTANT_SUBTYPES,
    "Sorcery": SORCERY_SUBTYPES
}
# endregion Typing


# region Card Layouts
# Type information for the card json Scryfall returns.
CARD_INFO = dict[str, Union[str, int, dict[str, str], list[str], list[dict]]]
CARD_SIDE = Literal['default', 'main', 'adventure', 'left', 'right', 'front', 'back', 'flipped', 'melded', 'prototype']


# https://scryfall.com/docs/api/layouts
class CardLayouts(Flag):
    NORMAL = auto()
    SPLIT = auto()
    FLIP = auto()
    TRANSFORM = auto()
    MODAL_DFC = auto()
    MELD = auto()
    LEVELER = auto()
    CLASS = auto()
    SAGA = auto()
    ADVENTURE = auto()
    PROTOTYPE = auto()

    BASIC = NORMAL | LEVELER | CLASS | SAGA
    FUSED = ADVENTURE | SPLIT | FLIP | PROTOTYPE
    TWO_SIDED = TRANSFORM | MODAL_DFC | MELD


LAYOUT_DICT: dict[str, CardLayouts] = {
    "normal": CardLayouts.NORMAL,
    "split": CardLayouts.SPLIT,
    "flip": CardLayouts.FLIP,
    "transform": CardLayouts.TRANSFORM,
    "modal_dfc": CardLayouts.MODAL_DFC,
    "meld": CardLayouts.MELD,
    "leveler": CardLayouts.LEVELER,
    "class": CardLayouts.CLASS,
    "saga": CardLayouts.SAGA,
    "adventure": CardLayouts.ADVENTURE,
    "prototype": CardLayouts.PROTOTYPE,
}
# endregion Card Layouts
