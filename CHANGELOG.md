# Changelog — Airport Photo Sourcing Automation

## 2026-10-15 — 初回成果物（Pilot）

### 追加
- `data/airport_photo_sourcing_102_pilot.xlsx`：4シート（Overview / Submission / Airports_102 / Photo_Evidence）の収集成果物を配置。
- `data/airports_102.csv`：世界102空港の自主選定候補を登録。
- `data/submission.csv`：納品仕様の4列を用意し、5空港分の画像URL10件を記録。
- `data/photo_evidence.csv`：画像10件の出典ページ・原画像URL・画像寸法・撮影者・ライセンス・確認メモを記録。
- `data/overview.csv`：件数と参照情報を記録。
- `WORKFLOW.md`：調査・同一性確認・画像品質と権利確認・提出の手順を作成。
- `CHANGELOG.md`：独立した変更履歴を開始。

### 維持するもの
- 既存の `README.md`（案件原文）は変更しない。

### 未着手・未完了
- 正式な依頼主提供CSVとの照合（現在の102空港は自主選定）。
- 残り97空港、194枚の調査。
- 既存10枚の独立した地理照合、用途別ライセンス確認。
- 写真自動収集・自動判定プログラムの実装。

## 2026-10-15 — 提出用CSVを5空港に限定

- `data/submission.csv` から画像URLが空欄の97空港を除き、2枚の候補URLがある5空港のみを保持。
- ヘッダーと既存5空港のデータは保持。Excelおよび102空港の一覧は変更なし。

## 2026-10-15 — 写真候補3件を不採用に変更

- ユーザー指定のKAPA写真1・2、KSDL写真1を不採用として証拠一覧に保持。
- CSVとExcelの提出URLから該当3件を除外。CSVは全URL空欄となったKAPA行も除外（4空港・7候補URL）。
- 空港一覧、集計、Excelを更新。有効候補2枚が揃うのは3空港。
- 代替候補未確認：Wikimediaへの検索接続はプロキシの403で失敗。

## 2026-10-15 — KSDLの代替空撮候補を追加

- KSDL画像1にEric Salardの2013年空撮を追加。原画像・寸法・出典ライセンスを確認し、独立したUSGS航空写真と配置を目視比較。承認待ちとして記録。
- CSV・Excel・集計を同期（4空港・8候補URL）。不採用3件の履歴は保持。
- `data/replacement_review.md` に根拠、除外候補、KAPA代替2枚の未完了事項を記録。Google Mapsの実表示・3D照合は未実施。
