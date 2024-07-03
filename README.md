# How to Use

`.env`ファイルを作成し，Azure OpenAI Service の API キーやデプロイ情報を記述する．書き方は`.env.sample`参照．

### Step. 1

`main.py`を実行すると，まずスクリーンショットの撮影が開始される．
取りたい範囲の左上を右クリック、次に右下を右クリックすることで指定範囲のスクリーンショットが自動で撮影される．撮影されたスクリーンショットは，`tmp/`以下に保存される．

### Step. 2

次にプロンプトの入力フェーズとなる．プロンプトの入力を完了すると，`Step. 1`の画像と共に ChatGPT の API へ送信される．

### Step. 3

API からレスポンスが返される．`Step. 1`へ戻る．

# Author

Copyright © 2024 Broccolingual. All rights reserved.
