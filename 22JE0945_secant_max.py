import time
import numpy as np
from tkinter import * #type:ignore
import matplotlib.pyplot as plt

def initialize() -> None:
    global epsilon, x_lower, x_upper, x_coeff, x_power
    epsilon = 4
    x_lower = -8
    x_upper = -96
    x_coeff = [1]
    x_power = [2]
    GUI_helper()
    solver() 
    return

def submit():
    global epsilon, x_lower, x_upper
    global x_coeff,x_power
    epsilon = float(epsilonField.get())
    x_lower = float(xLowerField.get())
    x_upper = float(xUpperField.get())
    x_coeff,x_power = [],[]
    for input in coeff_entries:
        x_coeff.append(float(input.get()))
    for input in xPower_entries:
        x_power.append(float(input.get()))
    root.destroy()

def clear():
    currentEntry = root.focus_get()
    if isinstance(currentEntry, Entry):
        currentEntry.delete(0, END)

def developer():
    dev_window = Toplevel(root)
    dev_window.title("Developer Info")
    Label(dev_window, text="Developed by: Shyam Sunder❤️", font=("Consolas", 12)).pack(padx=20, pady=10)
    Label(dev_window, text="Roll Number: 22JE0945", font=("Consolas", 12)).pack(padx=20, pady=10)
    Button(dev_window, text="Close", command=dev_window.destroy).pack(pady=10)

def add_term():
    row = len(coeff_entries) + 2  # Dynamically set row
    coeff_entry = Entry(root, width=10, borderwidth=5)
    coeff_entry.grid(row=row, column=0, padx=5, pady=5)
    coeff_entries.append(coeff_entry)
    
    xPower_entry = Entry(root, width=10, borderwidth=5)
    xPower_entry.grid(row=row, column=1, padx=5, pady=5)
    xPower_entries.append(xPower_entry)

def GUI_helper():
    global root, coeff_entries, xPower_entries, xLowerField, xUpperField, epsilonField
    global coeff_entries,xPower_entries
    root = Tk()
    root.title("Secant Method Maximizer")
    coeff_entries = []
    xPower_entries = []
    Label(root, text="22JE0945_Secant_Max", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=5, pady=10)
    Label(root, text="Coefficient of x", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
    Label(root, text="Power of x", font=("Arial", 10, "bold")).grid(row=1, column=1, padx=5, pady=5)
    Label(root, text="Other Fields", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=5, pady=5)
    add_term()
    Label(root, text="Lower X Bound:", font=("Arial", 10)).grid(row=2, column=2, padx=5, pady=5)
    xLowerField = Entry(root, width=10, borderwidth=5)
    xLowerField.grid(row=2, column=3, padx=5, pady=5)
    Label(root, text="Upper X Bound:", font=("Arial", 10)).grid(row=3, column=2, padx=5, pady=5)
    xUpperField = Entry(root, width=10, borderwidth=5)
    xUpperField.grid(row=3, column=3, padx=5, pady=5)
    Label(root, text="Epsilon (Error Tolerance):", font=("Arial", 10)).grid(row=4, column=2, padx=5, pady=5)
    epsilonField = Entry(root, width=10, borderwidth=5)
    epsilonField.grid(row=4, column=3, padx=5, pady=5)
    Button(root, text="Add Term", padx=20, pady=10, command=add_term).grid(row=2, column=4, pady=5)
    Button(root, text="Clear", padx=20, pady=10, command=clear).grid(row=3, column=4, pady=5)
    Button(root, text="Developer", padx=20, pady=10, command=developer).grid(row=4, column=4, pady=5)
    Button(root, text="Submit", padx=20, pady=10, command=submit).grid(row=5, column=4, pady=5)
    root.mainloop()

def f_val(x) -> float :
    val = 0
    for coeff,power in zip(x_coeff,x_power):
        val += (coeff*(x**power))
    return val

def plot(i: int, L, R, Z):
    fig, axes = plt.subplots(2, 1)
    step = 0.005
    x_val = np.arange(L, R, step)
    f_vec = np.array([f_val(x) for x in x_val])
    f_prime_vec = np.array([f_prime(x) for x in x_val])
    mask = np.isfinite(f_vec) & np.isfinite(f_prime_vec)  # Ensures no NaN or inf values
    axes[0].plot(x_val[mask], f_vec[mask], color='blue')
    if np.isfinite(f_val(Z)):  # Check if Z's function value is finite
        axes[0].scatter(Z, f_val(Z), color='red', s=50, label="z")
    axes[0].set_title(f"\nf(x) Graph")
    axes[0].set_xlabel("x values →")
    axes[0].set_ylabel("f(x) →")
    axes[1].plot(x_val[mask], f_prime_vec[mask], color='brown')
    if np.isfinite(f_prime(Z)):  # Check if Z's derivative value is finite
        axes[1].scatter(Z, f_prime(Z), color='red', s=50, label="z")
    axes[1].set_title("f'(x) Graph")
    axes[1].set_xlabel("x values →")
    axes[1].set_ylabel("f'(x) →")
    axes[0].grid(True)
    axes[1].grid(True)
    axes[0].legend()
    axes[1].legend()
    plt.tight_layout()
    fig.suptitle(f"Iteration {i}")
    fig.savefig(f"iteration_{i}.png")
    plt.show(block=False)
    plt.close()

def solver():
    i = 0
    L = x_lower
    R = x_upper
    z_vals, l_vals, r_vals, z_prime_vals, z_f_val=  [], [], [], [], []
    while(i<100): # maximum 100 iterations allowed
        result = termination_check(L,R)
        l_vals.append(L)
        r_vals.append(R)
        z_vals.append(result[0])
        z_f_val.append(result[1])
        z_prime_vals.append(result[2])
        plot(i,L,R,result[0])
        if(result[3]==False):
            break
        else:
            if(result[2]>0):
                L = result[0]
            else:
                R = result[0]
        i+=1
    for iter in range(0, i + 1, 1):
        remark = "Continue"
        if iter == i:
            remark = "Stop"
        print(f"{iter:<5}    {l_vals[iter]:<10.5f} {r_vals[iter]   :<10.5f} {z_vals[iter]:<10.5f} {z_f_val[iter]:<10.5f} {z_prime_vals[iter]:<10.5f} {remark}")
        file.write(f"{iter:<5}    {l_vals[iter]:<10.5f} {r_vals[iter]   :<10.5f} {z_vals[iter]:<10.5f} {z_f_val[iter]:<10.5f} {z_prime_vals[iter]:<10.5f} {remark}\n")
    return None
    

def f_prime(x) -> float:
    # will use central difference approximation method to find derivative
    delta = 0.00001
    f1 = f_val(x-delta)
    f2 = f_val(x+delta)
    f_prime_x = (f2-f1)/(2.0*delta)
    return f_prime_x

def z_val(L, R) -> float:
    z = R
    f_prime_L = f_prime(L)
    f_prime_R = f_prime(R)
    temp = (f_prime_R*(R-L)) / (f_prime_R-f_prime_L)
    z -= temp
    return z

def termination_check(L, R) -> tuple[float, float, float, bool]:
    Z = z_val(L,R)
    f_prime_z = f_prime(Z)
    f_val_z = f_val(Z)
    another_iter = False
    if(abs(f_prime_z)>epsilon):
        another_iter = True
    return (Z,f_val_z,f_prime_z,another_iter)



if __name__ == "__main__":
    ## file handling -- to make sure the result is saved in some file :)
    global file 
    file = open("22JE0945_secant_max_output.txt","w")
    print(f"{'Iteration':<10} {'L':<10} {'R':<10} {'Z':<10} {'f(Z)':<10} {'f\'(Z)':<10} {'Remark'}")
    file.write(f"{'Iteration':<10}    {'L':<10} {'R':<10}     {'Z':<10}     {'f(Z)':<10}          {'f\'(Z)':<10} {'Remark'}\n")
    initialize()
    file.close()