#I have set my Raspberry Pi to auto-run this script when power on
import cv2
import numpy as np
import keras
from keras.applications.mobilenet_v2 import preprocess_input
from gpiozero import Button
from DrawRubik import draw_rubik
from DrawRubik import draw_arrow
from DrawRubik import nextview
from rubik_solver import utils

#Set buttons
Next = Button(17) #GPIO
Back = Button(18) #GPIO

#Load all models
models = []
for i in range (24):
  models.append(keras.models.load_model('./rubik_MobileNet_p{}.h5'.format(i)))

#Warm up keras model
rubikpic = np.load('./rubikpic_random.npy') # A random rubik's cube image
rubikpic = models[0].predict(rubikpic)
del rubikpic

#Main window
winname = 'FastSolve'
cv2.namedWindow(winname,cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN) #the window size is full screen (without tab bar)

#Test camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)
ret, frame = cap.read()
try:
  shape = frame.shape
  del shape
except:
  img = cv2.imread('./camera_error.jpg')
  cv2.imshow(winname, img)                 #On the PiCamera there is a yellow thing called Sunny, and my Sunny is very fragile 
  while True:
    if(cv2.waitKey(50) & Next.is_pressed): #if Next button is pressed
      from subprocess import call
      call("sudo poweroff", shell=True)    #poweroff is the only way to fix
      break
      
#Prepare
welcome = cv2.imread('./welcome.jpg')
ori = cv2.imread('./rubikpic_ori.jpg')
solved_state = 'yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww'
trans = {'U':'U','U\'':'U\'','U2':'U2',
      'D':'D','D\'':'D\'','D2':'D2',
      'F':'L','F\'':'L\'','F2':'L2',
      'B':'R','B\'':'R\'','B2':'R2',
      'L':'B','L\'':'B\'','L2':'B2',
      'R':'F','R\'':'F\'','R2':'F2'} #Translate rubik_solver's view to my back view
font = cv2.FONT_HERSHEY_SIMPLEX
state = 0

#Main Loop
while True:
  #Before step into any state
  Back.wait_for_release()
  Next.wait_for_release()
  if(state==0):
    #Show welcome
    cv2.imshow(winname,welcome)
    while True:
      if(cv2.waitKey(50) & Next.is_pressed): #check per 50ms
        state = 1
        break
  elif(state==1):
    #Take front view image (when Next is pressed) then predict
    while(True):
      ret, frame = cap.read() #frame size is 256x256
      img = np.copy(frame)
      img = cv2.resize(img,dsize=(512,512),interpolation = cv2.INTER_AREA) #larger size for displaying
      cv2.putText(img,'Take a picture from front view',(60,480),font,0.8,(10,240,240),2,cv2.LINE_AA)
      cv2.imshow(winname, img)
      
      if(cv2.waitKey(1) & Back.is_pressed):
        state = 0
        break
      elif(cv2.waitKey(1) & Next.is_pressed): #predicting
        td = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        td = preprocess_input(td)
        td = np.array([td])
        color_front = np.zeros(24,np.uint8)
        for i in range(24): #Use models to predict
          color_front[i] = np.argmax(models[i].predict(td))
        state = 2
        break
  elif(state==2):
    #Draw front view and say 'Please check'
    #(mis-prediction may happen if the taken image is blurry or the reflected light on the cube is too bright)
    img = draw_rubik(color_front,front=True)
    cv2.putText(img,'Please check',(150,480),font,1,(128,20,20),2,cv2.LINE_AA)
    cv2.imshow(winname,img)
    while True:
      if(cv2.waitKey(25) & Back.is_pressed):
        state = 1
        break
      elif(cv2.waitKey(25) & Next.is_pressed):
        state = 3
        break
  elif(state==3):
    #Take back view image (when Next is pressed) then predict
    while(True):
      ret, frame = cap.read() #frame size is 256x256
      img = np.copy(frame)
      img = cv2.resize(img,(512,512))
      cv2.putText(img,'Take a picture from back view',(60,480),font,0.8,(10,240,240),2,cv2.LINE_AA)
      cv2.imshow(winname, img)
      if(cv2.waitKey(1) & Back.is_pressed):
        state = 2
        break
      elif(cv2.waitKey(1) & Next.is_pressed): #predicting
        td = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        td = preprocess_input(td)
        td = np.array([td])
        color_back = np.zeros(24,np.uint8)
        for i in range(24): #Use models to predict
          color_back[i] = np.argmax(models[i].predict(td))
        state = 4
        break
  elif(state==4):
    #Draw front view and say 'Please check'
    #(mis-prediction may happen if the taken image is blurry or the reflected light on the cube is too bright)
    img = draw_rubik(color_back,front=False)
    cv2.putText(img,'Please check',(150,480),font,1,(128,20,20),2,cv2.LINE_AA)
    cv2.imshow(winname,img)
    while True:
      if(cv2.waitKey(25) & Back.is_pressed):
        state = 3
        break
      elif(cv2.waitKey(25) & Next.is_pressed):
        img = np.copy(ori)
        cv2.putText(img,'Please wait...',(160,480),font,1,(128,20,20),2,cv2.LINE_AA)
        cv2.imshow(winname,img)
        cv2.waitKey(1)
        state = 5
        break
  elif(state==5):
    #This state would take very long time (20~30s) because the calculation to find optimal solution is complicate
    #Color to string for rubik_solver module
    c2c = 'wbrygo' #color to char
    cube_U = c2c[color_back[4]]+c2c[color_back[6]]+c2c[color_back[7]]+c2c[color_back[2]]+'y'+c2c[color_back[5]]+c2c[color_back[0]]+c2c[color_back[1]]+c2c[color_back[3]]
    cube_L = c2c[color_front[23]]+c2c[color_front[22]]+c2c[color_front[21]]+c2c[color_front[17]]+'b'+c2c[color_front[16]]+c2c[color_front[13]]+c2c[color_front[12]]+c2c[color_front[11]]
    cube_F = c2c[color_front[20]]+c2c[color_front[19]]+c2c[color_front[18]]+c2c[color_front[15]]+'r'+c2c[color_front[14]]+c2c[color_front[10]]+c2c[color_front[9]]+c2c[color_front[8]]
    cube_R = c2c[color_back[8]]+c2c[color_back[9]]+c2c[color_back[10]]+c2c[color_back[14]]+'g'+c2c[color_back[15]]+c2c[color_back[18]]+c2c[color_back[19]]+c2c[color_back[20]]
    cube_B = c2c[color_back[11]]+c2c[color_back[12]]+c2c[color_back[13]]+c2c[color_back[16]]+'o'+c2c[color_back[17]]+c2c[color_back[21]]+c2c[color_back[22]]+c2c[color_back[23]]
    cube_D = c2c[color_front[7]]+c2c[color_front[5]]+c2c[color_front[3]]+c2c[color_front[6]]+'w'+c2c[color_front[1]]+c2c[color_front[4]]+c2c[color_front[2]]+c2c[color_front[0]]
    cube = cube_U+cube_L+cube_F+cube_R+cube_B+cube_D
    #rubik-solver would solve a solved cube in 13 moves :), so
    if(cube==solved_state):
      img = draw_rubik(color_back,front=False)
      cv2.putText(img,'Solved!',(205,480),font,1,(128,20,20),2,cv2.LINE_AA)
      cv2.imshow(winname,img)
      while True:
        if(cv2.waitKey(50) & Next.is_pressed):
          state = 0
          break
    else:
      try:
        ans = utils.solve(cube, 'Kociemba') #may occur error if color predictions are wrong
        all_back = []                       #all the back views of every step
        cur_front = np.copy(color_front)    #current front
        cur_back = np.copy(color_back)      #current back
        ans_real = []                       #translate the answer to my back view
        for c in ans:
          ans_real.append(trans[str(c)])
        all_back.append(color_back)         #store the original back view first
        for c in ans_real:
          cur_front, cur_back = nextview(cur_front, cur_back, str(c))
          all_back.append(cur_back)         #store back view after every move
        img = draw_rubik(color_back,front=False)
        cv2.putText(img,'Ready!',(205,480),font,1,(128,20,20),2,cv2.LINE_AA)
        cv2.imshow(winname,img)
        while True:
          if(cv2.waitKey(25) & Back.is_pressed):
            state = 4
            break
          elif(cv2.waitKey(25) & Next.is_pressed):
            state = 6
            break
      except:
        img = np.copy(ori)
        cv2.putText(img,'There is something wrong!',(90,480),font,0.8,(20,20,128),2,cv2.LINE_AA) #maybe mis-predicted
        cv2.imshow(winname,img)
        while True:
          if(cv2.waitKey(25) & Back.is_pressed):
            state = 4
            break
          elif(cv2.waitKey(25) & Next.is_pressed):
            state = 0
            break
  elif(state==6):
    #Show instructions
    #Now we have len(ans) views(include initial back view)
    step = 0
    last_step = len(ans) # not a real last step
    
    #Text for displaying at the middle bottom of screen
    half_step = last_step/2
    text_ans_up = ''
    text_ans_down = ''
    for text_index in range(last_step):
      if(text_index<half_step):
        text_ans_up = text_ans_up + str(ans_real[text_index]) + ' '
      else:
        text_ans_down = text_ans_down + str(ans_real[text_index]) + ' ' 
    textsize_up = cv2.getTextSize(text_ans_up, font, 0.7, 2)[0]
    textsize_down = cv2.getTextSize(text_ans_down, font, 0.7, 2)[0]
    textX_up = (512 - textsize_up[0]) // 2
    textX_down = (512 - textsize_down[0]) // 2

    #Show back view with arrow according to step
    change_state = False
    while True:
      if(change_state):
        break
      if(step==last_step):
        img = draw_rubik(all_back[step],front=False)
        cv2.putText(img,'Congratulation!',(160,480),font,0.8,(128,20,20),2,cv2.LINE_AA)
      else:
        img = draw_rubik(all_back[step],front=False)
        cv2.putText(img,text_ans_up,(textX_up,440),font,0.7,(128,20,20),2,cv2.LINE_AA)
        cv2.putText(img,text_ans_down,(textX_down,480),font,0.7,(128,20,20),2,cv2.LINE_AA)
        img = draw_arrow(img, str(ans_real[step]))
      cv2.imshow(winname,img)
      while True:
        if(cv2.waitKey(25) & Back.is_pressed):
          if(step==0):
            state = 4 #Back to state 4, not 5
            change_state = True
          else:
            step -= 1
          Back.wait_for_release()
          break
        elif(cv2.waitKey(25) & Next.is_pressed):
          if(step==last_step):
            state = 0
            change_state = True
          else:
            step += 1
          Next.wait_for_release()
          break
