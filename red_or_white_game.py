from microbit import *
import random

COUNT_ONE_GAME = 5
SCORE_RANK_S = 2000
SCORE_RANK_A = 2500
SCORE_RANK_B = 3000
SCORE_RANK_C = 3500

# ランダムイメージ生成関数
# 引数    num             点灯させるLEDの数
# 返り値   image_buffer    ランダムイメージ
# イメージのサイズは5x5
# 引数が不正値の場合、空のイメージを返す
# Todo : num > 12 の場合は点灯させない場所を探索するようにする(処理高速化)
def generate_ramdom_image(num):
    image_buffer = Image(5, 5)  # 返り値初期化
    if num < 0 or num > 25:     # 引数不正
        return image_buffer     # 空のイメージを返す
    remain = num                # 場所未確定LED数
    right_pos_list = []         # 点灯確定位置リスト
    while remain > 0:           # 場所未確定LED数が0になるまで以下の処理を繰り返す
        random_num = random.randint(0, 24)      # 0~24までの範囲の乱数生成
        is_first_detect = True
        for right_pos in right_pos_list:        # すでに点灯が確定している位置との照らし合わせ
            if random_num == right_pos:         # すでに点灯が確定している位置とかぶっていたら
                is_first_detect = False
        if is_first_detect:                     # はじめて点灯が確定した位置だったら
            right_pos_list.append(random_num)   # 点灯確定位置リストに追加
            remain -= 1
            # random_numの位置を点灯("9")に設定
            image_buffer.set_pixel((random_num % 5), (random_num // 5), 9)
    return image_buffer

# 不正解画面表示関数
def show_incorrect_image():
    display.show(Image.SAD)

# 正解画面表示関数
def show_correct_image():
    display.show(Image.HAPPY)

# カウントダウン表示関数
def show_count_down(sec):
    for count in range(sec, 0, -1):
        display.show(str(count))
        sleep(1000)

# 結果表示関数
def show_result(correct_num, total_time):
    if correct_num < COUNT_ONE_GAME:
        display.show("D")
        return
    if total_time < SCORE_RANK_S:
        display.show("S")
    elif total_time < SCORE_RANK_A:
        display.show("A")
    elif total_time < SCORE_RANK_B:
        display.show("B")
    elif total_time < SCORE_RANK_C:
        display.show("C")
    else:
        display.show("D")

# メイン処理
uart.init(115200)
uart.write("start.\n")
display.show("W")
sleep(3000)
display.show(Image.ARROW_W)
sleep(3000)
display.show("R")
sleep(3000)
display.show(Image.ARROW_E)
sleep(3000)
while True:
    total_time = 0
    correct_num = 0
    show_count_down(3)
    for loop_count in range(COUNT_ONE_GAME):
        random_num = random.randint(0, 24)
        if random_num < 13:
            correct_button = "A"
        else:
            correct_button = "B"
        image = generate_ramdom_image(random_num)
        display.show(image)
        start_time = running_time()
        while True:
            if button_a.is_pressed():
                if correct_button == "A":
                    show_correct_image()
                    correct_num += 1
                    break
                else:
                    show_incorrect_image()
                    break
            if button_b.is_pressed():
                if correct_button == "B":
                    show_correct_image()
                    correct_num += 1
                    break
                else:
                    show_incorrect_image()
                    break
        total_time += running_time() - start_time
        uart.write(str(total_time))
        uart.write("\n")
        sleep(3000)
    show_result(correct_num, total_time)
    sleep(5000)