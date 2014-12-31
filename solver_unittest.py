#!/usr/bin/env python

import unittest

from solver import *

class SolverTestCaseBase(unittest.TestCase):
  def setUp(self):
    Rotator.init()

class SolvedStateTestCase(SolverTestCaseBase):
  def runTest(self):
    _W = Color.WHITE
    _R = Color.RED
    _G = Color.GREEN
    _Y = Color.YELLOW
    _O = Color.ORANGE
    _B = Color.BLUE
    initial_state = State([
      # RT, RB, LB, LT
      _W, _W, _W, _W, # FRONT
      _R, _R, _R, _R, # LEFT
      _G, _G, _G, _G, # UPPER
      _Y, _Y, _Y, _Y, # BACK
      _O, _O, _O, _O, # RIGHT
      _B, _B, _B, _B  # DOWN
    ])
    assert initial_state == Solver.solved_state()
    mixed_state = State([
      # RT, RB, LB, LT
      _W, _W, _W, _W, # FRONT
      _B, _R, _R, _G, # LEFT
      _R, _G, _G, _G, # UPPER
      _Y, _Y, _Y, _Y, # BACK
      _O, _O, _O, _O, # RIGHT
      _B, _B, _B, _R  # DOWN
    ])
    assert mixed_state != Solver.solved_state()

class TrivialTestCase(SolverTestCaseBase):
  def runTest(self):
    solver = Solver(Solver.solved_state())
    result = solver.solve()
    assert len(result) == 0

class TurnReverseTestCase(SolverTestCaseBase):
  def runTest(self):
    initial_state = Solver.solved_state()
    f_turn = Turn(Side.FRONT, Turn.T90)
    assert initial_state.apply(f_turn).apply(f_turn.reverse()) == initial_state
    f1_turn = Turn(Side.FRONT, Turn.T270)
    assert initial_state.apply(f1_turn).apply(f1_turn.reverse()) == initial_state
    f2_turn = Turn(Side.FRONT, Turn.T180)
    assert initial_state.apply(f2_turn).apply(f2_turn.reverse()) == initial_state

class BasicTurnsTestCase(SolverTestCaseBase):
  def runTest(self):
    _W = Color.WHITE
    _R = Color.RED
    _G = Color.GREEN
    _Y = Color.YELLOW
    _O = Color.ORANGE
    _B = Color.BLUE
    initial_state = Solver.solved_state()
    f_state = initial_state.apply(Turn(Side.FRONT, Turn.T90))
    assert f_state == State([
      # RT, RB, LB, LT
      _W, _W, _W, _W, # FRONT
      _B, _B, _R, _R, # LEFT
      _G, _R, _R, _G, # UPPER
      _Y, _Y, _Y, _Y, # BACK
      _O, _O, _G, _G, # RIGHT
      _B, _O, _O, _B  # DOWN
    ])
    f1_state = initial_state.apply(Turn(Side.FRONT, Turn.T270))
    assert f1_state == State([
      # RT, RB, LB, LT
      _W, _W, _W, _W, # FRONT
      _G, _G, _R, _R, # LEFT
      _G, _O, _O, _G, # UPPER
      _Y, _Y, _Y, _Y, # BACK
      _O, _O, _B, _B, # RIGHT
      _B, _R, _R, _B  # DOWN
    ])
    f2_state = initial_state.apply(Turn(Side.FRONT, Turn.T180))
    assert f2_state == State([
      # RT, RB, LB, LT
      _W, _W, _W, _W, # FRONT
      _O, _O, _R, _R, # LEFT
      _G, _B, _B, _G, # UPPER
      _Y, _Y, _Y, _Y, # BACK
      _O, _O, _R, _R, # RIGHT
      _B, _G, _G, _B  # DOWN
    ])
    u_state = initial_state.apply(Turn(Side.UPPER, Turn.T90))
    assert u_state == State([
      # RT, RB, LB, LT
      _O, _W, _W, _O, # FRONT
      _W, _R, _R, _W, # LEFT
      _G, _G, _G, _G, # UPPER
      _R, _Y, _Y, _R, # BACK
      _Y, _O, _O, _Y, # RIGHT
      _B, _B, _B, _B  # DOWN
    ])
    u1_state = initial_state.apply(Turn(Side.UPPER, Turn.T270))
    assert u1_state == State([
      # RT, RB, LB, LT
      _R, _W, _W, _R, # FRONT
      _Y, _R, _R, _Y, # LEFT
      _G, _G, _G, _G, # UPPER
      _O, _Y, _Y, _O, # BACK
      _W, _O, _O, _W, # RIGHT
      _B, _B, _B, _B  # DOWN
    ])
    u2_state = initial_state.apply(Turn(Side.UPPER, Turn.T180))
    assert u2_state == State([
      # RT, RB, LB, LT
      _Y, _W, _W, _Y, # FRONT
      _O, _R, _R, _O, # LEFT
      _G, _G, _G, _G, # UPPER
      _W, _Y, _Y, _W, # BACK
      _R, _O, _O, _R, # RIGHT
      _B, _B, _B, _B  # DOWN
    ])
    r_state = initial_state.apply(Turn(Side.RIGHT, Turn.T90))
    assert r_state == State([
      # RT, RB, LB, LT
      _B, _B, _W, _W, # FRONT
      _R, _R, _R, _R, # LEFT
      _W, _W, _G, _G, # UPPER
      _Y, _Y, _G, _G, # BACK
      _O, _O, _O, _O, # RIGHT
      _B, _B, _Y, _Y  # DOWN
    ])
    r1_state = initial_state.apply(Turn(Side.RIGHT, Turn.T270))
    assert r1_state == State([
      # RT, RB, LB, LT
      _G, _G, _W, _W, # FRONT
      _R, _R, _R, _R, # LEFT
      _Y, _Y, _G, _G, # UPPER
      _Y, _Y, _B, _B, # BACK
      _O, _O, _O, _O, # RIGHT
      _B, _B, _W, _W  # DOWN
    ])
    r2_state = initial_state.apply(Turn(Side.RIGHT, Turn.T180))
    assert r2_state == State([
      # RT, RB, LB, LT
      _Y, _Y, _W, _W, # FRONT
      _R, _R, _R, _R, # LEFT
      _B, _B, _G, _G, # UPPER
      _Y, _Y, _W, _W, # BACK
      _O, _O, _O, _O, # RIGHT
      _B, _B, _G, _G  # DOWN
    ])

class EquivalentsTestCase(SolverTestCaseBase):
  def runTest(self):
    initial_state = Solver.solved_state()
    f_state = initial_state.apply(Turn(Side.FRONT, Turn.T90))
    f_eqs = f_state.get_equivalents()
    assert f_state in f_eqs
    assert not initial_state in f_eqs
    f1_state = initial_state.apply(Turn(Side.FRONT, Turn.T270))
    f1_eqs = f1_state.get_equivalents()
    assert f1_state in f1_eqs
    assert not initial_state in f1_eqs
    f2_state = initial_state.apply(Turn(Side.FRONT, Turn.T180))
    f2_eqs = f2_state.get_equivalents()
    assert f2_state in f2_eqs
    assert not initial_state in f2_eqs

class Simple1MoveTestCase(SolverTestCaseBase):
  def runTest(self):
    initial_state = Solver.solved_state()
    f_state = initial_state.apply(Turn(Side.FRONT, Turn.T90))
    solver = Solver(f_state)
    result = solver.solve()
    assert len(result) == 1
    assert result[0].side() == Side.FRONT
    assert result[0].angle() == Turn.T270

class Simple2MovesTestCase(SolverTestCaseBase):
  def runTest(self):
    initial_state = Solver.solved_state()
    fu_state = initial_state.apply(
      Turn(Side.FRONT, Turn.T90)).apply(Turn(Side.UPPER, Turn.T90))
    solver = Solver(fu_state)
    result = solver.solve()
    assert len(result) == 2
    assert result[0].side() == Side.UPPER
    assert result[0].angle() == Turn.T270
    assert result[1].side() == Side.FRONT
    assert result[1].angle() == Turn.T270

if __name__ == "__main__":
  unittest.main()
