from PyQt5 import QtWidgets,QtGui , QtCore ,Qt
from PyQt5.QtWidgets import   QFileDialog  ,QWidget,QApplication
from PyQt5.QtGui import QPixmap,QPainter,QPen
from TASK11 import Ui_MainWindow
import sys
import cv2
import PIL
from qimage2ndarray import gray2qimage#,array2qimage
import numpy as np 
from PIL import Image,ImageEnhance
from PIL.ImageQt import ImageQt
#import matplotlib.pyplot as plt
import math

#import pyqtgraph as pg
#import pyqtgraph.exporters
#import matplotlib.pyplot as plt
#from random import randint
start = 10
end = 60
test_prep=0
null_test=0
null=0
class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setFixedSize(350,350)
        self.wheelEvent = self.zoom
        #self.setSceneRect(0, 0, 400, 400)
        self.wheelEvent = self.zoom
        #self.fitInView(0,0, 400, 400, QtCore.Qt.KeepAspectRatio)

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInVieww(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                viewrect = self.viewport().rect()
                print (viewrect)
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                print(factor)
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap):
        self._zoom = 0
        if pixmap :
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QPixmap())
        self.fitInVieww()

    def zoom(self, event):
        if self.hasPhoto():
            print (event.angleDelta().y())
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInVieww()
                print('hi')
            else:
                self._zoom = 0


class Phantom_browser(QtWidgets.QMainWindow):
    def __init__(self):
        super(Phantom_browser, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.browser.clicked.connect(self.selection_shepp)
        self.ui.browser.clicked.connect(self.Earnst)
        self.ui.push2.clicked.connect(self.selection_browse)
        self.ui.pushButton.clicked.connect(self.k_space)

        self.ui.horizontalSlider.valueChanged.connect(self.valuechangeb)
        self.ui.horizontalSlider_2.valueChanged.connect(self.valuechangec)
        
        self.ui.comboBox.currentIndexChanged.connect(self.selectionchange) 
        self.ui.comboBox_2.currentIndexChanged.connect(self.selectionfigure) 
        self.ui.comboBox_ACQUISTION.currentIndexChanged.connect(self.k_space)
        self.ui.comboBox_preparation.currentIndexChanged.connect(self.prep)
        self.ui.comboBox_tissue.currentIndexChanged.connect(self.tissue_selection)
        self.ui.PHANTOM.mousePressEvent=self.getPixel
        self.click=0
        self.iii=0
        self.lll=0
        self.zzz=0
        self.hhh=0
        self.mmm=0
        self.bbb=0
        self.viewer = PhotoViewer(self.ui.graphicsView_phantom)
        self.viewer2 = PhotoViewer(self.ui.graphicsView_Kspace)
        
       # self.ui.PHANTOM.mouseDoubleClickEvent=self.getPixel
        #self.ui.PHANTOM.mouseHold=self.getPixel
    def selection_shepp(self): 
        self.test=1
        self.selectionchange()
    def selection_browse(self):
        self.test=2
        self.selectionchange()
    def selectionchange(self):
         global N
         text = int(self.ui.comboBox .currentText())
         

         if text==128:
                N=32
         elif text==256:
                N=256
         else :
                N=512
          
         if self.test==1:        
            self.button_clicked() 
         if self.test==2:
            self.button_clicked2()
         
    def getPixel(self,event):
      global N
      def event_pos():
      #  self.ui.graphicsView.clear()  
        if(self.click<6):
          self.x=math.floor((event.pos().x()*N)/self.ui.PHANTOM.frameGeometry().width()) 
          self.y=math.floor((event.pos().y()*N)/self.ui.PHANTOM.frameGeometry().height())
          self.frame()
        elif(self.click>5):
          self.ui.graphicsView.clear()    
          self.ui.graphicsView_2.clear()
      if( N==32 and self.test==1): 
       self.click=self.iii+1
       self.iii=self.iii+1
       event_pos()
     #     self.ui.graphicsView.removeItem()
      if (N==256 and self.test==1   ):  
        self.click=self.lll+1
        self.lll=self.lll+1
        event_pos() 
     #     self.ui.graphicsView.removeItem()

      if (N==512 and self.test==1):
        self.click=self.zzz+1
        self.zzz=self.zzz+1
        event_pos()
          
      if( N==128 and self.test==2): 
       self.click=self.hhh+1
       self.hhh=self.hhh+1
       event_pos()
         
      if (N==256 and self.test==2):  
        self.click=self.mmm+1
        self.mmm=self.mmm+1
        event_pos() 
          
      if (N==512 and self.test==2):
        self.click=self.bbb+1
        self.bbb=self.bbb+1
        event_pos()
    def Earnst(self):
         T1 = 800
         flip_angle = np.arange(0,181,2)
         Intensity = np.zeros((len(flip_angle)))
         spinz = 1
         signal = 0
# ******************************************* #
          #T1 Weighted
          #TR = 100

         #T2 Weighted
          #TR = 3000
         tr=(self.ui.lineEdit_2.text())
         self.TR=int(tr)
           #TR = int(sys.argv[1])
         for idx, theta in enumerate(flip_angle):
         #signal = signal* np.sin(theta*np.pi/180)
             for i in range(20): 
                 signal = spinz * np.sin(theta*np.pi/180)
                 spinz = spinz * np.cos(theta*np.pi/180) + (1- spinz * np.cos(theta*np.pi/180)) * (1 - np.exp(-self.TR/T1))
             Intensity[idx] = signal
             spinz = 1
         #print(Intensity)
         plotWindow3 = self.ui.graphicsView_earnst
         plotWindow3.plot(flip_angle, Intensity, pen='m')
         print(np.argmax(Intensity))
         
    def frame(self):
        global image2,t1
        QApplication.processEvents()
        '''figure = str(self.ui.comboBox_2.currentText())
         
        if figure=="T1":
                N=m_s1=20*np.log(np.abs(t1))             
                f_new1=np.asarray( m_s1,dtype=np.uint8)
                T1_img=Image.fromarray(f_new1)
                image=ImageQt(T1_img)
            ##    self.ui.PHANTOM.setPixmap(QPixmap.fromImage(image))
           #     result1 = gray2qimage(self.t1)
                result1= QPixmap.fromImage(image).scaled(N, N,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        elif figure=="T2":
            #    result1 = gray2qimage(self.t2)
                result1= QPixmap.fromImage(image2).scaled(N, N,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
               # image=QPixmap.fromImage(image).scaled(N, N,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
         #       self.ui.PHANTOM.setPixmap(QPixmap.fromImage(image2))
        else :
               result1 = self.pix
               '''
        result1 = self.pix       
        painter= QtGui.QPainter(result1)
        painter.begin(self)
        if (self.click==1):
           self.penRect= QtGui.QPen(QtCore.Qt.red)
        elif (self.click==2):
           self.penRect= QtGui.QPen(QtCore.Qt.green)
        elif (self.click==3):
           self.penRect= QtGui.QPen(QtCore.Qt.blue)
        elif (self.click==4):
           self.penRect=QtGui.QPen(QtCore.Qt.yellow)
        elif (self.click==5):
           self.penRect= QtGui.QPen(QtCore.Qt.magenta)
        else:
            print("end")
        self.penRect.setWidth(1)
        painter.setPen(self.penRect)
        painter.drawRect(self.x,self.y,3, 3)
        painter.end()
        print(self.x , self.y)
        
        result=result1.scaled(int(result1.height()),int(result1.width()))
     
        self.ui.PHANTOM.setPixmap(result)
        QApplication.processEvents()
        self.plot()
        
        
   
        
    def plot(self):
        arr1 = []
        arr2 = []

        plotWindow = self.ui.graphicsView
        plotWindow2 = self.ui.graphicsView_2
        self.t1_value=self.tt1[self.x,self.y]
        self.t2_value=self.tt2[self.x,self.y]
        t1_plot=self.t1_value
        t2_plot=self.t2_value
     #   print('t1',t1_plot)
     #   print('t2',t2_plot)
       
        spin=(self.ui.lineEdit_4.text())
        self.ST=int(spin)
        tr=(self.ui.lineEdit_2.text())
        self.TR=int(tr)
        te=(self.ui.lineEdit_3.text())
        self.TE=int(te)
        for t in range (self.ST):
            Mz=(1-np.exp(-t/t1_plot))
            Mxy=np.exp(-t/t2_plot)
    
           
            arr1.append(Mz)
            arr2.append(Mxy)
        
            QtGui.QApplication.processEvents() 
            
        if(self.click==1):
           plotWindow.plot([self.TR,self.TR],(0,1), pen='w')
           plotWindow2.plot([self.TE,self.TE],(0,1), pen='w')
           plotWindow.plot(arr1, pen='r')
           plotWindow2.plot(arr2, pen='r')
        elif(self.click==2):
           plotWindow.plot(arr1, pen='g')
           plotWindow2.plot(arr2, pen='g')
        elif (self.click==3):
           plotWindow.plot(arr1, pen='b')
           plotWindow2.plot(arr2, pen='b')
        elif(self.click==4):   
           plotWindow.plot(arr1, pen='y')
           plotWindow2.plot(arr2, pen='y')
        elif(self.click==5):
           plotWindow.plot(arr1, pen='m')
           plotWindow2.plot(arr2, pen='m')
        else :
            print ("end")
            
       #############CLEAR##########
            
            
        #plot.showGrid(x=True, y=True, alpha=1)

    def selectionfigure(self): ###t1.t2.pd
        global t1,t2,N,image,image2
        
        figure = str(self.ui.comboBox_2.currentText())
         
        if (figure=="T1" and self.test==1):
                N=m_s1=20*np.log(np.abs(t1))             
                f_new1=np.asarray( m_s1,dtype=np.uint8)
                T1_img=Image.fromarray(f_new1)
                image=ImageQt(T1_img)
                self.ui.PHANTOM.setPixmap(QPixmap.fromImage(image))
        elif (figure=="T2" and self.test==1):
                N=m_s1=20*np.log(np.abs(t2))             
                f_new2=np.asarray( m_s1,dtype=np.uint8)
                T2_img=Image.fromarray(f_new2)
                image2=ImageQt(T2_img)
                self.ui.PHANTOM.setPixmap(QPixmap.fromImage(image2))
        elif (figure=="PD"):
                self.selectionchange()
        elif (figure=="T1" and self.test==2):
                m_s1=20*np.log(np.abs(t1))             
                f_new1=np.asarray( m_s1,dtype=np.uint8)
                T1_img=Image.fromarray(f_new1)
                image=ImageQt(T1_img)
                self.ui.PHANTOM.setPixmap(QPixmap.fromImage(image))
        elif (figure=="T2" and self.test==2):
                m_s1=20*np.log(np.abs(t2))             
                f_new2=np.asarray( m_s1,dtype=np.uint8)
                T2_img=Image.fromarray(f_new2)
                image2=ImageQt(T2_img)
                self.ui.PHANTOM.setPixmap(QPixmap.fromImage(image2))
    
    
    def button_clicked2(self):
        global t1,t2,P,N
        fileName, _filter = QFileDialog.getOpenFileName(self, "Title"," " , "Filter --  file (*.dat);;img file (*.PNG)")
        if fileName:
            v = np.load(fileName)
            scale=np.asarray(v,dtype=np.uint8)
            image=Image.fromarray(scale)
            image=ImageQt(image)
            self.pix=QPixmap.fromImage(image).scaled(N, N,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
            self.ui.PHANTOM.setPixmap(self.pix)
            image.save("ph.png")
            img = cv2.imread("ph.png", 0)
            img=cv2.resize(img, (N,N), interpolation = cv2.INTER_AREA)
            P = np.array(img)
            t1= np.array(img)
            t2= np.array(img)
        
                          
        
    
            for self.k in range (0,N):
               for self.m in range (0,N):
                   t1[self.k,self.m]=(t1[self.k,self.m]+(7000))/2
                   t2[self.k,self.m]=(t2[self.k,self.m]+(5))/2

            print("t1")
            self.tt1=t1 
            self.tt2=t2
             
               
    def button_clicked(self):

        global iff,t1,t2,P,N
        
        def phantom (n = N, p_type = 'Modified Shepp-Logan', ellipses = None):
	           if (ellipses is None):
		           ellipses = _select_phantom (p_type)
	           elif (np.size (ellipses, 1) != 6):
		           raise AssertionError ("Wrong number of columns in user phantom")
	
	
               
	           p = np.zeros ((n, n))
	
	           ygrid, xgrid = np.mgrid[-1:1:(1j*n), -1:1:(1j*n)]
	           for ellip in ellipses:
            		I   = ellip [0]
            		a2  = ellip [1]**2
            		b2  = ellip [2]**2
            		x0  = ellip [3]
            		y0  = ellip [4]
            		phi = ellip [5] * np.pi / 180  # Rotation angle in radians
            		
            		# Create the offset x and y values for the grid
            		x = xgrid - x0
            		y = ygrid - y0
            		
            		cos_p = np.cos (phi) 
            		sin_p = np.sin (phi)
            		
            		# Find the pixels within the ellipse
            		locs = (((x * cos_p + y * sin_p)**2) / a2 
                      + ((y * cos_p - x * sin_p)**2) / b2) <= 1
            		
            		# Add the ellipse intensity to those pixels
            		p [locs] += I

	           return p

        def _select_phantom (name):
	       
            
            if (name.lower () == 'shepp-logan'):
		      
                e = _shepp_logan ()
            
            elif (name.lower () == 'modified shepp-logan'):
		       
                e = _mod_shepp_logan ()
               
               
	       
            else:
               
		      
                raise ValueError ("Unknown phantom type: %s" % name)
               
	
	       
            return e

        
        def _shepp_logan ():
	#  Standard head phantom, taken from Shepp & Logan
	          return [[   2,   .69,   .92,    0,      0,   0],
	                  [-.98, .6624, .8740,    0, -.0184,   0],
	                  [-.02, .1100, .3100,  .22,      0, -18],
	                  [-.02, .1600, .4100, -.22,      0,  18],
	                  [ .01, .2100, .2500,    0,    .35,   0],
	                  [ .01, .0460, .0460,    0,     .1,   0],
	                  [ .02, .0460, .0460,    0,    -.1,   0],
	                  [ .01, .0460, .0230, -.08,  -.605,   0],
	                  [ .01, .0230, .0230,    0,  -.606,   0],
	                  [ .01, .0230, .0460,  .06,  -.605,   0]]

        def _mod_shepp_logan ():
	#  Modified version of Shepp & Logan's head phantom, 
	#  adjusted to improve contrast.  Taken from Toft.
    #PROTON DENSITY
	           return   [[ 6,   .69,   .92,    0,      0,   0],
	                     [-1, .6624, .8740,    0, -.0184,   0],
	                     [-4, .1100, .3100,  .22,      0, -18],
	                     [-4, .1600, .4100, -.22,      0,  18],
	                     [ 1, .2100, .2500,    0,    .35,   0],
	                     [ 1, .0460, .0460,    0,     .1,   0],
	                     [ 1, .0460, .0460,    0,    -.1,   0],
	                     [ 1, .0460, .0230, -.08,  -.605,   0],
	                     [ 1, .0230, .0230,    0,  -.606,   0],
	                     [ 1, .0230, .0460,  .06,  -.605,   0]]
       #def dis (self): 
       #TO CONVERT ARRAY TO IMAGE          
        self.P= phantom ()
        m_s=20*np.log(np.abs(self.P))
        f_new=np.asarray(m_s,dtype=np.uint8)
        
        image=Image.fromarray(f_new)
        image=ImageQt(image)
        #pix=QPixmap.fromImage(image)
        self.pix=QPixmap.fromImage(image).scaled(N, N,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.ui.PHANTOM.setPixmap(self.pix)
        image.save("my.png")
        img = cv2.imread("my.png", 0)
        img=cv2.resize(img, (N,N), interpolation = cv2.INTER_AREA)
        P = np.array(img)
        self.viewer.setPhoto(QPixmap(self.pix))
        
        '''t1= np.array(img)
        t2= np.array(img)
        
        for self.i in range (0,N):
              for self.j in range (0,N):
                   t1[self.i,self.j]=(t1[self.i,self.j]+(500))/2
                   t2[self.i,self.j]=(t2[self.i,self.j]+(3))/2
                   '''
        t1=np.random.random((N,N))
        t2=np.random.random((N,N))
    
        data=[]
        s=0
        q=0
        for i in range (0,N):
             for j in range (0,N):
              a=P[i,j]
              if(a not in data):
                data.append(a)
                s=s+10
                q=q+1
                for k in range(0,N):
                    for m in range (0,N):
                       if P[k,m]==P[i,j]:
                         # t1[k,m]=(P[k,m]+(s+800))/2
                          #t2[k,m]=(P[k,m]+(q+300))/2
                          t1[k][m]=(P[k,m]*(s+1)+(30))
                          t2[k][m]=(P[k,m]*(q+1)+(5))
         
        max_t1=np.max(t1)
        min_t1=np.min(t1)
        t1=(225/(max_t1-min_t1)*(t1-min_t1))+30
        max_t2=np.max(t2)
        min_t2=np.min(t2)
        t2=((195/(max_t2-min_t2)*(t2-min_t2))+5)           

        print ("P") 
        
        self.tt1=t1 
        self.tt2=t2
     
    def valuechangeb(self):
            global img,P,t1,t2,result1
            figure = str(self.ui.comboBox_2.currentText())
         
            if figure=="T1":
                result1 = gray2qimage(t1)
            elif figure=="T2":
                result1 = gray2qimage(t2)
            else :
               result1 = gray2qimage(P)
         
            self.ui.PHANTOM.setPixmap(QPixmap.fromImage(result1))
            result1.save("result1.png")
            img = PIL.Image.open("result1.png")
            factor = self.ui.horizontalSlider.value()
            brightness = ImageEnhance.Brightness(img).enhance(factor/8)
            brightness.save("out.png")
            self.ui.PHANTOM.setPixmap(QPixmap("out.png")) 
  #  def SELECT_ACQUISTION(self):
    def decay(self,phantom,ii,jj):
        dec=np.exp(-self.TE/t2[ii,jj])
        phantom[ii,jj,:]=np.dot(dec,phantom[ii,jj,:]) 
        return phantom[ii,jj,:]
    
    def recovery(self,phantom,ii,jj,timeR):
        phantom[ii,jj,0]=0
        phantom[ii,jj,1]=0
        phantom[ii,jj,2]=((phantom[ii,jj,2])*np.exp(-timeR/t1[ii,jj]))+(1-np.exp(-timeR/t1[ii,jj]))
                    
    def ROTATE(self,phantom,ii,jj,theta):
        RF=([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta),0,np.cos(theta)]])
        phantom[ii,jj,:]=np.dot(RF,phantom[ii,jj,:])
        return phantom[ii,jj,:]
    
    def prep(self):
        global test_prep
        preparation = str(self.ui.comboBox_preparation.currentText())
        if preparation=="IR":
          test_prep=1                
        elif preparation=="T2_prep":
          test_prep=2             
        elif preparation=="Tagging":
           test_prep=3              
        elif preparation=="none":
            test_prep=4   
            
    def create(self):
        global row ,col ,N
        row=col=N                    
        phantom=np.zeros((row,col,3))
        for ii in range(row):
            for jj in range(col):
                phantom[ii,jj,2]=1
        return phantom        
    def tissue_selection (self):
        global null_test
        tissue = str(self.ui.comboBox_tissue.currentText())
        if tissue=="Black":
                null_test=1
        
        elif tissue=="Gray":
                null_test=2
    def IR(self,null_test,row,col):
            if null_test==1:
                null=t1[2,2]  ##30
                print (null,"null")
            elif null_test==2:
                null=t1[20,8]         #255
                print (null,"null2")
            phantom=self.create()
            t_null= np.log(2)*null
            theta1=np.radians(180)
            for DD in range(row): 
                for FF in range(col):
                    phantom[DD,FF,:]=self.ROTATE(phantom,DD,FF,theta1)
            for DD in range(row): 
                for FF in range(col):       
                    phantom[DD,FF,0]=0
                    phantom[DD,FF,1]=0
                    phantom[DD,FF,2]=((phantom[DD,FF,2])*np.exp(-t_null/t1[DD,FF]))+(1-np.exp(-t_null/t1[DD,FF]))
            return phantom
        
    def t2_prep(self,row,col,timeR):
           phantom=self.create() 
           for DD in range(row): 
                for FF in range(col):
                  theta1=np.radians(90)
                  phantom[DD,FF,:]=self.ROTATE(phantom,DD,FF,theta1)
           for DDDD in range(row): 
                for FFFF in range(col):
                    phantom[DDDD,FFFF,2]=((phantom[DDDD,FFFF,2])*np.exp(-timeR/t1[DDDD,FFFF]))+(1-np.exp(-timeR/t1[DDDD,FFFF]))
           for DDD in range(row): 
                for FFF in range(col):
                  theta2=np.radians(-90)
                  phantom[DDD,FFF,:]=self.ROTATE(phantom,DDD,FFF,theta2)
           return phantom
    def tagging (self,row,col):
        phantom=self.create()
        for tt in range (row):
           for pp in range (col):
              theta3=(tt*np.pi)/row
              sinangle=np.sin(theta3)
              phantom[tt,pp,:]=phantom[tt,pp,:]*sinangle
        return phantom 
    def start_up(self,row,col,phantom,theta,timeR):
        for t in range (16):
          for p in range (16):
              for ee in range(row): 
                 for cc in range(col):
                    phantom[ee,cc,:]=self.ROTATE(phantom,ee,cc,theta)
                    phantom[ee,cc,:]=self.decay(phantom,ee,cc)
                    self.recovery(phantom,ee,cc,timeR)
        return phantom
    def GRE(self,phantom,ii,jj,theta):
        self.ROTATE(phantom,ii,jj,theta)
        self.decay(phantom,ii,jj)
    def SSFP(self,FA,phantom,ii,jj,theta):
        flip=FA 
        if flip==FA:
           flip==FA/2
           theta=np.radians(flip)
           self.ROTATE(phantom,ii,jj,theta)
           self.decay(phantom,ii,jj)
        elif flip==FA/2:
           theta=np.radians(FA)
           flip==FA/4
           self.ROTATE(phantom,ii,jj,theta)
           self.decay(phantom,ii,jj)
        elif flip==FA/4:
           theta=np.radians(FA*(-1))
           flip==FA/2
           self.ROTATE(phantom,ii,jj,theta)
           self.decay(phantom,ii,jj) 
#    def SE(self,phantom,row,col,timeR):
#        for ii in range(row): 
#                for jj in range(col):
#                    theta1=np.radians(90)
#                    self.ROTATE(phantom,ii,jj,theta1)
#                    self.decay(phantom,ii,jj) 
#        for ph_rowtr in range(row): 
#                for ph_coltr in range(col):
#                        phantom[ph_rowtr,ph_coltr,0]=0
#                        phantom[ph_rowtr,ph_coltr,1]=0
#                        phantom[ph_rowtr,ph_coltr,2]=((phantom[ph_rowtr,ph_coltr,2])*np.exp(-timeR/t1[ph_rowtr,ph_coltr]))+(1-np.exp(-timeR/t1[ph_rowtr,ph_coltr]))
#                                   
#        for iii in range(row): 
#                for jjj in range(col):
#                    theta2=np.radians(180)
#                    self.ROTATE(phantom,iii,jjj,theta2)
#                    self.decay(phantom,iii,jjj)
#        return phantom            
    def k_space(self):
        global iff ,N,t1,t2,P ,row ,col ,test_prep ,null_test
        kspace=np.zeros((P.shape[0],P.shape[1]),dtype=np.complex_)
        angle=(self.ui.lineEdit.text())
        self.flip_angle=int(angle)
        FA=self.flip_angle
        theta=np.radians(self.flip_angle)
        tr=(self.ui.lineEdit_2.text())
        self.TR=int(tr)
        timeR=self.TR
        te=(self.ui.lineEdit_3.text())
        self.TE=int(te)
        row=col=N
        if test_prep==1:      ##t1_prep
            phantom=self.IR(null_test,row,col)
            
        elif test_prep==4:      ##none
           phantom=self.create() 
           
        elif test_prep==2:       ##t2_prep
           phantom=self.t2_prep(row,col,timeR) 
          
        elif test_prep==3:        ##tagging
            phantom=self.tagging (row,col)
            
            '''phantom=self.create()
            for tt in range (row):
              for pp in range (col):
                  theta3=(tt*np.pi)/row
                  sinangle=np.sin(theta3)
                  phantom[tt,pp,:]=phantom[tt,pp,:]*sinangle
                  '''
        phantom=self.start_up(row,col,phantom,theta,timeR)         
        
        for KR0W_index in range(kspace.shape[0]):  #kspacerow
         #   for ii in range(row): 
         #       for jj in range(col):
                   #  dec=np.exp(-self.TE/t2[ii,jj])
            acquistion = str(self.ui.comboBox_ACQUISTION.currentText())
         
            if acquistion=="GRE":
                        for ii in range(row): 
                            for jj in range(col): 
                                self.GRE(phantom,ii,jj,theta) 
                        
            elif acquistion=="SSFP":
                         for ii in range(row): 
                             for jj in range(col):
                                 self.SSFP(FA,phantom,ii,jj,theta)
                        
            elif acquistion=="SE" :
                     #   phantom=self.SE(phantom,row,col,timeR)    
                for ii in range(row): 
                  for jj in range(col):
                    theta1=np.radians(90)
               #     phantom[ii,jj,:]=self.ROTATE(phantom,ii,jj,theta1)
                    RF=([[np.cos(theta1),0,np.sin(theta1)],[0,1,0],[-np.sin(theta1),0,np.cos(theta1)]])
                    phantom[ii,jj,:]=np.dot(RF,phantom[ii,jj,:])
                    
               #     phantom[ii,jj,:]=self.decay(phantom,ii,jj) 
                    dec=np.exp(-self.TE/2*t2[ii,jj])
                    phantom[ii,jj,:]=np.dot(dec,phantom[ii,jj,:])
                for ph_rowtr in range(row): 
                        for ph_coltr in range(col):
                                phantom[ph_rowtr,ph_coltr,0]=0
                                phantom[ph_rowtr,ph_coltr,1]=0
                                phantom[ph_rowtr,ph_coltr,2]=((phantom[ph_rowtr,ph_coltr,2])*np.exp(-timeR/t1[ii,jj]))+(1-np.exp(-timeR/t1[ph_rowtr,ph_coltr]))
                                           
                for ii in range(row): 
                        for jj in range(col):
                            theta2=np.radians(180)
                          #  phantom[ii,jj,:]=self.ROTATE(phantom,ii,jj,theta2)
                            RF=([[np.cos(theta2),0,np.sin(theta2)],[0,1,0],[-np.sin(theta2),0,np.cos(theta2)]])
                            phantom[ii,jj,:]=np.dot(RF,phantom[ii,jj,:])
                         #   phantom[ii,jj,:]=self.decay(phantom,ii,jj)
                            dec=np.exp(-self.TE/t2[ii,jj])
                            phantom[ii,jj,:]=np.dot(dec,phantom[ii,jj,:])
                phantom=phantom *255        
            for KCOL_index in range(kspace.shape[1]):
                Gx_step=((2*np.pi)/row)*KR0W_index
      #          Gy_step=((4*np.pi/(col))*(KCOL_index))  ### aliasing
                Gy_step=((2*np.pi/(col))*(KCOL_index))
                for ph_row in range(row): 
                    for ph_col in range(col):
                        Toltal_theta=(Gx_step*ph_row)+(Gy_step*(ph_col))
                        Mag=np.sqrt(((phantom[ph_row,ph_col,0])*(phantom[ph_row,ph_col,0]))+((phantom[ph_row,ph_col,1])*(phantom[ph_row,ph_col,1])))
                        kspace[KR0W_index,KCOL_index]=kspace[KR0W_index,KCOL_index]+(Mag*np.exp(-1j*Toltal_theta))
                    QApplication.processEvents()
                QApplication.processEvents()
            for ph_rowtr in range(row): 
                for ph_coltr in range(col):
                    if acquistion=="GRE" :
                      phantom[ph_rowtr,ph_coltr,0]=0
                      phantom[ph_rowtr,ph_coltr,1]=0
                      phantom[ph_rowtr,ph_coltr,2]=((phantom[ph_rowtr,ph_coltr,2])*np.exp(-self.TR/t1[ii,jj]))+(1-np.exp(-self.TR/t1[ph_rowtr,ph_coltr]))
                    elif acquistion=="SSFP":
                      phantom[ph_rowtr,ph_coltr,2]=((phantom[ph_rowtr,ph_coltr,2])*np.exp(-self.TR/t1[ii,jj]))+(1-np.exp(-self.TR/t1[ph_rowtr,ph_coltr]))
                    elif acquistion=="SE" :
                      phantom[ph_rowtr,ph_coltr,0]=0
                      phantom[ph_rowtr,ph_coltr,1]=0
                      phantom[ph_rowtr,ph_coltr,2]=((phantom[ph_rowtr,ph_coltr,2])*np.exp(-self.TR/t1[ii,jj]))+(1-np.exp(-self.TR/t1[ph_rowtr,ph_coltr]))
                   
                QApplication.processEvents()
            QApplication.processEvents()
        print(kspace)
        iff= np.fft.ifft2(kspace*155)
        inverse_array=np.abs(iff)
        inverse_img=gray2qimage(inverse_array)
        print("inverse_img")
        imgreconstruction = QPixmap(inverse_img)#piexel of image
        self.imgrecstructionon=imgreconstruction.scaled(int(imgreconstruction.height()), int(imgreconstruction.width()),QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation) #scale 3la elabel
        self.viewer2.setPhoto(QPixmap(self.imgrecstructionon))
    
    def valuechangec(self):
            global img, t1
            figure = str(self.ui.comboBox_2.currentText())
            if figure=="T1":
                result1 = gray2qimage(t1)
            elif figure=="T2":
                result1 = gray2qimage(t2)
            else :
               result1 = gray2qimage(P)
         #   result1 = gray2qimage(t1)
            self.ui.PHANTOM.setPixmap(QPixmap.fromImage(result1))
            result1.save("result1.png")
            img = PIL.Image.open("result1.png")
            factor = self.ui.horizontalSlider_2.value()
            contrast = ImageEnhance.Contrast(img).enhance(factor)
            contrast.save("out.png")
            self.ui.PHANTOM.setPixmap(QPixmap("out.png"))
                
        

            
            
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = Phantom_browser()
    application.show()
    
  
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()