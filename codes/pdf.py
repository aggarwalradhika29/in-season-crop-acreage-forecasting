
# code to create a final automated report of all the relevant outputs
# import required libraries : Python 3.11.0
import os, shutil
import rasterio
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
district = str(os.getcwd()) + r'\data\shapeFiles\AOI\\district.png'

outPath = str(os.getcwd()) + r'\\report\\'
if os.path.exists(outPath):
    shutil.rmtree(outPath)
Path(outPath).mkdir(parents=True, exist_ok=True)

polar = []
for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
    polar.append(line.strip())
print("Polarization specified: ", polar)

for p in polar:
    backscatter = str(os.getcwd()) + r'\data\shapeFiles\zonal_stats\\' + str(p) + r'\\backscatterCurve' + str(p) + '.png'           # backscatter curve image
    confusion_matrix = str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + r'\\confusionMatrix.png'                  # confusion matrix image
    crDF = str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + r'\\crDF.png'                                         # classification report of ml model image
    fp = str(os.getcwd()) + r'\data\commonData\classifiedData\\classifiedImage' + str(p) + '.tif'                                   # classified image
    out = str(os.getcwd()) + r'\\report\\' + str(p)                                                                                 # output report document
    if os.path.exists(out):
        shutil.rmtree(out)
    Path(out).mkdir(parents=True, exist_ok=True)

    # Open the TIF file using rasterio
    with rasterio.open(fp) as src:
        raster = src.read(1)

    # Apply a colormap to the raster data
    cmap = plt.get_cmap('inferno')
    raster_rgb = cmap(raster / raster.max())[:, :, :3] * 255
    raster_rgb = raster_rgb.astype('uint8')

    # Plot the image using matplotlib
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(raster_rgb)

    # Remove the axes and save the image as PNG
    ax.axis('off')
    figure_size = plt.gcf().get_size_inches()
    factor = 0.55
    plt.gcf().set_size_inches(factor * figure_size)
    plt.savefig(str(os.getcwd()) + r'\data\commonData\classifiedData\\classImg' + str(p) + '.png', bbox_inches='tight', pad_inches=0, dpi=300)
    
    classifiedImage = str(os.getcwd()) + r'\data\commonData\classifiedData\\classImg' + str(p) + '.png'

    # PAGE 1
    image1 = Image.open(str(os.getcwd()) + r'\\photos\\1.png')
    element11 = Image.open(district)
    width1, height1 = image1.size
    print(width1)
    print(height1)
    # Paste image2 onto image1 at a specified location
    x = 70  # The x-coordinate of the top-left corner of image2 in image1
    y = 610  # The y-coordinate of the top-left corner of image2 in image1
    image1.paste(element11, (x, y))

    # Save the resulting image
    image1.save(out + r'\\page1.png')
    # --------------------------------------------------------------------------

    image2 = Image.open(str(os.getcwd()) + r'\\photos\\2.png')
    element21 = Image.open(backscatter)
    # Resize image2 to fit within image1
    width1, height1 = image2.size
    print(width1)
    print(height1)
    # Paste image2 onto image1 at a specified location
    x = 55  # The x-coordinate of the top-left corner of image2 in image1
    y = 210  # The y-coordinate of the top-left corner of image2 in image1
    image2.paste(element21, (x, y))

    element22 = Image.open(classifiedImage)
    z = 70
    q = 1100
    image2.paste(element22, (z, q))
    # Save the resulting image
    image2.save(out + r'\\page2.png')
    # --------------------------------------------------------------------------

    image3 = Image.open(str(os.getcwd()) + r'\\photos\\3.png')
    element31 = Image.open(crDF)
    
    # Resize image2 to fit within image1
    width1, height1 = image3.size
    print(width1)
    print(height1)
    x = 230  # The x-coordinate of the top-left corner of image2 in image1
    y = 980  # The y-coordinate of the top-left corner of image2 in image1
    image3.paste(element31, (x, y))

    polar = 0
    for line in open(str(os.getcwd()) + r'\data\commonData\\accuracy' + str(p) + '.txt','r').readlines():
        polar = (line.strip())
    polar = polar[:6]
    myFont = ImageFont.truetype(str(os.getcwd()) + r'\\photos\\Raleway-Black.ttf', 36)
    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(image3)

    # Add Text to an image
    I1.text((845, 1775), polar, font=myFont, fill=(0, 0, 0))
    image3.save(out + r'\\page3.png')
    # --------------------------------------------------------------------------

    image4 = Image.open(str(os.getcwd()) + r'\\photos\\4.png')
    element41 = Image.open(confusion_matrix)
    # Resize image2 to fit within image1
    width1, height1 = image4.size
    print(width1)
    print(height1)
    # Paste image2 onto image1 at a specified location
    x = 10  # The x-coordinate of the top-left corner of image2 in image1
    y = 280  # The y-coordinate of the top-left corner of image2 in image1
    image4.paste(element41, (x, y))
    image4.save(out + r'\\page4.png')
    # --------------------------------------------------------------------------

    page1 = Image.open(out + r'\\page1.png')
    page2 = Image.open(out + r'\\page2.png')
    page3 = Image.open(out + r'\\page3.png')
    page4 = Image.open(out + r'\\page4.png')


    im_1 = page1.convert('RGB')
    im_2 = page2.convert('RGB')
    im_3 = page3.convert('RGB')
    im_4 = page4.convert('RGB')

    image_list = [im_2, im_3, im_4]
    # PDF CREATION
    im_1.save(out + r'\\classificationReport.pdf', save_all=True, append_images=image_list)
    print('Report has been created!')