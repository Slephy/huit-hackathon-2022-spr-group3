#備忘録

- 複数個応答メッセージを返したいときには、reply_messageの引数で渡すmessageにSendTextMessageクラスのタプルや配列を指定する。単に複数回reply_messageを呼び出しても最初の1回しか処理してくれない

- Yahoo乗換案内を使用

- soup.select()でCSSセレクタによる指定が可能

- 地下鉄利用時に漢字表記の"札幌"によって直通できないと誤判断された場合に、"さっぽろ"表記で自身の関数を再度呼び出して対応


## 経由地がある状況においてのCSSセレクタによる時刻取得
電車->電車の場合
乗車時刻->降車時刻(乗り換え)->乗車時刻(乗り換え)->降車時刻
```
#route01 > div > div:nth-child(1) > ul.time > li
#route01 > div > div.fareSection > div.station > ul > li:nth-child(1)
#route01 > div > div:nth-child(3) > ul.time > li
```
電車->徒歩の場合
乗車時刻->降車時刻->徒歩出発時刻->徒歩到着時刻 の場合
```
#route01 > div > div:nth-child(1) > ul.time > li
#route01 > div > div:nth-child(3) > ul > li:nth-child(1)
#route01 > div > div:nth-child(3) > ul > li:nth-child(2)
#route01 > div > div:nth-child(3) > ul.time > li
```
