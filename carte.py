#carte de controle par mesures
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#les fonctions
st.set_page_config(page_title='Carte de  contrôle')
st.title('Carte de  contrôle')
def saisie(j,n):#j:nombre de jour n:prelevement chaque jour
    l=[]
    R=[]
    Xmoy=[]
    Rmoy=0
    Xdouble_bar=0
    for i in range (1,j+1):
        ox=[]
        s=0
        for k in range(1,n+1):
            x=st.text_input(f'donner la valeur du {k}  prelevement du {i} échantillon:')
            try:
                x=float(x)
            except ValueError:
                x=0
            ox.append(x)
            s+=x
        if len(ox)!=0:
            R.append(max(ox)-min(ox))
        if n!=0:
            Xmoy.append(s/n)
        l.append(ox)
    if len(R)!=0:
        Rmoy=sum(R)/len(R)
    if len(Xmoy)!=0:
        Xdouble_bar=sum(Xmoy)/len(Xmoy)
    
    return l,Xmoy,R,Rmoy,Xdouble_bar #extraire une liste sous la forme des listes de : [les valeurs de chaque jour ]
                                        #liste des XMOY 
                                        #LISTE DES R        RMOY X DOUBLE BAR
def tolerance():
    col1, col2 = st.columns(2)
    Lmax = col1.text_input('Donnez la limite supérieure')
    #Lmax=st.text_input('donnez la limite supérieure')
    try:
        Lmax=float(Lmax)
    except ValueError:
        Lmax=0
    #Lmin=st.text_input('donnez la limite inférieure')   
    Lmin = col2.text_input('Donnez la limite inférieure')   
    try:
        Lmin=float(Lmin)
    except ValueError:
        Lmin=0  
    return Lmax,Lmin 
                                                                                                                   
def table(x):#x est le tuple l output de la fonction saisie
    df=pd.DataFrame()
    if x[4]!=0:
        for i in range (len(x[0])):
            df1=pd.DataFrame(x[0][i])
            df2=pd.DataFrame([x[1][i]])
            df3=pd.DataFrame([x[2][i]])
            temp_df=pd.concat([df1,df2,df3],axis=1,ignore_index=True)
            df=pd.concat([df,temp_df],axis=0,ignore_index=True)
        df4=pd.DataFrame([x[3]])
        df5=pd.DataFrame([x[4]])
        df=pd.concat([df,df4,df5],axis=1,ignore_index=True)
        df.columns = ['valeur', 'Xmoy', 'R etendue','Rmoy','Xdouble_bar' ]# définir les titres des  colonnes 
        df['Jour'] = df.groupby (df.index // len(x[0][0] )).ngroup() + 1 #
        df.set_index('Jour', inplace=True)
    df.fillna('', inplace=True)#remplacer le terme NAN par un espace
    return df

#tracage d une carte de controle avec les limites de controles et de serveillances
# x :l,Xmoy,R,Rmoy,Xdouble_bar
def tracage_moy(x,n):
    A=[1.88,1.02,0.73,0.58,0.48,0.42,0.37,0.34,0.31]
    X=x[4]#Xdouble bar
    R=x[3]#Rmoy
    LCSX=X+A[n-2]*R
    LCIX=X-A[n-2]*R
    LSSX=X+((2/3)*A[n-1]*R)
    LSIX=X-((2/3)*A[n-1]*R)
    y=x[1]#Xmoy
    for w in range(3):#chaque fois nous allons afficher 1/carte de controle brut apres carte de controle avec analyse
        plt.figure()
        plt.plot([i for i in range(1,len(y)+1)],y,marker='o',color='black')# tracage x y marker pour les points 
        plt.xticks(range(1, len(y) + 1))#axe x que des entiers
        plt.axhline(X, color='g', linewidth=1.5)#LC
        plt.text(j, X,'LC', color='g', va='bottom')
            #les limites de controles et de serveillance
        plt.axhline(LCSX, color='red', linestyle='--', linewidth=1.5)
        plt.axhline(y=LCIX, color='red', linestyle='--', linewidth=1.5)
        plt.axhline(y=LSSX, color='blue', linestyle='--', linewidth=1.5)
        plt.axhline(y=LSIX, color='blue', linestyle='--', linewidth=1.5)
        #le legende des limites
        plt.text(j, LCSX,'LCS', color='black', va='bottom')
        plt.text(j, LCIX,'LCI', color='black', va='bottom')
        plt.text(j, LSSX,'LSS', color='black', va='bottom')
        plt.text(j, LSIX,'LSI', color='black', va='bottom')
        #les titres des axes
        plt.title('Carte X-barre')
        plt.xlabel('Échantillon')
        plt.ylabel('Valeur')
        #partie d interpretation liste Xmoy=y
        if w==0:
            st.header('Carte X bar:')
            st.pyplot(plt)#1 er affichage
            st.header('Analyse de la carte :')
            prob=0
            legen=[]
            #point hors limite
            for i in range(len(y)):
                if (LCSX<y[i] or y[i]<LCIX):
                    plt.scatter(i+1, y[i], s=180, color='red', linewidths=2)
                    prob+=1
                    plt.text(i+1 + 0.2, y[i] + 0.2, prob, fontsize=10, color='blue')
                    p=str(prob)+' :point hors limite,Régler le processus'
                    legen.append(p)
            plt.legend(legen, loc='best',bbox_to_anchor=(0.5, -0.1))
                    #plt.text(0,LCIX-2*prob-1,str(prob)+' :point hors limite,Régler le processus')
            if prob!=0:
                st.subheader('Détection des points hors limites:')
                st.pyplot(plt)
        #7points consécutifs superieurs ou inférieurs a la lc
        elif w==1:
            prob=0
            indice1=['supérieur']
            indice2=["inférieur"]
            legen=[]
            for i in range(len(y)):#indice des point superieur ou inferieur a lc
                if X<y[i]:
                    indice1.append(i)
                elif y[i]<X:
                    indice2.append(i)
            for indice in [indice1,indice2]:
                b=indice[0]
                indice.pop(0)
                (q,r)=divmod(len(indice),7)
                for h in range(q):
                    liste=indice[7*h:7*(h+1)]
                    ox=[j for j in range(liste[0],liste[0]+7)]
                    if liste==ox:
                        prob+=1            
                        for a in range(ox[0],ox[0]+7): 
                            plt.scatter(a+1, y[a], s=100, color='orange', linewidths=2)
                        plt.text(a-3+0.2, y[a] + 0.2, prob, fontsize=10, color='red')
                        p=str(prob)+' :sept points consécutifs '+ b +' à la moyenne,régler le processus'
                        legen.append(p)
            plt.legend(legen, loc='best',bbox_to_anchor=(0.5, -0.1))
                        #plt.text(0,LCIX-2*prob-1,str(prob)+' :sept points consécutifs '+ b +' à la moyenne,régler le processus')
            if prob!=0:
                st.subheader('Tendence supérieure ou inférieure')
                st.pyplot(plt) 
        elif w==2:#dtection d une sequence croissante ou decroissant
            prob=0
            legen=[]
            for i in range(len(y)):
                if i+6<len(y):
                    l=y[i:i+7]
                    if l==sorted(l):
                        prob+=1
                        for a in range(i,i+7):     #de i jusqu a i+7 (exclu)                       #       pour ne repete pas une point
                            plt.scatter(a+1, y[a], s=100, color='orange', linewidths=2)
                        plt.text(a-3+0.2, y[a] + 0.2, prob, fontsize=10, color='red')
                        p=str(prob)+' :sept  point consécutifs sont en augmentation régulière'
                        legen.append(p)
                        #plt.text(0,LCIX-2*prob-1,str(prob)+' : 7 point consécutifs sont en augmentation régulière')
                    elif l==sorted(l,reverse=True):
                        prob+=1
                        for a in range(i,i+7):     #de i jusqu a i+7 (exclu)                       #       pour ne repete pas une point
                            plt.scatter(a+1, y[a], s=100, color='orange', linewidths=2)
                        plt.text(a-3+0.2, y[a-3] + 0.2, prob, fontsize=10, color='red')
                        p=str(prob)+' :sept  point consécutifs sont en diminution régulière'
                        legen.append(p)
            plt.legend(legen, loc='best',bbox_to_anchor=(0.5, -0.1))
                        #plt.text(0,LCIX-2*prob-1,str(prob)+' : 7 point consécutifs sont en diminution régulière')
            if prob!=0:
                st.subheader('Tendence croissante ou décroissante:')
                st.pyplot(plt) 
    return 0

def tracage_R(x,n):
    R=x[3]
    D4=[3.27,2.57,2.28,2.11,2,1.92,1.86,1.82,1.78]
    D3=[0,0,0,0,0,0.076,0.136,0.184,0.223]
    LCSR=D4[n-2]*R
    LCIR=D3[n-2]*R
    y=x[2]
    for w in range(3):
        plt.figure()
        plt.plot([i for i in range(1,len(y)+1)],y,marker='o',color='black')#marker pour les points 
        plt.axhline(R, color='g', linewidth=1.5)
        plt.text(j, R,'LC', color='g', va='bottom')
        plt.axhline(LCSR, color='red', linestyle='--', linewidth=1.5)
        plt.axhline(LCIR, color='red', linestyle='--', linewidth=1.5)
        plt.xticks(range(1, len(y) + 1))
        plt.text(j, LCSR,'LCS', color='black', va='bottom')
        plt.text(j, LCIR,'LCI', color='black', va='bottom')
        plt.title('Carte R')
        plt.xlabel('Échantillon')
        plt.ylabel('Valeur')
        if w==0:
            st.header('Carte des étendues:')
            st.pyplot(plt)#1 er affichage
            st.header('Analyse de la carte :')
            prob=0
            legen=[]
            #point hors limite
            for i in range(len(y)):
                if LCSR<y[i] :
                    plt.scatter(i+1, y[i], s=180, color='red', linewidths=2)
                    prob+=1
                    plt.text(i+1 + 0.2, y[i] + 0.2, prob, fontsize=10, color='blue')
                    p=str(prob)+' :point hors limite,La capabilité court terme se détériore. Il faut trouver l origine de cette détérioration et intervenir'
                    legen.append(p)
                elif y[i]<LCIR:
                    plt.scatter(i+1, y[i], s=180, color='red', linewidths=2)
                    prob+=1
                    plt.text(i+1 + 0.2, y[i] + 0.2, prob, fontsize=10, color='blue')
                    p=str(prob)+' :point hors limite,La capabilité court terme s améliore, système de mesure est bloqué'
                    legen.append(p)
            plt.legend(legen, loc='best',bbox_to_anchor=(0.5, -0.1))  
            if prob!=0:
                st.subheader('Détection des points hors limites:')
                st.pyplot(plt)
        #7points consécutifs superieurs ou inférieurs a la lc
        elif w==1:
            legen=[]
            prob=0
            indice1=['supérieur','La capabilité court terme se détériore. Il faut trouver l origine de cette détérioration et intervenir']
            indice2=['inférieur','La capabilité court terme s améliore. Il faut trouver l origine de cette amélioration pour la maintenir']
            for i in range(len(y)):#indice des point superieur ou inferieur a lc
                if R<y[i]:
                    indice1.append(i)
                elif y[i]<R:
                    indice2.append(i)
            for indice in [indice1,indice2]:
                b=indice[0]
                c=indice[1]
                indice.pop(0)
                indice.pop(0)
                (q,r)=divmod(len(indice),7)
                h=0
                while h <=q:
                    liste=indice[7*h:7*(h+1)]
                    ox=[j for j in range(liste[0],liste[0]+7)]
                    if liste==ox:
                        prob+=1            
                        for a in range(ox[0],ox[0]+7): 
                            plt.scatter(a+1, y[a], s=100, color='orange', linewidths=2)
                        plt.text(a-3+0.2, y[a] + 0.2, prob, fontsize=10, color='red')
                        p=str(prob)+' :sept points consécutifs '+ b +' à la moyenne'+c
                        legen.append(p)
                        h+=1
                    else:
                        for m in range(7):
                            liste=indice[7*h+m+1:7*(h+1)+m+1]
                            ox=[j for j in range(liste[0],liste[0]+7)]
                            if liste==ox:
                                prob+=1            
                                for a in range(ox[0],ox[0]+7): 
                                    plt.scatter(a+1, y[a], s=100, color='orange', linewidths=2)
                                h+=1
                                plt.text(a-3+0.2, y[a] + 0.2, prob, fontsize=10, color='red')
                                p=str(prob)+' :sept points consécutifs '+ b +' à la moyenne'+c
                                legen.append(p)
                            
                        
            plt.legend(legen, loc='best',bbox_to_anchor=(0.5, -0.1))
            if prob!=0:
                st.subheader('Tendence supérieure ou inférieure')
                st.pyplot(plt) 
        elif w==2:#dtection d une sequence croissante ou decroissant
            prob=0
            legen=[]
            for i in range(len(y)):
                if i+7<len(y):
                    l=y[i:i+7]
                    if l==sorted(l):
                        prob+=1
                        for a in range(i,i+7):     #de i jusqu a i+7 (exclu)                       #       pour ne repete pas une point
                            plt.scatter(a+1, y[a], s=100, color='orange', linewidths=2)
                        plt.text(a-3+0.2, y[a] + 0.2, prob, fontsize=10, color='red')
                        p=str(prob)+' : sept point consécutifs sont en augmentation régulière, La capabilité court terme se détériore. Il faut trouver l origine decette détérioration et intervenir.'
                        legen.append(p)
                    elif l==sorted(l,reverse=True):
                        prob+=1
                        for a in range(i,i+7):     #de i jusqu a i+7 (exclu)                       #       pour ne repete pas une point
                            plt.scatter(a+1, y[a], s=100, color='orange', linewidths=2)
                        plt.text(a-3+0.2, y[a] + 0.2, prob, fontsize=10, color='red')
                        p=str(prob)+' : sept point consécutifs sont en  diminution régulière, La capabilité court terme  s améliore.  Il faut trouver l origine decette amélioration pour la maintenir.'
                        legen.append(p)
            plt.legend(legen, loc='best',bbox_to_anchor=(0.5, -0.1))
            if prob!=0:
                st.subheader('Tendence croissante ou décroissante:')
                st.pyplot(plt) 
    return 0

def interp(x,a):
    if (x<1):
        rep='Pas capable probleme de '+ a
    elif (1<=x<1.33):
        rep='Juste capable'
    elif (1.33<=x<1.66):
        rep='acceptable'
    elif (1.66<=x):
        rep='Trés capable,performant'
    return rep
    
def capabilite(Lmax,Lmin,x):#cp,pp,cpk,ppk
    d2=[1.128,1.693,2.059,2.326,2.534,2.704,2.847,2.847,2.970]
    sigmaLT=np.std(x[1])#std:standard deviation ecart type
    sigmaCT=x[3]/d2[n-2]#Rmoy/d2
    #calcul
    IT=Lmax-Lmin
    cp=IT/(6*sigmaCT)
    pp=IT/(6*sigmaLT)
    cpk=min(((x[4]-Lmin)/(3*sigmaCT)),((Lmax-x[4])/(3*sigmaCT)))
    ppk=min(((x[4]-Lmin)/(3*sigmaLT)),((Lmax-x[4])/(3*sigmaLT)))
    #affichage long terme 
    st.header('Cpabilité long terme')
    df=pd.DataFrame([[pp],[ppk]])
    df1=pd.DataFrame([interp(pp,'dispersion'),interp(ppk,'centrage')])
    df=pd.concat([df,df1],axis=1,ignore_index=True)
    df.columns=['valeur','interprétation']
    df.index=['pp','ppk']
    st.write(df)
    #affichage court terme 
    st.header('Cpabilité court terme')
    df=pd.DataFrame([[cp],[cpk]])
    df1=pd.DataFrame([interp(cp,'dispersion'),interp(cpk,'centrage')])
    df=pd.concat([df,df1],axis=1,ignore_index=True)
    df.columns=['valeur','interprétation']
    df.index=['cp','cpk']
    st.write(df)
    return 0
#programme principale
col1,col2=st.columns(2)
j = col1.number_input('Donnez le nombre d échantillon', min_value=0, step=1)
n = col2.number_input('Donnez le taille  échantillon',min_value=0, step=1)
l=tolerance()
Lmax=l[0]
Lmin=l[1]
x=saisie(int(j),int(n))
df=table(x)
st.write(df)
if x[4]!=0:
    tracage_moy(x,n)
    tracage_R(x,n)
    capabilite(Lmax,Lmin,x)


            
             
    
    
