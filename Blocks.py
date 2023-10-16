import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import scipy
import imageio
import os
import shutil
import sys
import moviepy.editor as mp
import matplotlib.image as mpimg
import matplotlib as mpl
"""Goal:
   Make a funny gif making code
   Rules:
   A point has a certain speed and plots one square every second lapsed
   Each time the point reaches the end of the map he bounces back and gains x% speed
   The code stops after K bounces
   Limits: 
   A 100 by 100 map
   The point starts at 1m/s at a random location and direction
    
    
    
"""
def plot_squares(x_tab,y_tab,c,color,ax):
    """image='E:/Desktop/python perso/Blocks/dvd_logo/dvd.png'
    img=mpimg.imread(image)
    tx,ty=x_tab[-1],y_tab[-1]
    ax.imshow(img,extent=(tx,tx+5,ty,ty+5))"""
    for x , y , col in zip(x_tab,y_tab,color):
        x_space=[x-c/2,x+c/2]
        y_space=[y-c/2,y+c/2]
        a1=y-c/2
        a2=y+c/2
        plt.fill_between(x_space,a1,a2,color=col,alpha=1,zorder=col[1])
        plt.plot(x_space,[y-c/2,y-c/2],color='black',zorder=col[1])
        plt.plot(x_space,[y+c/2,y+c/2],color='black',zorder=col[1])
        plt.plot([x-c/2,x-c/2],y_space,color='black',zorder=col[1])
        plt.plot([x+c/2,x+c/2],y_space,color='black',zorder=col[1])
    
def where_are_we(x,y):
    if y<0:
        return "True","Lower"
    if x<0:
        return "True","Left"
    if x>100:
        return "True","Right"
    if y>100:
        return "True","Upper"
    else:
        return "False","None"
def initiate_point():
    x_init=np.random.randint(100)
    y_init=np.random.randint(100)
    vx_init=np.random.randint(-100,100)/100
    vy_init=np.sqrt(1-vx_init**2)   
    print("Starting point (%s,%s):" % (x_init,y_init))
    print("Initial speed v=%s*ex+%s*ey" % (vx_init,vy_init))
    return x_init,y_init,vx_init,vy_init
def compute_position(t_simu):
    c=5
    t_tab=np.arange(0,t_simu,0.1) #step of 0.1 sec
    #x_init,y_init,vx_init,vy_init=39,52,-0.68,0.733212
    x_init,y_init,vx_init,vy_init=initiate_point()
    x_tab=[]
    y_tab=[]
    v_x=vx_init
    v_y=vy_init
    """color_init=[0,0,0] #initial color is dark
    color_end=[1,1,1] #final color is white"""
    color_gradient=1/t_simu
    color=[]
    images=[]
    for i in t_tab:
       x_tab.append(x_init+i*v_x)
       y_tab.append(y_init+i*v_y)
       x_init=x_tab[-1]
       y_init=y_tab[-1]
       Veracity,kWord=where_are_we(x_init,y_init) # are we out of the limits yet ? if yes where ?
       if Veracity=="True":  
         v_x=1.001*v_x
         v_y=1.001*v_y
         if kWord=="Upper" or kWord=="Lower":
             v_x=v_x
             v_y=-v_y
         if kWord=="Left" or kWord=="Right":
             v_x=-v_x
             v_y=v_y
       if x_init>100-c/2:
            x_tab[-1]=100-c/2
       if y_init>100-c/2:
            y_tab[-1]=100-c/2
       if x_init<c/2:
            x_tab[-1]=c/2
       if y_init<c/2:
            y_tab[-1]=c/2
       if 4*i % 1==0:  #Plot every 1 seconds
         color.append([0,153*i/(255*t_simu),153/255])
         plt.figure(figsize=(8.00,8.00))
         plt.xlim(0,100)
         plt.ylim(0,100)
         plt.xticks([])
         plt.yticks([])
         ax = plt.gca()
         ax.set_aspect('equal', adjustable='box')
         plot_squares(x_tab,y_tab,c,color,ax)
         i=np.round(i,2)
         plt.title('Time elapsed: %s sec' %i )
         plt.savefig("E:/Desktop/python perso/Blocks/gif_images/%s.jpg" %i )
         images.append(imageio.imread("E:/Desktop/python perso/Blocks/gif_images/%s.jpg" %i ))
         plt.close()
         completion=100*i/t_simu
         print('\r'+str(completion) +'% progression',end='')
         sys.stdout.flush()
    print("")
    print("Plots done , computing final gif file")
    imageio.mimsave('E:/Desktop/python perso/Blocks/gif_save/movie.gif', images)
    clip = mp.VideoFileClip('E:/Desktop/python perso/Blocks/gif_save/movie.gif')
    audio_background = mp.AudioFileClip('E:/Desktop/python perso/Blocks/shitmp3/wii.mp3').set_duration(clip.duration)
    final_audio = mp.CompositeAudioClip([audio_background])
    final_clip = clip.set_audio(final_audio)
    final_clip.write_videofile('E:/Desktop/python perso/Blocks/gif_save/movie.mp4')
    jpg_dir='E:/Desktop/python perso/Blocks/gif_images/'
    print("Deleting image files")
    for filename in os.listdir(jpg_dir):
      file_path = os.path.join(jpg_dir, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
          elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
      except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == '__main__':    
    compute_position(30)