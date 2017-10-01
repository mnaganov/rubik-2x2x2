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
    sides = ['F', 'L', 'U', 'B', 'R', 'D']
    angles = ['', '2', '\'']
    return ('%s%s' % (sides[self._side], angles[self._angle]))

class State:
  def __init__(self, tiles_by_sides_6_x_4):
    self._state = tuple(tiles_by_sides_6_x_4)

  def verify(self):
    # verify that all corners do present
    # ??? What about any ???
    return True

  def get_equivalents(self):
    _X = Rotator.X
    _Y = Rotator.Y
    _Z = Rotator.Z
    _C = Turn.T90
    _C2 = Turn.T180
    _CC = Turn.T270
    return [
      self._rotate_cube(()),
      self._rotate_cube(((_Z, _C), (_Y, _C))),
      self._rotate_cube(((_Z, _CC), (_Y, _CC))),
      self._rotate_cube(((_Z, _CC),)),
      self._rotate_cube(((_Y, _C),)),
      self._rotate_cube(((_Z, _C2), (_X, _C))),
      self._rotate_cube(((_Z, _C2),)),
      self._rotate_cube(((_X, _CC), (_Z, _C))),
      self._rotate_cube(((_Y, _C), (_Z, _CC))),
      self._rotate_cube(((_Z, _C),)),
      self._rotate_cube(((_X, _CC),)),
      self._rotate_cube(((_Z, _C2), (_Y, _CC))),
      self._rotate_cube(((_Y, _CC),)),
      self._rotate_cube(((_X, _C),)),
      self._rotate_cube(((_Y, _C2), (_Z, _C))),
      self._rotate_cube(((_Z, _C), (_Y, _CC))),
      self._rotate_cube(((_Z, _C), (_X, _CC))),
      self._rotate_cube(((_X, _C2),)),
      self._rotate_cube(((_Z, _C2), (_X, _CC))),
      self._rotate_cube(((_Z, _C2), (_Y, _C))),
      self._rotate_cube(((_Y, _C2), (_Z, _CC))),
      self._rotate_cube(((_Y, _CC), (_Z, _CC))),
      self._rotate_cube(((_Y, _C2),)),
      self._rotate_cube(((_Z, _CC), (_Y, _C)))
    ]

  def apply(self, turn):
    axis = [Rotator.X, None, Rotator.Z, None, Rotator.Y, None][turn.side()]
    return self._rotate_half_cube(axis, turn.angle())

  def _rotate_cube(self, rotations):
    return State(Rotator.full_rotate(rotations, self._state))

  def _rotate_half_cube(self, axis, angle):
    return State(Rotator.half_rotate((axis, angle), self._state))

  def __hash__(self):
    return hash(self._state)

  def __eq__(self, other):
    return self._state == other._state

  def __repr__(self):
    return str(self._state)

class Rotator:
  X = 0
  Y = 1
  Z = 2

  @staticmethod
  def init():
    if hasattr(Rotator, '_initialized'):
      return
    Rotator._full_transposes = \
      {r: Rotator._full_rotation(r) for r in Rotator._FULL_ROTATIONS}
    Rotator._half_transposes = \
      {r: Rotator._half_rotation(r) for r in Rotator._HALF_ROTATIONS}
    _initialized = True

  @staticmethod
  def full_rotate(rotations, state):
    return Rotator._rotate(Rotator._full_transposes[rotations], state)

  @staticmethod
  def half_rotate(rotation, state):
    return Rotator._rotate(Rotator._half_transposes[rotation], state)

  @staticmethod
  def _rotate(transpose, state):
    result = list(state)
    for (pos, x) in enumerate(transpose):
      result[pos] = state[x]
    return result

  @staticmethod
  def _full_rotation(rotations):
    coords = Rotator._get_coords()
    return Rotator._do_rotate(coords, rotations)

  @staticmethod
  def _half_rotation(rotation):
    coords = Rotator._get_coords(positive_axis=rotation[0])
    return Rotator._do_rotate(coords, (rotation,))

  @staticmethod
  def _do_rotate(coords, rotations):
    m = Matrix4()
    for (axis, angle) in rotations:
      m.rotate_axis(Turn.RADIANS[angle], Rotator._AXIS[axis])
    points = map(lambda p: m * p, Rotator._coords_to_points(coords))
    return Rotator._create_transpose_from_coords(
      Rotator._points_to_coords(points))

  @staticmethod
  def _coords_to_points(coords):
    return map(lambda coord: Point3(coord[0], coord[1], coord[2]), coords)

  @staticmethod
  def _points_to_coords(points):
    return map(lambda point: \
      (int(round(point.x)), int(round(point.y)), int(round(point.z))), points)

  @staticmethod
  def _get_coords(positive_axis=None):
    coords = Rotator._COORDS
    if positive_axis != None:
      coords = map(
        lambda coord: coord if coord[positive_axis] > 0 else (0, 0, 0),
        coords)
    return coords

  @staticmethod
  def _create_transpose_from_coords(coords):
    positions = dict(zip(Rotator._COORDS, range(len(Rotator._COORDS))))
    transpose = range(len(Rotator._COORDS))
    for (pos, coord) in enumerate(coords):
      if coord != (0, 0, 0):
        transpose[pos] = positions[coord]
    return tuple(transpose)

  _AXIS = (Vector3(1, 0, 0), Vector3(0, 1, 0), Vector3(0, 0, 1))
  _COORDS = [
    (2, 1, 1), (2, 1, -1), (2, -1, -1), (2, -1, 1),
    (1, -2, 1), (1, -2, -1), (-1, -2, -1), (-1, -2, 1),
    (-1, 1, 2), (1, 1, 2), (1, -1, 2), (-1, -1, 2),
    (-2, -1, 1), (-2, -1, -1), (-2, 1, -1), (-2, 1, 1),
    (-1, 2, 1), (-1, 2, -1), (1, 2, -1), (1, 2, 1),
    (-1, -1, -2), (1, -1, -2), (1, 1, -2), (-1, 1, -2)
  ]
  _FULL_ROTATIONS = [
    (),
    ((Z, Turn.T90), (Y, Turn.T90)),
    ((Z, Turn.T270), (Y, Turn.T270)),
    ((Z, Turn.T270),),
    ((Y, Turn.T90),),
    ((Z, Turn.T180), (X, Turn.T90)),
    ((Z, Turn.T180),),
    ((X, Turn.T270), (Z, Turn.T90)),
    ((Y, Turn.T90), (Z, Turn.T270)),
    ((Z, Turn.T90),),
    ((X, Turn.T270),),
    ((Z, Turn.T180), (Y, Turn.T270)),
    ((Y, Turn.T270),),
    ((X, Turn.T90),),
    ((Y, Turn.T180), (Z, Turn.T90)),
    ((Z, Turn.T90), (Y, Turn.T270)),
    ((Z, Turn.T90), (X, Turn.T270)),
    ((X, Turn.T180),),
    ((Z, Turn.T180), (X, Turn.T270)),
    ((Z, Turn.T180), (Y, Turn.T90)),
    ((Y, Turn.T180), (Z, Turn.T270)),
    ((Y, Turn.T270), (Z, Turn.T270)),
    ((Y, Turn.T180),),
    ((Z, Turn.T270), (Y, Turn.T90))
  ]
  _HALF_ROTATIONS = [
    (X, Turn.T90), (X, Turn.T180), (X, Turn.T270),
    (Y, Turn.T90), (Y, Turn.T180), (Y, Turn.T270),
    (Z, Turn.T90), (Z, Turn.T180), (Z, Turn.T270)
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
  Rotator.init()
  _W = Color.WHITE
  _R = Color.RED
  _G = Color.GREEN
  _Y = Color.YELLOW
  _O = Color.ORANGE
  _B = Color.BLUE
  initial_state = State([
    # RT, RB, LB, LT
    _Y, _Y, _W, _Y, # FRONT
    _O, _R, _O, _O, # LEFT
    _G, _G, _G, _G, # UPPER
    _W, _W, _Y, _W, # BACK
    _R, _O, _R, _R, # RIGHT
    _B, _B, _B, _B  # DOWN
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
