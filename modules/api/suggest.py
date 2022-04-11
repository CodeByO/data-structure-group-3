from multiprocessing.pool import ThreadPool
from api import getData
import time



#[Function] 자료구조를 이용한 추천 기능
#[DESC] 힙을 이용하여 월세 또는 전세의 최저값인 데이터 리턴
#[TODO] routes/suggests로 호출될시 suggestMontly에 월세 전세 힙정렬 에러 수정

class heap:

    def __init__(self):
        self.input = 0
        self.endPoint = 0
        self.heap = [[0]*5 for _ in range(10001)]
        

    def insertHeap(self, input,index):
        self.endPoint += 1

        cur = self.endPoint

        while cur > 0:

            if int(self.heap[cur // 2][index]) > int(input[index]):

                self.heap[cur] = self.heap[cur // 2]
                cur = cur // 2
            else:
                break
        self.heap[cur] = input
        
    def popHeap(self,index):

        if self.endPoint == 0:
            return None
        root = 1
        value = self.heap[self.endPoint]

        self.heap[self.endPoint] = 0
        self.endPoint -= 1

        if self.endPoint == 0:
            return None
        
        while root * 2 + 1 < 10001 and value > self.heap[root*2] or value > self.heap[root* 2 + 1]:
            if self.heap[root * 2][index] > self.heap[root * 2 + 1][index]:
                self.heap[root] = self.heap[root * 2 + 1]
                root = root * 2 + 1
            else:
                self.heap[root] = self.heap[root*2]
                root = root * 2
        

        self.heap[root] = value

    def minHeap(self,list,index):
        for n in list:
            if(n[index] == '0'):
                self.popHeap(index)
            else:
                self.insertHeap(n,index)

        for i in self.heap:
            if i[index] != 0:
                return i

# class heapPython:
#     def heapPush(tree,value):
#         tree.append(value)

#         node = len(tree) - 1

#         lastIdx = node

#         while node > 1:

#             node //= 2

#             if tree[node] > value:
#                 tree[lastIdx] = tree[node]
#                 lastIdx = node
#             else:
#                 break

#         tree[lastIdx] = value

#         return

#     def getPriority(tree,node):
#         if len(tree) -1 > node*2 + 1:
#             if tree[node*2] > tree[node*2+1]:
#                 return node*2+1

#             else:
#                 return node * 2

#         elif len(tree) -1 == node * 2:
#             return node * 2

#         else:
#             return -1           


class suggest():
    def __init__(self):
        self.start = time.time()
        data = getData.getData()
        self.monthly, self.charter = data.devideRoom('202203')

    def suggestMonthly(self):
        monthlyHeap = heap()
        charterHeap = heap()
        monthly = monthlyHeap.minHeap(self.monthly,3)
        charter = charterHeap.minHeap(self.monthly,4)
        end = time.time() - self.start
        return monthly, charter, end

    def suggestCharter(self):
        minHeap = heap()
        # poolCharter = ThreadPool(processes=3)
        # asyncCharter = poolCharter.apply_async(minHeap.minHeap,(self.charter,4))
        # charter = asyncCharter.get()
        charter = minHeap.minHeap(self.charter,4)
        end = time.time() - self.start
        return charter, round(end, 3)

# if __name__ == '__main__':
#     sug = suggest()
#     monthlyList,mCharterList,monthlyTime = sug.suggestMonthly()
#     print(monthlyList)
#     print(mCharterList)

#     charterList,charterTime = sug.suggestCharter()
#     print(charterList)