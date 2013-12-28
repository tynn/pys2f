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


import ctypes


def _ensure_bytes (string) :
	return string if isinstance(string, bytes) else string.encode()


def load_svg_document (uri, handle_error = False, **kwargs) :
	try :
		return SvgFramesRenderer(uri, **kwargs)
	except SvgLoadError as error:
		if handle_error :
			if hasattr(handle_error, '__call__') :
				handle_error(error)
			else :
				raise error


class _RGBA (ctypes.Structure) :

	_fields_ = [('r', ctypes.c_double), ('g', ctypes.c_double), ('b', ctypes.c_double), ('a', ctypes.c_double)]


class _Config (ctypes.Structure) :

	_fields_ = [('width', ctypes.c_uint), ('height', ctypes.c_uint), ('time_offset', ctypes.c_double), ('position', ctypes.c_int), ('background', ctypes.POINTER(_RGBA)), ('border', ctypes.POINTER(_RGBA))]


def _rgba (color) :
	if not color :
		return None
	if not isinstance(color, _RGBA) :
		color = _RGBA(*color)
	return ctypes.pointer(color)


class SvgFramesRenderer (object) :

	POSITION_CENTER = 0
	POSITION_START = 1
	POSITION_END = 2

	def __init__ (self, uri, fps = 0, width = 0, height = 0, time_offset = 0, position = 0, background = None, border = None):
		if width or height or time_offset or position or background or border:
			self.config = ctypes.pointer(_Config(width, height, time_offset, position, _rgba(background), _rgba(border)))
		else :
			self.config = None
		self.data = _lib.svg2fps_load_document(_ensure_bytes(uri), fps if fps > 0 else 1, self.config)
		if not self.data :
			raise SvgLoadError("Failed to load document '{:s}' ({:s}x{:s}@{:d}fps)".format(uri, width or '', height or '', fps))

	def __del__ (self) :
		try :
			self.close()
		except :
			pass

	def is_closed (self) :
		return not self.data

	def close (self) :
		if self.data :
			_lib.svg2fps_unload_document(self.data)
			self.data = None

	def render_frame_as_png (self, frame) :
		if self.data :
			buffer = ctypes.pointer(ctypes.c_char())
			size = ctypes.c_ulong()
			if _lib.svg2fps_render_frame_as_png(frame, ctypes.byref(buffer), ctypes.byref(size), self.data) :
				return buffer[:size.value]


class SvgLoadError (Exception) :
	pass


_lib = ctypes.cdll.LoadLibrary("libsvg2fps.so")
