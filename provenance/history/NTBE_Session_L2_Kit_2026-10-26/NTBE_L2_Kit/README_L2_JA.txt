NT-BE / X2-omega Session L2 — ローカル元座標監査キット v1.0（2026-10-26）

目的: 154系すべての公開XTC/PDBからgeometry B0、omega Bω、FNC、ΔGを再計算し、保存NPZおよびCore表と比較する。新研究・閾値探索・科学的A1/A2判定をしない。

必須入力を C:\Users\user\NTBE に置く（ZIPは展開しない）。
- samples_delta_G.zip (1,959,113,732 bytes; SHA256 81fa710c667d29f664e378e551ee1f180975a62d8e37d859646be8b2fa9469c7)
- bioemu-benchmarks_code_release.zip
- all_npz.zip  ※ ChatGPT添付時の (1) を元ファイル名と誤認しない。
- NTBE_systems_154_reconciled.csv
- NTBE_pairs_112_reconciled.csv
- 本ZIPの ntbe_l2_verify.py / official_fnc_snapshot.py / ntbe_official_filter_snapshot.py

依存: Python 3、NumPy、MDTraj、SciPy、Biopython（旧snapshotが Bio.pairwise2 を使用）。
確認: py -3 -c "import numpy,mdtraj,scipy,Bio; from Bio import pairwise2; print('READY')"
依存のインストール・アップグレードはまず行わず、エラーの場合はメッセージを共有する。

出力: C:\Users\user\NTBE\NTBE_L2_output の下に新規作成。入力を読み取り専用で扱う。TEMPに系単位のXTC/PDBを展開し、終了時削除する。

まず少数系 pilot:
  cd C:\Users\user\NTBE
  py -3 .\ntbe_l2_verify.py --root . --mode pilot

pilot実行結果を確認し、FAILがなければ全件:
  py -3 .\ntbe_l2_verify.py --root . --mode full

集約:
  py -3 .\ntbe_l2_verify.py --root . --mode aggregate

ユーザーがChatへ提出するもの:
  まずは pilot後の NTBE_L2_output/systems/1EM7_L7A.json など代表4系JSONとPowerShell画面ログ。
  全件終了時 NTBE_L2_output/L2_aggregate.json と L2_pairs.json、FAILがあれば当該systems/*.json。全154系の個別JSONの一括ULは初回不要。

留意事項:
- メモリ保護のため100 frames/chunkで処理（--chunk 100、条件変更すると再開用fingerprintが変わる）。
- 元アーカイブは毎回SHA256で確認するため、最初に一定の読込I/Oがある。
- 成功系だけは入力・コード・chunk SHA fingerprint一致時に再開SKIP。失敗系は再試行される。処理途中でもsystem別JSONを保存。
- 154系の全てについてPASSが確認できるまで「全件再現成功」と言わない。
- 公式filterの候補選定はchunkごとであってもframe別結果が同じかを検査する。異なる場合はFAILとして原因分析する。
- FNCは公式snapshotを明示FNCSettingsで呼び出す。bare function defaultを呼ぶと異なる条件になる。
- 独立性: ωは独立四点式、Cα/C-Nは直接距離でも照合。一方FNCは公式関数による再実行、clashは公式filterによる再実行。これらを全面的独立実装と偽らない。
- 重要な境界frameで計算精度由来のmask不一致があり得る。隠さずFAILを出し、許容差・規則変更で自動通過させない。
- 単純な0.02°（ω）／2e-5（FNC）／0.0002 kcal/mol（Core ΔG）を事前記録した照合許容差として採用。正式なscientific significance判定の閾値ではない。
- 途中で極端に遅い／PCが重い場合は Ctrl+C で中断できる。処理済みPASS記録を残す。
