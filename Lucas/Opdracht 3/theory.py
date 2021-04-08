import numpy as np
import matplotlib.pyplot as plt

x = np.random.randint(0,100, size=500)
y = np.random.randint(low=-10,high=10, size=500)

custommers = np.concatenate((x, y), axis=0)
custommers.shape = (500,2)

def checker(a , b, custommers):
#     a = np.array(a)
#     b = np.array(b)
    custommers_for_a = 0
    custommers_for_b = 0
    for custommer in custommers:
        custommer = list(custommer)
        dist_to_a = abs(a[0] - custommer[0])
        dist_to_b = abs(b[0] - custommer[0])
        if dist_to_a < dist_to_b:
            custommers_for_a += 1
        elif dist_to_a == dist_to_a and np.random.choice([False, True]):
            custommers_for_a += 1

    # print(f"ca :{custommers_for_a}, cb: {custommers_for_b}")            
    return custommers_for_a

def determin_position(self, other, custommers):
    staying = checker(self, other, custommers)
    going_left = checker([self[0] -1,self[1]], other, custommers)
    going_right = checker([self[0] +1,self[1]], other, custommers)
    return (going_left, staying, going_right)

def act(name, self, other, custommers):
    new_pos = self
    left, stay, right = determin_position(self, other, custommers)
    scores = (f" Going left for {name} will give {left} custommers \n"
              f"Staying for {name} will give {stay} custommers \n"
              f"Going right for {name} will give {right} custommers \n\n")

    if left > stay and left > right:
        new_pos = [self[0] -1, self[1]]
        action = f"{name} will go left giving it the postion {new_pos}\n"
    elif stay > left and stay > right:
        action = f"{name} will stay giving it the postion {new_pos}\n"
    elif right > left and right > left:
        new_pos = [self[0] +1, self[1]]
        action = f"{name} will go right giving it the postion {new_pos}\n"
    elif stay == right or stay == left:
        action = f"{name} will stay giving it the postion {new_pos}\n"
    
    elif right > left:
        new_pos = [self[0] +1, self[1]]
        action = f"{name} will go right giving it the postion {new_pos}\n"
    else:
        new_pos = [self[0] -1, self[1]]
        action = f"{name} will go left giving it the postion {new_pos}\n"
        
    
    # print(scores)
    # print(action)
    
    return new_pos[0]

a_postions = []
b_postions = []
x_a = 25
x_b = 75
for i in range(1500):
    a_postions.append(x_a)
    b_postions.append(x_b)
    new_x_a = act("A", [x_a, 0], [x_b, 0], custommers)
    new_x_b = act("B", [x_b, 0], [x_a, 0], custommers)
    if new_x_a != x_b:
        x_a = new_x_a
    if new_x_b != x_a:
        x_b = new_x_b
    if x_b > 90:
        q = 12

plt.plot(a_postions,label = "a")
plt.plot(b_postions,label = "b")
axes = plt.gca()
axes.set_ylim([0,100])
plt.show()