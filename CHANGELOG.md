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
