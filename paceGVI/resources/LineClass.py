# Author: Brian Curran Jr
# Date: 10-8-17
# Description: Class to hold elements of a matlab line.

import copy, os, sys, re, json, logging
from lineMatchingResources import *
from scalingResources import *
  
class Line(object):
  def __init__(self, line, file, ln, cond_list, collapsed_ln):
    self.line = line
    self.file = file
    self.ln = ln
    self.cond_list = cond_list
    self.collapsed_ln = collapsed_ln
    self.in_cond = self.checkIfInConditional(self.cond_list)
    self.type = self.getType(self.line)
    self.LHS, self.RHS = self.getSidesOfEquation(self.line)
    self.LHS_str = self.LHS
    self.LHS = self.getRequiredVars(self.LHS)
    self.required_vars = self.getRequiredVars(self.RHS)

  def getSidesOfEquation(self, line):
    if checkIfLineMatchesEqStatement(line):
      split = [x.strip() for x in line.split('=')]
      LHS, RHS = split[0], split[1]
      return LHS.strip(), RHS.strip()
    else:
      return 'NAN', 'NAN'

  def getRequiredVars(self, RHS):
    reg_req_vars = re.compile('([a-zA-Z][a-zA-Z0-9_]*\.(?:[a-zA-Z][a-zA-Z0-9_]*\.*)+)')
    required_vars = reg_req_vars.findall(RHS)
    return required_vars

  def checkIfInConditional(self, cond):
    if len(cond) > 0:
      return True
    else:
      return False

  def getType(self, line):
    if checkIfLineMatchesEqStatement(line):
      return 'EQ'
    elif checkIfLineIsCommentOrEmptyLine(line):
      return 'SKIP'
    # all other types of conditionals held in objects self.cond_list
    elif checkIfLineMatchesOneLinerConditional(line):
        return '1_LINER_COND'
    elif checkIfLineContainsKnownCommand(line):
      return 'CMD'
    else:
      return 'NOTYPE'

