class SignalProcessor:
    
    def __init__(self, window_size=5, alpha=0.1):
        self.window_size = window_size
        self.alpha = alpha
        self._buffer = []
        self._prev_filtered_value = 0.0

    def moving_average(self, new_value):
        self._buffer.append(new_value)
        if len(self._buffer) > self.window_size:
            self._buffer.pop(0)
        return sum(self._buffer) / len(self._buffer)

    def low_pass_filter(self, new_value):
        filtered_value = self.alpha * new_value + (1 - self.alpha) * self._prev_filtered_value
        self._prev_filtered_value = filtered_value
        return filtered_value

    def reset(self):
        self._buffer = []
        self._prev_filtered_value = 0.0
