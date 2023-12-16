import cv2

# Load the input image
image = cv2.imread('colour.jpeg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,27,25,0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_TC89_L1)
print(type(contours)) #type list

c = max(contours, key=cv2.contourArea) #max contour
f = open('path.svg', 'w+')
f.write('<svg width="'+str(100)+'" height="'+str(100)+'" xmlns="http://www.w3.org/2000/svg">')
f.write('<path d="M')

for i in range(len(c)):
    #print(c[i][0])
    x, y = c[i][0]
    # print(x)
    f.write(str(x)+  ' ' + str(y)+' ')

f.write('"/>')
f.write('</svg>')
f.close()



