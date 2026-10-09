# 道路・建造物 クラック自動診断システム (Road Crack Detection AI)

AI（YOLOv8）を活用し、アップロードされた道路やコンクリートの写真からひび割れ（クラック）を自動検出・分析し、リスク評価を行うWebシステムです。

## 📌 背景と目的
地方自治体や建設業界におけるインフラ設備の老朽化に対し、目視点検の省力化・再現性向上を目指して開発した最小限の実用プロダクト（MVP）です。

## 🛠 システム構成・技術スタック
- **AI / 画像解析:** PyTorch, YOLOv8 (Object Detection)
- **バックエンド API:** Python, FastAPI, Uvicorn
- **フロントエンド UI:** Streamlit
- **開発・学習環境:** Google Colab (T4 GPU), Roboflow

## 🎯 工夫した点・精度向上のプロセス
1. **初期モデルの課題:** 
   汎用データセットで学習した初期モデルでは、薄いひび割れや質感によって検知漏れが発生していました。
2. **データ拡充と再学習:** 
   Roboflowから約2,000枚のひび割れ専門画像データセットを取得し、Google ColabのGPU環境にて50エポックの再学習（転移学習）を実施しました。
3. **成果:** 
   バウンディングボックスの位置精度および確信度（Confidence Score）が大幅に向上し、実用レベルでのひび割れ検出を実現しました。

## 🚀 セットアップ・起動方法

### 1. 依存ライブラリのインストール
```bash
pip install fastapi uvicorn ultralytics python-multipart pillow requests streamlit