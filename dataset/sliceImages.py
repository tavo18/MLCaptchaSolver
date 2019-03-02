from PIL import Image
from io import BytesIO

im = Image.open("/home/tavo/MEGA/ProyectoBOT/dataset/ejemplos/0.png")
ancho, alto = im.size
letra1 = im.crop(((ancho/5), 0, (ancho/5)*2, alto))
letra2 = im.crop(((ancho/5)*2, 0, (ancho/5)*3, alto))
letra3 = im.crop(((ancho/5)*3, 0, (ancho/5)*4, alto))
letra4 = im.crop(((ancho/5)*4, 0, 100, alto))
letra1.show()
letra2.show()
letra3.show()
letra4.show()
# sub_image = full_image[y_start: y_end, x_start:x_end]