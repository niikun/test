import requests
import pytesseract
from PIL import Image
from io import BytesIO
import streamlit as st

# 画像からテキストを抽出する関数
def extract_text_from_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    text = pytesseract.image_to_string(img, lang='jpn')
    return text

# Streamlit アプリ
def main():
    st.title('画像内テキスト検索')

    image_url = st.text_input('画像のURLを入力してください')
    keyword = st.text_input('キーワードを入力してください')

    if st.button('検索'):
        text = extract_text_from_image(image_url)
        if keyword in text:
            st.write('キーワードが見つかりました。')
        else:
            st.write('キーワードが見つかりませんでした。')

if __name__ == '__main__':
    main()
