# PinkLAB Signal Processor

A simple Python package providing a moving average and a first-order low-pass filter. This project is brought to you by PinkWink from PinkLAB, aiming to help everyone easily integrate low-pass filtering and moving average functionality in their applications or data processing workflows.


1. **Moving Average**: Compute the average of the most recent N samples (sliding window).
2. **First-Order Low-Pass Filter**: Smooth out noisy data with an exponential moving average.

Both methods are simple to configure and use, reducing the complexity for those who want quick results in signal processing or time-series data smoothing.

---

# Installation

## From PyPI (recommended)

If you have uploaded (or plan to upload) your package to PyPI, users can install directly via:

``` bash
pip install pw-signal-processor
```

## From source

If you are distributing the source code through GitHub (or another repository):

1. Clone (or download) this repository.
2. Navigate to the project root (where setup.py or pyproject.toml is located).
3. Install locally with:

``` bash
pip install -e .
```

# Usage
Once installed, simply import and create an instance of the SignalProcessor class. Configure the `window_size` and `alpha` parameters as needed:

``` python
from signal_processor import SignalProcessor

# Create a processor with a window size of 5 and alpha=0.2 for the low-pass filter
sp = SignalProcessor(window_size=5, alpha=0.2)

# Example data sequence
data = [10, 12, 13, 20, 22, 21, 18, 15, 10, 5, 8, 10]

for val in data:
    ma_val = sp.moving_average(val)
    lp_val = sp.low_pass_filter(val)
    print(f"Input: {val} | Moving Avg: {ma_val:.2f} | Low Pass: {lp_val:.2f}")

``` 

* `moving_average()`: Returns the average of the most recent window_size samples.
* `low_pass_filter()`: Returns an exponentially-weighted value based on the formula `filtered_value = alpha * current_value + (1 - alpha) * previous_filtered_value`.

# Example

``` python
import numpy as np
import matplotlib.pyplot as plt
from signal_processor import SignalProcessor

# Generate some noisy sinusoidal data
time = np.linspace(0, 10, 100)
noise = np.random.normal(0, 0.5, size=time.shape)
signal = np.sin(time) + noise

# Initialize the SignalProcessor
sp = SignalProcessor(window_size=5, alpha=0.1)

ma_output = []
lp_output = []

for val in signal:
    ma_output.append(sp.moving_average(val))
    lp_output.append(sp.low_pass_filter(val))

# Plot the results
plt.figure(figsize=(10,6))
plt.plot(time, signal, label='Noisy Signal', alpha=0.5)
plt.plot(time, ma_output, label='Moving Average', linewidth=2)
plt.plot(time, lp_output, label='Low Pass Filter', linewidth=2)
plt.legend()
plt.title('My-Signal-Processor Demo')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.show()

``` 

In this example:

* We create a noisy sine wave (`signal`) and feed it into the `SignalProcessor`.
* We store the outputs of both the moving average filter (`ma_output`) and the low-pass filter (`lp_output`).
* Finally, we visualize the differences.


# Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the project.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a Pull Request back to the main repository.

We will review your PR as soon as possible.

# License
This project is licensed under the MIT License - feel free to modify and use it as you see fit.

# Contact

If you have any questions or feedback, feel free to reach out:

* PinkWink from PinkLAB
* GitHub: https://github.com/pinklab-art/signal_processor
* Email: pinkwink@pinklab.art

We hope this package helps streamline your signal processing needs!

**Happy filtering!**
— PinkWink @ PinkLAB