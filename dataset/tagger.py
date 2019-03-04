from tkinter import *
from PIL import ImageTk, Image
from io import BytesIO
import matplotlib.pyplot as plt 
import os, os.path



#Returns a list of cropped images (one slice per letter)
def cutImage(img):
	cImg = []
	width,height = img.size
	cImg.append(img.crop(((width/5), 0, (width/5)*2, height)))
	# letra1.save("/home/tavo/MEGA/ProyectoBOT/dataset/ejemplos/"+str(i)+".png", "PNG")
	cImg.append(img.crop(((width/5)*2, 0, (width/5)*3, height)))
	cImg.append(img.crop(((width/5)*3, 0, (width/5)*4, height)))
	cImg.append(img.crop(((width/5)*4, 0, 100, height)))
	

	return cImg
	# letra2.show()
	# letra3.show()
	# letra4.show()

def func(event):
	print(txt.get())
	txt.delete(0, 'end')
	txt.focus()
	imtk = ImageTk.PhotoImage(imgs[4])
	lbl2 =  Label(window, image=imtk)
	lbl2.grid(column=0, row=0)
	# i+=1

def saveLetter(img,loc,name):
	img.save("/home/tavo/MEGA/ProyectoBOT/MLCaptchaSolver/dataset/examples/"+loc+"/"+str(name)+".png", "PNG")





imgs = []
letters = []
counter = {'a': 17,'b': 14,'c': 14,'d': 16,'e': 23,'f': 19,'g': 16,'h': 22,'i': 19,'j': 13,'k': 9,'l': 23,'m': 13,'n': 17,'o': 17,'p': 12,'q': 16,'r': 13,'s': 11,'t': 18,'u': 7,'v': 13,'w': 18,'x': 7,'y': 18,'z': 15,'0': 18,'1': 13,'2': 14,'3': 10,'4': 15,'5': 12,'6': 20,'7': 9,'8': 11,'9': 17}

contador = 0
for c in counter:
	counter[c] = len([name for name in os.listdir("/home/tavo/MEGA/ProyectoBOT/MLCaptchaSolver/dataset/examples/"+c) if os.path.isfile(os.path.join("/home/tavo/MEGA/ProyectoBOT/MLCaptchaSolver/dataset/examples/"+c, name))])
	# contador += len([name for name in os.listdir("/home/tavo/MEGA/ProyectoBOT/MLCaptchaSolver/dataset/examples/"+c) if os.path.isfile(os.path.join("/home/tavo/MEGA/ProyectoBOT/MLCaptchaSolver/dataset/examples/"+c, name))])
	# print(c+": ")
	# print(counter[c])
print (contador)

# Initialize the list of captchas and the list of letters of each captcha
# to make the classification
for i in range(999):
	imgs.append(Image.open("/home/tavo/MEGA/ProyectoBOT/dataset/ejemplos2/"+str(i+1)+".png"))
	for l in (cutImage(Image.open("/home/tavo/MEGA/ProyectoBOT/dataset/ejemplos2/"+str(i+1)+".png"))):
		letters.append(l)


print(len(letters))

root = Tk()

img = ImageTk.PhotoImage(letters[0])
panel = Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")
E1 = Entry(root, bd = 2) 
E1.focus()
E1.pack(side=BOTTOM, fill=BOTH, expand=YES)

i=1
def callback(e):
	if (E1.get()!='a' and E1.get()!='b' and E1.get()!='c' and E1.get()!='d' and E1.get()!='e' and E1.get()!='f' and E1.get()!='g' and E1.get()!='h' and E1.get()!='i' and E1.get()!='j' and E1.get()!='k' and E1.get()!='l' and E1.get()!='m' and E1.get()!='n' and E1.get()!='o' and E1.get()!='p' and E1.get()!='q' and E1.get()!='r' and E1.get()!='s' and E1.get()!='t' and E1.get()!='u' and E1.get()!='v' and E1.get()!='w' and E1.get()!='x' and E1.get()!='y' and E1.get()!='z' and E1.get()!='0' and E1.get()!='1' and E1.get()!='2' and E1.get()!='3' and E1.get()!='4' and E1.get()!='5' and E1.get()!='6' and E1.get()!='7' and E1.get()!='8' and E1.get()!='9'):
		E1.focus()
		E1.delete(0,'end')
	else:
		global i
		#E1.get() -an image letter- goes to his particular dir
		saveLetter(letters[i-1],E1.get(),counter[E1.get()])
		counter[E1.get()] = counter[E1.get()]+1
		# print(E1.get())
		print("Letra "+str(i)+" "+str(len(letters)))
		img2 = ImageTk.PhotoImage(letters[i])
		panel.configure(image=img2)
		panel.image = img2
		i+=1
		E1.focus()
		E1.delete(0,'end')	 

root.bind("<Return>", callback)
root.mainloop()

