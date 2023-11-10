import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import tkinter
import tkinter.filedialog
from sys import exit
pg.init()

HOLD_FAST_KEY_SENS = 1
fastKeysCount = {
	"backspace": 0,
	"enter": 0
}

def saveFile(contents):
	files = [("Uranium File", "*.uran"), ("All Files", "*.*")]

	top = tkinter.Tk()
	top.withdraw()  # hide window
	file_name = tkinter.filedialog.asksaveasfile(parent=top, filetypes=files, defaultextension=".uran")
	top.destroy()

	savePath = file_name.name
	with open(savePath, "w") as f:
		for i, l in enumerate(contents):
			if i < len(contents) - 1:
				f.write(l + "\n")
			else:
				f.write(l)

def handleInput(e, isEdit, lidx, keyCounts, contents):
	if isEdit:
		if e.type == pg.TEXTINPUT:
			contents[lidx] += e.text

		keys = pg.key.get_pressed()
		if keys[pg.K_BACKSPACE]:
			contents[lidx] = contents[lidx][:-1]
		elif keys[pg.K_RETURN]:
			lidx += 1
			contents.append("")
		elif keys[pg.K_TAB]:
			contents[lidx] += " " * 4

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

	return lidx

if __name__ == '__main__':
	win = pg.display.set_mode((800,500))
	pg.display.set_caption("Trinity Editor")
	on = True

	lines = [""]
	lineIdx = 0
	textField = pg.Rect(0,  y := 50, win.get_width(), win.get_height() - y)
	pg.key.start_text_input()
	isEditting = False

	fontSize = 20
	font = pg.font.SysFont("Calibri", fontSize, False, False)

	while on:
		win.fill((0, 0, 0))
		pg.draw.rect(win, (255, 0, 0), (0, textField.y + lineIdx * 1.2 * fontSize, win.get_width(), fontSize))

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

			lineIdx = handleInput(ev, isEditting, lineIdx, fastKeysCount, lines)

		if not on:
			break

		for i, line in enumerate(lines):
			text = font.render(line, True, (255, 255, 255), (0, 0, 0))
			# tRect = text.get_rect()
			win.blit(text, (textField.x + 10, textField.y + fontSize * 1.2 * i))

		pg.display.update()

exit(0)