import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_court(ax=None, color='#CDB38B', lw=2):
    if ax is None:
        ax = plt.gca()

    # コートの寸法 (メートル)
    length = 28.0
    width = 15.0
    
    # 背景（コートの色）
    court = patches.Rectangle((-length/2, -width/2), length, width, linewidth=lw, color=color)
    ax.add_patch(court)

    # ラインの色
    line_color = 'white'

    # 外枠
    plt.plot([-length/2, length/2], [width/2, width/2], color='black', linewidth=lw*1.5) # 上（サイドライン）
    plt.plot([-length/2, length/2], [-width/2, -width/2], color='black', linewidth=lw*1.5) # 下（サイドライン）
    plt.plot([-length/2, -length/2], [-width/2, width/2], color='black', linewidth=lw*1.5) # 左（エンドライン）
    plt.plot([length/2, length/2], [-width/2, width/2], color='black', linewidth=lw*1.5) # 右（エンドライン）

    # センターライン
    plt.plot([0, 0], [-width/2, width/2], color=line_color, linewidth=lw)

    # センターサークル (半径1.8m)
    center_circle = patches.Circle((0, 0), 1.8, linewidth=lw, edgecolor=line_color, facecolor='none')
    ax.add_patch(center_circle)

    # フープの中心座標 (エンドラインから1.575m)
    hoop_offset = 1.575
    hoop_left = -length/2 + hoop_offset
    hoop_right = length/2 - hoop_offset

    # 3ポイントライン (半径6.75m)
    three_pt_radius = 6.75
    # サイドラインからの距離 0.9m
    side_margin = 0.90
    
    # 左側の3ポイントライン
    # 直線部分
    plt.plot([-length/2, -length/2 + 2.99], [width/2 - side_margin, width/2 - side_margin], color=line_color, linewidth=lw) # 上
    plt.plot([-length/2, -length/2 + 2.99], [-width/2 + side_margin, -width/2 + side_margin], color=line_color, linewidth=lw) # 下
    # 弧の部分
    theta = np.linspace(-np.pi/2, np.pi/2, 100)
    # 直線部分との交差判定で角度を制限する必要があるが、簡易的に描画
    # アークの定義: フープ中心から6.75m。y座標が width/2 - 0.9 を超えない範囲
    max_y = width/2 - side_margin
    # y = r * sin(theta) => theta = asin(y/r)
    limit_angle = np.arcsin(max_y / three_pt_radius)
    theta_left = np.linspace(-limit_angle, limit_angle, 100)
    
    x_arc_left = hoop_left + three_pt_radius * np.cos(theta_left)
    y_arc_left = three_pt_radius * np.sin(theta_left)
    plt.plot(x_arc_left, y_arc_left, color=line_color, linewidth=lw)
    # 直線部分と弧をつなぐ線（厳密には上のplotでカバーされるはずだが微調整）
    plt.plot([-length/2, hoop_left + three_pt_radius * np.cos(limit_angle)], [max_y, max_y], color=line_color, linewidth=lw)
    plt.plot([-length/2, hoop_left + three_pt_radius * np.cos(limit_angle)], [-max_y, -max_y], color=line_color, linewidth=lw)


    # 右側の3ポイントライン
    x_arc_right = hoop_right - three_pt_radius * np.cos(theta_left) # 反転
    plt.plot(x_arc_right, y_arc_left, color=line_color, linewidth=lw)
    plt.plot([length/2, hoop_right - three_pt_radius * np.cos(limit_angle)], [max_y, max_y], color=line_color, linewidth=lw)
    plt.plot([length/2, hoop_right - three_pt_radius * np.cos(limit_angle)], [-max_y, -max_y], color=line_color, linewidth=lw)

    # 制限区域 (長方形) 幅4.9m, 長さ5.8m (エンドラインから)
    key_width = 4.9
    key_length = 5.8
    
    # 左
    rect_left = patches.Rectangle((-length/2, -key_width/2), key_length, key_width, linewidth=lw, edgecolor=line_color, facecolor='none')
    ax.add_patch(rect_left)
    # 右
    rect_right = patches.Rectangle((length/2 - key_length, -key_width/2), key_length, key_width, linewidth=lw, edgecolor=line_color, facecolor='none')
    ax.add_patch(rect_right)

    # フリースローサークル (半径1.8m)
    # 左
    fs_circle_left = patches.Arc((-length/2 + 5.8, 0), 3.6, 3.6, theta1=-90, theta2=90, linewidth=lw, edgecolor=line_color)
    ax.add_patch(fs_circle_left)
    fs_circle_left_dash = patches.Arc((-length/2 + 5.8, 0), 3.6, 3.6, theta1=90, theta2=270, linewidth=lw, edgecolor=line_color, linestyle='--')
    ax.add_patch(fs_circle_left_dash)
    
    # 右
    fs_circle_right = patches.Arc((length/2 - 5.8, 0), 3.6, 3.6, theta1=90, theta2=270, linewidth=lw, edgecolor=line_color)
    ax.add_patch(fs_circle_right)
    fs_circle_right_dash = patches.Arc((length/2 - 5.8, 0), 3.6, 3.6, theta1=-90, theta2=90, linewidth=lw, edgecolor=line_color, linestyle='--')
    ax.add_patch(fs_circle_right_dash)

    # ノーチャージセミサークル (半径1.25m)
    nc_radius = 1.25
    nc_left = patches.Arc((hoop_left, 0), nc_radius*2, nc_radius*2, theta1=-90, theta2=90, linewidth=lw, edgecolor=line_color)
    ax.add_patch(nc_left)
    nc_right = patches.Arc((hoop_right, 0), nc_radius*2, nc_radius*2, theta1=90, theta2=270, linewidth=lw, edgecolor=line_color)
    ax.add_patch(nc_right)

    # バックボード (エンドラインから1.2m) 幅1.8m
    bb_offset = 1.2
    bb_width = 1.8
    plt.plot([-length/2 + bb_offset, -length/2 + bb_offset], [-bb_width/2, bb_width/2], color='white', linewidth=lw)
    plt.plot([length/2 - bb_offset, length/2 - bb_offset], [-bb_width/2, bb_width/2], color='white', linewidth=lw)

    # ゴールリム (オレンジ) 半径0.225m
    rim_radius = 0.225
    rim_left = patches.Circle((hoop_left, 0), rim_radius, linewidth=lw, edgecolor='#FFA500', facecolor='none')
    ax.add_patch(rim_left)
    rim_right = patches.Circle((hoop_right, 0), rim_radius, linewidth=lw, edgecolor='#FFA500', facecolor='none')
    ax.add_patch(rim_right)


    # --- 寸法線の描画 ---
    
    # フォントサイズ設定 (ここを大きくする)
    FONT_SIZE_LARGE = 40 # 元の画像よりかなり大きく設定
    FONT_SIZE_MED = 18

    # 1. "28m" (上部中央)
    plt.text(0, width/2 + 0.8, "28m", ha='center', va='center', fontsize=FONT_SIZE_LARGE, color='black')

    # 2. "0.90m" (四隅の矢印)
    arrow_props = dict(facecolor='black', arrowstyle='<->', linewidth=1.5)
    
    # 左上
    ax.annotate('', xy=(-length/2 + 1.5, width/2), xytext=(-length/2 + 1.5, width/2 - side_margin), arrowprops=arrow_props)
    plt.text(-length/2 + 2.0, width/2 - side_margin/2, "0.90m", ha='left', va='center', fontsize=FONT_SIZE_MED)
    
    # 右上
    ax.annotate('', xy=(length/2 - 1.5, width/2), xytext=(length/2 - 1.5, width/2 - side_margin), arrowprops=arrow_props)
    plt.text(length/2 - 2.0, width/2 - side_margin/2, "0.90m", ha='right', va='center', fontsize=FONT_SIZE_MED)

    # 左下
    ax.annotate('', xy=(-length/2 + 1.5, -width/2), xytext=(-length/2 + 1.5, -width/2 + side_margin), arrowprops=arrow_props)
    plt.text(-length/2 + 2.0, -width/2 + side_margin/2, "0.90m", ha='left', va='center', fontsize=FONT_SIZE_MED)
    
    # 右下
    ax.annotate('', xy=(length/2 - 1.5, -width/2), xytext=(length/2 - 1.5, -width/2 + side_margin), arrowprops=arrow_props)
    plt.text(length/2 - 2.0, -width/2 + side_margin/2, "0.90m", ha='right', va='center', fontsize=FONT_SIZE_MED)


    # 3. "6.75m" (3ポイントラインの半径)
    # 左側のみ描画 (画像参考)
    # フープから斜め上に矢印
    angle = np.pi / 4 # 45度
    start_x = hoop_left
    start_y = 0
    end_x = hoop_left + three_pt_radius * np.cos(angle)
    end_y = three_pt_radius * np.sin(angle)
    
    ax.annotate('', xy=(start_x, start_y), xytext=(end_x, end_y), arrowprops=dict(facecolor='black', arrowstyle='<->', linewidth=1.5))
    
    # 文字の位置 (線の真ん中より少し外側)
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    plt.text(mid_x + 0.5, mid_y - 0.5, "6.75m", ha='left', va='top', fontsize=FONT_SIZE_LARGE)


    # 軸の設定
    ax.set_xlim(-length/2 - 1, length/2 + 1)
    ax.set_ylim(-width/2 - 1.5, width/2 + 1.5)
    ax.set_aspect('equal')
    plt.axis('off') # 軸を消す

# 描画実行
plt.figure(figsize=(14, 8), facecolor='white') # 画像サイズを大きめに
draw_court(color='#D2B48C') # 色を画像に合わせて調整
plt.tight_layout()
plt.show()