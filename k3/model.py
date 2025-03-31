from dataclasses import dataclass
from k3.storage import insert_reservatie, select_plaatsen, select_reservaties
import logging

logger = logging.getLogger(__name__)
class BezetError(Exception):
    def __init__(self, rijnr, stoelnr):
        self.rijnr = rijnr
        self.stoelnr = stoelnr
        super().__init__(f"rij {self.rijnr} stoel {self.stoelnr} is bezet")

class Stoel():
    def __init__(self, vak:int, rij:int, stoelnr:int, prijs:float):
        self.vak = vak
        self.rij = rij
        self.stoelnr = stoelnr
        self.bezet = False
        self.prijs = prijs
    def bezet_stoel(self):
        if self.bezet:
            logger.error("Stoelnr %s in vak %s op rijnr %s is bezet.", self.stoelnr, self.vak, self.rij)
            raise BezetError(self.rij, self.stoelnr)
        self.bezet = True
    def __str__(self):
        return f"{self.vak}: rij({self.rij}, stoel({self.stoelnr}), prijs({self.prijs}))"
    
class Rij():
    def __init__(self, vak:int, rij:int, aantal_stoelen:int, prijs:float):
        self.stoelen = []
        self.vaknr = vak
        self.rijnr = rij
        self.aantal_stoelen = aantal_stoelen
        for nr in range(aantal_stoelen):
            self.stoelen.append(Stoel(vak, rij, nr, prijs))
    
    def bezet_stoel(self, nr: int):
        self.stoelen[nr].bezet_stoel()

    def is_stoel_bezet(self, nr:int):
        return self.stoelen[nr].bezet

    def __repr__(self):
        return "\n".join([str(stoel) for stoel in self.stoelen])



class Vak():
    def __init__(self, vak:int, aantal_rijen:int, aantal_stoelen:int, start_prijs:float, eind_prijs:float, step_prijs:int):
        logger.info("Maak Vak met nr %s, aantal rijen: %s, aantal stoelen: %s", vak, aantal_rijen, aantal_stoelen)
        if aantal_rijen % step_prijs != 0:
            raise ValueError("aantal_rijen moet deelbaar zijn door step_prijs")
        self.vaknr = vak
        self.rijen = []
        self.aantal_rijen = aantal_rijen
        self.aantal_stoelen = aantal_stoelen
        rijnr = 0
        for prijs_index in range(step_prijs):
            prijs = start_prijs + (prijs_index * (eind_prijs-start_prijs)/step_prijs)
            for stap in range(aantal_rijen // step_prijs):
                self.rijen.append(Rij(vak, rijnr, aantal_stoelen, prijs))
                rijnr += 1
    def get_prijs(self, rijnr:int, stoelnr:int) -> float:
        return self.rijen[rijnr].stoelen[stoelnr].prijs
    
    def bezet_stoel(self, rijnr:int, stoelnr:int):
        self.rijen[rijnr].bezet_stoel(stoelnr)

    def get_stoel(self, rij:int, stoel:int):
        return self.rijen[rij].stoelen[stoel]

    def __repr__(self):
        return f"vaknr: {self.vaknr}, aantal_rijen: {self.aantal_rijen}"
    
class Reservatie():
    def __init__(self, nr:int, naam:str, stoel:Stoel):
        self.nr = nr
        self.naam = naam
        self.plaats = stoel

@dataclass
class GereserveerdePlaats:
    vaknr:int
    rijnr:int
    stoelnr:int

def maak_vakken():
    """Maakt het "vloerplan" met vakken, rijen en stoelen volgens tabel "plaats"

    Returns:
        list[Vak]: een list met de Vak-objecten
    """
    logger.debug("In maak_vakken")
    plaatsen = select_plaatsen()
    vakken = []
    for vak_db in plaatsen:
        vaknr, aantal_rijen, aantal_stoelen, start_prijs, eind_prijs, step_prijs = vak_db
        vak = Vak(vaknr, aantal_rijen, aantal_stoelen, start_prijs, eind_prijs, step_prijs)
        vakken.append(vak)
    return vakken

def bezet_plaats(vakken, vaknr, rijnr, stoelnr):
    """reserveert een stoel op een rij in een vak en past de list 'vakken' aan

    Args:
        vakken (list[Vak]): het 'vloerplan' met alle vakken
        vaknr (int): het vaknr van de stoel die gereserveerd moet worden
        rijnr (int): Het rijnr van de stoel die gereserveerd moet worden
        stoelnr (int): Het stoelnr van de stoel die gereserveerd moet woren

    Raises:
        ValueError: Het vaknummer is onbekend

    Returns:
        list[Vak]: het nieuwe 'vloerplan'
    """
    logger.debug("in bezet_plaats (vaknr=%s, rijnr=%s, stoelnr=%s)", vaknr, rijnr, stoelnr)
    vak = next(filter(lambda v:v.vaknr == vaknr, vakken), None) #zoek het vak met nr 'vaknr'
    if vak is None:
        logger.error('Vak met vaknr %s niet gevonden', vaknr)
        raise ValueError(f"Vak met nr {vaknr} bestaat niet.") 
    vak.bezet_stoel(rijnr, stoelnr)
    return vakken

def reserveer_plaatsen(vloerplan:list[Vak])->list[Vak] :
    """Reserveert de plaatsen in het 'vloerplan' op basis van de databank

    Args:
        vloerplan (list[Vak]): Het lege 'vloerplan' (zonder reservaties)

    Returns:
        list[Vak]: Het nieuwe 'vloerplan' (met reservaties uit de databank)
    """
    logger.debug("In reserveer_plaatsen")
    reservaties_db = select_reservaties()
    for reservatie_db in reservaties_db:
        _, _, _, vaknr, rijnr, stoelnr = reservatie_db
        logger.debug('reserveer vak %s (rij:%s, stoel:%s)', vaknr, rijnr, stoelnr)
        vloerplan = bezet_plaats(vloerplan, vaknr, rijnr, stoelnr)
    return vloerplan

def get_vloerplan() -> list[Vak]:
    """Maakt het 'vloerplan' met de reeds gereserveerde stoelen op basis van de databank

    Returns:
        list[Vak]: Het 'vloerplan' met de reservaties
    """
    vakken = maak_vakken()
    vloerplan = reserveer_plaatsen(vakken)
    return vloerplan

def reserveer_stoel(voornaam, vaknr, rijnr, stoelnr):
    """Reserveer een stoel voor 'voornaam'

    Args:
        voornaam (str): De naam van de persoon die wil reserveren
        vaknr (int): Het vaknummer van de stoel die gereserveerd moet worden
        rijnr (int): Het rijnummer van de stoel die gereserveerd moet worden
        stoelnr (int): Het stoelnummer van de stoel die gereserveerd moet worden

    Raises:
        BezetError: De stoel is al gereserveerd

    Returns:
        int: het nummer van de reservatie
    """
    vloerplan = get_vloerplan()
    vak:Vak = next(filter(lambda v:v.vaknr == vaknr, vloerplan), None)
    vak.bezet_stoel(rijnr, stoelnr) #controleer of stoel al gereserveerd is
    logger.info("Reserveer stoelnr %s op rij %s in vak %s voor %s", stoelnr, rijnr, vak, voornaam)
    reservatienr = insert_reservatie(voornaam, vaknr, rijnr, stoelnr)
    return reservatienr