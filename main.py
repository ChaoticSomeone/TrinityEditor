"""
@ToDo: Fix ssaving files after opening a file
"""


import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import tkinter
import tkinter.filedialog
from sys import exit
from time import time
from UI import Button
pg.init()

HOLD_FAST_KEY_SENS = 1

tkWin = tkinter.Tk()
tkWin.withdraw()

def clamp(x, min, max):
	if x < min: return min
	elif x > max: return max
	else: return x

def saveFile(tk, contents):
	files = [("Uranium File", "*.uran"), ("All Files", "*.*")]

	file_name = tkinter.filedialog.asksaveasfile(parent=tk, filetypes=files, defaultextension=".uran")
	print(contents)
	if file_name is not None:
		savePath = file_name.name
		with open(savePath, "w") as f:
			for idx, l in enumerate(contents):
				if idx < len(contents) - 1:
					f.write(l + "\n")
				else:
					f.write(l)

def openFile(tk, contents):
	files = [("Uranium File", "*.uran"), ("All Files", "*.*")]

	file = tkinter.filedialog.askopenfile(mode="r", parent=tk, filetypes=files, defaultextension=".uran")
	if file is not None:
		return file.readlines()
	else:
		return contents


def handleInput(e, isEdit, lidx, ilidx, contents):
	if isEdit:
		if e.type == pg.TEXTINPUT:
			contents[lidx] = contents[lidx][:ilidx] + e.text + contents[lidx][ilidx:]
			ilidx = clamp(ilidx + 1, 0, len(contents[lidx]))

		if e.type == pg.KEYDOWN:
			if e.key == pg.K_BACKSPACE:
				contents[lidx] = contents[lidx][:ilidx][:-1] + contents[lidx][ilidx:]
				ilidx = clamp(ilidx - 1, 0, len(contents[lidx]))
			elif e.key == pg.K_RETURN:
				lidx += 1
				contents.append("")
				ilidx = 0
			elif e.key == pg.K_TAB:
				contents[lidx] += " " * 4
				ilidx = clamp(ilidx + 4, 0, len(contents[lidx]))
			elif e.key == pg.K_DELETE:
				contents[lidx] = contents[lidx][:ilidx] + contents[lidx][ilidx + 1:]
			elif e.key == pg.K_UP and lidx > 0:
				lidx -= 1
			elif e.key == pg.K_DOWN and lidx < len(contents):
				lidx += 1
			elif e.key == pg.K_LEFT and ilidx > 0:
				ilidx = clamp(ilidx - 1, 0, len(contents[lidx]))
			elif e.key == pg.K_RIGHT and ilidx < len(contents[lidx]):
				ilidx = clamp(ilidx + 1, 0, len(contents[lidx]))

	return lidx, ilidx

if __name__ == '__main__':
	frames = 0
	fps = 0
	clock = pg.time.Clock()

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
	textYOffset = 0

	fontSize = 16
	font = pg.font.SysFont("lucidaconsole", fontSize, False, False)
	widthPerChar = font.size("m")[0]
	maxLines = win.get_height() // fontSize

	widthPerButton = win.get_width() // 6 - 2
	menuFont = pg.font.SysFont("lucidaconsole", 20, False, False)
	topMenuButtons = [
		Button("save", pg.Rect(2, 2, widthPerButton, 40), (255, 255, 255), (50, 50, 50), menuFont, "Save", saveFile, (tkWin, lines)),
		Button("load", pg.Rect(widthPerButton + 4, 2, widthPerButton, 40), (255, 255, 255), (50, 50, 50), menuFont, "Open", openFile, (tkWin, lines))
	]

	while on:
		win.fill((0, 0, 0))

		pg.draw.rect(win, (30, 30, 30), (0, 0, win.get_width(), 45))

		for button in topMenuButtons:
			button.render(win)

		pg.draw.rect(win, (50, 50, 50), ((widthPerButton + 2) * 2 + 2, 2, widthPerButton, 40))
		pg.draw.rect(win, (50, 50, 50), ((widthPerButton + 2) * 3 + 2, 2, widthPerButton, 40))
		pg.draw.rect(win, (50, 50, 50), ((widthPerButton + 2) * 4 + 2, 2, widthPerButton, 40))
		pg.draw.rect(win, (50, 50, 50), ((widthPerButton + 2) * 5 + 2, 2, widthPerButton, 40))

		fpsText = font.render(f"{fps:.0f} FPS", True, (255, 255, 255), (50, 50, 50))
		win.blit(fpsText, ((widthPerButton + 2) * 5 + 25, 13))

		for ev in pg.event.get():

			if ev.type == pg.QUIT:
				pg.quit()
				on = False
				break


			if ev.type == pg.MOUSEBUTTONDOWN:
				fittingX =  textField.x < pg.mouse.get_pos()[0] <= textField.x + textField.width
				fittingY = textField.y < pg.mouse.get_pos()[1] <= textField.y + textField.height
				isEditting = fittingX and fittingY

				for i, button in enumerate(topMenuButtons):
					result = button.update()
					if result is not None:
						print(result)
						buttonName = result[0]
						returnValues = result[1]
						if buttonName == "load" and returnValues is not None:
							lines = returnValues.copy()
							lineIdx = 0
							inlineIdx = 0
							isEditting = True
			lineIdx, inlineIdx = handleInput(ev, isEditting, lineIdx, inlineIdx, lines)

		if not on:
			break

		for i, line in enumerate(lines):
			text = font.render(line, True, (255, 255, 255), (0, 0, 0))
			win.blit(text, (textField.x + 10, textField.y + fontSize * LINE_SPACING * i))

			if i == lineIdx:
				cursorXOffset = inlineIdx - (1 if inlineIdx == 0 else 0)
				cursorX = widthPerChar * cursorXOffset + 10 + (10 if inlineIdx == 0 else 0)
				pg.draw.rect(win, (0,255,0), (cursorX, textField.y + fontSize * LINE_SPACING * i + fontSize + textYOffset, widthPerChar, 5))



		pg.display.update()
		clock.tick()
		frames += 1
		if frames % 500 == 0:
			fps = clock.get_fps()
exit(0)