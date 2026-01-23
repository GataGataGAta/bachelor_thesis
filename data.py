import matplotlib.pyplot as plt
import pandas as pd

def create_table_image():
    # データの定義
    data = {
        "Index": [str(i) for i in range(17)],
        "Key point": [
            "Nose", "Left-eye", "Right-eye", "Left-ear", "Right-ear",
            "Left-shoulder", "Right-shoulder", "Left-elbow", "Right-elbow",
            "Left-wrist", "Right-wrist", "Left-hip", "Right-hip",
            "Left-knee", "Right-knee", "Left-ankle", "Right-ankle"
        ]
    }
    
    df = pd.DataFrame(data)

    # 図の作成
    fig, ax = plt.subplots(figsize=(5, 8)) # 縦長に設定
    ax.axis('off')
    ax.axis('tight')

    # テーブルの作成
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     loc='center',
                     cellLoc='left',
                     colWidths=[0.2, 0.6]) # 列の幅を調整

    # スタイルの適用（Excel風のデザイン）
    header_color = '#4472C4'  # ヘッダーの濃い青
    row_colors = ['#D9E1F2', 'white']  # 縞模様の色（薄い青、白）
    border_color = 'white'    # 枠線の色

    # フォントサイズ設定
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1, 2) # 行の高さを広げる

    # 各セルの詳細設定
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(border_color) # 枠線を白にする
        cell.set_linewidth(1)
        
        # ヘッダー (row=0)
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color='white', weight='bold')
            cell.set_height(0.08)
        # データ行
        else:
            # 縞模様の設定 (行番号に基づいて色を切り替え)
            # 元画像に合わせてIndex 0(row 1)が薄い青になるように設定
            bg_color = row_colors[(row - 1) % 2]
            cell.set_facecolor(bg_color)
            cell.set_text_props(color='black')
            cell.set_height(0.05)
            
            # テキストのパディング（左寄せをきれいにするため）
            text = cell.get_text()
            text.set_x(0.05) # 左端からの余白

    # 画像として保存
    plt.savefig('keypoints_table.png', bbox_inches='tight', dpi=300, pad_inches=0.1)
    plt.show()

# 関数を実行
create_table_image()