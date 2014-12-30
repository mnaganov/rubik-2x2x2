#!/usr/bin/env python

from collections import deque
import math
import time

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
  RADIANS = (math.pi / 2, math.pi, math.pi / -2)

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

  def __repr__(self):
    return ('Turn %d %d' % (self._side, self._angle))

class State:
  X = 0
  Y = 1
  Z = 2
  AXIS = (Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1))

  def __init__(self, tiles_by_sides_6_x_4):
    self._state = tuple(tiles_by_sides_6_x_4)

  def verify(self):
    # verify that all corners do present
    # ??? What about any ???
    return True

  def get_equivalents(self):
    _X = State.X
    _Y = State.Y
    _Z = State.Z
    _C = Turn.T90
    _C2 = Turn.T180
    _CC = Turn.T270
    return [
      self._rotate_cube([]),
      self._rotate_cube([(_Z, _C), (_Y, _C)]),
      self._rotate_cube([(_Z, _CC), (_Y, _CC)]),
      self._rotate_cube([(_Z, _CC)]),
      self._rotate_cube([(_Y, _C)]),
      self._rotate_cube([(_Z, _C2), (_X, _C)]),
      self._rotate_cube([(_Z, _C2)]),
      self._rotate_cube([(_X, _CC), (_Z, _C)]),
      self._rotate_cube([(_Y, _C), (_Z, _CC)]),
      self._rotate_cube([(_Z, _C)]),
      self._rotate_cube([(_X, _CC)]),
      self._rotate_cube([(_Z, _C2), (_Y, _CC)]),
      self._rotate_cube([(_Y, _CC)]),
      self._rotate_cube([(_X, _C)]),
      self._rotate_cube([(_Y, _C2), (_Z, _C)]),
      self._rotate_cube([(_Z, _C), (_Y, _CC)]),
      self._rotate_cube([(_Z, _C), (_X, _CC)]),
      self._rotate_cube([(_X, _C2)]),
      self._rotate_cube([(_Z, _C2), (_X, _CC)]),
      self._rotate_cube([(_Z, _C2), (_Y, _C)]),
      self._rotate_cube([(_Y, _C2), (_Z, _CC)]),
      self._rotate_cube([(_Y, _CC), (_Z, _CC)]),
      self._rotate_cube([(_Y, _C2)]),
      self._rotate_cube([(_Z, _CC), (_Y, _C)])
    ]

  def apply(self, turn):
    axis = [State.X, None, State.Z, None, State.Y, None][turn.side()]
    return self._rotate_half_cube(axis, turn.angle())

  def _rotate_cube(self, rotations):
    (coords, colors) = self._state_to_coords()
    return self._do_rotate(coords, colors, rotations)

  def _rotate_half_cube(self, axis, angle):
    (coords, colors) = self._state_to_coords(positive_axis=axis)
    return self._do_rotate(coords, colors, [(axis, angle)])

  def _do_rotate(self, coords, colors, rotations):
    m = Matrix4()
    for (axis, angle) in rotations:
      m.rotate_axis(Turn.RADIANS[angle], State.AXIS[axis])
    points = map(lambda p: m * p, self._coords_to_points(coords))
    return self._create_state_from_coords(
      self._points_to_coords(points), colors)

  def _coords_to_points(self, coords):
    return map(lambda coord: Point3(coord[0], coord[1], coord[2]), coords)

  def _points_to_coords(self, points):
    return map(lambda point: \
      (int(round(point.x)), int(round(point.y)), int(round(point.z))), points)

  def _state_to_coords(self, positive_axis=None):
    coords = State._COORDS
    if positive_axis != None:
      coords = map(
        lambda coord: coord if coord[positive_axis] > 0 else (0, 0, 0),
        coords)
    return (coords, dict(zip(State._COORDS, self._state)))

  def _create_state_from_coords(self, coords, colors):
    new_state = list(self._state)
    for (pos, coord) in enumerate(coords):
      if coord != (0, 0, 0):
        new_state[pos] = colors[coord]
    return State(new_state)

  def __hash__(self):
    return hash(self._state)

  def __eq__(self, other):
    return self._state == other._state

  def __repr__(self):
    return str(self._state)

  _COORDS = [
    (2, 1, 1), (2, 1, -1), (2, -1, -1), (2, -1, 1),
    (1, -2, 1), (1, -2, -1), (-1, -2, -1), (-1, -2, 1),
    (-1, 1, 2), (1, 1, 2), (1, -1, 2), (-1, -1, 2),
    (-2, -1, 1), (-2, -1, -1), (-2, 1, -1), (-2, 1, 1),
    (-1, 2, 1), (-1, 2, -1), (1, 2, -1), (1, 2, 1),
    (-1, -1, -2), (1, -1, -2), (1, 1, -2), (-1, 1, -2)
  ]

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
    last_report_time = None
    while len(self._states_to_check) > 0 and \
          not self._find_known_state(final_state_eqs):
      t = time.clock()
      if not last_report_time or t - last_report_time >= 1.0:
        last_report_time = t
        print len(self._states_to_check)
      state = self._states_to_check.popleft()
      new_states_and_turns = self._generate_states_and_turns(state)
      for (new_state, turn) in new_states_and_turns:
        if self._find_known_state(new_state.get_equivalents()):
          continue
        self._known_states[new_state] = turn
        self._states_to_check.append(new_state)
    return self._find_known_state(final_state_eqs)

  def _phase2(self):
    state = self._find_known_state(self._final_state.get_equivalents())
    path = []
    while not self._initial_state in state.get_equivalents():
      turn = self._known_states[state]
      path.append(turn)
      state = state.apply(turn.reverse())
    path.reverse()
    return path

  def _generate_states_and_turns(self, state):
    sides = Side.minimal_list()
    angles = range(Turn.FIRST, Turn.LAST)
    turns = [Turn(s, a) for s in sides for a in angles]
    return [(state.apply(t), t) for t in turns]

  def _find_known_state(self, states):
    for s in states:
      if s in self._known_states:
        return s
    return None

  @staticmethod
  def solved_state():
    state_matrix = [c for c in range(Side.LAST) for t in range(Tile.LAST)]
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
    _W, _W, _W, _W, # FRONT
    _R, _R, _G, _B, # LEFT
    _G, _G, _G, _R, # UPPER
    _Y, _Y, _Y, _Y, # BACK
    _O, _O, _O, _O, # RIGHT
    _R, _B, _B, _B  # DOWN
  ])
  final_state = None
  # final_state = State([
  #   # RT, RB, LB, LT
  #   _W, _W, _W, _W, # FRONT
  #   _R, _R, _R, _R, # LEFT
  #   _G, _G, _G, _G, # UPPER
  #   _Y, _Y, _Y, _Y, # BACK
  #   _O, _O, _O, _O, # RIGHT
  #   _B, _B, _B, _B  # DOWN
  # ])
  solver = Solver(initial_state, final_state)
  print solver.solve()
