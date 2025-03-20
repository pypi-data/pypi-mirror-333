# 1. test obj.attr 修改

def modify(o):
    o['k']['k'] = 'vb'

a = {
    'k': 'v'
}

b = {
    'k': a
}
print(b)
c = a

# b['k']['k'] = 'vb'
modify(o=b)

print(b)
print(c)
print(a)
