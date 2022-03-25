import serial
import time
from FTPwork import myFtp
from time import gmtime, strftime


'''
            try:
                ftp = myFtp("BVIP")
                ftp.Login("root", "")            
                #設定目標路徑
                ftp.ChangeRount('..') #turn back                
                ftp.ChangeRount('bv/InBox')
#-------------------------------------------------------------------------------------------- 
            
#-------------------------------------------------------------------------------------------- 
                ftp.close()
                

            except:
                print("請確認RJ45是否有接好!")



'''



class ATFuc:
    def CheckFileExist(BVIP):
            try:
                ftp = myFtp(BVIP)
                ftp.Login("root", "")            
                #設定目標路徑
                ftp.ChangeRount('..') #turn back                
                ftp.ChangeRount('bv/InBox')
                
                FolderList=ftp.CheckRountsFileName()
                TargetFolders=[]
                for Folder in FolderList:
                    ftp.ChangeRount(Folder)
                    FileList=ftp.CheckRountsFileName()
                    
                    if len(FileList)>0:
                        TargetFolders.append(Folder)                    
                        
                        
                    ftp.ChangeRount('..') #turn back  
                    
                    
                ftp.close()
                
                return TargetFolders
    
                    
            except:
                print("請確認RJ45是否有接好!")
    
    def GetInboxfile(FolderList,BVIP):
        TestProjectName="DeviceID:"
        
        try:
            ftp = myFtp(BVIP)
            ftp.Login("root", "")
            
            #設定目標路徑
            ftp.ChangeRount('..') #turn back                
            ftp.ChangeRount('bv')
    
            #獲取需備份的檔案
            
            
            for TargetFolder in FolderList:
                local_path = 'Datas/'+TargetFolder
                romte_path = 'InBox/'+TargetFolder                      
                try:
                    ftp.DownLoadFileTree(local_path,romte_path,BVIP,TestProjectName)   
                    print("資料取得完成")
                    

                    
                    ftp.ChangeRount('..')
                except:
                    print("InBox資料獲取失敗")
                    
            ftp.close()
                
        except:
            print("請確認RJ45是否有接好!")
    def DeleteTargetFolder(FolderList,BVIP):
                
        try:
            ftp = myFtp(BVIP)
            ftp.Login("root", "")            
            #設定目標路徑
            ftp.ChangeRount('..') #turn back                
            ftp.ChangeRount('bv/InBox')
#-------------------------------------------------------------------------------------------- 
            for Folder in FolderList:
                ftp.DeleteFoldersFlies(Folder)  
                ftp.ChangeRount('..')
#-------------------------------------------------------------------------------------------- 
            ftp.close()
            

        except:
            print("請確認RJ45是否有接好!")
    def ChangeTimeProcess(Bvdate,DeltaTime,TimeType):
        
        BvdateString=Bvdate.decode("ascii").rstrip()    
        struct_time = time.strptime(BvdateString, "%Y:%m:%d:%H:%M:%S") # 轉成時間元組
        time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
        
        if TimeType=='H':
            DeltaTime=DeltaTime*3600
        else:
            DeltaTime=DeltaTime*60
        
        TargetStamp=time_stamp+DeltaTime
        
        t = time.localtime(TargetStamp)
        result = time.strftime("%Y%m%d%H%M.%S",t)
        
        return result
    
    def ShowTimeType(TimeType):
        if TimeType=='H':
            print('目前時間單位:小時')
        elif TimeType=='m':
            print('目前時間單位:分鐘')
        elif TimeType=='Y':
            print('目前時間單位:年份')
        elif TimeType=='M':
            print('目前時間單位:月份')
            
    def InitTimeActionFuc(InitTimeAction):
        if InitTimeAction=='1':
            TargetInitTime=strftime("%Y%m%d%H%M.%S",gmtime())
        elif InitTimeAction=='2':
            TargetInitTime=str(time.strftime("%Y%m%d"))
            TargetInitTime=TargetInitTime+"0000.00"
        return TargetInitTime
            

    
if __name__ == '__main__':
    struct_time =ATFuc.InitTimeActionFuc('1')
    print(struct_time)

            

