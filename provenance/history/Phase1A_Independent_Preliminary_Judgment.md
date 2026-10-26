# NT-BE／X2-ω — 独立暫定科学判定

判定日：2026-10-26（日本時間）。評価範囲：Phase 1Aのみ。

**Package 03を開く前に確定・保存した判定。総合：A2 — Valid with mandatory corrections。**

固定アーカイブ・固定算出規則における選別感度という中核は成立する。必要なのは主要数値の撤回ではなく、方法の完全な定義、歴史的固定の証拠レベル、検証の独立性、境界対照の意味の訂正・明示である。真の自由エネルギー補正、一般的性能向上、完全なphysical validityは支持しない。A2は公開推奨や学術的新規性の判定ではない。

## 1. 独立性と資料

Package 01・02のみを展開し、各manifestの全25ファイルのサイズ・SHA-256を照合した。公式コードZIPのMD5は公式Zenodo 15672282掲載値と一致。研究引継ぎに含まれる旧評価文は正当性の根拠とせず、Protocol復元部分だけを使用した。

承認済み評価基準はPost_Research_Independent_Assessment_Protocol_v1.0_FINALのPhase A。Master v1.6 PROPOSEDは未承認参考資料。P01–P15とX2規則は引継ぎ・コードから復元できるが、独立した最終承認時点の証明はない。

公式原著の著者版＋SIをMicrosoftから実取得し、Model architecture、S5/S7/S12、Evaluating free energy predictions、geometry filteringを読んだ。MolProbity原著のcis/trans/twisted定義をPMC本文で確認。公開GitHubのREADME、Technical_Note.pdf、Supplementary_Information.pdfを取得して監査対象として読んだ。これらの公開文書を数値の独立根拠には使用していない。Zenodoの研究公開版本文はこの時点で未確認。

[V] 今回直接検証、[H] 保存された実行記録を継承、[D] 公式一次資料の仕様、[I] 解釈、[U] 不足。

## 2. Claim別暫定判定

| Claim | 暫定結論 | 証拠と範囲 |
|---|---|---|
| 154系、42 baseline、112 mutant、112対応ペア | Supported / A1 | [V/D] 公式metadata、統合表、NPZ、L2 ID照合 |
| 153成功＋回復1系の統合は参照探索修正のみ | Supported / A1 | [V] コード差分と元表照合。数値再保存差最大4.44e-16 |
| A⊇B0⊇Bω、302800→298188→272381 | Supported / A1 | [V] 全154保存NPZを再集計。[H] 元XTC計算はL2実行記録 |
| B0が公式評価関数の判定結果 | Supported、検証独立性限定 | [V/D] 抽出8関数/クラスのAST一致、mask連続性。[H] L2座標再計算 |
| B0にω規約上のtwistedが残存 | Supported / A1 | [V] B0で27,329/14,922,082 bond–frames、25,807 frames。[H] 座標角度のL2検算 |
| FNC、soft foldedness、ΔG・ΔΔG算術 | Supported / A1 | [V/D] 公式明示Settings、保存FNCからtanh＋log/log1pの別式。ΔG最大差4.56e-13 kcal/mol |
| 19/112と40/112、MAE 0.702595→0.696142→0.707681 | Supported / A1（記述） | [V] 固定表・配列から再現。0.1は有意性の閾値ではない |
| 30°は無根拠な恣意的数値 | Not supported | [D] MolProbityの構造検証規約に根拠。ただし平衡集団への最適選別とは別 |
| L2は完全独立な全経路検証 | Not supported / A2で表現修正 | [V] FNC/clash公式再使用、同じMDTraj読込、snapshotのfingerprint欠落 |
| 境界2条件はΔΔGの上下限 | Not supported / A2 | [V/I] 29ペアでPrimaryが2値間にない。両者は選別シナリオ |
| XTC frameは時間自己相関を持つMD時系列である | Not supported as an assumption | [D] 原著はiid生成を記述。[U] 実アーカイブのseed/batch等の完全履歴 |
| 一般的精度改善・平衡回復・真の自由エネルギー補正 | Not supported | [I/U] 条件付き選別であり正しい平衡重みの証明なし |
| 研究全条件が結果閲覧前に正式承認された | Inconclusive / A3（当該claimのみ） | [H/U] 引継ぎはあるが最終承認原本・全ログ・lockfile未回収 |

## 3. 主要反証と判断

1. **FNC defaults取り違えの疑義は棄却。** 裸関数のlambda=0、delta=1.2とSettingsのlambda=1.2、delta=0は違うが、Core・L2・公式evaluateはいずれもSettingsを明示。snapshotは公式関数と一致。
2. **回復による条件変更の疑義は棄却。** `1TG0__D45C_N47P`の同名テストPDB重複に対し公式reference_mutantsへ検索を限定。閾値・対象・算式は変わらない。200→199 frames。
3. **L2の302 vs Primaryの292は数値矛盾ではない。** 保存near maskからA全体302、B0限定292を再現。10系各1 frameがA-only。該当frame indexは検算JSONに保存。
4. **境界シナリオを誤差上下限と呼ぶことは反証された。** `1EM7_V54S__D47W`はPrimary −0.1003079005、全除外側 −0.0989172631、全許容側 −0.0994791297 kcal/mol。両側39対Primary40の違いはこの1ペア。`4C26__K58A`はPrimary +0.0007984011が両側負値の間にない。Primaryを改変しない。
5. **L2 PASSに論理上の過大解釈余地。** fingerprintは実際にimportする2 snapshot・SciPy/Biopython等・pair CSVを含まない。aggregate `all_pass`はpair未実施でもTrueになり得る。ただし今回の成果物には154個別記録と112 pairが実在し、全件を直接照合した。今回のpair欠落を発見したわけではない。
6. **代替説明は観察を覆さず、解釈を限定。** 選別とsoft foldednessの相関、logitの増幅、mutant−shared WTの相殺で差は説明できる。これを新たな物理機構や平衡補正の証拠にはできない。ランダム同数除外の対照は固有の効果を主張するなら必要だが、固定アーカイブ差分の記述には必須でない。

## 4. 暫定判定の理由と最小修正

A1だけでは、検証範囲・Protocol固定・境界対照の意味が未整理であることを表せない。A3を研究全体に適用するほど、固定記述結果に不可欠な証拠が欠けているとは判断しない。A4を支持する主要計算破綻は認めない。

必須：①A/B0/Bω、FNC→soft foldedness→logit、30°両平面からの最小偏差、原子集合を自足的に定義する。②全154 raw-coordinate Work再計算とL2の継承を区別する。③境界2条件はシナリオであり誤差包絡でないと明記。④事前正式固定とコードから復元した実行規則を区別。⑤MD自己相関を未測定の既成事実として扱わない。これらは新規研究・再最適化を必要としない。

現時点で元1.96 GBの再転送や全154座標再計算を要求する具体的必要性はない。原子・配列・source hashの矛盾、主要mask不一致は見つかっていない。

## 5. この後の限定工程

本ファイルの内容とハッシュを固定した後に初めてPackage 03を開く。旧判定との一致を科学的根拠にせず、重要相違だけを一次証拠へ戻って確認する。最終報告完成後STOP。Phase B/C/D、公開物変更、追加Work起動は行わない。
