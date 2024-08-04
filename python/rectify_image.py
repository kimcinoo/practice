# [사용법]
# 1. 준비물: input.jpg
# 2. 실행: python rectify_image.py
# 3. 결과: rectified_output.jpg (새 창에서 확인 가능)

import cv2
import numpy as np

def rectify_label(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    orig = image.copy()

    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 노이즈를 줄이기 위해 블러 적용
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 엣지를 감지하기 위해 캐니 엣지 검출기 적용
    edged = cv2.Canny(blurred, 50, 200, 255)

    # 윤곽선 찾기
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # 윤곽선이 사각형 모양인지 확인
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    for c in contour:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    # 라벨 부분을 추출하기 위해 원근 변환 적용
    rect = np.zeros((4, 2), dtype="float32")
    for i in range(4):
        rect[i] = screenCnt[i][0]

    rect[rect[:, 1].argsort()]
    top_left, top_right = rect[0], rect[1]
    bottom_right, bottom_left = rect[2], rect[3]

    width_top = np.linalg.norm(top_right - top_left)
    width_bottom = np.linalg.norm(bottom_right - bottom_left)
    height_left = np.linalg.norm(top_left - bottom_left)
    height_right = np.linalg.norm(top_right - bottom_right)
    max_width = max(int(width_top), int(width_bottom))
    max_height = max(int(height_left), int(height_right))

    dst = np.array([
        [max_width - 1, 0],
        [0, 0],
        [0, max_height - 1],
        [max_width - 1, max_height - 1]   
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(orig, M, (max_width, max_height))

    return warp

# 이미지 경로 설정
image_path = 'input.jpg'

# 라벨 반듯하게 만들기
rectified_label = rectify_label(image_path)

# 결과 이미지 저장
cv2.imwrite('rectified_output.jpg', rectified_label)

# 결과 이미지 보기
cv2.imshow("Rectified Label", rectified_label)
cv2.waitKey(0)
cv2.destroyAllWindows()