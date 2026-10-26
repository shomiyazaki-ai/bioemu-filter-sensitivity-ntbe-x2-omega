# NT-BE／X2-ω — Phase 1A 独立科学妥当性監査

評価日：2026年10月26日（日本時間）  
対象：公式BioEmu benchmark metadataの154 systems／112 mutant–matched-baseline pairs  
範囲：Scientific Validityのみ。Phase B/C/D、新規研究、公開物変更は実施していない。

## 1. Executive Scientific Decision

**総合判定：A2 — Valid with mandatory corrections（必要な訂正・明示を伴って妥当）。**

**成立する中核は「固定された保存ensembleを固定規則で選別すると、同じFNC由来推定量がどの程度変化するか」という記述的結果である。主要なframe数、ΔG・ΔΔG、MAE、段階間の増幅・相殺を覆す計算誤りは見つからなかった。** 保存データを条件付きで再選別した結果であり、正しい平衡集団の回復、真の自由エネルギーへの補正、モデルの一般的性能改善を示すものではない。

A2の対象は、主解析値の撤回ではなく、次の限定された方法・証拠の記述である。

1. L2を「全経路の完全独立検証」「全入力・依存コードをfingerprintで保証」と扱わない。公式FNC/clash再使用、未記録のimport snapshot、aggregateのPASS条件の不足を明示する。
2. 境界の全許容／全除外は**二つの選別シナリオ**であり、ΔG・ΔΔGの数学的上下限でも座標誤差の信頼区間でもない。
3. 実装から復元した固定規則と、結果閲覧前の正式承認を立証できる規則を区別する。独立した最終Protocol・完全な当時の環境は未回収。
4. 方法を再利用する際は、ωの両平面からの最小偏差、FNCの明示Settings、filterの原子集合・候補探索を正確に記載する。短い公開Methodsだけでは完全な条件は分からず、元コードが必要である。

**個々の固定数値・集合関係はA1相当。上記の強い認証claimは非支持またはA3である。** 研究全体をA3とするほど中核観察の根拠が失われているとは判断しない。A4を支持する重大な反証もない。A2を過去の評価から転記したのではなく、Package 03を開く前に同じ暫定判定を保存した。

公開Technical NoteとZenodo説明には、一般化・平衡回復を主張しない旨が既に明記されている。旧Gateも境界対照を上下限とみなさないと明記していた。**存在しない過大主張を訂正対象として作り出さない。** 上記2は、その限定を維持する必要条件であり、現公開本文に上下限claimがあると認定したものではない。上記1は今回追加されたL2証拠を今後説明する際の必須事項である。

## 2. 評価基準、証拠階層、読込順序

正式基準は `Post_Research_Independent_Assessment_Protocol_v1.0_FINAL(4).txt` のPhase A。`Research_Design_Master_v1.6_PROPOSED_2026-10-25(1).txt` はUSER REVIEW PENDINGとして扱い、歴史的研究条件を遡及変更しなかった。

| ラベル | 本報告での意味 |
|---|---|
| [V] | 今回、実ファイル・コード・保存配列・別算式の検算で直接確認 |
| [H] | 本人のローカル実行や過去の座標検証の記録を継承。今回その元座標計算は未実行 |
| [D] | 公式一次資料・配布コードの仕様を確認 |
| [I] | 証拠からの科学的解釈・推論 |
| [U] | 未検証または資料不足 |

**[V]「L2 JSONに154 PASSが記録されている」と[H]「Windows上で元XTCを処理した」は異なる。** 本Workは1.96 GBの元アーカイブを取得しておらず、全154系のraw-coordinate replayを実施していない。

Package 01・02を先に開き、元コード、公式snapshot、元表、154 NPZ、L1/L2を検査した。公式資料と公開物も確認したが、公開物はclaimの監査対象として扱った。暫定判定を保存しSHA-256を固定した後にPackage 03を初めて開いた。

- 暫定判定ファイル：`Phase1A_Independent_Preliminary_Judgment.md`
- 固定SHA-256：`a13962f839442e45e1c13f8d8edebbb6ccafc0c8e88584296d56bc76b0b45f5f`
- 読込順序とハッシュ：`Phase1A_Verification_Results.json` の `preliminary_freeze`／`historical_open`
- Package 01は15、02は10、03は5のmanifest対象ファイルが全てサイズ・SHA-256一致。[V]

Package 01の引継ぎ自体には旧評価も含まれるため、完全なblind reviewではない。その評価文を正当性の根拠には使わず、Protocol復元とデータ・コード照合を分離した。単一の監査実行であり、別の人間専門家による査読を意味しない。

## 3. Independent Claim–Evidence Matrix

| ID | Claim | 判定 | 根拠・成立範囲 |
|---|---|---|---|
| C01 | 154系＝42 baseline＋112 mutant、112対応ペア | **Supported / A1** | [V/D] 公式system_info、統合表、NPZ、L2 ID集合を照合。42はmetadata上のmatched baselineであり、全て自然配列の未変異WTという意味ではない |
| C02 | 回復1系は条件変更を伴わない | **Supported / A1** | [V] コード差分は参照探索のみ。153成功行＋回復行と統合表が数値許容差内一致 |
| C03 | A⊇B0⊇Bωと主要frame件数 | **Supported / A1** | [V] 全保存配列を再集計。[H] 元XTCからの適用はL2記録 |
| C04 | B0は固定公式評価側filterの結果 | **Supported、独立性限定** | [V/D] snapshot関数AST一致・保存mask連続性。[H] L2で同関数を座標へ再適用 |
| C05 | B0は完全に物理的に妥当な構造集合 | **Not supported** | [D/I] 距離上限と限定的clashのみ。ω、Rama、全側鎖、エネルギー等を全面認証しない |
| C06 | B0に30°規約上twistedなpeptideが残る | **Supported / A1** | [V] 27,329 bond–frame観測、25,807 frames。[H] 角度の座標対応はL2。構造検証規約を満たさないという意味 |
| C07 | FNC・soft foldedness・logit ΔG、mutant−baseline ΔΔG | **Supported / A1** | [V/D] 明示設定・公式式と一致。別算式の保存配列検算で最大ΔG差4.56×10⁻13 kcal/mol |
| C08 | 19/112、40/112、累積44/112と3段階MAE | **Supported / A1、記述のみ** | [V] 全件再集計。統計的・生物学的有意差ではない |
| C09 | 除外集団のfoldednessと共有WT差分が符号・相殺を説明する | **Supported、算術的説明** | [V/I] 集団平均の恒等式と差分。局所twistが物理的安定性を因果的に決めることの証明ではない |
| C10 | 30°は科学的根拠がない任意の数値 | **Not supported** | [D] MolProbityのtwisted定義に根拠あり。ただしensembleへの最適acceptance ruleは未証明 |
| C11 | L2により全経路を独立実装で認証できた | **Not supported / A2で限定** | [V] ω・CA/CNには別式、FNC/clashには共通関数。入力読み取りもMDTrajを共有 |
| C12 | 境界2条件が全てのΔΔG摂動を挟む | **Not supported** | [V/I] 29/112でPrimaryが二値間の外。シナリオとしての数値は支持 |
| C13 | 「40ペア」が全ての精度摂動で不変 | **Not supported** | [V] 既存±0.02°シナリオで39。固定Primaryの40を上書きする理由ではない |
| C14 | XTCは時間自己相関を持つMD軌跡である | **その前提はNot supported** | [D] 原著はiid生成を記述。[U] 当該保存物の全seed/batch履歴は未回収 |
| C15 | 一般的な予測性能改善・真の自由エネルギー補正・平衡回復 | **Not supported** | [I/U] 正しい母分布・重みの検証なし。公開本文もこれを主張していない |
| C16 | 全条件の結果閲覧前の正式固定、完全な歴史的環境一致 | **Inconclusive / A3（当該claim）** | [H/U] 引継ぎとコードはあるが、最終承認原本・全ログ・lockfileなし |

## 4. Method and Code Audit

### 4.1 Protocol復元と153＋1の回復

NT-BEのP01–P15は2026-10-18引継ぎ第2節に記載され、Coreは `protocol='NT-BE P01–P15 v1.0'` を記録する。X2引継ぎは30°、Unknown保持、共有WT、0.1 kcal/molを報告用とする規則を記載する一方、最終decision ruleの本人確認を求めている。したがって、**当時の実行規則の再構成は可能、最終承認の独立証明は不可**と判断する。[V/H/U]

初回 `systems.csv` は154行中153 PASS、`1TG0__D45C_N47P` のみ同名PDBを2個検出してFAIL_QA。回復版の差分は以下だけである。[V]

- 元：ZIP全体で `/{sid}.pdb` のsuffix検索。
- 修正：公式asset内の `reference_mutants/` または `reference_wildtypes/` をmetadataで選び、完全パス一意性を検査。

公式asset外の `tests/test_data` にある同名ファイルの検出を避ける処置であり、FNC、filter、温度、対象、閾値の変更ではない。回復系はA=200、B0=199。回復単独のpairがNOT_COMPARABLEなのはWTを同時実行していないためで、元WTと統合して112番目を算出する方法は妥当。

全153成功行＋回復行と統合表の共通列に、1e-9を超える差はない。619セルに数値文字列再保存の末尾差があり、最大4.44×10⁻16。これは科学的な数値不一致ではない。今回の検算コードは当初ここを厳密float等価で判定したためFAILしたが、表の再保存差と確認し、許容差を明記した比較に訂正した。元研究の誤りとして計上していない。

### 4.2 Geometry filterの実際の意味

`ntbe_official_filter_snapshot.py` の2関数と公式benchmark `utils.py` の対応関数はAST一致。[V/D]

| 条件 | 実装規則 | 限界 |
|---|---|---|
| 隣接Cα | 全ての隣接残基で距離 **<4.5 Å** | 下限を検査しない。単一鎖連続配列を前提 |
| 隣接C–N | 全ての隣接残基で距離 **<2.0 Å** | 結合角・peptide平面性は検査しない |
| nonlocal clash | **|i−j|>2**の候補残基対で最短heavy-atom距離 **>1.0 Å** | 近接配列・同一残基内を含む完全なclash検査ではない |
| clash候補 | trajectory内のいずれかのframeでCα距離 **<6.0 Å**になった対 | 残基内原子がCαから約2.5 Å以内という想定に依存 |
| 合成 | 上記3 maskのAND | 通過＝この検査への通過に限る |

距離はMDTrajのnmからÅへ変換。サンプル距離計算はperiodic=False。clashの `compute_contacts` は提示原子のclosest-heavyを利用する。公式生成コード `convert_chemgraph.py:compute_backbone` はN、CA、C、OにCBを含む表現を出力する。**全面的なall-atom side-chain physical validationではない。** 元XTCの全topology原子を今回読み直したわけではないので、実サンプル原子名の全系保証はL2等の[H]と区別する。

公式関数の注意書き通り、Cαから遠く単独で飛び出した原子は候補探索で見逃し得る。任意の構造・複数鎖・極端な変形へ汎用的に適用できる保証もない。今回、これが主要maskを誤らせたという証拠はない。B0を「公式関数で定義したsubset」と呼ぶには問題なく、全物理妥当性の証明に使うことだけを制限する。

生成側snapshotはclashを `mdtraj.compute_contacts(traj, periodic=False)` で評価し、評価側には上記Cα候補絞り込みがある。Aで更に4,612 framesが落ちる事実から、生成時filterが無効だった、または公式処理が矛盾したとは結論できない。生成側と評価側の経路差、実際の生成オプション未回収を区別する。[V/D/U]

### 4.3 FNC、参照、残基対応

公式benchmarkのFNCSettingsと5関数は抽出snapshotとAST一致。[V] 各系の参照PDBのSHAがCore記録に一致し、154系全てで参照配列＝metadata配列、各残基CA一つを独立PDB読み取りで確認した。参照native-contact数も、PDBのCA座標から直接距離を計算して全154系で一致した。[V]

参照contact集合はCA同士、**|i−j|>3**かつ参照距離≤10 Å。対を両向きに登録するが、均一に二重化して平均するためFNC値は変わらない。実装は次式である。

\[
q(x)=\frac1{|C|}\sum_{(i,j)\in C}\frac1{1+\exp\{5[d_{ij}(x)-1.2d^{ref}_{ij}]\}}.
\]

λ=1.2、δ=0、β=5 Å⁻¹。参照CAとsample CAを配列alignmentで対応させる。`pairwise2.globalxx` は一般には曖昧な対応やgapを持ち得るが、今回の参照・metadata配列は一致し、Coreは不完全contact mappingを停止、L2はsample/reference/metadata配列の一致を検査する。今回の全sample側検査は[H]であり、参照側の独立確認は[V]。

**デフォルトの落とし穴は存在するが元研究の誤りではない。** 裸の `get_fnc_from_samples_trajectory` はλ=0、δ=1.2を既定とする。一方、公式evaluate、Core、L2は `FNCSettings` のλ=1.2、δ=0を明示する。再現コードを「公式関数を呼ぶだけ」に短縮すると異なる量になる。

FNCはreference-native contactsの保持度であり、局所bond validityや自由エネルギーそのものではない。native-likeであってもω異常を持ち得るし、native contactsが少ないことはそれだけで非物理構造を意味しない。

### 4.4 Soft foldednessと自由エネルギー変換

\[
f(q)=\frac1{1+e^{-20(q-0.5)}},\quad p_S=\frac1{|S|}\sum_{x\in S}f(q_x),\quad
\widehat{\Delta G}_S=-RT\ln\frac{p_S}{1-p_S}.
\]

R=0.001987203599772605 kcal mol⁻¹ K⁻¹、T=295 K。**平均FNCへsigmoidを適用するのではなく、frameごとに変換してから平均する。** ΔGはfolded−unfoldedの符号。ΔΔGはmutant−対応baseline。RとkBの名称差は、mol単位の定数を使うこの式では数値・単位の誤りではない。

空集合はCore/X2でNone・非比較として扱う。今回Bω最小は128 framesで全154系が非空。pを[1e-10,1−1e-10]、oddsを[1e-10,1e10]へclipするが、**擬似カウントの加算はない**。q∈[0,1]ならsigmoidの値は約4.54e-5～0.9999546に収まり、有限・非空の現規則ではclipに達しない。したがってclipping flagがゼロであることを、極端条件に対する頑健性の実証とはしない。

今回、保存qを用いて `0.5*(1+tanh(10*(q−0.5)))` と `log(p)−log1p(−p)` による別算式で全系を検算した。最大ΔG差4.5564×10⁻13 kcal/mol。FNCそのものを別実装で全元座標から求めた意味ではない。

公式原著SIの自由エネルギー評価節はPPFTと同じsoft foldednessを使うと記載する。hard thresholdによる別のtraining/reweighting説明と混同しない。SI式S12のk表記だけから実装を反転させず、公式実行コードの増加sigmoidを正本とする。保存推定値は、この操作的状態定義とモデルensembleに依存する推定量であり、実験的自由エネルギーの再測定ではない。[D/I]

### 4.5 Peptide ωと30°規則

四点は **CA(i)–C(i)–N(i+1)–CA(i+1)**。wrapを[−180°,180°)とし、

\[
d_\omega=\min\{|\operatorname{wrap}(\omega)|,|\operatorname{wrap}(\omega-180°)|\};\quad twisted\iff d_\omega>30°.
\]

30°ちょうどは除外しない。cisとtransのどちらにも近くない場合を除外し、cisを一律に落とさない。Pro分類は次残基i+1。これはMolProbityのtwisted定義を採用した操作であり、MolProbity全検査を実行したという意味ではない。[D/V]

主解析は射影ベクトル式、L2は平面法線式。今回、既知角度（0、±30、±90、±150、±180）、剛体変換、鏡映による符号反転、退化四点のUnknownを純粋関数で検査し、合格した。MDTraj依存の元unittest一式は今回再実行していない。

単一鎖L残基にはL−1個の候補結合を作り、鎖端に仮想結合を作らない。全154 NPZでL−1、隣接quartetのCA共有、next-is-Proと配列の一致を確認。[V] 主解析には欠損原子・非有限角のUnknown保持、重複原子・系統的不整合の停止処理がある。全B0でUnknown=0。一般的な欠損・複数鎖validatorとしての完全性は未認証。

Bωは `B0 & ~any(known_twisted)`。保存float32角から独立modulo式で再分類し、全154 maskと一致。30°ちょうどの保存角は0、最も近い保存偏差と30°の距離は3.05176×10⁻5°。L2の最大角度差7.62939×10⁻6°は保存角との比較であって、XTC圧縮前の真の座標精度や実構造誤差を測った値ではない。

## 5. Numerical and Provenance Audit

### 5.1 再確認した主要数値

| 指標 | 今回の結果 [V] |
|---|---:|
| A／B0／Bω | 302,800／298,188／272,381 frames |
| A→B0除外 | 4,612（Aの1.523%） |
| B0→Bω除外 | 25,807（B0の8.655%） |
| B0の評価可能ω | 14,922,082 bond–frame観測 |
| B0のtwisted ω | 27,329（約0.1831%のbond–frame観測） |
| B0のUnknown | 0 |
| ΔΔG変化中央値 A→B0 | +0.000966323 kcal/mol |
| ΔΔG変化IQR A→B0 | −0.0320311 ～ +0.0258302 |
| ΔΔG変化中央値 B0→Bω | +0.000845103 kcal/mol |
| ΔΔG変化IQR B0→Bω | −0.0370005 ～ +0.0872697 |
| 最大絶対ΔΔG変化 A→B0／B0→Bω | 0.575240／0.486820 kcal/mol |
| 報告用|変化|≥0.1：A→B0／B0→Bω | 19／40 pairs |
| 上記の共通／和集合／累積A→Bω | 12／47／44 pairs |
| ΔΔG MAE A／B0／Bω | 0.702594786／0.696141628／0.707681002 kcal/mol |
| B0→Bω実験絶対誤差改善／悪化 | 54／58 pairs |

全154系に少なくとも1つtwistedを含むB0 frameがあり、追加除外が生じる。ただしframeは多数の結合を含むため、**8.655%のframe率と0.1831%のbond率は異なる分母**である。系長、サンプル数、各残基の頻度が違う以上、集約率だけから系間の品質順位やProの因果効果を論じられない。

under70は `Bω <0.7×num_samples_target`。該当は `2RRT__A48P`（128/200）、`2RRT__F9P_F61V`（134/200）、`4C26__S6N_H43H`（136/200）。B0を分母とする割合ではない。公開版はこの点を既に正しく説明している。旧Core P15の各flagゼロも、S0–S4が同じ対象になるというだけで低情報条件への検証ではない。

### 5.2 L1/L2が実際に確認したもの

| 層 | 入力・計算 | 独立性と本Workの証拠等級 |
|---|---|---|
| L1 archive hash | 1,959,113,732 bytes、MD5、SHA-256 | Windowsの実測記録[H]。公式公開MD5との文字列一致[D/V]。本Workで元archive全体をhashしたわけではない |
| source対応 | 元XTC/PDBとCoreのSHA、reference SHA | L2がbyte比較[H]。記録相互の154系一致は今回[V] |
| CA/CN | 座標差の直接ノルムと公式maskの比較 | 算式は独立、座標ローダーMDTrajは共通[H/Vコード] |
| clash | `flt.filter_unphysical_traj_masks` | 元Coreと同じ公式関数。独立clash実装ではない |
| ω | 独立quartet構築＋平面法線式 | 元射影式とは別算式。原子選択規約とMDTraj入出力は共有 |
| FNC | `fnc.get_fnc_from_samples_trajectory`＋明示Settings | 座標から再計算するが共通公式実装。保存FNCは比較対象であって計算入力ではない |
| ΔG | 再計算qからexpit→logit | Core A/B0比較あり。Bωの元CSV値との直接比較はrun_system内にはない |
| pair | system ΔGの差分 | L2 aggregateは旧A/B0との比較。Bωの元X2表との照合は別の後続検算が必要 |
| 本Work | 154 NPZ／CSV／L2個別154 JSON／112 pair | Bωも含め今回全件比較[V]。raw-coordinate replayではない |

L2の実行記録はPython 3.13.1、MDTraj 1.10.2、NumPy 2.2.1。これを元Primaryの完全な当時環境とみなさない。本Workの配列検算はPython 3.12.14、NumPy 2.3.5。MDTrajをインストールして全座標検算した環境ではない。

L2 `fingerprint` にはarchive、benchmark ZIP、all_npz、Core CSV、script、chunk=100がある。**実際に動的importする `official_fnc_snapshot.py`／`ntbe_official_filter_snapshot.py` のhash、pair CSV、SciPy/Biopythonの版は含まれない。** したがってresume時に「全依存条件が同一」とは証明できない。添付snapshotが公式に一致することと、L2実行時のファイルがまさにそれだったという暗号学的な連結は別である。

さらに `main --mode aggregate` はpair CSVが無い／複数ある場合にpair検査をskipできる一方、`all_pass = counts['PASS']==154 and not pair_problem` はTrueになり得る。これは**検証コードの潜在的な判定不足**。今回の出力には実際に112 pairが存在し、全件を再照合したため、今回の研究にpair欠落があったとの結論にはならない。

chunk単位のclash候補探索はtrajectory全体探索と候補集合が異なり得る。通常の残基内幾何の想定が破れればchunk依存性が起こり得るが、今回のL2は各frameの保存B0 maskとの一致を記録している。[H] これを任意のchunkサイズ・任意の変形への保証に拡張しない。

### 5.3 境界302対292：実差ではなく集計範囲差

L2の `max_near_boundary_frames` は名前にmaxを含むが、実際には**全A frameにおけるany(near)の総数**。Primary `near_boundary_frames` はB0に限定する。今回、保存near maskから両方を計算し、302と292を直接確認した。[V]

差の10系とA-onlyの0-based frame index：

| system | frame |
|---|---:|
| 1EM7_V54S__D47W | 206 |
| 1PGA_L7S | 194 |
| 2M8U__K2Q | 387 |
| 2RRT | 2008 |
| 2RRT__A48P | 179 |
| 2RRT__F9P_F61V | 104 |
| 2ZW1_V55S__T3I | 765 |
| 4C26 | 1186 |
| EA_run2_0290_0001__E26I | 2481 |
| EA_run3_1140_0005 | 4553 |

各系1 frameずつ。B0/Bω件数やΔGの不一致ではない。正しい最小対応は、報告上 `near_frames_A`／`near_frames_B0` と区別すること。元JSONを無断訂正したり再計算したりする必要はない。

### 5.4 境界シナリオの非単調性

既存±0.02°診断について、nearに該当するtwistを許容する集合と、nearを全て除外する集合がある。しかし、集合の包含はfoldedness平均の単調性を保証せず、mutant−WTでは相殺も起こる。**二集合の出力は推定値の上下限にならない。**

| mutant | Primary D | near全除外側D | near許容側D |
|---|---:|---:|---:|
| 1EM7_V54S__D47W | −0.1003079005 | −0.0989172631 | −0.0994791297 |
| 4C26__K58A | +0.0007984011 | −0.0017544305 | −0.0002972162 |

DはB0→BωのΔΔG変化、単位kcal/mol。Primaryが二つのシナリオ値の間にない例は29/112（1e-12許容）で、全IDは検算JSONに記録した。前者の1ペアが報告閾値を跨ぐため、40が両シナリオで39になる。

これは既存固定診断の意味の検査であり、新しい閾値探索ではない。±0.02°は記録された診断幅で、測定された座標不確かさの95%区間ではない。全浮動小数・XTC圧縮誤差を覆う保証もない。固定保存座標に対するPrimary値は維持できる一方、40という件数の一般的精度頑健性は主張できない。

## 6. Scientific Interpretation and Alternatives

### 6.1 この解析が表す操作

選別後の経験分布は、元の保存分布をmaskで条件付けて正規化したものになる。重みが0/1に変わるという数学的意味で再重み付けだが、Boltzmann重みへの補正やimportance-samplingの不偏化ではない。

B0のframe数n、除外数r、除外集団の平均soft foldednessをp_removedとすると、

\[
p_\omega-p_0=\frac{r}{n-r}(p_0-p_{removed}).
\]

全154系で保存配列から検算して成立。この式は、除外率だけでは変化の符号や大きさが決まらない理由を説明する。さらに `dΔG/dp=−RT/[p(1−p)]` なので、pが端に近ければ小さな平均差でもΔG差が大きくなる。これ自体は新しい機構の発見ではなく、固定推定量の性質である。

`1TG0`ではω除外集団のfoldednessが保持集団より高くΔGは+0.130724変化する一方、`1TG0__E1N`は−0.239841。差を取るとpair変化−0.370565となる。`4C26`と`4C26__K58A`は両方約−0.124で、pair変化は+0.000798へ相殺される。これらは構造修復による真の安定化・不安定化の実験ではない。

### 6.2 代替説明がclaimに与える実際の影響

| 代替説明・問題 | 今回の中核を覆すか | 判断 |
|---|---|---|
| 選別がfoldednessと相関する | 覆さない | 条件付き平均が変わる直接の説明。性能改善の証明を制限 |
| logitの非線形増幅 | 覆さない | 少数除外で大きなΔG差が出ても実装誤りとは限らない。物理的重要性と分ける |
| 共有WT | 覆さない | pair差は正しいが112独立反復ではない。42群にも相同性等の依存があり得る |
| 有限サンプル・稀なunfolded側の情報不足 | 固定記述は覆さない | 母集団の期待値・推定差の有意性は未確定。小MAE差の優劣認定には不十分 |
| MD時系列の時間自己相関 | この資料からは確定しない | XTCは格納形式。BioEmuは原著上iid生成。モデル学習データのMDと生成物を混同しない |
| 保存ensembleの代表性、生成時filter履歴 | 固定記述は覆さない | Aが生成全体・真の平衡分布を代表するとの主張は不可 |
| FNCと物理妥当性の非同一性 | 中核を限定 | B0/Bωは操作的QC集合。FNCの高低だけでは物理品質を認証できない |
| 30°規則を平衡ensembleに適用すること | 観測は覆さない | 規約に根拠はあるが物理的に最適な選別との保証なし |
| ランダム等数除外対照なし | 記述には必須でない | 選別固有の効果が単なる除外数効果を超えるという比較claimは未証明 |
| 訓練・校正と評価の独立性 | 今回の差分算術を覆さない | 原著に分割説明はある。154 IDの訓練履歴全照合は未実施。漏洩を発見したとも独立外部検証したとも言えない |

有効サンプルサイズは今回推定していない。iidという生成モデルの仕様と、アーカイブの実行履歴から確認された独立性は同一ではない。ただし証拠なしに時間自己相関が存在すると断定し、そのために固定観察を無効とすることも不適切である。現在の記述的claimのためにbootstrapや新たな統計検定を追加する必要はない。

## 7. Historical Assessment Comparison

Package 03を開く前の暫定判定はA2。比較後も中核結論は変わらない。以下は差分と、既に解決・説明されていた点である。

| 論点 | 旧記録（2026-10-18～19） | 今回の更新 |
|---|---|---|
| 元座標検証範囲 | 10系2,700 framesの標的検証、残り144系未検証 | L2に154系のローカル実行記録が追加。本Workが154元座標を再計算したわけではない |
| 153＋1 lineage | 全履歴・元ログに不足 | 元出力・回復出力・差分コードから統合値の連続性を直接確認。コンソール全履歴は依然未回収 |
| FNC defaults | 既に注意、元Coreは正しいと記載 | 今回も独立AST・呼出し確認で同じ結論。新たなバグ発見とは扱わない |
| boundaryの上下限誤解 | 旧最終Gateに「二つの一括規則であり数学的上限ではない」と記載 | 今回は29/112の具体的非挟み込みを検算。旧評価にない訂正を強いて作らない |
| under70分母 | targetを分母とすべきと訂正要求 | 現公開Note/SIは既にtargetと明示。未修正扱いしない |
| 一般化・真の平衡 | 旧報告で非支持 | 現公開Note・Zenodoも限定済み。科学的留保を維持 |
| Masterの状態 | 旧記録にはv1.3の承認状態の記述あり | 今回のauthorityは承認済みPost-Research Protocol。v1.6を承認済みに変更しない |

旧判定A2との一致、旧MSC Supported、公開推奨は科学的証拠に加算していない。旧報告のPhase B/C/D部分を追認・更新していない。過去の10系座標結果は本報告では[H]であり、過去の[V]ラベルをそのまま引き継いでいない。

## 8. Mandatory Corrections vs Optional Improvements

### 8.1 必須の記述訂正・限定

| 重要度・項目 | 箇所→一次証拠→原因 | 影響claim／最小対応／判定への影響 |
|---|---|---|
| 高：L2独立性の範囲 | L2 `run_system` が公式filter/FNCを動的importして再使用 | 完全独立認証C11を否定。ω・CA/CNの別式検算とFNC/clash再実行を分けて記載。中核値の再計算は不要 |
| 高：L2 fingerprintの保証 | `main` のmanifestに実import snapshot・pair CSV・全依存版なし | 「全入力・code fingerprint」の文字通りの保証は不可。今回の結果に未連結部分があると明記。既存の実行版を後から推測して埋めない |
| 中：aggregate PASS | pair検査が条件付き、all_passはpair件数を条件としない | 今回は112実在・照合済み。all_pass単独の認証を避ける。将来再利用する時だけpair件数・ID・依存hashを条件へ加える |
| 中：境界集計名称 | L2はA全体302、PrimaryはB0の292 | 分母を併記して誤解を除く。元出力値を誤値として削除しない |
| 中：境界対照の解釈 | Primaryと二つのシナリオ値は一般に順序を持たない | 数値上下限・信頼区間と呼ばない。現公開文書・旧Gateの正しい限定を維持 |
| 中：歴史的固定と再現方法 | X2引継ぎには最終固定待ち文言、独立承認原本なし | 「使用規則はコードから復元」「事前承認時点は未証明」と記載。最終Protocolを遡って創作しない |
| 中：短いMethodsの精度 | 現Noteはappropriate planar reference、fixed sigmoid等の略記 | 再設計を行う場合は本報告§4の式・比較演算・snapshot識別を明示する。方法の再定義や新閾値導入ではない |

これらの必要条件は本報告で明示した。**公開物は変更していない。** 特に、既に正しい限定がある箇所を再度「未訂正」としてGateを増やす必要はない。

### 8.2 任意改善／今回実施しないこと

完全なlockfileの整備、validatorの汎用edge-case test追加、独立clash/FNC全実装、cluster-aware不確実性評価、同数ランダム除外対照は、将来の利用目的が要求するなら検討可能。しかし固定アーカイブ感度の成立を確認する本Phase 1Aの必須追加研究ではない。

公開Note末尾にはrepository URL/DOIがpendingという旧文言が残るが、README・Zenodoには実リンクがある。これは版・文書管理上の問題で、主要科学結論の反証ではない。今回の公開改訂作業には含めない。

## 9. Unresolved Evidence and Minimum Remedy

| 未確認事項 | 科学的影響 | 最小対応／今必要か |
|---|---|---|
| 最終承認済みMinimum Protocol原本・承認時刻 | 結果閲覧前に正式固定したとのclaimはA3 | 存在すれば当時の該当メッセージ・原本のみ。無ければ未回収と明記。中核記述のために再構成を承認済み原本へ昇格しない |
| 元Primaryの完全環境 | 原著数値の厳密再現・全版互換を認証できない | 元pip freeze等が存在すれば保存。現L2環境を歴史的環境へ置換しない |
| L2実行時のimport snapshot連結 | fingerprintによる完全な改変検出は未証明 | 手元に実行時snapshotと当時hashがあれば照合。新しく測ったhashは「現在のhash」と明示。全座標再計算を自動要求しない |
| XTC生成オプション・seed/batch・保存前filter履歴 | Aを未選別生成母集団と呼べない | 当時の生成command/logがあれば限定回収。現在のRQではA=保存全frameで十分 |
| 真の平衡分布・一般的性能・母集団不確実性 | C15は支持されない | 別の科学的設計が必要。今回の不足を埋めるために新研究を開始しない |
| 座標圧縮前後の厳密な誤差伝播 | 閾値件数の全精度頑健性は未証明 | 固定保存座標へのclaimに限定。必要なら将来、該当boundary frameだけを扱うが今回は不要 |

**現有証拠に、結論を左右する特定systemの元座標取り違え・mask不一致・参照不一致は見つからなかった。そのため、追加XTC/PDB取得を要求しない。** 1.96 GBのアップロード、全154系の重複再計算、追加Workを必要条件にしない。

## 10. 出典・監査ファイルへの追跡

### 10.1 添付内の主な証拠位置

以下の「P01/P02/P03」はPackage番号である。自動連番は版番号ではない。

| 証拠ID | 正式ファイル／関数・列 |
|---|---|
| E1 | P01 `NTBE_Session3_v1(2).zip` 内 `ntbe_session3.py`：`dg_stats`、reference探索、FNC明示引数、pair生成 |
| E2 | P01 `ntbe_session3_reference_fix(5).py`：元Coreとの差分2行 |
| E3 | P01 `official_fnc_snapshot.py`／`ntbe_official_filter_snapshot.py`（E1 ZIP内） |
| E4 | P01 `NTBE_Session3_output_new.zip`、`NTBE_Session3_recovery.zip` 内 `systems.csv`／`pairs.csv`／`fnc/*.npz` |
| E5 | P01 `NTBE_systems_154_reconciled(5).csv`、`NTBE_pairs_112_reconciled(5).csv` |
| E6 | P01 `NTBE_X2_Omega_Primary_v1(3).zip` 内 `ntbe_x2_primary.py:calc_system/make_pairs`、`ntbe_x2_omega_pilot.py:four_point_degrees/classify_omega` |
| E7 | P01 `NTBE_X2_Omega_Primary_output.zip` 内 `systems_omega.csv`／`pairs_omega.csv`／`omega_masks/*.npz`。重複 `all_npz(1).zip` の154メンバーはbyte一致 |
| E8 | P01 公式benchmark ZIP：`bioemu_benchmarks/utils.py`、`eval/folding_free_energies/{fraction_native_contacts,free_energies,evaluate,utils}.py`、assets内system_infoとreference |
| E9 | P02 `ntbe_l2_verify_L2_v1_0_1.py`：`run_system`（70行以降）、near集計（132行）、manifest（150行付近）、aggregate（155–174行）、動的import（177–178行） |
| E10 | P02 `NTBE_L2_output.zip`：154 `systems/*.json`、`L2_aggregate.json`、`L2_pairs.json`。独立照合JSONとL1_reportは証拠範囲を区別 |
| E11 | P03 `NTBE_X2_Final_Publication_Gate_2026-10-19_JA(2).md` §II-2/II-3、`NTBE_Dual_Mission_Assessment_2026-10-18_JA(3).md` §A1。旧評価との比較用 |

検算コード `Phase1A_Verification.py` はPackage 01・02を展開したevidenceディレクトリに対して実行する。元研究コードを呼んでΔGを出力する方法ではなく、保存配列に対する別算式・AST照合・table照合を使う。検算の出力 `Phase1A_Verification_Results.json` に主要値、system別値、境界frame、hash、未実行範囲を記録した。公式元XTCは不要。

### 10.2 外部一次資料と実取得状況

確認日はいずれも2026-10-26。URLの存在確認と内容読解を分けた。

| 出典 | 実取得・読解した範囲 |
|---|---|
| [BioEmu supplementary data, Zenodo 15672282](https://zenodo.org/records/15672282) | record本文、公開MD5、samples_delta_GとFig.4 B/C/Fの対応。コードZIPは添付bytesとMD5一致。元1.96 GBの全bytesは未取得 |
| [Lewis et al., Science 2025, DOI](https://doi.org/10.1126/science.adv9817)／[著者版＋SI](https://www.microsoft.com/en-us/research/wp-content/uploads/2024/12/accepted_paper.pdf) | PDF 31,205,701 bytesを実取得。Model architecture、S17–20のFNC/soft foldedness、S24–25のgeometry、S28のfree-energy evaluationを読解。Web parserはサイズ制限だったが通常HTTP取得に成功。出版社版との全行差分は未実施 |
| [MolProbity原著本文](https://pmc.ncbi.nlm.nih.gov/articles/PMC5734394/) | cis-nonProline/twisted peptide節とFig.9関連本文。>30°、次残基への帰属を確認 |
| [公式benchmark GitHub](https://github.com/microsoft/bioemu-benchmarks) | 現行READMEの依存版による数値非互換性警告を確認。固定解析の仕様は添付snapshotで判断 |
| [公式BioEmu GitHub](https://github.com/microsoft/bioemu) | 現行READMEを確認。生成filterの具体的監査は添付publication snapshotを使用。現行版を過去の実行版へ混ぜていない |
| [公開研究GitHub](https://github.com/shomiyazaki-ai/bioemu-filter-sensitivity-ntbe-x2-omega) | README、Technical_Note.pdf、Supplementary_Information.pdfをGitHub接続経由で実取得・本文抽出。科学的正しさの独立根拠ではない |
| [公開研究Zenodo 23615869](https://zenodo.org/records/23615869) | APIで説明本文と3添付のmetadata取得。GitHub取得PDFのMD5がZenodo掲載MD5と一致。Supporting_Data_and_Code全ZIPは新たに取得していない |

著者版BioEmu PDFのSHA-256は `b04d35cf6ee40f7582aa67d8253b5a39087318af36a333d46603f9709eed6da7`。公開NoteのMD5は `7c8819a6cfaf33cdca0454c47fdf1359`、SIは `5d9b2c6b080fc53f06179a95170cbc24`。URLの取得失敗を資料欠落と早合点せず、上記の成功経路を区別した。

## 11. Final Phase 1A Judgment and STOP

**NT-BE／X2-ωは、保存済み154系・112対応ペアに対する、公式geometry選別と固定ω選別の記述的感度として科学的に成立する。総合A2、個別の中核数値・集合関係はA1相当。**

今回の監査で主解析値の変更は必要と判断しない。L2の検証範囲、事前固定の証拠、境界シナリオの意味を本報告の範囲へ限定する必要がある。真の熱力学補正、一般的予測性能向上、全原子physical validity、完全な歴史的再現認証は成立していない。

本人が次のChatで決める事項は、この成立範囲を維持して方法・検証の説明を整理するか、別の科学的問いを持つ再設計が必要かである。本報告は後者を要求せず、公開媒体や新規性の採否も決めない。

**Phase 1Aは完了。ここでSTOPする。** GitHub／Zenodo、公開Technical Note／SI／READMEは変更していない。Phase B/C/D、新しい閾値・系・条件の解析、追加Work起動は実施していない。
