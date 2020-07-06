import math


class ConvolutionalState:
    def __init__(self, value, start_state=False):
        self.value = value
        self.path_metric = 0 if start_state else math.inf

    def set_shape(self, zero, zero_output, one, one_output):
        self.next_states = {0: zero, 1: one}
        self.next_outputs = {0: zero_output, 1: one_output}

    def get_next_encode_state(self, input_bit):
        if input_bit == '0':
            bit = 0
        elif input_bit == '1':
            bit = 1
        else:
            raise ValueError('Unvalid State Input Value')

        return self.next_states[bit], self.next_outputs[bit]

    def get_next_decode_state(self):
        if self.next_states[0].path_metric < self.next_states[1].path_metric:
            return self.next_states[0], '0'
        return self.next_states[1], '1'


# In[7]:


class Convolutional:
    def __init__(self):
        self.create_states()

    def create_states(self):
        state_00 = ConvolutionalState('00', start_state=True)
        state_10 = ConvolutionalState('10')
        state_01 = ConvolutionalState('01')
        state_11 = ConvolutionalState('11')

        state_00.set_shape(state_00, '00', state_10, '11')
        state_10.set_shape(state_01, '11', state_11, '00')
        state_01.set_shape(state_00, '10', state_10, '01')
        state_11.set_shape(state_01, '01', state_11, '10')

        self.states = [state_00, state_01, state_10, state_11]
        self.start_state = state_00

    def code(self, input_string, verbose=False):
        output_string = ''
        state = self.start_state
        for input_char in input_string:
            if verbose:
                print(f'In state: {state.value}')
            next_state, state_output = state.get_next_encode_state(input_char)
            output_string += state_output
            state = next_state
        return output_string

    def decode(self, input_string):
        global_state = self.start_state
        output_string = ''

        for i in range(0, len(input_string), 2):
            next_metrics = {}
            input_block = input_string[i:i+2]
            for state in self.states:
                next_metrics[state.value] = []
            for state in self.states:
                for i in range(2):
                    xor_of_edge = self.xor(input_block, state.next_outputs[i])
                    next_metrics[state.next_states[i].value].append(
                        xor_of_edge + state.path_metric)
            for state in self.states:
                state.path_metric = min(next_metrics[state.value])

            global_state, decoded_output = global_state.get_next_decode_state()
            output_string += decoded_output

        return output_string

    def xor(self, s1, s2):
        return sum([(int(a) ^ int(b)) for a, b in zip(s1, s2)])
