import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import tkinter
import tkinter.filedialog
from sys import exit
pg.init()

HOLD_FAST_KEY_SENS = 1

def clamp(x, min, max):
	if x < min: return min
	elif x > max: return max
	else: return x

def saveFile(contents):
	files = [("Uranium File", "*.uran"), ("All Files", "*.*")]

	top = tkinter.Tk()
	top.withdraw()  # hide window
	file_name = tkinter.filedialog.asksaveasfile(parent=top, filetypes=files, defaultextension=".uran")
	top.destroy()

	if file_name is not None:
		savePath = file_name.name
		with open(savePath, "w") as f:
			for i, l in enumerate(contents):
				if i < len(contents) - 1:
					f.write(l + "\n")
				else:
					f.write(l)

def handleInput(e, isEdit, lidx, ilidx, contents):
	if isEdit:
		if e.type == pg.TEXTINPUT:
			contents[lidx] = contents[lidx][:ilidx] + e.text + contents[lidx][ilidx:]
			ilidx = clamp(ilidx + 1, 0, len(contents[lidx]))

		keys = pg.key.get_pressed()
		if keys[pg.K_BACKSPACE]:
			contents[lidx] = contents[lidx][:ilidx][:-1] + contents[lidx][ilidx:]
			ilidx = clamp(ilidx - 1, 0, len(contents[lidx]))
		elif keys[pg.K_RETURN]:
			lidx += 1
			contents.append("")
			ilidx = 0
		elif keys[pg.K_TAB]:
			contents[lidx] += " " * 4
			ilidx = clamp(ilidx + 4, 0, len(contents[lidx]))
		elif keys[pg.K_DELETE]:
			contents[lidx] = contents[lidx][:ilidx] + contents[lidx][ilidx+1:]
		elif keys[pg.K_UP] and lidx > 0:
			lidx -= 1
		elif keys[pg.K_DOWN] and lidx < len(contents):
			lidx += 1
		elif keys[pg.K_LEFT] and ilidx > 0:
			ilidx = clamp(ilidx - 1, 0, len(contents[lidx]))
		elif keys[pg.K_RIGHT] and ilidx < len(contents[lidx]):
			ilidx = clamp(ilidx + 1, 0, len(contents[lidx]))

		"""
		keys = pg.key.get_pressed()
		if keys[pg.K_BACKSPACE]:
			if keyCounts["backspace"] % (400 * HOLD_FAST_KEY_SENS) == 0:
				contents[lidx] = contents[lidx][:-1]
			pg.event.post(pg.event.Event(pg.KEYDOWN, unicode="a", key=pg.K_a, mod=pg.KMOD_NONE))
			keyCounts["backspace"] += 1
		elif keys[pg.K_RETURN]:
			if keyCounts["enter"] % (1000 * HOLD_FAST_KEY_SENS) == 0:
				lidx += 1
				contents.append("")
			pg.event.post(pg.event.Event(pg.KEYDOWN, unicode="a", key=pg.K_a, mod=pg.KMOD_NONE))
			keyCounts["enter"] += 1
		elif keys[pg.K_TAB]:
			contents[lidx] += " " * 4
		"""

	return lidx, ilidx

if __name__ == '__main__':
	win = pg.display.set_mode((800,500))
	pg.display.set_caption("Trinity Editor")
	on = True

	lines = [""]
	lineIdx = 0
	inlineIdx = 0
	textField = pg.Rect(0,  y := 50, win.get_width(), win.get_height() - y)
	pg.key.start_text_input()
	isEditting = False
	LINE_SPACING = 1.2

	fontSize = 16
	font = pg.font.SysFont("lucidaconsole", fontSize, False, False)

	while on:
		win.fill((0, 0, 0))
		#pg.draw.rect(win, (255, 0, 0), (0, textField.y + lineIdx * LINE_SPACING * fontSize, win.get_width(), fontSize))

		for ev in pg.event.get():
			if ev.type == pg.QUIT:
				pg.quit()
				on = False
				break

			if ev.type == pg.MOUSEBUTTONDOWN:
				fittingX =  textField.x < pg.mouse.get_pos()[0] <= textField.x + textField.width
				fittingY = textField.y < pg.mouse.get_pos()[1] <= textField.y + textField.height
				isEditting = fittingX and fittingY

			if ev.type == pg.KEYDOWN:
				if ev.key == pg.K_ESCAPE:
					saveFile(lines)

			lineIdx, inlineIdx = handleInput(ev, isEditting, lineIdx, inlineIdx, lines)

		if not on:
			break

		for i, line in enumerate(lines):
			text = font.render(line, True, (255, 255, 255), (0, 0, 0))
			win.blit(text, (textField.x + 10, textField.y + fontSize * LINE_SPACING * i))

			if i == lineIdx:
				widthPerChar = font.size("m")[0]
				pg.draw.rect(win, (0,255,0), (widthPerChar * (inlineIdx-1) + 10 + (10 if inlineIdx == 0 else 0), textField.y + fontSize * LINE_SPACING * i + fontSize, widthPerChar, 5))

		pg.display.update()

exit(0)