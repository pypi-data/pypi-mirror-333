import os
import tempfile
import pandas as pd
import unittest
from pyfst import read_fst, write_fst

class TestFST(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame
        self.df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': ['x', 'y', 'z', 'p', 'q'],
            'c': [True, False, True, False, True]
        })
        
        # Create a temporary file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, 'test.fst')
        
    def tearDown(self):
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_write_read_fst(self):
        # Write DataFrame to FST file
        write_fst(self.df, self.temp_file)
        
        # Read FST file
        df_read = read_fst(self.temp_file)
        
        # Check if the read DataFrame is equal to the original
        pd.testing.assert_frame_equal(self.df, df_read)
    
    def test_read_columns(self):
        # Write DataFrame to FST file
        write_fst(self.df, self.temp_file)
        
        # Read only 'a' column
        df_read = read_fst(self.temp_file, columns=['a'])
        
        # Check if the read DataFrame has only 'a' column
        self.assertEqual(list(df_read.columns), ['a'])
        pd.testing.assert_series_equal(self.df['a'], df_read['a'])
    
    def test_read_rows(self):
        # Write DataFrame to FST file
        write_fst(self.df, self.temp_file)
        
        # Read only first 2 rows
        df_read = read_fst(self.temp_file, from_=0, to=1)
        
        # Check if the read DataFrame has only first 2 rows
        self.assertEqual(len(df_read), 2)
        pd.testing.assert_frame_equal(self.df.iloc[0:2], df_read)
    
    def test_compress(self):
        # For small test datasets, compression might sometimes not reduce file size
        # or even increase it slightly due to overhead. To make a more reliable test,
        # let's create a larger DataFrame
        import numpy as np
        large_df = pd.DataFrame({
            'a': np.random.randint(0, 100, size=1000),
            'b': np.random.choice(['x', 'y', 'z', 'p', 'q'], size=1000),
            'c': np.random.choice([True, False], size=1000),
            'd': np.random.randn(1000),
            'e': np.random.choice(['foo', 'bar', 'baz'], size=1000)
        })
        
        # Write large DataFrame to FST file with no compression
        write_fst(large_df, self.temp_file, compress=0)
        size_no_compress = os.path.getsize(self.temp_file)
        
        # Write large DataFrame to FST file with max compression
        write_fst(large_df, self.temp_file, compress=100)
        size_max_compress = os.path.getsize(self.temp_file)
        
        print(f"\nNo compression: {size_no_compress} bytes")
        print(f"Max compression: {size_max_compress} bytes")
        
        # Max compression should result in smaller file size
        self.assertLessEqual(size_max_compress, size_no_compress)

if __name__ == '__main__':
    unittest.main()