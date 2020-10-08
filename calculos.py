import numpy as np

def cp(mylist, usl, lsl):
    sigma=mylist.std(axis=0)
    sigma=(float(sigma))
    if sigma==0:
        cp=0
        return cp
    else:
        print('sigma= '+str(sigma)+' usl'+str(usl)+' lsl'+str(lsl)+' resta'+ str(float(usl-lsl)))
        cp = float(usl - lsl) / (6 * sigma)
        return cp
def filtrar (data):
    datafiltered = data[(data != 0)]  # quitar ceros y nulos
    Q1 = datafiltered.quantile(0.15)
    Q3 = datafiltered.quantile(0.85)
    IQR = Q3 - Q1
    data_noutliers = datafiltered[~((datafiltered < (Q1 - 1.5 * IQR)) | (datafiltered > (Q3 + 1.5 * IQR))).any(axis=1)]
    return data_noutliers
def cpk(mylist, usl, lsl):
    sigma = mylist.std(axis=0)
    sigma = (float(sigma))
    if sigma==0:
        cpk=0
        return cpk
    else:
        m=mylist['valores'].mean()
        Cpu = float(usl - m) / (3 * sigma)
        Cpl = float(m - lsl) / (3 * sigma)
        cpk = np.min([Cpu, Cpl])
        return cpk
def cpu(mylist,usl):
    sigma = mylist.std(axis=0)
    sigma = (float(sigma))
    if sigma == 0:
        cpu = 0
        return cpu
    else:
        m = mylist['valores'].mean()
        Cpu = m+(sigma*3)
        return Cpu
def cpl(mylist,lsl):
    sigma = mylist.std(axis=0)
    sigma = (float(sigma))
    if sigma == 0:
        cpl = 0
        return cpl
    else:
        m = mylist['valores'].mean()
        Cpl = m-(sigma*3)
        return Cpl