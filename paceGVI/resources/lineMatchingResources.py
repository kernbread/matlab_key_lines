# Author: Brian Curran Jr
# Date: 10-8-17
# Description: Functions to check a matlab line against certain regex's.

import copy, os, sys, re, json, logging

#*** General checks against a line to determine line type ***#
def checkIfLineMatchesEqStatement(line):
  reg_eq = r"([^=]*)=[^=].*;.*"
  match_eq = re.match(reg_eq, line)
  if match_eq:
    return True
  else:
    return False

def checkIfLineIsCommentOrEmptyLine(line):
  reg_comment = '^\s*%.*'
  match_comment = re.match(reg_comment, line)

  if match_comment:
    return True
  elif line.strip() == '':
    return True
  else:
    return False

def checkIfLineMatchesCondStatement(line):
  reg_if = r"^(?!%)\s*if\s.*"
  match_if = re.match(reg_if, line)

  reg_for = r"^(?!%)\s*for\s.*"
  match_for = re.match(reg_for, line)

  reg_while = r"^(?!%)\s*while\s.*"
  match_while = re.match(reg_while, line)

  reg_switch = r"^(?!%)\s*switch[\s\(].*"
  match_switch = re.match(reg_switch, line)

  if match_if or match_for or match_while or match_switch:
    return True
  else:
    return False

def checkIfLineMatchesOneLinerConditional(line):
  reg_if_1 = r"^\s*if\s.*(?!\()end(?!\)).*"
  match_if_1 = re.match(reg_if_1, line)

  reg_for_1 = r"^\s*for\s.*(?!\()end(?!\)).*"
  match_for_1 = re.match(reg_for_1, line)

  reg_while_1 = r"^\s*while\s.*(?!\()end(?!\)).*"
  match_while_1 = re.match(reg_while_1, line)

  reg_switch_1 = r"^(?!%)\s*switch\(.*\)\s.*(?!\()end(?!\)).*"
  match_switch_1 = re.match(reg_switch_1, line)

  if match_if_1 or match_for_1 or match_while_1 or match_switch_1:
    return True
  else:
    return False

def checkIfLineMatchesElifStatement(line):
  reg_elif = r"^\s*elseif\s.*"
  match_elif = re.match(reg_elif, line)
  if match_elif:
    return True
  else:
    return False

def checkIfLineMatchesElseStatement(line):
  reg_else = r"^\s*else\s.*"
  match_else = re.match(reg_else, line)
  if match_else:
    return True
  else:
    return False

def checkIfLineContainsEnd(line):
  reg_end = r"^(?!%)\s*end\s*"
  match_end = re.match(reg_end, line)
  if match_end:
    return True
  else:
    return False

def checkIfLineEndsWithSemiColon(line):
  reg_semi = r".*\;\s*(?!\.\.\.)"
  match_semi = re.match(reg_semi, line)
  if match_semi:
    return True
  else:
    return False

def checkIfLineContainsKnownCommand(line):
  reg_cmd = r"\s*(clear|warning|warndlg)\s*.*"
  match_cmd = re.match(reg_cmd, line)
  if match_cmd:
    return True
  else:
    return False

def checkIfLineMatchesLineWithContinuation(line):
  reg_cont = r"^(?!%).*\.\.\.\s*"
  match_cont = re.match(reg_cont, line)
  if match_cont:
    return True
  else:
    return False

#*** Other checking functions ***#
def checkIfKeywordInStatement(line, keyword):
  reg_keyword_in_line = r"^(.*?(\b" + re.escape(keyword) + r"\b)[^$]*)$"
  match_keyword_in_line = re.match(reg_keyword_in_line, line)
  if match_keyword_in_line:
    return True
  else:
    return False

def checkIfDependencyUsedInCondStatement(var, cond_list):
  for cond in cond_list:
    match_cond = checkIfKeywordInStatement(cond, var)
    if match_cond:
      return True
  return False

