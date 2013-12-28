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


from getopt import getopt
from os.path import abspath, basename, exists, splitext
from sys import argv, exit, stderr, stdout
try :
	from PIL import Image
	from io import BytesIO
except ImportError :
	BytesIO = None
from pys2f import SvgFramesRenderer as SFR


class Output (object) :

	def __init__ (self, input_file, output_file) :
		self.input_file = input_file
		self.output_file = output_file

	def configure (self, fps, dur, width, height, time_offset, first_index, position, background, border) :
		self.fps = fps
		self.dur = dur
		self.frames = int(fps * self.dur) + 1
		self.width = width
		self.height = height
		self.time_offset = time_offset
		self.first_index = first_index
		self.position = position
		self.background = background
		self.border = border

	def render (self) :
		svg = SFR("file://" + self.input_file, self.fps, self.width, self.height, self.time_offset, self.position, self.background, self.border)
		for frame in range(self.frames) :
			png = svg.render_frame_as_png(frame)
			frame += self.first_index
			if png :
				self.save(frame, png)
			else :
				print_warning("frame %d has no data" % frame)

	def save (self, frame, png) :
			with open(self.output_file % frame, 'wb') as file :
				file.write(png)


class PngOutput (Output) :

	def __init__ (self, input_file, output_file) :
		try :
			output_file % 42
		except TypeError :
			basename, ext = splitext(output_file)
			output_file = basename + ".%d" + ext
			output_file % 23
		Output.__init__(self, input_file, output_file)


class ImageOutput (PngOutput) :

	def __init__ (self, input_file, ext, output_file) :
		if not BytesIO :
			raise KeyError(ext)
		PngOutput.__init__(self, input_file, output_file)

	def save (self, frame, png) :
		Image.open(BytesIO(png)).save(self.output_file % frame)



def get_output (args) :
	if exists(args[0]) :
		input_file = abspath(args[0])
		output_file = args[1] if len(args) > 1 else "frame.%d.png"
		ext = splitext(output_file)[-1]
		if ext == ".png" :
			return PngOutput(input_file, output_file)
		elif not ext :
			return PngOutput(input_file, output_file + ".%d.png")
		elif ext == ".gif" :
			try :
				output_file % 404
			except :
				pass
		elif ext == ".apng" :
			pass
		elif ext == ".mng" :
			pass
		return ImageOutput(input_file, ext, output_file)
	raise IOError("file '%s' not found" % args[0])


def get_opts (iargs) :
	args = []
	opts = []
	while iargs :
		args.append(iargs[0])
		iopts, iargs = getopt(iargs[1:], 'h', ['help', 'fps=', 'dur=', 'size=', 'elapsed=', 'first-index=', 'position=', 'background=', 'border='])
		opts = opts + iopts
	return args[1:], opts


def get_color (string) :
	color = string.split(',')
	if len(color) == 1 :
		color.append(1)
	try :
		color, opacity = color
		if color.lower() == 'white' :
			color = [1, 1, 1]
		elif color.lower() == 'black' :
			color = [0, 0, 0]
		elif len(color) != 6 :
			raise Exception
		else :
			color = [int(color[0:2], 16) / 255.0, int(color[2:4], 16) / 255.0, int(color[4:6], 16) / 255.0]
		color.append(float(opacity))
		return color
	except :
		raise ValueError("invalid color format '%s'" % string)


def main () :
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	if set(('-h', '--help')).intersection(argv) :
		print_usage(stdout)
		print_help(stdout)
		exit(0)
	try :
		args, opts = get_opts(argv)
		if args :
			fps = 25
			dur = 1
			width = 0
			height = 0
			time_offset = 0
			first_index = 0
			position = 0
			background = None
			border = None
			for opt, arg in opts :
				if opt == '--fps' :
					fps = int(arg)
				elif opt == '--dur' :
					dur = float(arg)
				elif opt == '--size' :
					values = arg.split('x')
					width = int(values[0] or 0)
					if len(values) > 1 :
						height = int(values[1] or 0)
				elif opt == '--elapsed' :
					time_offset = float(arg)
				elif opt == '--first-index' :
					first_index = int(arg)
				elif opt == '--position' :
					arg = arg.upper()
					if arg == 'START' :
						position = SFR.POSITION_START
					elif arg == 'END' :
						position = SFR.POSITION_END
					elif arg == 'CENTER' :
						position = SFR.POSITION_CENTER
				elif opt == '--background' :
					background = get_color(arg)
				elif opt == '--border' :
					border = get_color(arg)
			output = get_output(args)
			output.configure(fps, dur, width, height, time_offset, first_index, position, background, border)
			output.render()
			exit(0)
		print_usage(stderr)
	except KeyError as format :
		print_error("image format %s not supported" % format)
	except Exception as error :
		print_error(error)
	exit(1)


def print_usage (stream) :
	stream.write("Usage: %s [options] input_file [output_file]\n" % (basename(argv[0]) or "svg2fps"))


def print_help (stream) :
	stream.write("""
  -h, --help                 display this help and exit

      --fps=INT              frames per second, defaults to 25
      --dur=FLOAT            duration in seconds, defaults to 1

      --size=SIZE           size of document
                             SIZE is [<width>][x<height>]
      --position=STRING      position of document, defaults to CENTER
                             either CENTER, START or END

      --background=COLOR     backgroundcolor of document
      --border=COLOR         color where canvas is not drawn
                             defaults to transparent
                             COLOR is either white, black or 'RRGGBB' hex
                             opacity can be set as value between 0.0 and 1.0,
                             seperated by a comma, eg. 'ff00ff,0.5'

      --elapsed=FLOAT        time offset of animation
      --first-index=INT      start numbering with INT
""")


def print_error (error) :
	stderr.write("Error: %s\n" % error)


def print_warning (warning) :
	stderr.write("Warning: %s\n" % warning)


if __name__ == '__main__' :
	main()
