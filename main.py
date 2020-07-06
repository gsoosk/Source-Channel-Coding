import sys
from utils import get_word_frequencis, noise_string
from channel_coding import Convolutional
from source_coding import HuffmanTree


def main(input_text):
    freq_dic = get_word_frequencis()

    network_tree = HuffmanTree(freq_dic)
    channel_conv = Convolutional()
    # Pipeline
    # coding
    network_coded = network_tree.code(input_text)
    channel_coded = channel_conv.code(network_coded)
    # noise
    noised_code = noise_string(channel_coded)
    # decoding
    channel_decoded = channel_conv.decode(noised_code)
    network_decoded = network_tree.decode(channel_decoded)

    output_text = network_decoded
    print(output_text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Please enter input string as argument!')
    main(sys.argv[1])
