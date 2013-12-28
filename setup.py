#	This file is part of pys2f.
#	
#	Copyright (c) 2013 Christian Schmitz <tynn.dev@gmail.com>
#
#	pys2f is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	pys2f is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pys2f. If not, see <http://www.gnu.org/licenses/>.

import os
from distutils.command.build_scripts import build_scripts as _build_scripts
from distutils.core import setup

class build_scripts (_build_scripts) :
	def copy_scripts (self) :
		# a little (dirty) hack to remove the .py extension
		_basename = os.path.basename
		os.path.basename = lambda path : os.path.splitext(_basename(path))[0]
		_build_scripts.copy_scripts(self)
		os.path.basename = _basename

setup(
	cmdclass={'build_scripts': build_scripts}, # if the basename trick fails, disable here ...
	name = 'pys2f',
	version = '0.1',
	author = 'Christian Schmitz',
	author_email = 'tynn.dev@gmail.com',
	license = 'GPLv3+',
	description = '',
	long_description = '',
	url = 'https://github.com/tynn/pys2f',
	platforms = ['any'],
	py_modules = ['pys2f'],
	scripts = ['svg2fps.py', 'svg2png.py']
)

