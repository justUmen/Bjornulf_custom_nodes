import random


class Everything(str):
    def __ne__(self, __value: object) -> bool:
        return False


class SharedLists:
    #Creatures
    CREATURE_TYPES = {
        "Dragon": {
            "name": "Dragon",
            "description": "Massive reptilian creature with scales, wings, and the ability to breathe fire. Known for their intelligence and hoarding treasure."
        },
        "Phoenix": {
            "name": "Phoenix",
            "description": "Immortal bird of flame that resurrects from its own ashes. Radiates golden light and healing energy."
        },
        "Unicorn": {
            "name": "Unicorn",
            "description": "Majestic horse-like creature with a single spiral horn, often pure white with healing and purifying powers."
        },
        "Griffin": {
            "name": "Griffin",
            "description": "Hybrid creature with eagle head/wings and lion body. Noble and fierce guardians of treasure."
        },
        "Hydra": {
            "name": "Hydra",
            "description": "Multi-headed serpentine monster that grows two heads when one is cut off. Highly regenerative and aggressive."
        },
        "Chimera": {
            "name": "Chimera",
            "description": "Monstrous hybrid with lion's head, goat's body, and serpent's tail. Breathes fire and combines the ferocity of multiple beasts."
        },
        "Basilisk": {
            "name": "Basilisk",
            "description": "Legendary reptile known as the King of Serpents. Its gaze can turn living creatures to stone."
        },
        "Kraken": {
            "name": "Kraken",
            "description": "Colossal sea monster with massive tentacles capable of destroying ships. Terror of the deep ocean."
        },
        "Werewolf": {
            "name": "Werewolf",
            "description": "Human who transforms into a powerful wolf-like creature under the full moon. Possesses superhuman strength and primal instincts."
        },
        "Vampire": {
            "name": "Vampire",
            "description": "Immortal undead being that feeds on life force or blood. Possesses supernatural powers and weakness to sunlight."
        },
        "Goblin": {
            "name": "Goblin",
            "description": "Small, grotesque humanoid known for craftiness and greed. Often skilled in mechanical crafts and trickery."
        },
        "Troll": {
            "name": "Troll",
            "description": "Large, brutish creature with regenerative abilities. Known for their immense strength and primitive nature."
        },
        "Ogre": {
            "name": "Ogre",
            "description": "Giant humanoid known for great strength and limited intelligence. Often solitary and territorial."
        },
        "Fairy": {
            "name": "Fairy",
            "description": "Tiny winged humanoid with magical powers. Associated with nature and mischievous enchantments."
        },
        "Pixie": {
            "name": "Pixie",
            "description": "Small, winged sprite known for playful nature and magical pranks. Often leaves a trail of sparkles."
        },
        "Mermaid": {
            "name": "Mermaid",
            "description": "Aquatic being with human upper body and fish tail. Known for enchanting songs and marine magic."
        },
        "Centaur": {
            "name": "Centaur",
            "description": "Half-human, half-horse creature skilled in archery and astronomy. Known for wisdom and wild nature."
        },
        "Minotaur": {
            "name": "Minotaur",
            "description": "Powerful creature with human body and bull's head. Known for incredible strength and maze-dwelling."
        },
        "Harpy": {
            "name": "Harpy",
            "description": "Creature with woman's head and bird's body. Known for their shrieking calls and vicious nature."
        },
        "Sphinx": {
            "name": "Sphinx",
            "description": "Wise creature with human head and lion's body. Known for posing riddles and guarding ancient secrets."
        },
        "Cerberus": {
            "name": "Cerberus",
            "description": "Three-headed hound that guards the underworld. Each head possesses unique abilities and awareness."
        },
        "Pegasus": {
            "name": "Pegasus",
            "description": "Majestic winged horse with pure white coat. Symbol of divine inspiration and heroic adventures."
        },
        "Manticore": {
            "name": "Manticore",
            "description": "Persian legendary creature with lion's body, human face, and scorpion's tail. Known for its deadly poison."
        },
        "Gorgon": {
            "name": "Gorgon",
            "description": "Female creature with snakes for hair whose gaze turns victims to stone. Powerful and cursed being."
        },
        "Selkie": {
            "name": "Selkie",
            "description": "Seal-like creature that can shed its skin to become human. Associated with the sea and shapeshifting."
        },
        "Yeti": {
            "name": "Yeti",
            "description": "Massive ape-like creature dwelling in snowy mountains. Known for supernatural strength and cold resistance."
            },
        "Sasquatch": {
            "name": "Sasquatch",
            "description": "Large, hairy humanoid of the forests. Elusive and powerful, with remarkable survival abilities."
        },
        "Wendigo": {
            "name": "Wendigo",
            "description": "Gaunt, towering spirit of winter and hunger. Possesses the power to induce madness and endless hunger."
        },
        "Djinn": {
            "name": "Djinn",
            "description": "Powerful spirit of smokeless fire with reality-altering powers. Master of wishes and ancient magic."
        },
        "Ifrit": {
            "name": "Ifrit",
            "description": "Powerful fire spirit with immense magical abilities. Associated with the underground and flames."
        },
        "Banshee": {
            "name": "Banshee",
            "description": "Female spirit whose wail heralds death. Capable of inducing terror and predicting doom."
        },
        "Kelpie": {
            "name": "Kelpie",
            "description": "Shape-shifting water spirit appearing as a horse. Lures victims into water with its supernatural beauty."
        },
        "Nymph": {
            "name": "Nymph",
            "description": "Nature spirit embodying natural features. Possesses powerful nature magic and eternal youth."
        },
        "Dryad": {
            "name": "Dryad",
            "description": "Tree spirit bound to its forest home. Protector of woods with power over plant life."
        },
        "Leprechaun": {
            "name": "Leprechaun",
            "description": "Tiny, clever fairy known for making shoes and hoarding gold. Masters of trickery and illusion."
        },
        "Ghoul": {
            "name": "Ghoul",
            "description": "Undead creature that feeds on corpses. Possesses supernatural strength and disease-spreading abilities."
        },
        "Zombie": {
            "name": "Zombie",
            "description": "Reanimated corpse driven by hunger for flesh. Spreads undeath through bites and scratches."
        },
        "Skeleton Warrior": {
            "name": "Skeleton Warrior",
            "description": "Animated skeleton with combat abilities. Immune to conventional wounds and tireless in battle."
        },
        "Specter": {
            "name": "Specter",
            "description": "Vengeful ghost with the power to drain life force. Can pass through solid objects and inspire terror."
        },
        "Wraith": {
            "name": "Wraith",
            "description": "Incorporeal undead being that feeds on life essence. Invisible to normal sight and immune to physical harm."
        },
        "Shade": {
            "name": "Shade",
            "description": "Shadow-like undead entity that stalks in darkness. Can manipulate shadows and drain strength."
        },
        "Dullahan": {
            "name": "Dullahan",
            "description": "Headless horseman carrying its own head. Herald of death whose speech can stop hearts."
        },
        "Cthulhu": {
            "name": "Cthulhu",
            "description": "Ancient cosmic entity with octopus-like head and dragon wings. Drives mortals mad with its mere presence."
        },
        "Deep One": {
            "name": "Deep One",
            "description": "Fish-like humanoid dwelling in ocean depths. Possesses immortality and supernatural strength."
        },
        "Shoggoth": {
            "name": "Shoggoth",
            "description": "Amorphous mass of protoplasm with countless eyes. Can change shape and absorb matter."
        },
        "Behemoth": {
            "name": "Behemoth",
            "description": "Massive beast of biblical proportions. Embodiment of natural might and unstoppable force."
        },
        "Leviathan": {
            "name": "Leviathan",
            "description": "Colossal sea serpent of primordial chaos. Can create whirlpools and command storms."
        },
        "Rakshasa": {
            "name": "Rakshasa",
            "description": "Shape-shifting demon with backward hands. Master of illusion and magical deception."
        },
        "Asura": {
            "name": "Asura",
            "description": "Multi-armed celestial being with divine powers. Warrior spirit with supernatural combat abilities."
        },
        "Nagini": {
            "name": "Nagini",
            "description": "Powerful serpent being with human features. Possesses deadly venom and magical abilities."
        },
            "Chupacabra": {
            "name": "Chupacabra",
            "description": "Blood-drinking creature with spikes and large eyes. Known for attacking livestock with vampiric abilities."
        },
        "Mothman": {
            "name": "Mothman",
            "description": "Winged humanoid with glowing red eyes. Associated with impending disasters and prophetic visions."
        },
        "Jiangshi": {
            "name": "Jiangshi",
            "description": "Chinese hopping vampire with rigid posture. Drains life force and moves by jumping with arms outstretched."
        },
        "Gremlin": {
            "name": "Gremlin",
            "description": "Small, mischievous creature that sabotages machinery. Multiplies when wet and causes technological chaos."
        },
        "Imp": {
            "name": "Imp",
            "description": "Minor demon known for mischief and minor evil deeds. Can fly and cast small spells."
        },
        "Succubus": {
            "name": "Succubus",
            "description": "Female demon that seduces and drains life force. Shape-shifter with powerful charm abilities."
        },
        "Incubus": {
            "name": "Incubus",
            "description": "Male demon counterpart to succubus. Preys on sleeping victims with dream manipulation powers."
        },
        "Fomorian": {
            "name": "Fomorian",
            "description": "Ancient race of deformed giants from the sea. Possess great strength and destructive magic."
        },
        "Fenrir": {
            "name": "Fenrir",
            "description": "Gigantic wolf of Norse mythology. Destined to devour the sun, with strength to break any chain."
        },
        "Jörmungandr": {
            "name": "Jörmungandr",
            "description": "World Serpent so large it encircles the earth. Its release heralds the end of the world."
        },
        "Hippogriff": {
            "name": "Hippogriff",
            "description": "Half-eagle, half-horse hybrid creature. Combines speed of horse with eagle's flight abilities."
        },
        "Wyvern": {
            "name": "Wyvern",
            "description": "Dragon-like creature with two legs and wings. Known for poisonous bite and aerial hunting."
        },
        "Cockatrice": {
            "name": "Cockatrice",
            "description": "Hybrid of rooster and dragon that can petrify. Its gaze and breath can turn victims to stone."
        },
        "Salamander": {
            "name": "Salamander",
            "description": "Magical lizard that lives in and breathes fire. Immune to flames and radiates intense heat."
        },
        "Lamia": {
            "name": "Lamia",
            "description": "Half-woman, half-serpent creature that devours children. Known for seductive powers and prophetic abilities."
        },
        "Seraphim": {
            "name": "Seraphim",
            "description": "Highest order of angels with six wings. Radiate divine light and burning holy power."
        },
        "Cherubim": {
            "name": "Cherubim",
            "description": "Angelic beings with four faces and multiple wings. Guard divine places with flaming swords."
        },
        "Golem": {
            "name": "Golem",
            "description": "Animated construct made of clay or stone. Follows commands literally with immense strength."
        },
        "Elemental": {
            "name": "Elemental",
            "description": "Pure manifestation of natural forces. Commands power over their respective element."
        },
        "Shadow Demon": {
            "name": "Shadow Demon",
            "description": "Demon made of living darkness. Can possess shadows and inspire terror."
        },
        "Hellhound": {
            "name": "Hellhound",
            "description": "Demonic dog with burning eyes and fiery breath. Guards the gates of the underworld."
        },
        "Bone Dragon": {
            "name": "Bone Dragon",
            "description": "Skeletal dragon reanimated by dark magic. Breathes death and commands undead."
        },
        "Frost Giant": {
            "name": "Frost Giant",
            "description": "Massive humanoid of ice and snow. Commands winter storms and freezing magic."
        },
        "Fire Giant": {
            "name": "Fire Giant",
            "description": "Enormous being of living flame and magma. Wreaks destruction with burning weapons and heat."
        },
        "Storm Giant": {
            "name": "Storm Giant",
            "description": "Colossal giant commanding weather and lightning. Can summon tempests and thunder."
        },
        "Zombie Dragon": {
            "name": "Zombie Dragon",
            "description": "Undead dragon reanimated by necromancy. Breathes plague and decay instead of fire."
        },
        "Sea Serpent": {
            "name": "Sea Serpent",
            "description": "Enormous aquatic monster with serpentine body. Creates whirlpools and capsizes ships."
        },
        "Anubite": {
            "name": "Anubite",
            "description": "Jackal-headed warrior with divine powers. Guards tombs and judges souls of the dead."
        },
        "Grim Reaper": {
            "name": "Grim Reaper",
            "description": "Personification of death with scythe and black robes. Harvests souls and guides them to afterlife."
        },
        "Poltergeist": {
            "name": "Poltergeist",
            "description": "Noisy ghost that manipulates physical objects. Creates chaos through telekinetic powers."
        },
        "Will-o'-the-Wisp": {
            "name": "Will-o'-the-Wisp",
            "description": "Mysterious floating light that leads travelers astray. Appears in swamps and dark forests."
        },
        "Boggart": {
            "name": "Boggart",
            "description": "Household spirit that causes mischief and fear. Can shapeshift to match victims' worst fears."
        },
        "Barghest": {
            "name": "Barghest",
            "description": "Goblin-dog hybrid that hunts at night. Can shapeshift and foretells death with its howl."
        },
        "Naga": {
            "name": "Naga",
            "description": "Snake-human hybrid with powerful magic. Masters of ancient wisdom and deadly poison."
        },
        "Kami": {
            "name": "Kami",
            "description": "Nature spirit of Japanese mythology. Protects natural features and grants blessings."
        },
        "Tengu": {
            "name": "Tengu",
            "description": "Bird-like spirit with long nose and wings. Master of martial arts and mountain magic."
        },
        "Kappa": {
            "name": "Kappa",
            "description": "Water imp with bowl-like head depression. Knows healing arts but can be mischievous."
        },
        "Oni": {
            "name": "Oni",
            "description": "Horned demon with colorful skin and great strength. Wields iron clubs and commands lightning."
        },
        "Yokai": {
            "name": "Yokai",
            "description": "Supernatural being of Japanese folklore. Various forms with unique supernatural abilities."
        },
        "Bakemono": {
            "name": "Bakemono",
            "description": "Shape-shifting monster of Japanese legend. Can transform into various objects and creatures."
        },
        "Slime": {
            "name": "Slime",
            "description": "Amorphous creature made of living ooze. Can absorb and dissolve various materials."
        },
        "Mimic": {
            "name": "Mimic",
            "description": "Shape-shifting creature that disguises as objects. Surprises prey with sudden attacks."
        },
        "Beholder": {
            "name": "Beholder",
            "description": "Floating spherical monster with multiple eye stalks. Each eye projects different magical effects."
        },
        "Mind Flayer": {
            "name": "Mind Flayer",
            "description": "Tentacle-faced humanoid with psychic powers. Feeds on brains and dominates minds."
        },
        "Aboleth": {
            "name": "Aboleth",
            "description": "Ancient aquatic being with psychic abilities. Enslaves minds and remembers all history."
        },
        "Displacer Beast": {
            "name": "Displacer Beast",
            "description": "Panther-like creature with tentacles that appears shifted from its true location. Master of illusion."
        },
        "Umber Hulk": {
            "name": "Umber Hulk",
            "description": "Powerful burrowing monster with confusing gaze. Can tunnel through solid rock."
        },
        "Bulette": {
            "name": "Bulette",
            "description": "Armored creature that burrows and leaps from underground. Known as the 'landshark'."
        },
        "Rust Monster": {
            "name": "Rust Monster",
            "description": "Insectoid creature that corrodes metal on contact. Drawn to metallic objects and armor."
        },
        "Gelatinous Cube": {
            "name": "Gelatinous Cube",
            "description": "Transparent cubic ooze that absorbs and digests all in its path. Perfectly shaped for dungeon corridors."
        },
            "Treant": {
            "name": "Treant",
            "description": "Sentient tree being of immense size and strength. Commands nature and protects forests."
        },
        "Ent": {
            "name": "Ent",
            "description": "Ancient shepherd of the forest in tree form. Slow to anger but terrible in wrath."
        },
        "Balrog": {
            "name": "Balrog",
            "description": "Demon of shadow and flame with burning whip. Ancient evil with wings of darkness and terror."
        },
        "Nazgûl": {
            "name": "Nazgûl",
            "description": "Wraith-like being in black robes with terrifying screech. Former kings corrupted by dark power."
        },
        "Uruk-hai": {
            "name": "Uruk-hai",
            "description": "Enhanced orc warrior bred for battle. Stronger, larger, and more intelligent than common orcs."
        },
        "Shelob": {
            "name": "Shelob",
            "description": "Giant spider of ancient evil. Weaves webs of darkness and hunts with paralyzing venom."
        },
        "Warg": {
            "name": "Warg",
            "description": "Evil wolf-like creature of great size and cunning. Often used as mounts by orcs."
        },
        "Fell Beast": {
            "name": "Fell Beast",
            "description": "Winged dragon-like mount of the Nazgûl. Strikes terror with its otherworldly screech."
        },
        "Ettin": {
            "name": "Ettin",
            "description": "Two-headed giant with brutal strength. Each head has its own personality and thoughts."
        },
        "Quetzalcoatl": {
            "name": "Quetzalcoatl",
            "description": "Feathered serpent deity of wisdom. Commands wind and knowledge with divine power."
        },
        "Garuda": {
            "name": "Garuda",
            "description": "Divine bird-human hybrid of immense size. Solar deity with power over winds and flight."
        },
        "Thunderbird": {
            "name": "Thunderbird",
            "description": "Massive bird that creates storms with its wings. Controls weather and shoots lightning from its eyes."
        },
        "Amphiptere": {
            "name": "Amphiptere",
            "description": "Winged serpent with feathered wings. Agile flyer with venomous bite."
        },
        "Jabberwock": {
            "name": "Jabberwock",
            "description": "Fearsome dragon-like creature with flaming eyes. Whiffling and burbling as it hunts."
        },
        "Nemean Lion": {
            "name": "Nemean Lion",
            "description": "Giant lion with impenetrable golden fur. Immune to conventional weapons."
        },
        "Satyr": {
            "name": "Satyr",
            "description": "Half-human, half-goat being of revelry. Masters of music and woodland magic."
        },
        "Faun": {
            "name": "Faun",
            "description": "Gentle forest spirit with goat legs. Plays enchanting music on pipes."
        },
        "Echidna": {
            "name": "Echidna",
            "description": "Mother of monsters, half-woman half-snake. Immortal nymph who bears legendary creatures."
        },
        "Typhon": {
            "name": "Typhon",
            "description": "Father of monsters with hundred dragon heads. Creates storms and natural disasters."
        },
        "Cyclops": {
            "name": "Cyclops",
            "description": "Giant with single eye in center of forehead. Master craftsman with incredible strength."
        },
        "Siren": {
            "name": "Siren",
            "description": "Beautiful being whose song lures sailors to doom. Voice can enchant and control minds."
        },
        "Scylla": {
            "name": "Scylla",
            "description": "Multi-headed sea monster with dog-like heads. Snatches sailors from passing ships."
        },
        "Charybdis": {
            "name": "Charybdis",
            "description": "Living whirlpool that swallows ships whole. Creates massive water vortexes."
        },
        "Hecatoncheires": {
            "name": "Hecatoncheires",
            "description": "Hundred-armed giant of immense power. Can perform hundred actions simultaneously."
        },
        "Lilith": {
            "name": "Lilith",
            "description": "First demon woman with powerful dark magic. Mother of monsters and night creatures."
        },
        "Astral Projection": {
            "name": "Astral Projection",
            "description": "Spirit form that travels through astral plane. Ethereal being of pure consciousness."
        },
        "Djinn of the Lamp": {
            "name": "Djinn of the Lamp",
            "description": "Powerful wish-granting spirit bound to lamp. Masters of reality-altering magic."
        },
        "Genasi": {
            "name": "Genasi",
            "description": "Humanoid embodiment of elemental forces. Commands power of their elemental heritage."
        },
        "Planar Entity": {
            "name": "Planar Entity",
            "description": "Being from another dimension or reality. Possesses powers alien to natural world."
        },
        "Ethereal Spirit": {
            "name": "Ethereal Spirit",
            "description": "Ghost-like being that exists between planes. Can phase through matter and possess objects."
        },
        "Archon": {
            "name": "Archon",
            "description": "Celestial being of pure law and good. Radiates divine light and authority."
        },
        "Demon Lord": {
            "name": "Demon Lord",
            "description": "Ruler of demonic forces with corrupt power. Commands legions of lesser demons."
        },
        "Archdemon": {
            "name": "Archdemon",
            "description": "Highest ranking demon of tremendous power. Embodies specific aspect of evil and corruption."
        }
    }
    
    LAND_ANIMALS = [
        # Tiny (less than 1 foot)
        "Mouse", "Hamster", "Ant", "Gecko", "Shrew", "Cricket", "Ladybug", "Butterfly", "Grasshopper", "Scorpion",
        
        # Small (1-3 feet)
        "Cat", "Rabbit", "Fox", "Raccoon", "Beaver", "Skunk", "Squirrel", "Chicken", "Meerkat", "Koala",
        
        # Medium (3-8 feet)
        "Wolf", "Dog", "Deer", "Lion", "Tiger", "Bear", "Leopard", "Cheetah", "Pig", "Sheep",
        
        # Large (8-15 feet)
        "Horse", "Cow", "Moose", "Bison", "Rhinoceros", "Hippopotamus", "Giraffe", "Camel", "Elk", "Buffalo",
        
        # Huge (15-30 feet)
        "Elephant", "Grizzly Bear", "Polar Bear", "Gorilla", "Anaconda", "Python", "Komodo Dragon", "Ostrich", "Kangaroo", "Sloth Bear",
        
        # Colossal (30-100 feet)
        "Brachiosaurus", "Tyrannosaurus Rex", "Spinosaurus", "Pteranodon", "Mammoth", "Ground Sloth", "Paraceratherium", "Deinotherium", "Woolly Rhinoceros", "Gigantopithecus",
        
        # Gigantic (100+ feet)
        "Argentinosaurus", "Supersaurus", "Diplodocus", "Amphicoelias", "Ultrasaurus", "Sauroposeidon", "Titanosaurus", "Paralititan", "Antarctosaurus", "Mamenchisaurus"
    ]

    WATER_ANIMALS = [
        # Tiny (less than 1 foot)
        "Guppy", "Seahorse", "Clownfish", "Shrimp", "Crab", "Starfish", "Sea Urchin", "Jellyfish", "Coral Polyp", "Plankton",
        
        # Small (1-3 feet)
        "Piranha", "Flying Fish", "Angel Fish", "Lobster", "Octopus", "Sea Bass", "Cuttlefish", "Ray", "Eel", "Salmon",
        
        # Medium (3-8 feet)
        "Dolphin", "Tuna", "Barracuda", "Sea Turtle", "Seal", "Manta Ray", "Swordfish", "Sturgeon", "Grouper", "Nurse Shark",
        
        # Large (8-15 feet)
        "Great White Shark", "Tiger Shark", "Hammerhead Shark", "Sea Lion", "Beluga Whale", "Narwhal", "Manatee", "Dugong", "Giant Grouper", "Marlin",
        
        # Huge (15-30 feet)
        "Orca", "Great White Shark", "Saltwater Crocodile", "Giant Pacific Octopus", "Greenland Shark", "Basking Shark", "Megalodon", "Giant Manta Ray", "Oarfish", "Giant Squid",
        
        # Colossal (30-100 feet)
        "Sperm Whale", "Humpback Whale", "Right Whale", "Colossal Squid", "Whale Shark", "Leedsichthys", "Megalodon", "Basilosaurus", "Mosasaurus", "Kronosaurus",
        
        # Gigantic (100+ feet)
        "Blue Whale", "Fin Whale", "Sei Whale", "Brygmophyseter", "Livyatan", "Megalodon (Largest specimens)", "Liopleurodon", "Shastasaurus", "Thalattoarchon", "Shonisaurus"
    ]
    
    CREATURE_SIZES = [
            "Tiny", "Small", "Medium", "Large", "Huge", "Colossal", "Gigantic"
    ]

    CREATURE_TEMPERAMENTS = [
            "Aggressive", "Peaceful", "Territorial", "Friendly", "Hostile", "Neutral", "Protective",
            "Cunning", "Savage", "Docile", "Fearsome"
    ]

    CREATURE_ABILITIES = [
            "Fire-breathing", "Ice-spawning", "Lightning-wielding", "Poison-secreting",
            "Shape-shifting", "Mind-controlling", "Telepathic", "Regenerating", "Flying",
            "Invisible", "Stone-turning gaze", "Water-breathing", "Earth-shaking"
    ]

    CREATURE_FEATURES = [
            "Scales", "Fur", "Feathers", "Chitin", "Spikes", "Horns", "Wings",
            "Multiple heads", "Tentacles", "Claws", "Fangs", "Tail", "Ethereal body"
    ]

    MAGICAL_PROPERTIES = [
            "Elemental power", "Ancient magic", "Cursed", "Blessed", "Soul-stealing",
            "Reality-bending", "Time-manipulating", "Dream-walking", "Nature-controlling"
    ]
    
    # Add this to your SharedLists class
    OBJECTS = [
        "sign",
        "paper",
        "sword",
        "shield",
        "staff",
        "wand",
        "book",
        "scroll",
        "potion",
        "dagger",
        "bow",
        "arrow",
        "spear",
        "axe",
        "hammer",
        "gun",
        "rifle",
        "pistol",
        "camera",
        "phone",
        "laptop",
        "tablet",
        "pen",
        "pencil",
        "notebook",
        "bag",
        "backpack",
        "hat",
        "glasses",
        "watch",
        "ring",
        "necklace",
        "bracelet",
        "umbrella",
        "lantern",
        "torch",
        "map",
        "compass",
        "key",
        "lock",
        "rope",
        "chain",
        "bottle",
        "cup",
        "plate",
        "fork",
        "knife",
        "spoon",
        "guitar",
        "violin",
        "drum",
        "flute",
        "microphone",
        "paintbrush",
        "canvas",
        "sculpture",
        "trophy",
        "medal",
        "flag",
        "banner",
        "crystal",
        "gem",
        "orb",
        "mirror",
        "clock",
        "hourglass",
        "basket",
        "box",
        "chest",
        "coin",
        "card",
        "dice",
        "mask",
        "crown",
        "scepter",
        "throne",
    ]

    # OBJECTS POSE STUFF
    POSE_OBJECT = [
        "holding",
        "carrying",
        "looking at",
        "examining",
        "reaching for",
        "grabbing",
        "lifting",
        "showing",
        "presenting",
        "playing with",
        "manipulating",
        "inspecting",
        "balancing",
        "throwing",
        "catching",
        "offering",
        "wielding",
        "aiming",
        "pointing at",
        "touching"
    ]

    # Style-related lists
    ARTISTIC_STYLES = [
        "photography", "oil painting", "watercolor", "digital art", "pencil sketch", "anime",
        "photorealistic", "comic book", "impressionist", "pop art", "minimalist",
        "concept art", "3D render", "cinematic", "studio photography", "film noir"
    ]

    COLOR_PALETTES = [
        "vibrant", "muted", "monochromatic", "pastel", "dark and moody",
        "warm", "cool", "high contrast", "earthy", "neon",
        "vintage", "black and white", "sepia", "technicolor", "iridescent"
    ]

    LIGHTING_TYPES = [
        "natural", "dramatic", "soft", "harsh", "backlit",
        "rim lighting", "volumetric", "ambient", "studio", "cinematic",
        "golden hour", "blue hour", "neon", "candlelit", "spotlit"
    ]

    MOODS = [
        "peaceful", "mysterious", "dramatic", "romantic", "melancholic",
        "energetic", "serene", "tense", "whimsical", "ethereal",
        "dark", "cheerful", "nostalgic", "dreamy", "epic"
    ]

    COMPOSITIONS = [
        "rule of thirds", "symmetrical", "dynamic", "minimalist", "centered",
        "diagonal", "framed", "leading lines", "golden ratio", "panoramic", "dutch angle"
    ]

    # Scene-related lists
    SCENE_TYPES = [
        "urban", "natural", "fantasy", "sci-fi", "historical",
        "industrial", "domestic", "underwater", "aerial", "space",
        "post-apocalyptic", "medieval", "futuristic", "tropical", "arctic"
    ]

    TIME_PERIODS = [
        "dawn", "morning", "noon", "afternoon", "dusk",
        "night", "midnight", "golden hour", "blue hour", "twilight"
    ]

    WEATHER_CONDITIONS = [
        "clear", "cloudy", "rainy", "stormy", "snowy",
        "foggy", "misty", "windy", "sunny", "overcast",
        "thunderstorm", "hazy", "humid", "frosty", "tropical"
    ]

    AMBIANCE_TYPES = [
        "peaceful", "mysterious", "chaotic", "serene", "bustling",
        "abandoned", "lively", "magical", "dystopian", "utopian",
        "ancient", "modern", "timeless", "ethereal", "supernatural"
    ]

    SETTINGS = [
        "city street", "forest", "beach", "mountains", "desert",
        "castle", "spaceship", "underwater city", "floating islands", "cyberpunk city", "shadow realm", "swamp", "volcano", "arctic", "sky"
        "ancient ruins", "space station", "magical realm", "steampunk world", "parallel dimension",
        "snowy tundra", "volcanic island", "abandoned theme park", "alien planet", "dystopian future",
        "post-apocalyptic wasteland", "enchanted forest", "underworld", "moon base", "faerie kingdom",
        "dreamscape", "mystical cave", "giant's lair", "superhero city", "nuclear wasteland",
        "retro-futuristic city", "medieval village", "ancient library", "time machine interior", "supernatural mansion",
        "dark alleyway", "secret laboratory", "holographic world", "floating city", "temple ruins",
        "hidden jungle", "space colony", "fantasy kingdom", "mythical mountain", "glowing cave",
        "interdimensional rift", "underground bunker", "abandoned subway", "magic academy", "suburban neighborhood",
        "artificial intelligence city", "cybernetic jungle", "world on fire", "parallel universe", "virtual reality landscape",
        "sunken shipwreck", "enchanted castle", "cloud city", "futuristic metropolis", "labyrinthine ruins",
        "swampy marshlands", "toxic wasteland", "magician's tower", "swirling vortex", "ancient temple",
        "tropical island", "underground world", "geothermal spring", "haunted forest", "ice planet",
        "glittering city", "steampunk airship", "spooky mansion", "digital world", "wizard's tower",
        "deserted island", "space-time anomaly", "ancient battlefield", "crystal cavern", "underwater ruins",
        "abandoned military base", "stormy ocean", "mystical oasis", "frozen tundra", "high-tech laboratory",
        "rustic farmhouse", "glowing meadow", "alien jungle", "robot city", "hidden temple",
        "demonic realm", "lost city", "barren wasteland", "moonlit bay", "twisted carnival",
        "vampire's castle", "clockwork world", "intergalactic market", "fantasy battlefield", "sunny meadow",
        "mysterious island", "spaceport", "hacker's lair", "ancient fortress", "robotic wasteland"
    ]

    # BASIC COLORS / OUTFITS
    BASIC_COLORS = [
        "black", "white", "grey"
    ]

    COLORS = [
        "black", "white", "grey", "red", "crimson", "scarlet", "burgundy", "pink",
        "rose", "purple", "violet", "lavender", "blue", "navy", "sky", "cyan", "teal",
        "green", "emerald", "lime", "yellow", "gold", "orange", "brown", "tan",
        "beige", "silver", "metallic", "transparent"
    ]

    STYLES = [
        "casual", "formal", "business", "streetwear", "athletic", "fantasy", "sci-fi",
        "historical", "military", "punk", "gothic", "bohemian", "minimal", "elegant",
        "vintage", "grunge", "preppy", "romantic", "avant-garde", "cyberpunk",
        "steampunk", "lolita", "kawaii"
    ]

    MALE_OUTFITS = {
        "TOPS": [
            "t-shirt", "button-up shirt", "sweater", "hoodie", "tank top", "dress shirt",
            "polo shirt", "blazer", "suit jacket", "military jacket", "bomber jacket",
            "windbreaker", "leather jacket", "v-neck shirt", "long sleeve shirt", "henley",
            "cardigan", "flannel shirt", "sweatshirt", "puffer jacket", "parka", "fleece jacket",
            "chambray shirt", "duster coat", "peacoat", "raincoat", "golf shirt", "thermal shirt",
            "polo neck", "crew neck shirt", "sherpa jacket"
        ],
        "BOTTOMS": [
            "jeans", "slacks", "trousers", "cargo pants", "dress pants",
            "shorts", "bermudas", "joggers", "track pants", "denim shorts",
            "chinos", "bootcut jeans", "skinny jeans", "wide leg pants", "sweatpants",
            "overalls", "corduroys", "leather pants", "high-waisted pants", "capris",
            "harem pants", "biker shorts"
        ],
        "OUTERWEAR": [
            "trench coat", "overcoat", "parka", "rain jacket", "varsity jacket",
            "bomber jacket", "military jacket", "denim jacket", "pea coat", "blazer",
            "puffer jacket", "windbreaker", "leather jacket", "duster coat", "chore jacket",
            "chanel-style jacket", "fleece jacket", "work jacket", "polo jacket", "cardigan sweater"
        ],
        "FOOTWEAR": [
            "sneakers", "oxford shoes", "loafers", "dress shoes", "chelsea boots",
            "combat boots", "derby shoes", "slip-ons", "work boots", "flip-flops",
            "boat shoes", "moccasins", "brogues", "athletic shoes", "high-top sneakers",
            "running shoes", "sandals", "hiking boots", "desert boots", "chukka boots"
        ],
        "HEAD_ITEMS": [
            "fedora", "beanie", "baseball cap", "bucket hat", "cowboy hat",
            "wide-brim hat", "trilby", "visor hat", "boater hat", "newsboy cap",
            "flat cap", "snapback", "wool hat", "straw hat", "trapper hat",
            "panama hat", "military cap", "pork pie hat", "safari hat", "top hat",
            "bowler hat", "aviator cap", "hunting cap", "hard hat", "beret",
            "biker helmet", "sports helmet", "skull cap", "headband", "durag"
        ],
        "EYE_ITEMS": [
            "sunglass", "aviator", "wayfarer", "retro sunglass", "polarized sunglass",
            "goggle", "tactical goggle", "steampunk goggle", "visor cap", "sun visor"
        ],
        "MOUTH_ITEMS": [
            "bandana", "scarf", "neck gaiter", "face shield", "welding mask",
            "leather face cover", "decorative mask", "minimalist eyemask",
            "balaclava", "safari scarf"
        ],
        "ACCESSORIES": [
            "watch", "tie", "bow tie", "hat", "cap", "scarf", "belt", "backpack"
        ]
    }

    FEMALE_OUTFITS = {
        "TOPS": [
            "t-shirt", "shirt", "sweater", "hoodie", "tank top", "dress shirt",
            "button-up shirt", "turtleneck", "polo shirt", "blazer", "suit jacket",
            "military jacket", "bomber jacket", "windbreaker", "leather jacket",
            "v-neck shirt", "long sleeve shirt", "henley", "cardigan", "flannel shirt",
            "sweatshirt", "crop top", "puffer jacket", "parka", "fleece jacket",
            "chambray shirt", "duster coat", "peacoat", "raincoat", "golf shirt",
            "thermal shirt", "polo neck", "crew neck shirt", "kimono", "sherpa jacket",
            "bra", "bralette", "sports bra", "bikini top", "corset", "bustier", "lingerie",
            "silk robe", "lace top", "camisole", "pajama set"
        ],
        "BOTTOMS": [
            "jeans", "slacks", "trousers", "cargo pants", "dress pants",
            "shorts", "bermudas", "joggers", "track pants", "denim shorts", "leggings",
            "chinos", "bootcut jeans", "skinny jeans", "wide leg pants",
            "palazzo pants", "paperbag waist pants", "sweatpants", "overalls", "corduroys",
            "leather pants", "high-waisted pants", "capris", "harem pants", "biker shorts",
            "denim skirt", "pencil skirt", "midi skirt", "maxi skirt", "mini skirt",
            "A-line skirt", "pleated skirt", "skorts", "skater skirt",
            "panties", "boyshorts", "thong", "denim thong", "mesh shorts", "leather shorts",
            "lace shorts", "see-through leggings", "cut-off shorts", "ripped jeans", "chamois pants",
            "vinyl pants", "sequined pants", "jogger shorts", "spandex shorts", "tight leather pants",
            "short shorts", "cheeky shorts", "bandage skirt", "faux leather skirt", "leather mini skirt",
            "latex pants", "harness pants", "motorcycle pants", "cargo shorts", "tactical pants",
            "fishnet stockings", "lace stockings", "thigh-high stockings", "sheer stockings",
            "fishnet tights", "mesh stockings", "over-the-knee stockings", "suspender stockings",
            "wet-look leggings", "latex stockings", "lace garter belt", "silk stockings"
        ],
        "DRESSES": [
            "dress", "sundress", "wrap dress", "cocktail dress", "evening gown", "princess dress",
            "babydoll dress", "bodycon dress", "shift dress", "maxi dress", "midi dress", "mini dress",
            "A-line dress", "sheath dress", "high-low dress", "peplum dress", "skater dress",
            "halter dress", "strapless dress", "tunic dress", "ball gown", "lace dress", "chiffon dress",
            "t-shirt dress", "denim dress", "floral dress", "knit dress", "sweater dress"
        ],
        "FULL_BODY_CLOTHES": [
            "jumpsuit", "romper", "playsuit", "catsuit", "bodysuit", "unitard", "leotard",
            "overalls", "dungarees", "boilersuit", "flight suit", "ski suit", "wetsuit",
            "onesie", "palazzo jumpsuit", "culotte jumpsuit", "denim jumpsuit",
            "utility jumpsuit", "wide-leg jumpsuit", "sleeveless jumpsuit", "halter jumpsuit",
            "strapless jumpsuit", "lace jumpsuit", "satin jumpsuit", "velvet jumpsuit",
            "corset bodysuit", "mesh bodysuit", "long sleeve bodysuit", "turtleneck bodysuit",
            "backless bodysuit", "dance leotard", "gymnastics leotard"
        ],
        "OUTERWEAR": [
            "cape", "shawl", "fur coat", "duffle coat", "trench coat", "puffer jacket", "parka",
            "pea coat", "blazer", "cardigan", "bolero jacket", "duster", "raincoat", "cloak",
            "leather jacket", "denim jacket", "military jacket", "bomber jacket", "oversized coat",
            "chanel-style jacket", "teddy coat", "long coat", "cropped jacket", "poncho", "cardigan sweater",
            "fur stole", "capelet", "fur-lined coat"
        ],
        "FOOTWEAR": [
            "pumps", "stilettos", "kitten heels", "block heels", "thigh-high boots",
            "ballet shoes", "sandals", "sneakers", "oxford shoes", "loafers", "dress shoes",
            "chelsea boots", "combat boots", "derby shoes", "slip-ons", "work boots",
            "flip-flops", "boat shoes", "moccasins", "brogues", "athletic shoes",
            "high-top sneakers", "running shoes", "hiking boots", "desert boots", "chukka boots"
        ],
        "HEAD_ITEMS": [
            "sun hat", "fedora", "beanie", "beret", "baseball cap",
            "bucket hat", "cloche hat", "cowboy hat", "wide-brim hat", "trilby",
            "visor hat", "boater hat", "newsboy cap", "turban", "headscarf",
            "wool hat", "straw hat", "trapper hat", "pillbox hat", "panama hat",
            "hijab", "bonnet", "snapback", "hat with veil", "knit hat",
            "fascinator", "skull cap", "safari hat", "military cap", "pork pie hat",
            "flower crown", "tiara", "crystal headpiece", "pearl-embellished hat", 
            "feathered fascinator"
        ],
        "EYE_ITEMS": [
            "sunglass", "cat-eye sunglass", "aviator", "oversized sunglass", 
            "heart-shaped sunglass", "eyemask", "lace mask", "rhinestone-studded mask",
            "gold-rimmed sunglass", "retro goggle", "fashion visor"
        ],
        "MOUTH_ITEMS": [
            "face veil", "mesh face cover", "choker with attached veil", "surgical face mask"
        ],
        "ACCESSORIES": [
            "necklace", "earrings", "bracelet", "rings", "tiara", "crown",
            "clutch", "handbag", "hair clips", "choker"
        ]
    }

    COSPLAY = {
        "MALE": [
            {"name": "Naruto Uzumaki",
                "description": "Orange jumpsuit with black accents, headband with leaf symbol."},
            {"name": "Geralt of Rivia",
                "description": "Dark leather armor, steel sword, and silver sword strapped to the back."},
            {"name": "Cloud Strife",
                "description": "Sleeveless navy top, black pants, and iconic large Buster Sword."},
            {"name": "Goku", "description": "Orange martial arts gi with blue belt, boots, and wristbands."},
            {"name": "Link", "description": "Green tunic, brown belt, and pointed hat with leather boots."},
            {"name": "Darth Vader",
                "description": "Black armored suit with cape and helmet, iconic red lightsaber."},
            {"name": "Captain America",
                "description": "Blue suit with white star on chest, red and white stripes, and shield."},
            {"name": "Iron Man",
                "description": "Red and gold armored suit with glowing arc reactor."},
            {"name": "Luffy", "description": "Red open shirt, blue shorts, yellow sash, and straw hat."},
            {"name": "Spider-Man",
                "description": "Red and blue spandex suit with black web patterns and spider emblem."}
        ],"FEMALE": [
            {"name": "Sailor Moon",
                "description": "White sailor-style top with blue pleated skirt and red bow."},
            {"name": "Princess Leia",
                "description": "White flowing dress with a high neckline, and iconic side-buns hairstyle."},
            {"name": "Elsa",
                "description": "Blue sparkling gown with sheer cape and icy details."},
            {"name": "Tifa Lockhart",
                "description": "White tank top, black skirt with suspenders, gloves, and boots."},
            {"name": "Lara Croft",
                "description": "Tank top, cargo shorts, combat boots, and gun holsters."},
            {"name": "Asuka Langley",
                "description": "Red pilot suit with futuristic armor details."},
            {"name": "Harley Quinn",
                "description": "Red and black diamond-patterned outfit, with pigtails and a mallet."},
            {"name": "Wonder Woman",
                "description": "Gold armor with red bodice, blue skirt, and lasso of truth."},
            {"name": "Zero Two",
                "description": "Red military-style jumpsuit with white accents and horns."},
            {"name": "Mikasa Ackerman",
                "description": "Brown jacket, white scarf, and beige pants with leather harness."},
            {"name": "Yennefer of Vengerberg",
                "description": "Black corset, leather pants, and a fur-trimmed cloak with magical accessories."},
            {"name": "Ciri",
                "description": "Light armor with a white shirt, brown gloves, and a silver sword."},
            {"name": "Ryuko Matoi",
                "description": "Black and red sailor uniform with a scissor blade."},
            {"name": "Hatsune Miku",
                "description": "Aqua twin-tails, futuristic gray and teal outfit with musical accessories."},
            {"name": "Samus Aran",
                "description": "Metallic blue Zero Suit with sleek designs and a blaster."},
            {"name": "Bulma",
                "description": "Colorful casual outfit with a utility belt, and pink 'BULMA' dress from Dragon Ball."},
            {"name": "Nezuko Kamado",
                "description": "Pink kimono with geometric patterns, bamboo mouthpiece, and a black cloak."},
            {"name": "Hinata Hyuga",
                "description": "Lavender jacket, black ninja pants, and her unique white eyes."},
            {"name": "Korra",
                "description": "Blue Water Tribe outfit with arm bracers and boots."},
            {"name": "Bayonetta",
                "description": "Black skin-tight suit with intricate details, glasses, and pistols for heels."},
            {"name": "Aerith Gainsborough",
                "description": "Pink dress with red jacket and a staff."},
            {"name": "Android 18",
                "description": "Blue denim jacket, striped shirt, black pants, and boots."},
            {"name": "Raven",
                "description": "Dark blue cloak, black leotard, and mystical red gemstone accents."},
            {"name": "Sakura Haruno",
                "description": "Red sleeveless dress with pink hair and ninja gloves."},
            {"name": "D.Va",
                "description": "Blue and pink mech pilot jumpsuit with gaming headphones."},
            {"name": "Sheik",
                "description": "Stealthy ninja-like outfit with wrapped fabrics and a harp."},
            {"name": "Zelda",
                "description": "Elegant white and purple royal dress with gold armor accents."},
            {"name": "Ada Wong",
                "description": "Red dress, black heels, and handgun accessories."},
            {"name": "Jean Grey",
                "description": "Green and gold bodysuit with a fiery Phoenix emblem."}
        ]
    }

    FACIAL_HAIR_TYPES = [
        # General styles
        "clean-shaven", "stubble", "light stubble", "heavy stubble",
        # Mustaches
        "pencil mustache", "handlebar mustache", "horseshoe mustache", "walrus mustache",
        "chevron mustache", "toothbrush mustache", "English mustache",
        # Beards
        "goatee", "chinstrap beard", "soul patch", "balbo beard",
        "Van Dyke beard", "full beard", "ducktail beard", "bandholz beard",
        "Garibaldi beard", "short boxed beard", "Verdi beard",
        # Sideburns
        "mutton chops", "friendly mutton chops", "burnsides mustache",
        # Specialty
        "anchor beard", "imperial beard"
    ]

    ASS_SHAPES = [
        # Size-based
        "tiny", "small", "medium", "large", "very large", "extremely large",
        # Shape-based
        "round", "heart shaped", "bubble", "pear shaped", "square",
        # Position/angle
        "high set", "low set", "outward facing", "inward facing",
        # Firmness/composition
        "firm", "soft", "muscular", "toned"
    ]

    BREAST_SHAPES = [
        # Size-based
        "tiny", "small", "medium", "large", "very large", "extremely large",
        # Shape-based
        "round", "teardrop", "bell shaped", "conical",
        # Position/spacing
        "wide set", "close set", "high set", "low set",
        # Firmness/composition
        "firm", "soft", "perky", "saggy"
    ]

    MATERIALS = [
        "cotton", "wool", "silk", "linen", "cashmere",
        "polyester", "nylon", "spandex", "leather", "latex",
        "velvet", "satin", "lace", "mesh", "tulle",
        "denim", "tweed", "chiffon", "latex"
    ]

    PATTERNS = [
        "solid", "striped", "plaid", "checkered", "polka dot",
        "floral", "animal print", "camouflage", "paisley", "tropical",
        "geometric", "abstract", "chevron", "diamond", "hexagonal",
        "tie-dye", "ombre", "gradient", "glitter", "holographic",
        "psychedelic", "optical illusion", "digital print",
        "herringbone", "houndstooth", "argyle", "tartan", "pinstripe"
    ]

    STYLE_DETAILS = [
        "fitted", "loose", "oversized", "skin-tight", "baggy",
        "layered", "asymmetric", "structured", "flowing", "draped",
        "distressed", "ripped", "frayed", "patched", "embellished",
        "studded", "buckled", "zipped", "laced", "buttoned"
    ]

    # Character-related lists
    POSITIONS = [
        "left", "center", "right", "top", "bottom",
        "top-left", "top-right", "bottom-left", "bottom-right"
    ]

    ETHNICITIES = {
        "MALE": [
            {"name": "Asian", "description": "Strong jawline, straight black hair, broad shoulders, defined cheekbones, often with monolid eyes and athletic build."},
            {"name": "Caucasian", "description": "Fair skin, strong facial features, height ranging from average to tall, facial hair potential from clean-shaven to full beard."},
            {"name": "African", "description": "Wide range of rich dark skin tones, strong facial bone structure, athletic build, various hair textures from tight coils to waves."},
            {"name": "Latino", "description": "Warm olive to brown skin, strong jawline, dark hair, prominent features, athletic to stocky build."},
            {"name": "Middle Eastern", "description": "Olive skin, thick dark hair, prominent nose, strong eyebrows, athletic build with facial hair ranging from stubble to full beard."},
            {"name": "Indian", "description": "Brown skin tones, defined features, thick black hair, strong brow, athletic to stocky build."},
            {"name": "Nord", "description": "Towering muscular build, pale skin, braided blonde or red hair, ice-blue eyes, frost-resistant features, war paint and runic tattoos."},
            {"name": "Argonian", "description": "Muscular reptilian humanoid, earth to bright-colored scales, prominent horns, spined crest, powerful tail, amber eyes with vertical pupils."},
            {"name": "Khajiit", "description": "Feline features with striped/spotted fur patterns, muscular build, retractable claws, cat-like eyes, long agile tail."},
            {"name": "High Elf", "description": "Exceptionally tall and broad-shouldered, golden skin, sharp angular features, long pointed ears, commanding presence."},
            {"name": "Dark Elf", "description": "Athletic build with ashen grey skin, intense red eyes, tribal scarification, sharp features, white hair."},
            {"name": "Drow", "description": "Obsidian black skin, stark white hair, muscular build, noble bearing, glowing red/purple eyes, sharp features."},
            {"name": "Orc", "description": "Massive muscular frame, green/grey skin, prominent tusks, fierce eyes, battle scars, tribal markings."},
            {"name": "Dwarf", "description": "Stocky powerful build, thick braided beard, weathered features, broad chest, intricate armor decorations."},
            {"name": "Dragonborn", "description": "Towering draconic humanoid, metallic/chromatic scales, horned crest, powerful tail, intimidating presence."},
            {"name": "Tiefling", "description": "Demonic features, curved horns, long tail, skin ranging from deep red to purple, golden eyes, athletic build."},
            {"name": "Aasimar", "description": "Celestial heritage, metallic-tinged skin, glowing eyes, muscular build, faint halo effect, luminous markings."},
            {"name": "Warforged", "description": "Powerful mechanical construct, metal/wood/stone plating, glowing runes, crystalline eyes, imposing frame."},
            {"name": "Na'vi", "description": "Tall athletic build, blue striped skin, large golden eyes, pointed ears, long tail, tribal markings and beads."},
            {"name": "Protoss", "description": "Tall warrior build, golden/blue skin, no mouth, glowing eyes, psychic appendages, ceremonial armor."},
            {"name": "Vulcan", "description": "Tall stature, pointed ears, slanted eyebrows, olive skin, disciplined bearing, logical expression."},
            {"name": "Tabaxi", "description": "Agile feline humanoid, spotted fur patterns, athletic build, keen eyes, long balanced tail."},
            {"name": "Goliath", "description": "Massive muscular frame, stone-like skin, tribal tattoos, calculated movements, intimidating presence."},
            {"name": "Minotaur", "description": "Hulking bull-headed humanoid, powerful horns, muscular build, thick fur, fierce demeanor."}
        ],
        "FEMALE": [
            {"name": "Asian", "description": "Delicate features, silky straight black hair, high cheekbones, graceful bearing, often with monolid eyes."},
            {"name": "Caucasian", "description": "Fair skin, variety of hair colors, refined features, height ranging from petite to tall."},
            {"name": "African", "description": "Rich dark skin tones, elegant facial structure, diverse hair textures from tight coils to flowing waves."},
            {"name": "Latina", "description": "Warm olive to brown skin, flowing dark hair, expressive eyes, graceful features."},
            {"name": "Middle Eastern",
                "description": "Olive skin, long dark hair, defined eyebrows, almond-shaped eyes, elegant features."},
            {"name": "Indian", "description": "Brown skin tones, long thick black hair, delicate features, expressive eyes."},
            {"name": "Nord", "description": "Tall athletic build, pale skin, long braided blonde or red hair, ice-blue eyes, elegant war paint."},
            {"name": "Argonian", "description": "Sleek reptilian humanoid, iridescent scales, graceful horns, feathered crest, lithe tail."},
            {"name": "Khajiit", "description": "Elegant feline features, soft fur patterns, nimble build, bright eyes, long graceful tail."},
            {"name": "High Elf", "description": "Tall and graceful, golden skin, ethereal features, long pointed ears, regal bearing."},
            {"name": "Dark Elf", "description": "Lithe build with ashen skin, striking red eyes, flowing white hair, elegant scarification."},
            {"name": "Drow", "description": "Obsidian black skin, flowing white hair, ethereal grace, glowing eyes, aristocratic features."},
            {"name": "Orc", "description": "Athletic build, green/grey skin, small tusks, fierce beauty, elegant tribal markings."},
            {"name": "Dwarf", "description": "Strong compact build, intricate braided hair, determined features, ornate accessories."},
            {"name": "Dragonborn", "description": "Elegant draconic humanoid, shimmering scales, graceful horns, powerful presence."},
            {"name": "Tiefling", "description": "Exotic features, delicate horns, slender tail, skin from crimson to violet, hypnotic eyes."},
            {"name": "Aasimar", "description": "Divine beauty, metallic-sheened skin, radiant eyes, ethereal presence, glowing marks."},
            {"name": "Warforged", "description": "Elegant mechanical form, smooth plating, flowing runes, crystalline eyes, graceful frame."},
            {"name": "Na'vi", "description": "Tall slender build, luminescent blue skin, large amber eyes, pointed ears, decorated tail."},
            {"name": "Protoss", "description": "Tall elegant build, luminous skin, no mouth, glowing eyes, flowing psychic cords."},
            {"name": "Vulcan", "description": "Graceful stature, pointed ears, arched eyebrows, olive skin, composed bearing."},
            {"name": "Tabaxi", "description": "Lithe feline humanoid, elegant fur patterns, fluid movement, bright eyes, long tail."},
            {"name": "Goliath", "description": "Tall athletic frame, stone-like skin, flowing tribal marks, powerful grace."},
            {"name": "Minotaur", "description": "Strong bull-headed humanoid, curved horns, athletic build, fierce elegance."}
        ]
    }

    NATIONALITIES = [
        # Asian
        "Chinese", "Japanese", "Korean", "Mongolian", "Vietnamese",
        "Thai", "Filipino", "Indonesian", "Malaysian", "Singaporean",
        "Nepalese", "Bhutanese", "Cambodian", "Laotian",

        # Caucasian (European & some neighboring regions)
        "French", "German", "Italian", "Spanish", "Portuguese",
        "Russian", "Ukrainian", "Polish", "Norwegian", "Swedish",
        "Finnish", "Danish", "Dutch", "Austrian", "Greek", "Icelandic",
        "Scottish", "Welsh", "English", "Irish", "Hungarian",
        "Swiss", "Belgian", "Czech", "Slovak", "Serbian",
        "Croatian", "Bulgarian", "Romanian", "Macedonian", "Latvian",
        "Lithuanian", "Estonian", "Georgian", "Armenian", "Moldovan",

        # African
        "Nigerian", "Ethiopian", "South African", "Kenyan", "Tanzanian",
        "Ugandan", "Somali", "Sudanese", "Egyptian", "Algerian",
        "Moroccan", "Ghanaian", "Congolese", "Rwandan", "Zimbabwean",
        "Senegalese", "Malian", "Ivory Coast (Ivorian)", "Botswanan",
        "Namibian", "Chadian", "Tunisian", "Libyan",

        # Latino (Hispanic/Latinx)
        "Mexican", "Argentinian", "Colombian", "Peruvian", "Chilean",
        "Venezuelan", "Ecuadorian", "Guatemalan", "Bolivian",
        "Uruguayan", "Honduran", "Cuban", "Panamanian",
        "Puerto Rican", "Costa Rican", "Dominican", "Salvadoran",
        "Paraguayan",

        # Middle Eastern
        "Turkish", "Persian (Iranian)", "Arabian (Saudi)",
        "Iraqi", "Syrian", "Lebanese", "Jordanian",
        "Israeli", "Palestinian", "Kuwaiti", "Emirati",
        "Omani", "Yemeni", "Qatari", "Bahraini",

        # Indian Subcontinent
        "Indian", "Pakistani", "Bangladeshi", "Sri Lankan",
        "Maldivian",

        # Others
        "Australian", "New Zealander (Kiwi)", "Papua New Guinean",
        "Native Hawaiian", "Inuit", "Samoan", "Tongan",
        "Fijian", "Maori", "Caribbean (specific islands can be listed)"
    ]

    ARMORS = [
        # Prehistoric
        "Bone Armor", "Wooden Plate Armor", "Reed Armor", "Stone-Studded Armor",
        "Animal Hide Armor", "Fiber-Woven Armor", "Primitive Scale Armor",

        # Ancient
        "Bronze Armor", "Linothorax Armor", "Scale Armor",
        "Lamellar Armor", "Greek Hoplite Armor", "Assyrian Iron Armor",
        "Roman Lorica Segmentata", "Persian Sparabara Armor",
        "Celtic Chainmail Armor", "Etruscan Bronze Plate Armor",
        "Egyptian Leather Scale Armor", "Hittite Bronze Scale Armor",

        # Medieval
        "Chainmail Armor", "Gambeson Armor", "Plate Armor",
        "Brigandine Armor", "Knight's Full Plate Armor",
        "Padded Armor", "Boiled Leather Armor", "Splint Armor",
        "Scale Hauberk Armor", "Mail-and-Plate Armor", "Kozane Samurai Armor",
        "Coat of Plates", "Crusader Surcoat Armor", "Byzantine Lamellar Armor",
        "Norman Hauberk Armor", "Viking Chainmail Armor",

        # Renaissance
        "Maximilian Armor", "Cuirassier Armor", "Half-Plate Armor",
        "Tournament Plate Armor", "Polish Hussar Winged Armor",
        "Blackened Plate Armor", "Landsknecht Armor",

        # Samurai and East Asian
        "O-Yoroi Samurai Armor", "Do-Maru Armor", "Han Chinese Lamellar Armor",
        "Mongol Lamellar Armor", "Tibetan Lamellar Armor",
        "Qing Dynasty Brigandine Armor", "Korean Brigandine Armor",
        "Japanese Tatami Armor", "Ryukyuan Gusuku Armor",
        "Vietnamese Lacquered Lamellar Armor", "Shikoro Armor",

        # Indigenous
        "Aztec Cotton Armor", "Inca Quilted Armor",
        "Native American Rawhide Armor", "Maori Woven Flax Armor",
        "Zulu Cowhide Shield Armor", "Iroquois Wooden Slat Armor",
        "Tupi Feathered Armor", "Pacific Islander Coconut Fiber Armor",

        # Modern Military/Steampunk
        "Ballistic Armor", "Kevlar Armor", "Exoskeleton Armor",
        "Powered Combat Armor", "Steampunk Brass Armor",
        "Dieselpunk Mechanized Armor", "Ceramic Plate Armor",
        "Carbon Fiber Combat Armor", "Graphene-Layered Armor",
        "Liquid Armor Suit", "Bulletproof Combat Suit",
        "Advanced Riot Control Armor",

        # Sci-Fi
        "Power Armor", "Energy Shield Armor", "Mech Armor",
        "Nanobot Weave Armor", "Plasma Reflective Armor",
        "Force Field Armor", "Stealth Camouflage Armor",
        "Cryo-Resistant Armor", "Magnetic Repulsion Armor",
        "Bio-Augmented Armor", "Gravity-Dampening Armor",
        "Photon Deflection Armor", "Plasma Shielded Suit",
        "Radiation-Absorbing Armor", "Zero-Gravity Combat Armor",
        "Neutron-Repellent Armor", "AI-Assisted Combat Suit",
        "Self-Healing Nano Armor", "Quantum Phase Armor",

        # Fantasy
        "Dragonbone Plate Armor", "Elven Chainmail Armor", "Dwarven Forge Plate Armor",
        "Shadow Silk Armor", "Runed Mithril Plate Armor", "Obsidian Plate Armor",
        "Crystal Armor", "Chitin Armor", "Demonforged Plate Armor",
        "Phoenix Feather Armor", "Hydra Scale Armor", "Lichlord's Bone Armor",
        "Stoneskin Plate Armor", "Celestial Radiance Armor",
        "Voidwalker Armor", "Bloodsteel Armor", "Frostforged Plate Armor",
        "Stormshard Armor", "Ethereal Woven Armor", "Spectral Plate Armor",
        "Wyrmscale Armor", "Aegis of the Eternal Flame", "Thornwood Plate Armor",
        "Silverlight Plate Armor", "Magus Enchanted Armor"
    ]

    UNIFORMS = [
        # Prehistoric and Tribal
        "Hunter-Gatherer Outfit", "Shaman Ritual Uniform", "Tribal War Paint Uniform",
        "Ceremonial Animal Skin Robe",

        # Ancient
        "Roman Legionary Uniform", "Spartan Hoplite Uniform", "Egyptian Priest Uniform",
        "Persian Immortal Uniform", "Assyrian Archer Uniform", "Greek Charioteer Uniform",
        "Macedonian Phalanx Uniform", "Celtic Warrior Uniform", "Babylonian Scholar Robe",

        # Medieval
        "Knight's Heraldic Tabard", "Monastic Robe Uniform", "Feudal Lord's Court Uniform",
        "Squire's Training Garb", "Medieval Peasant Work Uniform",
        "Crusader Knight Uniform", "Medieval Merchant's Outfit",
        "Plague Doctor's Uniform", "Jester's Costume Uniform",
        "Court Minstrel Attire", "Tournament Jousting Tabard",

        # Renaissance
        "Renaissance Merchant Uniform", "Italian City-State Militia Uniform",
        "Landsknecht Soldier Uniform", "French Musketeer Uniform",
        "English Longbowman Uniform", "Renaissance Painter's Robe",
        "Spanish Conquistador Uniform", "Royal Courtier Uniform",
        "Renaissance Scholar Gown", "Genoese Sailor Uniform",

        # Early Modern
        "Napoleonic Infantry Uniform", "British Redcoat Uniform",
        "French Revolutionary Guard Uniform", "American Continental Army Uniform",
        "Pirate Captain's Uniform", "Privateer's Garb",
        "East India Company Officer Uniform", "Spanish Armada Naval Uniform",
        "Russian Imperial Guard Uniform", "Prussian Hussar Uniform",
        "Ming Dynasty Imperial Guard Uniform", "Ottoman Janissary Uniform",

        # Victorian and Industrial
        "Victorian Policeman Uniform", "Industrial Revolution Factory Worker Uniform",
        "Victorian Nurse's Uniform", "British Officer Uniform",
        "Railroad Conductor Uniform", "Steampunk Engineer Uniform",
        "Victorian Schoolteacher Gown", "Steamship Captain's Uniform",
        "Circus Ringmaster Costume", "Victorian Fire Brigade Uniform",

        # Modern Military
        "World War I Infantry Uniform", "World War II Aviator Uniform",
        "Modern Army Combat Uniform (ACU)", "Marine Corps Dress Blues",
        "Navy SEAL Tactical Uniform", "Air Force Flight Suit",
        "Ghillie Suit (Sniper Uniform)", "UN Peacekeeper Uniform",
        "Special Forces Urban Combat Uniform", "Paratrooper Uniform",
        "Artillery Officer Dress Uniform", "Submarine Crew Uniform",
        "Desert Camo Uniform", "Arctic Survival Uniform",

        # Professional
        "Police Officer Uniform", "Firefighter Turnout Gear",
        "Paramedic Emergency Uniform", "Chef's Whites",
        "Doctor's Scrubs", "Nurse's Scrubs", "Mechanic's Coveralls",
        "Pilot's Flight Suit", "Train Engineer's Uniform",
        "Hotel Bellhop Uniform", "Mail Carrier Uniform",
        "Corporate Security Guard Uniform", "Construction Worker Safety Gear",
        "Factory Worker Uniform", "Judge's Robes",
        "Waiter's Service Uniform", "Clergy Vestments",

        # Academic and Sports
        "Graduation Cap and Gown", "School Uniform", "Sports Team Jersey",
        "Fencing Gear", "Karate Gi", "Football Quarterback Uniform",
        "Track and Field Athlete Uniform", "Cyclist Uniform",
        "Baseball Player Uniform", "Basketball Player Uniform",

        # Sci-Fi
        "Starfleet Officer Uniform", "Space Marine Combat Suit",
        "Alien Diplomatic Uniform", "Colonial Space Miner Outfit",
        "Zero-Gravity Technician Uniform", "Cyberpunk Hacker Attire",
        "Deep Space Pilot Suit", "Galactic Federation Guard Uniform",
        "Synth Overseer Uniform", "Time Traveler's Robe Uniform",

        # Fantasy
        "Elven Ranger's Uniform", "Wizard's Academic Robes",
        "Dwarven Smith's Garb", "Knight-Enchanter Uniform",
        "Royal Guard Uniform", "Dragon Priest's Ceremonial Robe",
        "Necromancer's Robe", "Thieves' Guild Shadow Uniform",
        "Battle Mage Combat Robe", "Assassin's Stealth Outfit",
        "Paladin's Holy Garb", "Forest Guardian Uniform",
        "Alchemist's Laboratory Coat", "Bard's Entertainer Uniform",
        "Vampire Court Uniform", "Warlock's Infernal Robe"
    ]

    AGES_FEMALE = ["baby girl", "girl", "teen girl",
                   "young woman", "woman", "elderly woman"]
    AGES_MALE = ["baby boy", "boy", "teen boy",
                 "young man", "man", "elderly man"]

    SKIN_TONES = [
        "fair", "pale", "medium", "olive", "tan", "dark", "ebony",
        "golden", "rosy", "ruddy", "porcelain", "chocolate", "mahogany",
        "amber", "ivory"
    ]

    EYE_COLORS = [
        "blue", "green", "brown", "hazel", "amber", "grey",
        "violet", "black", "golden", "silver", "turquoise", "aqua",
        "heterochromatic"
    ]

    POSE_CAMERA = [
        "facing camera", "looking away from camera",
        "looking towards camera", "looking past camera", "side glance at camera",
        "avoiding camera", "direct eye contact with camera"
    ]

    POSE_VIEW = [
        "view from the front", "view from the back",
        "view from the side", "view from above", "view from below",
        "three-quarter view", "profile view"
    ]

    POSE_FACE = [
        "smiling", "serious", "laughing", "crying", "angry",
        "neutral", "surprised", "smirking", "winking", "thoughtful",
        "joyful", "flirty", "disgusted", "fearful", "confident", "curious",
        "big wide smile", "closed-mouth smile", "grinning with teeth showing",
        "smirk with one eyebrow raised", "playful wink", "both eyebrows raised in surprise",
        "squinting in skepticism", "eyes wide open in shock", "blowing a kiss",
        "cheeks puffed out", "pursed lips", "sticking tongue out playfully",
        "sticking tongue out and winking", "biting lower lip", "frowning deeply",
        "pout with lower lip pushed out", "teeth clenched in frustration", "grimace",
        "closed eyes with a serene smile", "tears streaming down face", "sniffing back tears",
        "brows furrowed in anger", "scowling", "intense glare",
        "half-smile with eyes looking to the side", "expression of utter boredom",
        "slight frown with head tilted", "narrowed eyes in suspicion", "cheek resting in one hand",
        "laughing with head tilted back", "cheeky grin with eyes squinted", "lip curled in a sneer",
        "tongue sticking out in mock disgust", "face scrunched up in mock anger",
        "confused look with one eyebrow raised", "blinking rapidly in disbelief",
        "mouth open in exaggerated gasp", "biting the inside of cheek",
        "tongue pressed against cheek in thought", "mouth slightly open in awe",
        "nostrils flared in anger", "eyes closed with a broad grin",
        "head tilted with eyes closed in bliss", "half-closed eyes in tiredness",
        "face scrunched in concentration", "eyebrows arched in flirtation",
        "head tilted with lips slightly parted", "chin raised in defiance",
        "rolling eyes dramatically", "wide eyes and mouth open in excitement",
        "lips drawn into a straight line of neutrality", "sucking in cheeks",
        "lip biting with shyness", "lower lip quivering in sadness", "snarling with bared teeth",
        "lips puckered as if blowing", "tongue clicking against teeth",
        "smiling through clenched teeth", "head tilted slightly with soft smile",
        "face tilted downward with eyes looking up", "cheek resting against fist in boredom",
        "glaring intensely while squinting", "eyes tightly shut in frustration",
        "face in an exaggerated yawn", "sneaky grin with eyes darting to the side",
        "mock shock with hands framing face", "head tilted back with mouth wide open in laughter",
        "eyes narrowed with lips curled upwards", "face cringing as if tasting something sour",
        "eyebrows drawn together in determination", "playful tongue between teeth",
        "one eyebrow raised with a small smile", "eyelids fluttering with a dreamy expression",
        "pained expression with eyes closed", "nostrils flared with head tilted back in triumph",
        "terrified wide eyes and mouth agape", "trembling lower lip with tearful eyes",
        "fearful expression with eyebrows high and pulled together",
        "screaming face with mouth wide open and eyes shut tight",
        "face frozen in shock with wide eyes and raised eyebrows",
        "quivering lips with eyes darting nervously", "looking over shoulder with fearful glance",
        "clenched jaw with darting eyes in paranoia",
        "horrified expression with hands covering mouth",
        "gasp of surprise with hands pressed to cheeks",
        "face twisted in agony, teeth bared",
        "face half-hidden in hands in shame", "smirking with lips curled on one side",
        "sneaky smirk with narrowed eyes", "sarcastic smirk with head slightly tilted",
        "eyes narrowed in resentment with tight-lipped smile",
        "mocking smile with exaggerated lip curve", "sad smile with downcast eyes",
        "cautious smile with one eyebrow raised",
        "hesitant expression with eyes glancing sideways",
        "overwhelmed expression with a shaky breath and moist eyes",
        "fearful squinting with head recoiled",
        "deeply worried frown with chin resting on hands",
        "anxious look with lip pressed between teeth",
        "shocked with hand covering one eye and wide open mouth",
        "frantic expression with eyebrows raised and eyes darting around",
        "expression of disbelief with head tilted slightly and a blank stare",
        "teasing grin with head tilted forward",
        "expression of mischief with eyes squinting and tongue peeking out"
    ]

    POSE_ARMS = [
        "one hand in the air", "thumbs up with both hands", "thumbs up with one hand",
        "hands raised above head", "hands behind head", "hands in pockets", "hand on chin",
        "peace sign", "pointing with index finger", "hand on heart", "palm outstretched",
        "hands together in prayer", "hands in front of face", "hand on cheek", "grabbing head",
        "fist raised", "finger on lips", "saluting", "both hands on hips",
        "arms crossed over chest", "hands resting on knees", "hand touching forehead",
        "hands framing face", "fingers spread wide", "one hand on hip",
        "hands clasped together", "hands cupping face", "index fingers touching",
        "hands behind back", "one hand pointing up", "both hands pointing outwards",
        "hand covering one eye", "fingers making a circle", "two hands clasped in front",
        "arms relaxed at sides", "one hand brushing hair back",
        "hand resting on chest", "one hand raised to ear", "both arms out to sides palms up",
        "one hand pinching bridge of nose", "hands making a heart shape",
        "one hand scratching head", "both hands in a 'stop' position",
        "fingers interlocked and stretched outwards", "one hand touching neck",
        "hands making a triangle shape", "one hand rubbing chin", "fingers folded together",
        "both hands in fists held close to chest", "both hands outstretched upwards",
        "hand resting on opposite shoulder", "one hand covering mouth in surprise",
        "arms gesturing a large circle", "hand resting on hip with elbow out",
        "one hand raised with palm outward", "hands together over head in a triangle",
        "one hand casually dangling at the side", "both hands folded behind neck",
        "hands apart and slightly forward as if pushing away",
        "fingers held together in a neutral position", "hands pressed flat together above head",
        "one hand tapping chin thoughtfully", "hands angled outward from waist",
        "hands forming a V-shape", "both arms extended forward with hands open",
        "one hand lightly touching the cheek", "both hands resting on thighs",
        "hands crossed gently over chest", "one hand under chin, head tilted",
        "hands resting calmly at the sides", "fingers of one hand lightly touching wrist",
        "palms pressed flat together in front of chest", "arms crossed over stomach",
        "arms raised with elbows bent", "elbows pointing outward", "arms bent with fists near shoulders",
        "arms extended forward parallel to the ground", "arms outstretched sideways",
        "arms hanging loosely at sides", "elbows tucked in tightly to sides",
        "arms behind back holding opposite elbows", "elbows resting on knees in seated pose"
    ]

    POSE_LEGS = [
        "one foot forward", "standing on tiptoe", "one leg slightly bent", "kick",
        "kicking in the air", "one leg up", "legs crossed while standing", "legs crossed while seated",
        "feet together", "feet apart", "feet wide in a stance", "squatting",
        "foot pointed", "feet in lotus position", "stepping forward", "feet positioned in a lunge",
        "knees bent in a crouch", "running stance with one knee bent", "sprinting stance",
        "marching pose with knees raised", "walking on toes", "side stepping pose",
        "feet raised off ground slightly", "sitting with legs crossed", "sitting with one knee raised",
        "standing on one leg", "knee raised to waist height", "legs bent in fighting stance",
        "legs extended straight in front (seated)", "legs bent inward at knees",
        "one foot crossed behind the other", "one leg extended to the side", "feet in a pigeon-toed stance",
        "knees pressed together", "knees apart in a relaxed seated pose", "legs angled outward in a wide squat",
        "kneeling on one knee", "both knees bent slightly while standing", "legs outstretched in a V shape (seated)",
        "feet touching with knees bent outward (butterfly pose)", "legs held in a figure-four shape while seated",
        "standing with one leg crossed over the other at ankle", "heels raised while knees are bent",
        "one foot angled outward, toes pointed", "toes turned inward while heels apart",
        "one leg stretched back in a dramatic pose", "legs bent to simulate a low crouch"
    ]

    POSE_BODY = [
        "standing", "twisting torso", "body bent forward", "arching back", "leaning to the side", "bending over",
        "flexing muscles", "body turned sideways", "reaching forward", "stretching backwards",
        "half bent", "crouching", "ducking", "laying on stomach", "laying on back",
        "crawling", "squatting with arms outstretched", "sitting with back straight", "rolling body",
        "jump squat", "climbing position", "hanging from something"
    ]

    POSE_HEAD_NECK = [
        "head tilted", "head down", "head up", "looking over shoulder", "looking forward",
        "looking to the side", "head held high", "head resting on hand", "nodding", "shaking head"
    ]
    POSE_DYNAMIC = [
        "running with arms outstretched", "jumping with arms raised", "kicking while running", "dancing with hands in air",
        "spinning", "cartwheel", "flip", "somersault", "leap", "twisting jump", "spinning kick",
        "high jump", "forward roll", "backflip", "front flip", "breakdancing move", "dance pose"
    ]

    POSE_ACTION = [
        "sword fighting stance", "boxing stance", "martial arts pose", "archery stance", "holding a bow",
        "shooting a gun", "throwing something", "catching something", "hitting something", "dodging",
        "pushing", "pulling", "lifting", "picking up", "throwing punch", "guard stance", "block",
        "kickboxing stance", "karate chop", "tai chi", "spinning staff pose", "kung fu pose", "spinning attack"
    ]

    POSE_SITTING = [
        "cross-legged sitting", "legs hanging off edge", "one leg up sitting", "knees bent up sitting",
        "one leg stretched out sitting", "leaning back sitting", "sitting on the floor", "sitting on a chair",
        "sitting with back straight", "sitting with hands on lap"
    ]

    POSE_UNIQUE = [
        "superhero pose", "yoga pose", "lotus position", "zombie walk", "angel pose", "devil pose",
        "ballet pose", "high kick", "spinning fist", "hands over head", "holding a pose for balance",
        "vogue pose", "exaggerated model pose", "stretching arms wide", "standing with one leg raised",
        "hands clasped in front", "elbows out in victory", "hands holding head", "looking up with arms extended",
        "celebrating pose", "stretching backward with arms to sides", "picking up something off the ground",
        "t-rex arms", "hand over eyes shielding from sun", "hands placed firmly on hips", "twist and shout pose",
        "jumping jacks", "dabbing pose", "sitting with hands behind", "leaning forward on knees",
        "swaying arms to music", "bending sideways", "laying sideways"
    ]

    BODY_SHAPES = [
        "athletic", "muscular", "slim", "slender", "petite", "average", "curvy",
        "full-figured", "tall and lean", "short and stocky", "broad-shouldered",
        "narrow-waisted", "hourglass figure", "pear-shaped", "apple-shaped",
        "rectangle-shaped", "diamond-shaped", "toned", "well-built", "lean muscular",
        "bodybuilder physique", "tall", "very tall", "short", "very short",
        "average height", "thin", "skinny", "plump", "heavy-set", "robust",
        "long-legged", "short-legged", "long-waisted", "short-waisted",
        "straight-postured", "broad-chested", "square-shouldered", "round-shouldered",
        "willowy", "statuesque", "compact", "lanky", "lithe", "svelte",
        "sturdy", "delicate", "graceful", "imposing"
    ]

    HAIR_STYLES = [
        "long", "short", "curly", "straight", "wavy", "braided",
        "bald", "buzzcut", "bob", "pixie", "ponytail", "buns", "double ponytail",
        "afro", "dreadlocks", "spiky", "layered", "feathered", "messy",
        "tied-back", "fishtail braid", "french braid", "cornrows", "twists",
        "shaved sides", "undercut", "fade", "pompadour", "quiff",
        "mohawk", "faux hawk", "half-up half-down", "space buns", "ringlets"
    ]

    # Background-related lists
    # ENVIRONMENTS = ["indoor", "outdoor", "urban", "nature", "studio", "space"]

    TIMES_OF_DAY = ["dawn", "morning", "noon", "afternoon", "sunset", "night"]

    WEATHER = ["clear", "cloudy", "rainy", "stormy", "snowy", "foggy"]

    ATMOSPHERES = ["peaceful", "tense", "magical", "mysterious", "romantic"]

    LOCATIONS = [
        "city streets", "forest", "beach", "mountains",
        "desert", "space station"
    ]

    # Camera and style-related lists
    CAMERA_ANGLES = [
        "front view", "side view", "three-quarter view", "back view",
        "bird's eye view", "worm's eye view", "dutch angle", "over-the-shoulder",
        "high angle", "low angle", "eye level", "aerial view", "tilted angle"
    ]

    SHOT_TYPES = [
        "close-up", "medium shot", "full body", "wide shot",
        "extreme close-up", "medium close-up", "medium long shot",
        "long shot", "extreme long shot", "establishing shot"
    ]

    LIGHTING = [
        "natural", "studio", "dramatic", "soft", "harsh",
        "backlit", "atmospheric", "neon", "candlelight"
    ]

    ART_STYLES = [
        "photography", "hyperrealism", "anime", "digital art",
        "oil painting", "watercolor", "sketch", "cyberpunk"
    ]

    ACTIONS = [
        "talking to each other", "fighting", "dancing", "walking together",
        "having dinner", "playing games", "working together", "arguing",
        "celebrating", "performing", "studying", "shopping"
    ]


class TextGeneratorOutfitFemale:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "top": (["NONE", "RANDOM"] + SharedLists.FEMALE_OUTFITS["TOPS"], {"forceInput": False}),
                "COLOR_top": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "bottom": (["NONE", "RANDOM"] + SharedLists.FEMALE_OUTFITS["BOTTOMS"], {"forceInput": False}),
                "COLOR_bottom": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "dress": (["NONE", "RANDOM"] + SharedLists.FEMALE_OUTFITS["DRESSES"], {"forceInput": False}),
                "COLOR_dress": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "full_body": (["NONE", "RANDOM"] + SharedLists.FEMALE_OUTFITS["FULL_BODY_CLOTHES"], {"forceInput": False}),
                "COLOR_full_body": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "footwear": (["NONE", "RANDOM"] + SharedLists.FEMALE_OUTFITS["FOOTWEAR"], {"forceInput": False}),
                "COLOR_footwear": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "head_item": (["NONE", "RANDOM"] + SharedLists.FEMALE_OUTFITS["HEAD_ITEMS"], {"forceInput": False}),
                "COLOR_head_item": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "eye_item": (["NONE", "RANDOM"] + SharedLists.FEMALE_OUTFITS["EYE_ITEMS"], {"forceInput": False}),
                "COLOR_eye_item": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "mouth_item": (["NONE", "RANDOM"] + SharedLists.FEMALE_OUTFITS["MOUTH_ITEMS"], {"forceInput": False}),
                "COLOR_mouth_item": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "accessories": (["NONE", "RANDOM"] + SharedLists.FEMALE_OUTFITS["ACCESSORIES"], {"forceInput": False}),
                "COLOR_accessories": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "armors": (["NONE", "RANDOM"] + SharedLists.ARMORS, {"forceInput": False}),
                "uniforms": (["NONE", "RANDOM"] + SharedLists.UNIFORMS, {"forceInput": False}),
                "material": (["NONE", "RANDOM"] + SharedLists.MATERIALS, {"forceInput": False}),
                "pattern": (["NONE", "RANDOM"] + SharedLists.PATTERNS, {"forceInput": False}),
                "style_details": (["NONE", "RANDOM"] + SharedLists.STYLE_DETAILS, {"forceInput": False}),
                "style": (["NONE", "RANDOM"] + SharedLists.STYLES, {"forceInput": False}),
                "cosplay": (["NONE", "RANDOM"] + [character["name"] for character in SharedLists.COSPLAY["FEMALE"]], {"forceInput": False}),
                "cosplay_description": ("BOOLEAN", {"default": False}),
                "CUSTOM_PROMPT": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("GEN_OUTFIT",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"
    
    def select_value(self, options, current_value, rng):
        if current_value == "RANDOM":
            valid_options = [
                opt for opt in options if opt not in ["RANDOM", "NONE"]]
            return rng.choice(valid_options)
        elif current_value == "NONE":
            return ""
        return current_value

    def generate(self, seed, style, top, COLOR_top, bottom, COLOR_bottom, dress, COLOR_dress, full_body, COLOR_full_body,
                footwear, COLOR_footwear, accessories, COLOR_accessories, material, pattern,
                head_item, COLOR_head_item, mouth_item, COLOR_mouth_item, eye_item, COLOR_eye_item,
                style_details, cosplay, cosplay_description, armors, uniforms, CUSTOM_PROMPT):
        rng = random.Random(seed)

        values = {
            'top': self.select_value(self.INPUT_TYPES()["required"]["top"][0], top, rng),
            'COLOR_top': self.select_value(self.INPUT_TYPES()["required"]["COLOR_top"][0], COLOR_top, rng),
            'bottom': self.select_value(self.INPUT_TYPES()["required"]["bottom"][0], bottom, rng),
            'COLOR_bottom': self.select_value(self.INPUT_TYPES()["required"]["COLOR_bottom"][0], COLOR_bottom, rng),
            'dress': self.select_value(self.INPUT_TYPES()["required"]["dress"][0], dress, rng),
            'COLOR_dress': self.select_value(self.INPUT_TYPES()["required"]["COLOR_dress"][0], COLOR_dress, rng),
            'full_body': self.select_value(self.INPUT_TYPES()["required"]["full_body"][0], full_body, rng),
            'COLOR_full_body': self.select_value(self.INPUT_TYPES()["required"]["COLOR_full_body"][0], COLOR_full_body, rng),
            'footwear': self.select_value(self.INPUT_TYPES()["required"]["footwear"][0], footwear, rng),
            'COLOR_footwear': self.select_value(self.INPUT_TYPES()["required"]["COLOR_footwear"][0], COLOR_footwear, rng),
            'head_item': self.select_value(self.INPUT_TYPES()["required"]["head_item"][0], head_item, rng),
            'COLOR_head_item': self.select_value(self.INPUT_TYPES()["required"]["COLOR_head_item"][0], COLOR_head_item, rng),
            'eye_item': self.select_value(self.INPUT_TYPES()["required"]["eye_item"][0], eye_item, rng),
            'COLOR_eye_item': self.select_value(self.INPUT_TYPES()["required"]["COLOR_eye_item"][0], COLOR_eye_item, rng),
            'mouth_item': self.select_value(self.INPUT_TYPES()["required"]["mouth_item"][0], mouth_item, rng),
            'COLOR_mouth_item': self.select_value(self.INPUT_TYPES()["required"]["COLOR_mouth_item"][0], COLOR_mouth_item, rng),
            'accessories': self.select_value(self.INPUT_TYPES()["required"]["accessories"][0], accessories, rng),
            'COLOR_accessories': self.select_value(self.INPUT_TYPES()["required"]["COLOR_accessories"][0], COLOR_accessories, rng),
            'armors': self.select_value(self.INPUT_TYPES()["required"]["armors"][0], armors, rng),
            'uniforms': self.select_value(self.INPUT_TYPES()["required"]["uniforms"][0], uniforms, rng),
            'material': self.select_value(self.INPUT_TYPES()["required"]["material"][0], material, rng),
            'pattern': self.select_value(self.INPUT_TYPES()["required"]["pattern"][0], pattern, rng),
            'style_details': self.select_value(self.INPUT_TYPES()["required"]["style_details"][0], style_details, rng),
            'style': self.select_value(self.INPUT_TYPES()["required"]["style"][0], style, rng),
            'cosplay': self.select_value(self.INPUT_TYPES()["required"]["cosplay"][0], cosplay, rng),
        }
        
        def add_item_with_color(item, color):
            if item and item != "NONE":
                color_text = f" {color}" if color and color != "NONE" else ""
                return f"{color_text} {item}"
            return None

        desc_parts = []
        if values['style']:
            desc_parts.append(f"{values['style']} style outfit")

        if values['cosplay']:
            selected_cosplay = None
            for category in SharedLists.COSPLAY.values():
                selected_cosplay = next(
                    (character for character in category if character["name"] == values['cosplay']), None)
                if selected_cosplay:
                    break

            if selected_cosplay:
                if cosplay_description:
                    desc_parts.append(
                        f"dressed as {selected_cosplay['name']}, {selected_cosplay['description']}")
                else:
                    desc_parts.append(f"dressed as {selected_cosplay['name']}")

        if values['dress']:
            desc_parts.append(
                f"wearing a{add_item_with_color(values['dress'], values['COLOR_dress'])}")
        else:
            if values['top']:
                desc_parts.append(
                    f"wearing a{add_item_with_color(values['top'], values['COLOR_top'])}")
            if values['bottom']:
                desc_parts.append(
                    f"with{add_item_with_color(values['bottom'], values['COLOR_bottom'])}")

        if values['footwear']:
            desc_parts.append(
                f"wearing{add_item_with_color(values['footwear'], values['COLOR_footwear'])}")
        
        if values['head_item']:
            desc_parts.append(
                f"wearing{add_item_with_color(values['head_item'], values['COLOR_head_item'])}")
        if values['eye_item']:
            desc_parts.append(
                f"wearing{add_item_with_color(values['eye_item'], values['COLOR_eye_item'])}")
        if values['mouth_item']:
            desc_parts.append(
                f"wearing{add_item_with_color(values['mouth_item'], values['COLOR_mouth_item'])}")
            
        if values['full_body']:
            desc_parts.append(
                f"wearing{add_item_with_color(values['full_body'], values['COLOR_full_body'])}")

        if values['armors']:
            desc_parts.append(f"wearing {values['armors']}")
        if values['uniforms']:
            desc_parts.append(f"wearing {values['uniforms']}")

        if values['accessories']:
            desc_parts.append(
                f"accessorized with{add_item_with_color(values['accessories'], values['COLOR_accessories'])}")

        if values['material']:
            desc_parts.append(f"made of {values['material']}")

        if values['pattern']:
            desc_parts.append(f"in a {values['pattern']} pattern")

        if values['style_details']:
            desc_parts.append(f"with {values['style_details']} styling")

        outfit_desc = ", ".join(desc_parts)

        if CUSTOM_PROMPT.strip():
            outfit_desc += f", {CUSTOM_PROMPT.strip()}"

        return (outfit_desc,)

class TextGeneratorOutfitMale:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "top": (["NONE", "RANDOM"] + SharedLists.MALE_OUTFITS["TOPS"], {"forceInput": False}),
                "COLOR_top": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "bottom": (["NONE", "RANDOM"] + SharedLists.MALE_OUTFITS["BOTTOMS"], {"forceInput": False}),
                "COLOR_bottom": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "footwear": (["NONE", "RANDOM"] + SharedLists.MALE_OUTFITS["FOOTWEAR"], {"forceInput": False}),
                "COLOR_footwear": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "head_item": (["NONE", "RANDOM"] + SharedLists.MALE_OUTFITS["HEAD_ITEMS"], {"forceInput": False}),
                "COLOR_head_item": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "eye_item": (["NONE", "RANDOM"] + SharedLists.MALE_OUTFITS["EYE_ITEMS"], {"forceInput": False}),
                "COLOR_eye_item": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "mouth_item": (["NONE", "RANDOM"] + SharedLists.MALE_OUTFITS["MOUTH_ITEMS"], {"forceInput": False}),
                "COLOR_mouth_item": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "accessories": (["NONE", "RANDOM"] + SharedLists.MALE_OUTFITS["ACCESSORIES"], {"forceInput": False}),
                "COLOR_accessories": (["NONE", "RANDOM"] + SharedLists.COLORS, {"forceInput": False}),
                "armors": (["NONE", "RANDOM"] + SharedLists.ARMORS, {"forceInput": False}),
                "uniforms": (["NONE", "RANDOM"] + SharedLists.UNIFORMS, {"forceInput": False}),
                "material": (["NONE", "RANDOM"] + SharedLists.MATERIALS, {"forceInput": False}),
                "pattern": (["NONE", "RANDOM"] + SharedLists.PATTERNS, {"forceInput": False}),
                "style_details": (["NONE", "RANDOM"] + SharedLists.STYLE_DETAILS, {"forceInput": False}),
                "style": (["NONE", "RANDOM"] + SharedLists.STYLES, {"forceInput": False}),
                "cosplay": (["NONE", "RANDOM"] + [character["name"] for character in SharedLists.COSPLAY["MALE"]], {"forceInput": False}),
                "cosplay_description": ("BOOLEAN", {"default": False}),
                "CUSTOM_PROMPT": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("GEN_OUTFIT",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"

    def select_value(self, options, current_value, rng):
        if current_value == "RANDOM":
            valid_options = [opt for opt in options if opt not in ["RANDOM", "NONE"]]
            return rng.choice(valid_options)
        elif current_value == "NONE":
            return ""
        return current_value

    def generate(self, seed, style, top, COLOR_top, bottom, COLOR_bottom, footwear, COLOR_footwear,
                 head_item, COLOR_head_item, eye_item, COLOR_eye_item, mouth_item, COLOR_mouth_item,
                 accessories, COLOR_accessories, material, pattern, style_details, cosplay,
                 cosplay_description, armors, uniforms, CUSTOM_PROMPT):
        rng = random.Random(seed)

        values = {
            'top': self.select_value(self.INPUT_TYPES()["required"]["top"][0], top, rng),
            'COLOR_top': self.select_value(self.INPUT_TYPES()["required"]["COLOR_top"][0], COLOR_top, rng),
            'bottom': self.select_value(self.INPUT_TYPES()["required"]["bottom"][0], bottom, rng),
            'COLOR_bottom': self.select_value(self.INPUT_TYPES()["required"]["COLOR_bottom"][0], COLOR_bottom, rng),
            'footwear': self.select_value(self.INPUT_TYPES()["required"]["footwear"][0], footwear, rng),
            'COLOR_footwear': self.select_value(self.INPUT_TYPES()["required"]["COLOR_footwear"][0], COLOR_footwear, rng),
            'head_item': self.select_value(self.INPUT_TYPES()["required"]["head_item"][0], head_item, rng),
            'COLOR_head_item': self.select_value(self.INPUT_TYPES()["required"]["COLOR_head_item"][0], COLOR_head_item, rng),
            'eye_item': self.select_value(self.INPUT_TYPES()["required"]["eye_item"][0], eye_item, rng),
            'COLOR_eye_item': self.select_value(self.INPUT_TYPES()["required"]["COLOR_eye_item"][0], COLOR_eye_item, rng),
            'mouth_item': self.select_value(self.INPUT_TYPES()["required"]["mouth_item"][0], mouth_item, rng),
            'COLOR_mouth_item': self.select_value(self.INPUT_TYPES()["required"]["COLOR_mouth_item"][0], COLOR_mouth_item, rng),
            'accessories': self.select_value(self.INPUT_TYPES()["required"]["accessories"][0], accessories, rng),
            'COLOR_accessories': self.select_value(self.INPUT_TYPES()["required"]["COLOR_accessories"][0], COLOR_accessories, rng),
            'armors': self.select_value(self.INPUT_TYPES()["required"]["armors"][0], armors, rng),
            'uniforms': self.select_value(self.INPUT_TYPES()["required"]["uniforms"][0], uniforms, rng),
            'material': self.select_value(self.INPUT_TYPES()["required"]["material"][0], material, rng),
            'pattern': self.select_value(self.INPUT_TYPES()["required"]["pattern"][0], pattern, rng),
            'style_details': self.select_value(self.INPUT_TYPES()["required"]["style_details"][0], style_details, rng),
            'style': self.select_value(self.INPUT_TYPES()["required"]["style"][0], style, rng),
            'cosplay': self.select_value(self.INPUT_TYPES()["required"]["cosplay"][0], cosplay, rng),
        }

        def add_item_with_color(item, color):
            if item and item != "NONE":
                color_text = f" {color}" if color and color != "NONE" else ""
                return f"{color_text} {item}"
            return None

        desc_parts = []
        if values['style']:
            desc_parts.append(f"{values['style']} style outfit")

        if values['cosplay']:
            selected_cosplay = None
            for category in SharedLists.COSPLAY.values():
                selected_cosplay = next(
                    (character for character in category if character["name"] == values['cosplay']), None)
                if selected_cosplay:
                    break

            if selected_cosplay:
                if cosplay_description:
                    desc_parts.append(
                        f"dressed as {selected_cosplay['name']}, {selected_cosplay['description']}")
                else:
                    desc_parts.append(f"dressed as {selected_cosplay['name']}")

        if values['top']:
            desc_parts.append(
                f"wearing a{add_item_with_color(values['top'], values['COLOR_top'])}")
        if values['bottom']:
            desc_parts.append(
                f"with{add_item_with_color(values['bottom'], values['COLOR_bottom'])}")

        if values['footwear']:
            desc_parts.append(
                f"wearing{add_item_with_color(values['footwear'], values['COLOR_footwear'])}")

        if values['head_item']:
            desc_parts.append(
                f"wearing{add_item_with_color(values['head_item'], values['COLOR_head_item'])}")
        if values['eye_item']:
            desc_parts.append(
                f"wearing{add_item_with_color(values['eye_item'], values['COLOR_eye_item'])}")
        if values['mouth_item']:
            desc_parts.append(
                f"wearing{add_item_with_color(values['mouth_item'], values['COLOR_mouth_item'])}")

        if values['armors']:
            desc_parts.append(f"wearing {values['armors']}")
        if values['uniforms']:
            desc_parts.append(f"wearing {values['uniforms']}")

        if values['accessories']:
            desc_parts.append(
                f"accessorized with{add_item_with_color(values['accessories'], values['COLOR_accessories'])}")

        if values['material']:
            desc_parts.append(f"made of {values['material']}")

        if values['pattern']:
            desc_parts.append(f"in a {values['pattern']} pattern")

        if values['style_details']:
            desc_parts.append(f"with {values['style_details']} styling")

        outfit_desc = ", ".join(desc_parts)

        if CUSTOM_PROMPT.strip():
            outfit_desc += f", {CUSTOM_PROMPT.strip()}"

        return (outfit_desc,)


def pluralize_age(age, count):
    plurals = {
        "woman": "women",
        "man": "men",
        "girl": "girls",
        "boy": "boys",
        "baby girl": "baby girls",
        "baby boy": "baby boys",
        "teen girl": "teen girls",
        "teen boy": "teen boys",
        "young woman": "young women",
        "young man": "young men",
        "elderly woman": "elderly women",
        "elderly man": "elderly men"
    }
    return plurals.get(age, age) if count > 1 else age


def count_characters(text):
    if text is None:
        return 0

    character_count = 0
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('-'):
            # Count the number of consecutive dashes at the start
            dash_count = len(line) - len(line.lstrip('-'))
            character_count += dash_count

    return character_count


def number_to_word(number):
    words = {
        1: "one", 2: "two", 3: "three", 4: "four",
        5: "five", 6: "six", 7: "seven", 8: "eight",
        9: "nine", 10: "ten"
    }
    return words.get(number, "Invalid number")


class TextGeneratorCharacterFemale:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True}),
                "number_of_characters": ("INT", {"default": 1, "min": 1, "max": 10}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "location_on_image": (["NONE", "RANDOM"] + SharedLists.POSITIONS,),
                "ethnicity": (["NONE", "RANDOM"] + [ethni["name"] for ethni in SharedLists.ETHNICITIES["FEMALE"]], {"forceInput": False}),
                "ethnicity_description": ("BOOLEAN", {"default": False}),
                "nationality": (["NONE", "RANDOM"] + SharedLists.NATIONALITIES,),
                "age": (["RANDOM"] + SharedLists.AGES_FEMALE, {"default": "woman"}),
                "add_specific_age": ("STRING", {"multiline": False, "default": ""}),
                "body_shape": (["RANDOM", "NONE"] + SharedLists.BODY_SHAPES,),
                "breasts": (["RANDOM", "NONE"] + SharedLists.BREAST_SHAPES,),
                "ass": (["RANDOM", "NONE"] + SharedLists.ASS_SHAPES,),
                "skin_tone": (["NONE", "RANDOM"] + SharedLists.SKIN_TONES,),
                "eye_color": (["NONE", "RANDOM"] + SharedLists.EYE_COLORS,),
                "hair_style": (["NONE", "RANDOM"] + SharedLists.HAIR_STYLES,),
                "hair_color": (["NONE", "RANDOM"] + SharedLists.COLORS,),
                "CUSTOM_PROMPT": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "add_GEN_CHARACTER": ("GEN_CHARACTER",),
                "GEN_OUTFIT": ("GEN_OUTFIT",),
                "GEN_POSE": ("GEN_POSE",),
            }
        }

    RETURN_TYPES = ("GEN_CHARACTER",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"

    def select_value(self, options, current_value, rng):
        if current_value == "RANDOM":
            valid_options = [
                opt for opt in options if opt not in ["RANDOM", "NONE"]]
            return rng.choice(valid_options)
        elif current_value == "NONE":
            return ""
        return current_value

    def generate(self, enabled, number_of_characters, seed, location_on_image, ethnicity, ethnicity_description, nationality,
                 age, add_specific_age, body_shape, ass, breasts, skin_tone, eye_color, hair_style, hair_color,
                 CUSTOM_PROMPT, add_GEN_CHARACTER=None, GEN_OUTFIT=None, GEN_POSE=None):

        if not enabled:
            return (add_GEN_CHARACTER if add_GEN_CHARACTER else "",)

        rng = random.Random(seed)

        values = {
            'location_on_image': self.select_value(self.INPUT_TYPES()["required"]["location_on_image"][0], location_on_image, rng),
            'ethnicity': self.select_value(self.INPUT_TYPES()["required"]["ethnicity"][0], ethnicity, rng),
            'nationality': self.select_value(self.INPUT_TYPES()["required"]["nationality"][0], nationality, rng),
            'age': self.select_value(self.INPUT_TYPES()["required"]["age"][0], age, rng),
            'body_shape': self.select_value(self.INPUT_TYPES()["required"]["body_shape"][0], body_shape, rng),
            'ass': self.select_value(self.INPUT_TYPES()["required"]["ass"][0], ass, rng),
            'breasts': self.select_value(self.INPUT_TYPES()["required"]["breasts"][0], breasts, rng),
            'skin_tone': self.select_value(self.INPUT_TYPES()["required"]["skin_tone"][0], skin_tone, rng),
            'eye_color': self.select_value(self.INPUT_TYPES()["required"]["eye_color"][0], eye_color, rng),
            'hair_style': self.select_value(self.INPUT_TYPES()["required"]["hair_style"][0], hair_style, rng),
            'hair_color': self.select_value(self.INPUT_TYPES()["required"]["hair_color"][0], hair_color, rng),
        }

        desc_parts = []
        
        # Location
        if values['location_on_image']:
            desc_parts.append(f"On the {values['location_on_image']} of the image:")

        # Age and ethnicity description
        if values['age']:
            age_desc = values['age']
            if add_specific_age:
                age_desc = f"{add_specific_age} years old {pluralize_age(values['age'], number_of_characters)}"
            else:
                age_desc = pluralize_age(values['age'], number_of_characters)

            combined_desc = []
            if values['nationality']:
                combined_desc.append(values['nationality'])
            if values['ethnicity']:
                combined_desc.append(values['ethnicity'])
                if ethnicity_description:
                    for eth in SharedLists.ETHNICITIES['FEMALE']:
                        if eth['name'] == values['ethnicity']:
                            combined_desc.append(f"({eth['description']})")
                            break

            if combined_desc:
                desc_parts.append(f"{number_to_word(number_of_characters)} {' '.join(combined_desc)} {age_desc}")
            else:
                desc_parts.append(f"{number_to_word(number_of_characters)} {age_desc}")

        # Pose
        if GEN_POSE:
            desc_parts.append(GEN_POSE)

        # Physical characteristics
        if values['body_shape']:
            desc_parts.append(f"with a {values['body_shape']} build")
        if values['skin_tone']:
            desc_parts.append(f"with {values['skin_tone']} skin")
        if values['eye_color']:
            desc_parts.append(f"{values['eye_color']} eyes")
        if values['hair_color']:
            desc_parts.append(f"{values['hair_color']} hair")
        if values['hair_style']:
            desc_parts.append(f"{values['hair_style']} haircut")
        if values['ass']:
            desc_parts.append(f"{values['ass']} ass")
        if values['breasts']:
            desc_parts.append(f"{values['breasts']} breasts")

        # Outfit
        if GEN_OUTFIT:
            desc_parts.append(GEN_OUTFIT)

        # Combine description
        if values['location_on_image']:
            # Join parts properly with no redundant comma after location
            character_desc = desc_parts[0] + " " + ", ".join(desc_parts[1:])
        else:
            character_desc = ", ".join(desc_parts)

        # Custom prompt
        if CUSTOM_PROMPT.strip():
            character_desc += f", {CUSTOM_PROMPT.strip()}"

        # Final description
        if number_of_characters > 1:
            # Add multiple dashes based on number of characters
            dashes = '-' * number_of_characters
            final_description = f"{dashes} {character_desc}"
        else:
            final_description = f"- {character_desc}"

        if add_GEN_CHARACTER:
            return (f"{add_GEN_CHARACTER}\n{final_description}",)
        return (final_description,)



class TextGeneratorCharacterMale:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True}),
                "number_of_characters": ("INT", {"default": 1, "min": 1, "max": 10}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "location_on_image": (["NONE", "RANDOM"] + SharedLists.POSITIONS,),
                "ethnicity": (["NONE", "RANDOM"] + [ethni["name"] for ethni in SharedLists.ETHNICITIES["MALE"]], {"forceInput": False}),
                "ethnicity_description": ("BOOLEAN", {"default": False}),
                "nationality": (["NONE", "RANDOM"] + SharedLists.NATIONALITIES,),
                "age": (["RANDOM"] + SharedLists.AGES_MALE, {"default": "man"}),
                "add_specific_age": ("STRING", {"multiline": False, "default": ""}),
                "body_shape": (["RANDOM", "NONE"] + SharedLists.BODY_SHAPES,),
                "skin_tone": (["NONE", "RANDOM"] + SharedLists.SKIN_TONES,),
                "facial_hair": (["NONE", "RANDOM"] + SharedLists.FACIAL_HAIR_TYPES,),
                "eye_color": (["NONE", "RANDOM"] + SharedLists.EYE_COLORS,),
                "hair_style": (["NONE", "RANDOM"] + SharedLists.HAIR_STYLES,),
                "hair_color": (["NONE", "RANDOM"] + SharedLists.COLORS,),
                "CUSTOM_PROMPT": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "add_GEN_CHARACTER": ("GEN_CHARACTER",),
                "GEN_OUTFIT": ("GEN_OUTFIT",),
                "GEN_POSE": ("GEN_POSE",),
            }
        }

    RETURN_TYPES = ("GEN_CHARACTER",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"

    def select_value(self, options, current_value, rng):
        if current_value == "RANDOM":
            valid_options = [
                opt for opt in options if opt not in ["RANDOM", "NONE"]]
            return rng.choice(valid_options)
        elif current_value == "NONE":
            return ""
        return current_value

    def generate(self, enabled, number_of_characters, seed, location_on_image, ethnicity, ethnicity_description, nationality,
                 age, add_specific_age, body_shape, skin_tone, eye_color, hair_style, hair_color, facial_hair,
                 CUSTOM_PROMPT, add_GEN_CHARACTER=None, GEN_OUTFIT=None, GEN_POSE=None):

        if not enabled:
            return (add_GEN_CHARACTER if add_GEN_CHARACTER else "",)

        rng = random.Random(seed)

        values = {
            'location_on_image': self.select_value(self.INPUT_TYPES()["required"]["location_on_image"][0], location_on_image, rng),
            'ethnicity': self.select_value(self.INPUT_TYPES()["required"]["ethnicity"][0], ethnicity, rng),
            'nationality': self.select_value(self.INPUT_TYPES()["required"]["nationality"][0], nationality, rng),
            'age': self.select_value(self.INPUT_TYPES()["required"]["age"][0], age, rng),
            'body_shape': self.select_value(self.INPUT_TYPES()["required"]["body_shape"][0], body_shape, rng),
            'skin_tone': self.select_value(self.INPUT_TYPES()["required"]["skin_tone"][0], skin_tone, rng),
            'eye_color': self.select_value(self.INPUT_TYPES()["required"]["eye_color"][0], eye_color, rng),
            'hair_style': self.select_value(self.INPUT_TYPES()["required"]["hair_style"][0], hair_style, rng),
            'hair_color': self.select_value(self.INPUT_TYPES()["required"]["hair_color"][0], hair_color, rng),
            'facial_hair': self.select_value(self.INPUT_TYPES()["required"]["facial_hair"][0], facial_hair, rng),
        }

        desc_parts = []
        
        # Location
        if values['location_on_image']:
            desc_parts.append(f"On the {values['location_on_image']} of the image:")

        # Age and ethnicity description
        if values['age']:
            age_desc = values['age']
            if add_specific_age:
                age_desc = f"{add_specific_age} years old {pluralize_age(values['age'], number_of_characters)}"
            else:
                age_desc = pluralize_age(values['age'], number_of_characters)

            combined_desc = []
            if values['nationality']:
                combined_desc.append(values['nationality'])
            if values['ethnicity']:
                combined_desc.append(values['ethnicity'])
                if ethnicity_description:
                    for eth in SharedLists.ETHNICITIES['MALE']:
                        if eth['name'] == values['ethnicity']:
                            combined_desc.append(f"({eth['description']})")
                            break

            if combined_desc:
                desc_parts.append(f"{number_to_word(number_of_characters)} {' '.join(combined_desc)} {age_desc}")
            else:
                desc_parts.append(f"{number_to_word(number_of_characters)} {age_desc}")

        # Pose
        if GEN_POSE:
            desc_parts.append(GEN_POSE)

        # Physical characteristics
        if values['body_shape']:
            desc_parts.append(f"with a {values['body_shape']} build")
        if values['facial_hair']:
            desc_parts.append(f"{values['facial_hair']}")
        if values['skin_tone']:
            desc_parts.append(f"with {values['skin_tone']} skin")
        if values['eye_color']:
            desc_parts.append(f"{values['eye_color']} eyes")
        if values['hair_color']:
            desc_parts.append(f"{values['hair_color']} hair")
        if values['hair_style']:
            desc_parts.append(f"{values['hair_style']} haircut")

        # Outfit
        if GEN_OUTFIT:
            desc_parts.append(GEN_OUTFIT)

        # Combine description
        if values['location_on_image']:
            # Avoid redundant commas; treat first part as a prefix
            character_desc = desc_parts[0] + " " + ", ".join(desc_parts[1:])
        else:
            character_desc = ", ".join(desc_parts)

        # Custom prompt
        if CUSTOM_PROMPT.strip():
            character_desc += f", {CUSTOM_PROMPT.strip()}"

        # Final description
        if number_of_characters > 1:
            # Add multiple dashes based on number of characters
            dashes = '-' * number_of_characters
            final_description = f"{dashes} {character_desc}"
        else:
            final_description = f"- {character_desc}"

        if add_GEN_CHARACTER:
            return (f"{add_GEN_CHARACTER}\n{final_description}",)
        return (final_description,)



class TextGeneratorStyle:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "artistic_style": (["RANDOM", "NONE"] + SharedLists.ARTISTIC_STYLES,),
                "color_palette": (["RANDOM", "NONE"] + SharedLists.COLOR_PALETTES,),
                "lighting_type": (["RANDOM", "NONE"] + SharedLists.LIGHTING_TYPES,),
                "mood": (["RANDOM", "NONE"] + SharedLists.MOODS,),
                "composition": (["RANDOM", "NONE"] + SharedLists.COMPOSITIONS,),
                "CUSTOM_PROMPT": ("STRING", {"multiline": True, "default": ""})
            }
        }

    RETURN_TYPES = ("GEN_STYLE",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"

    def select_random_element(self, available_options, selected_value, random_generator):
        if selected_value == "RANDOM":
            valid_choices = [
                opt for opt in available_options if opt not in ["RANDOM", "NONE"]]
            return random_generator.choice(valid_choices)
        elif selected_value == "NONE":
            return ""
        return selected_value

    def generate(self, seed, artistic_style, color_palette, lighting_type, mood, composition, CUSTOM_PROMPT):
        random_generator = random.Random(seed)

        style_elements = {
            k: self.select_random_element(
                self.INPUT_TYPES()["required"][k][0], v, random_generator)
            for k, v in locals().items()
            if k not in ['self', 'seed', 'random_generator', 'CUSTOM_PROMPT']
        }

        style_components = []
        if style_elements['artistic_style']:
            style_components.append(
                f"{style_elements['artistic_style']} style")
        if style_elements['color_palette']:
            style_components.append(
                f"using a {style_elements['color_palette']} color scheme")
        if style_elements['lighting_type']:
            style_components.append(
                f"with {style_elements['lighting_type']} lighting")
        if style_elements['mood']:
            style_components.append(
                f"conveying a {style_elements['mood']} mood")
        if style_elements['composition']:
            style_components.append(
                f"in a {style_elements['composition']} composition")

        style_description = ", ".join(style_components)

        if CUSTOM_PROMPT.strip():
            style_description += f", {CUSTOM_PROMPT.strip()}"

        return (style_description,)


class TextGeneratorScene:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "scene_type": (["RANDOM", "NONE"] + SharedLists.SCENE_TYPES,),
                "time_period": (["RANDOM", "NONE"] + SharedLists.TIME_PERIODS,),
                "weather_condition": (["RANDOM", "NONE"] + SharedLists.WEATHER_CONDITIONS,),
                "ambiance": (["RANDOM", "NONE"] + SharedLists.AMBIANCE_TYPES,),
                "setting": (["RANDOM", "NONE"] + SharedLists.SETTINGS,),
                "CUSTOM_PROMPT": ("STRING", {"multiline": True, "default": ""})
            }
        }

    RETURN_TYPES = ("GEN_SCENE",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"

    def select_random_element(self, available_options, selected_value, random_generator):
        if selected_value == "RANDOM":
            valid_choices = [
                opt for opt in available_options if opt not in ["RANDOM", "NONE"]]
            return random_generator.choice(valid_choices)
        elif selected_value == "NONE":
            return ""
        return selected_value

    def generate(self, seed, scene_type, time_period, weather_condition, ambiance, setting, CUSTOM_PROMPT):
        random_generator = random.Random(seed)

        scene_elements = {
            k: self.select_random_element(
                self.INPUT_TYPES()["required"][k][0], v, random_generator)
            for k, v in locals().items()
            if k not in ['self', 'seed', 'random_generator', 'CUSTOM_PROMPT']
        }

        scene_components = []
        if scene_elements['ambiance'] and scene_elements['scene_type']:
            scene_components.append(
                f"in a {scene_elements['ambiance']} {scene_elements['scene_type']} scene")
        if scene_elements['setting']:
            scene_components.append(f"located in {scene_elements['setting']}")
        if scene_elements['time_period']:
            scene_components.append(
                f"during the {scene_elements['time_period']}")
        if scene_elements['weather_condition']:
            scene_components.append(
                f"with {scene_elements['weather_condition']} conditions")

        scene_description = ", ".join(scene_components)

        if CUSTOM_PROMPT.strip():
            scene_description += f", {CUSTOM_PROMPT.strip()}"

        return (scene_description,)


class TextGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "camera_angle": (["NONE", "RANDOM"] + SharedLists.CAMERA_ANGLES,),
                "shot_type": (["NONE", "RANDOM"] + SharedLists.SHOT_TYPES,),
                "multi_char_action": (["NONE", "CUSTOM", "RANDOM"] + SharedLists.ACTIONS,),
                "CUSTOM_action": ("STRING", {"multiline": False, "default": ""}),
                "CUSTOM_PROMPT": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "GEN_STYLE": ("GEN_STYLE",),
                "GEN_CHARACTER": ("GEN_CHARACTER",),
                "GEN_SCENE": ("GEN_SCENE",),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"

    def select_random_element(self, options, current_value, random_generator):
        if current_value == "RANDOM":
            valid_choices = [
                opt for opt in options if opt not in ["RANDOM", "NONE"]]
            return random_generator.choice(valid_choices)
        elif current_value == "NONE":
            return ""
        return current_value

    def generate(self, seed, camera_angle, shot_type, multi_char_action, CUSTOM_action,
                 CUSTOM_PROMPT, GEN_CHARACTER=None, GEN_STYLE=None, GEN_SCENE=None):
        random_generator = random.Random(seed)

        local_vars = locals()
        if CUSTOM_action.strip():
            local_vars['multi_char_action'] = CUSTOM_action.strip()

        values = {k: self.select_random_element(self.INPUT_TYPES()["required"][k][0], v, random_generator)
                  for k, v in local_vars.items()
                  if k in ['camera_angle', 'shot_type', 'multi_char_action']}

        if GEN_CHARACTER is not None:
            character_count = 0
            for line in GEN_CHARACTER.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    # Count the number of consecutive dashes at the start
                    dash_count = len(line) - len(line.lstrip('-'))
                    character_count += dash_count
        else:
            character_count = 0

        prompt_parts = []

        if values['shot_type'] or values['camera_angle']:
            shot_description = []
            if values['shot_type']:
                shot_description.append(values['shot_type'])
            if values['camera_angle']:
                shot_description.append(f"from {values['camera_angle']}")
            prompt_parts.append(" ".join(shot_description))

        if character_count > 1 and values['multi_char_action']:
            if values['multi_char_action'] == "CUSTOM":
                character_intro = f"Image with {character_count} characters {values['CUSTOM_action']} :"
            else:
                character_intro = f"Image with {character_count} characters {values['multi_char_action']} :"
        elif character_count > 1:
            character_intro = f"Image with {character_count} characters :"
        else:
            character_intro = ""

        technical_desc = ", ".join(prompt_parts) if prompt_parts else ""

        final_parts = []
        if technical_desc:
            if CUSTOM_PROMPT.strip():
                technical_desc += f", {CUSTOM_PROMPT.strip()}"
            final_parts.append(technical_desc)
        if character_intro:
            final_parts.append(character_intro)

        # Combine all parts
        final_prompt_parts = []

        if GEN_STYLE:
            final_prompt_parts.append(GEN_STYLE)

        if final_parts:
            final_prompt_parts.append(", ".join(final_parts))

        if GEN_CHARACTER:
            final_prompt_parts.append(GEN_CHARACTER)

        if GEN_SCENE:
            final_prompt_parts.append(GEN_SCENE)

        final_prompt = "\n".join(
            part for part in final_prompt_parts if part.strip())

        return (final_prompt,)

class ListLooperOutfitMale:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SELECTION": ([
                    "top",
                    "bottom",
                    "footwear",
                    "head_item",
                    "eye_item",
                    "mouth_item",
                    "accessories",
                    "armors",
                    "uniforms",
                    "material",
                    "pattern",
                    "style_details",
                    "style",
                    "cosplay",
                    "colors"
                ], {"forceInput": False}),
                "top": ([f"ALL ({len(SharedLists.MALE_OUTFITS['TOPS'])})"] + SharedLists.MALE_OUTFITS["TOPS"],),
                "bottom": ([f"ALL ({len(SharedLists.MALE_OUTFITS['BOTTOMS'])})"] + SharedLists.MALE_OUTFITS["BOTTOMS"],),
                "footwear": ([f"ALL ({len(SharedLists.MALE_OUTFITS['FOOTWEAR'])})"] + SharedLists.MALE_OUTFITS["FOOTWEAR"],),
                "head_item": ([f"ALL ({len(SharedLists.MALE_OUTFITS['HEAD_ITEMS'])})"] + SharedLists.MALE_OUTFITS["HEAD_ITEMS"],),
                "eye_item": ([f"ALL ({len(SharedLists.MALE_OUTFITS['EYE_ITEMS'])})"] + SharedLists.MALE_OUTFITS["EYE_ITEMS"],),
                "mouth_item": ([f"ALL ({len(SharedLists.MALE_OUTFITS['MOUTH_ITEMS'])})"] + SharedLists.MALE_OUTFITS["MOUTH_ITEMS"],),
                "accessories": ([f"ALL ({len(SharedLists.MALE_OUTFITS['ACCESSORIES'])})"] + SharedLists.MALE_OUTFITS["ACCESSORIES"],),
                "armors": ([f"ALL ({len(SharedLists.ARMORS)})"] + SharedLists.ARMORS,),
                "uniforms": ([f"ALL ({len(SharedLists.UNIFORMS)})"] + SharedLists.UNIFORMS,),
                "material": ([f"ALL ({len(SharedLists.MATERIALS)})"] + SharedLists.MATERIALS,),
                "pattern": ([f"ALL ({len(SharedLists.PATTERNS)})"] + SharedLists.PATTERNS,),
                "style_details": ([f"ALL ({len(SharedLists.STYLE_DETAILS)})"] + SharedLists.STYLE_DETAILS,),
                "style": ([f"ALL ({len(SharedLists.STYLES)})"] + SharedLists.STYLES,),
                "cosplay": ([f"ALL ({len(SharedLists.COSPLAY['MALE'])})"] + [character["name"] for character in SharedLists.COSPLAY["MALE"]],),
                "colors": ([f"ALL ({len(SharedLists.COLORS)})"] + SharedLists.COLORS,),
            }
        }

    RETURN_TYPES = (Everything("*"),)
    FUNCTION = "get_list"
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Bjornulf"

    def get_list(self, SELECTION, top, bottom, footwear, head_item, eye_item, mouth_item,
                 accessories, armors, uniforms, material, pattern, style_details, 
                 style, cosplay, colors):
        selection_map = {
            "top": (top, SharedLists.MALE_OUTFITS["TOPS"]),
            "bottom": (bottom, SharedLists.MALE_OUTFITS["BOTTOMS"]),
            "footwear": (footwear, SharedLists.MALE_OUTFITS["FOOTWEAR"]),
            "head_item": (head_item, SharedLists.MALE_OUTFITS["HEAD_ITEMS"]),
            "eye_item": (eye_item, SharedLists.MALE_OUTFITS["EYE_ITEMS"]),
            "mouth_item": (mouth_item, SharedLists.MALE_OUTFITS["MOUTH_ITEMS"]),
            "accessories": (accessories, SharedLists.MALE_OUTFITS["ACCESSORIES"]),
            "armors": (armors, SharedLists.ARMORS),
            "uniforms": (uniforms, SharedLists.UNIFORMS),
            "material": (material, SharedLists.MATERIALS),
            "pattern": (pattern, SharedLists.PATTERNS),
            "style_details": (style_details, SharedLists.STYLE_DETAILS),
            "style": (style, SharedLists.STYLES),
            "cosplay": (cosplay, [character["name"] for character in SharedLists.COSPLAY["MALE"]]),
            "colors": (colors, SharedLists.COLORS)
        }
        selected_value, full_list = selection_map[SELECTION]
        return (full_list,) if "ALL" in selected_value else ([selected_value],)

class ListLooperOutfitFemale:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SELECTION": ([
                    "top",
                    "bottom",
                    "dress",
                    "full_body",
                    "footwear",
                    "head_item",
                    "eye_item",
                    "mouth_item",
                    "accessories",
                    "armors",
                    "uniforms",
                    "material",
                    "pattern",
                    "style_details",
                    "style",
                    "cosplay",
                    "colors"
                ], {"forceInput": False}),
                "top": ([f"ALL ({len(SharedLists.FEMALE_OUTFITS['TOPS'])})"] + SharedLists.FEMALE_OUTFITS["TOPS"],),
                "bottom": ([f"ALL ({len(SharedLists.FEMALE_OUTFITS['BOTTOMS'])})"] + SharedLists.FEMALE_OUTFITS["BOTTOMS"],),
                "dress": ([f"ALL ({len(SharedLists.FEMALE_OUTFITS['DRESSES'])})"] + SharedLists.FEMALE_OUTFITS["DRESSES"],),
                "full_body": ([f"ALL ({len(SharedLists.FEMALE_OUTFITS['FULL_BODY_CLOTHES'])})"] + SharedLists.FEMALE_OUTFITS["FULL_BODY_CLOTHES"],),
                "footwear": ([f"ALL ({len(SharedLists.FEMALE_OUTFITS['FOOTWEAR'])})"] + SharedLists.FEMALE_OUTFITS["FOOTWEAR"],),
                "head_item": ([f"ALL ({len(SharedLists.FEMALE_OUTFITS['HEAD_ITEMS'])})"] + SharedLists.FEMALE_OUTFITS["HEAD_ITEMS"],),
                "eye_item": ([f"ALL ({len(SharedLists.FEMALE_OUTFITS['EYE_ITEMS'])})"] + SharedLists.FEMALE_OUTFITS["EYE_ITEMS"],),
                "mouth_item": ([f"ALL ({len(SharedLists.FEMALE_OUTFITS['MOUTH_ITEMS'])})"] + SharedLists.FEMALE_OUTFITS["MOUTH_ITEMS"],),
                "accessories": ([f"ALL ({len(SharedLists.FEMALE_OUTFITS['ACCESSORIES'])})"] + SharedLists.FEMALE_OUTFITS["ACCESSORIES"],),
                "armors": ([f"ALL ({len(SharedLists.ARMORS)})"] + SharedLists.ARMORS,),
                "uniforms": ([f"ALL ({len(SharedLists.UNIFORMS)})"] + SharedLists.UNIFORMS,),
                "material": ([f"ALL ({len(SharedLists.MATERIALS)})"] + SharedLists.MATERIALS,),
                "pattern": ([f"ALL ({len(SharedLists.PATTERNS)})"] + SharedLists.PATTERNS,),
                "style_details": ([f"ALL ({len(SharedLists.STYLE_DETAILS)})"] + SharedLists.STYLE_DETAILS,),
                "style": ([f"ALL ({len(SharedLists.STYLES)})"] + SharedLists.STYLES,),
                "cosplay": ([f"ALL ({len(SharedLists.COSPLAY['FEMALE'])})"] + [character["name"] for character in SharedLists.COSPLAY["FEMALE"]],),
                "colors": ([f"ALL ({len(SharedLists.COLORS)})"] + SharedLists.COLORS,),
            }
        }

    RETURN_TYPES = (Everything("*"),)
    FUNCTION = "get_list"
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Bjornulf"

    def get_list(self, SELECTION, top, bottom, dress, full_body, footwear, head_item, 
                 eye_item, mouth_item, accessories, armors, uniforms, material, pattern, 
                 style_details, style, cosplay, colors):
        selection_map = {
            "top": (top, SharedLists.FEMALE_OUTFITS["TOPS"]),
            "bottom": (bottom, SharedLists.FEMALE_OUTFITS["BOTTOMS"]),
            "dress": (dress, SharedLists.FEMALE_OUTFITS["DRESSES"]),
            "full_body": (full_body, SharedLists.FEMALE_OUTFITS["FULL_BODY_CLOTHES"]),
            "footwear": (footwear, SharedLists.FEMALE_OUTFITS["FOOTWEAR"]),
            "head_item": (head_item, SharedLists.FEMALE_OUTFITS["HEAD_ITEMS"]),
            "eye_item": (eye_item, SharedLists.FEMALE_OUTFITS["EYE_ITEMS"]),
            "mouth_item": (mouth_item, SharedLists.FEMALE_OUTFITS["MOUTH_ITEMS"]),
            "accessories": (accessories, SharedLists.FEMALE_OUTFITS["ACCESSORIES"]),
            "armors": (armors, SharedLists.ARMORS),
            "uniforms": (uniforms, SharedLists.UNIFORMS),
            "material": (material, SharedLists.MATERIALS),
            "pattern": (pattern, SharedLists.PATTERNS),
            "style_details": (style_details, SharedLists.STYLE_DETAILS),
            "style": (style, SharedLists.STYLES),
            "cosplay": (cosplay, [character["name"] for character in SharedLists.COSPLAY["FEMALE"]]),
            "colors": (colors, SharedLists.COLORS)
        }
        selected_value, full_list = selection_map[SELECTION]
        return (full_list,) if "ALL" in selected_value else ([selected_value],)

class ListLooperCharacter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SELECTION": ([
                    # Human characteristics
                    "location_on_image",
                    "ethnicity",
                    "nationality",
                    "age_male",
                    "age_female",
                    "body_shape",
                    "skin_tone",
                    "eye_color",
                    "hair_style",
                    "hair_color",
                    "facial_hair",
                    "breasts",
                    "ass",
                    # Monster/Creature characteristics
                    "land_animal",
                    "water_animal",
                    "creature_type",
                    "creature_size",
                    "creature_temperament",
                    "creature_ability",
                    "creature_features",
                    "magical_properties"
                ], {"forceInput": False}),
                # Human-related options
                "location_on_image": ([f"ALL ({len(SharedLists.POSITIONS)})"] + SharedLists.POSITIONS,),
                "ethnicity": ([f"ALL ({len([ethni['name'] for ethni in SharedLists.ETHNICITIES['MALE']] + [ethni['name'] for ethni in SharedLists.ETHNICITIES['FEMALE']])})"] + 
                            [ethni["name"] for ethni in SharedLists.ETHNICITIES["MALE"]] + [ethni["name"] for ethni in SharedLists.ETHNICITIES["FEMALE"]],),
                "nationality": ([f"ALL ({len(SharedLists.NATIONALITIES)})"] + SharedLists.NATIONALITIES,),
                "age_male": ([f"ALL ({len(SharedLists.AGES_MALE)})"] + SharedLists.AGES_MALE,),
                "age_female": ([f"ALL ({len(SharedLists.AGES_FEMALE)})"] + SharedLists.AGES_FEMALE,),
                "body_shape": ([f"ALL ({len(SharedLists.BODY_SHAPES)})"] + SharedLists.BODY_SHAPES,),
                "skin_tone": ([f"ALL ({len(SharedLists.SKIN_TONES)})"] + SharedLists.SKIN_TONES,),
                "eye_color": ([f"ALL ({len(SharedLists.EYE_COLORS)})"] + SharedLists.EYE_COLORS,),
                "hair_style": ([f"ALL ({len(SharedLists.HAIR_STYLES)})"] + SharedLists.HAIR_STYLES,),
                "hair_color": ([f"ALL ({len(SharedLists.COLORS)})"] + SharedLists.COLORS,),
                "facial_hair": ([f"ALL ({len(SharedLists.FACIAL_HAIR_TYPES)})"] + SharedLists.FACIAL_HAIR_TYPES,),
                "breasts": ([f"ALL ({len(SharedLists.BREAST_SHAPES)})"] + SharedLists.BREAST_SHAPES,),
                "ass": ([f"ALL ({len(SharedLists.ASS_SHAPES)})"] + SharedLists.ASS_SHAPES,),
                # Monster/Creature-related options
                "land_animal": ([f"ALL ({len(SharedLists.LAND_ANIMALS)})"] + SharedLists.LAND_ANIMALS,),
                "water_animal": ([f"ALL ({len(SharedLists.WATER_ANIMALS)})"] + SharedLists.WATER_ANIMALS,),
                "creature_type": ([f"ALL ({len(SharedLists.CREATURE_TYPES)})"] + [creature["name"] for creature in SharedLists.CREATURE_TYPES.values()],),
                "creature_size": ([f"ALL ({len(SharedLists.CREATURE_SIZES)})"] + SharedLists.CREATURE_SIZES,),
                "creature_temperament": ([f"ALL ({len(SharedLists.CREATURE_TEMPERAMENTS)})"] + SharedLists.CREATURE_TEMPERAMENTS,),
                "creature_ability": ([f"ALL ({len(SharedLists.CREATURE_ABILITIES)})"] + SharedLists.CREATURE_ABILITIES,),
                "creature_features": ([f"ALL ({len(SharedLists.CREATURE_FEATURES)})"] + SharedLists.CREATURE_FEATURES,),
                "magical_properties": ([f"ALL ({len(SharedLists.MAGICAL_PROPERTIES)})"] + SharedLists.MAGICAL_PROPERTIES,),
            }
        }

    RETURN_TYPES = (Everything("*"),)
    FUNCTION = "get_list"
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Bjornulf"

    def get_list(self, SELECTION, location_on_image, ethnicity, nationality, 
                 age_male, age_female, body_shape, skin_tone, eye_color, 
                 hair_style, hair_color, facial_hair, breasts, ass,
                 creature_type, creature_size, creature_temperament, water_animal, land_animal,
                 creature_ability, creature_features, magical_properties):
        
        # Create a dictionary mapping selection names to their values and lists
        selection_map = {
            # Human characteristics
            "location_on_image": (location_on_image, SharedLists.POSITIONS),
            "ethnicity": (ethnicity, [ethni["name"] for ethni in SharedLists.ETHNICITIES["MALE"]] + 
                         [ethni["name"] for ethni in SharedLists.ETHNICITIES["FEMALE"]]),
            "nationality": (nationality, SharedLists.NATIONALITIES),
            "age_male": (age_male, SharedLists.AGES_MALE),
            "age_female": (age_female, SharedLists.AGES_FEMALE),
            "body_shape": (body_shape, SharedLists.BODY_SHAPES),
            "skin_tone": (skin_tone, SharedLists.SKIN_TONES),
            "eye_color": (eye_color, SharedLists.EYE_COLORS),
            "hair_style": (hair_style, SharedLists.HAIR_STYLES),
            "hair_color": (hair_color, SharedLists.COLORS),
            "facial_hair": (facial_hair, SharedLists.FACIAL_HAIR_TYPES),
            "breasts": (breasts, SharedLists.BREAST_SHAPES),
            "ass": (ass, SharedLists.ASS_SHAPES),
            # Monster/Creature characteristics
            "land_animal": (land_animal, SharedLists.LAND_ANIMALS),
            "water_animal": (water_animal, SharedLists.WATER_ANIMALS),
            "creature_type": (creature_type, [creature["name"] for creature in SharedLists.CREATURE_TYPES.values()]),
            "creature_size": (creature_size, SharedLists.CREATURE_SIZES),
            "creature_temperament": (creature_temperament, SharedLists.CREATURE_TEMPERAMENTS),
            "creature_ability": (creature_ability, SharedLists.CREATURE_ABILITIES),
            "creature_features": (creature_features, SharedLists.CREATURE_FEATURES),
            "magical_properties": (magical_properties, SharedLists.MAGICAL_PROPERTIES)
        }

        # Get the selected value and corresponding full list
        selected_value, full_list = selection_map[SELECTION]

        # If "ALL" is in the selected value (accounting for the count), return the full list
        if "ALL" in selected_value:
            return (full_list,)
        
        # Otherwise, return just the selected value as a single-item list
        return ([selected_value],)

class ListLooperStyle:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SELECTION": ([
                    "artistic_style",
                    "color_palette",
                    "lighting_type",
                    "mood",
                    "composition"
                ], {"forceInput": False}),
                "artistic_style": ([f"ALL ({len(SharedLists.ARTISTIC_STYLES)})"] + SharedLists.ARTISTIC_STYLES,),
                "color_palette": ([f"ALL ({len(SharedLists.COLOR_PALETTES)})"] + SharedLists.COLOR_PALETTES,),
                "lighting_type": ([f"ALL ({len(SharedLists.LIGHTING_TYPES)})"] + SharedLists.LIGHTING_TYPES,),
                "mood": ([f"ALL ({len(SharedLists.MOODS)})"] + SharedLists.MOODS,),
                "composition": ([f"ALL ({len(SharedLists.COMPOSITIONS)})"] + SharedLists.COMPOSITIONS,),
            }
        }

    RETURN_TYPES = (Everything("*"),)
    FUNCTION = "get_list"
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Bjornulf"

    def get_list(self, SELECTION, artistic_style, color_palette, 
                 lighting_type, mood, composition):
        selection_map = {
            "artistic_style": (artistic_style, SharedLists.ARTISTIC_STYLES),
            "color_palette": (color_palette, SharedLists.COLOR_PALETTES),
            "lighting_type": (lighting_type, SharedLists.LIGHTING_TYPES),
            "mood": (mood, SharedLists.MOODS),
            "composition": (composition, SharedLists.COMPOSITIONS)
        }
        selected_value, full_list = selection_map[SELECTION]
        return (full_list,) if "ALL" in selected_value else ([selected_value],)

class ListLooperPose:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SELECTION": ([
                    "pose_view",
                    "pose_camera",
                    "pose_face",
                    "pose_arms",
                    "pose_legs",
                    "pose_body",
                    "pose_head_neck",
                    "pose_dynamic",
                    "pose_action",
                    "pose_sitting",
                    "pose_unique",
                    "pose_for_object"
                ], {"forceInput": False}),
                "pose_view": ([f"ALL ({len(SharedLists.POSE_VIEW)})"] + SharedLists.POSE_VIEW,),
                "pose_camera": ([f"ALL ({len(SharedLists.POSE_CAMERA)})"] + SharedLists.POSE_CAMERA,),
                "pose_face": ([f"ALL ({len(SharedLists.POSE_FACE)})"] + SharedLists.POSE_FACE,),
                "pose_arms": ([f"ALL ({len(SharedLists.POSE_ARMS)})"] + SharedLists.POSE_ARMS,),
                "pose_legs": ([f"ALL ({len(SharedLists.POSE_LEGS)})"] + SharedLists.POSE_LEGS,),
                "pose_body": ([f"ALL ({len(SharedLists.POSE_BODY)})"] + SharedLists.POSE_BODY,),
                "pose_head_neck": ([f"ALL ({len(SharedLists.POSE_HEAD_NECK)})"] + SharedLists.POSE_HEAD_NECK,),
                "pose_dynamic": ([f"ALL ({len(SharedLists.POSE_DYNAMIC)})"] + SharedLists.POSE_DYNAMIC,),
                "pose_action": ([f"ALL ({len(SharedLists.POSE_ACTION)})"] + SharedLists.POSE_ACTION,),
                "pose_sitting": ([f"ALL ({len(SharedLists.POSE_SITTING)})"] + SharedLists.POSE_SITTING,),
                "pose_unique": ([f"ALL ({len(SharedLists.POSE_UNIQUE)})"] + SharedLists.POSE_UNIQUE,),
                "pose_for_object": ([f"ALL ({len(SharedLists.POSE_OBJECT)})"] + SharedLists.POSE_OBJECT,),
            }
        }

    RETURN_TYPES = (Everything("*"),)
    FUNCTION = "get_list"
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Bjornulf"

    def get_list(self, SELECTION, pose_view, pose_camera, pose_face, 
                 pose_arms, pose_legs, pose_body, pose_head_neck, 
                 pose_dynamic, pose_action, pose_sitting, pose_unique, 
                 pose_for_object):
        selection_map = {
            "pose_view": (pose_view, SharedLists.POSE_VIEW),
            "pose_camera": (pose_camera, SharedLists.POSE_CAMERA),
            "pose_face": (pose_face, SharedLists.POSE_FACE),
            "pose_arms": (pose_arms, SharedLists.POSE_ARMS),
            "pose_legs": (pose_legs, SharedLists.POSE_LEGS),
            "pose_body": (pose_body, SharedLists.POSE_BODY),
            "pose_head_neck": (pose_head_neck, SharedLists.POSE_HEAD_NECK),
            "pose_dynamic": (pose_dynamic, SharedLists.POSE_DYNAMIC),
            "pose_action": (pose_action, SharedLists.POSE_ACTION),
            "pose_sitting": (pose_sitting, SharedLists.POSE_SITTING),
            "pose_unique": (pose_unique, SharedLists.POSE_UNIQUE),
            "pose_for_object": (pose_for_object, SharedLists.POSE_OBJECT)
        }
        selected_value, full_list = selection_map[SELECTION]
        return (full_list,) if "ALL" in selected_value else ([selected_value],)

class ListLooperScene:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SELECTION": (["scene_type", "time_period", "weather_condition", "ambiance", "setting"], {"forceInput": False}),
                "scene_type": ([f"ALL ({len(SharedLists.SCENE_TYPES)})"] + SharedLists.SCENE_TYPES,),
                "time_period": ([f"ALL ({len(SharedLists.TIME_PERIODS)})"] + SharedLists.TIME_PERIODS,),
                "weather_condition": ([f"ALL ({len(SharedLists.WEATHER_CONDITIONS)})"] + SharedLists.WEATHER_CONDITIONS,),
                "ambiance": ([f"ALL ({len(SharedLists.AMBIANCE_TYPES)})"] + SharedLists.AMBIANCE_TYPES,),
                "setting": ([f"ALL ({len(SharedLists.SETTINGS)})"] + SharedLists.SETTINGS,),
            }
        }

    RETURN_TYPES = (Everything("*"),)
    FUNCTION = "get_list"
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Bjornulf"

    def get_list(self, SELECTION, scene_type, time_period, weather_condition, ambiance, setting):
        selection_map = {
            "scene_type": (scene_type, SharedLists.SCENE_TYPES),
            "time_period": (time_period, SharedLists.TIME_PERIODS),
            "weather_condition": (weather_condition, SharedLists.WEATHER_CONDITIONS),
            "ambiance": (ambiance, SharedLists.AMBIANCE_TYPES),
            "setting": (setting, SharedLists.SETTINGS)
        }
        selected_value, full_list = selection_map[SELECTION]
        return (full_list,) if "ALL" in selected_value else ([selected_value],)

class ListLooper:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SELECTION": (["camera_angle","shot_type","lighting","multi_char_action"],{"forceInput": False}),
                "camera_angle": ([f"ALL ({len(SharedLists.CAMERA_ANGLES)})"] + SharedLists.CAMERA_ANGLES,{"forceInput": False}),
                "shot_type": ([f"ALL ({len(SharedLists.SHOT_TYPES)})"] + SharedLists.SHOT_TYPES,{"forceInput": False}),
                # "lighting": ([f"ALL ({len(SharedLists.LIGHTING)})"] + SharedLists.LIGHTING,{"forceInput": False}),
                "multi_char_action": ([f"ALL ({len(SharedLists.ACTIONS)})"] + SharedLists.ACTIONS,{"forceInput": False}),
            }
        }

    RETURN_TYPES = (Everything("*"),)
    FUNCTION = "get_list"
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "Bjornulf"

    def get_list(self, SELECTION, camera_angle, shot_type, lighting, multi_char_action):
        selection_map = {
            "camera_angle": (camera_angle, SharedLists.CAMERA_ANGLES),
            "shot_type": (shot_type, SharedLists.SHOT_TYPES),
            # "lighting": (lighting, SharedLists.LIGHTING),
            "multi_char_action": (multi_char_action, SharedLists.ACTIONS)
        }
        selected_value, full_list = selection_map[SELECTION]
        return (full_list,) if "ALL" in selected_value else ([selected_value],)

class TextGeneratorCharacterPose:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "pose_view": (["NONE", "RANDOM"] + SharedLists.POSE_VIEW,),
                "pose_camera": (["NONE", "RANDOM"] + SharedLists.POSE_CAMERA,),
                "pose_face": (["NONE", "RANDOM"] + SharedLists.POSE_FACE,),
                "pose_arms": (["NONE", "RANDOM"] + SharedLists.POSE_ARMS,),
                "pose_legs": (["NONE", "RANDOM"] + SharedLists.POSE_LEGS,),
                "pose_body": (["NONE", "RANDOM"] + SharedLists.POSE_BODY,),
                "pose_head_neck": (["NONE", "RANDOM"] + SharedLists.POSE_HEAD_NECK,),
                "pose_dynamic": (["NONE", "RANDOM"] + SharedLists.POSE_DYNAMIC,),
                "pose_action": (["NONE", "RANDOM"] + SharedLists.POSE_ACTION,),
                "pose_sitting": (["NONE", "RANDOM"] + SharedLists.POSE_SITTING,),
                "pose_unique": (["NONE", "RANDOM"] + SharedLists.POSE_UNIQUE,),
                "pose_for_GEN_OBJECT": (["NONE", "RANDOM"] + SharedLists.POSE_OBJECT,),
                "CUSTOM_PROMPT": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "GEN_OBJECT": ("GEN_OBJECT",),
                "add_GEN_POSE": ("GEN_POSE",),
            }
        }

    RETURN_TYPES = ("GEN_POSE",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"

    def select_value(self, options, current_value, rng):
        if current_value == "RANDOM":
            valid_options = [opt for opt in options if opt not in ["RANDOM", "NONE"]]
            return rng.choice(valid_options) if valid_options else ""
        elif current_value == "NONE":
            return ""
        return current_value

    def generate(self, seed, pose_view, pose_camera, pose_face, pose_arms, pose_legs, pose_body,
                pose_head_neck, pose_dynamic, pose_action, pose_sitting, pose_unique,
                pose_for_GEN_OBJECT, CUSTOM_PROMPT, GEN_OBJECT=None, add_GEN_POSE=None):
        rng = random.Random(seed)
        all_poses = []

        # If there's an incoming pose, add it to all_poses first
        if add_GEN_POSE is not None:
            all_poses.extend([pose.strip() for pose in add_GEN_POSE.split(',')])

        # Dictionary mapping input parameters to their corresponding lists
        pose_mappings = {
            'pose_view': (pose_view, SharedLists.POSE_VIEW),
            'pose_camera': (pose_camera, SharedLists.POSE_CAMERA),
            'pose_face': (pose_face, SharedLists.POSE_FACE),
            'pose_arms': (pose_arms, SharedLists.POSE_ARMS),
            'pose_legs': (pose_legs, SharedLists.POSE_LEGS),
            'pose_body': (pose_body, SharedLists.POSE_BODY),
            'pose_head_neck': (pose_head_neck, SharedLists.POSE_HEAD_NECK),
            'pose_dynamic': (pose_dynamic, SharedLists.POSE_DYNAMIC),
            'pose_action': (pose_action, SharedLists.POSE_ACTION),
            'pose_sitting': (pose_sitting, SharedLists.POSE_SITTING),
            'pose_unique': (pose_unique, SharedLists.POSE_UNIQUE)
        }

        # Process each pose type
        for pose_name, (pose_value, pose_list) in pose_mappings.items():
            selected_pose = self.select_value(['NONE', 'RANDOM'] + pose_list, pose_value, rng)
            if selected_pose:
                all_poses.append(selected_pose)

        # Handle object-related poses
        if pose_for_GEN_OBJECT != "NONE" and GEN_OBJECT:
            action = self.select_value(['NONE', 'RANDOM'] + SharedLists.POSE_OBJECT, pose_for_GEN_OBJECT, rng)
            if action:
                objects = [obj.strip() for obj in GEN_OBJECT.split(',')]
                object_poses = [f"{action} {obj}" for obj in objects]
                all_poses.extend(object_poses)
        elif pose_for_GEN_OBJECT != "NONE":
            action = self.select_value(['NONE', 'RANDOM'] + SharedLists.POSE_OBJECT, pose_for_GEN_OBJECT, rng)
            if action:
                all_poses.append(f"{action} something")

        if CUSTOM_PROMPT:
            all_poses.append(CUSTOM_PROMPT)

        # Remove any empty strings and join with commas
        all_poses = [pose for pose in all_poses if pose.strip()]
        return (", ".join(all_poses),)


class TextGeneratorCharacterObject:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "object_selection": (["CUSTOM"] + SharedLists.OBJECTS,),
                "custom_object": ("STRING", {"default": "", "multiline": False}),
                "CUSTOM_PROMPT_PREFIX": ("STRING", {"default": "", "multiline": True}),
                "CUSTOM_PROMPT_SUFFIX": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "add_GEN_OBJECT": ("GEN_OBJECT",),
            }
        }

    RETURN_TYPES = ("GEN_OBJECT",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"

    def generate(self, object_selection, custom_object, CUSTOM_PROMPT_PREFIX, CUSTOM_PROMPT_SUFFIX, add_GEN_OBJECT=None):
        # Handle the current object
        if object_selection == "CUSTOM":
            current_object = custom_object.strip() if custom_object.strip() else "object"
        else:
            current_object = object_selection

        # Create the formatted object string
        prefix = f"{CUSTOM_PROMPT_PREFIX.strip()} " if CUSTOM_PROMPT_PREFIX.strip(
        ) else ""
        suffix = f" {CUSTOM_PROMPT_SUFFIX.strip()}" if CUSTOM_PROMPT_SUFFIX.strip(
        ) else ""
        formatted_object = f"{prefix}{current_object}{suffix}"

        # If there are previous objects, append the current one
        if add_GEN_OBJECT:
            return (f"{add_GEN_OBJECT}, {formatted_object}",)

        return (formatted_object,)

class TextGeneratorCharacterCreature:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True}),
                "number_of_creatures": ("INT", {"default": 1, "min": 1, "max": 10}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "location_on_image": (["NONE", "RANDOM"] + SharedLists.POSITIONS,),
                "creature_type": (["RANDOM", "NONE"] + [creature["name"] for creature in SharedLists.CREATURE_TYPES.values()],),
                "show_creature_description": ("BOOLEAN", {"default": False}),
                "land_animal": (["NONE", "RANDOM"] + SharedLists.LAND_ANIMALS,),
                "water_animal": (["NONE", "RANDOM"] + SharedLists.WATER_ANIMALS,),
                "size": (["NONE", "RANDOM"] + SharedLists.CREATURE_SIZES,),
                "temperament": (["NONE", "RANDOM"] + SharedLists.CREATURE_TEMPERAMENTS,),
                "special_ability": (["NONE", "RANDOM"] + SharedLists.CREATURE_ABILITIES,),
                "features": (["NONE", "RANDOM"] + SharedLists.CREATURE_FEATURES,),
                "magical_properties": (["NONE", "RANDOM"] + SharedLists.MAGICAL_PROPERTIES,),
                "CUSTOM_PROMPT": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "add_GEN_CHARACTER": ("GEN_CHARACTER",),
            }
        }

    RETURN_TYPES = ("GEN_CHARACTER",)
    FUNCTION = "generate"
    CATEGORY = "Bjornulf"

    def select_value(self, options, current_value, rng):
        if current_value == "RANDOM":
            valid_options = [
                opt for opt in options if opt not in ["RANDOM", "NONE"]]
            return rng.choice(valid_options)
        elif current_value == "NONE":
            return ""
        return current_value
    
    def generate(self, enabled, number_of_creatures, seed, location_on_image, creature_type, land_animal, water_animal,
                show_creature_description, size, temperament, special_ability, features, 
                magical_properties, CUSTOM_PROMPT, add_GEN_CHARACTER=None):
        
        if not enabled:
            return (add_GEN_CHARACTER if add_GEN_CHARACTER else "",)

        rng = random.Random(seed)

        values = {
            'location_on_image': self.select_value(self.INPUT_TYPES()["required"]["location_on_image"][0], location_on_image, rng),
            'creature_type': self.select_value(self.INPUT_TYPES()["required"]["creature_type"][0], creature_type, rng),
            'size': self.select_value(self.INPUT_TYPES()["required"]["size"][0], size, rng),
            'land_animal': self.select_value(self.INPUT_TYPES()["required"]["land_animal"][0], land_animal, rng),
            'water_animal': self.select_value(self.INPUT_TYPES()["required"]["water_animal"][0], water_animal, rng),
            'temperament': self.select_value(self.INPUT_TYPES()["required"]["temperament"][0], temperament, rng),
            'special_ability': self.select_value(self.INPUT_TYPES()["required"]["special_ability"][0], special_ability, rng),
            'features': self.select_value(self.INPUT_TYPES()["required"]["features"][0], features, rng),
            'magical_properties': self.select_value(self.INPUT_TYPES()["required"]["magical_properties"][0], magical_properties, rng),
        }

        desc_parts = []
        
        # Location
        if values['location_on_image']:
            desc_parts.append(f"On the {values['location_on_image']} of the image:")

        # Basic description
        base_desc = f"{number_to_word(number_of_creatures)} {values['size']} {values['creature_type']}"
        desc_parts.append(base_desc)

        # Add creature description if enabled
        if show_creature_description and values['creature_type'] in SharedLists.CREATURE_TYPES:
            desc_parts.append(f"({SharedLists.CREATURE_TYPES[values['creature_type']]['description']})")
                
        # Animals
        if values['land_animal']:
            desc_parts.append(values['land_animal'])
        if values['water_animal']:
            desc_parts.append(values['water_animal'])
                        
        # Temperament
        if values['temperament']:
            desc_parts.append(f"with a {values['temperament']} nature")

        # Features
        if values['features']:
            desc_parts.append(f"covered in {values['features']}")

        # Special ability
        if values['special_ability']:
            desc_parts.append(f"possessing {values['special_ability']} abilities")

        # Magical properties
        if values['magical_properties']:
            desc_parts.append(f"imbued with {values['magical_properties']}")

        # Custom prompt
        if CUSTOM_PROMPT.strip():
            desc_parts.append(CUSTOM_PROMPT.strip())

        # Combine description
        # Use careful join logic to prevent unwanted commas
        if values['location_on_image']:
            # Treat the first part separately to avoid a leading comma
            character_desc = desc_parts[0] + " " + ", ".join(desc_parts[1:])
        else:
            character_desc = ", ".join(desc_parts)

        if number_of_creatures > 1:
            final_description = f"{'-' * number_of_creatures} {character_desc}"
        else:
            final_description = f"- {character_desc}"

        if add_GEN_CHARACTER:
            return (f"{add_GEN_CHARACTER}\n{final_description}",)
        return (final_description,)