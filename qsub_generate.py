#!/usr/bin/env python
# -*- coding: utf-8 -*-

# by harry mangalam, uc irvine. 2011

"""
This is a qsub script generator skeleton to show how to use python to
emit qsub scripts.  This could be used as a more sophisticated way of
generating input variables for a repeated analysis that does somthing
a Monte Carlo sampling of parameter space.

It will do this by:
- creating a multi-line qsub bash script as a Python string
- generating a set of variables in a master loop
- in that loop,
  - doing some basic string substitution to create a unique instance of
    the variables and the qsub script/string
  - writing the qsub string to a file, along with the created input file
  - printing the qsub command or
  - exec'ing qsub on that file to submit it to SGE.

In this script, we will use 'trial.py' as the target script that will be
launched by SGE on as many cores as possible.  It requires an input file
that will be called xxx.[trial].param and will write to a file called
xxx.[trial].output where 'xxx' is identical for one submission and [trial]
is set in the code below (fncore) to be any string desired.
ie: a run would be initiated from a shell as:
$ trial.py 973.trial.param > 973.trial.output

"""

import sys, os, commands, random
from pydoc import pipepager

# for superior debugging support, iPython is unbeatable
from IPython.Shell import IPShellEmbed
dbg = IPShellEmbed(['']) # and insert 'dbg()' where you want to break.

### Globals
fncore = "trial"
param={} # the hash that stores the
infiles = []
outfiles = []

### defs

# usage if you want to create a help file and read it with the 'less' pager
def usage(code, msg=''):
    #read in the help file
    try:
        help_fp = file("qsubber_help.txt", "r")
        help_txt = help_fp.read()
    except:
        print "Can't find the help file - should be called 'qsubber_help.txt' - Did you rename it?"
        sys.exit(code)
    pipepager(help_txt, '/usr/bin/less -NS') # pipe help text into 'less -NS'
    sys.exit(code)


### Main part of program

# define the qsub skeleton string and a tmp/backup
qsub_tmp_skel = SGE_qsub_skel='''
#!/bin/bash

# the following SGE parameters (#$ lines) may need to be changed
# depending on what the length of run and other requirements are.

#$ -S /bin/bash    # run with this shell
#$ -q long-ics     # run in this Q
#$ -l h_rt=50:00:00  # need 50 hour runtime

# load the appro module
module load enthought_python

# trial.py is responsible for reading _INFILE_ and printing to STDOUT
python trial.py  _INFILE_ > _OUTFILE_
'''

### Set the range of the input parameters
##  This will use simple ranges to set some input parameters
##  We'll set 5 parameters for each file.

### Define the input params and a tmp/backup.  Only for demo purposes.
TMP_TEMPLATE = QSUB_TEMPLATE = '''
# input file for trial.py, test _SUB_iteration
random   = _SUB_random    # random float seed (0-1)
range    = _SUB_range     # int range (iteration * 100)
x_rng_s  = _SUB_x_rng_s   # int start  (int)
x_rng_e  = _SUB_x_rng_e   # int end    (int)
y_rng_s  = _SUB_y_rng_s   # int start  (int)
y_rng_e  = _SUB_y_rng_e   # int end    (int)
z_rng_s  = _SUB_z_rng_s   # int start  (int)
z_rng_e  = _SUB_z_rng_e   # int end    (int)
picollo  = _SUB_picollo   # float seed (1-100)
flower   = _SUB_flower    # int seed   (1-5)
'''

# idx[] is related to the params below as a way to step thru the variables
# and ease the autogeneration of them.  If you set up your variables in a different
# way, you will omit this array.
idx = ("iteration", "random", "range", "x_rng_s", "x_rng_e", "y_rng_s", "y_rng_e", "z_rng_s", "z_rng_e", "picollo", "flower")

# generate the intput params - this is all BS of course.
# Replace or mod with your own set  of params or you can even
# manually edit them if necessary.

for iter in range(0, 5):
	# set the variables
	param["iteration"] = iter
	param["random"] = random.random()
	param["range"] = iter*100
	param["x_rng_s"] = random.randint(1, 100)
	param["x_rng_e"] = random.randint(1, 100)
	if param["x_rng_s"] > param["x_rng_e"]:
		param["x_rng_s"], param["x_rng_e"] = param["x_rng_e"], param["x_rng_s"]
	param["y_rng_s"] = random.randint(1, 100)
	param["y_rng_e"] = random.randint(1, 100)
	if param["y_rng_s"] > param["y_rng_e"]:
		param["y_rng_s"], param["y_rng_e"] = param["y_rng_e"], param["y_rng_s"]
	param["z_rng_s"] = random.randint(1, 100)
	param["z_rng_e"] = random.randint(1, 100)
	if param["z_rng_s"] > param["z_rng_e"]:
		param["z_rng_s"], param["z_rng_e"] = param["z_rng_e"], param["z_rng_s"]
	param["picollo"] = random.uniform(1, 100)
	param["flower"] =  random.randint(1, 5)
	# now write them to the file
	ifname = str(iter) + "." + fncore + ".param"
	ofname = str(iter) + "." + fncore + ".output"
	#dbg()

	# don't need the following 2 lines anymore since it's all being
	# done in a loop
	#infiles[iter]  = ifname
	#outfiles[iter] = ofname # since we're iterating..
	pf = open(ifname, 'w')
	for it in range(11):
		# substitute all the indexes
		oldstr = '_SUB_' + idx[it]
		#print oldstr
		newstr = str(param[idx[it]])
		#print newstr
		QSUB_TEMPLATE = QSUB_TEMPLATE.replace(oldstr, newstr)
	pf.write(QSUB_TEMPLATE)
	pf.close()
	QSUB_TEMPLATE = TMP_TEMPLATE # and reset the template
	# should now have however many files that we need to supply the qsubber
	# and the names are stored in infiles[] and outfiles[]

	#substitute the qsub script template
	SGE_qsub_skel = SGE_qsub_skel.replace("_INFILE_", ifname)
	SGE_qsub_skel = SGE_qsub_skel.replace("_OUTFILE_", ofname)
	qsfname = str(iter) + "_" + fncore + "_qsub" + ".sh"
	qsub = open(qsfname, 'w')
	qsub.write(SGE_qsub_skel)
	qsub.close()
	SGE_qsub_skel = qsub_tmp_skel  #reset the skeleton

	# and finally submit it to SGE with qsub
	cmd = "qsub " + qsfname

	# now we print the command.  When it's printing OK, we uncomment the
	# commands.getstatusoutput(cmd) line below it
	print cmd

	#qsub_status = commands.getstatusoutput(cmd)

	# process qsub_status for error-checking, etc as you want
	# returns the return value and combined STDERR & STDOUT of the cmd in a list.





