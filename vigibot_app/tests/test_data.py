__author__ = 'fccoelho'

import unittest
from vigibot.data import get_geocode, get_city_names, get_alerta


class MyTestCase(unittest.TestCase):
    def test_find_geocode_sem_acento(self):
        gc = get_geocode('niteroi')
        self.assertEqual(gc, 3303302)

    def test_find_geocode_sem_acento2(self):
        gc = get_geocode('santo hipolito')
        self.assertEqual(gc, 3160603)
    @unittest.skip
    def test_find_geocode_com_acento_no_começo(self):
        gc = get_geocode('Sao Luis do Curu')
        self.assertEqual(2312601, gc)

    def test_find_geocode_cidade_desconhecida(self):
        gc = get_geocode('sldfk skdjf')
        self.assertEqual([], gc)

    def test_find_geocode_rio(self):
        gc = get_geocode('rio de janeiro')
        self.assertEqual(gc, 3304557)

    def test_find_geocode_senges(self):
        gc = get_geocode('sengés')
        self.assertEqual(gc, 4126306)

    def test_get_alerta(self):
        alerta = get_alerta(3304557, 'dengue')
        self.assertIn(alerta[0], [1, 2, 3, 4])



if __name__ == '__main__':
    unittest.main()
