import streamlit as st
from PIL import Image, ImageDraw
import io

def create_house_image(wall_color, roof_type, roof_color, number_of_windows):
    # 画像サイズを2倍にする
    image = Image.new('RGBA', (400, 400), color=(255, 255, 255, 0))  # 背景を透明に設定
    draw = ImageDraw.Draw(image)

    # 壁のサイズと位置を調整
    draw.rectangle([100, 200, 300, 360], fill=wall_color)

    # 屋根のタイプに応じてサイズと位置を調整
    if roof_type == 'たいらなやね':
        draw.rectangle([80, 160, 320, 200], fill=roof_color)
    else: # さんかくやね
        draw.polygon([80, 200, 200, 120, 320, 200], fill=roof_color)
 
    # 窓のサイズと位置を調整
    for i in range(number_of_windows):
        window_x = 120 + (i % 3) * 60  # 位置を調整
        window_y = 220 + (i // 3) * 50  # 位置を調整
        draw.rectangle([window_x, window_y, window_x + 40, window_y + 40], fill='lightblue')  # サイズを調整

    return image

def save_image(image):
    # PIL画像をバイトデータに変換する
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

# Streamlitのインターフェース設定
st.title('おうち デザイン ツール')

wall_color = st.color_picker('かべのいろは？', '#00f')
roof_type = st.selectbox('やねのかたちは', ['たいらなやね',  'さんかくやね'])
roof_color = st.color_picker('やねのいろは？', '#00f')
number_of_windows = st.slider('まどのかずは？', 0, 9, 1)

def process_image(base_img, img1):
    base_img.paste(img1, (310, 310))
    return base_img

def resize_and_pad(img, desired_size):
    w, h = img.size
    desired_w, desired_h = desired_size

    # アスペクト比を維持してリサイズ
    ratio = min(desired_w / w, desired_h / h)
    new_w = int(w * ratio)
    new_h = int(h * ratio)
    img = img.resize((new_w, new_h))

    # 新しい画像を生成して白で塗りつぶす
    new_img = Image.new("RGBA", desired_size, color=(255, 255, 255, 0))  # 完全透明な背景の白

    # 元の画像を左上に配置
    new_img.paste(img, (0, 0))

    return new_img

def make_background_transparent(image, bgcolor):
    # 画像をRGBAモードに変換
    image = image.convert("RGBA")
    
    # 透明背景の新しい画像を作成
    transparent_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    
    # 各ピクセルをチェックし、背景色の場合は透明に設定
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if pixel[:3] == bgcolor:
                transparent_image.putpixel((x, y), (0, 0, 0, 0))
            else:
                transparent_image.putpixel((x, y), pixel)
    
    return transparent_image


if st.button('おうちをつくる'):
    # 画像を生成して表示
    image = create_house_image(wall_color, roof_type, roof_color, number_of_windows)
    img1 = Image.open("img1.png")
    img1 = resize_and_pad(img1, (160, 160))
    # 背景を透過させる（ここでは白色の背景を透明にすると仮定）
    transparent_img1 = make_background_transparent(img1, (255,255,255))
    result = process_image(image,transparent_img1)
    st.image(result, caption='あなたのデザインしたおうち')

    # 画像をダウンロード可能なバイトデータに変換
    img_byte_arr = save_image(result)


    # ダウンロードボタンを提供
    st.download_button(label="画像をダウンロード",
                       data=img_byte_arr,
                       file_name="house_design.png",
                       mime="image/png")