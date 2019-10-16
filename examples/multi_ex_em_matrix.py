# allows import of package from parent directory
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cary_reader import CaryData

# four samples

data = CaryData.from_csv('test_data/multi_sample_matrix_4s.csv', skiplog=True)
dataframes = data.get_multisample_ex_em_matrix()
# dataframes is now a dictionary of pandas data frames with the sample name as key. Each dataframe is an excitation emission matrix

# some basic tests
assert len(dataframes) == 4
assert all([s.shape == (226,31) for _,s in dataframes.items()]) # all ex-em matrices must have the same shape


# three samples

data = CaryData.from_csv('test_data/multi_sample_matrix_3s.csv', skiplog=True)
dataframes = data.get_multisample_ex_em_matrix()
# dataframes is now a dictionary of pandas data frames with the sample name as key. Each dataframe is an excitation emission matrix

# some basic tests
assert len(dataframes) == 3
assert all([s.shape == (226,31) for _,s in dataframes.items()]) # all ex-em matrices must have the same shape
