# 鼠标连点器
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
import time

# 需要连点的按键 .left .middle .right 
btnClick = Button.right
# 连点次数，0则无限连点
loopCount = 0
# 连点时间，单位为s，0则无限时间
timeClick = 5
# 连点的间隔
timeSleep = 0.5

# 暂停/开始 热键
pauseKey=keyboard.Key.pause
# 结束 热键
stopKey=keyboard.Key.esc

# 已经连点了的次数，不需要设置
clickCount = 1
clickCount_lock = threading.Lock()
# 记录点击次数
clickSum = 0
# 互斥访问以实现停止连点
stopFlag = True
stopFlag_lock = threading.Lock()

def MouseClick():
    global stopFlag
    global clickCount
    global clickSum
    mouse = Controller()
    while clickCount <= loopCount or loopCount == 0:
        mouse.click(btnClick, 1)
        time.sleep(timeSleep)
        with stopFlag_lock:
            if(stopFlag):
                break
        with clickCount_lock:
            clickCount = clickCount+1
            clickSum = clickSum+1
    with stopFlag_lock:
        stopFlag = True

def StopClick():
    global stopFlag
    global clickCount
    global clickSum
    global loopCount
    global timeClick
    # 监听键盘键入
    with keyboard.Events() as events:
        for event in events:
            # 监听stopKey键，结束连点
            if event.key == stopKey:
                print('连点结束，共点击{}次'.format(clickSum))
                break
            elif event.key == pauseKey:
                # 按下和松开都算一个事件
                if isinstance(event, keyboard.Events.Press):
                    print(stopFlag)
                    with stopFlag_lock:
                        if(stopFlag):
                            stopFlag = False
                            threadClick = threading.Thread(target= MouseClick)
                            threadClick.start()
                        else:
                            stopFlag = True
                        with clickCount_lock:
                            if(clickCount >= loopCount):
                                if(loopCount == 0 and timeClick != 0):
                                    loopCount = timeClick / timeSleep
                                clickCount = 1
    with stopFlag_lock:
        stopFlag = True

if __name__ == '__main__':
    btn=eval(input("0.Left 1.Middle 2.Right. Please type mouse click:\n"))
    btn_list=["Left", "Middle", "Right"]
    if(btn==0):
        btnClick = Button.left
    elif(btn==1):
        btnClick = Button.middle
    else:
        btnClick = Button.right
    print("Mouse {}, please press hotkey to start".format(btn_list[btn]))
    threadStop = threading.Thread(target=StopClick)
    threadStop.start()
    # 阻塞线程，免得程序结束了线程还没结束
    threadStop.join()
