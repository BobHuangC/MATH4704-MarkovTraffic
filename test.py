import numpy as np

# 定义状态空间
states = ['A', 'B', 'C']

# 定义状态转移概率矩阵
transition_matrix = np.array([
    [0.2, 0.4, 0.4],
    [0.3, 0.2, 0.5],
    [0.1, 0.6, 0.3]
])

# 定义初始状态分布
initial_distribution = np.array([0.3, 0.4, 0.3])

# 生成马尔科夫链
def generate_markov_chain(num_steps):
    current_state = np.random.choice(states, p=initial_distribution)
    chain = [current_state]
    
    for _ in range(num_steps - 1):
        current_state = np.random.choice(states, p=transition_matrix[states.index(current_state)])
        chain.append(current_state)
    
    return chain

# 生成一个长度为10的马尔科夫链
markov_chain = generate_markov_chain(10)
print(markov_chain)