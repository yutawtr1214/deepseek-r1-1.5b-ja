# Deepseek-r1:1.5b-ja

このプロジェクトは[Masato13](https://zenn.dev/masato13)さんの[Deepseek-r1:1.5bを日英翻訳付きで快適に使う方法](https://zenn.dev/masato13/articles/5af9d8d0f60b2b)を参考にさせていただきました。

## 概要
このプロジェクトはローカルリソース上で、Deepseek-r1:1.5bモデルを使用して、日本語での入力を受け付け、日本語⇔英語の自動翻訳を行い応答生成を行うチャットボットです。

## 機能

- 日本語での入力を受け付け
- 日本語⇔英語の自動翻訳
- 会話履歴を考慮した応答生成
- ストリーミング形式での応答表示

## テスト環境
- ホストOS: Windows 11
- CPU: 13th Gen Intel(R) Core(TM) i5-1335U   1.30 GHz
- GPU: なし
- RAMM 16.0 GB

## 使用技術

- Python 3.10
- Ollama (AIモデルサーバー)
- LangChain (LLMフレームワーク)
- Docker & Docker Compose

## 使用モデル

- 翻訳: 7shi/gemma-2-jpn-translate:2b-instruct-q8_0
- 推論: deepseek-r1:1.5b

## セットアップ方法

1. リポジトリをクローン

```
git clone <repository-url>
cd <repository-name>
```


2. Docker ollamaコンテナを起動
```
docker-compose up -d ollama
```

3. モデルのダウンロード(PoweShellの場合)
- deepseek-r1:1.5b
```
docker exec -it (docker ps -q -f name=ollama) ollama pull deepseek-r1:1.5b
```

- 7shi/gemma-2-jpn-translate:2b-instruct-q8_0
```
docker exec -it (docker ps -q -f name=ollama) ollama pull 7shi/gemma-2-jpn-translate:2b-instruct-q8_0
```

4. サービスを起動
```
docker-compose run --rm app
```

## 使用方法

1. サービスが起動すると、対話型のチャットインターフェースが表示されます
2. 日本語で質問や指示を入力してください
3. システムが以下の3ステップで処理を行います：
   - 入力を英語に翻訳
   - 英語で回答を生成
   - 回答を日本語に翻訳
4. 終了するには「exit」と入力してください

## プロジェクト構成

- `main.py`: メインのアプリケーションコード
- `Dockerfile`: アプリケーションのコンテナ化設定
- `docker-compose.yml`: サービスの構成定義
- `requirements.txt`: Pythonの依存パッケージリスト

