#coding:utf-8
# terminal command: python ua.py data.json(dataname)
from sys import argv
import json,csv
import numpy as np
import matplotlib.pyplot as plt

def help():
    '''help message'''
    print ""
    print "Usage: %s [input_file]" %argv[0]
    print ""
    print "This command eliminates something... in the input file."
    sys.exit(1)

def jsonanalysis(anInputFile):

    with open(anInputFile, "r") as JsonFile:
        jsonData = json.load(JsonFile)
        enc = json.dumps(jsonData, sort_keys=True, indent=4)
        dec = json.loads(enc)
        
        timeList = []
        xList = []
        yList = []
        zList = []
        
        for i in range(0,len(dec)):
            timeList.append(jsonData[i]["time"])
            xList.append(float(unicode(jsonData[i]["x"])))
            yList.append(float(unicode(jsonData[i]["y"])))
            zList.append(float(unicode(jsonData[i]["z"])))
                
        def summaryfunction(List):
            Array = np.array(List)
            max = Array.max()
            min = Array.min()
            mean = Array.mean()
            std = Array.std()
            return max,min,mean,std

        def curvefunction(List1,List2):
            x=List1
            y=List2
            plt.figure(1)
            plt.plot(x,y)
            plt.title("time-xyz curve",fontsize=16)
            plt.xlabel("time",fontsize=14)
            plt.ylabel("xyz",fontsize=14)
            plt.xticks(fontsize=12)
            plt.xticks(fontsize=12)
            plt.legend(("x","y","z"),loc='best',fontsize=14)

        curvefunction(timeList,xList)
        curvefunction(timeList,yList)
        curvefunction(timeList,zList)

        def histgramfunction(List,title,max,min,mean,std):
            plt.hist(List,facecolor='g', alpha=0.8)
            plt.title(title, size=16)
            plt.xlabel('Score', size=14)
            plt.ylabel('Frequency', size=14)
            plt.grid(True)
            plt.text(mean, 100,r'''
                $mean=%.1f$
                $std=%.2f$
                $min=%.3f$
                $max=%.4f$
                ''' % (mean,std,min,max),va="center",ha="center",fontsize=14)
            plt.axvline(x=mean, linewidth=1, color='r')

        plt.figure(2)
        histgramfunction(xList,'Histogram x',summaryfunction(xList)[0],summaryfunction(xList)[1],summaryfunction(xList)[2],summaryfunction(xList)[3])
        plt.figure(3)
        histgramfunction(yList,'Histogram y',summaryfunction(yList)[0],summaryfunction(yList)[1],summaryfunction(yList)[2],summaryfunction(yList)[3])
        plt.figure(4)
        histgramfunction(zList,'Histogram z',summaryfunction(zList)[0],summaryfunction(zList)[1],summaryfunction(zList)[2],summaryfunction(zList)[3])
        
        def pcafunction(List1,List2,List3):
            from sklearn.decomposition import PCA
            import pylab as pl
            
            pcadataList = []
            
            pcadataList.append(List1)
            pcadataList.append(List2)
            pcadataList.append(List3)
            
            pcaCountList = []
            
            pcaCountList.append(0)
            pcaCountList.append(1)
            pcaCountList.append(2)
            
            pcaCountArray = np.array(pcaCountList)
            
            pcaNameList = []
            
            pcaNameList.append('x')
            pcaNameList.append('y')
            pcaNameList.append('z')
            
            '''
            for i in range(0,len(List1)):
                data = [List1[i],List2[i],List3[i]]
                pcadataList.append(data)
            #print pcadataList
            '''
            
            pcadataArray = np.array(pcadataList)
            pca = PCA(n_components=2)
            X = pca.fit(pcadataArray).transform(pcadataArray)
            
            print X

            print('explained variance ratio (first two components): %s'
                  % str(pca.explained_variance_ratio_))
            
            plt.plot(X[pcaCountArray == 0, 0], X[pcaCountArray == 0, 1], 'or',
                     X[pcaCountArray == 1, 0], X[pcaCountArray == 1, 1], '^b',
                     X[pcaCountArray == 2, 0], X[pcaCountArray == 2, 1], 'sg'
                     )
            plt.xlabel('explained variance ratio: ' + str(pca.explained_variance_ratio_[0]),fontsize=14)
            plt.ylabel('explained variance ratio: ' + str(pca.explained_variance_ratio_[1]),fontsize=14)
            plt.legend((str(pcaNameList[0]),str(pcaNameList[1]),str(pcaNameList[2])),loc='best',fontsize=14)
            plt.title('PCA',fontsize=16)
        
        plt.figure(5)
        pcafunction(xList,yList,zList)
        
        plt.show()


if __name__=='__main__':
    if len(argv)!=2:
        help()
    jsonanalysis(argv[1])