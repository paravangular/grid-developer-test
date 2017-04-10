import unittest
import viagogo

class TestWorld(unittest.TestCase):
	def setUp(self):
		self.w = viagogo.World()

	def test_itemgetter(self):
		self.w.world[3][1] = 5
		self.assertEqual(self.w.world[3][1], self.w[(1, 3)])

	def test_itemsetter_when_empty(self):
		self.w[(1, 3)] = 5
		self.assertEqual(self.w.world[3][1], 5)

	def test_itemsetter_when_occupied(self):
		self.w.world[3][1] = 5
		self.w[(1, 3)] = 10
		self.assertEqual(self.w.world[3][1], 5)

	def test_empty(self):
		self.assertTrue(self.w.empty(3, 5))

	def test_not_empty(self):
		self.w.world[5][3] = 8
		self.assertFalse(self.w.empty(3, 5))

	def test_size(self):
		self.assertEqual(self.w.size(), (viagogo.WORLD_X_SIZE, viagogo.WORLD_Y_SIZE))

	def test_events_coordinates(self):
		self.w.world[0][1] = 2
		self.w.world[5][3] = 8
		self.w.world[9][8] = 4
		self.assertEqual(self.w.events_coordinates(), [[2, (1, 0)], [8, (3, 5)], [4, (8, 9)]])


class TestEvent(unittest.TestCase):
	def setUp(self):
		self.event = viagogo.Event([1.00, 2.05, 100.00])

	def test_cheapest_ticket(self):
		self.assertEqual(self.event.cheapest_ticket_price(), 1.00)


class TestMain(unittest.TestCase):
	def test_valid_input_format(self):
		# arbitrary valid point
		self.assertTrue(viagogo.valid_input_format("4,    2"))

		# edge cases
		self.assertTrue(viagogo.valid_input_format("    0, 0    "))
		self.assertTrue(viagogo.valid_input_format(" -10, -10"))
		self.assertTrue(viagogo.valid_input_format("-10, 10   "))
		self.assertTrue(viagogo.valid_input_format("10,-10"))
		self.assertTrue(viagogo.valid_input_format("10,      10"))

	def test_invalid_input_format(self):
		# empty string and whitespace
		self.assertFalse(viagogo.valid_input_format(""))
		self.assertFalse(viagogo.valid_input_format(" "))
		self.assertFalse(viagogo.valid_input_format("\n"))

		# missing coordinates
		self.assertFalse(viagogo.valid_input_format("4, "))
		self.assertFalse(viagogo.valid_input_format(", 2"))

		# no comma
		self.assertFalse(viagogo.valid_input_format("4 2"))

		# wrong number format (only accept integers)
		self.assertFalse(viagogo.valid_input_format("4.00, 2"))
		self.assertFalse(viagogo.valid_input_format("0xffff, 2"))
		self.assertFalse(viagogo.valid_input_format("--1, 2"))
		self.assertFalse(viagogo.valid_input_format("1E+02, 2"))

		# non-numeric characters
		self.assertFalse(viagogo.valid_input_format("this is a string"))
		self.assertFalse(viagogo.valid_input_format(",./;'[]\-="))
		self.assertFalse(viagogo.valid_input_format("-"))
		self.assertFalse(viagogo.valid_input_format("'"))
		self.assertFalse(viagogo.valid_input_format("田中さんにあげて下さい"))
		self.assertFalse(viagogo.valid_input_format("ﾟ･✿ヾ╲(｡◕‿◕｡)╱✿･ﾟ"))
		self.assertFalse(viagogo.valid_input_format("😍"))
		self.assertFalse(viagogo.valid_input_format("$HOME"))
		self.assertFalse(viagogo.valid_input_format("%d"))

	def test_valid_input_range(self):
		# test arbitrary valid point
		self.assertTrue(viagogo.valid_input_range((4, 2)))

		# test edge cases
		self.assertTrue(viagogo.valid_input_range((0, 0)))
		self.assertTrue(viagogo.valid_input_range((-10, -10)))
		self.assertTrue(viagogo.valid_input_range((10, -10)))
		self.assertTrue(viagogo.valid_input_range((-10, 10)))
		self.assertTrue(viagogo.valid_input_range((10, 10)))

	def test_invalid_input_range(self):
		self.assertFalse(viagogo.valid_input_range((-12, -6)))
		self.assertFalse(viagogo.valid_input_range((11, -6)))
		self.assertFalse(viagogo.valid_input_range((8, -15)))
		self.assertFalse(viagogo.valid_input_range((10, 30)))

	def test_parse_input(self):
		self.assertTrue(viagogo.parse_input("4,    2"), (4, 2))
		self.assertTrue(viagogo.parse_input("    0, 0    "), (0, 0))
		self.assertTrue(viagogo.parse_input(" -20, -10"), (-20, -10))
		self.assertTrue(viagogo.parse_input("-10, 30   "), (-10, 30))
		self.assertTrue(viagogo.parse_input("10,-10"), (10, -10))
		self.assertTrue(viagogo.parse_input("10,      10"), (10, 10))

	def test_manhattan_distance(self):
		self.assertTrue(viagogo.manhattan_distance((5, 6), (10, 10)), 9)
		self.assertTrue(viagogo.manhattan_distance((-5, 6), (-10, 10)), 9)
		self.assertTrue(viagogo.manhattan_distance((-5, 6), (10, -10)), 9)

	def test_offset(self):
		self.assertTrue(viagogo.offset((0, 0)), (-viagogo.WORLD_X_MIN, -viagogo.WORLD_Y_MIN))

	def test_closest_events(self):
		self.w = viagogo.World()

		self.w[(0, 0)] = viagogo.Event([1.00, 2.00, 3.00])
		self.w[(0, 1)] = viagogo.Event([1.00, 2.00, 3.00])
		self.w[(1, 1)] = viagogo.Event([1.00, 2.00, 3.00])
		self.w[(5, 0)] = viagogo.Event([1.00, 2.00, 3.00])
		self.w[(2, 1)] = viagogo.Event([1.00, 2.00, 3.00])

		self.assertTrue(viagogo.closest_events(self.w, (0, 0), 3), [[1, 0], [2, 1], [2, 2]])
		self.assertTrue(viagogo.closest_events(self.w, (0, 0), 5), [[1, 0], [2, 1], [2, 2], [5, 3], [4, 5]])
		self.assertTrue(viagogo.closest_events(self.w, (0, 0), 7), [[1, 0], [2, 1], [2, 2], [5, 3], [4, 5]])

if __name__ == '__main__':
	unittest.main()