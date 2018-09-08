# MonaCoin Block Getter  
### Useage
* `python3 main.py`
MONA_Blocksフォルダに保存されているブロックデータをひとつのjsonファイルにまとめる。また、トランザクションのみをまとめたjsonファイルも作成する。  作成されたファイルはOutputsフォルダに保存される。
  
* `python3 main.py [tail_block_height] [head_block_height]`  
tail_block_heightで何ブロックから取得を始めるか設定する。head_block_heightで何ブロックまで取得するかを決める。
例えば、
`python3 main.py 1000 1010`  
と入力すれば1000ブロック目〜1010ブロック目の取得を行う。  

* `python3 main.py [tail_block_height]`  
tail_block_heightから現在の最高ブロックまでを取得し、ブロックデータ、トランザクションデータをまとめたjsonファイルを作成する。作成されたファイルはOutputsフォルダに保存される。また、処理は致命的なエラーが発生しない限り10秒間隔で何回も繰り返される。

### Requirements
 * requests

### Warning
MONA_Blocksには既に1410501〜1430308ブロックが保存されています。

### Author
#####  https://twitter.com/GuriTech.com
