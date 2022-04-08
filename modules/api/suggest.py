from multiprocessing.pool import ThreadPool
from api import getData
import time



#[Function] 자료구조를 이용한 추천 기능
#[DESC] 힙을 이용하여 월세 또는 전세의 최저값인 데이터 리턴
#[TODO] routes/suggests로 호출될시 suggestMontly에 월세 전세 힙정렬 에러 수정

class suggest:
    def __init__(self):
        self.start = time.time()
        data = getData.getData()
        self.monthly, self.charter = data.devideRoom('202201')
        self.input = 0
        self.endPoint = 0
        self.heap = [[0]*5 for _ in range(1000001)]
        
    
    def suggestMonthly(self):
        poolMonthly = ThreadPool(processes=1)
        poolCharter = ThreadPool(processes=2)
        asyncMonthly = poolMonthly.apply_async(self.minHeap,(self.monthly,3))
        asyncCharter = poolCharter.apply_async(self.minHeap,(self.monthly,4))
        monthly = asyncMonthly.get()
        charter = asyncCharter.get()
        end = time.time() - self.start
        return monthly, charter, end

    def suggestCharter(self):
        poolCharter = ThreadPool(processes=3)
        asyncCharter = poolCharter.apply_async(self.minHeap,(self.charter,4))
        charter = asyncCharter.get()
        end = time.time() - self.start
        return charter, round(end, 3)

    def insertHeap(self, input,index):
        self.endPoint += 1

        cur = self.endPoint

        while cur > 0:

            if int(self.heap[cur // 2][index]) > int(input[index]):

                self.heap[cur] = self.heap[cur // 2]
                cur = cur // 2
            else:
                break
        self.heap.insert(cur,input)
        
    def popHeap(self,index):

        if self.endPoint == 0:
            return None
        root = 1
        returnValue = self.heap[root]
        value = self.heap[self.endPoint]

        self.heap[self.endPoint] = 0
        self.endPoint -= 1

        if self.endPoint == 0:
            return None
        
        while root * 2 + 1 < 1000001 and value > self.heap[root*2] or value > self.heap[root* 2 + 1]:
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
                n[index] = n[index].replace(',','')
                self.insertHeap(n,index)

        for i in range(len(self.heap)):

            if self.heap[i][index] == 0:
                return self.heap[i+1]
            else:
                return self.heap[i]

# if __name__ == '__main__':
#     sug = suggest()
#     charterList,charterTime = sug.suggestCharter()
#     print(charterList)
#     monthlyList,mCharterList,monthlyTime = sug.suggestMonthly()
#     print(monthlyList)
#     print(mCharterList)