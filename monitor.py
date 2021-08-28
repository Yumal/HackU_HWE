import PySimpleGUI as sg
import time
import threading
import pyautogui
import statistics
from pynput import keyboard
import tkinter as tk
from tkinter import messagebox
from pygame import mixer
import datetime



one = "C:/Users/admin/PycharmProjects/Hack U/pysimpleGUI_sample/my/one.wav"
two = "C:/Users/admin/PycharmProjects/Hack U/pysimpleGUI_sample/my/two.wav"
three = "C:/Users/admin/PycharmProjects/Hack U/pysimpleGUI_sample/my/three.wav"
four = "C:/Users/admin/PycharmProjects/Hack U/pysimpleGUI_sample/my/four.wav"
five = "C:/Users/admin/PycharmProjects/Hack U/pysimpleGUI_sample/my/five.wav"
six = "C:/Users/admin/PycharmProjects/Hack U/pysimpleGUI_sample/my/six.wav"
seven = "C:/Users/admin/PycharmProjects/Hack U/pysimpleGUI_sample/my/seven.wav"
eight = "C:/Users/admin/PycharmProjects/Hack U/pysimpleGUI_sample/my/eight.wav"
onsei = [one, two, three, four,five, six, seven, eight]

def timer(h, m):
    global tStop, tOn, CountOutput
    tOn = False

    t = 3600 * h + 60 * m

    while t > 0:

        # 一時停止,休憩中はストップできるようにする
        if tStop == False:
            # この中でさぼり判定をするかのフラグを立てる→別のスレッドでさぼり判定
            print(t)
            t = t - 1
            tOn = True

            CountOutput = str(datetime.timedelta(seconds=t))

            time.sleep(1)

    tOn = False


def seq1():
    global SABORI, ON_Key
    print("マウスポインタ位置取得開始")

    while True:

        # マウスのxyを保存しておくリスト
        xl = []
        yl = []

        # さぼりを判定するインターバル（分）
        # インターバルを10で割った頻度で位置を取得
        interval = 0.8

        for i in range(0, 10):
            mp = pyautogui.position()
            x, y = mp
            xl.append(x)
            yl.append(y)
            time.sleep(60 * interval / 10)

        # 平均-最初の位置を絶対値にする
        # そうすると初期位置から平均どれぐらい動いてるかがわかる
        xs = abs(statistics.mean(xl) - xl[0])
        ys = abs(statistics.mean(yl) - yl[0])

        # print(xs)
        # print(ys)

        # キーボード入力時はジャッジスルー
        # 事故防止は大切
        if ON_Key == False:
            if xs < 10 and ys < 10:
                # print("アウト")
                SABORI = True

            else:
                # print("セーフ")
                SABORI = False

        else:
            ON_Key = False


def seq2():
    global SABORI, ON_Key

    def on_press(key):
        ON_Key = True

    def on_release(key):
        # キー入力は離した時に判定
        SABORI = KeySabori(key)

    def KeySabori(key):
        global KeyList, SABORI
        retS = False

        # KeyListの最大数は10ぐらい
        # そうでもないと処理を続ければ続けるほど重くなるクソソフトの完成
        if len(KeyList) < 11:
            KeyList.append(key)
        else:
            KeyList.pop(0)
            KeyList.append(key)

            # KeyList内が全部同じ文字ならさぼり判定
            retS = True
            for i in KeyList:
                if i != key:
                    retS = False

        SABORI = retS

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def seq0():
    # 起動時の初期設定
    global SABORI, KeyList, ON_Key, Gint, tStop, tOn, CountOutput, SABORI_count
    SABORI_count = 0 #初期化

    # SABORI...さぼりの最終出力。[True = さぼり]
    SABORI = False

    # KeyList...キーボードの入力を保存しておくリスト
    KeyList = []

    # ON_Key...キー入力がされているかどうか。[True = 入力中]
    ON_Key = False

    # Gint...SABORI出力のインターバル(単位：分)
    Gint = 0.5

    # tStop...タイマー一時停止
    tStop = False

    # tOn...タイマー起動中か？
    tOn = False

    # CountOutput...出力用の時間
    CountOutput = ""


def seq3():
    # SABORI,残り時間の最終出力
    # ここから受け渡し処理をすれば完了
    global SABORI, Gint, CountOutput, SABORI_count, tStop
    DoOnse = False
    while True:
        print(f"SABORI = {SABORI}")
        print(CountOutput)
        if tStop ==False:
            print(f"SABORI={SABORI}")
            print(CountOutput)
        if SABORI == True and DoOnse == False:
            SABORI_count += 1
            DoOnse = True
        elif SABORI == False and DoOnse == True:
            DoOnse = False
        else:
            pass
        print(f"サボった回数：{SABORI_count}回")
        time.sleep(60 * Gint)



def play():
    global SABORI, SABORI_count
    DoOnce = False
    while True:
        if SABORI == True:
            if DoOnce == False:
                mixer.init()
                mixer.music.load(onsei[SABORI_count])
                mixer.music.play()
                DoOnce = True
            else:
                DoOnce = False


def give_fear():
    global SABORI, SABORI_count
    while True:
        if SABORI_count == 1:
            root = tk.Tk()
            root.attributes('-fullscreen', True)
            cv = tk.Canvas(root, bg="black", highlightthickness=0)
            cv.pack(fill=tk.BOTH, expand=True)
            for i in range(1000):
                for j in range(1, 1000, 3):
                    cv.create_text(50 * i, 9 * j, text="仕事しろ      ", font="Comic-Sans", fill="red")
            root.mainloop()
            play("four.wav")




blank = " " * 60
b = " " * 5
bl = " " * 20


class MainDisplay:
    def __init__(self):
        sg.theme("Light Gray1")
        self.layout = [[sg.Text(blank + "Hack your Work Efficiency!", font=("papyrus", 16))],
                       [sg.Text(blank + "どのくらい作業する？"),
                        sg.InputText(size=(10, 1), text_color="#ffff00", background_color="#00aaff", key="-Hour-"),
                        sg.Text("時間"),
                        sg.InputText(size=(10, 1), text_color="#ffff00", background_color="#00aaff", key="-Minutes-"),
                        sg.Text("分")],
                       [sg.Text(blank + "休憩時間はどのくらい欲しい？"),
                        sg.Combo(("5分", "10分", "15分", "必要ねぇんだよ！"), default_value="10分", key="rest")],
                       [sg.Text(blank + "何分おきにチェックして欲しい？"),
                        sg.Combo(("30秒", "1分", "1分30秒"), default_value="1分", key="monitor")],
                       [sg.Text(blank + ""), sg.Button("ボイス設定"), sg.Text(b + ""), sg.Button("START?"), sg.Text(b + ""),
                        sg.Button("やっぱりやめる")]]
        self.window = sg.Window("作業監視アプリ", layout=self.layout, size=(800, 200), resizable=True)

    def make_option_display(self):
        option = SecondDisplay()
        option.main()
        del option

    def make_confirm_display(self):
        confirm = ThirdDisplay()
        confirm.main()
        del confirm

    def main(self):
        global jikan, hun, kyu, kanshi
        while True:
            event, values = self.window.read()
            jikan =int(values["-Hour-"])
            hun = int(values["-Minutes-"])
            if values["rest"] == "5分":
                kyu = 5
            elif values["rest"] == "10分":
                kyu = 10
            elif values["rest"] == "15分":
                kyu = 15
            else:
                kyu = 0
            if values["monitor"] == "30秒":
                kanshi = 0.5
            elif values["monitor"] == "1分":
                kanshi = 1
            else:
                kanshi = 1.5
            if event == sg.WIN_CLOSED or event == "やっぱりやめる":
                break
            elif event == "ボイス設定":
                self.make_option_display()
            elif event == "START?":
                self.make_confirm_display()
        self.window.close()


class SecondDisplay:
    def __init__(self):
        sg.theme("Light Gray1")
        self.voice_dic = {
            "1": "サンプル1",
            "2": "サンプル2",
            "3": "サンプル3"
        }

        self.layout = [
            [sg.Text('select voice(開発中)', size=(45, 1))],
            [sg.Radio(item[1], key=item[0], group_id='0') for item in self.voice_dic.items()],
            [sg.Button("適用して戻る")],
        ]
        self.window = sg.Window('ボイス設定', self.layout)
        del self.window

    def main(self):
        while True:
            event, value = self.window.read()
            if event == "適用して戻る" or event == sg.WIN_CLOSED:
                break
        self.window.close()



class Clock:
    def __init__(self):
        sg.theme("Light Gray1")
        self.layout = [
            [sg.Text("Working!",size=(10,2),font=("Comic-Sans",20),justification="center")]
            [sg.Text(size=(10,2), font =("Comic-Sans",20),justification="center",key="-OUT-")]]
        self.window = sg.Window("Now Working...", self.layout)

    def main(self):
        while True:
            event, value = self.window.read(timeout=100,timeout_key="-time-")
            if event in (None,):
                break
            elif event in "-time-":
                C = CountOutput
                self.window["-OUT-"].update(C)
            if event ==sg.WIN_CLOSED:
                break
        self.window.close()

class ThirdDisplay:
    def __init__(self):
        sg.theme("Light Gray1")
        self.layout = [
            [sg.Text(bl + "イヤホンを装着しながらでの使用をお勧めします・・・・")],
            [sg.Text(blank + b + ""), sg.Button("START!")],
            [sg.Text("",size=(10,2), font =("Comic-Sans",20),justification="center",key=("-OUT-"))]
            ]
        self.window = sg.Window('Are you ready??', self.layout)

    def show_clock(self):
        c = Clock()
        c.main()
        del c

    def main(self):
        global jikan,hun
        doonce = True
        while True:
            event, value = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == "START!":
                # テキストから数値を入力する方法がよくわからん。そっちで頼める？
                h = jikan
                m = hun
                if doonce == True:
                    thread0 = threading.Thread(target=seq0)
                    thread1 = threading.Thread(target=seq1)
                    thread2 = threading.Thread(target=seq2)
                    thread3 = threading.Thread(target=seq3)
                    thread4 = threading.Thread(target=play)
                    thread5 = threading.Thread(target=give_fear)
                    #thread6 = threading.Thread(target=show_time)

                    thread0.start()
                    thread1.start()
                    thread2.start()
                    thread3.start()
                    thread4.start()
                    thread5.start()

                    timer(h, m)
                    self.window.write_event_value("残り時間", CountOutput)
                    #thread6.start()
                    #self.window["-OUT-"].update(CountOutput)
                    doonce = False

        self.window.close()

disp1 = MainDisplay()
disp1.main()
#print(SABORI)