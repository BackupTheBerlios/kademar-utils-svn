#! /usr/bin/env python

# -------------------------------------LICENCE----------------------------------
# This application is released under the GNU General Public License v3 (or, at
# your option, any later version). You can find the full text of the license
# under http://www.gnu.org/licenses/gpl.txt.
# By using, editing and/or distributing this software you agree to the terms
# and conditions of this license.
# Thank you for using free software!
# ------------------------------------------------------------------------------


#Direct code get from MusicPlayerDaemon classes and functions
from string import Template
import screenlets
from screenlets.options import StringOption, BoolOption, IntOption, FontOption, ColorOption
from screenlets import DefaultMenuItem, Plugins
import cairo
import gobject
import gtk
import os
import pango
import rsvg

"""
Escapes some of the html entities.
@param s String to escape
@return Escaped string
"""
def htmlentities(s):
	REPLACEMENTS = { '&': '&amp;', '<': '&lt;', '>': '&gt;' }
	out = ''
	for c in s:
		if c in REPLACEMENTS: c = REPLACEMENTS[c]
		out += c
	return out

"""
Removes last printed characters from a HTML string.
@param s The HTML string
@param times How many characters should be stripped (default: 1)
@return The new HTML string
"""
def htmlremovelastchars(s, times = 1):
	if times < 1 or len(s) < 1: return s
	c = s[-1]
	if c == '>':
		p = s.rfind('<')
		if p == -1: raise Exception(_('Invalid string!'))
		mclose = s[p:]
		mopen = mclose[0] + mclose[2:]
		p = s.rfind(mopen)
		if p == -1: raise Exception(_('Invalid string!'))
		text = s[p:]
		text = text[len(mopen):-len(mclose)]
		text = htmlremovelastchars(text)
		if text != "": text = mopen + text + mclose
		s = s[:p] + text
	else:
		if c == ';' and s.rfind('&', -5):
			s = s[:s.rfind('&', -5)]
		if (len(s) <= 1): s = ''
		else: s = s[:-1]
	return htmlremovelastchars(s, times - 1)

"""
Removes last chars from a string.
@param s The string
@param isHTML Whether the string is a HTML string (default: False)
@param times How many characters should be stripped (default: 1)
@return The new string
"""
def removelastchars(s, isHTML = False, times = 1):
	if times < 1 or len(s) < 1: return s;
	if isHTML:
		try: return htmlremovelastchars(s, times)
		except: pass
	return s[:-int(times)]

"""
Safe conversion to an integer.
@param s
@return int(s) or 0
"""
def safe_int(s):
	try: return int(s)
	except: return 0

"""
Returns a tuple for the given font.
Example: font_split('Arial 9') => ('Arial', 9)
@param font The font string
@param dsize The default font size, used when could not parse (default: 8)
@return Tuple (name, size)
"""
def font_split(font, dsize = 8):
	name = font.rstrip(' 0123456789')
	size = safe_int(font[len(name)-len(font):].strip())
	if size < 1: size = dsize
	return (name, size)

"""
Returns the line count of a given text.
@return How many lines needs the text to be painted
"""
def get_text_size(drawable, ctx, text, font, size, width = 9999, weight = 0, isHTML = True):
	if text == '': return ((0, 0), (0, 0), 0, (0, 0), False)
	ctx.save()
	if drawable.p_layout == None:
		drawable.p_layout = ctx.create_layout()
	else:
		drawable.p_layout.set_text('')
		ctx.update_layout(drawable.p_layout)
	lay = drawable.p_layout
	if drawable.p_fdesc == None:
		drawable.p_fdesc = pango.FontDescription()
	fnt = drawable.p_fdesc
	fnt.set_family(font)
	fnt.set_size(size * pango.SCALE)
	fnt.set_weight(weight)
	lay.set_font_description(fnt)
	lay.set_width(width * pango.SCALE)
	if isHTML:
		lay.set_markup(text)
	else:
		lay.set_text(text)
	extents, lextents = lay.get_pixel_extents()
	lines = lay.get_line_count()
	ctx.restore()
	return ((extents[2], extents[3]), \
		(lextents[2], lextents[3]), \
		lines, \
		((extents[2] + lextents[2]) / 2, (extents[3] + lextents[3]) / 2), \
		lines > 1 or lextents[2] > width)

"""
Strips the text, so it can be printed on a single line.
@return New text
"""
def fix_text_render_on_line(drawable, ctx, text, font, size, width, weight = 0, isHTML = True):
	ln = get_text_size(drawable, ctx, text, font, size, width, weight, isHTML)
	if ln[4]:
		if ln[2] > 2: text = removelastchars(text, isHTML, len(text) * (2.0 / ln[2]))
		else: text = removelastchars(text, isHTML)
		del ln
		while get_text_size(drawable, ctx, text + '...', font, size, width, weight, isHTML)[4]:
			text = removelastchars(text, isHTML)
		text += '...'
	return text

#
# Interface management
#

""" Interface event """
class ciEvent():
	source = None
	action = ''
	button = 0
	x      = 0
	y      = 0
	time   = 0
	
	"""
	Initializes a new event.
	@param source The source object (default: None)
	"""
	def __init__(self, source = None):
		self.source = source
		self.time   = int(gobject.get_current_time() * 1000)

""" Interface object """
class ciObject():
	x          = 0
	y          = 0
	eventPaint = None # function(slet, ctx)
	_back      = False
	
	"""
	Tells whether the object can be painted.
	@param type 0: no bg; 1: all; 2: bg
	@return Boolean telling if the object can be painted
	"""
	def canPaint(self, type):
		return (type != 0 or not self._back) and (type != 2 or self._back)
	
	"""
	Paints the object.
	"""
	def paint(self, slet, ctx, type = 0):
		if self.canPaint(type) and self.eventPaint:
			ctx.save()
			ctx.translate(self.x, self.y)
			self.eventPaint(slet, ctx)
			ctx.restore()

""" Interface text """
class ciText(ciObject):
	text     = ''
	color    = [0, 0, 0, 1]
	font     = ''
	size     = 10
	width    = 9999
	align    = pango.ALIGN_LEFT
	line     = True
	template = None
	
	"""
	New text to paint.
	"""
	def __init__(self, text, x = 0, y = 0, color = [0, 0, 0, 1], font = '', size = 10, width = 9999, align = pango.ALIGN_LEFT, line = True, template = None):
		self.text     = text
		self.x        = x
		self.y        = y
		self.color    = color
		self.font     = font
		self.size     = int(size)
		self.width    = int(width)
		self.align    = align
		self.line     = line
		self.template = template
	
	def canPaint(self, type):
		return self.text != '' and ciObject.canPaint(self, type)

	def paint(self, slet, ctx, type = 0):
		if not self.canPaint(type): return
		ctx.save()
		ctx.set_source_rgba(self.color[0], self.color[1], self.color[2], self.color[3])
		text = self.text
		if self.template: text = self.template.applyTo(text)
		if self.line: text = fix_text_render_on_line(slet, ctx, text, self.font.rstrip(' 1234567890'), self.size, self.width)
		slet.draw_text(ctx, text, self.x, self.y, self.font.rstrip(' 1234567890'), self.size, self.width, self.align)
		ctx.restore()

""" Interface template """
class ciTemplate():
	items = None
	html  = False
	
	def __init__(self, toHTML):
		self.html = toHTML
	
	def getValue(self, name):
		try: return self.items[str(name)]
		except: return None
	
	def setValue(self, name, value):
		if name == None or name == '': return
		if self.items == None: self.items = {}
		value = str(value)
		if self.html: value = htmlentities(value)
		self.items[str(name)] = value
	
	"""
	Applies this template to a string.
	"""
	def applyTo(self, text):
		text = str(text)
		if self.items == None or text.find('$') == -1: return text
		text = Template(text).safe_substitute(self.items)
		return text

""" Interface button or image """
class ciButton(ciObject):
	src        = ''
	srcOver    = ''
	img        = None
	imgOver    = None
	width      = -1
	height     = -1
	_mouseOver = False
	_toPaint   = False
	action     = ''
	text     = ''
	pre_aspect = False
	eventClick = None # function(ciEvent)
	parent = None
	ident = None
	
	def __init__(self, src = '', action = '', text = '', parent = None, ident = None):
		self.src = src
		self.action = action
		self.text = text
		self.parent = parent
		self.ident = ident
	
	def __setattr__(self, name, value):
		self.__dict__[name] = value
		# Reset the image hander when the source has changed
		if name == 'src': self.img = None
		elif name == 'srcOver': self.imgOver = None
	
	"""
	Checks whether (x,y) is over this image or button.
	"""
	def isOver(self, x ,y):
		over = x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height
		if over != self._mouseOver:
			self._mouseOver = over
			self._toPaint = self._toPaint or self.srcOver != ''
		return self._mouseOver
	
	"""
	Gets an image handler for the image name.
	"""
	def getImage(self, slet, src):
		if src == '': return None
		img = None
		type = 'svg'
		if slet.theme.has_key(src + '.svg'):
			img = slet.theme[src + '.svg']
		else: # Try to paint the image (even if it is not in the theme)
			if os.path.isabs(src): path = src
			else: path = os.path.join(slet.theme.path, src)
			if not os.path.isfile(path): path += '.svg' # default extension?
			if os.path.isfile(path):
				if path[-4:] == '.svg':
					try:
						f = open(path, 'r')
						img = rsvg.Handle(data = f.read())
						f.close()
					except: img = None
				elif path[-4:] == '.jpg':
					img = gtk.gdk.pixbuf_new_from_file(path)
					type = 'jpg'
				elif path[-4:] == '.png':
					img = cairo.ImageSurface.create_from_png(path)
					type = 'png'
		if img != None: return (img, type)
		return None
	
	def paint(self, slet, ctx, type = 0):
		self._toPaint = False
		if not self.canPaint(type):
			return
		if self.src == '':
			ciObject.paint(self, slet, ctx)
			return
		img = None
		if self._mouseOver and self.srcOver != '':
			#print "hola"
			if self.imgOver == None:
				self.imgOver = self.getImage(slet, self.srcOver)
			img = self.imgOver
			
			if self.text:
				self.parent.__say__(self.text)
			
			
		if img == None:
			if self.img == None:
				self.img = self.getImage(slet, self.src)
			img = self.img
		if not (img == None or self.width == 0 or self.height == 0):
			if img[1] == 'svg': size = img[0].get_dimension_data()
			else: size = [img[0].get_width(), img[0].get_height()]
			if not size: return
			if self.width < 0: scx = 1.0
			else: scx = float(self.width) / size[0]
			if self.height < 0: scy = 1.0
			else: scy = float(self.height) / size[1]
			if self.pre_aspect: scx = scy = min(scx, scy)
			ctx.save()
			ctx.translate(self.x, self.y)
			ctx.scale(scx, scy)
			if img[1] == 'svg': img[0].render_cairo(ctx)
			else:
				try:
					if img[1] == 'jpg': ctx.set_source_pixbuf(img[0], 0, 0)
					elif img[1] == 'png': ctx.set_source_surface(img[0], 0, 0)
					ctx.rectangle(0, 0, size[0], size[1])
					ctx.fill()
				except: pass
			ctx.restore()

	"""
	Executes the event when (x,y) is over this image or button
	"""
	def mouse_click(self, x, y, button):
		if self.eventClick != None and self.isOver(x, y):
			ev = ciEvent(self)
			ev.action = self.action
			ev.button = button
			ev.x      = x
			ev.y      = y
			ev.ident  = self.ident
			self.eventClick(ev)
			return True
		return False


	
""" Interface group of ci* objects """
class ciGroup(ciButton):
	items = None
	
	def __init__(self, x = 0, y = 0, elements = 0):
		self.x = x
		self.y = y
		while elements > 0:
			self.add_ci(None)
			elements -= 1
	
	def add_ci(self, ci):
		if self.items == None: self.items = [ci]
		else: self.items.append(ci)
		return ci
	
	def __getitem__(self, i):
		return self.items[i]
	
	def __setitem__(self, i, val):
		self.items[i] = val
	
	def __len__(self):
		if self.items == None: return 0
		return len(self.items)
	
	def canPaint(self, type):
		return not self._back or type > 0
	
	def paint(self, slet, ctx, type = 0):
		self._toPaint = False
		if self.items == None or len(self.items) == 0 or not self.canPaint(type):
			return
		if self._back:
			type = 1
		ctx.save()
		ctx.translate(self.x, self.y)
		for i in self.items:
			if i != None:
				i.paint(slet, ctx, type)
		ctx.restore()
	
	def isOver(self, x, y):
		if self.items == None or len(self.items) == 0:
			return False
		over = False
		x -= self.x
		y -= self.y
		for i in self.items:
			try:
				if i.isOver(x, y): over = True
				if i._toPaint: self._toPaint = True
			except (AttributeError): pass
		return over
	
	def mouse_click(self, x, y, button):
		if self.items == None or len(self.items) == 0:
			return False
		x -= self.x
		y -= self.y
		clicked = False
		for i in self.items:
			has_click_method = False
			try: has_click_method = i.mouse_click != None
			except (AttributeError): pass
			if has_click_method and i.mouse_click(x, y, button): clicked = True
		return clicked

