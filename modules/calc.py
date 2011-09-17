#encoding:UTF-8
#
# Copyright (C) 2011 - pyAnna
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details at
# http://www.gnu.org/copyleft/gpl.html
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses>.
#

from module import Module

class Calc(Module):
	def __init__(self, room):
		self.room = room

	def convert(self, expression):
		operateurs = "+*-/x"
		chiffres = "0123456789"
		priorite = dict()
		priorite['+'] = 1
		priorite['-'] = 1
		priorite['*'] = 2
		priorite['x'] = 2
		priorite['/'] = 2
		s = []
		ss = [s]
		postfix = []
		prev_was_chiffre = False 
		for e in expression:
			if e in operateurs:
				while len(s) > 0:
					t = s.pop()
					if priorite[t] >= priorite[e]:
						postfix.append(t)
					else:
						s.append(t)
						break
				s.append(e)
				prev_was_chiffre = False
			elif e in chiffres:
				if prev_was_chiffre:
					t = postfix.pop()
					postfix.append(t * 10 + int(e))
				else:
					postfix.append(int(e))
				prev_was_chiffre = True
			elif e == '(':
				s = []
				ss.append(s)
			elif e == ')':
				while len(s) > 0:
					postfix.append(s.pop())

				ss.pop()
				s = ss.pop()
				ss.append(s)

		while len(s) > 0:
			postfix.append(s.pop())
					
		return postfix
	
	def calc(self, expression):
		postfix = self.convert(expression)
		s = []
		for symbol in postfix:
			if type(symbol) == int:
				s.append(symbol)
			else:
				a2 = s.pop()
				a1 = s.pop()
				if symbol == '+':
					r = a1 + a2
				elif symbol == '-':
					r = a1 - a2
				elif symbol == '/':
					r = a1 / a2
				elif symbol == '*' or symbol == 'x':
					r = a1 * a2
				s.append(r)
		return s.pop()

	def handle_message(self, msg):
		if msg['body'].startswith("!calc "):
			try:
				self.room.send_message(str(self.calc(msg['body'][6:])))
			except:
				self.room.send_message('yé pas compris.')

	def handle_private_message(self, msg, to):
		if msg['body'].startswith("!calc "):
			try:
				self.room.send_private_message(str(self.calc(msg['body'][6:])), to)
			except:
				self.room.send_message('yé pas compris.')
