import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def draw_court_diagram_final_params():
    # 図の設定
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 諸定数の設定 (模式的な値)
    court_width = 16
    court_height = 10
    
    # 原点等の設定
    center_x = 0
    center_y = 1.5  # フープの中心y座標
    
    # 3ポイントラインのパラメータ
    R = 6.0  # 半径
    straight_line_dist = 5.5 
    x_L = -straight_line_dist
    x_R = straight_line_dist
    
    # 直線と曲線の交点 y_int を計算
    dy = np.sqrt(R**2 - straight_line_dist**2)
    y_int = center_y + dy

    # 描画範囲の制限
    x_min, x_max = -8, 8
    y_min, y_max = 0, 9

    # ==========================================
    # 1. 領域の描画 (前回のロジックを維持)
    # ==========================================

    # --- コーナーエリア (緑の斜線) ---
    # 左コーナー
    rect_l = patches.Rectangle((x_min, y_min), x_L - x_min, y_int - y_min,
                               hatch='//', edgecolor='green', facecolor='none', linewidth=0)
    ax.add_patch(rect_l)
    
    # 右コーナー
    rect_r = patches.Rectangle((x_R, y_min), x_max - x_R, y_int - y_min,
                               hatch='//', edgecolor='green', facecolor='none', linewidth=0)
    ax.add_patch(rect_r)

    # --- トップエリア (青の斜線) ---
    # 円弧用のデータ (右から左へ)
    theta_start = np.arcsin((y_int - center_y) / R)
    theta_end = np.pi - theta_start
    thetas = np.linspace(theta_start, theta_end, 100)
    arc_x = center_x + R * np.cos(thetas)
    arc_y = center_y + R * np.sin(thetas)
    
    # パスの頂点リストを作成 (一筆書き順序：外枠 -> 内側のライン)
    poly_x = [x_min, x_max]
    poly_y = [y_max, y_max]
    poly_x.extend([x_max, x_R]) # 右上 -> 右接続点
    poly_y.extend([y_int, y_int])
    poly_x.extend(arc_x)        # 円弧 (右->左)
    poly_y.extend(arc_y)
    poly_x.extend([x_L, x_min, x_min]) # 左接続点 -> 左端 -> 左上
    poly_y.extend([y_int, y_int, y_max])
    
    # 多角形を描画
    poly = patches.Polygon(np.column_stack([poly_x, poly_y]), closed=True,
                           hatch='//', edgecolor='navy', facecolor='none', linewidth=0)
    ax.add_patch(poly)

    # ==========================================
    # 2. ラインの描画 (黒線)
    # ==========================================
    # 外枠
    ax.plot([x_min, x_max, x_max, x_min, x_min], [y_min, y_min, y_max, y_max, y_min], 'k-', lw=1.5)
    
    # 3ポイントライン
    ax.plot([x_L, x_L], [y_min, y_int], 'k-', lw=1.5)
    ax.plot([x_R, x_R], [y_min, y_int], 'k-', lw=1.5)
    ax.plot(arc_x, arc_y, 'k-', lw=1.5)
    
    # 制限区域、フリースローサークル
    key_width = 3.0
    ax.plot([-key_width/2, -key_width/2], [y_min, y_int+1], 'k-', lw=1)
    ax.plot([key_width/2, key_width/2], [y_min, y_int+1], 'k-', lw=1)
    ax.plot([-key_width/2, key_width/2], [y_int+1, y_int+1], 'k-', lw=1)
    circle = patches.Arc((center_x, y_int+1 - 1.5), 3, 3, theta1=0, theta2=180, linestyle='--', color='k')
    ax.add_patch(circle)
    
    # フープとバックボード（ゴール中心を明確にするため）
    ax.plot([-0.9, 0.9], [center_y - 0.2, center_y - 0.2], 'k-', lw=2) # ボード
    hoop = patches.Circle((center_x, center_y), 0.2, fill=False, color='k', lw=1.5) # リング
    ax.add_patch(hoop)

    # 境界線 (破線)
    ax.axhline(y=y_int, color='gray', linestyle='--', linewidth=1)
    # xL, xR の位置を示す縦の補助線（下の方だけ）
    ax.plot([x_L, x_L], [y_min, y_min+0.5], 'k-', lw=1)
    ax.plot([x_R, x_R], [y_min, y_min+0.5], 'k-', lw=1)

    # ==========================================
    # 3. テキストとパラメータの注釈 (ここを更新)
    # ==========================================
    ax.set_xticks([])
    ax.set_yticks([])
    font_size = 14
    
    # --- パラメータ: (cx, cy) ---
    # ゴール付近に座標を表示
    ax.text(center_x, center_y - 0.8, '$(c_x, c_y)$', ha='center', va='top', fontsize=font_size)
    # 点を打つ
    ax.plot(center_x, center_y, 'ko', markersize=4)

    # --- パラメータ: R ---
    # 中心から円弧に向かう矢印
    arrow_angle = np.pi / 3  # 60度方向に矢印
    arrow_x = center_x + R * np.cos(arrow_angle)
    arrow_y = center_y + R * np.sin(arrow_angle)
    # 矢印を描画
    ax.annotate('', xy=(arrow_x, arrow_y), xytext=(center_x, center_y),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    # テキスト R を矢印の中点付近に
    text_r_x = center_x + (R * 0.6) * np.cos(arrow_angle)
    text_r_y = center_y + (R * 0.6) * np.sin(arrow_angle)
    ax.text(text_r_x - 0.2, text_r_y + 0.2, '$R$', fontsize=font_size, fontweight='bold')

    # --- パラメータ: xL, xR ---
    # X軸上の位置にラベル
    ax.text(x_L, y_min - 0.3, '$x_L$', ha='center', va='top', fontsize=font_size)
    ax.text(x_R, y_min - 0.3, '$x_R$', ha='center', va='top', fontsize=font_size)

    # --- パラメータ: y_int ---
    # Y軸方向のラベル
    ax.text(x_min - 0.2, y_int, '$y_{int}$', ha='right', va='center', fontsize=font_size)

    # --- その他のラベル (エリア説明など) ---
    # コーナーエリア
    ax.text(x_min + 1.5, (y_min + y_int)/2, "Corner Area\n($y' \leq y_{int}$)", 
            ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    ax.text(x_max - 1.5, (y_min + y_int)/2, "Corner Area\n($y' \leq y_{int}$)", 
            ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    # トップエリア
    ax.text(0, y_int + 2.5, "Top Area ($y' > y_{int}$)", 
            ha='center', fontsize=12, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    # OUT表記
    ax.text(x_min + 1, y_max - 1, 'OUT (3pt)', ha='center', fontsize=12)
    ax.text(x_max - 1, y_max - 1, 'OUT (3pt)', ha='center', fontsize=12)

    # 軸ラベル
    ax.text(x_max + 0.2, y_min, 'X', ha='left', va='center', fontsize=12)
    ax.text(x_min - 0.2, y_max, 'Y', ha='right', va='center', fontsize=12)

    # グラフ範囲設定
    ax.set_xlim(x_min - 1.5, x_max + 1.5)
    ax.set_ylim(y_min - 1.0, y_max + 1)
    
    # 枠線
    ax.spines['right'].set_visible(True)
    ax.spines['top'].set_visible(True)
    
    plt.tight_layout()
    plt.savefig('3point_judge_params.png', dpi=300)
    plt.show()

# 関数を実行
draw_court_diagram_final_params()