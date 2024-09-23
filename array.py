my_array = [1,3,4,5,6]
---
student = ["sadini,tarindu,kamal"]
-------
for student in students:
    print(student)
---------
def print_scores(scores):
    for score in scores:
        print(score)
      ---------
scores=[10,20,30,40,50]
scores.append(5)
scores.remove(20)
print(scores)
------------
scores=[10,20,30,40,50,36,87,54,35]
scores.sort()
print(scores)
---------------
scores=[10,20,30,40,50,36,87,54,35]
scores.reverse()
print(scores)
------
import array
arr = array.array('i', [1,2,3,4,5,6,7])
element = arr[2]
print(element)
-------------
import array
arr =array.array('i', [2,4,5,4,4,6,6,3,4,6])
arr.extend([6,6,6,88,8,4,8,8,3,2])
print(arr)
------------
import array
arr =array.array('i', [2,4,5,4,4,6,6,3,4,6])
arr.remove(6)
print(arr)
