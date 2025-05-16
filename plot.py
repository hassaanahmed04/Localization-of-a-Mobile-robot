import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt

r_values = [1/64, 1/16, 1/4, 4, 16, 64]
trials = 10
filter_type = 'pf'  # or 'pf'

mean_position_errors = []
mean_mahalanobis_errors = []
anees_values = []

def run_trial(data_factor, filter_factor):
    cmd = [
        'python', 'localization.py',
        filter_type,
        '--data-factor', str(data_factor),
        '--filter-factor', str(filter_factor)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout

    # Extract values
    match_position = re.search(r'Mean position error:\s*([0-9.]+)', output)
    match_mahal = re.search(r'Mean Mahalanobis error:\s*([0-9.]+)', output)
    match_anees = re.search(r'ANEES:\s*([0-9.]+)', output)

    if match_position and match_mahal and match_anees:
        pos = float(match_position.group(1))
        mahal = float(match_mahal.group(1))
        anees = float(match_anees.group(1))
        return pos, mahal, anees
    else:
        print("Warning: Failed to parse output.")
        print(output)
        return None, None, None

for r in r_values:
    pos_errors = []
    mahal_errors = []
    anees_list = []

    for _ in range(trials):
        pos, mahal, anees = run_trial(1.0, r)
        if pos is not None:
            pos_errors.append(pos)
            mahal_errors.append(mahal)
            anees_list.append(anees)

    mean_position_errors.append(np.mean(pos_errors))
    mean_mahalanobis_errors.append(np.mean(mahal_errors))
    anees_values.append(np.mean(anees_list))

    print(f"r = {r} => Avg Pos: {mean_position_errors[-1]}, "
          f"Mahalanobis: {mean_mahalanobis_errors[-1]}, ANEES: {anees_values[-1]}")

# Subplotting
fig, axs = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

axs[0].plot(r_values, mean_position_errors, 'o-', color='blue')
axs[0].set_ylabel('Mean Position Error')
axs[0].grid(True)

axs[1].plot(r_values, mean_mahalanobis_errors, 's-', color='green')
axs[1].set_ylabel('Mean Mahalanobis Error')
axs[1].grid(True)

axs[2].plot(r_values, anees_values, 'x-', color='red')
axs[2].set_ylabel('ANEES')
axs[2].set_xlabel('r (Scaling Factor)')
axs[2].grid(True)

plt.xscale('log')
fig.suptitle(f'{filter_type.upper()} Filter Performance vs Noise Scaling')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

