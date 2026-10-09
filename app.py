import base64
import io
from PIL import Image
import requests
import streamlit as st

st.set_page_config(page_title="クラック自動診断システム", layout="centered")

st.title(" 道路・建造物 クラック自動診断システム")
st.write(
    "写真をアップロードすると、AIがひび割れ（クラック）箇所を自動で検出・分析します。"
)

# 画像アップロード
uploaded_file = st.file_uploader(
    "診断したい写真を選択してください", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  # アップロード画像を表示
  st.image(
      uploaded_file, caption="アップロードされた画像", use_container_width=True
  )

  if st.button("AIで診断を実行する"):
    with st.spinner("AIが画像を解析中..."):
      try:
        # FastAPI (main.py) に画像を送信
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }
        response = requests.post("http://127.0.0.1:8000/predict", files=files)

        if response.status_code == 200:
          data = response.json()

          st.markdown("---")
          st.subheader(" 診断結果")

          # 検出数の表示
          st.metric(
              label="検出されたクラック数",
              value=f"{data['crack_count']} 箇所",
          )

          # 判定結果の色分け表示
          risk = data["risk_level"]
          if "危険" in risk:
            st.error(f"判定: {risk}")
          elif "要観察" in risk:
            st.warning(f"判定: {risk}")
          else:
            st.success(f"判定: {risk}")

          # 検出結果画像を表示
          img_data = base64.b64decode(data["result_image_base64"])
          result_img = Image.open(io.BytesIO(img_data))
          st.image(
              result_img,
              caption="AI解析画像 (検出枠表示)",
              use_container_width=True,
          )

        else:
          st.error("APIでの処理に失敗しました。")

      except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.info("FastAPIサーバー (main.py) が起動しているか確認してください。")