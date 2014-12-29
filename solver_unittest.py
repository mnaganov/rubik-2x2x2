#!/usr/bin/env python

import unittest

from solver import *

class SolverTestCaseBase(unittest.TestCase):
  def setUp(self):
    pass

class TrivialTestCase(SolverTestCaseBase):
  def runTest(self):
    solver = Solver(Solver.solved_state())
    result = solver.solve()
    assert len(result) == 0

if __name__ == "__main__":
  unittest.main()
