'''
最简单的四个格子的迷宫
---------------
| start |     |
---------------
|  die  | end |
---------------

每个格子是一个状态，此时都有上下左右4个动作
'''

import pandas as pd
import random

epsilon = 0.9   # 贪婪度 greedy
alpha = 0.1     # 学习率
gamma = 0.8     # 奖励递减值

states = range(4)      # 0, 1, 2, 3 四个状态
actions = list('udlr') # 上下左右 4个动作。还可添加动作'n'，表示停留
rewards = [0,0,-10,10] # 奖励集。到达位置3（出口）奖励10，位置2（陷阱）奖励-10，其他皆为0


q_table = pd.DataFrame(data=[[0 for _ in actions] for _ in states],index=states, columns=actions)

def get_next_state(state, action):
    #对状态执行动作后，得到下一状态
    #u,d,l,r,n = -2,+2,-1,+1,0
    if state % 2 != 1 and action == 'r':    # 除最后一列，皆可向右(+1)
        next_state = state + 1
    elif state % 2 != 0 and action == 'l':  # 除最前一列，皆可向左(-1)
        next_state = state -1
    elif state // 2 != 1 and action == 'd': # 除最后一行，皆可向下(+2)
        next_state = state + 2
    elif state // 2 != 0 and action == 'u': # 除最前一行，皆可向上(-2)
        next_state = state - 2
    else:
        next_state = state
    return next_state
        

def get_valid_actions(state):
    '''取当前状态下的合法动作集合
    global reward
    valid_actions = reward.ix[state, reward.ix[state]!=0].index
    return valid_actions
    '''
    # 与reward无关！
    global actions
    valid_actions = set(actions)
    if state % 2 == 1:                              # 最后一列，则
        valid_actions = valid_actions - set(['r'])  # 无向右的动作
    if state % 2 == 0:                              # 最前一列，则
        valid_actions = valid_actions - set(['l'])  # 无向左
    if state // 2 == 1:                             # 最后一行，则
        valid_actions = valid_actions - set(['d'])  # 无向下
    if state // 2 == 0:                             # 最前一行，则
        valid_actions = valid_actions - set(['u'])  # 无向上
    return list(valid_actions)
    
    
# 总共探索300次
for i in range(100):
    # 0.从最左边的位置开始（不是必要的）
    current_state = 0
    #current_state = random.choice(states)
    while current_state != states[-1]:
        # 1.取当前状态下的合法动作中，随机（或贪婪）地选一个作为 当前动作
        if (random.uniform(0,1) > epsilon) or ((q_table.ix[current_state] == 0).all()):
            current_action = random.choice(get_valid_actions(current_state))
        else:
            current_action = q_table.ix[current_state].idxmax() # 利用（贪婪）
        # 2.执行当前动作，得到下一个状态（位置）
        next_state = get_next_state(current_state, current_action)
        # 3.取下一个状态所有的Q value，待取其最大值
        next_state_q_values = q_table.ix[next_state, get_valid_actions(next_state)]
        # 4.根据贝尔曼方程，更新 Q table 中当前状态-动作对应的 Q value
        q_table.ix[current_state, current_action] += alpha * (rewards[next_state] + gamma * next_state_q_values.max() - q_table.ix[current_state, current_action])
        # 5.进入下一个状态（位置）
        current_state = next_state
        print(q_table)

print('\nq_table:')
print(q_table)