#!/usr/bin/env python
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


from os.path import abspath, basename, exists
from re import match, sub
from sys import argv, exit, stderr, stdout
from pys2f import load_svg_document


def error (error = None) :
	if error : stderr.write("Error: {:s}\n".format(error))
	stderr.write("Usage: {:s} uri [output_file] [size]\n".format(basename(argv[0]) or "svg2png"))
	exit(1)


def get_uri () :
	if len(argv) > 1 :
		uri = argv[1]
		if match(r'\w+://', uri) : return uri
		if exists(uri) : return "file://" + abspath(uri)
		return "http://" + uri
	error()

def get_size () :
	size = {}
	if len(argv) > 3 :
		values = argv[3].split('x')
		try : size['width'] = int(values[0])
		except : pass
		if len(values) > 1 :
			try : size['height'] = int(values[1])
			except : pass
	return size

def write_png () :
	png = load_svg_document(get_uri(), handle_error = error, **get_size()).render_frame_as_png(0)
	if png :
		if len(argv) > 2 :
			with open(argv[2], 'wb') as file : file.write(png)
		else : stdout.write(png)
	else : error()


def main () :
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	write_png()


if __name__ == '__main__' :
	main()
