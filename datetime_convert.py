from datetime import  datetime

# a = datetime.now()
# b = a.strftime('%Y%m%d')
# print(b)
# c = datetime.strptime(b, '%Y%m%d')
# print(c)
#
# a = datetime.fromtimestamp(1234567896)
# print(a)
now = datetime.now()
now = now.strftime("%Y%m%d")
print(now)