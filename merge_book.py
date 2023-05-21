import pyautogui
import time
from PIL import ImageGrab
import os
import shutil
from PyPDF2 import PdfMerger

# 폴더 삭제 후 재생성
try:
    shutil.rmtree('./pdf')
except:
    pass

os.makedirs('./pdf/', exist_ok=True)

# ebook으로 탭 전환
pyautogui.keyDown('win')
pyautogui.press(str(0))
pyautogui.keyUp('win')
time.sleep(1)

# 전체화면 모드
pyautogui.moveTo(1884,51)
pyautogui.click()

time.sleep(3)
for i in range(3):
    print(f"{3-i}초 뒤 캡처를 시작합니다.")
    time.sleep(1)
print()
    
i=0 # 페이지 변수
captured = {'past':0, 'now':1} # 현재 캡처와 이전 캡처 비교

# 캡처 시작
while True:
    i+=1
    captured['now'] = ImageGrab.grab()

    # 캡처 이미지가 바뀌지 않으면 반복문 종료
    if captured['now'] == captured['past']:
        print('이미지가 같아서 종료합니다.')
        break

    else:
        # 시간에 따른 파일명 지정
        base_name = f"./pdf/{round(time.time(), 2)}"
        
        # 왼쪽 페이지와 오른쪽 페이지를 나눠서 저장
        width, height = captured['now'].size        
        left_image = captured['now'].crop((0,0,width//2,height))
        right_image = captured['now'].crop((width//2,0,width,height))
        left_image.save(base_name+"_left.pdf")
        right_image.save(base_name+"_right.pdf")
        
        # quality를 높이면 저장 용량이 증가함
        # left_image.save(base_name+"_left.pdf", quality=100)
        # right_image.save(base_name+"_right.pdf", quality=100)
        print(f"{2*i-1}, {2*i}번째 페이지가 저장되었습니다.")
        captured['past'] = captured['now']
        
        # 페이지 전환
        pyautogui.press('right')
        time.sleep(0.5)

print()
print(f"전체 {2*i-2} 페이지로 구성됩니다.")

# 개별 pdf를 병합하기 위한 객체
merger = PdfMerger()

# pdf 폴더에 있는 pdf 리스트를 읽어서 병합
pdf_list = os.listdir('./pdf/')[:-2]
for pdf in pdf_list:
    merger.append('./pdf/' + pdf)
merger.write('merged.pdf')
merger.close()    

print()
print('pdf 병합이 완료되었습니다.')
