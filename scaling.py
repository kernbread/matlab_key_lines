# Author: Brian Curran Jr
# Date: 2-10-2018
# Description: This script creates a scaling m file script based on whatever variable you wish to scale.

import logging, sys, copy, shutil

from paceGVI.resources.scalingResources import *

def main(argv):
  # setting config vars. X = variable to change
  logging.basicConfig(filename='loggingScaling.log',filemode='w', level=logging.DEBUG)

  collapsed_m_file, X = getCmdLineOptsScaling(argv) 
  
  matfile_lines = getMatFileLines([collapsed_m_file])
  
  dependencies = []
  for line_obj in matfile_lines:
    unique_dep_names = getUniqueDependencyNames(X, dependencies)

    for var in unique_dep_names:
      if var in line_obj.required_vars or var in line_obj.LHS or checkIfDependencyUsedInCondStatement(var, line_obj.cond_list):
        dependencies.append(line_obj)
        break

  logging.debug('Unique dependency names: %s', unique_dep_names)
  logging.info('Number of unique dependencies: %s', len(unique_dep_names))
  logging.info('Total number of dependency lines: %s', len(dependencies))

  last_cond = []
  for dep in dependencies:
    diff_cond = [x for x in dep.cond_list if x not in last_cond]
    for cond in diff_cond:
      print cond
    # print an end if we just popped something off of dep.cond_list
    if len(dep.cond_list) < len(last_cond): print 'end'

    print dep.line
    last_cond = copy.deepcopy(dep.cond_list)

  assigned_vars_file = open("assigned_var_names.txt", "w")
  all_var_names_file = open("all_var_names.txt", "w")
  assigned_vars = getAssignedVars(dependencies)
  all_var_names = getAllVarNames(dependencies)

  for var in uniquifyList(assigned_vars):
    assigned_vars_file.write(var + '\n')

  for var in uniquifyList(all_var_names):
    all_var_names_file.write(var + '\n')

if __name__ == '__main__':
  main(sys.argv[1:])
 
