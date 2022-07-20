# Gridskyline
#### 期刊衝起來，程式肝起來

## 0720開會重點：
* edge實驗下 window size的比較(100,500,700)
  * 不同節點數量不同sliding window
* 維持相同的實驗設置(5萬筆跟10萬筆)
  * 來看資料筆數變多，對於節點數會不會有幫助
* inverted table & grid 開發
  * 各種開發，加油。


----

## 0713開會重點：
* 討論多edge的延遲為何提高
  * 大家輪流送資料進去(test_node164-172要改，迴圈要反過來)
  * 顯示edge拿到的資料數量
  * 擷取的時間(recieve&updata這兩個然後去做累加--> server, edge max--> edge)
* 將r-tree進行抽離
  * 找一個點當作代表代表然後製作inverted-index


----
## 0629開會重點：
* 1.了解r-tree在演算法中扮演的角色
* 2.在indexing的時候要注意到 inverted-index，也就是能夠雙向查找
* 3.整理實驗數據
* 4.不用照著論文開發喇


---
