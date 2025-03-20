# 簡化字轉漢字

* 支持《通用規範漢字表》中的全部簡化字
* 對於一對多的簡化字，人工標註規則
* 支持運行時增加自定義規則
* 簡單快速

[pypi](https://pypi.org/project/pyhan/)

[pages](https://github.com/lizongying/hanzi)

附：[《通用規範漢字表》](./files/)

## 安裝

```
pip install pyhan
```

## 示例

```
from pyhan import to_traditional,add_rule

if __name__ == '__main__':
    # 簡化字轉漢字
    res = to_traditional('萝卜去哪了，可以在茶几卜上几卦')
    # output: 蘿蔔去哪了，可以在茶几卜上幾卦
    print(res)
    
    # 運行時增加自定義規則
    add_rule('卜,蔔,-1|0|胡')
    res = to_traditional('胡卜')
    # output: 胡蔔
    print(res)
```

## 完善

如果你需要增加规则，可以编辑 [st02.csv](./src/pyhan/files/st02.csv) 文件, 例如：

```csv
卜,蔔,-1|0|萝
卜,卜
```

會匹配第三列及以後，這裡是`-1|0|萝`，`-1`代表索引開始，`0`代表索引結束，`萝`代表匹配的目標詞，如果匹配成功，返回第二列

如果沒有第三列，返回第二列

### 測試

```
make test
```

## 貢獻

你可以按照以下步驟貢獻代碼：

1. Fork 本倉庫。
2. 提交 pull request。