import random
import re

WORLD_X_SIZE = 21 # -10 to 10
WORLD_Y_SIZE = 21
WORLD_X_MIN = -10
WORLD_Y_MIN = -10

class World:
	def __init__(self):
		self.world = [[None] * WORLD_X_SIZE for y in range(WORLD_Y_SIZE)]

	def __getitem__(self, coordinates):
		x = coordinates[0]
		y = coordinates[1]
		return self.world[y][x]

	def __setitem__(self, coordinates, event):
		x = coordinates[0]
		y = coordinates[1]
		if self.empty(x, y):
			self.world[y][x] = event
		else:
			return False

	def empty(self, x, y):
		return self.world[y][x] is None

	def size(self):
		return (len(self.world[0]), len(self.world))

	def events_coordinates(self):
		x = self.size()[0]
		y = self.size()[1]

		events = []
		for i in range(y):
			for j in range(x):
				if self.world[i][j] is not None:
					events.append([self.world[i][j], (j, i)])

		return events

	def __str__(self):
		x = self.size()[0]
		y = self.size()[1]

		s = ""
		for j in range(y):
			for i in range(x):
				val = self.world[i][j]
				if val is not None:
					s += "{:^4}".format(val.id)
				else:
					s += "{:^4}".format(".")
			s += "\n"

		return s

class Event:
	id_counter = 1

	def __init__(self, tickets):
		self.__id = Event.id_counter
		Event.id_counter += 1
		self.tickets = tickets

	@property
	def id(self):
		return self.__id

	def cheapest_ticket_price(self):
		return min(self.tickets)

	def __repr__(self):
		return str(self.__id)

	def __str__(self):
		return "Event {}".format(self.__id)


def main():
	# generating data
	world = World()
	num_events = random.randint(1, WORLD_X_SIZE * WORLD_Y_SIZE)

	for i in range(num_events):
		x = random.randint(0, WORLD_X_SIZE - 1)
		y = random.randint(0, WORLD_Y_SIZE - 1)
		tickets = generate_tickets()

		# ensures one location only has one event
		while world[(x, y)] is None:
			world[(x, y)] = Event(tickets)

	# prompt, read and parse input
	raw_coor = read_input()
	coordinates = offset(raw_coor)

	# search for closest events
	events = closest_events(world, coordinates, 5)

	print()
	print("Closest events to {}: ".format(raw_coor))
	for [event, dist] in events:
		eid = event.id
		ticket = event.cheapest_ticket_price()
		print("Event {:03} - ${:0.2f}, Distance {:d}".format(eid, ticket, dist)) ##%(eid)s - $%(ticket)s, Distance %(dist)s" % locals())


def generate_tickets():
	return [round(random.uniform(0.01, 1000), 2) for x in range(random.randint(1, 10))]

def read_input():
	while True:
		s = input("Please enter a coordinate: ")

		if not re.match("^\s*?(\-?\d+)\s*,\s*(\-?\d+)\s*?$", s):
			print("Sorry, I didn't understand that. Please input a valid coordinate.")
		else:
			coordinates = tuple(map(int, s.strip().split(',')))

			x_lim = (WORLD_X_MIN, WORLD_X_MIN + WORLD_X_SIZE - 1)
			y_lim = (WORLD_Y_MIN, WORLD_Y_MIN + WORLD_Y_SIZE - 1)

			if coordinates[0] < x_lim[0] or coordinates[0] > x_lim[1]:
				print("Your x coordinates must be between " + str(x_lim) + "!")
			elif coordinates[1] < y_lim[0] or coordinates[1] > y_lim[1]:
				print("Your y coordinates must be between " + str(y_lim) + "!")
			else:
				break

	return coordinates

def offset(coordinates):
	x = coordinates[0] - WORLD_X_MIN
	y = coordinates[1] - WORLD_Y_MIN

	return (x, y)

def manhattan_distance(source, dest):
	return abs(source[0] - dest[0]) + abs(source[1] - dest[1])

def closest_events(world, source, k):
	events = world.events_coordinates()

	for event in events:
		dist = manhattan_distance(source, event[1])
		event[1] = dist

	return sorted(events, key=lambda x: x[1])[0:min(k, len(events))]


main()