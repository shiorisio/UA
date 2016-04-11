#coding:utf-8
# terminal command: python ua.py data.json(dataname) data2.json(dataname2)
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

def jsonanalysis(anInputFile,anInputCompFile):

    timeList = []
    xList = []
    yList = []
    zList = []

    with open(anInputFile, "r") as JsonFile:
        jsonData = json.load(JsonFile)
        enc = json.dumps(jsonData, sort_keys=True, indent=4)
        dec = json.loads(enc)
        
        for i in range(0,len(dec)):
            timeList.append(jsonData[i]["time"])
            xList.append(float(unicode(jsonData[i]["x"])))
            yList.append(float(unicode(jsonData[i]["y"])))
            zList.append(float(unicode(jsonData[i]["z"])))

    timeCompList = []
    xCompList = []
    yCompList = []
    zCompList = []

    with open(anInputCompFile, "r") as JsonCompFile:
        jsonCompData = json.load(JsonCompFile)
        encComp = json.dumps(jsonCompData, sort_keys=True, indent=4)
        decComp = json.loads(encComp)
        
        for i in range(0,len(decComp)):
            timeCompList.append(jsonCompData[i]["time"])
            xCompList.append(float(unicode(jsonCompData[i]["x"])))
            yCompList.append(float(unicode(jsonCompData[i]["y"])))
            zCompList.append(float(unicode(jsonCompData[i]["z"])))

    def summaryfunction(List):
        Array = np.array(List)
        max = Array.max()
        min = Array.min()
        mean = Array.mean()
        std = Array.std()
        return max,min,mean,std

    def curvefunction(List1,List2,dataname):
        x=List1
        y=List2
        plt.plot(x,y)
        plt.title("time-xyz curve("+dataname+")",fontsize=16)
        plt.xlabel("time",fontsize=14)
        plt.ylabel("xyz",fontsize=14)
        plt.xticks(fontsize=12)
        plt.xticks(fontsize=12)
        plt.legend(("x","y","z"),loc='best',fontsize=14)

    plt.figure(1)
    curvefunction(timeList,xList,'data1')
    curvefunction(timeList,yList,'data1')
    curvefunction(timeList,zList,'data1')
    
    plt.figure(2)
    curvefunction(timeCompList,xCompList,'data2')
    curvefunction(timeCompList,yCompList,'data2')
    curvefunction(timeCompList,zCompList,'data2')

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

    plt.figure(3)
    histgramfunction(xList,'Histogram x (data1)',summaryfunction(xList)[0],summaryfunction(xList)[1],summaryfunction(xList)[2],summaryfunction(xList)[3])
    plt.figure(4)
    histgramfunction(yList,'Histogram y (data1)',summaryfunction(yList)[0],summaryfunction(yList)[1],summaryfunction(yList)[2],summaryfunction(yList)[3])
    plt.figure(5)
    histgramfunction(zList,'Histogram z (data1)',summaryfunction(zList)[0],summaryfunction(zList)[1],summaryfunction(zList)[2],summaryfunction(zList)[3])
    
    plt.figure(6)
    histgramfunction(xCompList,'Histogram x (data2)',summaryfunction(xCompList)[0],summaryfunction(xCompList)[1],summaryfunction(xCompList)[2],summaryfunction(xCompList)[3])
    plt.figure(7)
    histgramfunction(yCompList,'Histogram y (data2)',summaryfunction(yCompList)[0],summaryfunction(yCompList)[1],summaryfunction(yCompList)[2],summaryfunction(yCompList)[3])
    plt.figure(8)
    histgramfunction(zCompList,'Histogram z (data2)',summaryfunction(zCompList)[0],summaryfunction(zCompList)[1],summaryfunction(zCompList)[2],summaryfunction(zCompList)[3])
    
    def prepcafunction(List1,List2,List3,List4,List5,List6):
    
        pcadataList = []
        pcaCountList = []
        pcaNameList = []
        
        for i in range(0,len(List1)):
            data = [List1[i],List2[i],List3[i]]
            pcadataList.append(data)
            pcaCountList.append(0)
            pcaNameList.append('data1')

        for i in range(0,len(List1)):
            data = [List4[i],List5[i],List6[i]]
            pcadataList.append(data)
            pcaCountList.append(1)
            pcaNameList.append('data2')

        return pcadataList,pcaCountList,pcaNameList

    pcaready = prepcafunction(xList,yList,zList,xCompList,yCompList,zCompList)
    
    def pcafunction(dataList,countList,nameList):
        from sklearn.decomposition import PCA
        import pylab as pl

        pcadataArray = np.array(dataList)
        pcaCountArray = np.array(countList)
        pca = PCA(n_components=2)
        X = pca.fit(pcadataArray).transform(pcadataArray)
        
        pcaNameList = []
        
        for i in range(0,len(nameList)):
            if nameList[i] not in pcaNameList:
                pcaNameList.append(nameList[i])

        print('explained variance ratio (first two components): %s'
              % str(pca.explained_variance_ratio_))
        
        plt.plot(X[pcaCountArray == 0, 0], X[pcaCountArray == 0, 1], 'or',
                 X[pcaCountArray == 1, 0], X[pcaCountArray == 1, 1], '^b',
                 X[pcaCountArray == 2, 0], X[pcaCountArray == 2, 1], 'sg'
                 )
        plt.xlabel('PC1 (explained variance ratio: ' + str(pca.explained_variance_ratio_[0])+')',fontsize=14)
        plt.ylabel('PC2 (explained variance ratio: ' + str(pca.explained_variance_ratio_[1])+')',fontsize=14)
        plt.legend((str(pcaNameList[0]),str(pcaNameList[1])),loc='best',fontsize=14)
        plt.title('PCA',fontsize=16)
    
    plt.figure(9)
    pcafunction(pcaready[0],pcaready[1],pcaready[2])
    
    plt.show()


if __name__=='__main__':
    if len(argv)!=3:
        help()
    jsonanalysis(argv[1],argv[2])