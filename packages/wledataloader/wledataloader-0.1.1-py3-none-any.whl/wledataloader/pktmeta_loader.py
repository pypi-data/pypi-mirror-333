from .utils import *
from .base_loader import DataBase

SEED = 42

class PktMetaLoader(DataBase):

    def __init__(self, seed=0xDEADBEEF, printable=True, rate_list=[0.9, 0.1, 0.0], save_csv=True) -> None:
        self.download_url = 'http://clouds.iec-uit.com/wireless-link-estimation/Packetmetadata.zip'
        self.dataname = 'Packetmetadata'
        super().__init__(seed, printable, rate_list, save_csv)
        self.drop_columns = ['prr', 'received']

    def __parser(self, filename: str) -> pd.DataFrame:
        list_df = []
        with open(filename, mode='r') as file:
            for line in file:
                row = line.split(',')[:-1]
                assert len(row) >= 9, 'Expected row length at least 9, got {}'.format(len(row))
                row = list(map(int, row))

                data = np.full(shape=(300, 4), fill_value=0, dtype=np.int32)

                for i in range(9, len(row), 9):
                    if row[i + 5] == 0:  # rssi
                        data[row[i] - 1, :] = np.array([0] + row[i + 5:i + 8])
                    else:
                        data[row[i] - 1, :] = np.array([1] + row[i + 5:i + 8])
                df = pd.DataFrame(data, columns=['received', 'rssi', 'noise_floor', 'LQI'])
                df['rssi'] = df['rssi'] - 45

                list_df.append(df)
        return list_df

    def __loadData(self, path_to_data):
        li = []
        for root, _, files in os.walk(path_to_data):
            for filename in natsorted(files):
                dfs = self.__parser(f'{root}/{filename}')
                li = li + dfs
        return li

    def __prepareDatasets(self, path_to_data, drop_frac=0.0) -> pd.DataFrame:
        dfs = []
        # self._print("Data dir/path:" + path_to_data, type="info")

        for df in self.__loadData(path_to_data):
            df.loc[df['received'] == 0, 'rssi'] = np.nan
            dfs.append(df)
        df = dfs
        # self._print("Loaded {} record data".format(len(df)), type="process")
        if len(df) == 0:
            # self._print("Can not loading data. Exit", type="error")
            return None

        # self._print("Replacing Node data by using Interpolation", type="process")
        df = CustomInterpolation(source='rssi', strategy='constant', constant=0).fit_transform(df)

        # self._print("Adding rssi_mean, rssi_median and rssi_std features", type="process")
        df = SyntheticFeatures(source='rssi', window_size=20).fit_transform(df)

        # self._print("Adding PRR (packet received ratio) features", type="process")
        df = PRR(source='received', window_size=20, ahead=1, target='prr').fit_transform(df)

        # self._print('Apply discrete derivation (backward difference)', type="process")
        for i in range(len(df)):
            df[i]['drssi'] = df[i]['rssi'].diff()

        df = CustomMerger().fit_transform(df)

        # self._print("Adding quality detection target column", type="process")

        df['target'] = df['prr'].apply(self._prrToLabel)

        # self._print("Clean Data", type="process")
        df = df.loc[df['received'] != 0]
        df = df.dropna()

        # self._print("Drop {} percentence samples".format(drop_frac * 100), type="process")

        for index in df["target"].value_counts().index:
            df = df.drop(df[df['target'] == index].sample(frac=drop_frac).index)

        return df

    def _traceToLoadDf(self, datadir, drop_frac=0.98):
        data_dir = os.path.join(datadir, self.dataname)
        dfs = []
        dirs = os.listdir(data_dir)
        # self._print("Loading data from: " + os.path.basename(data_dir), type="title")
        for file in dirs:
            dfs.append(self.__prepareDatasets(os.path.join(data_dir, file), drop_frac))
            break
        self._data_df = pd.concat(dfs, axis=0, ignore_index=True)
