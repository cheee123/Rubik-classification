#Some helper functions 
import numpy as np
import cv2
color = [(230,224,208),(180,92,20),(37,27,158),(17,190,192),(13,153,27),(21,91,200),(85,85,85)]
# BGR white,blue,red,yellow,green,orange,gray
def draw_rubik(color_p,front=True):
  assert len(color_p)==24,"draw_rubik() error: Number of colors is wrong, expected 24"
  def color_true(position):
    return color[color_p[position]]
  img = np.zeros((512,512,3),np.uint8)
  img.fill(239)
  quadrilaterals = []
  #3 big quads
  pts = np.array([[238,63], [96,134], [295,217], [411,114]]).reshape((-1,1,2))
  quadrilaterals.append(pts)
  pts = np.array([[96,134], [114,303], [284,405], [295,217]]).reshape((-1,1,2))
  quadrilaterals.append(pts)
  pts = np.array([[295,217], [284,405], [392,288], [411,114]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  #Blocks color for filling, UP face
  pts = np.array([[238,63], [291,80], [252,104], [197,84]]).reshape((-1,1,2))
  quadrilaterals.append(pts) 

  pts = np.array([[197,84], [252,104], [208,130], [150,110]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[291,80], [352,99], [312,126], [252,104]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[150,110], [208,130], [159,160], [96,134]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[252,104], [312,126], [270,155], [208,130]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[352,99], [411,114], [374,146], [312,126]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[208,130], [270,155], [224,189], [159,160]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[312,126], [374,146], [335,180], [270,155]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[270,155], [335,180], [295,217], [224,189]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  #Layer 1 color
  pts = np.array([[96,134], [159,160], [162,227], [105,201]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[159,160], [224,189], [222,255], [162,227]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[224,189], [295,217], [289,286], [222,255]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[295,217], [335,180], [330,246], [289,286]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[335,180], [374,146], [368,207], [330,246]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[374,146], [411,114], [403,175], [368,207]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  #Layer 2 color
  pts = np.array([[105,201], [162,227], [166,285], [111,257]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[162,227], [222,255], [223,316], [166,285]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[222,255], [289,286], [286,348], [223,316]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[289,286], [330,246], [326,307], [286,348]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[330,246], [368,207], [362,268], [326,307]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[368,207], [403,175], [397,232], [362,268]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  #Layer 3 color
  pts = np.array([[111,257], [166,285], [165,333], [114,303]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[166,285], [223,316], [224,367], [165,333]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[223,316], [286,348], [284,405], [224,367]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[286,348], [326,307], [320,366], [284,405]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[326,307], [362,268], [359,321], [320,366]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  pts = np.array([[362,268], [397,232], [392,288], [359,321]]).reshape((-1,1,2))
  quadrilaterals.append(pts)

  #Fill color:
  position = 0
  for i in range (3,7):
    img = cv2.fillPoly(img, [quadrilaterals[i]], color_true(position))
    position += 1
  for i in range (8,19):
    img = cv2.fillPoly(img, [quadrilaterals[i]], color_true(position))
    position += 1
  for i in range (20,22):
    img = cv2.fillPoly(img, [quadrilaterals[i]], color_true(position))
    position += 1
  for i in range (23,len(quadrilaterals)):
    img = cv2.fillPoly(img, [quadrilaterals[i]], color_true(position))
    position += 1

  #Center color
  if(front):
    img = cv2.fillPoly(img, [quadrilaterals[7]], color[0])
    img = cv2.fillPoly(img, [quadrilaterals[19]], color[2])
    img = cv2.fillPoly(img, [quadrilaterals[22]], color[1])
  else:
    img = cv2.fillPoly(img, [quadrilaterals[7]], color[3])
    img = cv2.fillPoly(img, [quadrilaterals[19]], color[4])
    img = cv2.fillPoly(img, [quadrilaterals[22]], color[5])

  #Draw frames and lines
  img = cv2.polylines(img, quadrilaterals[0:3], True, (0,0,0), 4, cv2.LINE_AA)
  cv2.line(img,(197,84),(374,146),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(150,110),(335,180),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(291,80),(159,160),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(224,189),(352,99),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(374,146),(359,321),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(335,180),(320,366),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(159,160),(165,333),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(224,189),(224,367),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(105,201),(289,286),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(111,257),(286,348),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(289,286),(403,175),(0,0,0),4,cv2.LINE_AA)
  cv2.line(img,(286,348),(397,232),(0,0,0),4,cv2.LINE_AA)

  return img

#Arrow for instruction
def draw_arrow(img, move):
  color_a = (237,60,225) #arrow color
  if(move=='U'):
    cv2.arrowedLine(img,(255,238),(128,181),color_a,5,cv2.LINE_AA,tipLength=0.2)
  elif(move=='U\''):
    cv2.arrowedLine(img,(128,181),(255,238),color_a,5,cv2.LINE_AA,tipLength=0.2)
  elif(move=='U2'):
    cv2.line(img,(389,160),(292,248),color_a,5,cv2.LINE_AA)
    cv2.arrowedLine(img,(292,248),(128,181),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='L'):
    cv2.arrowedLine(img,(128,181),(130,305),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='L\''):
    cv2.arrowedLine(img,(130,305),(128,181),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='L2'):
    cv2.line(img,(246,84),(129,149),color_a,5,cv2.LINE_AA)
    cv2.arrowedLine(img,(129,149),(138,305),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='F'):
    cv2.arrowedLine(img,(314,236),(307,368),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='F\''):
    cv2.arrowedLine(img,(280,188),(151,136),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='F2'):
    cv2.line(img,(302,368),(314,200),color_a,5,cv2.LINE_AA)
    cv2.arrowedLine(img,(314,200),(151,136),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='R'):
    cv2.arrowedLine(img,(252,370),(259,229),color_a,5,cv2.LINE_AA,tipLength=0.2)
  elif(move=='R\''):
    cv2.arrowedLine(img,(259,229),(252,370),color_a,5,cv2.LINE_AA,tipLength=0.2)
  elif(move=='R2'):
    cv2.line(img,(252,370),(260,205),color_a,5,cv2.LINE_AA)
    cv2.arrowedLine(img,(260,205),(368,120),color_a,5,cv2.LINE_AA,tipLength=0.2)
  elif(move=='B'):
    cv2.arrowedLine(img,(366,127),(244,85),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='B\''):
    cv2.arrowedLine(img,(244,85),(366,127),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='B2'):
    cv2.line(img,(244,85),(392,132),color_a,5,cv2.LINE_AA)
    cv2.arrowedLine(img,(392,132),(379,283),color_a,5,cv2.LINE_AA,tipLength=0.1)
  elif(move=='D'):
    cv2.arrowedLine(img,(138,295),(255,364),color_a,5,cv2.LINE_AA,tipLength=0.2)
  elif(move=='D\''):
    cv2.arrowedLine(img,(255,364),(138,300),color_a,5,cv2.LINE_AA,tipLength=0.15)
  elif(move=='D2'):
    cv2.line(img,(138,295),(285,374),color_a,5,cv2.LINE_AA)
    cv2.arrowedLine(img,(285,374),(378,280),color_a,5,cv2.LINE_AA,tipLength=0.1)
  else:
    assert False,"draw_arrow() error: Wrong move!"
  return img

#Give current state of rubik and return next state according to 'Move' c
def nextview(cur_front, cur_back, c):
  next_front = np.copy(cur_front)
  next_back = np.copy(cur_back)
  if(c=='U'):
    next_back[0]=cur_back[3]
    next_back[1]=cur_back[5]
    next_back[2]=cur_back[1]
    next_back[3]=cur_back[7]
    next_back[4]=cur_back[0]
    next_back[5]=cur_back[6]
    next_back[6]=cur_back[2]
    next_back[7]=cur_back[4]
    
    next_back[8]=cur_back[11]
    next_back[9]=cur_back[12]
    next_back[10]=cur_back[13]
    
    next_back[11]=cur_front[23]
    next_back[12]=cur_front[22]
    next_back[13]=cur_front[21]

    next_front[23]=cur_front[20]
    next_front[22]=cur_front[19]
    next_front[21]=cur_front[18]

    next_front[20]=cur_back[8]
    next_front[19]=cur_back[9]
    next_front[18]=cur_back[10]
  elif(c=='U\''):
    next_back[0]=cur_back[4]
    next_back[1]=cur_back[2]
    next_back[2]=cur_back[6]
    next_back[3]=cur_back[0]
    next_back[4]=cur_back[7]
    next_back[5]=cur_back[1]
    next_back[6]=cur_back[5]
    next_back[7]=cur_back[3]
    
    next_back[8]=cur_front[20]
    next_back[9]=cur_front[19]
    next_back[10]=cur_front[18]
    
    next_back[11]=cur_back[8]
    next_back[12]=cur_back[9]
    next_back[13]=cur_back[10]

    next_front[23]=cur_back[11]
    next_front[22]=cur_back[12]
    next_front[21]=cur_back[13]

    next_front[20]=cur_front[23]
    next_front[19]=cur_front[22]
    next_front[18]=cur_front[21]
  elif(c=='U2'):
    next_back[0]=cur_back[7]
    next_back[1]=cur_back[6]
    next_back[2]=cur_back[5]
    next_back[3]=cur_back[4]
    next_back[4]=cur_back[3]
    next_back[5]=cur_back[2]
    next_back[6]=cur_back[1]
    next_back[7]=cur_back[0]

    next_back[8]=cur_front[23]
    next_back[9]=cur_front[22]
    next_back[10]=cur_front[21]

    next_back[11]=cur_front[20]
    next_back[12]=cur_front[19]
    next_back[13]=cur_front[18]

    next_front[23]=cur_back[8]
    next_front[22]=cur_back[9]
    next_front[21]=cur_back[10]

    next_front[20]=cur_back[11]
    next_front[19]=cur_back[12]
    next_front[18]=cur_back[13]
  elif(c=='L'):
    next_front[8]=cur_front[18]
    next_front[9]=cur_front[14]
    next_front[10]=cur_front[8]
    next_front[14]=cur_front[19]
    next_front[15]=cur_front[9]
    next_front[18]=cur_front[20]
    next_front[19]=cur_front[15]
    next_front[20]=cur_front[10]

    next_back[8]=cur_back[0]
    next_back[14]=cur_back[1]
    next_back[18]=cur_back[3]

    next_back[0]=cur_front[11]
    next_back[1]=cur_front[16]
    next_back[3]=cur_front[21]

    next_front[11]=cur_front[3]
    next_front[16]=cur_front[5]
    next_front[21]=cur_front[7]

    next_front[3]=cur_back[8]
    next_front[5]=cur_back[14]
    next_front[7]=cur_back[18]
  elif(c=='L\''):
    next_front[8]=cur_front[10]
    next_front[9]=cur_front[15]
    next_front[10]=cur_front[20]
    next_front[14]=cur_front[9]
    next_front[15]=cur_front[19]
    next_front[18]=cur_front[8]
    next_front[19]=cur_front[14]
    next_front[20]=cur_front[18]

    next_back[8]=cur_front[3]
    next_back[14]=cur_front[5]
    next_back[18]=cur_front[7]

    next_back[0]=cur_back[8]
    next_back[1]=cur_back[14]
    next_back[3]=cur_back[18]

    next_front[11]=cur_back[0]
    next_front[16]=cur_back[1]
    next_front[21]=cur_back[3]

    next_front[3]=cur_front[11]
    next_front[5]=cur_front[16]
    next_front[7]=cur_front[21]
  elif(c=='L2'):
    next_front[8]=cur_front[20]
    next_front[9]=cur_front[19]
    next_front[10]=cur_front[18]
    next_front[14]=cur_front[15]
    next_front[15]=cur_front[14]
    next_front[18]=cur_front[10]
    next_front[19]=cur_front[9]
    next_front[20]=cur_front[8]

    next_back[8]=cur_front[11]
    next_back[14]=cur_front[16]
    next_back[18]=cur_front[21]

    next_back[0]=cur_front[3]
    next_back[1]=cur_front[5]
    next_back[3]=cur_front[7]

    next_front[11]=cur_back[8]
    next_front[16]=cur_back[14]
    next_front[21]=cur_back[18]

    next_front[3]=cur_back[0]
    next_front[5]=cur_back[1]
    next_front[7]=cur_back[3]
  elif(c=='F'):
    next_back[8]=cur_back[18]
    next_back[9]=cur_back[14]
    next_back[10]=cur_back[8]
    next_back[14]=cur_back[19]
    next_back[15]=cur_back[9]
    next_back[18]=cur_back[20]
    next_back[19]=cur_back[15]
    next_back[20]=cur_back[10]

    next_back[3]=cur_front[8]
    next_back[5]=cur_front[14]
    next_back[7]=cur_front[18]

    next_front[8]=cur_front[0]
    next_front[14]=cur_front[1]
    next_front[18]=cur_front[3]

    next_front[0]=cur_back[11]
    next_front[1]=cur_back[16]
    next_front[3]=cur_back[21]

    next_back[11]=cur_back[3]
    next_back[16]=cur_back[5]
    next_back[21]=cur_back[7]
  elif(c=='F\''):
    next_back[8]=cur_back[10]
    next_back[9]=cur_back[15]
    next_back[10]=cur_back[20]
    next_back[14]=cur_back[9]
    next_back[15]=cur_back[19]
    next_back[18]=cur_back[8]
    next_back[19]=cur_back[14]
    next_back[20]=cur_back[18]

    next_back[3]=cur_back[11]
    next_back[5]=cur_back[16]
    next_back[7]=cur_back[21]

    next_front[8]=cur_back[3]
    next_front[14]=cur_back[5]
    next_front[18]=cur_back[7]

    next_front[0]=cur_front[8]
    next_front[1]=cur_front[14]
    next_front[3]=cur_front[18]

    next_back[11]=cur_front[0]
    next_back[16]=cur_front[1]
    next_back[21]=cur_front[3]
  elif(c=='F2'):
    next_back[8]=cur_back[20]
    next_back[9]=cur_back[19]
    next_back[10]=cur_back[18]
    next_back[14]=cur_back[15]
    next_back[15]=cur_back[14]
    next_back[18]=cur_back[10]
    next_back[19]=cur_back[9]
    next_back[20]=cur_back[8]

    next_back[3]=cur_front[0]
    next_back[5]=cur_front[1]
    next_back[7]=cur_front[3]

    next_front[8]=cur_back[11]
    next_front[14]=cur_back[16]
    next_front[18]=cur_back[21]

    next_front[0]=cur_back[3]
    next_front[1]=cur_back[5]
    next_front[3]=cur_back[7]

    next_back[11]=cur_front[8]
    next_back[16]=cur_front[14]
    next_back[21]=cur_front[18]
  elif(c=='R'):
    next_back[11]=cur_back[21]
    next_back[12]=cur_back[16]
    next_back[13]=cur_back[11]
    next_back[16]=cur_back[22]
    next_back[17]=cur_back[12]
    next_back[21]=cur_back[23]
    next_back[22]=cur_back[17]
    next_back[23]=cur_back[13]

    next_back[4]=cur_back[10]
    next_back[6]=cur_back[15]
    next_back[7]=cur_back[20]

    next_back[10]=cur_front[0]
    next_back[15]=cur_front[2]
    next_back[20]=cur_front[4]

    next_front[0]=cur_front[13]
    next_front[2]=cur_front[17]
    next_front[4]=cur_front[23]

    next_front[13]=cur_back[4]
    next_front[17]=cur_back[6]
    next_front[23]=cur_back[7]
  elif(c=='R\''):
    next_back[11]=cur_back[13]
    next_back[12]=cur_back[17]
    next_back[13]=cur_back[23]
    next_back[16]=cur_back[12]
    next_back[17]=cur_back[22]
    next_back[21]=cur_back[11]
    next_back[22]=cur_back[16]
    next_back[23]=cur_back[21]

    next_back[4]=cur_front[13]
    next_back[6]=cur_front[17]
    next_back[7]=cur_front[23]

    next_back[10]=cur_back[4]
    next_back[15]=cur_back[6]
    next_back[20]=cur_back[7]

    next_front[0]=cur_back[10]
    next_front[2]=cur_back[15]
    next_front[4]=cur_back[20]

    next_front[13]=cur_front[0]
    next_front[17]=cur_front[2]
    next_front[23]=cur_front[4]
  elif(c=='R2'):
    next_back[11]=cur_back[23]
    next_back[12]=cur_back[22]
    next_back[13]=cur_back[21]
    next_back[16]=cur_back[17]
    next_back[17]=cur_back[16]
    next_back[21]=cur_back[13]
    next_back[22]=cur_back[12]
    next_back[23]=cur_back[11]

    next_back[4]=cur_front[0]
    next_back[6]=cur_front[2]
    next_back[7]=cur_front[4]

    next_back[10]=cur_front[13]
    next_back[15]=cur_front[17]
    next_back[20]=cur_front[23]

    next_front[0]=cur_back[4]
    next_front[2]=cur_back[6]
    next_front[4]=cur_back[7]

    next_front[13]=cur_back[10]
    next_front[17]=cur_back[15]
    next_front[23]=cur_back[20]
  elif(c=='B'):
    next_front[11]=cur_front[21]
    next_front[12]=cur_front[16]
    next_front[13]=cur_front[11]
    next_front[16]=cur_front[22]
    next_front[17]=cur_front[12]
    next_front[21]=cur_front[23]
    next_front[22]=cur_front[17]
    next_front[23]=cur_front[13]

    next_front[4]=cur_front[10]
    next_front[6]=cur_front[15]
    next_front[7]=cur_front[20]

    next_front[10]=cur_back[0]
    next_front[15]=cur_back[2]
    next_front[20]=cur_back[4]

    next_back[0]=cur_back[13]
    next_back[2]=cur_back[17]
    next_back[4]=cur_back[23]

    next_back[13]=cur_front[4]
    next_back[17]=cur_front[6]
    next_back[23]=cur_front[7]
  elif(c=='B\''):
    next_front[11]=cur_front[13]
    next_front[12]=cur_front[17]
    next_front[13]=cur_front[23]
    next_front[16]=cur_front[12]
    next_front[17]=cur_front[22]
    next_front[21]=cur_front[11]
    next_front[22]=cur_front[16]
    next_front[23]=cur_front[21]

    next_front[4]=cur_back[13]
    next_front[6]=cur_back[17]
    next_front[7]=cur_back[23]

    next_front[10]=cur_front[4]
    next_front[15]=cur_front[6]
    next_front[20]=cur_front[7]

    next_back[0]=cur_front[10]
    next_back[2]=cur_front[15]
    next_back[4]=cur_front[20]

    next_back[13]=cur_back[0]
    next_back[17]=cur_back[2]
    next_back[23]=cur_back[4]
  elif(c=='B2'):
    next_front[11]=cur_front[23]
    next_front[12]=cur_front[22]
    next_front[13]=cur_front[21]
    next_front[16]=cur_front[17]
    next_front[17]=cur_front[16]
    next_front[21]=cur_front[13]
    next_front[22]=cur_front[12]
    next_front[23]=cur_front[11]

    next_front[4]=cur_back[0]
    next_front[6]=cur_back[2]
    next_front[7]=cur_back[4]

    next_front[10]=cur_back[13]
    next_front[15]=cur_back[17]
    next_front[20]=cur_back[23]

    next_back[0]=cur_front[4]
    next_back[2]=cur_front[6]
    next_back[4]=cur_front[7]

    next_back[13]=cur_front[10]
    next_back[17]=cur_front[15]
    next_back[23]=cur_front[20]
  elif(c=='D'):
    next_front[0]=cur_front[3]
    next_front[2]=cur_front[1]
    next_front[4]=cur_front[0]
    next_front[1]=cur_front[5]
    next_front[6]=cur_front[2]
    next_front[3]=cur_front[7]
    next_front[5]=cur_front[6]
    next_front[7]=cur_front[4]

    next_front[8]=cur_front[11]
    next_front[9]=cur_front[12]
    next_front[10]=cur_front[13]

    next_front[11]=cur_back[23]
    next_front[12]=cur_back[22]
    next_front[13]=cur_back[21]

    next_back[23]=cur_back[20]
    next_back[22]=cur_back[19]
    next_back[21]=cur_back[18]

    next_back[20]=cur_front[8]
    next_back[19]=cur_front[9]
    next_back[18]=cur_front[10]
  elif(c=='D\''):
    next_front[0]=cur_front[4]
    next_front[2]=cur_front[6]
    next_front[4]=cur_front[7]
    next_front[1]=cur_front[2]
    next_front[6]=cur_front[5]
    next_front[3]=cur_front[0]
    next_front[5]=cur_front[1]
    next_front[7]=cur_front[3]

    next_front[8]=cur_back[20]
    next_front[9]=cur_back[19]
    next_front[10]=cur_back[18]

    next_front[11]=cur_front[8]
    next_front[12]=cur_front[9]
    next_front[13]=cur_front[10]

    next_back[23]=cur_front[11]
    next_back[22]=cur_front[12]
    next_back[21]=cur_front[13]

    next_back[20]=cur_back[23]
    next_back[19]=cur_back[22]
    next_back[18]=cur_back[21]
  elif(c=='D2'):
    next_front[0]=cur_front[7]
    next_front[2]=cur_front[5]
    next_front[4]=cur_front[3]
    next_front[1]=cur_front[6]
    next_front[6]=cur_front[1]
    next_front[3]=cur_front[4]
    next_front[5]=cur_front[2]
    next_front[7]=cur_front[0]

    next_front[8]=cur_back[23]
    next_front[9]=cur_back[22]
    next_front[10]=cur_back[21]

    next_front[11]=cur_back[20]
    next_front[12]=cur_back[19]
    next_front[13]=cur_back[18]

    next_back[23]=cur_front[8]
    next_back[22]=cur_front[9]
    next_back[21]=cur_front[10]

    next_back[20]=cur_front[11]
    next_back[19]=cur_front[12]
    next_back[18]=cur_front[13]
  else:
    assert False,"nextview() error: Wrong move!"
  return next_front, next_back
