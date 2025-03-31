DROP TABLE if exists reservatie;
DROP TABLE if exists plaats;

CREATE TABLE plaats (
    vaknr INTEGER PRIMARY KEY NOT NULL,
    aantal_rijen int NOT NULL,
    aantal_stoelen int NOT NULL,
    start_prijs float,
    eind_prijs float,
    step_prijs int
);

CREATE TABLE reservatie(
    nr INTEGER PRIMARY KEY NOT NULL,
    voornaam TEXT NOT NULL,
    achternaam TEXT,
    vaknr int references plaats(vaknr) NOT NULL,
    rijnr int NOT NULL,
    stoelnr int NOT NULL
);

INSERT INTO plaats (aantal_rijen, aantal_stoelen, start_prijs, eind_prijs, step_prijs) 
            VALUES (10, 10, 30, 50, 10), (10, 10, 40, 60, 5);
INSERT INTO reservatie (nr, voornaam, achternaam, vaknr, rijnr, stoelnr)
            VALUES (1, 'Joske', 'Vermeulen', 1, 3, 5);
