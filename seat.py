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
    # 공통 상수
    pair_offset_y = 0.4
    height       = 0.4   # 이전에 pair_height 역할

    # 배경
    bg_img = plt.imread("A507.png")
    ax.imshow(bg_img, extent=[0, 6, 0, 8], zorder=0)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([]); ax.set_yticks([])

    # 1) 재실 좌석
    for key, (x, y) in points.items():
        if key == 'hrv': continue
        if key in occupied:
            ax.add_patch(patches.Rectangle((x-0.2, y-0.2), 0.4, 0.4,
                                           fill=True, facecolor='lightblue',
                                           edgecolor='black', linewidth=1.2, zorder=2))
            ax.text(x, y, key, ha='center', va='center', fontsize=8, zorder=3)

    # 2) 페어별 3등분 박스 + 값·수신 시간
    pairs = [("1","2"),("3","4"),("5","6"),("7","8"),
             ("9","10"),("11","12"),("13","14"),("15","16"),
             ("17","18"),("19","20")]
    for pair in pairs:
        a, b = pair
        x1, y1 = points[a]; x2, y2 = points[b]
        left, right = min(x1, x2), max(x1, x2)
        width = (right-left) + 0.4
        xs, ys = left-0.2, y1 + pair_offset_y

        # 외곽 + 분할선
        ax.add_patch(patches.Rectangle((xs, ys), width, height,
                                       fill=False, edgecolor='black',
                                       linewidth=1.2, zorder=1))
        cw = width/3
        for i in (1,2):
            ax.plot([xs+cw*i]*2, [ys, ys+height],
                    color='black', linewidth=1, zorder=1)

        # API 값과 수신 시간
        ta = co2 = pm = "N/A"
        recv_time = "N/A"
        try:
            resp = requests.get(api_urls[pair]).json()
            last = resp['feeds'][-1]
            ta   = last.get('field1', ta)
            co2  = last.get('field4', co2)
            pm   = last.get('field3', pm)
            ts   = last.get('created_at')
            if ts:
                recv_time = ts.split("T")[1].replace("Z","")
        except:
            pass

        # 값 표시
        yt = ys + height/2
        ax.text(xs+cw*0.5, yt, f"{ta}",  ha='center', va='center', fontsize=5, zorder=2)
        ax.text(xs+cw*1.5, yt, f"{co2}", ha='center', va='center', fontsize=5, zorder=2)
        ax.text(xs+cw*2.5, yt, f"{pm}",  ha='center', va='center', fontsize=5, zorder=2)

        # 수신 시간 표시 (박스 우측 아래)
        ax.text(xs + width + 0.02, ys, recv_time,
                ha='left', va='bottom', fontsize=5, color='gray', zorder=2)

    # 3) HRV 3등분 박스 + 값·수신 시간
    hrv_x, hrv_y   = points['hrv']
    hrv_off_x, hrv_w = -1.5, 1.2
    cw             = hrv_w / 3
    ys             = hrv_y - height/2

    ax.add_patch(patches.Rectangle((hrv_x+hrv_off_x, ys),
                                   hrv_w, height,
                                   fill=False, edgecolor='black',
                                   linewidth=1.2, zorder=1))
    for i in (1,2):
        ax.plot([hrv_x+hrv_off_x+cw*i]*2,
                [ys, ys+height],
                color='black', linewidth=1, zorder=1)

    ta = co2 = pm = "N/A"
    recv_time_hrv = "N/A"
    try:
        resp = requests.get(api_urls['hrv']).json()
        last = resp['feeds'][-1]
        ta   = last.get('field1', ta)
        co2  = last.get('field4', co2)
        pm   = last.get('field3', pm)
        ts   = last.get('created_at')
        if ts:
            recv_time_hrv = ts.split("T")[1].replace("Z","")
    except:
        pass

    # 값 표시
    ax.text(hrv_x+hrv_off_x+cw*0.5, hrv_y, f"{ta}",  ha='center', va='center', fontsize=5, zorder=2)
    ax.text(hrv_x+hrv_off_x+cw*1.5, hrv_y, f"{co2}", ha='center', va='center', fontsize=5, zorder=2)
    ax.text(hrv_x+hrv_off_x+cw*2.5, hrv_y, f"{pm}",  ha='center', va='center', fontsize=5, zorder=2)

    # 수신 시간 (3등분 박스 아래)
    center_x = hrv_x + hrv_off_x + hrv_w/2
    ax.text(center_x, ys - 0.02, recv_time_hrv,
            ha='center', va='top', fontsize=5, color='gray', zorder=2)

    # 4) HRV 작은 풍량 박스 + 수신 시간
    try:
        data = requests.get(api_urls['hrv']).json()
        val  = float(data['feeds'][-1].get('field1', 0.0))
    except:
        val = 0.0

    if val <= 10:
        color, label = 'white','off'
    elif 30 <= val <= 50:
        color, label = 'green','150CMH'
    elif 60 <= val <= 80:
        color, label = 'yellow','250CMH'
    else:
        color, label = 'red','400CMH'

    ax.add_patch(patches.Rectangle((hrv_x-0.2, hrv_y-0.2), 0.4, 0.4,
                                   fill=True, facecolor=color,
                                   edgecolor='black', linewidth=1.2, zorder=5))
    ax.text(hrv_x, hrv_y, label, ha='center', va='center', fontsize=5, zorder=6)

    # 작은 박스 수신 시간
    ax.text(hrv_x, hrv_y - height/2 - 0.05, recv_time_hrv,
            ha='center', va='top', fontsize=5, color='gray', zorder=6)

    # 5) 범례 (생략 가능)
    legend_ax = ax.figure.add_axes([0.40, 0.02, 0.3, 0.12])
    legend_ax.axis('off')
    from matplotlib.patches import Rectangle as LegRect
    lw, lh = 0.8, 0.3
    cellw   = lw/3
    legend_ax.add_patch(LegRect((0,0.4), cellw, lh, facecolor='white', edgecolor='black'))
    legend_ax.add_patch(LegRect((cellw,0.4), cellw, lh, facecolor='white', edgecolor='black'))
    legend_ax.add_patch(LegRect((2*cellw,0.4), cellw, lh, facecolor='white', edgecolor='black'))
    legend_ax.text(cellw/2, 0.15, "Ta(℃)", ha='center', va='center', fontsize=6)
    legend_ax.text(cellw*1.5, 0.15, "CO2(ppm)", ha='center', va='center', fontsize=6)
    legend_ax.text(cellw*2.5, 0.15, "PM2.5(㎍/㎥)", ha='center', va='center', fontsize=6)

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 8)
    ax.axis('off')