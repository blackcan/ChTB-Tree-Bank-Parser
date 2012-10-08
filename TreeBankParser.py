#-*-coding:utf-8-*-

#ChTB Tree Bank Parser by blackcan

import os, StringIO

class TreeBankParser:
    tree = {} #存放解析完的結果

    #初始化Parser，並將傳入文字解析
    def __init__(self, doc):
        self.tree = {}
        linesList = doc.strip().replace('((', '( (').split('\n')
        sentenceNum = -1
        nowSID = ''
        contentNum = 0
        POSStack = []
        contentStack = []
        layerNum = 0
        for line in linesList:
            if line.find('<S ID') == 0:
                nowSID = line[line.find('=') + 1:line.find('>')]
            elif line[0] != '<':
                lineContents = line.strip().split()
                for content in lineContents:
                    if content.find('(') > -1:
                        if len(content) == 1:
                            sentenceNum += 1
                            contentNum = 0
                            contentStack = []
                            layerNum = 0
                            self.tree[sentenceNum] = {}
                            contentStack.append('(S')
                        else:
                            contentStack.append(content)
                            layerNum += 1
                    elif content.find(')') > -1:
                        while content.find(')') > -1:
                            if content.find(')') != 0:
                                outputPosTag = contentStack.pop(-1)[1:]
                                outputContent = content[:content.find(')')]
                                content = content[content.find(')') + 1:]
                                self.tree[sentenceNum][contentNum] = [nowSID, layerNum, outputPosTag, outputContent]
                                contentStack.append(contentNum)
                            else:
                                outputContent = []
                                findPOS = False
                                while(not findPOS):
                                    popContent = contentStack.pop(-1)
                                    if type(popContent) == int:
                                        outputContent.append(popContent)
                                    else:
                                        outputPosTag = popContent[1:]
                                        self.tree[sentenceNum][contentNum] = [nowSID, layerNum, outputPosTag, outputContent]
                                        contentStack.append(contentNum)
                                        findPOS = True
                                content = content[content.find(')') + 1:]

                            layerNum -= 1
                            contentNum += 1

    #將tree中的結果輸出成{SentenceNum, ContentNum, SID, Layer, Semantic Tag, Content}形式的字串 
    def toString(self, sid = -1, cid = -1):
        output = StringIO.StringIO()
        if sid == -1:
            for i in sorted(self.tree.keys()):
                for j in sorted(self.tree[i].keys()):
                    if type(self.tree[i][j][3]) == list:
                        output.write('{' + str(i) + ',' + str(j) + ',' + self.tree[i][j][0] + ',' + str(self.tree[i][j][1]) + ',' + self.tree[i][j][2] + ',' + str(self.tree[i][j][3]) + '}\n')
                    else:
                        output.write('{' + str(i) + ',' + str(j) + ',' + self.tree[i][j][0] + ',' + str(self.tree[i][j][1]) + ',' + self.tree[i][j][2] + ',' + self.tree[i][j][3] + '}\n')
                output.write('\n')
        else:
            if cid == -1:
                for i in sorted(self.tree[sid].keys()):
                    if type(self.tree[sid][i][3]) == list:
                        output.write('{' + str(sid) + ',' + str(i) + ',' + self.tree[sid][j][0] + ','  + str(self.tree[sid][i][1]) + ',' + self.tree[sid][i][2] + ',' + str(self.tree[sid][i][3]) + '}\n')
                    else:
                        output.write('{' + str(sid) + ',' + str(i) + ',' + self.tree[sid][j][0] + ','  + str(self.tree[sid][i][1]) + ',' + self.tree[sid][i][2] + ',' + self.tree[sid][i][3] + '}\n')

            else:
                if type(self.tree[sid][cid][3]) == list:
                    output.write('{' + str(sid) + ',' + str(cid) + ',' + self.tree[sid][cid][0] + ','  + str(self.tree[sid][cid][1]) + ',' + self.tree[sid][cid][2] + ',' + str(self.tree[sid][cid][3]) + '}')
                else:
                    output.write('{' + str(sid) + ',' + str(cid) + ',' + self.tree[sid][cid][0] + ','  + str(self.tree[sid][cid][1]) + ',' + self.tree[sid][cid][2] + ',' + self.tree[sid][cid][3] + '}')

        return output.getvalue().strip()

#執行測試區
fileList = []
def VisitFiles(fileList, dirName, files):
    for file in files:
        if os.path.splitext(file)[-1] == '.fid':
            fileList.append(file)
os.path.walk('./Data/', VisitFiles, fileList)

for file in fileList:
    readDoc = open('./Data/' + file, 'r')
    try:
        parseTree = TreeBankParser(readDoc.read().decode('utf-8', 'ignore'))
        readDoc.close()
        writeResult = open('./Result/' + file[:-3] + 'txt', 'w')
        writeResult.write(parseTree.toString().encode('utf-8'))
        writeResult.close()
        print file 
    except:
        print file + 'error!'
#readDoc = open('./Data/chtb_0004.fid', 'r')
#parserTree = TreeBankParser(readDoc.read().decode('utf-8', 'ignore'))
#print parserTree.toString(32).encode('utf-8')
                
