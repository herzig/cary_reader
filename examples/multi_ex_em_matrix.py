# allows import of package from parent directory
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cary_reader import CaryData

data = CaryData.from_csv('test_data/547_304_678_961_pm800.csv')
df = data.get_collapsed_df()

# extract dataframe for each single sample
datasets = {
    961: df.iloc[:,0::4], 
    678: df.iloc[:,1::4], 
    304: df.iloc[:,2::4], 
    547: df.iloc[:,3::4]}

# rewrite columns names to excitation wavelengths
for (n,d) in datasets.items():
    d.columns = range(300,601,10)