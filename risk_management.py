import itertools
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

global debug
global plot

# Import data from csv
def import_data(filename):
    data = pd.read_csv(filename)
    risks = data[['Reference', 'Likelihood', 'Impact']]
    return risks.values.tolist()

# Export (save) to csv
def export_data(filename, data):
    df = pd.DataFrame(data) 
    df.to_csv(filename) 

# Get all the possible risk cobinations
def get_all_combinations(all_risks):
    
    all_comb = []
    
    for r in range(0, len(all_risks) + 1):
        sol = itertools.combinations(all_risks, r)
        
        for it in sol:
            all_comb.append(it)
    
    return all_comb

# Get Probability (P) & Impact (I) of each combination
def calculate_PI_combinations(all_risks, all_comb):
    
    all_comb_with_PI = []

    for comb_id in range(len(all_comb)):
        comb = all_comb[comb_id]
        pocc_total = 1 # Total Probability
        iocc_total = 0 # Total Impact

        # Risk in the combination (occure)
        for risk in comb:
            pocc_total *= risk[1]
            iocc_total += risk[2]

        # Risk NOT in the combination (do not occure)
        for risk in all_risks:
            if risk not in comb:
                pocc_total *= 1 - risk[1]

        # Get combination name
        comb_name = "" 
        for i in comb:
            comb_name += i[0] + "-"

        # Save values
        all_comb_with_PI.append((iocc_total, pocc_total, comb_id, comb_name)) # IMPACT, PROBABILITY, ID
    
    return all_comb_with_PI

# Create risk curve profile
def create_risk_curve_profile(all_comb_with_PI):

    # Order based on Impact + NUMPY Array
    ord_acc_comb_with_PI = sorted(all_comb_with_PI)
    ord_acc_comb_with_PI = np.array(ord_acc_comb_with_PI, dtype=[('iocc_total', np.float64), ('pocc_total', np.float64), ('comb_id', np.float64), ('comb_name', np.unicode_, 16)])
    pprint(ord_acc_comb_with_PI)

    # Accumulate Probability
    acc_p = 0
    for i in range(len(ord_acc_comb_with_PI)):
        acc_p += ord_acc_comb_with_PI[i]["pocc_total"]
        ord_acc_comb_with_PI[i]["pocc_total"] = acc_p

    # DEBUG & PLOT
    if debug:
        pprint(all_risks)
        pprint(all_comb)
        pprint(all_comb_with_PI)

    if plot: 
        plt.plot(ord_acc_comb_with_PI[:]["iocc_total"], ord_acc_comb_with_PI[:]["pocc_total"])
        plt.show()

    return ord_acc_comb_with_PI

# MAIN
if __name__ == "__main__":
    
    debug = False
    plot = True

    # all_risks = [("1.1", 0.232, 100000), ("1.2", 0.0323, 1000000), ("2.3", 0.063, 50000), ("5.1", 0.0432, 1000), ("7.1", 0.023, 400000)]
    all_risks = import_data("data_post.csv")
    if debug:
        pprint(all_risks)

    # RUN
    all_comb = get_all_combinations(all_risks)
    all_comb_with_PI = calculate_PI_combinations(all_risks, all_comb)
    ord_acc_comb_with_PI = create_risk_curve_profile(all_comb_with_PI)

    # EXPORT - SAVE
    # export_data("export_2.csv", ord_acc_comb_with_PI)