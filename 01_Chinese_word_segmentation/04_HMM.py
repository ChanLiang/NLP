# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 19:33
# @Author  : ChanLiang
# @FileName: 04_HMM.py
# @Software: PyCharm
# @Github  ：https://github.com/ChanLiang

class HMM(object):
    def __init__(self):
        # 初始化：状态序列，观测序列，模型参数(其中A，B没有用二维数组，而是用的二维字典，更灵活)
        self.states = ['B', 'M', 'E', 'S']
        self.text = '这是一个非常棒的方案'
        self.pi = {key:0 for key in self.states}
        self.A = {state1:{state2:0 for state2 in self.states} for state1 in self.states}  # 两个key都表示states， value表示转移概率
        self.B = {key:{} for key in self.states}   # 第一个key表示state， 第二个key表示observation， value表示发射概率

    def train(self, corpus_path):   # 有监督：频次法就可以
        def word2labels(word):  # 将一个词转化为标记序列
            if len(word) == 1:
                return ['S']
            else:
                return ['B'] + ['M'] * (len(word) - 2) + ['E']

        file = open(corpus_path, encoding='utf-8')
        line_count, state_count = 0, {state:0 for state in self.states}
        for line in file:   # 一行代表一条训练记录
            line = line.strip()
            if not line:    break
            line_count += 1
            words = line.split()
            line_labels = []
            for word in words:
                line_labels.extend(word2labels(word))
            line = [char for char in line if char != ' ']
            assert len(line) == len(line_labels)    # 验证 状态序列(q1,q2...qt) 和 观测序列(y1,y2...yt) 是否等长

            for i in range(len(line_labels)):   # 统计频次
                state_count[line_labels[i]] += 1
                if i == 0:
                    self.pi[line_labels[i]] += 1
                else:
                    self.A[line_labels[i - 1]][line_labels[i]] += 1
                    self.B[line_labels[i]][line[i]] = self.B[line_labels[i]].get(line[i], 0) + 1
        file.close()

        self.pi = {key:val/line_count for key, val in self.pi.items()}
        self.A = {state1:{state2:val/state_count[state1] for state2, val in self.A[state1].items()} for state1 in self.states}
        self.B = {state1:{char:val/state_count[state1] for char, val in self.B[state1].items()} for state1 in self.states}


    def viterbi(self):
        # 二维dp问题
        dp = [{state:0 for state in self.states} for _ in range(len(self.text))]
        # 初始化 状态 和 路径 的备忘录
        dp[0] = {state:prob * self.B[state].get(self.text[0], 0) for state, prob in self.pi.items()}
        paths = {state:[state] for state in self.states}

        # O(T*n^2)
        for t in range(1, len(self.text)):
            record_pre = 'S'
            cur_paths = {state:[] for state in self.states}
            for cur_state in self.states:
                # 如果该字没有在训练语料库中出现(不能由任何状态生成)，那么将任意状态生成它的概率都置为1
                emition_p = self.B[cur_state].get(self.text[t], 0) if self.text[t] in self.B['B'] or self.text[t] in self.B['M'] or self.text[t] in self.B['E'] or self.text[t] in self.B['S'] else 1
                for pre_state in self.states:
                    prob = dp[t - 1][pre_state]*self.A[pre_state][cur_state]*emition_p
                    if prob > dp[t][cur_state]:
                        dp[t][cur_state] = prob
                        record_pre = pre_state
                cur_paths[cur_state] = paths[record_pre] + [cur_state]
            paths = cur_paths

        if dp[len(self.text) - 1]['S'] > dp[len(self.text) - 1]['M']:
            return paths['S']
        else:
            return paths['E']

    def cut(self):
        states = self.viterbi()
        string = ''
        for i in range(len(self.text)):
            string += self.text[i]
            if states[i] == 'S' or states[i] == 'E':    # 遇到 single 和 end 时加空格
                string += ' '
        return string


def main():
    model = HMM()
    model.train('./data/trainCorpus.txt_utf8')
    print (model.cut())

if __name__ == '__main__':
    main()

