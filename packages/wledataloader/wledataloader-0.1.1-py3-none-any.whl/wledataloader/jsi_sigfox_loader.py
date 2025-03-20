from .utils import *
from .base_loader import DataBase

SEED = 42

class JsiSigfoxLoader(DataBase):
    """
    Load JSI_SIGFOX data from csv or raw file in the given directory.
    """
    def __init__(self, seed=SEED, printable=False, rate_list=[0.9, 0.1, 0.0], save_csv=True) -> None:
        """
        Initialize the JSI_SIGFOX loader.
        
        Parameters:
        seed (int): The seed for the random number generator.
        printable (bool): Whether to print the data.
        rate_list (list): The list of rates.
        save_csv (bool): Whether to save the data to a csv file.
        datatype (int): The type of the data.
        """
        self.download_url = 'http://clouds.iec-uit.com/wireless-link-estimation/JSI_SIGFOX.zip'
        self.dataname = 'JSI_SIGFOX'
        super().__init__(seed, printable, rate_list, save_csv)
        self.drop_columns = ['prr']

    def __loadData(self, path_to_data):
        li = []
        for root, _, files in os.walk(path_to_data):
            for filename in natsorted(files):
                if not filename.endswith(".csv"):
                    continue
                df = pd.read_csv(os.path.join(path_to_data, filename), index_col=None, header=0)
                li.append(df)
        return pd.concat(li, axis=0, ignore_index=True)

    def __prepareDatasets(self, path_to_data) -> pd.DataFrame:
        # self._print("================================== Preparing datasets ==================================")
        # self._print("Data dir/path: " + path_to_data)
        df = self.__loadData(path_to_data)

        if len(df) == 0:
            # self._print("=================================== Can not loading data. Exit ===================================")
            return

        df.loc[df['received'] == 0, 'rssi'] = 0

        # self._print("=================================== Adding PRR (packet received ratio) features")
        df = PRR(source='received', window_size=20, ahead=0, target='prr').fit_transform(df)

        # self._print("=================================== Adding rssi_mean, rssi_std and rssi_median features")
        df = SyntheticFeatures(source='rssi', window_size=20).fit_transform(df)

        # self._print('Apply discrete derivation (backward difference)')
        df['drssi'] = df['rssi'].diff()

        # self._print("=================================== Adding quality detection target column")
        df['target'] = df['prr'].apply(self._prrToLabel)

        # self._print("=================================== Clean Data")
        df = df.dropna()
        # self._print("Loaded {} record data".format(len(df)))
        # self._print("================================== End Prepare Data ==================================")

        return df

    def __traceLoadDf_20160916(self, data_dir):
        dfs = []
        for file in os.listdir(data_dir):
            dfs.append(self.__prepareDatasets(os.path.join(data_dir, file)))
        df = pd.concat(dfs, axis=0, ignore_index=True)
        df = df.drop(columns=['attenuator', 'gain', "received"])
        return df

    def __traceLoadDf_20161124(self, data_dir):
        dfs = []
        for file in os.listdir(data_dir):
            dfs.append(self.__prepareDatasets(os.path.join(data_dir, file)))
        df = pd.concat(dfs, axis=0, ignore_index=True)
        df = df.drop(columns=['attenuator', 'pga_gain', 'timestamp', 'seq', "received"])
        return df

    def _traceToLoadDf(self, datadir, tracer=0):
        if tracer == 0:
            data_dir = os.path.join(datadir, "JSI_SIGFOX/JSI_sigfox_20161124")
            df_5 = self.__traceLoadDf_20161124(data_dir)
            data_dir = os.path.join(datadir, "JSI_SIGFOX/JSI_sigfox_20160916")
            df_4 = self.__traceLoadDf_20160916(data_dir)
            self._data_df = pd.concat([df_5, df_4], axis=0, ignore_index=True)
        elif tracer == 1:
            data_dir = os.path.join(datadir, "JSI_SIGFOX/JSI_sigfox_20160916")
            self._data_df = self.__traceLoadDf_20160916(data_dir)
        elif tracer == 2:
            data_dir = os.path.join(datadir, "JSI_SIGFOX/JSI_sigfox_20161124")
            self._data_df = self.__traceLoadDf_20161124(data_dir)