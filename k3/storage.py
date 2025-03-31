import sqlite3
import logging
from flask import g, current_app
from pathlib import Path

logger = logging.getLogger(__name__)
_SCRIPTSDIR = 'sqlscripts'

_INSERT_RESERVATIE = """INSERT INTO reservatie (voornaam, achternaam, vaknr, rijnr, stoelnr) VALUES (?, ?, ?, ?, ?)"""
_SELECT_RESERVATIES = """SELECT nr, voornaam, achternaam, vaknr, rijnr, stoelnr FROM reservatie"""
_SELECT_PLAATSEN = """SELECT vaknr, aantal_rijen, aantal_stoelen, start_prijs, eind_prijs, step_prijs FROM plaats"""

def get_connection() -> sqlite3.Connection:
    db = getattr(g, '_database', None)
    if db is None:
        logger.info("Create databank connectie met URI %s", current_app.config['DATABASE_URI'])
        db = g._database = sqlite3.connect(current_app.config['DATABASE_URI'])
    return db

def init_db():
    sql_commando = _load_script("createdb.sql")
    with get_connection() as con:
        logger.info("Databank gecreëerd met script %s", sql_commando)
        con.executescript(sql_commando)
        con.commit()

def select_reservaties() -> list[tuple]:
    logger.debug("in select_reservaties")
    with get_connection() as con:
        cursor = con.cursor()
        resultaat = cursor.execute(_SELECT_RESERVATIES)
        return resultaat.fetchall()

def select_plaatsen() -> list[tuple]:
    logger.debug("in select_plaatsen")
    with get_connection() as con:
        cursor = con.cursor()
        resultaat = cursor.execute(_SELECT_PLAATSEN)
        return resultaat.fetchall()
    
def insert_reservatie(voornaam:str, vaknr:int, rijnr:int, stoelnr:int) -> int:
    logger.info("Voeg reservatie toe voor %s (vak: %s, rij: %s, stoel: %s)", voornaam, vaknr, rijnr, stoelnr)
    with get_connection() as con:
        cursor = con.cursor()
        cursor.execute(_INSERT_RESERVATIE, (voornaam, None, vaknr, rijnr, stoelnr))
        con.commit()
        return cursor.lastrowid
    
def _load_script(naam):
    path = Path(current_app.root_path, _SCRIPTSDIR, naam)
    logger.info("Laad sql script %s", path)
    with open(path) as f:
        data = f.read()
    return data