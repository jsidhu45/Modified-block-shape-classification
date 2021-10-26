from tkinter import *
from tkinter.filedialog import askopenfile
#from PIL import Image, ImageTk
root = Tk()

root.title("MBSCT")

root.geometry('+%d+%d'%(1250,10))

header = Frame(root,width=700, height= 150, bg="LightSalmon")
header.grid(columnspan=4, rowspan=2, row=0)

middle = Frame(root,width=700, height= 50)
middle.grid(columnspan=4, rowspan=1, row=1)

lower = Frame(root,width=700, height= 50)
lower.grid(columnspan=4, rowspan=1, row=2)

Label(root, text="Modified Block Shape Classification Tool",bg="white", font=("Comic Sans MS", 15, "bold")).grid(rowspan=1,columnspan=4, row=0)

def open_file():
	browse_text.set("loading...")
	file = askopenfile(parent=root, mode ='rb', filetypes=[('Excel', ('*.xls', '*.xlsx'))])
	if file:
				
		global data
		data=pd.read_excel(file, sheet_name='Sheet1')
		data.drop_duplicates(ignore_index=True, inplace=True)
		global area
		area=pd.read_excel(file, sheet_name='Sheet3')
		global volume
		volume=pd.read_excel(file, sheet_name='Sheet2')
		
		browse_text.set("Browse data file")		

import pandas as pd
import numpy as np

def funct():
    #import pandas as pd
    #import numpy as np
    #data=pd.read_excel(file, sheet_name='Sheet1')
    #data.drop_duplicates(ignore_index=True, inplace=True)

    #Button(root, text="Finished", font=("Raleway",12), bg="PaleVioletRed", fg="white", height=1, width=15).grid(row=2,column=2)
  
    uni=[i for i in data['Block']]
    uni=np.array(uni)
    uni=np.unique(uni)
    blk=uni

    def elongation_index():
        uni=[i for i in data['Block']]
        uni=np.array(uni)
        uni=np.unique(uni)
        fn = pd.DataFrame()
        for u in uni:
            d=data.groupby(data.Block)
            g=d.get_group(u)
            g3=d.get_group(u)
            g=g.to_numpy()
            n=0
            r1=[i for i in range(len(g))]
            ary_vec=[]
            for i in r1:
                n=n+1
                r2=[i for i in r1[n:]]
                for j in r2:

                    x=g[i]-g[j]
                    ary_vec.append(x)
            length=[np.linalg.norm(i) for i in ary_vec]  		#length of all chords
            med=np.median(length)
            max=np.max(length)					#max length chord
            index=length.index(max)
            l1=[i for i in range(len(g))]
            l1=sorted(l1, reverse=True)
            l1=l1[:-1]
            n1=0
            m1=0
            for i in l1:
                if m1<=index:
                    n1=n1+1
                    m1=m1+i
            sum=0
            for i in range(n1-1):
                sum=sum+l1[i]
            n2=n1-1								#max length chord vertex1
            n3=(index+1)-sum
            n4=n3+n2							#max length chord vertex2
            l_chrd_vec = np.array(g[n4] - g[n2])				#longest chord vector
            chords=[]
            l_chord=[]
            for i in range(len(g)):
                chrd=g[n4]-g[i]									
                l_chord1=np.linalg.norm(chrd)  
                chords.append(chrd)
                l_chord.append(l_chord1)
            df_chords=pd.DataFrame(chords)					#all chords passing through max length chord vertex2 (n4)
				
				
            df_chords['lng']=l_chord
            df_chords['Block']=u
            df11=df_chords[df_chords['lng']>=med]				#Chords greater than median chord length
				
            df11.reset_index(inplace=True)
            del df11['index']
            del df11['lng']
            del df11['Block']
            df11_np=df11.to_numpy()						#all chords greater than median chord length and passing though max_length_chord vertex (n4)	
		
            if len(df11_np)<=1:
                continue					

            k=0
            w1=[]
            r=range(len(df11_np))
            for i in r:
                k=k+1
                r1= [j for j in r[k:]]
                for j in r1:
                    w=np.dot(df11_np[i],df11_np[j])/(np.linalg.norm(df11_np[i])*np.linalg.norm(df11_np[j]))
                    w1.append(w)
			  	
            w1 =[ i**2 for i in w1]
		
            #area=pd.read_excel('elong.xlsx', sheet_name='Sheet3')
            d=area.groupby(area.Block)
            d=d.get_group(u)
            surf_area=np.sum(d['Area'])
            #volume=pd.read_excel('elong.xlsx', sheet_name='Sheet2')
            d=volume.groupby(volume.Block)
            d=d.get_group(u)
            vol=d.iloc[0]['Volume']
            avg_cod_lng=np.average(length)

            alpha= (surf_area*avg_cod_lng)/(7.7*vol)
            elong= np.min(w1)
            l=[u,max, np.min(w1), elong, alpha, vol]
            df=pd.DataFrame(l).T
            fn=fn.append(df, ignore_index=True)
		
        fn.rename(columns ={0:'Block', 1: 'Max', 2: 'Width', 3:'Elong_index', 4:'alpha', 5:'vol'}, inplace=True)
        return fn		

    def elongation_index1():
        uni=[i for i in data['Block']]
        uni=np.array(uni)
        uni=np.unique(uni)
        fn = pd.DataFrame()
        for u in uni:
            d=data.groupby(data.Block)
            g=d.get_group(u)
            g3=d.get_group(u)
            g=g.to_numpy()
            n=0
            r1=[i for i in range(len(g))]
            ary_vec=[]
            for i in r1:
                n=n+1
                r2=[i for i in r1[n:]]
                for j in r2:

                    x=g[i]-g[j]
                    ary_vec.append(x)
            length=[np.linalg.norm(i) for i in ary_vec]  		#length of all chords
            med=np.median(length)
            max=np.max(length)					#max length chord
            index=length.index(max)
            l1=[i for i in range(len(g))]
            l1=sorted(l1, reverse=True)
            l1=l1[:-1]
            n1=0
            m1=0
            for i in l1:
                if m1<=index:
                    n1=n1+1
                    m1=m1+i
            sum=0
            for i in range(n1-1):
                sum=sum+l1[i]
            n2=n1-1								#max length chord vertex1
            n3=(index+1)-sum
            n4=n3+n2							#max length chord vertex2
            l_chrd_vec = np.array(g[n2] - g[n4])				#longest chord vector
            chords=[]
            l_chord=[]
            for i in range(len(g)):
                chrd=g[n2]-g[i]									
                l_chord1=np.linalg.norm(chrd)  
                chords.append(chrd)
                l_chord.append(l_chord1)
            df_chords=pd.DataFrame(chords)					#all chords passing through max length chord vertex2 (n2)
				
				
            df_chords['lng']=l_chord
            df_chords['Block']=u
            df11=df_chords[df_chords['lng']>=med]				#Chords greater than median chord length
				
            df11.reset_index(inplace=True)
            del df11['index']
            del df11['lng']
            del df11['Block']
            df11_np=df11.to_numpy()						#all chords greater than median chord length and passing though max_length_chord vertex (n2)	
            if len(df11_np)<=1:
                continue					

            k=0
            w1=[]
            r=range(len(df11_np))
            for i in r:
                k=k+1
                r1= [j for j in r[k:]]
                for j in r1:
                    w=np.dot(df11_np[i],df11_np[j])/(np.linalg.norm(df11_np[i])*np.linalg.norm(df11_np[j]))
                    w1.append(w)
			  	
		
            w1 =[ i**2 for i in w1]
            #area=pd.read_excel('elong.xlsx', sheet_name='Sheet3')
            d=area.groupby(area.Block)
            d=d.get_group(u)
            surf_area=np.sum(d['Area'])
            #volume=pd.read_excel('elong.xlsx', sheet_name='Sheet2')
            d=volume.groupby(volume.Block)
            d=d.get_group(u)
            vol=d.iloc[0]['Volume']
            avg_cod_lng=np.average(length)

            alpha= (surf_area*avg_cod_lng)/(7.7*vol)
            elong= np.min(w1)
            l=[u,max, np.min(w1), elong, alpha, vol]
            df=pd.DataFrame(l).T
            fn=fn.append(df, ignore_index=True)
		
        fn.rename(columns ={0:'Block', 1: 'Max', 2: 'Width', 3:'Elong_index', 4:'alpha', 5:'vol'}, inplace=True)
        return fn

    elng=elongation_index()
    l_elng=elng['Elong_index'].to_list()
    l_block= elng['Block'].to_list()
    l_alpha= elng['alpha'].to_list()
    l_vol=elng['vol'].to_list()

    elng1=elongation_index1()
    l_elng1=elng1['Elong_index'].to_list()
    l_block1= elng1['Block'].to_list()
    l_alpha1= elng1['alpha'].to_list()
    l_vol1=elng1['vol'].to_list()


    df=pd.DataFrame(l_elng, index=l_block)
    df[1]=l_alpha
    df[2]=l_vol

    df1=pd.DataFrame(l_elng1, index=l_block1)
    df1[1]=l_alpha1
    df1[2]=l_vol1

    df_i=df.index.to_list()
    df1_i=df1.index.to_list()
    l=[]

    for i in blk:
        if i in df_i:
            if i in df1_i:
                l.append(i)
    l1=[]
    for i in blk:
        if i not in l:
            l1.append(i)

    l2=[]
    block=[]
    alpha=[]
    vol=[]
    for u in l:
        m= (df.loc[u][0]*df1.loc[u][0])*2/(df.loc[u][0] + df1.loc[u][0])
        l2.append(m)
        block.append(u)
        alpha.append(df.loc[u][1])
        vol.append(df.loc[u][2])
    for u in l1:
        if u in df_i:
            l2.append(df.loc[u][0])
            block.append(u)
            alpha.append(df.loc[u][1])
            vol.append(df.loc[u][2])
        else:
            l2.append(df1.loc[u][0])
            block.append(u)
            alpha.append(df1.loc[u][1])
            vol.append(df1.loc[u][2])

    l_alpha1=[]
    for i in alpha:
        if i>10:
            l_alpha1.append(10)
        else:
            l_alpha1.append(i)

    global df_final	
    df_final=pd.DataFrame(block)	
    df_final['Beta']= l2
    df_final['Alpha']= l_alpha1
    df_final['Volume']=vol
    df_final.rename(columns ={0:'Block'}, inplace=True)
    df_final.to_excel('MBSC.xlsx')
    
def Tri_plot():
	import matplotlib.pyplot as plt
	plt.figure()
	plt.plot([-0.5,0.5],[0,0], 'k-', linewidth=0.5)
	plt.plot([-0.5,0],[0,0.8660], 'k-', linewidth=0.5)
	plt.plot([0.5,0],[0,0.8660], 'k-', linewidth=0.5)
	plt.plot([-0.35,0.35],[0.259807621,0.259807621], 'k-', linewidth=0.5)
	plt.plot([-0.125,0.125],[0.64952,0.64952], 'k-', linewidth=0.5)
	plt.plot([-0.125,0.125],[0.64952,0.64952], 'k-', linewidth=0.5)
	plt.plot([-0.016015122,-0.005719686],[0.259807621,0.649519053], 'k-', linewidth=0.5)
	plt.plot([-0.198970004,-0.139279003],[0,0.25981], 'k-', linewidth=0.5)
	plt.plot([0.198970004,0.139279003],[0,0.25981], 'k-', linewidth=0.5)

	plt.text(-0.02,0.70776, 'E', color='black', fontsize=15, fontweight='bold')
	plt.text(-0.15,0.454629042, 'CE', color='black', fontsize=15, fontweight='bold')
	plt.text(0.08,0.454629042, 'EP', color='black', fontsize=15, fontweight='bold')
	plt.text(-0.33,0.129905, 'C', color='black', fontsize=15, fontweight='bold')
	plt.text(0,0.129905, 'PC', color='black', fontsize=15, fontweight='bold')
	plt.text(0.27,0.129905, 'P', color='black', fontsize=15, fontweight='bold')

	plt.text(-0.3,0.454629042, '\u03B2', color='black', fontsize=15)
	plt.text(-0.02,-0.08, '\u03B1', color='black', fontsize=15)

	plt.text(-0.55,0, '0', color='black', fontsize=13)
	plt.text(-0.44,0.25981, '0.3', color='black', fontsize=13)
	plt.text(-0.25,0.64952, '0.75', color='black', fontsize=13)
	plt.text(-0.1,0.8620, '1.0', color='black', fontsize=13)

	plt.text(-0.52,-0.08, '1', color='black', fontsize=13)
	plt.text(-0.208970004,-0.08, '2', color='black', fontsize=13)
	plt.text(0.188970004,-0.08, '5', color='black', fontsize=13)
	plt.text(0.48,-0.08, '10', color='black', fontsize=13)

	alpha = []
	for i in df_final['Alpha']:
		if i < 1.0:
			alpha.append(1.0)
		elif i > 10.0:
			alpha.append(10.0)
		else:
			alpha.append(i)

	y1 = (df_final['Beta'])*np.sin(np.deg2rad(60))
	x1 = ((np.sin(np.deg2rad(60)) - y1)/(np.sin(np.deg2rad(60))))*(np.log10(alpha)-0.5)

	plt.scatter(x1,y1,s=4, marker='o', c='red')
	plt.axis('off')
	plt.show()

def pie_plot():
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt

	data1=df_final
	n=len(data1)

	df_vol=data1.sort_values('Volume')

	df=df_vol['Volume']
	df=df.reset_index()
	del df['index']
	index = df. index
	index = [(i/n)*100 for i in index]



	d20=np.interp(20, index,df['Volume'])
	d40=np.interp(40, index,df['Volume'])
	d60=np.interp(60, index,df['Volume'])
	d80=np.interp(80, index,df['Volume'])


	df_d20=df_vol[df_vol['Volume']<=d20]

	df_d2040=df_vol[df_vol['Volume']<=d40]
	df_d2040=df_d2040[df_d2040['Volume']>d20]

	df_d4060=df_vol[df_vol['Volume']<=d60]
	df_d4060=df_d4060[df_d4060['Volume']>d40]

	df_d6080=df_vol[df_vol['Volume']<=d80]
	df_d6080=df_d6080[df_d6080['Volume']>d60]

	df_d80=df_vol[df_vol['Volume']>d80]



	l=[df_d20,df_d2040,df_d4060,df_d6080, df_d80]


	d=[]
	k=[3]

	for i in range(len(l)):
	
		E = l[i][l[i]['Beta']>0.75]
		d.append(len(E))	

		CP_E1 = l[i][l[i]['Beta']<=0.75]
		CP_E = CP_E1[CP_E1['Beta']>0.3]
		CE = CP_E[CP_E['Alpha']<=3.0]
		EP = CP_E[CP_E['Alpha']>3.0]
		d.append(len(CE))
		d.append(len(EP))


		C_PC_P = l[i][l[i]['Beta']<=0.3]
		C = C_PC_P[C_PC_P['Alpha']<=2.0]
		PC = C_PC_P[C_PC_P['Alpha']<=5.0]
		PC = PC[PC['Alpha']>2.0]
		P = C_PC_P[C_PC_P['Alpha']>5.0]
		d.append(len(C))
		d.append(len(PC))
		d.append(len(P))


	d20=d[0:6]
	d2040=d[6:12]
	d4060=d[12:18]
	d6080=d[18:24]
	d80=d[24:30]

	e = np.sum([d20[0],d2040[0],d4060[0],d6080[0],d80[0]])
	ce = np.sum([d20[1],d2040[1],d4060[1],d6080[1],d80[1]])
	ep = np.sum([d20[2],d2040[2],d4060[2],d6080[2],d80[2]])
	c = np.sum([d20[3],d2040[3],d4060[3],d6080[3],d80[3]])
	cp = np.sum([d20[4],d2040[4],d4060[4],d6080[4],d80[4]])
	p = np.sum([d20[5],d2040[5],d4060[5],d6080[5],d80[5]])

	pie = np.array([e,ce,ep,c,cp,p])
	mylabels = ["E", "CE", "EP", "C", "CP", "P"]
	plt.pie(pie, labels = mylabels, autopct='%.2f')
	plt.legend()
	plt.show() 

def BVD():
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt

	data1=df_final
	n=len(data1)

	df_vol=data1.sort_values('Volume')

	df=df_vol['Volume']
	df=df.reset_index()
	del df['index']
	index = df. index
	index = [(i/n)*100 for i in index]

	ax=plt.gca()
	ax.set_ylim([0,100])
	ax.yaxis.grid()
	plt.scatter(df['Volume'],index,s=10, marker='o', c='red')
	plt.xscale('log')

	d20=np.interp(20, index,df['Volume'])
	d40=np.interp(40, index,df['Volume'])
	d60=np.interp(60, index,df['Volume'])
	d80=np.interp(80, index,df['Volume'])


	plt.plot([d20,d20],[0,20],'k', linewidth=1.0)
	plt.plot([d40,d40],[0,40], 'k-', linewidth=1.0)
	plt.plot([d60,d60],[0,60], 'k-', linewidth=1.0)
	plt.plot([d80,d80],[0,80], 'k-', linewidth=1.0)

	plt.text(d20,15, '$d_{20}$', color='black', fontsize=15, fontweight='bold')
	plt.text(d40,35, '$d_{40}$', color='black', fontsize=15, fontweight='bold')
	plt.text(d60,55, '$d_{60}$', color='black', fontsize=15, fontweight='bold')
	plt.text(d80,75, '$d_{80}$', color='black', fontsize=15, fontweight='bold')
	plt.ylabel('% volume smaller than',fontsize=15 )
	plt.xlabel('volume (m$^3$)', fontsize=15)
	plt.show()

def bar_plot():
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt

	data1=df_final
	n=len(data1)

	df_vol=data1.sort_values('Volume')

	df=df_vol['Volume']
	df=df.reset_index()
	del df['index']
	index = df. index
	index = [(i/n)*100 for i in index]

	d20=np.interp(20, index,df['Volume'])
	d40=np.interp(40, index,df['Volume'])
	d60=np.interp(60, index,df['Volume'])
	d80=np.interp(80, index,df['Volume'])
	


	df_d20=df_vol[df_vol['Volume']<=d20]

	df_d2040=df_vol[df_vol['Volume']<=d40]
	df_d2040=df_d2040[df_d2040['Volume']>d20]

	df_d4060=df_vol[df_vol['Volume']<=d60]
	df_d4060=df_d4060[df_d4060['Volume']>d40]

	df_d6080=df_vol[df_vol['Volume']<=d80]
	df_d6080=df_d6080[df_d6080['Volume']>d60]

	df_d80=df_vol[df_vol['Volume']>d80]



	l=[df_d20,df_d2040,df_d4060,df_d6080, df_d80]


	d=[]
	k=[3]

	for i in range(len(l)):
	
		E = l[i][l[i]['Beta']>0.75]
		d.append(len(E))	

		CP_E1 = l[i][l[i]['Beta']<=0.75]
		CP_E = CP_E1[CP_E1['Beta']>0.3]
		CE = CP_E[CP_E['Alpha']<=3.0]
		EP = CP_E[CP_E['Alpha']>3.0]
		d.append(len(CE))
		d.append(len(EP))


		C_PC_P = l[i][l[i]['Beta']<=0.3]
		C = C_PC_P[C_PC_P['Alpha']<=2.0]
		PC = C_PC_P[C_PC_P['Alpha']<=5.0]
		PC = PC[PC['Alpha']>2.0]
		P = C_PC_P[C_PC_P['Alpha']>5.0]
		d.append(len(C))
		d.append(len(PC))
		d.append(len(P))


	d20=d[0:6]
	d2040=d[6:12]
	d4060=d[12:18]
	d6080=d[18:24]
	d80=d[24:30]


	w =0.1
	x = ["<D20","D20toD40","D40toD60","D60toD80", ">D80"]

	e = [d20[0],d2040[0],d4060[0],d6080[0],d80[0]]
	e = [(i/n)*100 for i in e]
	ce = [d20[1],d2040[1],d4060[1],d6080[1],d80[1]]
	ce = [(i/n)*100 for i in ce]
	ep = [d20[2],d2040[2],d4060[2],d6080[2],d80[2]]
	ep = [(i/n)*100 for i in ep]
	c = [d20[3],d2040[3],d4060[3],d6080[3],d80[3]]
	c = [(i/n)*100 for i in c]
	cp = [d20[4],d2040[4],d4060[4],d6080[4],d80[4]]
	cp = [(i/n)*100 for i in cp]
	p = [d20[5],d2040[5],d4060[5],d6080[5],d80[5]]
	p = [(i/n)*100 for i in p]



	bar1 = np.arange(len(x))
	bar2 = [i+w for i in bar1]
	bar3 = [i+w for i in bar2]
	bar4 = [i+w for i in bar3]
	bar5 = [i+w for i in bar4]
	bar6 = [i+w for i in bar5]

	plt.bar(bar1,e,w, label ='E')
	plt.bar(bar2,ce,w, label ='CE')
	plt.bar(bar3,ep,w, label ='EP')
	plt.bar(bar4,c,w, label ='C')
	plt.bar(bar5,cp,w, label ='CP')
	plt.bar(bar6,p,w, label ='P')

	plt.ylabel('% of total block')
	plt.xticks(bar1,x)
	plt.legend()
	plt.show()




Button(root, text="Triangular Diagram", command=Tri_plot, bg="SkyBlue1", height=1, width=15).grid(row=2,column=0)
Button(root, text="Bar Plot",command =bar_plot, bg="SkyBlue1", height=1, width=15).grid(row=2,column=1)
Button(root, text="Pie Chart", command=pie_plot, bg="SkyBlue1", height=1, width=15).grid(row=2,column=2)
Button(root, text="Volume Distribution", command = BVD, bg="SkyBlue1", height=1, width=15).grid(row=2,column=3)
Button(root, text="Execute", command=funct, font=("Raleway",12), bg="PaleVioletRed", fg="white", height=1, width=15).grid(row=1,column=2)

browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway",12), bg="#20bebe", fg="white", height=1, width=15).grid(row=1,column=1)
browse_text.set("Browse data file")

#browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway",12), bg="#20bebe", fg="white", height=1, width=15)
#browse_text.set("Browse data file")
#browse_btn.grid(rowspan=1, column=1, row=1, sticky=NE, padx=50)

#my_button = Button(root, text='Block Shape Press')
#my_button.pack()
root.mainloop()