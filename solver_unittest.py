#!/usr/bin/env python

import unittest

from solver import *

class SolverTestCaseBase(unittest.TestCase):
  def setUp(self):
    pass

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

if __name__ == "__main__":
  unittest.main()
