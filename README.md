# Gridskyline
#### 期刊衝起來，程式肝起來

## 0803開會重點：
* edge端傳至server端的資料筆數
  * 上傳有變化的部分
* Esk1,Esk2是什麼
  * communication load
* R-tree的參考
  * 找到就不用開發Grid-index
* Grid-index 持續努力
  * pruning的方法尚在研擬

* Compared Methods:
  1. Edge-assisted Parallel Uncertain Skyline (EPUS).
  2. Parallel R-tree Pruning Only (PRPO).
  3. Parallel Grid-index Pruning Only (PRGO).
  4. Parallel Brute-Force (PBF).

  - Performance metrixs:
  1. Average Latency (Computation Time).
  2. Average Transmission Cost.
  3. Average Sizes of ESK_{k,1} and ESK_{k,2}

  - Results From the System Architecture Perspective:
  1. Number of Edge Computing Nodes.
  2. Size of sliding window.

  - Results From the System Architecture Perspective:
  1. Size of Data Set.
  2. Data Dimensionality.
  3. Number of Instances.
  4. Radius of data object.

## 0727(暫停一次)文字提示：
* edge實驗中 window size的比較(100,300,500,700)
  * 結點數量不同的情況下，在edge的window-size以及server的window-size進行改變
  * 兩邊的windowsize同時成為變因，在每一種節點(1,2,4,6,8,10,12,14,16)的情況下可以得出下表，共9張
  * 紀錄時間為edge max、server兩個時間相加

|edge\server| 100 | 300 | 500 | 700 |
|:---------:|:---:|:---:|:---:|:---:|
|100        |     |     |     |     |
|300        |     |     |     |     |
|500        |     |     |     |     |
|700        |     |     |     |     |

* 持續跑5W以及10W的資料

-----
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
