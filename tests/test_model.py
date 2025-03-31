import unittest
from unittest.mock import patch
from k3.model import BezetError, Rij, Stoel, Vak, maak_vakken, reserveer_plaatsen

class ModelTest(unittest.TestCase):
    def test_maak_vakken(self):
        records = [
            (0, 10, 10, 30, 50, 10),
            (1, 10, 10, 40, 60, 5)
        ]
        with patch('k3.model.select_plaatsen') as mock_select_plaatsen:
            mock_select_plaatsen.return_value = records
            vakken = maak_vakken()
            self.assertEqual(len(records), len(vakken))
            self.assertEqual(vakken[0].get_stoel(0, 0).prijs, 30)
            self.assertEqual(vakken[0].get_stoel(9, 9).prijs, 48)
            self.assertEqual(vakken[1].get_stoel(0, 0).prijs, 40)
            self.assertEqual(vakken[1].get_stoel(9, 9).prijs, 56)

    def test_reserveer_plaatsen(self):
        vakken = [
            Vak(0, 10, 10, 30, 50, 10),
            Vak(1, 10, 10, 40, 60, 5)
        ]
        reservaties = [
            (1, 'Joske', None, 0, 3, 2),
            (2, 'Marieke', None, 1, 9, 9)
        ]
        with patch('k3.model.select_reservaties') as mock_select_reservaties:
            mock_select_reservaties.return_value = reservaties
            vakken = reserveer_plaatsen(vakken)
            self.assertTrue(vakken[0].rijen[3].is_stoel_bezet(2))
            self.assertTrue(vakken[1].rijen[9].is_stoel_bezet(9))
            
    def test_rij_stoelen(self):
        aantal_stoelen = 10
        prijs = 50
        rij = Rij(0, 0, aantal_stoelen, prijs)
        self.assertEqual(len(rij.stoelen), aantal_stoelen)
        totaalprijs_oracle = aantal_stoelen * prijs
        totaalprijs = sum([stoel.prijs for stoel in rij.stoelen])
        self.assertEqual(totaalprijs_oracle, totaalprijs)

    def test_stoel_bezet(self):
        stoel = Stoel(0, 0, 0, 10)
        stoel.bezet_stoel()
        with self.assertRaises(BezetError):
            stoel.bezet_stoel()

    def test_vak_bezet_stoel(self):
        start_prijs = 10
        eind_prijs = 21
        step_prijs = 3
        aantal_rijen = 12
        aantal_stoelen = 2
        vak = Vak(0, aantal_rijen, aantal_stoelen, start_prijs, eind_prijs, step_prijs)   
        vak.bezet_stoel(0, 0)
        with self.assertRaises(BezetError):
            vak.bezet_stoel(0, 0)

    def test_vak_prijs(self):
        start_prijs = 10
        eind_prijs = 22
        step_prijs = 3
        aantal_rijen = 12
        aantal_stoelen = 2
        vak = Vak(0, aantal_rijen, aantal_stoelen, start_prijs, eind_prijs, step_prijs)
        prijs_rij0_oracle = 10
        prijs_rij3_oracle = 10
        prijs_rij4_oracle = 14
        prijs_rij7_oracle = 14
        prijs_rij8_oracle = 18
        prijs_rij11_oracle = 18
        self.assertAlmostEqual(prijs_rij0_oracle, vak.get_prijs(0, 0))
        self.assertAlmostEqual(prijs_rij3_oracle, vak.get_prijs(3, 0))
        self.assertAlmostEqual(prijs_rij4_oracle, vak.get_prijs(4, 0))
        self.assertAlmostEqual(prijs_rij7_oracle, vak.get_prijs(7, 0))
        self.assertAlmostEqual(prijs_rij8_oracle, vak.get_prijs(8, 0))
        self.assertAlmostEqual(prijs_rij11_oracle, vak.get_prijs(11, 0))
    
     

if __name__ == '__main__':
    unittest.main()