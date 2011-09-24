import random
import unittest
import extsea
import rpgdb

class TestSequenceFunctions(unittest.TestCase):
	
	def test_items(self):
		character = extsea.Character('null')
		item = rpgdb.createl('money', 20)
		character.add(item)
		item = rpgdb.createl('money', 54)
		character.add(item)
		self.assertEqual(character.attrib['money'].rlevel, 74)
		
