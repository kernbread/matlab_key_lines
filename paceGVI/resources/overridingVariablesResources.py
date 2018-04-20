import sys, re, os, subprocess, tempfile, shutil, getopt
import xml.etree.ElementTree as ET
sys.path.insert(0,'../../')
from paceGVI.resources.scalingResources import *
from paceGVI.resources.lineMatchingResources import *
from paceGVI.resources.LineClass import *

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

def overrideMFiles(overriddenVarsAndValues, in_file, search_path):
  if not os.path.exists('./tmp/'): os.makedirs('./tmp/')
  matfiles = findMFilesFromFile(in_file, search_path)
  for mfile in matfiles:
    shutil.copy(mfile, './tmp/')

  for tmp_mfile in os.listdir('./tmp/'):
    t = tempfile.NamedTemporaryFile(mode='r+')

    tmp_mfile = './tmp/' + tmp_mfile
    with open(tmp_mfile, 'r') as f:
      for line in f:
        line = line.rstrip()
        line_obj = Line(line, tmp_mfile, 0, [], 0)
        for elem in overriddenVarsAndValues:
          if checkIfKeywordInStatement(line_obj.LHS_str, elem['name']):
            logging.info('Appending to %s', tmp_mfile)
            # append to end of file var = val
            write_line = elem['name'] + ' = ' + elem['value'] + ';\n'
            logging.debug('Line appended: %s', write_line.strip())
            t.write(write_line)
            break

    # writing contents of temp file to the temp m file
    t.seek(0)
    with open(tmp_mfile, 'a') as f:
      for line in t:
        f.write('\n' + line)
    t.close()

