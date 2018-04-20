# Author: Brian Curran Jr
# Date: 10-8-17
# Description: Various functions utilized to scale variables.

import copy, os, sys, re, json, logging, getopt
from lineMatchingResources import *
from LineClass import *

def uniquifyList(seq): 
   # order preserving
   checked = []
   for e in seq:
       if e not in checked:
           checked.append(e)
   return checked

def getAssignedVars(dependencies):
	assigned_vars = []
	for dep in dependencies:
		for var in dep.LHS:
			assigned_vars.append(var)
	
	return assigned_vars
	
def getAllVarNames(dependencies):
	all_var_names = []
	for dep in dependencies:
		for vars_lhs in dep.LHS:
			all_var_names.append(vars_lhs)
		for vars_rhs in dep.required_vars:
			all_var_names.append(vars_rhs)
	
	return all_var_names

def findMFilesFromFile(in_file_name, search_path):
  files = []
  with open(in_file_name, 'r') as f:
    for filename in f:
      path = __find(filename.strip(), search_path)
      if path == 'UNKNOWN':
        logging.warn('Could not find matfile: %s', filename.strip())
        continue
      files.append(path)

  return files

# to be used only be findMFilesFromFile
def __find(name, search_path):
  for root, dirs, files in os.walk(search_path):
    if name in files:
      return os.path.join(root, name)
  return 'UNKNOWN'

# gets all matfile lines. Returns a list of Line objects
def getMatFileLines(matfiles):
  lines, collapsed_ln = [], 0
  for file in matfiles:
    with open(file) as f:
      ln, cond_list = 0, []
      for line in f:
        ln+=1
        collapsed_ln+=1

        # skip unimportant lines
        if checkIfLineIsCommentOrEmptyLine(line):
          continue

        # update conditional list
        if checkIfLineMatchesCondStatement(line) and not checkIfLineMatchesOneLinerConditional(line):
          cond_list.append(line)
          continue
        elif checkIfLineMatchesElifStatement(line) or checkIfLineMatchesElseStatement(line):
          # if we find an elif/else, pop off the if statement and append the elif/else instead
          cond_list.pop()
          cond_list.append(line)
          continue
        elif checkIfLineContainsEnd(line):
          cond_list.pop()
          continue

        cond_list_dc = copy.deepcopy(cond_list)
        line = line.rstrip()
        line_obj = Line(line, file, ln, cond_list_dc, collapsed_ln)
        lines.append(line_obj)
        
        if line_obj.type == 'NOTYPE':
          logging.warn('The type of this line is unknown: %s', line_obj.line)
          logging.debug('Unknown line loc: %s', line_obj.file + ':' + str(line_obj.ln))
  return lines

def getUniqueDependencyNames(X, dependencies):
  # X is the variable we are initially searching for
  uniqueDependencies = [X]
  for elem in dependencies:
    # case of multiple dependencies being assigned on LHS of an eq
    for dep in elem.LHS:
      if dep != 'NAN' and dep not in uniqueDependencies:
        uniqueDependencies.append(dep)
  return uniqueDependencies

def findAllDeclarationsOfVariable(var, lines):
  declarations = []
  for line_obj in lines:
    for LHS in line_obj.LHS:
      if LHS == var:
        declarations.append(line_obj)
  return declarations

def getCmdLineOptsScaling(argv):
  help_msg = """Example Usage:\nuser$ python scaling.py -m collapsedMFileMRZR.m -v eng.plant.scale.pwr_max_des\n
|---------------------------------------------------------------------------------------------------|
|long argument       short argument  required  Description                                          |
|---------------------------------------------------------------------------------------------------|
|--help              -h              False     This help message.                                   |
|--collapsed_m_file  -m              True      Collapsed m file for vehicle.                        |
|--var_to_change     -v              True      Variable you want to change.                         |
|---------------------------------------------------------------------------------------------------|

For more information, refer to the help documents in paceGVI/docs.
  """
  if len(argv) < 4:
    print help_msg
    sys.exit(2)
  unix_options, gnu_options = "hm:v:", ["help", "collapsed_m_file", "var_to_scale"]
  collapsed_m_file, X = '',''
  try:
    arguments, values = getopt.getopt(argv, unix_options, gnu_options)
  except getopt.error as err:
    print str(err)
    sys.exit(2)
  for curr_arg, curr_val in arguments:
    if curr_arg in ("-m", "--collapsed_m_file"):
      collapsed_m_file = curr_val
    elif curr_arg in ("-v", "--var_to_scale"):
      X = curr_val
    elif curr_arg in ("-h", "--help"):
      print help_msg
      sys.exit(2)

  return collapsed_m_file, X


# ***DEPRECIATED FUNCTIONS***
SEEN = []
def findAllRequiredVars(line, matfile_lines):
  for LHS in line.LHS:
    SEEN.append(LHS)
  req_vars = line.required_vars
  for var in req_vars:
    declarations = findAllDeclarationsOfVariable(var, matfile_lines)
    for dec in declarations:
      if dec.collapsed_ln < line.collapsed_ln:
        findAllRequiredVars(dec, matfile_lines)
  return SEEN

def resetSeen():
  SEEN = []

