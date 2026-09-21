# くらしの計算箱（kurashi-calc）

**公開サイト：https://kabosuburi5555-commits.github.io/kurashi-calc/**

暮らし・趣味のミニ計算ツール集（登録不要・無料・入力内容はブラウザ内でのみ計算）。静的サイト（HTML/CSS/JS のみ、サーバー不要）。

## 公開中のツール（12 本）
- 料理・キッチン：[炊飯の水加減計算](https://kabosuburi5555-commits.github.io/kurashi-calc/rice-water/)／[調味料の分量換算](https://kabosuburi5555-commits.github.io/kurashi-calc/seasoning-convert/)／[解凍時間の目安](https://kabosuburi5555-commits.github.io/kurashi-calc/thaw-time/)
- DIY・住まい：[壁紙・ペンキ必要量計算](https://kabosuburi5555-commits.github.io/kurashi-calc/wallpaper-paint/)／[引越しダンボール枚数](https://kabosuburi5555-commits.github.io/kurashi-calc/moving-boxes/)
- 趣味・スポーツ：[新ペリア計算](https://kabosuburi5555-commits.github.io/kurashi-calc/golf-peria/)／[コンペ順位表メーカー](https://kabosuburi5555-commits.github.io/kurashi-calc/golf-compe-ranking/)／[賞品予算シミュレーター](https://kabosuburi5555-commits.github.io/kurashi-calc/golf-prize-budget/)／[コンペ会計・精算計算](https://kabosuburi5555-commits.github.io/kurashi-calc/golf-compe-accounting/)
- ペット・動物：[犬・猫の年齢換算](https://kabosuburi5555-commits.github.io/kurashi-calc/pet-age/)
- 日付・時間：[日数計算・あと何日](https://kabosuburi5555-commits.github.io/kurashi-calc/date-count/)／[生後日数・お祝い日](https://kabosuburi5555-commits.github.io/kurashi-calc/baby-days/)

関連：[ゴルフコンペ幹事おまかせセット（Excel）](https://kabosuburi5555-commits.github.io/kurashi-calc/golf-kanji-set/)

## 構成
- `tools/<slug>.html` … ツール1本＝1ファイル（先頭の `<!--meta {...} -->` にタイトル・説明・FAQ）
- `pages/` … about / privacy / contact
- `site.json` … サイト名・公開URL（`base_url` を自分の GitHub Pages の URL に変更する）
- `build.py` … `python3 build.py` で `dist/` に生成（index・sitemap.xml・robots.txt も自動）
- `.github/workflows/pages.yml` … main に push すると自動でビルドして GitHub Pages に公開

## 初回の公開手順（GitHub）
1. このフォルダの中身をリポジトリ（例: `kurashi-calc`）に push（main ブランチ）
2. リポジトリの Settings → Pages → Build and deployment → Source を **GitHub Actions** にする
3. `site.json` の `base_url` を `https://<ユーザー名>.github.io/kurashi-calc` に書き換えて push
4. Actions が緑になれば `https://<ユーザー名>.github.io/kurashi-calc/` で公開

## ツールを増やす
`tools/` に新しい HTML を追加して push するだけ。カテゴリが同じツールは自動で「関連ツール」に相互リンクされる。
