import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import seaborn as sns

sns.set(style = 'whitegrid', rc = {'axes.labelsize': 16})

### user-defined parameters    
image_width_nm = 135000 # image width in nm, get from Gwyddion or similar software
number_of_circles_want = 150 # desired (approximate) number of particles, must be less than 1990
minD_nm = 1500
maxD_nm = 10000
###

def run(f, image_width_nm, number_of_circles_want, minD_nm, maxD_nm):
    # image cropping
    img = cv2.imread(f)
    area = (0, 0, 1024, 672) # (x0, y0, x, y)
    cropped_img = img[:area[3], :area[2]]
    output = cropped_img.copy()
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

    image_width_pixels = cropped_img.shape[1] #image width in pixels, usually 1024
    nm_to_pixels_coefficient = image_width_pixels/image_width_nm    
    minR_nm = minD_nm/2
    maxR_nm = maxD_nm/2
    minR_pixels = int(minR_nm*nm_to_pixels_coefficient)
    maxR_pixels = int(maxR_nm*nm_to_pixels_coefficient)

    #initial conditions
    number_of_circles_real = 2000
    boundary = 10
    number_of_circles_difference = 10
    i = 0
    # detect circles on the image
    while abs(number_of_circles_real - number_of_circles_want) > number_of_circles_difference:
        circles = cv2.HoughCircles(gray,
            cv2.HOUGH_GRADIENT,
            0.1, #reciprocal resolution
            maxR_pixels, #min distance between particles
            #param1=0,
            param2 = boundary,
            minRadius = minR_pixels,
            maxRadius = maxR_pixels
                                   )
        if circles is not None:
            radia = circles[:,:,2]
            radia = radia.transpose()
            number_of_circles_real = len(radia)
            boundary = boundary+5*np.log(float(number_of_circles_real)/float(number_of_circles_want))
        else:
            boundary = 0.5*boundary
            radia = [1]
        if i < 10:
            i = i + 1
        else:
            number_of_circles_difference = number_of_circles_difference + 10
            i = 0
        #radia=np.array(radia)
        #radia=radia.transpose()
        #print len(radia)
        print('boundary = '+ str(boundary))
        
    print(str(number_of_circles_real)+' particles found')
    radia_nm = radia/nm_to_pixels_coefficient
    diameter_nm = radia_nm*2
    mean = np.mean(diameter_nm)
    std = np.std(diameter_nm)
    
    #histogram plotting
    fig, ax = plt.subplots(1, 1)
    ax.set_ylabel("Number of particles")
    ax.set_xlabel("Particle diameter, nm")

    diameter_nm = [float(x) for x in diameter_nm]
    upper_bound = round(max(diameter_nm)*2,-3)
    bins = np.arange(0, upper_bound, 500)
    plt.xticks(np.arange(0, upper_bound, 2000))
    
    ax.hist(diameter_nm, #bins = int(np.power(len(radia_nm),0.333)))
            bins=bins)
    ax.text(0.75, 0.6,
            'Mean diameter = '+str(int(mean))+' nm\n'
            +'Standard deviation = '+str(int(std))+' nm'+'\n'
            +'Relative std = '+str(round(100*std/mean,1))+' %',
            ha='center', va='center', transform=ax.transAxes)
    plt.savefig('hist_'+f[:-3]+'png')
    plt.close()
    
    #writing text file
    file = open('txt_'+f[:-3]+'txt',"w")
    for i in diameter_nm:
        file.write(str(i) + '\n')
    file.close()
    
    # ensure at least some circles were found
    if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
     
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(output, (x, y), r, (0, 255, 0), 1)
                    width = 1
                    cv2.rectangle(output, (x - width, y - width), (x + width, y + width), (0, 128, 255), -1)
     
    cv2.imwrite('circles_'+f[:-3]+'png',output)
    cv2.destroyAllWindows()

l = os.listdir('.')
for f in l:
    if (f[-3:] == 'tif') and (f.startswith('hist') == False) and (f.startswith('circles') == False):
        run(f, image_width_nm, number_of_circles_want, minD_nm, maxD_nm)