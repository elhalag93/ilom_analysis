#!/usr/bin/env python
# coding: utf-8

# In[3]:


from zipfile import ZipFile
import os
from datetime import datetime
start_time = datetime.now()
logs=['@usr@local@bin@fmadm_faulty.out','@usr@local@bin@collect_properties.out','@usr@local@bin@spshexec_show_faulty.out'
     ,'@persist@faultdiags@faults.log','@usr@local@bin@spshexec_show_-d_properties_-level_all_@SYS.out','@usr@local@bin@env_test.out'
     ,'@usr@local@diag@listlinkup.out','@conf@hostname','@conf@hosts','@usr@local@bin@ipmiint_fru_print.out']
# open file
path='D:\pm_analysis\iloms\logs'
total=len(os.listdir('D:\pm_analysis\iloms\\logs'))
counter=0
for iloms in os.listdir(path):
    counter += 1
    start_p_time=datetime.now()
#    ratio=(counter/total)*100
    print(iloms + '  progress = '+str(counter)+ " / " +str(total) + '     '+str((counter/total)*100)+ '%' )
    with ZipFile(str(path)+'\\'+str(iloms), 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
        for i in listOfFileNames :
            for x in logs :
                if i.endswith(x) :
                    zipObj.extract(i,path='D:\pm_analysis\iloms\\analysis')        
    # extracting file
    zipObj.close()
    end_p_time=datetime.now()
    duration=end_p_time - start_p_time
    print('duration: {}'.format(end_p_time - start_p_time))
end_time = datetime.now()
print('over_all_extracting_files: {}'.format(end_time - start_time))


# In[4]:


import os
import shutil
path = 'D:\pm_analysis\iloms\\analysis'
for ilom in os.listdir('D:\pm_analysis\iloms\\analysis'):  
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(str(path)+'\\'+str(ilom)):
        for file in f:
            files.append(os.path.join(r, file))
    for f in files:
            shutil.move(f,str(path)+'\\'+str(ilom))
    if os.path.exists(str(path)+'\\'+str(ilom)+'\\'+'fma') :
        shutil.rmtree(str(path)+'\\'+str(ilom)+'\\'+'fma')
    if os.path.exists(str(path)+'\\'+str(ilom)+'\\'+'ilom') :
        shutil.rmtree(str(path)+'\\'+str(ilom)+'\\'+'ilom')
    if os.path.exists(str(path)+'\\'+str(ilom)+'\\'+'NM2') :
        shutil.rmtree(str(path)+'\\'+str(ilom)+'\\'+'NM2')        
        


# In[5]:


from zipfile import ZipFile
import os
from datetime import datetime
error=['fault_state = Faulted']
message_list=['@usr@local@bin@collect_properties.out','@usr@local@bin@fmadm_faulty.out','@usr@local@bin@spshexec_show_faulty.out']
format_list=['unknown','found','not']
x=[]
t=''
path = 'D:\pm_analysis\iloms\\analysis'

w = open("D:\\pm_analysis\\iloms\\summary"+"\\"+"list_of_server.txt", "a")

for ilom in os.listdir('D:\pm_analysis\iloms\\analysis'): 
    if os.path.exists('D:\pm_analysis\iloms\\analysis'+'\\'+ilom+"\\"+"@conf@hostname") :
        with open('D:\pm_analysis\iloms\\analysis'+'\\'+ilom+"\\"+"@conf@hostname") as log_file:
                    for line in log_file:
                        server_name=line.split(sep='_')[0].strip()
    if os.path.exists('D:\pm_analysis\iloms\\analysis'+'\\'+ilom+"\\"+"@conf@hosts") :
        with open('D:\pm_analysis\iloms\\analysis'+'\\'+ilom+"\\"+"@conf@hosts") as log_file:
                server_name = log_file.readlines()[0].rstrip().split()[-1]

    log_file.close()
    log_file.close()
    w.write(server_name+"\n")
    x.append(server_name)
    logs=os.listdir('D:\pm_analysis\iloms\\analysis'+'\\'+ilom)
    sumarry_file = open("D:\\pm_analysis\\iloms\\summary"+"\\"+server_name+".txt", "a")
    sumarry_file.write("host name = "+server_name+"\n")
    for log in logs :
        if log ==  "@usr@local@bin@ipmiint_fru_print.out" :
            with open('D:\pm_analysis\iloms\\analysis'+'\\'+ilom+"\\"+"@usr@local@bin@ipmiint_fru_print.out") as log_file:
                p=False
                s=False
                c= True
                for line in log_file:      
                    if 'FRU Device Description : /SYS' in line and c :
                        p=True
                        s=True
                    if p == True :
                        if 'Product Name' in line :
                                sumarry_file.write(line+"\n")
                                p=False
                    if s  == True :           
                        if 'Product Serial' in line :
                                sumarry_file.write(line+"\n")
                                s=False
                                c=False 
        if log ==  "@usr@local@bin@collect_properties.out" :
            with open('D:\pm_analysis\iloms\\analysis'+'\\'+ilom+"\\"+"@usr@local@bin@collect_properties.out") as log_file:
                flag=True
                for line in log_file:
                    if 'type = ' in line :
                        t=line
                    for reg in error:
                        if reg in line:
                            flag=False
                            sumarry_file.write('hardware status of '+str(t)+"\n")
                            sumarry_file.write(line+"\n")
                            t=''
                if flag:
                        sumarry_file.write("no faulty parts"+"\n")
            log_file.close()
            sumarry_file.write("------------------------------------------------------------------------------"+"\n")
        if log ==  "@usr@local@bin@fmadm_faulty.out" :
            with open('D:\pm_analysis\iloms\\analysis'+'\\'+ilom+"\\"+"@usr@local@bin@fmadm_faulty.out") as log_file:
                for line in log_file:
                    sumarry_file.write("fmadm output")
                    sumarry_file.write(line+"\n")
            log_file.close()
            sumarry_file.write("------------------------------------------------------------------------------"+"\n")
        if log ==  "@usr@local@bin@spshexec_show_faulty.out" :
            with open('D:\pm_analysis\iloms\\analysis'+'\\'+ilom+"\\"+"@usr@local@bin@spshexec_show_faulty.out") as log_file:
                for line in log_file:
                    sumarry_file.write(line+"\n")
                    sumarry_file.write("show faulty output"+"\n")
            log_file.close()
            sumarry_file.write("------------------------------------------------------------------------------"+"\n")
print(len(x))
sumarry_file.close()    
w.write('number of servers = ' + str(len(x))+"\n")
w.close()


# In[ ]:




