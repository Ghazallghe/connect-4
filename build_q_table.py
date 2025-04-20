import numpy as np

from game import Connect4


class BuildQTable(Connect4):
    ACTION_SET_SIZE = 7
    STATE_SPACE_SIZE = 42  # we consider only the last piece possible state

    def __init__(self, alpha, gamma, epsilon, times, file_addr):
        super().__init__()
        self.action_set = np.arange(self.ACTION_SET_SIZE)
        self.q_table1 = np.zeros((self.STATE_SPACE_SIZE, self.ACTION_SET_SIZE))

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.times = times
        self.file_addr = file_addr

    def epsilon_policy_algorithm(self, Q, epsilon, state):
        random_action_p = np.random.random()

        if random_action_p < epsilon:
            action = np.random.choice(self.action_set)
        else:
            action = np.argmax(Q[state])

        return action

    def update_q_table(self, Q, state, action, alpha, reward, gamma, new_state):
        update_value = (1 - alpha) * Q[state, action] + \
            alpha * (reward + gamma * np.argmax(Q[new_state, :]))
        Q[state, action] = update_value

    def find_location_on_board(self, state):
        row = state // self.COLUMN
        col = state % self.COLUMN
        return (row, col)

    def find_state_from_board(self, location):
        return location[0] * self.COLUMN + location[1]

    def find_new_state(self, board, action):
        row = self.select_row(board, action)

        return self.find_state_from_board((row, action))

    def training_function(self, Q1, board):

        s = 0
        reward = 0
        return_value = 0
        count = 0
        is_finished = False
        turn = 1
        while not is_finished:

            if turn == 1:
                action1 = self.epsilon_policy_algorithm(
                    Q1, self.epsilon, s)

                if self.is_valid(board, action1):
                    state1 = self.find_new_state(board, action1)
                    self.select_place(board, action1, 1)
                    count += 1
                    if self.fully_goal_test(board, 1):
                        reward = 20
                        is_finished = True
                        return_value = 1

                    elif count == 42:
                        reward = -15
                        is_finished = True

                    self.update_q_table(
                        Q1, s, action1, self.alpha, reward, self.gamma, state1)
                    turn = not turn
                else:
                    reward = -10
                    self.update_q_table(
                        Q1, s, action1, self.alpha, reward, self.gamma, s)
            else:
                action2 = np.random.choice(self.action_set)

                if self.is_valid(board, action2):
                    state2 = self.find_new_state(board, action2)
                    self.select_place(board, action2, 2)
                    count += 1
                    if self.fully_goal_test(board, 2):
                        reward = -40
                        is_finished = True
                        return_value = 2

                    elif count == 42:
                        reward = -15
                        is_finished = True

                    self.update_q_table(Q1, state1, action2, self.alpha,
                                        reward, self.gamma, state2)
                    turn = not turn
                    s = state2
        return return_value

    def start_training(self):
        learning_agent_wins = 0
        for t in range(self.times):
            b = np.zeros((self.ROW, self.COLUMN))

            result = self.training_function(self.q_table1, b)

            if result == 1:
                learning_agent_wins += 1

        learning_agent_wins /= float(self.times)
        print("Percentage of winning games for learning agent :",
              learning_agent_wins * 100)
        np.savetxt(self.file_addr + '.csv', self.q_table1,
                   delimiter=',', fmt='%.2f', header='My Array')
        return self.q_table1


# a = BuildQTable(0.01, 0.9, 0.3, 20, './test_functions')
# a.start_training()
