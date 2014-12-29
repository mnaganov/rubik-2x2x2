#!/usr/bin/env python

from collections import deque
import copy

from euclid import *

class Color:
  WHITE = 0
  RED = 1
  GREEN = 2
  YELLOW = 3
  ORANGE = 4
  BLUE = 5
  FIRST = WHITE
  LAST = BLUE + 1
  ANY = LAST + 1

class Side:
  FRONT = 0
  LEFT  = 1
  UPPER = 2
  BACK  = 3
  RIGHT = 4
  DOWN  = 5
  FIRST = FRONT
  LAST = DOWN + 1

  @staticmethod
  def minimal_list():
    return [Side.FRONT, Side.UPPER, Side.RIGHT]

class Tile:
  RT = 0
  RB = 1
  LB = 2
  LT = 3
  FIRST = RT
  LAST = LT + 1

class Turn:
  T90 = 0
  T180 = 1
  T270 = 2
  FIRST = T90
  LAST = T270 + 1

  def __init__(self, side, angle):
    self._side = side
    self._angle = angle

  def side(self):
    return self._side

  def angle(self):
    return self._angle

  def reverse(self):
    if self._angle == Turn.T180:
      return self
    if self._angle == Turn.T90:
      return Turn(self._side, Turn.T270)
    else:
      return Turn(self._side, Turn.T90)

class State:
  X = 0
  Y = 1
  Z = 2

  def __init__(self, tiles_by_sides_6_x_4):
    self._state = tuple(tuple(l) for l in tiles_by_sides_6_x_4)

  def verify(self):
    # verify that all corners do present
    # ??? What about any ???
    return True

  def get_equivalents(self):
    return [State(copy.deepcopy(self._state))]
    # _X = State.X
    # _Y = State.Y
    # _Z = State.Z
    # _C = Turn.T90
    # _C2 = Turn.T180
    # _CC = Turn.T270
    # return [
    #   self._rotate_cube([]),
    #   self._rotate_cube([(_Z, _C), (_Y, _C)])
    #   self._rotate_cube([(_Z, _CC), (_Y, _CC)]),
    #   self._rotate_cube([(_Z, _CC)]),
    #   self._rotate_cube([(_Y, _C)]),
    #   self._rotate_cube([(_Z, _C2), (_X, _C)]),
    #   self._rotate_cube([(_Z, _C2)]),
    #   self._rotate_cube([(_X, _CC), (_Z, _C)]),
    #   self._rotate_cube([(_Y, _C), (_Z, _CC)]),
    #   self._rotate_cube([(_Z, _C)]),
    #   self._rotate_cube([(_X, _CC)]),
    #   self._rotate_cube([(_Z, _C2), (_Y, _CC)]),
    #   self._rotate_cube([(_Y, _CC)]),
    #   self._rotate_cube([(_X, _C)]),
    #   self._rotate_cube([(_Y, _C2), (_Z, _C)]),
    #   self._rotate_cube([(_Z, _C), (_Y, _CC)]),
    #   self._rotate_cube([(_Z, _C), (_X, _CC)]),
    #   self._rotate_cube([(_X, _C2)]),
    #   self._rotate_cube([(_Z, _C2), (_X, _CC)]),
    #   self._rotate_cube([(_Z, _C2), (_Y, _C)]),
    #   self._rotate_cube([(_Y, _C2), (_Z, _CC)]),
    #   self._rotate_cube([(_Y, _CC), (_Z, _CC)]),
    #   self._rotate_cube([(_Y, _C2)]),
    #   self._rotate_cube([(_Z, _CC), (_Y, _C)])
    # ]

  def apply(self, turn):
    axis = [State.X, None, State.Z, None, State.Y, None][turn.side()]
    return self._rotate_half_cube(axis, turn.angle())

  def _rotate_cube(self, rotations):
    points = self._state_to_points(self._state)
    # rotate points
    return self._create_state_from_points(points)

  def _rotate_half_cube(self, axis, angle):
    points = self._state_to_points(self._state, positive_axis=axis)
    # rotate points
    return self._create_state_from_points(points)

  def _state_to_points(self, state, positive_axis=[]):
    # return list of points 3d coupled with colors
    return []

  def _create_state_from_points(self, points):
    new_state = copy.deepcopy(self._state)
    # update new_state from points
    return State(new_state)

  def __hash__(self):
    return hash(self._state)

  def __eq__(self, other):
    return self._state == other._state

class Solver:
  def __init__(self, initial_state, final_state=None):
    if not final_state:
      final_state = Solver.solved_state()
    self._initial_state = initial_state
    self._final_state = final_state
    self._known_states = {initial_state: None}
    self._states_to_check = deque([initial_state])

  def solve(self):
    if not self._phase1():
      return None
    return self._phase2()

  def _phase1(self):
    final_state_eqs = self._final_state.get_equivalents()
    while len(self._states_to_check) > 0 and \
          not self._find_known_state(final_state_eqs):
      state = self._states_to_check.popleft()
      new_states_and_turns = self._generate_states_and_turns(state)
      for (new_state, turn) in new_states_and_turns:
        if self._find_known_state(new_state.get_equivalents()):
          continue
        self._known_states[new_state] = turn
        self._states_to_check.enque(new_state)
    return self._find_known_state(final_state_eqs)

  def _phase2(self):
    state = self._find_known_state(self._final_state.get_equivalents())
    path = []
    while not self._initial_state in state.get_equivalents():
      turn_back = self._known_states[state].reverse()
      path.append(turn_back)
      state = state.apply(turn_back)
    path.reverse()
    return path

  def _generate_states_and_turns(self, state):
    sides = Side.minimal_list()
    angles = range(Turn.FIRST, Turn.LAST)
    turns = [Turn(s, a) for s in sides for a in angles]
    return [state.apply(t) for t in turns]

  def _find_known_state(self, states):
    for s in states:
      if s in self._known_states:
        return s
    return None

  @staticmethod
  def solved_state():
    state_matrix = []
    for side_or_color in range(Side.LAST):
      state_matrix.append(
        [side_or_color for tile in range(Tile.LAST)])
    state = State(state_matrix)
    assert state.verify()
    return state

if __name__ == '__main__':
  _W = Color.WHITE
  _R = Color.RED
  _G = Color.GREEN
  _Y = Color.YELLOW
  _O = Color.ORANGE
  _B = Color.BLUE
  initial_state = State([
    # RT, RB, LB, LT
    [], # FRONT
    [], # LEFT
    [], # UPPER
    [], # BACK
    [], # RIGHT
    []  # DOWN
  ])
  final_state = None
  final_state = State([
    # RT, RB, LB, LT
    [], # FRONT
    [], # LEFT
    [], # UPPER
    [], # BACK
    [], # RIGHT
    []  # DOWN
  ])
  solver = Solver(initial_state, final_state)
  print solver.solve()
