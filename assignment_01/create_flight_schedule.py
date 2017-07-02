
# coding: utf-8

# In[1]:

flt_t = [['AUS','DAL',50],
         ['AUS','HOU',45],
         ['DAL','HOU',65],
         ['DAL','AUS',50],
         ['HOU','AUS',45],
         ['HOU','DAL',65]]
flt_t


# In[2]:

grnd_t = {'AUS':25,
          'DAL':30,
          'HOU':35}
grnd_t


# In[3]:

flt_s = [['T1','AUS','HOU',360,405,440],
         ['T2','HOU','DAL',360,425,455],
         ['T3','HOU','DAL',360,425,455],
         ['T4','DAL','HOU',360,425,460],
         ['T5','DAL','HOU',360,425,460],
         ['T6','HOU','AUS',360,405,430]]
flt_s


# In[4]:

#To store the open time of the gates
h_open = []
d_open = []
a_open = []

gate_open_t={'HOU':[0,0,0],'DAL':[0,0],'AUS':[0]} 

for temp in flt_s:
    print(temp[2])
    if temp[2] == 'HOU':
        h_open.append(temp[5])
    if temp[2] == 'DAL':
        d_open.append(temp[5])
    if temp[2] == 'AUS':
        a_open.append(temp[5])
        
gate_open_t['HOU'] = h_open[:]
gate_open_t['DAL'] = d_open[:]
gate_open_t['AUS'] = a_open[:]
print(gate_open_t)
gates={'HOU':4,'DAL':3,'AUS':2} #the total gates+1 for calculation purposes


# In[5]:

#Check for possible destination and timing

def check_next(dep,t_dep):
    depart = dep # Current location of flight
    tim = t_dep + 1  #Earliest possible depart time
    pos_des =[]

    for x in gate_open_t:
        gate_open_t[x].sort()

    for src in flt_t:
            print("tim total:",tim + src[2])
            print("gates open time:",gate_open_t[src[1]][0])
            print("gates closed:",gate_close[src[1]])
            print("gates:",gates[src[1]])
            if (src[0] == depart) and ((tim + src[2]) > gate_open_t[src[1]][0]) and (gate_close[src[1]] < gates[src[1]]) and (tim + src[2]) <=1320: #
                print('from:',depart)
                print('to:',src[1])
                print('no of gates closed:',gate_close[src[1]])
                print("gates avl:",gates[src[1]])
                print("gate open time :",gate_open_t[src[1]][0])
                #print("arrival time :",(tim + src[2]))
                temp=[]
                temp.append(src[1])
                temp.append(tim + src[2]) 
                pos_des.append(temp)
                print(gate_open_t)
                
    if ctr <4:
        print('prog 1', ctr)
        pos_des_sort=sorted(pos_des, key=lambda x: x[1]) #change if u want earliest time
    elif ctr > 4 and ctr%2 == 0:
        print('prog 1 but>4', ctr)
        pos_des_sort=sorted(pos_des, key=lambda x: x[1]) #change if u want earliest time
    else:
        print('prog 2', ctr)
        pos_des_sort=sorted(pos_des, key=lambda x: x[1], reverse = True) #change if u want earliest time
        print('poss', pos_des_sort)
        
    if len(pos_des_sort) > 0:
        
        arrival = depart
        destination = pos_des_sort[0][0]
        depart_time = tim
        arrival_time = pos_des_sort[0][1]
        grnd_time = pos_des_sort[0][1] + grnd_t[destination]
        print('Decided leaving from:',arrival)
        print('Decided dest to:',destination)
        print('grnd_time:',grnd_time)
        print('out of func')
        return arrival,destination,depart_time,arrival_time,grnd_time

    elif tim + 44 > 1320:
        return 0,0,0,0,0
     

    else: 
        print('calling func again')
        return check_next(depart,tim+1)
    


# In[6]:

ctr = 0
list_flight = []
for i in flt_s:
    list_flight+=i
list_flight

while(len(flt_s) > 0):    
    flt_s = [item for item in flt_s if not item[5] > 1320]
    flt_s = sorted(flt_s, key=lambda x: x[5])

    gate_close={'HOU':1,'DAL':1,'AUS':1}
    for flight in flt_s:        
        #print('start Flight no:',flight)
        #print('from:',flight[2])
        arrival, dest, depart_t, arrival_t, ground_t = check_next(flight[2],flight[5])
        if arrival != 0:
            gate_open_t[dest][0]=arrival_t+grnd_t[dest]
            flight[1] = arrival
            flight[2] = dest
            flight[3] = depart_t
            flight[4] = arrival_t
            flight[5] = ground_t
            print('Modifying the record:',flight)
            gate_close[dest] += 1
        else:
            flt_s.remove(flight)            

    for i in flt_s:
        list_flight+=i
    ctr += 1
print('list', list_flight)
print('flight', flt_s)
flt_s = sorted(flt_s, key=lambda x: x[3])
print('flight', flt_s)
print(gate_close)




# In[7]:

print(list_flight)


# In[8]:

j=0
new=[]
while j<len(list_flight):
  new.append(list_flight[j:j+6])
  j+=6
new


# In[9]:

def mintomid_miltim(a):
    if a//60 < 10 and a%60 < 10:
        b='0'+str(a//60)+'0'+str(a%60)
    elif a//60 >= 10 and a%60 < 10:
         b=str(a//60)+'0'+str(a%60)
    elif a//60 < 10 and a%60 >= 10:
        b='0'+str(a//60)+str(a%60)
    else :
        b=str(a//60)+str(a%60)
    return b

final = []

for item in new:
    temp=[]
    temp.append(item[0])
    temp.append(item[1])
    temp.append(item[2])
    temp.append(mintomid_miltim(item[3]))
    temp.append(mintomid_miltim(item[4]))
    final.append(temp)

final
final = sorted(final, key=lambda x: x[0])
final
del final [-1]
final


# In[10]:

csv_header = 'tail_number,origin,destination,departure_time,arrival_time'
file_name = 'flight_schedule.csv'

def print_flt_sedule(fn, csv_hdr, flt_sched):
    with open(fn,'wt') as f:
        print(csv_hdr, file=f)
        for s in flt_sched:
            print(','.join(s), file=f)
            
print_flt_sedule(file_name, csv_header, final)

