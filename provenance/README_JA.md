# NT-BE-X2-ω Session — Primary解析実装 v1.0

## 今回の状態

- Pilot 3系（V39G, Y45R, 1TG0__D45C_N47P）の実データ監査終了。
- このパッケージは154 system / 112 WT–mutant pair用Primary実装です。**全件実データ解析はまだ実行されていません。**
- 元のNT-BE Coreは変更しません。B0=既存の公式geometry filter後通過frame、Bω=B0から明確にtwistedであるframeを追加除外した集合。
- 30°の厳密不等号、cis/trans双方許容、Proを次側残基で分類、固定foldedness・固定T=295 Kを維持。探索・モデル調整なし。

## 前提

Python 3でnumpy、mdtrajを利用可能。既存Coreの全154系FNC NPZは
`C:\Users\user\new_research\NTBE_Session3_output_new\fnc\<system>.npz`。

入力archive（約1.96GB）はPC上で使用し、チャットへアップロード不要。公式benchmark ZIPはSession3で使った**同じbytes**にしてください。

## 実行例（PowerShell）

ZIPを展開し、`ntbe_x2_primary.py`のあるフォルダで実行：

```powershell
python -m unittest -v test_primary test_integration test_omega_pilot test_proline
python ntbe_x2_primary.py `
  --archive "C:\Users\user\new_research\samples_delta_G.zip" `
  --bench "C:\Users\user\new_research\bioemu-benchmarks_code_release.zip" `
  --fnc-dir "C:\Users\user\new_research\NTBE_Session3_output_new\fnc" `
  --out "C:\Users\user\new_research\NTBE_X2_Omega_Primary_output"
```

小さな任意system限定で事前に再動作確認する場合は、`--systems "1TG0__D45C_N47P"`を追加できます。ただし`analysis_scope=SUBSET_QA_ONLY`でありPrimary完了とは表示しません。繰り返しpilotをする必要はありません。

## 出力

- `report_omega.json`：集計と、全件完了フラグ。
- `systems_omega.csv`：154系のbaseline/追加filter、角度分類、Unknown、境界、folded fraction、ΔG、品質flag、SHAの照合を記録。
- `pairs_omega.csv`：112 pairのB0・BωのΔΔG、主解析差D、共有WTの寄与、実験値との差（Secondary）、Unknown/境界の感度値。
- `omega_masks/<system>.npz`：全154系のframe別maskと二面角、frame別FNC。データ量が大きくなることがありますが、重要な再現証拠として保存を推奨します。

`status=FAIL`、`BOMEGA_EMPTY`、pairの`INCONCLUSIVE`がある場合も理由とともに残ります。全154系・112 pairの計算に成功したときだけ`full_primary_complete=true`になります。例外があればプロセスは非0終了しますがCSV/reportは出力します。

## 注意と未解決領域

1. ω角のUnknownはtwisted扱いせず保持しますが、件数を別記。局所欠損はUnknown、曖昧なatom mapping・整合しないC–N topology接続はsystem QA FAIL。
2. `topology_connectivity_unverified=true`ならPDBからbond graphを独立に検証できなかった意味です。正常と証明したものではありません。系統的な接続異常があればSTOPして検証してください。原子の距離だけを理由にchain boundaryを推測しません。
3. `near_boundary`は|dω-30°|<=0.02°の診断用。境界とUnknownを保守的に除外する／保持する差の両側を計算し、主要結論に影響すればInconclusiveを検討します。今回は分類閾値を動かしません。
4. Bω<=10、Bωが公式ターゲット70%未満、clippingはflagであり、計算可能例を無断除外しません。
5. `|D|>=0.1 kcal/mol`は記述的な参考値でありGO/MSCの基準ではありません。
6. 112 pairは42共有WTに依存。独立サンプルとみなす推論統計は実施しません。
7. 実験ΔΔG絶対誤差はSecondaryであり、ω閾値の正当化や汎化精度改善の主張に用いません。
8. 出力中に個別のatom/bond-level異常が出れば、代表例だけを限定的に確認し、全残基探索を追加しません。
9. 同じCSVからの検算は完全なXTC独立再解析とは異なります。原sample archiveのSHAをCore行と照合します。

## 既知の留意点

全系の実データ検証はこの場では不可です。必要な元XTCと154 FNC NPZがチャットに添付されていないため、まず本人PCで実行し、`report_omega.json`、`systems_omega.csv`、`pairs_omega.csv`を添付してください。予期しないFAILがある場合には原因を限定して再実行します。
