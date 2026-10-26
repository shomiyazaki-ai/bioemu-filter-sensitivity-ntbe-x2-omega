NT-BE / X2-omega Session L1 2026-10-26
=====================================
目的：公式samples_delta_G.zipと154対象系の入力・参照対応を検証する。科学計算の再解析はまだ行わない。

【準備】
1) C:\Users\user\NTBE\ にこのキットの ntbe_l1_verify.py を置く。
2) 同じフォルダに samples_delta_G.zip (1,959,113,732 bytes) があることを確認。
3) bioemu-benchmarks_code_release.zip も同じフォルダに置く。
   既存名が bioemu-benchmarks_code_release(8).zip の場合はファイル名を変更せず、実行時 --benchmark で指定してもよい。
4) 任意で all_npz(1).zip、NTBE_Session3_output_new.zip、NTBE_Session3_recovery.zip、NTBE_systems_154_reconciled(5).csv を同じフォルダに置く。
   これらはなくても、L1の元ZIP・公式参照・座標QAは実施できる。

【PowerShell 推奨コマンド】
cd C:\Users\user\NTBE
py -3 .\ntbe_l1_verify.py --root 'C:\Users\user\NTBE' --benchmark 'C:\Users\user\NTBE\bioemu-benchmarks_code_release(8).zip' --systems 'C:\Users\user\NTBE\NTBE_systems_154_reconciled(5).csv' --coordinate-qa

※オプション --systems のファイルが手元になければ、その引数丸ごと削除してOK。
※--benchmarkのファイル名は実在名に合わせる。
※--coordinate-qaはMDTrajおよびNumPyがインストールされている場合に動作。
  py -3 -c "import mdtraj,numpy; print('mdtraj OK')" で確認。
  未導入時に勝手なpip installはせず、まずメッセージを確認する。

【L1必須チェック】
・1.96 GBのZIP全体を読み、公式MD5およびこのチャットで確認したSHA-256に一致すること
・公式154系/112mutant/42WTのmetadata、参照PDB154本の一意性
・154系のsamples.xtc / topology.pdbのZIP内存在、非空、一意性（対象外系は別記）
・1EM7_L7Aと1TG0__D45C_N47Pの元XTC/PDBのSHA-256
・任意--coordinate-qaなら、この2系のXTC読込、原子/配列/chain数とreference/metadata一致
・保存NPZ/結果CSVを渡した場合、その存在・ID・CRCとハッシュ（中身の科学的検算はL2）

【出力（必ずアップロードするファイル）】
 C:\Users\user\NTBE\NTBE_L1_output\L1_report.json
 C:\Users\user\NTBE\NTBE_L1_output\inventory_154.csv
 C:\Users\user\NTBE\NTBE_L1_output\L1_manifest_sha256.txt
 ※XTC/PDBの実体はアップロード不要。上記3つだけでよい。
 エラーの場合はPowerShellに表示されたエラー文もコピーして提示。

【重要な注意】
・スクリプトは元ZIPおよび入力資料を読み取り専用で開く。出力フォルダ内は上書きあり。
・1A0N_L7Sは今回の154系のmetadataに含まれないため、対象外として表示する。
・XTC中の原子座標の全frame有限性や幾何学的正しさ、FNC/omegaの再計算はL1では行わない。
・ZIP全体のSHA256/MD5を毎回計算するため、大きいファイルの読み取り時間が発生する。
・L1でのPASSは入出力の取り違え・欠損を否定する範囲に限定される。
