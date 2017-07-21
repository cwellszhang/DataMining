# coding=utf-8

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue    # 节点元素名称，在构造时初始化为给定值
        self.count = numOccur    # 出现次数，在构造时初始化为给定值
        self.nodeLink = None     # 指向下一个相似节点的指针，默认为None
        self.parent = parentNode # 指向父节点的指针，在构造时初始化为给定值
        self.children = {}       # 指向子节点的字典，以子节点的元素名称为键，指向子节点的指针为值，初始化为空字典

    def inc(self, numOccur):     #增加节点的出现次数值
        self.count += numOccur

    def disp(self, ind=1):       #输出节点和子节点的FP树结构
        print (' ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

def createTree(dataSet, minSup=1):
    ''' 创建FP树 '''
    # 第一次遍历数据集，创建头指针表
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 移除不满足最小支持度的元素项
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del(headerTable[k])
    # 空元素集，返回空
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    # 增加一个数据项，用于存放指向相似元素项指针
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None) # 根节点
    # 第二次遍历数据集，创建FP树
    for tranSet, count in dataSet.items():
        localD = {} # 对一个项集tranSet，记录其中每个元素项的全局频率，用于排序
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0] # 注意这个[0]，因为之前加过一个数据项
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)] # 排序
            updateTree(orderedItems, retTree, headerTable, count) # 更新FP树
    return retTree, headerTable