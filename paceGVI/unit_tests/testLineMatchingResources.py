import sys, unittest
sys.path.insert(0,'../../')
from paceGVI.resources.scalingResources import *
from paceGVI.resources.lineMatchingResources import *
from paceGVI.resources.LineClass import *

class TestVarsEffected(unittest.TestCase):
  def setUp(self):
    self.x = 'eng.plant.init.pwr_max'
    self.in_file = '../../data/mrzr/evaluation_order_MRZR.txt'
    self.search_path = '../../data/mrzr/MRZR_Conv_CVT_2wd_Midsize_wEng_Scaling_altered_continuation_lines/'

  def test_check_if_variable_in_statement(self):
    statement = 'eng.plant.init.pwr_max = 532'
    self.assertEqual(checkIfKeywordInStatement(statement, self.x), True)
    statement = '   eng.plant.init.pwr_max=532'
    self.assertEqual(checkIfKeywordInStatement(statement, self.x), True)
    statement = 'x = eng.plant.init.pwr_max*4343;'
    self.assertEqual(checkIfKeywordInStatement(statement, self.x), True) 
    statement = 'while x<eng.plant.init.pwr_max && !valid'
    self.assertEqual(checkIfKeywordInStatement(statement, self.x), True)
    statement = 'x = eng.plant.init.pwr_maxxxxxxxxx * 5'
    self.assertEqual(checkIfKeywordInStatement(statement, self.x), False)
    statement = 'x=gbeng.plant.init.pwr_max'
    self.assertEqual(checkIfKeywordInStatement(statement, self.x), False)
    statement = 'x=5*eng.plant.init.pwr_max'
    self.assertEqual(checkIfKeywordInStatement(statement, self.x), True)
    statement = 'eng.plant.init.pwr_max'
    self.assertEqual(checkIfKeywordInStatement(statement, self.x), True)

  def test_check_if_line_matches_eq_statement(self):
    statement = 'x = 5 + y;'
    self.assertEqual(checkIfLineMatchesEqStatement(statement), True)
    statement = 'x=5+y;'
    self.assertEqual(checkIfLineMatchesEqStatement(statement), True)
    statement = '    x      =       5+y    *   3;'
    self.assertEqual(checkIfLineMatchesEqStatement(statement), True)
    statement = ' if x == 5 ;'
    self.assertEqual(checkIfLineMatchesEqStatement(statement), False)
    statement = 'tmp.position_zero_spd           = find(gen.plant.init.eff_trq.idx1_spd==0);'
    self.assertEqual(checkIfLineMatchesEqStatement(statement), True)

 
  def test_check_if_line_matches_cond_statement(self):
    statement = 'if tmp_map(i,j)<0 && i>1'
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)
    # this should match 1 liner conditionals
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)
    statement = "   if isfield(eng,'calc'), eng = rmfield(eng,'calc');end"
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)
    statement = '        if    tmp_map(i,j)<0 && i>  1 '
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)
    statement = 'for cpt = 1:length(eng.plant.tmp.variables)'
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)
    statement = '      for    cpt = 1:length(eng.plant.tmp.variables)'
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)
    statement = 'while i < 3'
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)
    statement = '   while       x < 3 '
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)
    statement = 'switch(type_dens)'
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)
    statement = '   switch variable   '
    self.assertEqual(checkIfLineMatchesCondStatement(statement), True)

  def test_check_if_line_matches_one_liner_conditional(self):
    statement = "if isfield(eng,'calc'), eng = rmfield(eng,'calc');end"
    self.assertEqual(checkIfLineMatchesOneLinerConditional(statement), True)
    statement = 'if tmp_map(i,j)<0 && i>1'
    self.assertEqual(checkIfLineMatchesOneLinerConditional(statement), False)
    statement = "if eng.plant.calc.eff_hot_pwr.map(:,2:end)"
    self.assertEqual(checkIfLineMatchesOneLinerConditional(statement), False)
    statement = "  if   eng.plant.calc.eff_hot_pwr.map(:,2:end)  ;   end"
    self.assertEqual(checkIfLineMatchesOneLinerConditional(statement), True)

  def test_check_if_line_contains_end(self):
    statement = '    end    '
    self.assertEqual(checkIfLineContainsEnd(statement), True)
    statement = 'end'
    self.assertEqual(checkIfLineContainsEnd(statement), True)
    statement = 'gb.plant.init.trq_loss.idx3_gear = gb.plant.init.ratio.idx1_gear(2:end);'
    self.assertEqual(checkIfLineContainsEnd(statement), False)

  # checks that we find an equal number of conditionals and ends
  def test_conditional_and_line_counting_alg(self):
    matfiles = findMFilesFromFile(self.in_file, self.search_path) 
    for file in matfiles:
      with open(file) as f:
        num_cond = 0
        for line in f:
          if checkIfLineMatchesCondStatement(line) and not checkIfLineMatchesOneLinerConditional(line):
            num_cond +=1
          elif checkIfLineContainsEnd(line):
            num_cond -=1
        # for each file, checks that we found = number of cond and end's
        self.assertEqual(num_cond, 0)

if __name__ == '__main__':
  unittest.main()
