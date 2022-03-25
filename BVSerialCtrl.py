# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 14:45:13 2022

@author: ed_liu
"""
import serial
import threading
import time
from BVLogFuctions import ATFuc

class SerialCtrl:
    # 建構式
    def __init__(self,COMPortNo):
        self.start_threads=False
        try:
            self.ser=serial.Serial("com{}".format(COMPortNo),115200,timeout=0.5)
            print('COM連接成功')
        except:
            print('COM連接失敗')
            exit()
            
    # 方法(Method)
    def ChangeBVIP(self,BVIP):
        self.ser.write("ifconfig eth0 {} up\r\n".format(BVIP).encode())
        print("已變更為",BVIP)

    def SetBVTimeProcess(self,ChangeTimeAction):
        TimeType='H'    
        while(1):
            ATFuc.ShowTimeType(TimeType) 
            try:                            
                if TimeType=='H' or TimeType=='m':
                    print("時間變更量:",ChangeTimeAction)
                    self.ser.write('date "+%Y:%m:%d:%H:%M:%S"\r\n'.encode())
                    Bvdate=self.ser.readline()#該段為指令回應值
                    Bvdate=self.ser.readline()#替代為時間
                    
                    TargetDate=ATFuc.ChangeTimeProcess(Bvdate,eval(ChangeTimeAction),TimeType)   
                    
                    print(TargetDate)
                    
                    self.ser.write('date {}\r\n'.format(TargetDate).encode())
                    
                else:
                    print('植入日期')       
                    if TimeType=='Y':   
                        
                        #取得BV年份
                        self.ser.write('date "+%Y"\r\n'.encode())
                        Bvdate=self.ser.readline()#該段為指令回應值
                        Bvdate=self.ser.readline()#替代為時間
                        
                        TargetYear=str(eval(Bvdate.decode("ascii").rstrip())+eval(ChangeTimeAction))
                        
                        #取得完整時間格式
                        self.ser.write('date "+%m%d%H%M.%S"\r\n'.encode())
                        Bvdate=self.ser.readline()#該段為指令回應值
                        Bvdate=self.ser.readline()#該段為指令回應值
                        Bvdate=self.ser.readline()#替代為時間
                        EntireBvdate=Bvdate.decode("ascii").rstrip()
                        
                        #設定日期
                        TargetDate=TargetYear+EntireBvdate
                        self.ser.write('date {}\r\n'.format(TargetDate).encode())
    
                break
            except:
                print('except process!')
                if len(ChangeTimeAction)==1 and ChangeTimeAction.isalpha():    
                    if ChangeTimeAction=='H' or ChangeTimeAction=='m' or ChangeTimeAction=='Y' or ChangeTimeAction=='M': 
                        print("已變更時間單位!")
                        TimeType=ChangeTimeAction
                    else:
                        print('輸入格式錯誤!!!')
                        break
        
    def InitTimeProcess(self,InitTimeAction):
        TargetInitTime=ATFuc.InitTimeActionFuc(InitTimeAction)
        self.ser.write('date {}\r\n'.format(TargetInitTime).encode())
        self.ser.write('hwclock --systohc\r\n'.encode())#同步到硬體時間

    def GetBVDebugInfo(self):
        AllDebugInfo=self.ser.readlines()
        for x in  AllDebugInfo:
            print(x.decode("big5"))

    def SerialClose(self):
        self.ser.close()
        print("已關閉COM port")
        
    def DebugCtrl(self):
        print('DebugCtrl\n')
        while(1):
            AllDebugInfo=self.ser.readlines()
            for x in  AllDebugInfo:
                print(x.decode("big5"))
            time.sleep(1)
            if self.start_threads==False:
                break




if __name__ == '__main__':
    ser = SerialCtrl('3')

    
    # 主執行緒繼續執行自己的工作
    while(1):
        Cmd=input("輸入~~")
        if Cmd=='1':
            if ser.start_threads==False:
                t = threading.Thread(target = ser.DebugCtrl)
                ser.start_threads=not ser.start_threads
                t.start()
                print("關閉Debug Mode")
            else:
                ser.start_threads=False
                t.join()
                t = threading.Thread(target = ser.DebugCtrl)
                
        if Cmd=='99':
            if t.is_alive():
                ser.start_threads=False
                t.join()
            break

    # 等待 t 這個子執行緒結束

    ser.SerialClose()