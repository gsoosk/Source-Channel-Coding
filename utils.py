def get_word_frequencis():
    import scipy.io
    mat = scipy.io.loadmat('freq.mat')
    freq_dic = {}
    for i in range(97, 122 + 1):
        freq_dic[chr(i)] = mat['freq'][i - 97][0]
    return freq_dic


def noise(input):
    import numpy as np
    for i in range(len(input)):
        r = np.random.rand()
        if r < 0.01:
            input[i] = 1 - input[i]
    output = input
    return output


def noise_string(input_string):
    input_arr = [int(i) for i in list(input_string)]
    output_arr = noise(input_arr)
    return ''.join([str(i) for i in output_arr])
