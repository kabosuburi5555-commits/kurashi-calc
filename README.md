# くらしの計算箱（kurashi-calc）

暮らし・趣味のミニ計算ツール集。静的サイト（HTML/CSS/JS のみ、サーバー不要）。

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
