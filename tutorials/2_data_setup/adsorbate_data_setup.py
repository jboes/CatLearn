"""Script to show fingerprint generators."""
import numpy as np
import ase.io
from atoml.fingerprint.setup import return_fpv, get_combined_descriptors
from atoml.fingerprint import AdsorbateFingerprintGenerator
from atoml.fingerprint.db2thermo import slab_index, info2primary_index
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    plot = True
except ImportError:
    print('Pandas and seaborn modules are needed for this tutorial.')

# Data in the form of a dictionary
dictionary = {'Ag': {'E': 1.44, 'ads_index': [30, 31, 32, 33]},
              'Au': {'E': 1.16, 'ads_index': [30, 31, 32, 33]},
              'Cu': {'E': 1.11, 'ads_index': [30, 31, 32, 33]}}

# We first create a list of atoms objects from a simple dataset.
structures = []
targets = []
for f in dictionary.keys():
    # Loading the atoms objects from traj files.
    atoms = ase.io.read(f + '.traj')
    # Attach indices of adsorbate atoms to the info dict in the key 'add_atoms'
    atoms.info['ads_atoms'] = dictionary[f]['ads_index']
    # Get other information about the surface/adsorbate nearest neighbors.
    atoms.info['surf_atoms'] = slab_index(atoms)
    i_add1, i_surf1, Z_add1, Z_surf1, i_surfnn = info2primary_index(atoms)
    atoms.info['i_add1'] = i_add1
    atoms.info['i_surf1'] = i_surf1
    atoms.info['Z_add1'] = Z_add1
    atoms.info['Z_surf1'] = Z_surf1
    atoms.info['i_surfnn'] = i_surfnn
    # Append atoms objects to a list.
    structures.append(atoms)
    targets.append(dictionary[f]['E'])

# Get the fingerprint generator.
fingerprint_generator = AdsorbateFingerprintGenerator()

# List of functions to call.
feature_functions = [fingerprint_generator.primary_surfatom,
                     fingerprint_generator.primary_adds_nn]
# There are many more available.

# Get a list of names of the features.
feature_names = get_combined_descriptors(feature_functions)

# Generate the data
training_data = return_fpv(structures, feature_functions, use_prior=False)

for l in range(len(feature_names)):
    print(l, feature_names[l])

# Select some features to plot.
selection = [13, 14]

# Plot selected of the feature distributions.
data = {}
traint = np.transpose(training_data[:, selection])
for i, j in zip(traint, selection):
    data[j] = i
df = pd.DataFrame(data)
fig = plt.figure(figsize=(20, 10))
ax = sns.violinplot(data=df, inner=None)
plt.title('Feature distributions')
plt.xlabel('Feature No.')
plt.ylabel('Distribution.')

string = 'Plotting:'
for s in selection:
    string += '\n' + feature_names[s]
print(string)
plt.show()