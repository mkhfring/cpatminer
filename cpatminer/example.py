
import numpy as np
import matplotlib.pyplot as plt

def hello_world(a):
    if a == 1:
        print("Hello world!")

    else:
        print("Bye Bye")



if __name__ == "__main__":
    hello_world('s')
    xvalues = np.linspace(-np.pi, np.pi)
    yvalues1 = np.sin(xvalues)
    yvalues2 = np.cos(xvalues)
    plt.plot(xvalues, yvalues1, lw=2, color='red',
             label='sin(x)')
    plt.plot(xvalues, yvalues2, lw=2, color='blue',
             label='cos(x)')
    plt.title('Trigonometric Functions')
    plt.xlabel('x')
    plt.ylabel('sin(x), cos(x)')
    plt.axhline(0, lw=0.5, color='black')
    plt.axvline(0, lw=0.5, color='black')
    plt.legend()
    plt.show()