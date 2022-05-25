#!/usr/bin/sh
#-*-coding:utf-8 -*-

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
import pyautogui
from datetime import *
from tkinter import *
from tkinter import messagebox
import googletrans
from PIL import ImageGrab
from functools import partial
import os
import mouse
import time
#import clipboard

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

def btncmd():
    print("btncmd started")
    while 1:
        btn1['state'] = DISABLED
        time.sleep(0.01)
        
        dir = os.path.join(os.path.expanduser('~'),'Desktop')
        
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        
        while True:
            if mouse.is_pressed("left"):
                x1, y1 = mouse.get_position()
                print(x1,y1)
                time.sleep(0.1)
                
                while True:
                    if mouse.is_pressed("left"):
                        x2, y2 = mouse.get_position()
                        if x1 == x2:
                            x2 += 1
                        if y1 == y2:
                            y2 += 1
                        print(x2,y2)
                        break
                break
        
        if x1 > x2:
            x = x2
            dx = x1-x2
        else:
            x = x1
            dx = x2 - x1
            
        if y1 > y2:
            y = y2
            dy = y1 - y2
        else:
            y = y1
            dy = y2 - y1
        
        im = pyautogui.screenshot(region=(x,y,dx,dy))
        
        language = textBox.get(1.0, 'end-1c')
        
        if language == "":
            print("lang = x")
            text = pytesseract.image_to_string(im)
        else:
            print("lang = {}".format(language))
            try:
                text = pytesseract.image_to_string(im, lang = language)
            except pytesseract.pytesseract.TesseractError:
                messagebox.showerror("warning", "Failed loading language \'{}\'".format(language))
                btn1['state'] = NORMAL
                break
                
        
        #clipboard.copy(text) #test
        
        if text == "\u000c": #U+000c
            messagebox.showerror("warning", "No characters detected\nerror-1")
            btn1['state'] = NORMAL
            break
        
        print("text = " + text)
        
        translator = googletrans.Translator()
        try:
            tText = translator.translate(text, dest = 'ko')
        except IndexError:
            print("googletranse error")
            print("\n"*3)
            messagebox.showerror("warning", "No charactrs detected\nerror-2")
            btn1['state'] = NORMAL
            break
        
        resultText = tText.text
        
        now = datetime.now()
        nowTime = now.strftime("%Y_%m_%d-%H%M%S")
        fileName = dir + "\\" + "translated_text-" + nowTime
        
        if saveImage.get() == 1:
            print("save image")
            im.save("{0}\\image-{1}.png".format(dir, nowTime))
            #im.show()
        
        
        memo = open("%s.txt" %fileName, "w", encoding = "utf-8")
        memo.write("%s" %resultText)
        memo.close()
        messagebox.showinfo("complete", "complete")
        btn1['state'] = NORMAL
        print("finish")
        break


 
screen = Tk()
screen.title("Translator")
xs, ys = pyautogui.size()
if (xs < 301) or (ys < 301):
    screen.geometry("300x300+0+0")
else:
    temp = "300x300+{0}+{1}".format(int((xs/2)-150),int((ys/2)-150))
    screen.geometry(temp)
#screen.attributes('-alpha', 0)
screen.resizable(True,True)


label1=Label(screen, text='버튼을 누르고 번역할 범위를\n마우스로 클릭해 주세요.')
label1.pack()
textBox = Text(screen, height=1)
textBox.pack()
#listbox = Listbox(screen, selectmode = "extend", height = 1)
#listbox.insert(0, "eng")
#listbox.pack()
saveImage = IntVar()
cBox = Checkbutton(screen, text = "Save image", variable = saveImage)
cBox.pack()
btn1 = Button(screen, text='번역 시작', command=btncmd)
btn2 = Button(screen, text = '')
btn1.pack()
 
screen.mainloop()