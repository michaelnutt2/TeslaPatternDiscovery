'''
with open('VortexDataset.csv', 'w+') as o_f:
    for i in range(100,500):
        for j in range(100,500):
            for k in range(100,500):
                line = str(i*j*k) + ',' + str(i) + ',' + str(j) + ',' + str(k) + ','  + '\n'
                o_f.write(line)
            line = str(i*j) + ',' + str(i) + ',' + str(j) + ',' + '\n'
            o_f.write(line)


for i in range(100,499):
    for j in range(100,499):
        for k in range(100,499):
            line = str(i*j*k) + ',' + str(i) + ',' + str(j) + ',' + str(k) + ','  + '\n'
        line = str(i*j) + ',' + str(i) + ',' + str(j) + ',' + '\n'




with open('VortexDataset.csv','rt') as i_f:
    for i in range(0,100):
        with open('VortexDataset_' + str(i), 'w+') as o_f:
            for j in range(0,641600):
                o_f.write(i_f.readline() )
'''

with open('vortex_operations.csv', 'w+') as v:
    i = 0
    for input in range(0,3):
        for operation in range(0,4):
            for digit in range(0,7):
                v.write(str(i) + ',' + str(input) + ',' + str(digit) + ',' + str(operation) + ',\n')
                i += 1

'''retrieval sample
weights[83] = [...]
# given state, 
index = max(weights)
function = reusable_operation_function(operation => operations[0] == index)

def reusable_operation_function(operation):
    d_sets = [(0),(1),(2),(0,1),(0,2),(1,2),(0,1,2)]
    input = operation[1]
    digit = d_sets(operation[2])
    operator = ''
    switch(operation[3]):
        case 0:
            operator = '+'
        case 1:
            operator = '-'
        case 2:
            operator = '*'
        case 3:
            operator = '/'
# the class we use to hold (o,i,i,i,s,m) is called the_thing
    def func(the_thing):
        value = digital_root(the_thing.input[input], digits) 
        the_thing.scaffold = execute(str(the_thing.scaffold) + operator + str(value))
        the_thing.memory.append(operation[0])
    return func
    
def digital_root(i, d):
    o = 0
    for n in d:
        o += int(str(i)[n])
    if o > 9:
        o = int(str(o)[0]) + int(str(o)[1])
    return o




'''


