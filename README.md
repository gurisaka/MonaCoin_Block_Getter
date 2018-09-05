# MonaCoin Block Getter  
### Useage
* `python3 main.py`
MONA_Blocksフォルダに保存されているブロックデータをひとつのjsonファイルにまとめる。また、トランザクションのみをまとめたjsonファイルも作成する。  作成されたファイルはOutputsフォルダに保存される。
  
* `python3 main.py [start_block_height] [dig_block_height]`
start_block_heightで何ブロックから取得を始めるか設定する。dig_block_heightで何ブロック取得するかを決める。
例えば、
`python3 main.py 1000 10`
と入力すれば1000ブロック目〜991ブロック目の取得を行う。

### Requirements
 * requests

### Warning
MONA_Blocksには既に1410501〜1430308ブロックが保存されています。

### Author
#####  https://twitter.com/GuriTech.com
