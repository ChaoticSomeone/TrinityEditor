import pygame as pg

class Button:
	def __init__(self, name:str, rect:pg.rect.Rect, fg:tuple[int, int, int], bg:tuple[int, int, int], font:pg.font.Font, text:str="", onclick=None, args:tuple|None=None):
		self.name = name
		self.rect = rect
		self.fg = fg
		self.bg = bg
		self.text = text
		self.font = font
		self.onclick = onclick
		self.args = args

	def render(self, surf:pg.Surface):
		pg.draw.rect(surf, self.bg, self.rect)

		text = self.font.render(self.text, True, self.fg, self.bg)
		tRect = text.get_rect()
		x = self.rect.x + self.rect.width / 2 - tRect.width / 2
		y = self.rect.y + self.rect.height / 2 - tRect.height / 2
		surf.blit(text, (x, y))

	def update(self):
		if self.rect.collidepoint(*pg.mouse.get_pos()) and self.onclick is not None:
			if self.args is None:
				return self.name, self.onclick()
			else:
				if isinstance(self.args, tuple):
					return self.name, self.onclick(*self.args)
				else:
					return self.name, self.onclick(self.args)
		return self.name, None