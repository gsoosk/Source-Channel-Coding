import heapq


class HuffmanTreeNode:
    def __init__(self, value=None, freq=None, right=None, left=None, top=None):
        self.value = value
        self.freq = freq
        self.right = right
        self.left = left
        if self.right and self.left:
            self.freq = self.left.freq + self.right.freq

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanTree:
    def __init__(self, freq_dic):
        self.make_tree(freq_dic)
        self.make_codes()

    def make_tree(self, freq_dic):
        heap = []
        for freq in freq_dic.items():
            node = HuffmanTreeNode(value=freq[0], freq=freq[1])
            heapq.heappush(heap, node)

        while(len(heap) != 1):
            right_node = heapq.heappop(heap)
            left_node = heapq.heappop(heap)
            top_node = HuffmanTreeNode(
                value="$", left=left_node, right=right_node)
            heapq.heappush(heap, top_node)

        self.head = heapq.heappop(heap)

    def make_codes(self):
        self.codes = {}
        self.dfs(self.head, '')

    def dfs(self, head, code):
        if head.value is not '$':
            self.codes[head.value] = code
            return

        self.dfs(head.left, code + '0')
        self.dfs(head.right, code + '1')

    def code(self, input_string):
        output_string = ''
        for ch in input_string.lower():
            output_string += self.codes[ch]
        return output_string

    def decode(self, input_string):
        inv_codes = {v: k for k, v in self.codes.items()}
        start = 0
        decoded = ''
        for i in range(len(input_string)):
            try:
                char = inv_codes[input_string[start:i+1]]
                decoded += char
                start = i + 1
            except:
                continue
        return decoded
