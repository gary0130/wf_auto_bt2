import cv2
import subprocess
import numpy as np
import time
import json

re_po=0.4 #縮放倍率

def find_pic(target_pic):
    #adb截圖
    pipe = subprocess.Popen("adb shell screencap -p",
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
    image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    

    #搜尋目標圖片
    img_template = cv2.imread(target_pic)
    
    d,w, h = img_template.shape[::-1]

    res = cv2.matchTemplate(image,img_template,cv2.TM_SQDIFF_NORMED)
    # 得到最大和最小值得位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc #左上角的位置
    bottom_right = (top_left[0] + w, top_left[1] + h) #右下角的位置
    #控制相似度
    if min_val<0.01:
        print(target_pic," find at", top_left[0],  top_left[1],"posible",min_val)
        #cv2.rectangle(image,top_left, bottom_right, (0,0,255), 2)
        return top_left[0],  top_left[1]
    else:
        #print("not found")
        return -1,-1

def show_xy(event,x,y,flags,userdata):
    if event == 1:
        print(event,x/re_po,y/re_po,flags)

def adb_click_of(x,y):
    #adb點擊
    #因為辨識出來是在邊界，所以要加上一個偏移量
    pipe = subprocess.Popen("adb shell input tap "+str(x+30)+" "+str(y+30),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
    
#start
with open('rule.json','r', encoding='utf-8') as f:
    cf=json.loads(f.read())

print(cf['rule_name'])
print(cf['rule'])


cttr=1
while True:
    flg=0
    print("第",cttr,"次")
    if cttr>=50:
        break
    #搜尋順序
    for i in cf['rule']:
        if cttr>=50:
            break

        for j in cf["rule_det"]:
            if j["id"]==i:
                #檢查失敗條件
                x,y=find_pic(cf["rule_fail"])
                if x!=-1:
                    print("沒體拉")
                    cttr=999
                    break

                #搜尋位置
                print("搜尋 ",j["name"])
                x,y=find_pic(j['file_name'])
                if x==-1:
                    print("找不到")
                    cttr=999
                    break
                print("點擊 " ,x,y," 並休息 ",j["wait_time"])
                adb_click_of(x,y)
                time.sleep(j["wait_time"])

    
    print("循環" ,cttr,"結束\n")
    cttr+=1



        
'''
while True:
    #adb截圖
    pipe = subprocess.Popen("adb shell screencap -p",
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
    image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
    image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    

    #搜尋目標圖片
    img_template = cv2.imread("capture.png")

    d,w, h = img_template.shape[::-1]

    res = cv2.matchTemplate(image,img_template,cv2.TM_SQDIFF_NORMED)
    # 得到最大和最小值得位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc #左上角的位置
    bottom_right = (top_left[0] + w, top_left[1] + h) #右下角的位置
    #控制相似度
    if min_val<0.0001:
        print("find at", top_left[0],  top_left[1],"posible",min_val)
        cv2.rectangle(image,top_left, bottom_right, (0,0,255), 2)
    else:
        print("not found")
    
    #除錯用，顯示圖片
    image = cv2.resize(image, (0, 0), fx=re_po, fy=re_po)
    cv2.imshow("aa", image)
    cv2.setMouseCallback("aa", show_xy)
    time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
'''