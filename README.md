pys2f
=====

#### The module

*pys2f* is a *ctypes* wrapper for [libsvg2fps](https://github.com/tynn/libsvg2fps).


#### Applications

*svg2png* is a simple console script to render an SVG image as PNG. The elapsed time will be set to 0.

*svg2fps* is a console script to render an SVG animation as a series of bitmap images.
The default output format is PNG. GIF and JPG are supported through the *PIL* module.


Installation
------------

Install with

	 python setup.py install

The .py extension of the script files will be removed by default.  
To retain them comment out the line

		cmdclass = {'build_scripts': build_scripts}, # remove .py extensions

in [setup.py](setup.py)

