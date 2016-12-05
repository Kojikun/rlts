# creates rows in Item table
# included in rlts.py, ran in init_db
import sqlite3


def main(database):
    db = database
    c = db.cursor()

    certified = ["Acrobat",
                 "Aviator",
                 "Goalkeeper",
                 "Guardian",
                 "Juggler",
                 "Paragon",
                 "Playmaker",
                 "Scorer",
                 "Show-Off",
                 "Sniper",
                 "Striker",
                 "Sweeper",
                 "Tactician",
                 "Turtle",
                 "Victor"]

    painted = ["Black",
               "Burnt Sienna",
               "Cobalt",
               "Crimson",
               "Forest Green",
               "Grey",
               "Lime",
               "Orange",
               "Pink",
               "Purple",
               "Saffron",
               "Sky-Blue",
               "Titanium White"]

    c.execute("insert into Item (name) values ('Key');")
    c.execute("insert into Item (name, collection) values ('Champions Crate 1', 'Champions Crate 1');")
    c.execute("insert into Item (name, collection) values ('Champions Crate 2', 'Champions Crate 2');")
    c.execute("insert into Item (name, collection) values ('Champions Crate 3', 'Champions Crate 3');")

    # bodies
    bodies = ["1Dominus GT",
              "2Road Hog XL",
              "1Takumi RX-T",
              "2X-Devil MK2",
              "3Breakout Type-S"]

    # insert uncertified bodies before certified bodies
    for b in bodies:
        c.execute("insert into Item (name, type, quality, collection) values (?, ?, ?, ?)",
                  [b[1:], 'Body', 'Import', 'Champions Crate ' + b[0]])
    for cert in certified:
        for b in bodies:
            c.execute("insert into Item (name, type, quality, collection, certified) values (?, ?, ?, ?, ?)",
                      [b[1:], 'Body', 'Import', 'Champions Crate ' + b[0], cert])

    # uncommon painted wheels
    uwheels = ["Alchemist",
               "Almas",
               "Dieci",
               "Falco",
               "Invader",
               "Lowrider",
               "Neptune",
               "Octavian",
               "OEM",
               "Rat Rod",
               "Spyder",
               "Stern",
               "Sunburst",
               "Trahere",
               "Tunica",
               "Veloce",
               "Vortex"]

    for p in painted:
        for w in uwheels:
            c.execute("insert into Item (name, type, quality, painted) values (?, ?, ?, ?)",
                      [w, "Wheels", "Uncommon", p])
    for cert in certified:
        for p in painted:
            for w in uwheels:
                c.execute("insert into Item (name, type, quality, painted, certified) values (?, ?, ?, ?, ?)",
                          [w, "Wheels", "Uncommon", p, cert])

    # rare wheels
    rwheels = ["Asterias",
               "Zeta"]

    for w in rwheels:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [w, "Wheels", "Rare"])
    for p in painted:
        for w in rwheels:
            c.execute("insert into Item (name, type, quality, painted) values (?, ?, ?, ?)",
                      [w, "Wheels", "Rare", p])
    for cert in certified:
        for w in rwheels:
            c.execute("insert into Item (name, type, quality, certified) values (?, ?, ?, ?)",
                      [w, "Wheels", "Rare", cert])
    for cert in certified:
        for p in painted:
            for w in rwheels:
                c.execute("insert into Item (name, type, quality, painted, certified) values (?, ?, ?, ?, ?)",
                          [w, "Wheels", "Rare", p, cert])

    # Very rare wheels
    vwheels = ["1Chakram",
               "3Troika"]

    for w in vwheels:
        c.execute("insert into Item (name, type, quality, collection) values (?, ?, ?, ?)",
                  [w[1:], "Wheels", "Very Rare", "Champions Crate " + w[0]])
    for p in painted:
        for w in vwheels:
            c.execute("insert into Item (name, type, quality, collection, painted) values (?, ?, ?, ?, ?)",
                      [w[1:], "Wheels", "Very Rare", "Champions Crate " + w[0], p])
    for cert in certified:
        for w in vwheels:
            c.execute("insert into Item (name, type, quality, collection, certified) values (?, ?, ?, ?, ?)",
                      [w[1:], "Wheels", "Very Rare", "Champions Crate " + w[0], cert])
    for cert in certified:
        for p in painted:
            for w in vwheels:
                c.execute("insert into Item (name, type, quality, collection, painted, certified) values (?, ?, ?, ?, ?, ?)",
                          [w[1:], "Wheels", "Very Rare", "Champions Crate " + w[0], p, cert])

    # exotic wheels
    ewheels = ["1Photon",
               "1Looper",
               "2Lobo",
               "2Lightning",
               "3Discotheque",
               "3Pulsus"]

    for w in ewheels:
        c.execute("insert into Item (name, type, quality, collection) values (?, ?, ?, ?)",
                  [w[1:], "Wheels", "Exotic", "Champions Crate " + w[0]])
    for p in painted:
        for w in ewheels:
            c.execute("insert into Item (name, type, quality, collection, painted) values (?, ?, ?, ?, ?)",
                      [w[1:], "Wheels", "Exotic", "Champions Crate " + w[0], p])
    for cert in certified:
        for w in ewheels:
            c.execute("insert into Item (name, type, quality, collection, certified) values (?, ?, ?, ?, ?)",
                      [w[1:], "Wheels", "Exotic", "Champions Crate " + w[0], cert])
    for cert in certified:
        for p in painted:
            for w in ewheels:
                c.execute("insert into Item (name, type, quality, collection, painted, certified) values (?, ?, ?, ?, ?, ?)",
                          [w[1:], "Wheels", "Exotic", "Champions Crate " + w[0], p, cert])

    # Limited Wheels
    c.execute("insert into Item (name, type, quality) values ('Carriage', 'Wheels', 'Limited')")
    c.execute("insert into Item (name, type, quality) values ('Goldstone [Alpha Reward]', 'Wheels', 'Limited')")

    # Very Rare drop boosts
    vboost = ["Toon Smoke",
              "Frostbite",
              "Hearts",
              "Lightning",
              "Ink",
              "Treasure"]

    for b in vboost:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [b, "Boost", "Very Rare"])

    for cert in certified:
        for b in vboost:
            c.execute("insert into Item (name, type, quality, certified) values (?, ?, ?, ?)",
                      [b, "Boost", "Very Rare", cert])

    # special exception for polygonal, champ 2 crate
    c.execute("insert into Item (name, type, quality, collection) values ('Polygonal', 'Boost', 'Very Rare', 'Champions Crate 2')")
    for cert in certified:
        c.execute("insert into Item (name, type, quality, collection, certified) values (?, ?, ?, ?, ?)",
                  ["Polygonal", "Boost", "Very Rare", "Champions Crate 2", cert])

    # import boosts
    iboost = ["2Pixel Fire",
              "1Trinity",
              "3Dark Matter",
              "3Hypernova"]

    for b in iboost:
        c.execute("insert into Item (name, type, quality, collection) values (?, ?, ?, ?)",
                  [b[1:], "Boost", "Import", "Champions Crate " + b[0]])
    for cert in certified:
        for b in iboost:
            c.execute("insert into Item (name, type, quality, collection, certified) values (?, ?, ?, ?, ?)",
                      [b[1:], "Boost", "Import", "Champions Crate " + b[0], cert])

    # Limited boosts
    lboost = ["Gold Rush [Alpha Reward]",
              "Candy Corn",
              "Xmas",
              "Netherworld"]

    for b in lboost:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [b, "Boost", "Limited"])

    # Uncommon Antennas
    uantenna = ["Rainbow Flag",
                "Waffle",
                "Rubber Duckie",
                "Rocket",
                "Pinata",
                "Parrot",
                "Hula Girl",
                "Genie Lamp",
                "Foam Finger",
                "Venus Flytrap",
                "Sunflower",
                "Rose",
                "Donut",
                "Balloon Dog",
                "Disco Ball",
                "Cupcake",
                "Chick Magnet",
                "Candle",
                "Alien",
                "Harpoon",
                "Seastar",
                "Trident"]

    for a in uantenna:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [a, "Antenna", "Uncommon"])

    # Limited Antennas
    lantenna = ["Gold Nugget [Beta Reward]",
                "Calavera",
                "Fuzzy Brute",
                "Fuzzy Vamp",
                "Candy Cane",
                "Holiday Gift",
                "Fuzzy Skull"]

    for a in lantenna:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [a, "Antenna", "Limited"])

    # Black Market Decals
    bdecal = ["Slipstream",
              "Parallax",
              "Labyrinth",
              "Heatwave"]

    for d in bdecal:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [d, "Decal", "Black Market"])
    for cert in certified:
        for d in bdecal:
            c.execute("insert into Item (name, type, quality, certified) values (?, ?, ?, ?)",
                      [d, "Decal", "Black Market", cert])

    # Rare non-crate decals
    rdecal = ["Breakout: Junk Food",
              "Dominus: Royalty",
              "Octane: Racer",
              "Venom: Flex"]

    for d in rdecal:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [d, "Decal", "Rare"])
    for cert in certified:
        for d in rdecal:
            c.execute("insert into Item (name, type, quality, certified) values (?, ?, ?, ?)",
                      [d, "Decal", "Rare", cert])

    # Rare crate decals
    rcdecal = ["1Takumi: Combo",
               "1Breakout: Vice",
               "1Dominus: Pollo Caliente",
               "1Dominus: Arcana",
               "1Breakout: Shibuya",
               "2Octane: Dragon Lord",
               "2Venom: Nine Lives",
               "2Road Hog: Carbonated",
               "2Takumi: Whizzle",
               "2Merc: Narwhal",
               "3Breakout: Falchion",
               "3Breakout: Turbo",
               "3Dominus: Mondo",
               "3Octane: Shisa",
               "3Masamune: Oni"]

    for d in rcdecal:
        c.execute("insert into Item (name, type, quality, collection) values (?, ?, ?, ?)",
                  [d[1:], "Decal", "Rare", "Champions Crate " + d[0]])
    for cert in certified:
        for d in rcdecal:
            c.execute("insert into Item (name, type, quality, collection, certified) values (?, ?, ?, ?, ?)",
                      [d[1:], "Decal", "Rare", "Champions Crate " + d[0], cert])

    # very rare decals
    vdecal = ["1Takumi: Anubis",
              "1Breakout: Dot Matrix",
              "1Dominus: Snakeskin",
              "2Octane: Distortion",
              "2Merc: Warlock",
              "2X-Devil: Snake Skin",
              "3Takumi: Distortion",
              "3Breakout: Snakeskin",
              "3Octane: MG-88"]

    for d in vdecal:
        c.execute("insert into Item (name, type, quality, collection) values (?, ?, ?, ?)",
                  [d[1:], "Decal", "Very Rare", "Champions Crate " + d[0]])
    for cert in certified:
        for d in vdecal:
            c.execute("insert into Item (name, type, quality, collection, certified) values (?, ?, ?, ?, ?)",
                      [d[1:], "Decal", "Very Rare", "Champions Crate " + d[0], cert])

    # uncommon toppers
    utopper = ["Unicorn",
               "Traffic Cone",
               "Tiara",
               "Shuriken",
               "Rhino Horns",
               "Mouse Trap",
               "Rasta",
               "Police Hat",
               "Plunger",
               "Paper Boat",
               "Graduation Cap",
               "Bowler",
               "Fruit Hat",
               "Brodie Helmet",
               "Homburg",
               "Derby",
               "Deerstalker",
               "Deadmau5",
               "Cockroach",
               "Chef's Hat",
               "Chainsaw",
               "Captain's Hat",
               "Work Boot",
               "Birthday Cake",
               "Biker Cap",
               "Beret",
               "Antlers",
               "Pigeon",
               "Little Bow",
               "Cattleman",
               "Pork Pie",
               "Ivy Cap",
               "Light Bulb",
               "Party Hat",
               "Trucker Hat",
               "Visor",
               "Baseball Cap [F]",
               "Baseball Cap [B]",
               "Foam Hat"]

    for t in utopper:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [t, "Topper", "Uncommon"])
    for cert in certified:
        for t in utopper:
            c.execute("insert into Item (name, type, quality, certified) values (?, ?, ?, ?)",
                      [t, "Topper", "Uncommon", cert])

    # rare toppers
    rtopper = ["Robo-Visor",
               "Wildcat Ears",
               "Drink Helmet",
               "Clamshell"]

    for t in rtopper:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [t, "Topper", "Rare"])
    for cert in certified:
        for t in rtopper:
            c.execute("insert into Item (name, type, quality, certified) values (?, ?, ?, ?)",
                      [t, "Topper", "Rare", cert])

    # limited toppers
    ltopper = ["Gold Cap [Alpha Reward]",
               "Pumpkin",
               "Blitzen",
               "Christmas Tree",
               "Sad Sapling",
               "Santa",
               "White Hat",
               "Bone King",
               "Ghost"]

    for t in ltopper:
        c.execute("insert into Item (name, type, quality) values (?, ?, ?)",
                  [t, "Topper", "Limited"])

    # commit to table
    db.commit()
