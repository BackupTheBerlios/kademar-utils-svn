#! /usr/bin/env python

# -------------------------------------LICENCE----------------------------------
# This application is released under the GNU General Public License v3 (or, at
# your option, any later version). You can find the full text of the license
# under http://www.gnu.org/licenses/gpl.txt.
# By using, editing and/or distributing this software you agree to the terms
# and conditions of this license.
# Thank you for using free software!
# ------------------------------------------------------------------------------

#  CsicStarterScreenlet (c) Adonay Sanz Alsina 2009
#   Based on code of  MusicPlayerDaemon Screenlet (c) Krzysztof Magusiak <chrmag@poczta.onet.pl>


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
import sys
import xml.dom.minidom

# Debugging
#import time # for time.clock() function

# Profiling: execute with '-m cProfiler' option

# i18n
import gettext
gettext.install("CsicStarterScreenlet", os.path.abspath(os.path.dirname(sys.argv[0])) + "/locale")

from common import *

#
# Media Player Daemon
# Main class
#

""" MPD Screenlet """
class CsicStarterScreenlet(screenlets.Screenlet):
	# Info
	__name__ = 'Accessibility - CSIC Starter'
	__version__ = '0.4'
	__author__ = 'Adonay Sanz Alsina -adonay@kademar.org- using code of Krzysztof Magusiak'
	__desc__ = 'Accessibility Csic applet to start applications. Developed for kademar Linux.'	
	
	
	# settings
	global __scrread__
	screenread_buttons = __scrread__ = True
	mypath = sys.argv[0][:sys.argv[0].find('CsicStarterScreenlet.py')].strip()
	
	
	
	# Timeouts
	_paint_interval   = 200
	_timeout_paint    = None
	
	# Runtime variables
	_paint_time      = 0
	_reloadControls  = False
	_filter_text     = ''
	_mousedown       = 0
	_mouse_pos       = [0, 0]
	_pl_line_height  = 1
	_buffer_back     = None
	_ci_theme        = None # group (all the interface controls)
	_ci_ctrl_vol     = None # volume
	_ci_ctrl_chks    = None # group of 4 buttons: repeat, random, single, consume
	_ci_pbr_img      = None # group of 4 images: done, bg, left, right
	_ci_playlist     = None # group of 2 buttons: playlist, playlist_scroll
	_ci_coverart     = None # image
	_ci_filter_text  = None # filter text
	_ci_txt_template = None # ciTemplate
	
	# Display
	d_show_over  = True
	d_text_font  = 'Sans 8'
	d_text_color = [1, 1, 1, 1]
	
	"""
	Initializes the MPD screenlet.
	"""
	def __init__(self, **keyword_args):
		# Screenlet
		screenlets.Screenlet.__init__(self, width=int(400), height=int(300),uses_theme=True, **keyword_args) 
		self.theme_name = 'default'
		self.add_options_group('Csic Starter', 'Specific options')

		self.add_option(BoolOption('Csic Starter', 'screenread_buttons', self.screenread_buttons, 'Screenreader', 'Enable reading content button with a screenreader'))
		# Defautl values
		__scrread__ = self.screenread_buttons
		
	"""
	Sets an attribute.
	"""
	def __setattr__(self, name, value):
		screenlets.Screenlet.__setattr__(self, name, value)
		if name == '_paint_interval':
			if self._timeout_paint != None:
				gobject.source_remove(self._timeout_paint)
			self._timeout_paint = gobject.timeout_add(value, self.update_check)
			print(_('Paint check rate set to %dms') % value)
		elif name == "screenread_buttons":
			global __scrread__
			__scrread__ = value
			print "chnged scrread", value

	def __say__(self, txt):
		if __scrread__:
			#print "say ",txt
			os.system('spd-say "'+txt+'" &')
		#else:
			#print "nosay ", txt

	def on_init(self):
		#print('MPD Screenlet has been initialized.')
		
		# Menu
		#self.add_default_menuitems(DefaultMenuItem.XML)
		self.add_default_menuitems(DefaultMenuItem.STANDARD)
		#self.add_default_menuitems(DefaultMenuItem.SIZE | DefaultMenuItem.THEMES | DefaultMenuItem.WINDOW_MENU | DefaultMenuItem.PROPERTIES | DefaultMenuItem.DELETE | DefaultMenuItem.QUIT)
		
		# MPD
		#self.mpd.update(force = True)
		
		# Initialize controls
		self.loadControls(forceLoad = True)
		#self.playlist.sel = self.playlist.cur
		
		# Timeouts
		self.__setattr__('_paint_interval', self._paint_interval)
		
		# Update
		self.update_shape()
	
	"""
	Loads the screenlet interface.
	"""
	def loadControls(self, forceLoad = False):
		self._reloadControls = False
		if self.theme == None or (not forceLoad and self._ci_theme == None):
			print(_('Interface not loaded...'))
			self._ci_theme = None
			return
		print(_('Loading the screenlet interface: %s' % str(self.theme_name)))
		try:
			dom = xml.dom.minidom.parse(os.path.join(self.theme.path, 'theme_display.xml'))
			display = dom.getElementsByTagName('display')[0]
		except:
			print(_('Error: Invalid theme display (xml file)'))
			return
		self.width = int(display.getAttribute('width'))
		self.height = int(display.getAttribute('height'))
		# Initialize _ci_*
		self._ci_theme        = ciGroup()
		self._ci_ctrl_vol     = None
		self._ci_ctrl_chks    = ciGroup(elements = 4)
		self._ci_pbr_img      = None
		self._ci_playlist     = ciGroup(elements = 2)
		self._ci_coverart     = None
		self._ci_filter_text  = None
		self._ci_txt_template = ciTemplate(True)
		# Initialize other properties
		self.dc_vol      = {'bg': None, 'used': [0, 0, 1, 1]}
		self.dc_playlist = {'cur': [0, 0, 0, 1], 'sel': [0, 0, 1, 1], 'sel_bg': [0, 0, 0, 0], 'text': None, \
			'scroll': {'color' : [0.2, 0.2, 0.2, 1], 'rounded': 0, 'border': {'width': 0, 'color': [0, 0, 0, 0]}}}
		# Load
		self.loadControlsNode(self._ci_theme, display)
		# Background buffer
		self._buffer_back = gtk.gdk.Pixmap(self.window.window, int(self.width * self.scale), int(self.height * self.scale), -1)
		bctx = self._buffer_back.cairo_create()
		self.clear_cairo_context(bctx)
		bctx.scale(self.scale, self.scale)
		self._ci_theme.paint(self, bctx, 2)
		# Update
		#self.update(plForceUpdate = True, updateCover = True)
		#gc.collect()
	
	"""
	Loads a node from a theme display file.
	"""
	def loadControlsNode(self, ci, node):
		if node.nodeType == 1:
			for n in node.childNodes:
				if n.nodeType == 1:
					type = n.nodeName
					obj  = None
					grp  = None
					if type == 'execute':
						try:
							ex = n.childNodes[0].nodeValue.strip()
							if ex[:5] != 'self.': ex = 'self.' + ex
							if ex.find('=') != -1 and ex.find('\n') == -1: exec(ex)
						except: pass
					elif type == 'group':
						grp = obj = ciGroup()
					elif type == 'text':
						obj = ciText(''.join(map(xml.dom.minidom.Node.toxml, n.childNodes)).strip(), template = self._ci_txt_template)
						try: obj.width = int(n.getAttribute('width'))
						except: obj.width = self.width - safe_int(n.getAttribute('x'))
						try: exec('obj.color = ' + n.getAttribute('color'))
						except: obj.color = self.d_text_color
						default_font = font_split(self.d_text_font)
						(obj.font, obj.size) = font_split(n.getAttribute('font'), default_font[1])
						if obj.font == '': obj.font = default_font[0]
						obj.size = safe_int(n.getAttribute('size')) or obj.size
						align = n.getAttribute('align')
						if align == 'center': obj.align = pango.ALIGN_CENTER
						elif align == 'right': obj.align = pango.ALIGN_RIGHT
						singleline = n.getAttribute('singleline')
						if len(singleline) > 0: obj.line = int(singleline) > 0
					elif type == 'image' or type == 'button':
						obj = ciButton(n.getAttribute('src'))
						if self.d_show_over: obj.srcOver = n.getAttribute('src_over')
						ratio = n.getAttribute('preserve_scale_ratio')
						if len(ratio) > 0: obj.pre_aspect = bool(int(ratio))
						try: exec('obj.eventClick = ' + n.getAttribute('on_click'))
						except: obj.eventClick = None
						action = n.getAttribute('action')
						if action: obj.action = action
						
						#set text to read
						text = n.getAttribute('text')
						if action: obj.text = text
						
						hover = n.getAttribute('hover')
						if action: obj.hover = hover
						
						obj.parent = self
						
						obj.ident = n.getAttribute('id')
						
					if type == 'group' or type == 'image' or type == 'button':
						obj.width = safe_int(n.getAttribute('width')) or -1
						obj.height = safe_int(n.getAttribute('height')) or -1
					if obj != None:
						ci.add_ci(obj)
						obj.x = safe_int(n.getAttribute('x'))
						obj.y = safe_int(n.getAttribute('y'))
						try: exec('obj.eventPaint = ' + n.getAttribute('on_paint'))
						except: obj.eventPaint = None
						if n.getAttribute('background'): obj._back = True
						self.loadControlsNodeCheck(obj, n.getAttribute('id'))
						if grp != None: self.loadControlsNode(grp, n)
	
	
	def event_player_click(self, a):
		#print "weno", a
		#print a.ident
		os.system(a.ident+" &")
	"""
	Checks if the object has to be saved for other purposes.
	"""
	def loadControlsNodeCheck(self, obj, name):
		if obj == None or name == None or name == '':
			return
		elif name == 'progress':
			self._ci_pbr_img = obj
			if obj.width < 1: obj.width = self.width - 2 * obj.x
		elif name[:9] == 'progress_':
			if self._ci_pbr_img.height > 0 and obj.height < 1: obj.height = self._ci_pbr_img.height
			if name == 'progress_right': obj.x = self._ci_pbr_img.width
		elif name == 'volume': self._ci_ctrl_vol = obj
		elif name == 'repeat': self._ci_ctrl_chks[0] = obj
		elif name == 'random': self._ci_ctrl_chks[1] = obj
		elif name == 'single': self._ci_ctrl_chks[2] = obj
		elif name == 'consume': self._ci_ctrl_chks[3] = obj
		elif name == 'playlist': self._ci_playlist[0] = obj
		elif name == 'playlist_scroll': self._ci_playlist[1] = obj
		elif name == 'coverart': self._ci_coverart = obj
		elif name == 'pl_filter_text': self._ci_filter_text = obj


	
	"""
	Checks whether the interface has to be redrawn.
	@return True
	"""
	def update_check(self):
		if self._ci_theme and self._ci_theme._toPaint:
			self.redraw_canvas()
		return True

	"""
	Draws the interface.
	"""
	def on_draw(self, ctx):
		if self._ci_theme != None:
			ctx.set_operator(cairo.OPERATOR_OVER)
			ctx.save()
			if self._buffer_back:
				ctx.set_source_pixmap(self._buffer_back, 0, 0)
				ctx.paint()
			ctx.scale(self.scale, self.scale)
			self._ci_theme.paint(self, ctx)
			ctx.fill()
			ctx.restore()
	 
	def on_draw_shape(self, ctx):
		self.on_draw(ctx)

	

	
	def on_mouse_down(self, event):
		self._mousedown = event.button
		self._mouse_pos = [(event.x_root - self.x) / self.scale, (event.y_root - self.y) / self.scale]
		if event.button == 1:
			if self._ci_theme:
				if self._ci_theme.mouse_click(self._mouse_pos[0], self._mouse_pos[1], self._mousedown):
					return True
			self.is_dragged = True
		elif event.button == 3:
			self.menu.popup(None, None, None, event.button, event.time)
		return False
	
	def on_mouse_up(self, event):
		self._mousedown = 0
		return True
	
	def on_mouse_move(self, event):
		self._mouse_pos = [(event.x_root - self.x) / self.scale, (event.y_root - self.y) / self.scale]
		if self._ci_theme and self.d_show_over:
			self._ci_theme.isOver(self._mouse_pos[0], self._mouse_pos[1])
		return True
	
	def on_mouse_leave(self, event):
		self._mousedown = 0
		return self.on_mouse_move(event)

	def on_scale(self):
		self.loadControls()
	
	def on_load_theme(self):
		self.loadControls()

# Start the screenlet
if __name__ == '__main__':
	import screenlets.session
	screenlets.session.create_session(CsicStarterScreenlet)
