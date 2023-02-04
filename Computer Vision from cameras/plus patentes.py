img = cv2.imread("/path/to/your_image")

width=0 
height=0

start_x=0 
start_y=0
end_x=0 
end_y=0

output = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gw, gs, gw1, gs1, gw2, gs2 = (3,1.0,7,3.0, 3, 2.0)

img_blur = cv2.GaussianBlur(gray, (gw, gw), gs)
g1 = cv2.GaussianBlur(img_blur, (gw1, gw1), gs1)
g2 = cv2.GaussianBlur(img_blur, (gw2, gw2), gs2)
ret, thg = cv2.threshold(g2-g1, 127, 255, cv2.THRESH_BINARY)

contours, hier = cv2.findContours(thg, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

img_cpy = img.copy()

width=0 
height=0

start_x=0 
start_y=0
end_x=0 
end_y=0

for i in range(len(contours)):
    
    if hier[0][i][2] == -1:
        continue
        
    x ,y, w, h = cv2.boundingRect(contours[i])
    a=w*h    
    aspectRatio = float(w)/h
    if  aspectRatio >= 2.5 and a>600:          
        approx = cv2.approxPolyDP(contours[i], 0.05* cv2.arcLength(contours[i], True), True)
        if len(approx) == 4 and x>15  :
            width=w
            height=h   
            start_x=x
            start_y=y
            end_x=start_x+width
            end_y=start_y+height      
            cv2.rectangle(img_cpy, (start_x,start_y), (end_x,end_y), (0,0,255),3)
            cv2.putText(img_cpy, "rectangle "+str(x)+" , " +str(y-5), (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
          
plt.imshow(img_cpy)

print("start",start_x,start_y)
print("end", end_x,end_y)