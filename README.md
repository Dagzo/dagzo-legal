# dagzo-legal

公開しているアプリのプライバシーポリシーと利用規約を、**アプリストアから参照できるURLとして置いておく**ためのリポジトリ。GitHub Pages で配信する。

Google Play は「ネット上で誰でも見られるプライバシーポリシーのURL」を要求する。アプリ本体のリポジトリを公開したくないので、規約類だけを分けてここに置いている。

## 本文の正本はここではない

**HTML は生成物。文章を直すときは元の Markdown を直す。**

| 公開ページ | 正本 |
| --- | --- |
| `timephoto/privacy-ja.html` | `../time-photo/docs/privacy-policy-ja.md` |
| `timephoto/privacy-en.html` | `../time-photo/docs/privacy-policy-en.md` |
| `timephoto/terms-ja.html` | `../time-photo/docs/terms-of-service-ja.md` |

md を直したら、変換し直してコミットする。

```bash
cd projects/dagzo-legal
python3 build.py
```

`build.py` は同じ階層にある各アプリのリポジトリを相対パスで読む（`../time-photo/...`）。
**ワークスペースの外に置くと動かない。**アプリを増やすときは `build.py` の `PAGES` に行を足す。

## 構成

```
index.html            アプリ一覧。ここから各規約へ
style.css             読みやすさだけを狙った共通スタイル
build.py              md → HTML
timephoto/
  privacy-ja.html
  privacy-en.html
  terms-ja.html
```

## 公開のしかた

GitHub の Settings → Pages で、Source を `main` ブランチのルートにする。数分で次のURLで見えるようになる。

```
https://dagzo.github.io/dagzo-legal/
https://dagzo.github.io/dagzo-legal/timephoto/privacy-ja.html
```

**このURLを Play Console の「プライバシーポリシー」に入れる。**

## 注意

- このリポジトリは**公開**である必要がある（private だと Pages が有料プランになる）。逆に言えば、**ここには公開してよいものしか置かない**
- 規約の日付（「最終更新日」）は md 側にある。内容を変えたら日付も直す
- 公開後にURLを変えると、ストアの審査で参照切れになる。**ディレクトリ名とファイル名は変えない**
