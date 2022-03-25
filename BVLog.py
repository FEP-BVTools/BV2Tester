import os
import threading
from BVLogFuctions import ATFuc
from BVSerialCtrl import SerialCtrl


def Ctrlprint(words,sw):
    if(sw==1):
        print(words)

if __name__ == '__main__':
    
    Cmd=0
    BVIP="192.168.3.50"
    IPFileName="BVIPConfig.txt"
    start_threads=False

    COMPortNo=input("請輸入使用的Com,例:com3,則輸入3\n")    
    
    try:
        ser = SerialCtrl(COMPortNo)
        t = threading.Thread(target=ser.DebugCtrl)
        if  os.path.exists(IPFileName): #確認是否存在儲存路徑
            f=open(IPFileName)
            BVIP=f.readline()
            f.close()
        else:
            f=open(IPFileName,'w+')
            f.write(BVIP)
            f.close()



        while(Cmd!=99):

            print("Cmd:",Cmd)

            print("1.下載並刪除資料")
            print("2.清除資料")
            print("3.時間變更")
            print("4.時間初始化")
            print("5.Debug資訊接收")
            print("99.離開")

            Cmd=eval(input("請輸入要執行的功能:\n"))

            if Cmd==1:
                ser.ChangeBVIP(BVIP)
                print("開始取得資料...")
                TargetFile=ATFuc.CheckFileExist(BVIP)
                if len(TargetFile)>0:
                    #下載Log資料
                    ATFuc.GetInboxfile(TargetFile,BVIP)
                    #刪除資料
                    ATFuc.DeleteTargetFolder(TargetFile,BVIP)
                else:
                    print("無交易資料!!!")

            elif Cmd==2:
                ser.ChangeBVIP(BVIP)
                TargetFile=ATFuc.CheckFileExist(BVIP)
                Ctrlprint(TargetFile,1)
                if len(TargetFile)>0:
                    ATFuc.DeleteTargetFolder(TargetFile,BVIP)
                else:
                    print("無交易資料!!!")
            elif Cmd==3:
                ChangeTimeAction=input('請輸入變更時間(不變更輸入0)')
                if ChangeTimeAction=='':
                    ChangeTimeAction='0'
                ser.SetBVTimeProcess(ChangeTimeAction)

            elif Cmd==4:
                print("1.設為現在時間  2.設為今天8點 ")
                InitTimeAction=input('請輸入執行項目')
                if InitTimeAction=='1' or InitTimeAction=='2':
                    ser.InitTimeProcess(InitTimeAction)
                else:
                    print("指令錯誤!!!")

            elif Cmd==5:
                if ser.start_threads==False:
                    ser.start_threads=not ser.start_threads
                    t.start()

                else:
                    ser.start_threads=False
                    print("關閉Debug Mode...")
                    t.join()



            elif Cmd==99:
                if t.is_alive():
                    ser.start_threads=False
                    t.join()
                ser.SerialClose()
                break
            else:
                print("無該功能!")

            #=====================================================================================================================


    except:
        a=input('連接失敗!!')
        

    