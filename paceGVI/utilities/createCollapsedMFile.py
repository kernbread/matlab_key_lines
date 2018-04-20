# Author: Brian Curran Jr
# Date: 11-6-17
# Description: This script takes all collapses all the m files defined in evaluation_order.txt into one m file. If it comes across an rmfield command, it removes this line.

import sys, re, os, subprocess, tempfile, shutil, getopt
import xml.etree.ElementTree as ET
sys.path.insert(0,'../../')
from paceGVI.resources.scalingResources import *
from paceGVI.resources.lineMatchingResources import *
from paceGVI.resources.LineClass import *
from paceGVI.resources.overridingVariablesResources import *

DELETE_TMP_DIR = True # set to False if you want to see modified m files after overrides

def main(argv):
  logging.basicConfig(filename='loggingCreateCollapsedMFile.log', filemode='w', level=logging.DEBUG)
  in_file, search_path, a_run_file = getCmdLineOptsCreateCollapsedMFile(argv) 

  overridden_vars_and_vals = findOverriddenVarsAndValues(a_run_file)
  tmp_overridden_m_files = overrideMFiles(overridden_vars_and_vals, in_file, search_path) # overrides m files and places in ./tmp

  matfiles = findMFilesFromFile(in_file, './tmp')
  for mfile in matfiles:
    with open(mfile, 'r') as f:
      for line in f:
        # skip all rmfield lines
        if checkIfKeywordInStatement(line, 'rmfield'):
          continue
        else:
          print line.rstrip()

  if DELETE_TMP_DIR: shutil.rmtree('./tmp')
  
def findOverriddenVarsAndValues(a_run_file):
  tree = ET.parse(a_run_file)
  root = tree.getroot()

  vars_and_vals = []
  for param in root.findall(".//parameter"):
    attr = param.attrib
    name = attr.get('name')
    value = attr.get('value')

    # ensuring we have a variable name of form eng.plant....
    reg_var = r'[a-zA-Z][a-zA-Z0-9_]*\.([a-zA-Z][a-zA-Z0-9_])+'
    match_var = re.match(reg_var, name)

    if value is not None and match_var:
      vars_and_vals.append(attr) 
 
  logging.info('Number of overridden variables: %s', len(vars_and_vals)) 
  logging.debug('Overridden variables and their values: %s', vars_and_vals)
  return vars_and_vals


def getCmdLineOptsCreateCollapsedMFile(argv):
  help_msg = """Example Usage:\nuser$ python createCollapsedMFile.py -e ../../data/mrzr/evaluation_order_MRZR.txt -m ../../data/mrzr/MRZR_Conv_CVT_2wd_Midsize_wEng_Scaling -a ../../data/mrzr/MRZR.a_run\n
|--------------------------------------------|
|long argument       short argument  required|
|--------------------------------------------|
|--help              -h              False   |
|--evaluation_order  -e              True    |
|--m_file_dir        -m              True    |
|--a_run_file        -a              True    |
|--------------------------------------------|
  """
  if len(argv) < 6:
    print help_msg
    sys.exit(2)
  unix_options, gnu_options = "he:m:a:", ["help", "evaluation_order", "m_file_dir", "a_run_file"]
  in_file, search_path, X = '','',''
  try:
    arguments, values = getopt.getopt(argv, unix_options, gnu_options)
  except getopt.error as err:
    print str(err)
    sys.exit(2)
  for curr_arg, curr_val in arguments:
    if curr_arg in ("-e", "--evaluation_order"):
      in_file = curr_val
    elif curr_arg in ("-m", "--m_file_dir"):
      search_path = curr_val
    elif curr_arg in ("-a", "--a_run_file"):
      a_run_file = curr_val
    elif curr_arg in ("-h", "--help"):
      print help_msg
      sys.exit(2)

  return in_file, search_path, a_run_file


if __name__ == '__main__':
    main(sys.argv[1:])


