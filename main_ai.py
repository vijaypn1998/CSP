#CSP Encoding Problem

import sys

def display_result(array, valid_flag): #To display the results in the form of string, returns nothing

    global display_ind
    dis_str = str(display_ind) + ". "
    for i in range(len(array) - 1):
        dis_str = dis_str + array[i] + ", "
    dis_str = dis_str + array[-1]
    if(valid_flag == 0):
        dis_str = dis_str + " failure"
    else:
        dis_str = dis_str + " solution"
    print(dis_str)
    display_ind += 1
    return 0

def get_variable(curr_ind): #To get the most constrained & constraining variable, returns index of variable

    global degree_dic, domain_list, rank_dic
    domain_size = len(degree_dic)
    if(curr_ind == domain_size - 1):
        return
    
    swap_ind = curr_ind
    curr_d_len = len(domain_list[curr_ind][1])
    while((swap_ind < domain_size - 1) and (curr_d_len == len(domain_list[swap_ind + 1][1]))): #Get all equally constrained variables
        swap_ind += 1
    if(swap_ind == curr_ind):# No equally constrained variables
        return

    #calculate the degree of all equally constrained variable
    for i in range(curr_ind, swap_ind + 1):
        curr_ele = domain_list[i][0]
        degree_dic[curr_ele][1] = 0
        for neigh in degree_dic[curr_ele][2]:
            if(degree_dic[neigh][0] == 0):
                degree_dic[curr_ele][1] += 1

    #sort with decresing order of degree
    relative_i = 0
    for i in range(curr_ind, swap_ind + 1):
        swapped = False
        for j in range(curr_ind, swap_ind - relative_i):
            if((degree_dic[domain_list[j][0]][1] < degree_dic[domain_list[j + 1][0]][1])):
                rank_dic[domain_list[j][0]] = j + 1
                rank_dic[domain_list[j + 1][0]] = j
                domain_list[j], domain_list[j + 1] = domain_list[j + 1], domain_list[j]
                swapped = True
        relative_i += 1
        if(swapped == False):
            break

    swap_ind = curr_ind
    curr_degree = degree_dic[domain_list[curr_ind][0]][1]
    while((swap_ind < domain_size - 1) and (curr_degree == degree_dic[domain_list[swap_ind + 1][0]][1])): #Get all equally constraining variables
        swap_ind += 1
    if(swap_ind == curr_ind):# No equally constraining variables
        return

    #sort with increasing ASCII value of variables
    relative_i = 0
    for i in range(curr_ind, swap_ind + 1):
        swapped = False
        for j in range(curr_ind, swap_ind - relative_i):
            if(domain_list[j][0] > domain_list[j + 1][0]):
                rank_dic[domain_list[j][0]] = j + 1
                rank_dic[domain_list[j + 1][0]] = j
                domain_list[j], domain_list[j + 1] = domain_list[j + 1], domain_list[j]
                swapped = True
        relative_i += 1
        if(swapped == False):
            break   
    return

def get_values(curr_ind): #To get the least constraining value.

    global degree_dic, domain_list, rank_dic, con_list, domain_dic
    value_dic = {}   
    cur_ele = domain_list[curr_ind][0]
    cur_d = domain_list[curr_ind][1]
    for v in cur_d:
        value_dic[v] = 0
    for neigh in degree_dic[cur_ele][2]:
        for condition in con_list:
            if((cur_ele in condition) and (neigh in condition) and (degree_dic[neigh][0] == 0)):
                for v in cur_d:
                    for neigh_v in domain_dic[neigh]:
                        if(condition[1] == ">"):
                            if(condition[0] == cur_ele):
                                if(v > neigh_v):
                                    value_dic[v] += 1
                            else:
                                if(v < neigh_v):
                                    value_dic[v] += 1
                        elif(condition[1] == "<"):
                            if(condition[0] == cur_ele):
                                if(v < neigh_v):
                                    value_dic[v] += 1
                            else:
                                if(v > neigh_v):
                                    value_dic[v] += 1
                        elif(condition[1] == "=" and v == neigh_v):
                            value_dic[v] += 1
                        elif(condition[1] == "!" and v != neigh_v):
                            value_dic[v] += 1
    max_ind = len(cur_d)
    least_cons_val = cur_d[0]
    for i in range(max_ind):
        if(value_dic[cur_d[i]] > value_dic[least_cons_val]):
            least_cons_val = cur_d[i]

    return [value_dic, least_cons_val] 

def arrange_domains(var, array, domain):#To arrange domains in increasing order of domain_length

    if(len(array) == 0):
        array.insert(0, [var, domain])
        return
    i = 0
    d_len = len(domain)
    while(i < len(array)):
        if(d_len < len(array[i][1])):
            array.insert(i, [var, domain])
            return i
        elif(d_len == len(array[i][1])):
            if(var < array[i][0]):
                array.insert(i, [var, domain])
                return i
        i += 1
    array.insert(i, [var, domain])
    return

def check_condition(var_select, val_select):#To check if a value is consistent, return 1 else 0

    global degree_dic, domain_list, con_list
    valid_flag = 1
    for condition in con_list:
        for neigh in degree_dic[var_select][2]:
            if((neigh in condition) and (var_select in condition) and degree_dic[neigh][0] == 1):
                neigh_val = degree_dic[neigh][3]
                if(condition[1] == ">"):
                    if(condition[0] == var_select):
                        if(val_select <= neigh_val):
                            valid_flag = 0
                    else:
                        if(val_select >= neigh_val):
                            valid_flag = 0
                elif(condition[1] == "<"):
                    if(condition[0] == var_select):
                        if(val_select >= neigh_val):
                            valid_flag = 0
                    else:
                        if(val_select <= neigh_val):
                            valid_flag = 0
                elif(condition[1] == "=" and val_select != neigh_val):
                    valid_flag = 0
                elif(condition[1] == "!=" and val_select == neigh_val):
                    valid_flag = 0
            if(valid_flag == 0):
                break
    
    if(valid_flag == 1):
        degree_dic[var_select][0] = 1
        degree_dic[var_select][3] = val_select
    return valid_flag

def forward_check(var_select, val_select):#To reduce domain of variables not yet assigned

    global degree_dic, domain_list, rank_dic, con_list, restore_dic
    reorder_flag = 0
    for condition in con_list:
        for neigh in degree_dic[var_select][2]:
            if((neigh in condition) and (var_select in condition) and degree_dic[neigh][0] == 0):
                neigh_ind = rank_dic[neigh]
                neigh_list = list(domain_list[neigh_ind][1])
                for neigh_v in neigh_list:
                    if(condition[1] == ">"):
                        if(condition[0] == var_select):
                            if(val_select <= neigh_v):
                                domain_list[rank_dic[neigh]][1].remove(neigh_v)
                                restore_dic[neigh].append(neigh_v)
                                reorder_flag = 1
                        else:
                            if(val_select >= neigh_v):
                                domain_list[rank_dic[neigh]][1].remove(neigh_v)
                                restore_dic[neigh].append(neigh_v)
                                reorder_flag = 1
                    elif(condition[1] == "<"):
                        if(condition[0] == var_select):
                            if(val_select >= neigh_v):
                                domain_list[rank_dic[neigh]][1].remove(neigh_v)
                                restore_dic[neigh].append(neigh_v)
                                reorder_flag = 1 
                        else:
                            if(val_select <= neigh_v):
                                domain_list[rank_dic[neigh]][1].remove(neigh_v)
                                restore_dic[neigh].append(neigh_v)
                                reorder_flag = 1
                    elif(condition[1] == "=" and val_select != neigh_v):
                        domain_list[rank_dic[neigh]][1].remove(neigh_v)
                        restore_dic[neigh].append(neigh_v)
                        reorder_flag = 1
                    elif(condition[1] == "!=" and val_select == neigh_v):
                        domain_list[rank_dic[neigh]][1].remove(neigh_v)
                        restore_dic[neigh].append(neigh_v)
                        reorder_flag = 1
    return reorder_flag

def reorder_domains(start_ind, reorder_flag):

    global domain_list, rank_dic
    end_ind = len(domain_list) - 1
    if(reorder_flag == 0):
        return
    relative_i = 0
    for i in range(start_ind, end_ind + 1):
        swapped = False
        for j in range(start_ind, end_ind - relative_i):
            if(len(domain_list[j][1]) > len(domain_list[j + 1][1])):
                rank_dic[domain_list[j][0]] = j + 1
                rank_dic[domain_list[j + 1][0]] = j
                domain_list[j], domain_list[j + 1] = domain_list[j + 1], domain_list[j]
                swapped = True
        relative_i += 1
        if(swapped == False):
            break
    return

def restore_domains(start_ind):

    global domain_list, restore_dic
    end_ind = len(domain_list)
    for i in range(start_ind, end_ind):
        for var in restore_dic:
            if(var == domain_list[i][0]):
                for value in restore_dic[var]:
                    domain_list[i][1].append(value)
                break

#Input Validity check
num_arg = len(sys.argv)
if(num_arg != 4):
    print("Usage: python3 main.py variable_file condition_file backtrack")
    exit()
try:
    var_file = open(sys.argv[1], 'r')
except:
    print("Usage: python3 main.py variable_file condition_file backtrack")
    exit()
try:
    con_file = open(sys.argv[2], 'r')
except:
    print("Usage: python3 main.py variable_file condition_file backtrack")
    exit()
if((sys.argv[3] != "fc") and (sys.argv[3] != "none")):
    print("Usage: python3 main.py variable_file condition_file backtrack")
    exit()

domain_list = list() #Used to store the domain as the search progresses :[variable, Domain]
degree_dic = dict() #Dictionary {variables : [0/1 to indicate variable assignment, degree, set of neigbours, value_assigned]}
domain_dic = dict() #Used to store the original domain of all variables, doesnt change : {variable : domain}
restore_dic = dict() #Used to keep track of eleminated values for restoring during forward_check
con_list = list() #Used to store all the conditions [cond1, cond2...]
steps = list() #Used to store the assignments
restore_list = list() #Used to store the inferences of foward checking
rank_dic = dict() #Used to store the order in which variables should be assinged, updates as the search progresses, {variable : rank}
display_ind = 1#Used for presenting the output

#Read the variable file and populate domain_list, domain_dic and parts of degree_dic
var_data = var_file.readlines()
for line in var_data:
    line = line.split(':')
    var = line[0]
    domain = line[1].split()
    domain = [int(each) for each in domain]
    domain_dic[var] = list(domain)
    restore_dic[var] = []
    arrange_domains(var, domain_list, domain)
    degree_dic[var] = [0, 0, set(), 0]

for variable in restore_dic:
    for i in range(len(domain_list)):
        if(variable == domain_list[i][0]):
            rank_dic[variable] = i
            break

#Read the condition file and populate con_list and parts of degree_dic
con_data = con_file.readlines()
for line in con_data:
    line = line.split()
    con_list.append(line)
    degree_dic[line[0]][2].add(line[2])
    degree_dic[line[2]][2].add(line[0])

assign_ind = 0
assign_max = len(degree_dic) - 1
reorder_flag = 0
while(assign_ind <= assign_max):

    #Getting the variable
    get_variable(assign_ind)
    var_select = domain_list[assign_ind][0]
    #Getting the value
    [value_dic, val_select] = get_values(assign_ind)

    #Check if the assignment is consistent
    valid_flag = check_condition(var_select, val_select)
    steps.append(str(var_select) + "=" + str(val_select))
    #Forward Checking:    
    if(valid_flag == 1): #If the assignment is valid
        if(sys.argv[3] == "fc"): #Forward Checking
            reorder_flag = forward_check(var_select, val_select)
            reorder_domains(assign_ind + 1, reorder_flag)
            if((assign_ind + 1 <= assign_max) and domain_list[assign_ind + 1][1] == []): #Forward checking caught a failure
                display_result(steps, 0)
                steps.pop(-1)
                restore_domains(assign_ind + 1)
                del value_dic[val_select]
                domain_list[assign_ind][1].remove(val_select)
                continue
            else:
                #If forward checking passes, empty out the restore_dic
                for i in range(assign_max):
                    restore_dic[domain_list[i][0]] = list()
                del value_dic[val_select]
                domain_list[assign_ind][1].remove(val_select)
                assign_ind += 1
                continue        
        else:
            del value_dic[val_select]
            domain_list[assign_ind][1].remove(val_select)
            assign_ind += 1
            continue

    else:
        del value_dic[val_select]
        domain_list[assign_ind][1].remove(val_select)

    if(domain_list[assign_ind][1] == []):

        display_result(steps, 0)
        steps.pop(-1) #pop last failed 
        if(steps == []):
            exit()
        steps.pop(-1)
        domain_list[assign_ind][1] = list(domain_dic[var_select])
        assign_ind -= 1
    else:
        display_result(steps, 0)
        steps.pop(-1) #pop  last failed

        if(len(value_dic) != 0):
            continue
        assign_ind -= 1
display_result(steps, valid_flag)