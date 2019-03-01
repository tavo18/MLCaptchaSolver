import matplotlib.pyplot as plt
category=[]
plt.ion()

for i,image in enumerate(allImages):
    plt.imshow(image)
    plt.pause(0.05)
    category.append(raw_input('category: '))