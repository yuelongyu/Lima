###########################################################################
# This file is part of LImA, a Library for Image Acquisition
#
#  Copyright (C) : 2009-2017
#  European Synchrotron Radiation Facility
#  BP 220, Grenoble 38043
#  FRANCE
# 
#  Contact: lima@esrf.fr
# 
#  This is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
# 
#  This software is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.
############################################################################
import sys,os

configFile = 'scripts/config.txt'

#### FOR CI : ONLY LINUX ####
def ConfigGitandOptions(options):
	optionName=[]
	config = []
	del options[0]
	os.system("git submodule --quiet init third-party/Processlib")
	os.system("git submodule --quiet update")
	os.chdir(os.getcwd()+"/third-party/Processlib")
	os.system("git remote rm gitlab")
	os.system("git remote add gitlab git@gitlab.esrf.fr:limagroup/processlib.git")
	os.system("git fetch gitlab")
	os.system("git checkout gitlab/cmake")
	os.chdir(os.getcwd()+"/../..")
	for arg in options:
		if "camera/" in str(arg):
			optionName.append(str.upper(str(arg)[7:]))
		elif "third-party/" in str(arg):
			optionName.append(str.upper(str(arg)[12:]))
		else:
			#probably test or python options.
			optionName.append(str.upper(str(arg)))
	with open(configFile) as f:
		for line in f:
			line=line[:-1]
			for option in optionName:
				if option in line:
					line=line[:-1]
					line=line+str(1)
			if line.startswith('LIMA'):
				if line[len(line)-1]==str(1):
					config.append("-D"+line)
        config= " ".join([str(cmd) for cmd in config])
        return config
	f.close()
#### ONLY LINUX ####
"""
#### WORKS UNDER UNIX & WINDOWS BUT CAN'T BE USED FOR CI ####
def getModuleConfig():
    config = []
    try:
        with open(configFile) as f:
            for line in f:
				if line.startswith('LIMA'):
					if line[len(line)-2]==str(1):
						config.append("-D"+line[:-1])
				elif line.startswith('CMAKE') or line.startswith('PYTHON'):
					config.append("-D"+line[:-1])
        config= " ".join([str(cmd) for cmd in config])
        return config
    except IOError:
        print 'Error'
        raise
#### WORKS UNDER UNIX & WINDOWS BUT CAN'T BE USED FOR CI ####
"""
		
if __name__ == '__main__':
	config = ConfigGitandOptions(sys.argv)
	#config = getModuleConfig()
	print config
