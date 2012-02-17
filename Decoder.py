'''
@name    Decoder
@package sublime_plugin
@author  Neil Opet

This Sublime Text 2 plugin adds encoding/encryption and decoding
features to the right click context menu.

To use, you just select a string and right click it, then select the Decode or Encode
menu options and select the tool you wish to use from there.
'''

import sublime
import sublime_plugin
import md5
import sha
from base64 import b64encode, b64decode
from binascii import b2a_uu
from urllib import quote, unquote
from cgi import escape

# needed functions
def append0( string ):
	bstr = string.replace('b', '')
	if len(bstr) == 8:
		return bstr
	return '0' + bstr

def int2( string ):
	return int( string, 2 )

def int16( string ):
	return int( string, 16 )

# Selected Word Handler
class Word(object):
	def getSelected(self, view):
		region   = view.sel()[0]
		return {"region" : region, "word" : view.substr(view.word(region))}
	def insert(self, edit, view, region, string):
		view.erase(edit, region)
		view.insert(edit, region.begin(), string)

# Base64 Decode
class Base64DecodeCommand(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(edit, self.view, word['region'], b64decode(word['word']))

# Base64 Encode
class Base64EncodeCommand(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(edit, self.view, word['region'], b64encode(word['word']))

# Hex to String
class HexToStringCommand(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(
			edit, 
			self.view, 
			word['region'],
			''.join(map(chr, map(int16, [word['word'][n:n+2] for n in xrange(0, len(word['word']), 2)])))
		)

# String to Hex
class StringToHexCommand(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(
			edit, 
			self.view, 
			word['region'], 
			''.join(map(hex, map(ord, word['word']))).replace('0x', '')
		)

# Binary to String
class BinaryToStringCommand(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(
			edit, 
			self.view, 
			word['region'],
			''.join(map(chr, map(int2, [word['word'][n:n+8] for n in xrange(0, len(word['word']), 8)])))
		)

# String to Binary
class StringToBinaryCommand(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(
			edit, 
			self.view, 
			word['region'], 
			"".join(map(append0, map(bin, map(ord, word['word']))))
		)
	
# Url Encode
class UrlEncodeToStringCommand(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(
			edit, 
			self.view, 
			word['region'],
			unquote(word['word'])
		)

# Url Decode
class StringToUrlEncodeCommand(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(
			edit, 
			self.view, 
			word['region'], 
			quote(word['word'])
		)

# HTML Special Chars
class StringToHtmlSpecialChars(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(
			edit,
			self.view,
			word['region'],
			escape(word['word'], True)
		)

# Md5 encryption
class StringToMd5(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(
			edit,
			self.view,
			word['region'],
			md5.new(word['word']).hexdigest()
		)

# Sha-1 encryption
class StringToSha1(sublime_plugin.TextCommand, Word):
	def run(self, edit):
		word = self.getSelected(self.view)
		self.insert(
			edit,
			self.view,
			word['region'],
			sha.new(word['word']).hexdigest()
		)