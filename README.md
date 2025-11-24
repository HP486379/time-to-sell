# time-to-sell

Utility scripts and a Streamlit prototype for the "S&P500 売り時ダッシュボード v1".

## プロジェクトのコピー

`.git` やキャッシュを除外してローカルに丸ごとコピーするには次を実行します。

```bash
python scripts/copy_project.py path/to/destination
```

追加で除外したいパターンがある場合は `--ignore pattern` を複数指定できます。リポジトリ履歴ごとコピーしたい場合は `--include-git` を付けてください。

## Streamlit デモの実行

依存関係をインストールします。

```bash
pip install -r requirements.txt
```

Streamlit アプリを起動します。

```bash
streamlit run nisa_sp500_timing/app.py
```

サイドバーに保有数量と平均取得単価を入力すると、テクニカル・マクロ・イベント補正にもとづく売り時スコアと判定ラベルが表示されます。

## テスト

スコアロジックに対する簡易テストは `pytest` で実行できます。

```bash
pytest -q
```
