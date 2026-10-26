# NT-BE / NT-BE-X2-ω 最終独立研究後評価

確認日：2026-10-19（Asia/Tokyo）｜状態：監査完了、研究Core STOP維持、公開未承認・未実施

## I. Executive decision

**第一推奨は、二つのRQを区別した単一の統合技術記録を、必須の記録整備後に公開すること。研究の追加・二本の論文化・独立した二成果への分割は推奨しない。** 内容の中心は、保存済みBioEmu ensembleに対する二段階の事後選別が、固定されたΔG/ΔΔG計算へどう伝わるかを第三者が照合できる記録である。新しい一般則、精度向上法、正しい平衡ensembleの回復とは認めない。[I]

| 評価対象 | Phase A | MDC | MSC | 公開判断 |
|---|---|---|---|---|
| NT-BE：A→B0 | **A2：mandatory corrections付きで限定範囲内妥当** | Supported：保存後geometry選別に対する固定archiveの評価値感度 | **Supported, limited**：公式処理経路の再利用可能な照合記録 | 単独公開も可能だが、統合に劣後 |
| X2-ω：B0→Bω | **A2** | Supported：固定30°規則による追加選別と、そのpaired評価値変化 | **Supported, limited**：distance/clash-pass後のω診断とendpointを結ぶcase record | 単独自立も可能だが、B0の由来と旧コード説明を要する |
| 統合：A→B0→Bω | **A2** | Supported：同一対象・同一参照・同一WTで二段階を追跡できる | **Supported, limited incremental**：段階別の増幅・相殺・対象の非重複を照合できる | **構成①を推奨。学術出版適性が自動上昇するわけではない** |

Phase C：現成果を査読論文・preprintへ優先的に仕立てる根拠は弱い。カテゴリーとしての可能性と推奨を分離し、投稿不可と一律断定しない。Phase D：コード、固定表、保存配列にアクセスできる短い技術記録の公開には具体的な利益がある。媒体の第一案は**GitHubで説明・コードを閲覧可能にし、同じ統合成果をZenodoで固定・引用可能にする構成**。保守をさらに減らす場合はZenodo単独で足りる。[I]

**今回の到達点。** 全154保存NPZ、112ペアの算術、代表9系4,443除外frameを直接検算した。さらに公式約1.96 GB ZIPから10系分のXTC/PDBだけを取得し、2,700 frameで別式によるω、原子対応、B0/Bω mask、境界flagを確認した。固定設定でのFNC再計算差は0。主要数値を覆す不整合は見つからなかった。[V]

**最大の残余未確認事項。** 元研究実行時の正確な依存版、旧153系＋回復1系の元ログと統合操作の全履歴、残り144系の元座標からの再計算は今回未確認。公式ZIP全体のMD5を再計算したわけでもない。最近接研究のうちkinase論文本文/SIとProteinConformers eLife版は今回完読できなかった。これらは限定的な記録公開を直ちに否定しないが、全座標独立再現・世界的非重複・原著数値の完全再現の認証には使えない。[U]

判定基準は添付の承認済み共通Protocol v1.0 FINAL。Master v1.3は**USER REVIEW PENDINGのまま**適用し、無断承認・改訂していない。過去のPASSやMSC Supportedは証拠と区別した。A2は主解析数値の訂正要求ではなく、IX節の説明・出所・再現範囲・権利の整備条件を意味する。現在の資料で「全154系を元座標から独立再現済み」と主張するなら、その強い主張はA3相当である。

証拠ラベル：**[V]** 今回の実ファイル・一次資料・計算による確認、**[H]** 過去記録の継承、**[D]** 公式仕様・媒体規程、**[I]** 解釈・推奨、**[U]** 未確認。異なる実験・別研究者による再現試験や、人間専門家による査読を実施した意味ではない。

## II. Phase A：何をどこまで検証したか

### II-1. 入力と出所

添付20ファイルを直接使用し、末尾の自動連番は版と解釈していない。ZIPのメンバーを展開して読んだ。全添付の完全SHA-256、ZIP内主解析ファイルのSHA-256、154 NPZ個別SHA-256、全keys/shape/dtypeは付属検算JSONに収録した。[V]

| 入力群 | 実体・件数 | 今回の扱い |
|---|---|---|
| 作業依頼文、共通Protocol、Master | 3 TXT | 権限・判定基準の正本。内容変更なし |
| 旧独立報告＋旧監査証拠ZIP | MDと4メンバー | 先行判断[H]。旧監査コードも読み、今回別スクリプトで重要項目を再検算 |
| Primary実装ZIP | 9メンバー | 旧154系/112ペアCSV、X2本体・pilot・既存test・README |
| X2結果と既存監査 | report、systems、pairs、primary audit、代表frame/bond、crosswalk、cross-study JSON | 結果表・保存NPZ間の照合。過去のPASSを転記して認定しない |
| Session3参照修正コード、FNC/filter snapshot | 3 PY | 関数ASTと公式snapshotの一致、引数、参照パス、計算規約を検査 |
| 公式benchmark code ZIP | 861メンバー | metadata、reference、関数、LICENSE/NOTICEを直接検査 |
| all_npz.zip | 154 NPZ、圧縮51,612,943 bytes | 全系の保存配列から分類・mask・endpointを再集計 |
| 今回取得した公式原入力の一部 | 10系×XTC/PDB＝20メンバー、圧縮約3.57 MB | HTTP Rangeで取得、ZIP CRCと個別SHA照合。全archive再取得なし |

主要入力の固定識別子：

| ファイル | SHA-256 |
|---|---|
| 共通Protocol | `bab458e286a70230c8139baeff96afdf6a50fe393292b5f2064f39b0dae8738c` |
| Master v1.3 | `97c009852be0e912604875b1d34fca81b73bdcdce1c3944cfd840695d240afaa` |
| all_npz.zip | `569a09744787d2c6c9b35e9e0cc80ce2ef4dd40d6a3f494cd45fe33bed8584b7` |
| bioemu-benchmarks_code_release ZIP | `b1ed5564f5c575069d6ce855ba47af69e6e43691a9dacffc0eaaa908c1d58e3c` |

公式Zenodo record 15672282のbenchmark ZIP公開MD5 `dd8f50a68aa8e01751069f0845966d66` と添付bytesは一致。添付snapshotのpyproject versionは1.0.0。ZIPから特定git commitを逆算したとは主張しない。原sample ZIPの公開MD5は `30c285d2a503fb3436cefda86c75a5c6`、全体サイズ1,959,113,732 bytesだが、**今回は部分取得なので全体MD5は未検証**。10系の個別XTC/PDBについては、公式配布メンバーのbytesと研究CSV中のSHAが一致した。[V,D; R2]

NPZの共通スキーマ（F＝A frame数、B＝隣接残基間結合数）：

| key | shape / dtype | 直接再検証できること／できないこと |
|---|---|---|
| `b0_mask`, `bomega_mask` | (F,), bool | subset・件数。元座標でのgeometry判定はNPZだけでは不可 |
| `unknown_frame_mask`, `twisted_frame_mask` | (F,), bool | 保存角度からのframe分類との照合 |
| `near_boundary_mask` | (F,B), bool | ±0.02°診断maskの照合 |
| `omega_degrees` | (F,B), float32 | 保存角度の分類。原子座標そのものではない |
| `next_is_pro` | (B,), bool | 公式sequenceの次残基との対応 |
| `omega_atom_indices` | (B,4), int32 | index配列の整合。原子名そのものは含まない |
| `fnc` | (F,), float32 | foldedness、ΔG、ΔΔG。FNCの元座標計算はNPZ単独では不可 |

NPZに元XTCのbytesやhashフィールドはない。provenanceは**系ID→結果CSVのsource SHA→公式配布メンバー**で結び付ける。代表9系のNPZ SHAは代表監査JSON内の9 hashと全て一致した。ただし代表9系ZIP自体は今回添付されていないため、「二つのZIPのbytesを直接比較した」とは書かない。[V/U]

### II-2. 決定的な検査と限界

| 主張・疑義 | 今回の検証 | 判定・限界 |
|---|---|---|
| 154系・112ペア・42共有WTが同じか | 公式metadata、旧CSV、X2 CSV、NPZのID集合・順序、mutant/WT、実験値、目標数を照合 | 全一致[V]。ペアを112独立反復とみなさない |
| A→B0とX2 baselineが同じか | 全系のFNC/maskから旧A/B0のΔGも再計算 | 最大差約4.4×10⁻¹⁴ kcal/mol[V] |
| referenceと1TG0回復 | 全154 reference bytesのhashと正規WT/mutantパスを照合。`1TG0__D45C_N47P`は原座標からFNCも再計算 | 現在の完成結果の参照整合は[V]。旧153＋1の作業履歴は[H/U] |
| 抽出関数が公式と同じか | FNCSettingsと5 FNC関数、geometry filterと補助関数のAST照合 | 対応する関数本体が一致[V]。logger等のstandalone import調整は区別 |
| ωの原子順とPro側 | ソース検査、全系sequenceとnext-is-Pro照合、10系の実topologyからquartet再構成 | Cα(i)–C(i)–N(i+1)–Cα(i+1)、次残基Proを確認[V] |
| wrap・30°・鎖端 | 主解析と異なるmodulo式で全保存角度を分類。既知角度の四点座標で±30/±150/±180°、退化座標を検査 | 厳密 `>30°`、鎖端を除いたL−1結合、退化角Unknownを確認[V] |
| Bω⊆B0、二重計数 | 全154配列からmask・frame数・bond観測数を再計算 | mask全一致。frame数とbond数を別の分母で報告[V] |
| 元座標からωが一致するか | 10系2,700 frameで、元のprojection式と異なるplane-normal式を使用 | 保存float32角との差最大7.63×10⁻⁶°、mask/境界flag完全一致[V] |
| B0・FNCを座標から確認できるか | 同10系でsnapshot関数を固定明示引数で実行 | B0 mask完全一致、FNC差0[V]。FNC自体は別実装でなく同snapshot関数の再実行 |
| Unknown/topology QA | 全NPZに非有限角なし、L−1結合、全CSVのmissing/unknown/connectivity flagなし。10系の原子名とsequence確認 | Unknown=0は[V]。残り144系の原topology全面認証ではない |
| 保存後float32化による境界分類変更 | 全保存角度から再分類し保存boolと比較 | 現配列にmask差なし[V]。原float64角は全系保存されていない |
| 全件完了と古いREADME | 現reportはFULL/154 PASS/112 computable。保存NPZ・表がこれを裏付ける | READMEの「未実行」は実装配布時の文言。結果無効化の根拠ではないが、公開前訂正が必須 |

標的10系は、最大|D|側の `1EM7_L7A__V39G`、境界で報告分類が変わる `1EM7_V54S__D47W`、参照回復を含む `1TG0`, `1TG0__E1N`, `1TG0__D45C_N47P`、WT寄与が大きい `6FVC`, `6FVC__L6Q`、under70の3系。これは**監査目的の標的選択**であり、全体を代表する無作為標本ではない。元研究の代表9系とは別の集合である。

今回の座標QA環境はPython 3.12.14、NumPy 2.3.5、MDTraj 1.11.2、SciPy 1.17.0、Biopython 1.88。保存配列検算にはpandas 2.2.3も使用。これを元研究の実行版と書き換えない。元Session3ヘッダにはPython 3.13とあるが、当時の正確な版一覧はない。現行公式READMEはPython <3.13と、v0.0.2対v1.0.0+の数値非互換性を警告する。今回10系で一致しても、全依存版に対する互換性保証にはならない。[V,D,U; R3]

**再現手順で注意すべき具体点。** FNC関数を引数省略で直接呼ぶ場合の既定値は `contact_lambda=0.0, contact_delta=1.2` で、FNCSettingsの `1.2, 0.0` と異なる。元Session3はFNCSettingsを明示しており正しい。今回の監査コードでもその明示引数へ統一した。裸の関数既定値へ置換した再現例は使えない。これは元主解析の誤りではなく、公開時に固定引数を省略しない必要性である。[V]

元のmapping guardは重複原子、全結合欠落、MDTrajとのquartet不一致、混在したC–N接続をFailとする。一部欠損をUnknownとする一般ルールはあるが、任意の異常topologyを網羅的に分類できる汎用validatorとしては検証していない。今回の固定入力ではUnknown・missing・未確認connectivityのCSV flagはいずれも0で、標的10系の原topologyにも不整合はなかった。[V/H]

### II-3. 数値検算

以下は保存NPZ・固定CSVから今回直接確認した値。[V]

| 項目 | 検算値 | 分母・解釈 |
|---|---:|---|
| A → B0 | 302,800 → 298,188 frame | 旧除外4,612、Aの1.523% |
| B0 → Bω | 298,188 → 272,381 frame | 追加除外25,807、B0の8.6546% |
| 評価可能ω | 14,922,082 bond-frame観測 | 同一結合の別frameは別観測 |
| twisted | 27,329 bond-frame観測 | 上の0.1831%。25,807 frameと混同しない |
| twisted Pro / non-Pro | 1,860 / 25,469観測 | 次残基で分類。独立因果効果ではない |
| cis-Pro / cis-nonPro | 17,960 / 223観測 | B0中。cis自体は除外条件でない |
| Unknown frame | 0 | 評価不能を正常へ数え直した結果ではない |
| 30°±0.02° | 292 B0 frame、292 bond観測 | 86系、89ペアでeither-boundary flag |
| D中央値、Q1～Q3 | +0.000845；−0.037000～+0.087270 kcal/mol | D=ΔΔG(Bω)−ΔΔG(B0) |
| 最大|D|、|D|≥0.1 | 0.486820 kcal/mol；40/112 | 0.1は報告用のみ |
| MAE：A / B0 / Bω | 0.702595 / 0.696142 / 0.707681 kcal/mol | 同じ112ペア、同じ実験参照 |
| B0→BωのMAE変化 | +0.011539 kcal/mol | 改善54、悪化58。一般的改善は支持されない |
| 等WT重みのMAE変化 | +0.009260 kcal/mol | 既存要約の算術照合。統計検定ではない |
| under70該当ペアを除いた既存診断 | +0.012511 kcal/mol | 主解析は112を維持。この診断で対象を再定義しない |

保存角度から作ったmaskは全154系で一致。エネルギー・ペア検算の最大差は約4.4×10⁻¹⁴ kcal/mol、foldedness分解恒等式の最大残差は2.84×10⁻¹⁶。検算コードの成功は計算整合性を示すが、実在平衡集団の妥当性を示すものではない。

代表9系の照合（表のΔG shiftはBω−B0、kcal/mol）：

| 系 | B0 | Bω | 除外frame | ΔG shift | p(B0) / p(保持) / p(除外) |
|---|---:|---:|---:|---:|---|
| 1EM7_L7A | 7,469 | 6,654 | 815 | -0.084136 | 0.989013 / 0.990468 / 0.977135 |
| 1EM7_L7A__V39G | 196 | 174 | 22 | -0.570955 | 0.978048 / 0.991596 / 0.870890 |
| 1TG0 | 397 | 313 | 84 | +0.130724 | 0.993704 / 0.992144 / 0.999519 |
| 1TG0__D45C_N47P | 199 | 155 | 44 | -0.255571 | 0.989776 / 0.993365 / 0.977134 |
| 1TG0__E1N | 490 | 372 | 118 | -0.239841 | 0.995578 / 0.997058 / 0.990911 |
| 4C26 | 9,748 | 8,055 | 1,693 | -0.124706 | 0.975721 / 0.980282 / 0.954022 |
| 4C26__K58A | 9,782 | 8,155 | 1,627 | -0.123907 | 0.975027 / 0.979688 / 0.951663 |
| 6FVC | 200 | 185 | 15 | -0.438085 | 0.996579 / 0.998377 / 0.974407 |
| 6FVC__L6Q | 195 | 170 | 25 | -0.029582 | 0.839899 / 0.846569 / 0.794545 |

代表removed-frame CSVのframe ID集合・FNC/foldedness・twist数を照合し、267の結合位置別集計行も観測数、平均foldedness、偏差中央値、Pro分類と照合した。4,443は重複排除した除外frame総数であり、267はbond-event総数ではない。[V]

**「70%未満」の分母訂正は必須。** 実装flagは `n_Bomega < 0.7 × num_samples_target`。以下の3系であり、Bω/B0は全系70%以上（最小約75.92%）。「B0の70%未満が3系」と記載すると誤りになる。[V]

| 系 | target | B0 | Bω | Bω/target | Bω/B0 |
|---|---:|---:|---:|---:|---:|
| 2RRT__A48P | 200 | 166 | 128 | 64.0% | 77.11% |
| 2RRT__F9P_F61V | 200 | 169 | 134 | 67.0% | 79.29% |
| 4C26__S6N_H43H | 200 | 175 | 136 | 68.0% | 77.71% |

**境界診断。** 既存コードの保守的規則（nearを含め除外）と許容的規則（nearだけのtwistは除外しない）を、固定保存配列から再現した。Dの基準結果からの最大変化はそれぞれ0.010632、0.018162 kcal/mol。両規則で|D|≥0.1は39/112へ変わり、変わるのは `1EM7_V54S__D47W`（主解析−0.100308、保守的−0.098917、許容的−0.099479）。主解析40を39へ上書きするのではなく、固定primaryと既存診断を並記する。[V]

これは独立した全bondの誤差を任意に組み合わせた数学的な上限ではなく、**指定された二つの一括規則**である。「全ての数値摂動で頑健」とは言えない。境界flagが付いたペア数を、そのまま実質的に不安定なペア数とも解釈しない。[I]

### II-4. 横断比較と解釈の上限

旧|ΔΔG(B0−A)|≥0.1は19、X2の|D|≥0.1は40、共通12、旧のみ7、ωのみ28。二つのフラグ集合の和集合は47であり、累積A→Bωの|変化|≥0.1である44とは別の量。各ペアの加法関係は全112で照合した。[V]

| ペア（mutant） | A→B0 | B0→Bω | A→Bω | 読み方 |
|---|---:|---:|---:|---|
| 1TG0__E1N | -0.575240 | -0.370565 | -0.945805 | 同方向に増幅 |
| 2M0C__Y5T | -0.366569 | +0.135706 | -0.230863 | 部分相殺 |
| 2AMI__F63S | +0.338207 | +0.002038 | +0.340244 | ω段階でほぼ不変 |
| 4C26__K58A | -0.005397 | +0.000798 | -0.004599 | mutant/WT shiftが相殺 |
| 1EM7_L7A__V39G | -0.107813 | -0.486820 | -0.594633 | 最大|D|の例 |
| 6FVC__L6Q | -0.008816 | +0.408504 | +0.399688 | WT側shiftの寄与が大きい |

同一系のfoldedness平均について、除外数r、B0数n₀、除外平均pᵣを用いると

\[
p_\omega-p_0=\frac{r(p_0-p_r)}{n_0-r},\quad
\Delta G=-RT\log\frac{p}{1-p},\quad
D_j=\delta G_{mut,j}-\delta G_{WT(j)}.
\]

これは既知の算術であり新しい機構発見ではない。一方、実際にどのframeが除かれ、pᵣがどれだけ違い、どのWTとの相殺になるかは入力依存で、割合だけからは決まらない。たとえば4C26__K58Aはmutant/WTのΔG shiftがともに約−0.124でΔΔG差は小さい。1TG0では除外frameのfoldednessが高く、保持後のΔG shiftは正。V39Gの大きな変化を「当該twist結合が安定性を因果的に支配する」と読み替えない。[V/I]

次の限界を公開物の結論に残す。

- Aは公開XTCに保存された集合。生成前のraw母集団ではなく、上流の選別履歴を除去した対照でもない。
- Bωは追加の事後選別集合。MolProbity由来の警告基準を使っても、平衡分布・熱力学的正しさ・推定のunbiasednessは得られない。
- 30°の基準は既知の構造検証規則。cis-Proを正常範囲として扱うことは整合するが、cis-nonProを含む他の品質問題をすべて評価したMolProbity全体の代替ではない。[R4]
- 複数twistの共存frameを一度除外している。各結合の独立効果や、Pro置換の因果効果は同定していない。
- 任意のframe除外でも、残るfoldednessが変われば非線形logitからΔGは変わる。無作為除外対照を行っていないため、twist選別の特異的優越性や一般的bias補正は主張できない。
- 有限sample、長さによる「1個以上twist」の発生機会、同一WTの再利用がある。bond観測とframeの独立性、112ペアの独立性、統計的有意性を仮定しない。
- soft membershipは0/1の実観測ではない。clipping=0はrare-state sampling十分性を保証しない。0≤q≤1と固定sigmoidではpは約4.54×10⁻⁵～0.999955に収まり、1e−10 clippingに到達しないこと自体が数式上予期される。
- MAEの僅かな変化はこのarchiveの記述値。閾値選択の正当化、モデル全体の改善・劣化、独立した実験的検証には用いない。

0.1と30°の固定経緯は依頼文、前回提案、コードに整合するが、全実行に先立つ署名済み登録・時刻証明を今回確認したわけではない。したがって「登録済み事前解析」とは表現しない。[H/U]

## III. Phase B：最近接先行研究、MDC、MSC

### III-1. 反証を優先した比較

2026-10-19にBioEmu＋peptide omega/twisted/filter/folding free energy、ProteinConformers、ConforMix、ensemble selectionを検索し、既存報告の候補を原著・SI・公式コードへ辿った。以下の比較範囲を超えた世界初を主張しない。

| 一次資料・確認範囲 | 既に知られていること／今回への反証 | X2・統合で残る具体的差分 | 未確認・判断への影響 |
|---|---|---|---|
| BioEmu Science 2025、著者accepted PDF本文＋SI、S20/S24–25/S28 [R1] | geometry除外、soft foldedness、mutant−WT評価は既知。filterやsigmoid自体の新規性は否定 | 同じ保存archiveでA/B0/Bωを固定対応させた、ω追加選別後の個別ペア監査 | 著者版を実取得。出版社版との差を全行比較したわけではない |
| 公式snapshot・現行README・PR #24 [R2,R3] | 公式距離/clash判定、2025-06-18のsigmoid変更、依存版による数値変化 | 公式関数の再提案でなく、追加ω maskとΔΔGへの伝播を追跡 | 現行mainを固定snapshotへ混在させない |
| Williams et al., MolProbity 2018 p.305、Fig.9関連節 [R4] | planarから>30°をtwisted、次残基に結合を帰属。ω異常の発見や閾値の新規性はない | 既知規則に対する**当該archiveの実際の応答**と可検証なframe対応 | 結晶構造validatorの閾値はensembleの熱力学的acceptance ruleを保証しない |
| ProteinConformers 2025、§4.1.2/Table 1/3/4、公式Ramaコード [R5] | BioEmuを含むensembleの局所品質・分布評価は既出 | 論文のΩはCα–Cβ–Cβ–Cαの残基対virtual dihedralで、peptide ωと異なる。paired stability sensitivityも異なるendpoint | 2026 eLife版はchallengeで未完読[U]。2025 PDFと公式コードは[V] |
| Shin et al., JCIM 2026 [R6] | 26 kinase約1,300構造の選択とdocking性能。品質・多様性だけで下流性能を保証しない問題は既出 | stability benchmarkの154/112、ω規則、共有WTによるΔΔG分解とは入力・endpointが異なる | AbstractとSIメタデータのみ今回確認。本文403、SI403/500。前回SI詳細は[H]、今回[V]としない |
| ConforMix, arXiv:2512.03312v1 §3.3/4.4/App.E/G [R7] | guidance、構造filter、MBARとBioEmu free-energy推定の組合せは既出。品質と自由エネルギーを関連づける一般論は新しくない | App.EはBoltzのbond/Rama、App.Gはtrp-cageのRMSD状態間ΔG。固定geometry-pass後のω除外による112ペア応答とは異なる | 本文HTML・該当付録を直接確認。twisted diffusionはtwisted peptideの同義語でない |
| Enhanced Diffusion Sampling, arXiv:2602.16634v1 §2.2式16–17/§5 [R8] | hard/soft membership、rare-event、不偏化、weighted free-energy推定は既知 | 今回はsteering/reweighting法でなく、保存集合の条件付けの感度を記録 | 本文を確認。新しい熱力学推定法・rare-event解決を主張しない |
| BioEmu現行physical steering YAML [R9] | chain break/clash potentialによる生成時品質制御も既存 | 保存後選別である今回と操作段階が異なる | YAMLを実取得。全current implementationの否定的網羅証明ではない |

ProteinConformersの本文はRamaをfavored領域外と説明する一方、確認したコードはPyRosetta `phipsi_in_forbidden_rama` を呼ぶ。用語をMolProbity outlierと同一視せず、当該論文の10.69%というRama率を今回の8.65%除外率と直接比較しない。[V; R5]

**非重複性の結論は限定的。** 取得した最近接一次資料では、今回と同一の154/112、二段階の事後mask、固定soft estimator、共有WTの個別対応を一式で代替できる出力は確認できなかった。ただしこれは検索不検出による世界初証明ではない。kinase SI/eLife未取得は学術的新規性の強い主張を制限する。一方、実在する入力・出力・対応表の利用可能性というMSCは、世界的優先権が証明できなくても評価できる。[I/U]

### III-2. 三つのMDCとMSCを独立判定

**NT-BE単体**

- MDC：この固定公開archiveの154系112ペアでは、保存後に公式geometry filterを適用すると、固定FNC/ΔG規約下のΔΔGがペアごとに変化し、旧報告用閾値以上は19/112となる。[V]
- MSC：公式benchmarkを再解析する利用者が、保存全frameと評価filter後frameの混同を避け、参照修正・共有WTを含む具体的なID付き差分を照合できる独立監査記録を追加する。[I]
- 判定：限定MSC supported。既知の公式コードの実行だけでは不足だが、A/B0の対応、参照パスの問題、再現可能な差分を明示する情報は単純な動作デモを超える。原著値の全面再現やモデル批判へ拡張しない。

**X2-ω単体**

- MDC：同じB0の298,188 frameから、既知の30°規則で25,807 frameを追加選別すると、保存maskとFNCに対応する112ペアのΔΔGが上記分布で変化し、全体MAEの改善は見られない。[V]
- MSC：geometry-pass後に追加のω QCを実装・評価する利用者が、結合→frame mask→foldedness→mutant/WT shiftという照合経路を使い、QC選別とthermodynamic endpointの変化を混同せずにwrapperを検証できる具体的case recordを追加する。[I]
- 判定：限定MSC supported。価値は8.65%や40件の大きさではなく、QC合格集合の意味、固定入力での実際の除外構成、WT相殺、数値境界を再利用者が点検できる点にある。新filter、新指標、新たな一般原理ではない。残基・結合ごとの因果効果はunsupported。

**統合成果**

- MDC：二つの段階の効果は同じペア上で加算できるが、報告閾値を超える対象は一致せず、増幅・部分相殺・ほぼ不変を含む。[V]
- MSC：benchmark再解析者が一つのsource/ID/WT対応表から両段階を追い、累積効果を一方のfilterだけへ誤帰属しないための、二つの単独要約では失われる横断照合情報を追加する。[I]
- 判定：**小さな追加MSCあり**。加法恒等式そのもの、単にファイルを一つにしたこと、二つのPositive判定を合算したことには科学的加点をしない。第三者が自分でcrosswalkを作れば得られる情報であり、寄与の大きさは限定的。

この判定は、別実験による独立検証という意味ではない。旧snapshotと公開sampleに依存した再解析であり、今回独立化したのは保存配列の算術実装と、標的10系のω計算式などに限られる。原データやFNC定義の誤りを独立データで否定したわけではない。

## IV. 5出力構成と10媒体カテゴリー

### IV-1. 研究成果の構成を先に選ぶ

| 構成（指定の5案） | 科学的自然さ・MDC/MSC | 依存・再現性・重複 | 発見性・引用/版管理 | credit・権利・整備/保守 | 判定 |
|---|---|---|---|---|---|
| **① 単一の統合成果** | 共通入力と二つのRQを二節で区別し、横断MSCも伝えやすい | source、B0、WT、全表の正本が一つ。重複説明が最少 | 二テーマを同じ入口で検索可能。成果単位一つ、版系列一つ | 共通credit/notices/環境記録を一度整備。負荷最小級 | **第一推奨**。統合を新規性増強と称さない |
| ② 別々だが関連する二成果 | 各MDCは成立するが、強い別読者層・別成果物需要は現状未立証 | B0、対象、方法、出所が重複。別改訂時に数値が分岐しやすい | 各題名で発見可能でも、理解に往復が必要。二DOIは合法的に可能だが必然性が薄い | 両方に権利/出所/訂正を管理。相互リンク・版対応が増える | **劣後**。二本化で成果数を増やさない |
| ③ NT-BEのみ公開 | 旧限定MSCを単純に伝えられる | X2を説明せず完結するが、同じB0の未検査軸と下流応答は公開から欠落 | 小さな単独記録として引用可能 | 旧M1–M4が残るため、X2非公開による節約は限定的 | **可能だが劣後**。X2の主張責任を持てない場合の縮小案 |
| ④ X2のみ公開 | X2のQC→endpointという焦点は自立可能 | 旧A→B0の結果全体は不要。ただしB0の定義・FNCコード・参照修正・source/WT表は公開側に必要 | 焦点は明快。統合crosswalkの価値を捨てる | 「旧成果をprivateにしたから旧依存も非公開でよい」とはならない。整備量は①に近い | **第二に自然な構成だが第一推奨にはしない** |
| ⑤ 双方非公開 | 科学的終了として妥当。MSC不足と断定する必要はない | 既存ファイルを保存すれば再作業不要 | 第三者利用・引用・発見の利益は生じない | 公開整備と継続訂正の負担が最小 | **合理的fallback**。負荷や権利説明が解決しない場合に選ぶ |

①を選んでも「二つのRQが一つの新発見になった」とは書かない。NT-BEのA→B0、X2のB0→Bωを別の問い・別の結果として記載し、統合節は対応関係だけを担う。④で公開する場合はAの感度結果を省いても、B0を再現する公開ソース・参照・固定baseline数値を残す必要があり、旧データへの秘密の依存を作らない。

### IV-2. 全10カテゴリーの一次screening

S＝Suitable、C＝Conditionally feasible、N＝Not suitable（今回の目的・範囲で推奨しない）、U＝Not verifiable。形式上の可否と推奨順位を区別する。①～⑤は上表の構成番号。

| カテゴリー | 状態 | 科学的・実務的理由、構成との相性 | 深掘り |
|---|---|---|---|
| 1. Private research record | **S** | ⑤に直接適合。①～④の公開前保存にも有用。公開しない正当な終了形 | 媒体規程不要 |
| 2. 一般的科学発信：記事・ブログ等 | **C** | ①/③/④の要約紹介は可能。説明だけではframeやmaskを照合できず、単独の証拠置き場として弱い。②は分散しやすい | 今回の必須経路にせず、具体SNSを推薦しない |
| 3. Open code/data：GitHub | **C** | ①/③/④でコード・表の閲覧と比較に有用。②は二repoにする利益が乏しい。⑤は非公開保存のみ | **有** |
| 4. 汎用引用archive：Zenodo | **C** | 固定版、配列、表、短い技術記録を同じ成果単位で保存できる。①と最も相性がよい | **有** |
| 5. 分野別data/software archive | **N** | 新規実験構造depositや広い独立datasetが主目的ではない。全5構成で汎用archiveに対する優位性が未立証 | 個別受入は未審査。全サービスの拒否を意味しない |
| 6. Technical report / research note / methods・data・software output | **S（形式）** | ①/③/④の限定的監査に自然。②の二本化は不要。journalのResearch Note枠と無査読技術記録を同格扱いしない | Zenodo上の短いreportとして有 |
| 7. Preprint / working paper | **C、非推奨** | ①/④なら研究記事として構成は可能。ただし新しい推定法や一般化はなく、受理不確実性・原稿整備が増える。②は重複の問題が強い | arXiv一般規程をscreen。特定serverへの投稿推薦はしない |
| 8. 査読誌：regular/short/methods/data/software | **N（優先戦略として）** | 限定的archive監査だけで投稿負荷・査読要求を負う利益が明確でない。新規性不足だけで絶対不受理とは断定しない。JOSSは現形の一回的script群には不適合 | JOSS scope/history条件を確認。個別誌を網羅探索しない |
| 9. Conference/workshop/poster | **C** | ①/④の局所的監査はdiscussion題材になり得るが、会議参加・発表制作・費用が目的外。現行の具体募集枠は**U** | 特定会議を推薦しない |
| 10. その他：upstream issue等 | **C、独立成果の代替にはしない** | 固定FNC引数や説明の注意点を共有できる可能性。ただし公式bugと断定できず、外部対応義務も生じる | 連絡・投稿は今回実施も推薦必須化もしない |

arXivはscholarly archival interestを求め、独創性・意義不足や大きな修正を要するものをdeclineし得る。JOSSは現在、継続した公開開発履歴や十分なsoftware貢献を要求し、minor utility等を除外する。本研究をその条件へ合わせるため、研究拡張や長期software育成を始める合理性はない。[D/I; R18,R19]

## V. 推奨媒体の現行条件・役割・権利

以下は2026-10-19確認。推薦は受理・削除されないことの保証ではない。

| 条件 | GitHub | Zenodo |
|---|---|---|
| 役割 | 人が読みやすいREADME、コード、固定表、差分履歴 | 同じ統合成果の固定版・大きめのNPZ・引用記録 |
| scope・形式 | コード/資料repository。査読論文ではない | 全分野・研究段階・成果形式が対象。短いreportとsupporting code/dataを置ける[R10] |
| 費用 | GitHub Freeで公開repoを運用可能[R14]。有料computeは不要 | 通常deposit無料[R11]。今回規模は標準quota内 |
| 引用 | `CITATION.cff` / preferred-citationで統合reportを指定できる[R15] | version DOIとconcept DOIの役割を分ける[R13] |
| 既公開との関係 | Zenodo archiveと同じ成果の閲覧用コピーにできる | 公開GitHub releaseのarchive経路がある[R16]。別成果・別研究として二重計上しない |
| 更新 | 修正commitとtagを作る。既引用tagの上書きを避ける | 重要なfile変更はnew version。metadata訂正とfile差替えを区別[R12] |
| 発見性 | 検索・コード閲覧・再利用導線。発見を保証しない | DOI・metadata・引用検索の入口。保存しただけで読まれる保証はない |
| 権利 | 自作、MIT由来コード、由来dataのlicenseを分ける。licenseなしを再利用許可とみなさない[R17] | 公開fileのlicense指定とdeposit権限が必要。metadataは原則CC0[R10,R11] |
| AIと著者 | 今回はauthor責任と利用範囲をREADMEにも明記する方針。AI利用だけで貢献を著者扱いしない | AIをauthors/creators/contributorsに載せない。研究の人間による基盤、内容への責任、実質的AI使用のdescription内開示を求める[R20] |
| 公開後負荷 | 環境固定と訂正窓口を記載。継続機能開発は約束しない | 重要誤り発見時の訂正・新版・旧版からの案内を管理 |

**権利とcreditの最小構成。** 公式コード由来のsnapshotにはMicrosoftのMIT copyright/permission noticeを保持する。公式構造dataにはCDLA-Permissive-2.0が適用され、共有dataにはその本文を添える。同規約§3.1はResultsへの制約を課さないが、何を元data・加工data・結果として配るかは区別し、一括して全体を「自作MIT」としない。公式NOTICEはPDBのCC0とMegaScaleのCC BY 4.0を記載するため、含まれる由来を維持する。原著、公式Zenodo DOI、MolProbity定義、依存softwareを引用・記載する。[V,D; R2,R21]

新たなnote本文のlicense、自作codeのlicense、派生表/NPZの扱いは本人が最終決定する。混在するlicenseをファイル群ごとに明示する方式が適切。全原XTCの再配布は最小構成に不要で、公式DOIとmember path/hashから取得させればよい。保存NPZは小さく、今回検算の入力として意味があるので、公開を採用するなら同じ固定版に含める利益が高い。[I]

**一成果一系列の管理。** 推奨は一つの統合Zenodo record系列。GitHubはその閲覧・修正元とし、正式な引用先は同じ統合成果のversion DOIへ揃える。Zenodoが自動で持つconcept DOI＋version DOIは不適切な二重DOIではない。①を選びながらNT-BE、X2、統合noteをほぼ同じ内容で別々のDOIにする必要はない。自動GitHub連携を使うなら、手動depositとの二重登録を避け、一つの経路だけにする。[D/I; R13,R16]

NPZをGitHubの履歴に繰り返し入れず、Zenodoの同じrecordへ置き、GitHubからversion DOIとSHAで参照する運用が低負担。GitHub releaseのコードとZenodo版の対応を一行で明示し、note内の数値表を正本CSVから生成すれば手修正による矛盾を抑えられる。[I]

**訂正の規程には記述差がある。** Zenodoの一般policyは固定保存を説明するが、現行Manage filesは公開30日以内のminor correctionと、元公開45日以内の再publishを認め、その場合DOIは変わらないとする。Manage recordsの簡略文だけで「公開後fileは常に変更不能」とは書かない。科学的数値が変わる訂正はnew version＋変更理由＋旧版からの案内を原則とし、minor correctionでもhashを記録する。metadataは後から編集可能なので、DOIだけで説明文まで永久不変とは考えない。[D/I; R12]

共同著者・所属先の権利をこの監査だけで法的に確定したものではない。ただし提供資料は公開由来で、非公開所属先data流用を示す証拠はない。本人の実際の研究判断・コード確認・原データ実行等を正確に説明し、このAI監査出力を未確認のまま研究本文としてdepositしないことが必要。未知の共同著者を加えたり、所属先の承認が得られたと表現したりしない。[I/U]

## VI. Evidence-based recommendation

本人の公開希望を加点しない順位。[I]

1. **①統合成果：短い技術記録＋GitHub閲覧用コード/表＋Zenodo固定版。** 科学的境界を保ったまま、実装者が保存配列から照合できる利益があり、既存成果の重複整備を最も減らせる。IXの必須事項を満たすことが前提。論文形式・図・別SI・新解析は不要。
2. **①統合成果：Zenodo単独。** 継続repo運用を避けたい場合。同じnote・code・CSV・NPZを一つの版へ保存する。コード閲覧性と修正diffは弱くなるが、核心となる再利用利益は残る。GitHubを必須条件にしない。
3. **⑤双方非公開で終了／公開を延期。** 必須説明への本人確認、権利・AI利用の責任、最小整備が負担になる場合は合理的。科学的失敗ではない。公開価値のためにCoreを増強しない。

②の二成果化は読者・data・codeの重複と版対応の負担が上回る。③は有効なX2の情報を捨てても旧記録整備を免れない。④は実行可能だが、B0の由来説明を要するため①ほど負担を減らさず、横断情報も失う。これらを上位3戦略の数合わせに入れない。

preprint・査読誌を第一候補にしない理由は「数値差が小さいから」ではない。新たな物理的機構、推定量、広範な外的妥当性を示す成果ではなく、価値が既存archiveの監査可能性に集中しているため、より軽い技術記録が情報価値と負荷に見合うからである。受理条件を満たすための研究再開を提案しない。

## VII. Preference-aware feasible options

本人の「小さくても具体的な利用価値があれば残したい」という希望を考慮しても、**第一推奨の構成①は変わらない**。希望を加味する効果は、今回限定MSCを持つ記録を非公開より公開へ進める実務上の選択を後押しする点であり、科学的評価や学術誌適性を上げる点ではない。[I]

採用時の最小構成は、(a)二つのRQ・方法・主要結果・限界を短く説明する一つのnote、(b)旧/X2の全system/pair表と一つのcrosswalk、(c)既存コードと必要snapshot、(d)154保存NPZ、(e)source/環境/コマンド/参照修正/版/権利/AI利用の説明。代表frame/bond表は診断資料として同梱できるが、別論文・別DOI・図集は要らない。**これは構成案であり、今回これらの公開パッケージは制作していない。**

未実測の制作見積もり（新研究なし、既存資料再利用、標準的操作を仮定）：

| 作業 | 本人の実作業 | AI作業 | CPU処理 |
|---|---:|---:|---:|
| 環境・統合経緯の既存証拠整理、欠落の明記 | 15–30分 | 10–25分 | 数分以内が目安 |
| 短い統合noteと再現説明の確認・判断 | 30–50分 | 30–60分 | 表の検算は数分以内 |
| license/credit/AI開示・版の確認 | 15–25分 | 10–25分 | 実質なし |
| 実際の公開操作とリンク/数値確認（別途承認後） | 15–30分 | 10–20分 | 転送時間は回線依存 |
| 合計 | **75–135分程度、30–60分単位で分割** | **60–130分程度** | 計算と通信を分離 |

これらは予算見積もりで、今までの研究時間の復元値ではない。AI作業時間は本人作業へ加算しない。環境log探索が長引くなら、欠落を明示した限定再現説明に切り替えるか延期する。全XTC再解析・新図・論文用の網羅的文献探索・新規CI/閾値grid・MAE最適化・追加SNS原稿を必須化しない。公開後の定期保守は約束せず、重要誤りが判明したときの訂正責任を引き受けられる範囲に留める。[I]

## VIII. Non-publication assessment

双方非公開は十分に合理的な選択肢だが、**現時点の証拠だけから科学的理由で非公開を第一推奨にはしない**。理由は、保存配列の再計算だけで実装照合に使え、標的座標QAも成功し、小さな追加整備で第三者に残せる情報が存在するためである。一般的な大発見がないことは、この用途を消さない。[V/I]

非公開が優位になるのは、(1)本人が内容・AI支援結果の責任を確認できない、(2)実際の権利・機密性問題が判明する、(3)数値や出所の重大な矛盾が後に見つかる、(4)最小整備でも負荷に見合わない場合。今回(2)(3)を示す証拠は得ていない。過去logが全て揃わないことだけで原研究を無効化せず、再現範囲を限定した記録を選べる。[I/U]

「公開を希望するので必ず公開」でも「学術的新規性が弱いので全て非公開」でもない。GitHub単独は引用固定性が弱く、一般記事単独は再解析用証拠が不足するため、軽量公開を選ぶなら固定archiveが中核となる。

## IX. 必須訂正・推奨・任意・未確認事項

### IX-1. 旧M1–M4は何が解消したか

| 旧項目 | 今回解消したこと | 公開前に残ること |
|---|---|---|
| M1：保存後選別と主張の限定 | A/B0/Bω、固定FNC、非線形分解を検証。誤った物理改善主張は支持しないと確定 | 公開説明に同じ境界を反映。70%の分母と境界40→39を明記 |
| M2：出所・snapshot・環境・実行 | 公式benchmark checksum、20原メンバーのSHA、今回QA環境を直接確認 | 元研究環境の回収、または不明の明記。今回版との混同を避ける。実行コマンドの引数を固定 |
| M3：153＋1→154/112、WT・最終hash | 全完成表、154 NPZ、全reference SHA、対象/順序/共有WT、回復系座標QAを検証 | 元153/111と回復1系の作業履歴は未提出。完成表への統合ルールと欠落を説明。古い153/未実行表記を正本から除く |
| M4：検証範囲・clipping・権利・AI | 検算範囲を拡大し、MIT/CDLA/NOTICEと現行AI policyを確認 | 公開fileへnotices/適切なlicense/credit/AI利用と人間責任を反映 |

M1–M4を全て「未着手」と再宣言するのは不正確。一方、この監査報告ができただけで将来公開物へ反映済みとも言えない。**数値検証の大部分は今回完了し、残りは公開説明と本人確認が中心**である。

### IX-2. 優先順位・依存・最小証拠

| 区分・優先 | 作業と担当 | 依存／最小必要証拠 | 完了条件・不要な拡張 |
|---|---|---|---|
| **Must-fix 1** | AIが説明案、本人がclaim確認：A/B0/Bω、分母、境界、MAE、因果の限界 | 本報告IIと固定CSV/NPZ | 主解析数値は維持。70%はtarget基準、40と診断39を区別。新規計算不要 |
| **Must-fix 2** | AIがreproducibility記録、本人が元環境・実行履歴を確認 | 公式DOI/hash、現存log/PC記録、今回検算 | 旧版と今回版を区別。取得不能は不明と明示し再現主張を限定。失われたlogを復元したふりをしない |
| **Must-fix 3** | 正本と時点の整理 | 153＋回復1の説明、154/112完成表、最終hash | READMEを現在の状態に更新し、実装時「未実行」は履歴へ。二重集計や別数値の正本を残さない |
| **Must-fix 4** | rights/credit/license/AI開示 | 公式LICENSE/NOTICE/CDLA、実際の人間の役割、本人の同意 | 既存code noticeを保持。AIを著者にせず、実質支援を明記。本文の責任を本人が判断 |
| **Must-fix 5：公開採用時のみ** | 一成果一版系列、配布実行経路の確認 | ①の採否→最終file list→SHA→tag/record対応 | NPZからの検算経路と元XTCからの経路を分ける。FNCSettings明示。投稿や追加研究は不要 |
| Recommended | 一つのcrosswalkと入力manifest、保存NPZを同じ版で提供 | Must-fix 2/3 | 再利用者が元XTC全体を取得しなくても算術検算できる |
| Recommended | 代表事例を短く説明 | 既存frame/bond表 | 相殺・増幅と結合因果の違いが読めれば十分。新図は不要 |
| Optional | 仕上げ図、一般記事、追加配布先、広い文献追跡 | 科学的完成後、必要を本人が判断 | 公開条件にしない。今回作成しない |
| Unresolved | 元実行依存版・完全な153＋1履歴 | 元logの現存状況 | 不明のまま限定公開可能。全再実行を義務化しない |
| Unresolved | 全archive checksum、残り144系座標再計算 | 原ZIP全bytes／該当座標 | 今回の限定監査の必須追加ではない。完全再現認証を主張する場合は別問題 |
| Unresolved | kinase本文/SI、eLife版の追加内容 | 正式全文へのアクセス | 世界初・全面的非重複は主張しない。今回の低負荷記録公開を無期限保留しない |

今回、根本的欠陥に基づく研究再開・主要数値訂正・Protocol変更の要求はない。必要なのは、この表で定義した有限の記録整備である。新しいGateを追加せず、本人が公開を選んだ場合の制作工程で完了させる。

## X. STOP and handoff

**このWorkの独立評価を完了し、STOPする。** 新しいRQ、閾値grid、モデル生成、MD、全件Primaryのやり直しは行っていない。Phase Aとして既存配列全件の算術検算と標的10系の固定座標QAのみを行った。GitHub/Zenodoへの操作、投稿、SNS、外部連絡、公開用本文・図・SI・公開ZIPの本制作は行っていない。

本人が次に決める事項は、(1)①統合公開を採るか⑤非公開/延期とするか、(2)公開ならGitHub＋ZenodoかZenodo単独か、(3)欠落した過去履歴を明示した限定再現説明を受け入れるか、(4)人間としての内容責任・credit・licenseを確定できるか、の4点。決定後は必須整備と公開準備へ進めばよく、今回のGateを最初から繰り返す必要はない。

### 付録A：出典台帳（確認日すべて2026-10-19）

以下のURLは今回の確認先。取得方法によってWeb表示が失敗しても、実際にPDF bytesを取得した場合はその旨を記載する。未取得全文を既読と扱わない。

| ID | 出典・URL | 今回の取得範囲 |
|---|---|---|
| R1 | Lewis et al., Science 2025, [DOI](https://doi.org/10.1126/science.adv9817)、[著者accepted manuscript＋SI](https://www.microsoft.com/en-us/research/wp-content/uploads/2024/12/accepted_paper.pdf) | PDF 31,205,701 bytesを直接取得。S20 sigmoid、S24–25 filter、S28 ΔΔG等。SHAを検算JSONに記録 |
| R2 | [公式data/code record 15672282](https://zenodo.org/records/15672282) | record/checksum/licenseを閲覧。benchmark ZIP bytes一致、sample ZIPは20メンバーを部分取得 |
| R3 | [BioEmu-Benchmarks](https://github.com/microsoft/bioemu-benchmarks)、[PR #24](https://github.com/microsoft/bioemu-benchmarks/pull/24) | 現行READMEの非互換性/環境警告とPR本文・merge日。固定関数は添付snapshotを検査 |
| R4 | Williams et al., Protein Sci. 2018, [DOI](https://doi.org/10.1002/pro.3330)、[著者側PDF](https://keedylab.org/pdf/2018_williams.pdf) | PDF 4,605,445 bytes、p.305のcis/twisted節をテキスト・ページ画像で確認。PMCはchallenge |
| R5 | [ProteinConformers 2025 PDF](https://aideepmed.com/papers/2025_9.pdf)、[公式code](https://github.com/auroua/ProteinConformers)、[Rama code](https://raw.githubusercontent.com/auroua/ProteinConformers/main/tools/tools_calculate_rama_outlier_rates.py)、[eLife版](https://elifesciences.org/reviewed-preprints/110874) | 2025 PDF 17,638,944 bytes、Table 1ページ画像、該当本文とRama codeを確認。eLife本文未取得 |
| R6 | Shin et al. 2026, [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/42670848/)、[DOI](https://doi.org/10.1021/acs.jcim.6c01677)、[公式SI](https://acs.figshare.com/articles/journal_contribution/33148171)、[SI API](https://api.figshare.com/v2/articles/33148171) | abstract、SI題名/DOI/file情報。本文403、ci6c01677_si_001.pdfのbytesは403/500で未取得 |
| R7 | Richman et al., [arXiv:2512.03312v1](https://arxiv.org/html/2512.03312v1) | 本文§3.3/4.4、App.E Table S3、App.Gを閲覧。査読済み認定なし |
| R8 | Xie et al., [arXiv:2602.16634v1](https://arxiv.org/html/2602.16634v1) | §2.2式16–17、§5/式と方法を閲覧。査読済み認定なし |
| R9 | [BioEmu](https://github.com/microsoft/bioemu)、[physical steering YAML](https://raw.githubusercontent.com/microsoft/bioemu/main/src/bioemu/config/steering/physical_steering.yaml) | READMEとYAML bytesを確認。YAMLの現物SHAを記録、main全履歴を固定したとはしない |
| R10 | [Zenodo General Policies v1.0](https://about.zenodo.org/policies/) | scope、研究段階、rights、license、metadata CC0 |
| R11 | [Zenodo Terms of Use v1.3](https://about.zenodo.org/terms/) | 無料deposit、投稿者責任、CERNの承認を意味しないこと |
| R12 | [Manage files](https://help.zenodo.org/docs/deposit/manage-files/)、[Manage versions](https://help.zenodo.org/docs/deposit/manage-versions/)、[Manage records](https://help.zenodo.org/docs/deposit/manage-records/) | minor correctionの30/45日、new version、metadata編集。ページ間の簡略記述差も記録 |
| R13 | [What is DOI versioning?](https://support.zenodo.org/help/en-gb/1-upload-deposit/97-what-is-doi-versioning) | concept DOIとversion DOI |
| R14 | [GitHub's plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) | Free/public repository |
| R15 | [About citation files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files) | CITATION.cff、report/preferred-citation |
| R16 | [Referencing and citing content](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content) | GitHub公開releaseとZenodo連携、releaseごとのDOI |
| R17 | [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) | 再利用許可とlicenseの必要性 |
| R18 | [JOSS submitting](https://joss.readthedocs.io/en/latest/submitting.html) | Scope/significance、公開開発履歴6か月以上、minor utilityの扱い。具体投稿は推薦しない |
| R19 | [arXiv moderation](https://info.arxiv.org/help/moderation/index.html) | scholarly interest、content type、類似投稿の統合/版管理。具体投稿は推薦しない |
| R20 | [Zenodo generative AI policy for depositors](https://support.zenodo.org/help/en-gb/13-policies/227-what-is-your-usage-policy-for-generative-ai-for-depositors) | 2026-04-27公開。人間の研究基盤、責任、AI著者不可、実質使用開示 |
| R21 | [CDLA-Permissive-2.0](https://cdla.dev/permissive-2-0/)＋添付公式LICENSE/NOTICE | §2.1と§3.1、MIT notice、PDB/MegaScale由来 |

### 付録B：監査成果物と再実行範囲

本報告と対になる `NTBE_Gate_Evidence_2026-10-19.json` には、保存配列検算、標的座標QA、全入力/メンバーhash、NPZスキーマ、取得記録、スクリプト本文・hashをまとめた。これは監査証拠であり、公開用研究パッケージではない。

- `NTBE_Gate_Checks_2026-10-19.py`：添付ZIPを展開した `audit_inputs/primary`, `audit_inputs/official`, `audit_inputs/npz` と `upload` を入力とする。numpy/pandasを使い、座標を再生成しない。
- `NTBE_Targeted_Archive_Fetch_2026-10-19.py`：公式ZIPのRange応答とCRCを検証し、指定10系の元メンバーだけを取得する。作業rootで実行。`sources`を事前に用意する。ネットワーク依存であり、全archive MD5検証ではない。
- `NTBE_Targeted_Coordinate_Checks_2026-10-19.py`：上の元メンバーと公式reference、snapshotを入力とする。依存版はII節に記載。ωは別式、FNC/filterは同snapshot関数の再実行。

今回のスクリプトはAIが作成し、実データへ実行して出力と元表を照合した。人間による最終科学判断や公開可否の承認は代行していない。検算コード自身にも実行時の依存・入力構成があるので、単にPYを開くだけで元データなしに全検証ができるとは説明しない。
