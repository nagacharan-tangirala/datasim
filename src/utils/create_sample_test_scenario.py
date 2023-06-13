import pandas as pd

ids = [1, 2, 3, 1, 2, 3, 1, 2, 3]
x = [1000.0, 2000.0, 3000.0, 1000.0, 2000.0, 3000.0, 1000.0, 2000.0, 3000.0]
y = [1000.0, 1000.0, 1000.0, 2000.0, 2000.0, 2000.0, 3000.0, 3000.0, 3000.0]
time = [1000, 1000, 1000, 2000, 2000, 2000, 3000, 3000, 3000]

df = pd.DataFrame({'time': time, 'vehicle_id': ids, 'x': x, 'y': y})

# Save the dataframe to a parquet file
df.to_parquet('/mnt/hdd/workspace/datasim/input/sample/sample.parquet')

# Create a coverage dataframe
neighbours = [[2, 3], [1, 3], [1, 2], [2, 3], [1, 3], [1, 2], [2, 3], [1, 3], [1, 2]]
coverage_df = pd.DataFrame({'time': time, 'vehicle_id': ids, 'neighbours': neighbours})

# Save the coverage dataframe to a parquet file
coverage_df.to_parquet('/mnt/hdd/workspace/datasim/input/sample/sample_coverage.parquet')
