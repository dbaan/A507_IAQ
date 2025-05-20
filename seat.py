## seat.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import requests

# 좌표 딕셔너리
csp_points = {
    "1": (4.9, 5.85),  "2": (4.2, 5.85),  "3": (1.84, 5.85), "4": (1.16, 5.85),
    "5": (4.9, 4.6),   "6": (4.2, 4.6),   "7": (1.84, 4.6),  "8": (1.16, 4.6),
    "9": (4.9, 3.4),   "10": (4.2, 3.4),  "11": (1.84, 3.4), "12": (1.16, 3.4),
    "13": (4.9, 2.15), "14": (4.2, 2.15), "15": (1.84, 2.15),"16": (1.16, 2.15),
    "17": (4.9, 0.93), "18": (4.2, 0.93), "19": (1.84, 0.93),"20": (1.16, 0.93),
    "hrv": (5.1, 0.45),
}

# API URL 매핑
api_urls = {
    ("1","2"):  "https://api.thingspeak.com/channels/2943403/feeds.json?api_key=O12JYVOKYDYVA2HD&results=2",
    ("3","4"):  "https://api.thingspeak.com/channels/2943407/feeds.json?api_key=6QVPZ0QK0JPEUOZ5&results=2",
    ("5","6"):  "https://api.thingspeak.com/channels/2967888/feeds.json?api_key=6LJKU10BLAI27ZOB&results=2",
    ("7","8"):  "https://api.thingspeak.com/channels/2967889/feeds.json?api_key=5CNIXFX1HQCR7ADH&results=2",
    ("9","10"): "https://api.thingspeak.com/channels/2967891/feeds.json?api_key=13TFQSTTG3ABK3WJ&results=2",
    ("11","12"): "https://api.thingspeak.com/channels/2967894/feeds.json?api_key=2DKPZYVTAPMO7VAF&results=2",
    ("13","14"): "https://api.thingspeak.com/channels/2943404/feeds.json?api_key=8ZEOBBUOGU824AC6&results=2",
    ("15","16"): "https://api.thingspeak.com/channels/2943414/feeds.json?api_key=QCNGKKMQDOJ1Y0MM&results=2",
    ("17","18"): "https://api.thingspeak.com/channels/2967895/feeds.json?api_key=QNT10V4RA4YVGUHI&results=2",
    ("19","20"): "https://api.thingspeak.com/channels/2967896/feeds.json?api_key=BA9YKMHV1BFRY53S&results=2",
    "hrv":       "https://api.thingspeak.com/channels/2943401/feeds.json?api_key=I9HFOIOELN9CKVCS&results=2"
}


def plot_seats_with_pairs(points, occupied, ax):
    """
    points: 좌표 딕셔너리
    occupied: 재실자 좌석 번호의 집합 (예: {"1","2","4"})
    ax: matplotlib Axes
    """
    # 배경 이미지
    bg_img = plt.imread("A507.png")
    ax.imshow(bg_img, extent=[0,6,0,8], zorder=0)
    ax.set_aspect('equal', adjustable='box')

    # 1) 재실 좌석 사각형
    for key, (x,y) in points.items():
        if key == 'hrv':
            continue
        if key in occupied:
            rect = patches.Rectangle((x-0.2,y-0.2), 0.4,0.4,
                                     fill=True, facecolor='lightblue',
                                     edgecolor='black', linewidth=1.2, zorder=2)
            ax.add_patch(rect)
            ax.text(x, y, key, ha='center', va='center', fontsize=8, zorder=3)

    # 2) 쌍별 3등분 박스 + API 수치 표시
    pairs = [("1","2"),("3","4"),("5","6"),("7","8"),
             ("9","10"),("11","12"),("13","14"),("15","16"),
             ("17","18"),("19","20")]
    offset_y, height = 0.4, 0.4

    for pair in pairs:
        a,b = pair
        x1,y1 = points[a]; x2,y2 = points[b]
        left, right = min(x1,x2), max(x1,x2)
        width = (right-left)+0.4
        xs, ys = left-0.2, y1+offset_y
        # 외곽
        ax.add_patch(patches.Rectangle((xs,ys), width, height,
                                       fill=False, edgecolor='black', linewidth=1.2, zorder=1))
        # 분할선
        cw = width/3
        for i in (1,2):
            ax.plot([xs+cw*i]*2, [ys, ys+height], color='black', linewidth=1.0, zorder=1)
        # API
        ta=co2=pm="N/A"
        try:
            last = requests.get(api_urls[pair]).json()['feeds'][-1]
            ta  = last.get('field1',ta)
            co2 = last.get('field4',co2)
            pm  = last.get('field3',pm)
        except:
            pass
        yt = ys+height/2
        ax.text(xs+cw*0.5, yt, f"{ta}", ha='center', va='center', fontsize=5, zorder=2)
        ax.text(xs+cw*1.5, yt, f"{co2}", ha='center', va='center', fontsize=5, zorder=2)
        ax.text(xs+cw*2.5, yt, f"{pm}", ha='center', va='center', fontsize=5, zorder=2)

    # 3) HRV 3등분 박스
    hrv_x,hrv_y = points['hrv']
    off_x, w = -1.5, 1.2
    cw = w/3; ys = hrv_y - height/2
    ax.add_patch(patches.Rectangle((hrv_x+off_x, ys), w, height,
                                   fill=False, edgecolor='black', linewidth=1.2, zorder=1))
    for i in (1,2):
        ax.plot([hrv_x+off_x+cw*i]*2, [ys, ys+height], color='black', linewidth=1.0, zorder=1)
    ta=co2=pm="N/A"
    try:
        last = requests.get(api_urls['hrv']).json()['feeds'][-1]
        ta  = last.get('field1',ta)
        co2 = last.get('field4',co2)
        pm  = last.get('field3',pm)
    except:
        pass
    yt = hrv_y
    ax.text(hrv_x+off_x+cw*0.5, yt, f"{ta}", ha='center', va='center', fontsize=6, zorder=2)
    ax.text(hrv_x+off_x+cw*1.5, yt, f"{co2}", ha='center', va='center', fontsize=6, zorder=2)
    ax.text(hrv_x+off_x+cw*2.5, yt, f"{pm}", ha='center', va='center', fontsize=6, zorder=2)


    # 4) HRV 작은 풍량 박스 (always on)
    # 수정된 4) HRV 작은 풍량 박스 부분 (field1 값이 실수 문자열일 때도 처리)
    HRV_URL = "https://api.thingspeak.com/channels/2943401/feeds.json?api_key=I9HFOIOELN9CKVCS&results=2"
    try:
        data = requests.get(HRV_URL).json()
        val = float(data['feeds'][-1].get('field1', 0.0))
    except Exception as e:
        print("HRV API 호출 에러:", e)
        val = 0.0

    if val <= 10:
        color, label = 'white', 'off'
    elif 11 <= val <= 50:
        color, label = 'green', '150CMH'
    elif 51 <= val <= 80:
        color, label = 'yellow', '250CMH'
    elif val >= 80:
        color, label = 'red', '400CMH'
    else:
        color, label = 'lightgray', '?'

    ax.add_patch(patches.Rectangle((hrv_x - 0.2, hrv_y - 0.2), 0.4, 0.4,
                                   fill=True, facecolor=color,
                                   edgecolor='black', linewidth=1.2, zorder=4))
    ax.text(hrv_x, hrv_y, label, ha='center', va='center', fontsize=5, zorder=5)