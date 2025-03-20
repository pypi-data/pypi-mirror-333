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

    def plot_signals(time, signal, ma_output, lp_output, x_range=None):
        import numpy as np
        import matplotlib.pyplot as plt

        """
        Plots the noisy signal, moving average, and low pass filter outputs.
        
        Parameters:
        - time: 1D array-like, time data.
        - signal: 1D array-like, original noisy signal.
        - ma_output: 1D array-like, moving average output.
        - lp_output: 1D array-like, low pass filter output.
        - x_range: Optional list or tuple [start, end] to set the x-axis range.
                If provided, the function will also adjust the y-axis limits
                to include a 10% margin based on the data within this x range.
        """
        
        plt.figure(figsize=(10, 6))
        plt.plot(time, signal, label='Noisy Signal', alpha=0.5)
        plt.plot(time, ma_output, label='Moving Average', linewidth=2)
        plt.plot(time, lp_output, label='Low Pass Filter', linewidth=2)
        plt.legend()
        plt.title('My-Signal-Processor Demo')
        plt.xlabel('Time (second)')
        plt.ylabel('Amplitude')
        plt.grid()
        
        if x_range is not None:
            # Set x-axis limits
            plt.xlim(x_range)
            
            # Create a boolean mask for the selected x range
            mask = (time >= x_range[0]) & (time <= x_range[1])
            
            # Combine the y-values for the selected range from all signals
            y_values = np.concatenate([ np.array(signal)[mask],
                                        np.array(ma_output)[mask],
                                        np.array(lp_output)[mask]])
            
            # Compute y min and max, then add a 10% margin
            y_min = np.min(y_values)
            y_max = np.max(y_values)
            margin = 0.1 * (y_max - y_min)
            plt.ylim(y_min - margin, y_max + margin)
        
        plt.show()
