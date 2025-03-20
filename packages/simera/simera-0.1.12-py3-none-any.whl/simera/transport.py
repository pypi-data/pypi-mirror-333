from pathlib import Path

import numpy as np
import pandas as pd


class TransportRatesheet:
    def __init__(self, file, worksheet):
        self.source = self._Source(file, worksheet)
        self.meta = self._Meta(self)

    class _Source:
        def __init__(self, file, worksheet):
            self.file = file
            self.worksheet = worksheet
            self.data_raw = self.read_worksheet()
            self.data_meta = self.get_meta_data()
            self.data_lane = self.get_lane_data()

        def __repr__(self):
            return f"Source(file='{self.file.parts[-1]}', worksheet='{self.worksheet}')"

        def read_worksheet(self):
            """Read ratesheet all raw data"""
            dtypes = {'<dest_ctry>': 'str', '<dest_zip>': 'str', '<dest_zone>': 'str', '<dest_leadtime>': np.float64}
            return pd.read_excel(io=self.file, sheet_name=self.worksheet, dtype=dtypes, engine='calamine').dropna(
                how='all')

        def get_meta_data(self):
            # Get clean rawdata for meta
            df = self.data_raw[['<meta>', '<meta_value>']].dropna(how='all', ignore_index=True)
            df.columns = df.columns.str.replace(r'[<>]', '', regex=True)
            df['meta'] = df['meta'].astype('str')
            return df

        def get_lane_data(self):
            df = self.data_raw[['<dest_ctry>', '<dest_zip>', '<dest_zone>', '<transit_time>']].dropna(how='all',
                                                                                                      ignore_index=True)
            return df

    class _Meta:
        def __init__(self, transport_ratesheet_instance):
            self._outer = transport_ratesheet_instance
            self.load_ratesheet_meta_attributes()
            self.set_final_ratesheet_meta_attributes()

        def __repr__(self):
            return f"Meta(file='{self._outer.source.file.parts[-1]}', worksheet='{self._outer.source.worksheet}')"

        def load_ratesheet_meta_attributes(self):
            """Convert <meta> and <meta_value> columns of ratesheet and sets all <group_name> as meta attribute.
            Meat and meta_value is converted to dict.
            Example: <source> url, file.xlsx it set as Ratesheet.meta.source. {'url': 'file.xlsx'}"""

            # Get rawdata for meta
            df = self._outer.source.data_meta

            # Set all <groups> as meta attributes
            df_meta = df[df['meta'].str.contains('<.+>', regex=True)].copy()
            df_meta['idx_from'] = df_meta.index + 1
            df_meta['idx_to'] = (df_meta.idx_from.shift(-1) - 2).fillna(df.shape[0] - 1).astype(int)
            df_meta['meta_value'] = df_meta['meta'].str.replace(r'[<>]', '', regex=True)
            for _, row in df_meta.iterrows():
                attr_dict = df[row.idx_from:row.idx_to + 1].set_index('meta')['meta_value'].to_dict()
                setattr(self, row.meta_value, attr_dict)

        # def set_final_ratesheet_meta_attributes(self):
        #     """Convert initial ratesheet meta attributes to fixed and clean input."""
        #     def get_or_default(attribute, value, default_value=None):
        #         x = getattr(self, attribute).get(value)
        #         if x is None:
        #             x =
        #
        #     # Source
        #     self.source['type'] = self.source.get('type', 'downstream_standard')
        #     self.source['test'] = get_or_default('source', 'test')


if __name__ == '__main__':
    test_dir = Path(r'C:\Users\plr03474\NoOneDrive\Python\SimeraProject\simera_resources\transport')
    test_rs = 'TransportRatesheetTemplate_v0.4.1.xlsb'
    test_file = test_dir / test_rs
    test_worksheet = "_0.4.1"
    test_rs_config = 1  # TODO: Consider using a more descriptive name

    rs = TransportRatesheet(test_file, test_worksheet)

    # todo use yaml to structure: default ratesheet input; use last chatgpt message to make it perfect
    #  in this file only some should go to yaml -> max shipment size (company specific), rest max_range - keep in code
    # todo - currency - set in ratesheet as fix and if not set, get from config file
