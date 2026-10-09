import base64
import io
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from ultralytics import YOLO

app = FastAPI(title="Road Crack Detection API")

# 同一フォルダ内の best.pt を読み込む
model = YOLO("best.pt")


@app.post("/predict")
async def predict_crack(file: UploadFile = File(...)):
  # 1. アップロードされた画像を受け取る
  image_bytes = await file.read()
  image = Image.open(io.BytesIO(image_bytes))

  # 2. YOLOv8で画像解析を実行
  results = model(image, conf=0.10)
  result = results[0]

  # 3. 検出されたひび割れの個数をカウント
  crack_count = len(result.boxes)

  # 4. リスク評価ロジック
  if crack_count == 0:
    risk_level = "健全 (ひび割れは検出されませんでした)"
  elif crack_count <= 2:
    risk_level = "要観察 (軽微なひび割れがあります)"
  else:
    risk_level = "危険・要補修 (多数のひび割れが検出されました)"

  # 5. 検出枠が描画された画像を生成し、Base64文字列に変換
  res_plotted = result.plot()
  res_image = Image.fromarray(res_plotted[..., ::-1])  # BGR -> RGB
  buffered = io.BytesIO()
  res_image.save(buffered, format="JPEG")
  img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

  # 6. 解析結果を返却
  return {
      "crack_count": crack_count,
      "risk_level": risk_level,
      "result_image_base64": img_str,
  }