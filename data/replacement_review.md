# 代替写真の調査（2026-10-15）

## KSDL画像1：代替候補

- 出典：https://commons.wikimedia.org/wiki/File:SDL_SCOTTSDALE_AIRPORT_FROM_FLIGHT_TUS-LAS_737_N748SW_(10500329945)_(2).jpg
- 原画像：https://upload.wikimedia.org/wikipedia/commons/4/44/SDL_SCOTTSDALE_AIRPORT_FROM_FLIGHT_TUS-LAS_737_N748SW_%2810500329945%29_%282%29.jpg
- 著作者：Eric Salard。撮影日：2013-07-30。
- 実ファイル確認：JPEG、2308 × 1539、横長。SHA-256：`d0af97b265eb28fe77599cc28dfd62b6d05c104332288bac48fbee79a6bd58e6`。
- 目視：屋外の実写空撮。滑走路、誘導路、駐機場、格納庫群が写る。目立つ透かしは認めない。実写の出典・撮影情報あり（AI生成を技術的に完全否定したものではない）。
- 独立照合資料：https://commons.wikimedia.org/wiki/File:Scottsdale_Airport-2006-USGS.jpg （USGSの2006年航空写真）。画像を実際に取得して目視比較。
- 一致点：単一の長い滑走路、両側の平行誘導路、西側の広い駐機場、連続した細長い格納庫と周辺の道路・建物群の相対配置。画像の回転と撮影年代差を考慮。
- 出典の位置指定は33.621838, -111.912832だが、EXIFは33°32′32.74″N / 112°0′50.14″W。対象位置と撮影機位置の可能性があり、位置タグだけでは確定しない。
- Google MapsはJavaScriptが必要というページまで取得。操作可能な地図表示は検証できておらず、Google Maps / Earthの3D照合済みとはしない。
- ライセンス：CC BY-SA 2.0。出典ページで確認。著作者表示、ライセンスへのリンク、改変の表示、改変時の継承条件等を要確認。https://creativecommons.org/licenses/by-sa/2.0/
- 提出CSVには承認待ちの候補として記録。古い写真である点を明示。

## KAPA：代替2枚は未確定

- 公式航空写真PDFを取得・目視し、照合の基準資料とした：https://www.centennialairport.com/files/e3a6747bd/23.+Airport+Aerial.pdf
- NASA宇宙撮影の候補：https://commons.wikimedia.org/wiki/File:ISS016-E-16598_-_View_of_Colorado.jpg 。3032 × 2008、NASA由来、米国でPublic Domainと記載。実画像の空港滑走路の相対配置は公式航空写真と整合するが、雪景色で空港が小さく、鮮明で空港中心の構図という観点から保留。提出URLには追加しない。
- 管制塔写真2件は縦長（533 × 800、1252 × 1300）。別の塔写真は442 × 409で出典にもぼけの注意があるため除外。
- Dassault Falcon 900、Learjet、Gulfstream等の写真は航空機が主役で、空港を識別する資料として弱く、採用しない。
- 公式トップページに別候補の画像DSC005071.JPGがある：https://www.centennialairport.com/ 。画像配信先 `streamline.imgix.net` はプロキシの403で取得不可。画像そのもの・寸法・利用条件は未確認。公式サイトはCopyright表記があり、公開されていることを転載許可とは扱わない。

## 現在の件数

提出CSV：4空港・8候補URL（2枚ずつ）。KAPAの代替2枚は未確定。不採用3件の履歴は証拠一覧に保持し、再採用しない。地理照合済みという今回の判断は新しいKSDL候補のみを対象とし、以前の7候補全件に拡張しない。

## 追跡調査（2026-10-15・ブラウザ検証）

- ユーザー承認を得て環境提供プロキシCAの登録を実施。証明書の指紋比較により、同じCAが既存の `OpenAI-nebula-dns` としてすでに登録済みと判明。CA不足という診断は訂正。
- 通常の制限付きブラウザでは信頼ストア利用に問題がある一方、許可された実行条件ではTLS検証を有効にしたまま空港公式サイトを閲覧できた。
- Google検索は共有ネットワークへのアクセス確認画面となり、検索結果を取得できなかった。確認画面の回避は行わない。
- 保存済み設定には `streamline.imgix.net` が含まれているが、公式トップページのJPEGおよび紹介ページの6件の画像URLは、通信プロキシのCONNECT 403で取得できなかった。設定の保存だけでは現在の通信の成功を確認できない。
- 新たに確認した紹介ページ：https://www.centennialairport.com/discover-centennial-airport-kapa 。画像自体・解像度・用途別の利用許諾は未確認。
- 公式プライバシーポリシーも確認したが、写真の転載を許可する条件は確認できなかった。公開ページにあることを利用許諾とは扱わない。
- この追跡調査で採用に足るKAPA代替写真は確認できていない。提出CSV・写真証拠CSV・Excelの内容は変更しない。
