#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

'''
Plots a barchart of mutations at >1% frequency from allele frequencies file
Takes allele frequency file as argument.
Run as 'python visualize.py /path/to/frequency/file'
'''

frq_file = sys.argv[1]
data_df = pd.read_csv(frq_file, sep='\t')

#screw around with df to get it in into seaborn usable format
sites = []
alleles = []
frqs = []
al_type = []

for site,wt,mut in zip(data_df.CHROM, data_df.N_CHR,data_df['{ALLELE:FREQ}']):
	wt_al = wt.split(':')[0]
	wt_fr = wt.split(':')[1]
	mut_al = mut.split(':')[0]
	mut_fr= mut.split(':')[1]
	if float(wt_fr) < 0.99:
		alleles.append(wt_al)
		frqs.append(float(wt_fr))
		al_type.append('WT')
		sites.append(site)
		alleles.append(mut_al)
		frqs.append(float(mut_fr))
		al_type.append('MUT')
		sites.append(site)

p_df = pd.DataFrame({'site':pd.Categorical(sites),
						'allele':pd.Categorical(alleles), 'frq':frqs,
						'Type':pd.Categorical(al_type)}, index=range(0,len(sites)))


ax = sns.barplot(x="site", y="frq", hue="Type", data=p_df)
#plt.figsize=(12,5)
ax.set_ylabel('Frequency')
ax.set_xlabel('Nucleotide Position')
ax.set_title('Nucleotide Sites W/ Mutations at Frequency >1%')
rects = ax.patches

for rect, label in zip(rects, p_df.allele):
	height = rect.get_height()
	ax.text(rect.get_x() + rect.get_width()/2, height, label,
	 			ha='center', va='bottom')

plt.savefig('Mutation Frequency Bar Chart.pdf', format='pdf')
#plt.show()
