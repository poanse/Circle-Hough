import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import fileinput
import seaborn as sns

sns.set(style = 'whitegrid')#, rc = {'axes.labelsize': 16})

size_var=20 #font size
diameter_nm=[]
l = os.listdir('.')
temp_list=[]
for f in l:
	if (f[-3:] == 'TXT') or (f[-3:] == 'txt') and (f[:3] == 'TXT') or (f[:3] == 'txt'):
		temp_list.append(f)

with open('merged.txt', 'w') as fout:
    fin = fileinput.input(temp_list)
    for line in fin:
        fout.write(line)
        diameter_nm.append(float(line))
    fin.close()
#histogram plotting
diameter_nm = np.array(diameter_nm)
#fig, ax = plt.subplots(1, 1)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)

ax.set_ylabel("Amount of particles",fontsize=size_var)
ax.set_xlabel("Particle diameter, nm",fontsize=size_var)

xmax = round(max(diameter_nm)*2,-3)
bins = np.arange(0, xmax, 500)
plt.xticks(np.arange(0, xmax, 2000), fontsize = size_var-2)
plt.yticks(fontsize = size_var)

ax.hist(diameter_nm, #bins = int(np.power(len(radia_nm),0.333)))
        bins = bins)
mean = np.mean(diameter_nm)
std = np.std(diameter_nm)
ax.text(0.85, 0.85,
        'mean D = '+str(int(mean))+' nm\n'
        +'std = '+str(int(std))+' nm'+'\n'
        +'rel. std = '+str(round(100*std/mean,1))+' %',
        ha='center', va='center', transform=ax.transAxes,size=size_var)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('merged_hist.png')
#plt.show()
plt.close()
