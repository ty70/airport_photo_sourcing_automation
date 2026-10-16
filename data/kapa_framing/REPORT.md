# KAPA：座標から決める航空写真の範囲・向きの実験

実施日：2026-10-16。今回は構図の実証であり、royalty-free納品写真の確保完了ではない。

## 結果

横長3:2、空港外周の各辺に10%ずつ余白を加え、さらに縦横比に合わせて枠を拡大した。切り落として横長にはしていない。

| 指標 | 北を上 | 主滑走路に合わせる |
| --- | ---: | ---: |
| 地上範囲（画像の横×縦） | 6.961 × 4.641 km | 4.658 × 3.105 km |
| 面積 | 32.305 km² | 14.464 km² |
| 枠に占めるOSM空港外周内の面積 | 約13.2% | 約29.5% |
| 2400×1600で出力したときの地上間隔 | 約2.90 m/画素 | 約1.94 m/画素 |
| 仮に1 m/画素の実データで確保するなら | 6962×4641画素 | 4658×3106画素 |
| 今回の参考画像が枠を覆える割合（概略位置合わせ） | 約49.8% | 100% |

滑走路に合わせると、同じ空港全体を含む枠の面積は約55.2%小さくなる。同じ出力画素数なら、線方向の細部の大きさは約1.49倍になる。面積倍率2.23倍と線方向の倍率を混同しない。

主滑走路はUTM座標で北から時計回り約177.86°の方向に延びる。右向きを南寄りに合わせるので、回転後の画像では北がおおむね左になる。表示の回転であり、斜めからの撮影や3D視点は作っていない。

`frame_geometry.svg` は写真を含まない地理範囲の図。`frames.geojson` は両構図の四隅をWGS84経緯度で保存している。回転枠は四隅を使い、単純な経緯度bboxをそのまま横長写真の枠とは扱わない。

## 元データ

- OSM空港外周：way 427832843、ICAO=KAPA、Centennial Airport。閉じた398頂点の外周。法的な敷地境界を証明するデータではない。
- 滑走路中心線：way 34541383（17L/35R）、23329836（17R/35L）、49908107（10/28）。
- 主滑走路の座標からの長さ：約3045.4 m。FAA図の10001 ft（約3048.3 m）と概ね整合する。OSMの`length`属性に単位がないため、これをメートルとして計算に使っていない。
- 計算はEPSG:32613（WGS84 / UTM zone 13N）で行い、経度・緯度を同じ距離単位として扱っていない。
- OSM取得経路・wayの版・更新日時は `airport_geometry.geojson` に保存。必要な全頂点が取得されていることを確認した。広い範囲のAPI取得は50000ノード制限で失敗したが、分割取得した2領域に対象4wayと全参照ノードがそろった。
- OSM由来データ・図：© OpenStreetMap contributors、[ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)、[著作権・帰属表示](https://www.openstreetmap.org/copyright)。この帰属・ライセンスは航空写真には適用しない。

参考写真・図面：

- [空港公式の航空写真PDF](https://www.centennialairport.com/files/e3a6747bd/23.+Airport+Aerial.pdf)。PDF内のJPEGは2666×4000画素。撮影原本の最大画素数・撮影年月・ネイティブGSD・商用再利用条件は未確認。
- [空港公式サイトで配布されているFAA空港図AL-5715](https://www.centennialairport.com/files/8edb73294/23.+Airport+Diagram.pdf)。取得した図の有効期間は2026-10-01〜2026-10-29。

公式航空写真の商用再利用条件が未確認なので、画像本体と画像を含む比較プレビューはGitに追加していない。画像をダウンロードできることや、この実験で表示できることを、納品への利用許諾とは扱わない。提出CSV・Excelの提出URLは変更していない。

## 参考写真の位置合わせの限界

参考PDFには、この実験で利用できる地理参照情報を確認できなかった。そのため、滑走路端付近の6点を手作業で選び、OSMの端点とアフィン変換で概略対応させた。ピクセル座標・地理座標・元ファイルのハッシュは `registration.json` に保存している。

- 6点の当てはめRMSE：約29.2 m、最大誤差約39.3 m。
- 各点を1つずつ除外して推定した最大誤差：約160.3 m。
- ランドマークの選び方、OSMの精度、撮影年代差などの影響があり、測量精度や正確な撮影地点の証明には使わない。
- 写真の枠内カバー率は、この概略位置合わせに基づく値。地理範囲の計算そのものは手作業の位置合わせとは独立している。
- 元画像がない範囲は灰色で表示する。生成画像や周辺風景の補完は行わない。

北上の比較画像の左右が灰色なのは、必要な地上範囲の約半分しか参考PDFに含まれないため。空港が欠けているという意味ではない。実際に北上の納品画像を作るなら、約7×4.6 kmを覆う別の元画像が必要。

## 再現

既存の隔離済みチェックアウトを使う。Git worktreeは作成しない。

リポジトリルート `/workspace/airport_photo_sourcing_automation` で実行：

```bash
python -m venv --system-site-packages /workspace/.venvs/kapa-geospatial
/workspace/.venvs/kapa-geospatial/bin/python -m pip install --no-cache-dir -r scripts/requirements-kapa-framing.txt
/workspace/.venvs/kapa-geospatial/bin/python -m unittest discover -s tests -v
/workspace/.venvs/kapa-geospatial/bin/python scripts/kapa_framing.py --output /tmp/kapa-geometry
```

写真なしの範囲・寸法・図は、保存済み地理データからオフラインで再計算できる。これはKAPA専用の実証であり、他空港のUTMゾーンを自動選択する汎用収集プログラムではない。

写真付きの比較を再現するときは、公式PDFからJPEGを無改変で取り出し、`registration.json` のSHA-256と一致する画像を指定する：

```bash
/workspace/.venvs/kapa-geospatial/bin/python scripts/kapa_framing.py --image /tmp/kapa-framing/aerial_source.jpeg --output /workspace/artifacts/kapa_framing
```

JPEG抽出にはPyMuPDFを使用した（実行環境に導入済み）。例：

```python
import fitz
from pathlib import Path
doc = fitz.open('/tmp/kapa-framing/aerial.pdf')
assert len(doc) == 1 and len(doc[0].get_images(full=True)) == 1
image = doc.extract_image(doc[0].get_images(full=True)[0][0])
assert (image['width'], image['height']) == (2666, 4000)
Path('/tmp/kapa-framing/aerial_source.jpeg').write_bytes(image['image'])
```

今回の計算・図生成自体は約1.5秒。資料探索、ダウンロード、初回環境準備、手作業の位置合わせ、利用条件の確認はこの時間に含めない。204枚を同じ速度で納品できる実証ではない。

## 検証結果と次の段階

- 既存の空港外周・3滑走路の全頂点が両枠内に含まれること、3:2、余白、座標変換を確認。
- 既知の長方形、90°回転、両側余白、UTM規模の座標への平行移動を使う4テストが成功。
- 北上と回転の比較を実画像で目視確認。異なる2枚の写真を確保したものではなく、同じ参考写真の2通りの枠を比較した。
- USGS `naip.nationalmap.gov` と `imagery.nationalmap.gov` はプロキシ403でサービス情報を取得できなかった。既存許可リストを維持して両ドメインの追加を環境設定案に保存した。保存・公開による反映は別途必要で、USGS画像の取得成功や特定レイヤーのroyalty-free確認は未達。
- 次は地理参照情報付きの航空写真を、この回転枠（約4.66×3.11 km）を覆う形で取得する。元画像のレイヤー別利用条件・撮影年・実解像度を確認できれば、手作業の位置合わせを省き、写真の取得からフレーミングまでを評価できる。
