class RMM(object):
    def __init__(self):
        self.dic = ['南京', '南京市', '南京市长', '江', '大桥', '江大桥', '长江大桥', '研究', '研究生', '生命', '命', '的', '起源']
        self.max_word_size = 4

    def cut(self, text):
        text_len = len(text)   # 注意：py2用utf-8中一个中文是3字节，py3中使用的是unicode一个中文2字节（py3不用考虑中文编码问题）
        start = text_len
        res = []
        while start > 0:
            for size in range(self.max_word_size, 0, -1):
                piece = text[start - size : start]
                if piece in self.dic:
                    start = start - size + 1
                    break
            # 如果字典里没有这个词，那么就按照单字成词(single)来处理
            start = start - 1
            res.append(piece)
        return res[::-1]

def main():
    tokenizer = RMM()
    print (tokenizer.cut('我是南京市长江大桥'))
    print (tokenizer.cut('研究生命的起源'))

if __name__ == '__main__':
    main()


