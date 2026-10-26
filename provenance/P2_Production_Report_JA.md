# P2 Production Report - NT-BE / X2-ω

作成日：2026-10-26（Asia/Tokyo）
対象：未公開候補 v1.1.0-rc1。既公開 v1.0.0 の元研究結果は変更していない。

## 実施内容

英文Technical NoteとSIを統合改訂した。Primary RQは固定ensembleの段階的geometry/ω選別に対するfoldedness・操作的ΔG/ΔΔGの感度であり、実験参照AE/MAEはSecondaryとして独立した節にした。FNC、frameごとのsigmoid、集合平均、clipping付き295 K変換、mutant−matched baseline、AE/MAEを明記した。MDCは0.1 kcal/molに依存させていない。

Figure 1は棒グラフ、Figure 2は両段階のsigned ΔΔG散布図という基本形式を維持した。保持集合、除外分母、軸の符号・単位・象限を明示し、段階間の符号とmutant−baseline内の寄与を区別した。400 dpi PNGとPDF/SVG、生成コードを用意した。完全表はCSV、本文/SIは必要な要約と出力案内とした。

## 入力回収・照合

添付20ファイルをSHA-256で識別し、ZIP内955ファイルのinventoryを保存した。Primary ZIP 2個は同一ではなかった。全154-member NPZとreconciled CSVは公開Zenodo v1.0.0と一致する。本人repositoryは接続GitHubから取得し、既公開基点commitは `7681674d5ec80545239e80214de1bd164c07eff8`。これは新候補のcommitではない。

公開Zenodo metadataと52,284,767-byte supporting ZIPを実取得し、公開MD5と一致を確認した。公式benchmark/BioEmu code ZIPは添付bytesのMD5・サイズを公式recordと照合した。公式コードとsnapshotの対象8関数/クラスのASTは一致した。BioEmu著者版本文/SIとMolProbity著者PDFを取得し、関係する方法を確認した。最近接の方法は既知のBioEmu評価とpeptide検証規約として扱い、新手法・世界初・一般的性能改善を主張しない。既存の文献探索全体はやり直していない。

L1_report、L2実行出力、実行版L2 v1.0.1、Session3初回出力・回復出力と参照探索修正版を追加回収し、Phase1Aに記録されたSHAと一致した。初回CSV 153 PASS＋1 FAIL_QAと回復1行から、154系への連続性を照合した。619セルの再保存末尾差（最大4.44e-16）以外に1e-9を超える相違はない。初回出力ZIP内には回復IDのNPZも含まれるため、回復NPZとの完全一致と、ファイル単体から時系列を証明できない点を明記した。

L2の154個別system JSON、112 pair JSONを直接確認し、ID、hash、frame数、3段階のenergyを今回の配列再計算と照合した。元1.96 GB XTCアーカイブは取得・再計算していない。公式FNC/clash再使用、MDTraj共有、snapshot/pair CSV等のfingerprint欠落、aggregate PASSの件数条件不足を維持して説明した。

## 独立読み取り専用検算

verification/はPrimaryをimportしない別実装で、公式metadataと保存FNC/maskから先に全量を計算し、その後に旧CSVを比較対象として読む。平均はmath.fsumを使う。人工入力22試験とacceptance_specを先に固定し、指示された許容差を一度も緩めていない。

- V0：hash、154/42/112の対応、112ペア、全mask・frame数・元geometry NPZとの連続性を確認。
- V1：pとΔG各462値、paired ΔΔG 336値、全段階差・累積差と寄与分解を確認。
- V2：公式参照と全336 AE、3 MAE、3 MAE差、改善/悪化/同等と0.1集計を確認。
- 非線形検査：p±1e-10の区間を元clipping付きlogitへ通し、全462旧ΔGを包含。直接数値一致とは別に検査。

直接比較6,726件、exact/identity等5,230 checksはすべて合格した。最大絶対差はp 3.33e-16、system ΔG/paired ΔΔG/AE 6.58e-13 kcal/mol、system ΔG差6.59e-13、pair/AE差7.42e-13。MAEとその差の最大誤差はそれぞれ2.45e-15未満、4.33e-15未満。各セル・最大誤差・許容差・環境・入力hashはdata/results/に保存した。

MAE A/B0/Bω=0.702594785554029/0.696141628039697/0.707681001609196。6桁表示は旧報告と同じ。B0→BωはAE改善54・悪化58。A→B0は59/52/1、累積は54/58/0。閾値近傍は0件、AE符号近傍は既存の完全同等1件（6FVC__L24V、A→B0）で、元分類を変更していない。

最初の検算器は回復NPZとの重複IDを検出して停止した。そのFAIL JSON/logを保存し、同一回復ID・配列完全一致だけを明示的に許可した。数値許容差を変更した事例ではない。PDF制作時のReportLab引数重複エラーも科学データに無関係な制作エラーとして区別した。

## クリーン環境と編集確認

system site-packagesを使わない新規venvへNumPy 2.3.5を導入し、Python 3.12.14/Linuxで人工22試験とV0-V2を再実行した。すべてPASS。7個の科学結果CSV/JSONは初回成功出力とbyte-identical。実行コマンドと導入・試験・検算logを保存した。Windowsで新たに実行したとは記載していない。

Technical Note/SIはそれぞれ7ページ。PDFを再描画し、全ページ、数式、図、表、キャプション、ページ番号と主要リンクを確認した。表とキャプションの分断を修正した。編集可能ソースはMarkdownとPDF生成Python。元PDF、元図、元コード・CSVは旧版として保存した。

現行公開CFFのトップレベルtype=reportはCFF1.2.0 schemaに適合しないため、元bytesをhistoryへ保存し、新候補はcompendium metadataと旧報告preferred-citationを持つschema適合CFFにした。DOIを新候補へ流用したものではない。記録上のlicense選択・著者申告を継承し、公式MIT/CDLA/NOTICEと本人作成物の範囲を分けた。

## 未実施・未完了の区別

未実施：新規研究、全154座標の新規再計算、元完全依存環境の復元、GitHub push/release、Zenodo upload/新版公開。これらを実施済みと主張しない。元依存履歴・L2の欠落fingerprintは研究解釈上の限界であり、今回のV0-V2の欠落ではない。

本人による最終原稿・申告・権利・version確認と、別途の公開可否判断は次の工程である。公開commit/tag/新DOIは実在後にのみ記録できる。現時点で架空の識別子は入れていない。
