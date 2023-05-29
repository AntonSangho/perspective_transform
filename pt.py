import cv2, os
import numpy as np

#img_path = './img/pexels-photo-276690.jpg'
img_path = './img/pexels-photo-734968.jpg'
filename, ext = os.path.splitext(os.path.basename(img_path))
# 1.원본 이미지를 불러와서 ori_img 변수에 넣어준다.  
ori_img = cv2.imread(img_path)

# 2.src라는 전역 변수를 지정해준다. 
src = []

# mouse callback handler
# 5. mouse_handler를 마우스에서 5개의 hangdler를 받는다. 
def mouse_handler(event, x, y, flags, param):
  # 이벤트가 마우스의 옆 버튼에 올라왔을 때 
  if event == cv2.EVENT_LBUTTONUP:
    # 이미지의 변수에 오리지널 이미지를 복사한다.
    img = ori_img.copy()
    #src의 전역변수에다가 x,y값을 저장합니다.
    src.append([x, y])
    #클릭을 했을 때, 점으로 표시하는 것 
    for xx, yy in src:
      cv2.circle(img, center=(xx, yy), radius=5, color=(0, 255, 0), thickness=-1, lineType=cv2.LINE_AA)
    # 이미지를 보여준다. 
    cv2.imshow('img', img)

    # perspective transform
    # perspective transform에서는 네개의 점을 필요로 합니다. 
    if len(src) == 4:
      # src에 있는 변수들을 32비트 float형태로 변경해주고, src_np라는 변수에 넣어준다.
      src_np = np.array(src, dtype=np.float32)

      # 만들어 놓은 이미지의 가로길이(width)와 세로길이(height)를 계산하는 부분
      # 윗 변의 가로길이와 아래변의 가로 측정하고 가장 큰 길이를 사용하겠다는 부분. norm은 사이의 길이를 구하겠다는 부분   
      width = max(np.linalg.norm(src_np[0] - src_np[1]), np.linalg.norm(src_np[2] - src_np[3]))
      # 옆 변의 세로 길이 두개를 측정하고 가장 큰 길이를 사용하겠다는 부분 
      height = max(np.linalg.norm(src_np[0] - src_np[3]), np.linalg.norm(src_np[1] - src_np[2]))

      # 참고이미지 동영상 (https://youtu.be/Bz8g83XbPk4?t=396)
      dst_np = np.array([
        [0, 0],
        [width, 0],
        [width, height],
        [0, height]
      ], dtype=np.float32)

      # dst_np와 src_np의 값을 getPerspectiveTransform에 넣어준다. 
      M = cv2.getPerspectiveTransform(src=src_np, dst=dst_np)
      #result = cv2.warpPerspective(ori_img, M=M, dsize=(width, height))
      # M값은 warpPerspective에 넣어준다. 
      result = cv2.warpPerspective(ori_img, M=M, dsize=(int(width), int(height)))

      cv2.imshow('result', result)
      cv2.imwrite('./result/%s_result%s' % (filename, ext), result)

# main
# 3.윈도우에 이름을 지정해준다.  
cv2.namedWindow('img')
# 4.img라고 지정된 윈도우에 마우스콜백 함수를 지정해줘서 마우스에 동작이 있으면 mouse_handler로 전달이 된다.
cv2.setMouseCallback('img', mouse_handler)
# 이미지를 띄운다. 
cv2.imshow('img', ori_img)
cv2.waitKey(0)