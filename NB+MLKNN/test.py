#计算一个向量的k近邻,返回各个情绪类别的数量n[],train_test_flag=0 train
def find_neighbor(test_weight,train_vec,k,train_test_flag):
        #相似度值
        cos=[]
        for train_weight in train_vec:
            #训练集中邻居不包括自己
            if train_test_flag==0 and train_weight==test_weight:
                continue
            up=0.0
            down1=0.0
            down2=0.0
            for i in range(0,len(train_weight)):
                up=up+train_weight[i]*test_weight[i]
                down1=down1+train_weight[i]*train_weight[i]
                down2=down2+test_weight[i]*test_weight[i]
            down1=math.sqrt(down1)
            down2=math.sqrt(down2)
            if down1==0 or down2==0:
                cos_theta=-2
                cos.append(cos_theta)
                continue
            #print("train %r"%(down1))
            #print("test %r"%(down2))
            down=down1*down2
            cos_theta=up*1.0/down
            cos.append(cos_theta)
        #降序排序，取前k个相似度
        cosTemp=sorted(cos)
        cosTemp.reverse()
        train_index=[]
        for i in range(0,k):
            for j in range(0,len(cos)):
                if cos[j]==cosTemp[i]:
                    train_index.append(j)
                    cos[j]=2
                    break
        # 计算结果train_label
        emotion=['happiness', 'like','anger','sadness','fear','disgust','surprise']
        num=[0 for i in range(0,7)]
        for i in train_index:
            for j in range(0,len(emotion)):
                if train_label[i]==emotion[j]:
                    num[j]=num[j]+1
        return num


#只针对有情绪的
def map(k,train_label, train_vec):
    #1从训练集中计算先验概率PH[emotion][1]
    emotion=['happiness', 'like','anger','sadness','fear','disgust','surprise']
    m=len(train_label)
    #训练集中每个类别的数量
    n=[0 for i in range(0,7)]
    for i in range(0,len(train_label)):
        for j in range(0,len(emotion)):
            if train_label[i]==emotion[j]:
                n[j]=n[j]+1
       #平滑s
    s=1
    ph=[[0 for col in range(2)] for row in range(7)]
    for i in range(0,len(emotion)):
        ph[i][1]=(s+n[i])*1.0/(s*2+m)
        ph[i][0]=1-PH[i][1]
    #2从训练集中计算后验概率
     #为训练集中的每一条微博计算它的K近邻
    dic_train_neighbor={}
    #dic_train_neighbor[0]=[邻居index]
    index=0
    for train_weight in train_vec:
        neighbor_emotion_num=find_neighbor(train_weight,train_vec,k,0)
        dic_train_neighbor[index]=neighbor_emotion_num
        index=index+1
    #对于每种情绪，计算出后验概率p(e[emotion][j]|h[emotion][1]),p(e[emotion][j]|h[emotion][0])
    pe1=[[0 for col in range(k)] for row in range(7)]
    pe0=[[0 for col in range(k)] for row in range(7)]
    for i in range(0,len(emotion)):
         #情绪label i
         c1=[0 for ii in range(0,k)]
         c2=[0 for ii in range(0,k)]
         for j in range(0,m):
             #对于第J个训练样本
             temp=dic_train_neighbor[j][i]
             if train_label[j]==emotion[i]:
                 c1[temp]=c1[temp]+1
             else:
                 c2[temp]=c2[temp]+1
         sum_c1=0
         sum_c2=0
         for jj in range(0,k):
             sum_c1=sum_c1+c1[jj]
             sum_c2=sum_c2+c2[jj]
         for jj in range(0,k):
             pe1[i][jj]=(s+c1[jj])*1.0/(s*(k+1)+sum_c1)
             pe0[i][jj]=(s+c2[jj])*1.0/(s*(k+1)+sum_c2)
    return ph,pe1,pe0,n

#预测测试样本t,R(l)最大的所对应的情绪也就是预测情绪类别
def predict_test(test_weight,k,train_vec,ph,pe1,pe0,n):
    emotion=['happiness', 'like','anger','sadness','fear','disgust','surprise']
    r=[0 for i in range(0,7)]
    #测试样本邻居对应的类别的数目
    neighbor_emotion_num=find_neighbor(test_weight,train_vec,k,1)
    for i in range(0,len(emotion)):
        up=ph[i][1]*(neighbor_emotion_num[i]*1.0/n[i])
        down=ph[i][1]*pe1[i][neighbor_emotion_num[i]] + ph[i][0]*pe0[i][neighbor_emotion_num[i]]
        r[i]=up*1.0/down
    rtemp=sorted(r)
    for i in range(0,len(emotion)):
        if r[i]==rtemp[6]:
            test_emotion_temp=emotion[i]
    return test_emotion_temp
















