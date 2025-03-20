from .utils import *
from collections import OrderedDict
import pathlib
from .base_loader import DataBase
from pathlib import Path

class RutgersLoader(DataBase):
    def __init__(self, seed=0xDEADBEEF, printable=True, rate_list=[0.9, 0.8, 0.7, 0.6, 0.5, 0.0], save_csv=True) -> None:
        self.download_url = 'http://clouds.iec-uit.com/wireless-link-estimation/Rutgers.zip'
        self.dataname = 'Rutgers'
        super().__init__(seed, printable, rate_list, save_csv)
        self.drop_columns = ['error','seq',"src",'dst','prr','received']

    def __parser(self, filename: str) -> pd.DataFrame:
        filename = str(pathlib.PurePosixPath(Path(filename)))
        noise = np.int8(filename.split('/')[-3][len('dbm'):])
        tx = filename.split('/')[-2].split('_')[1]
        rx = 'node' + filename.split('/')[-1][len('sdec'):]

        rssi = np.full(shape=300, fill_value=0, dtype=np.uint8)
        received = np.full(shape=300, fill_value=False, dtype=bool)
        error = np.full(shape=300, fill_value=False, dtype=bool)

        with open(filename, mode='r') as file:
            for line in file:
                row = line.split()
                assert len(row) == 2, 'Expected row length 2, got {}'.format(len(row))
                seq, value = int(row[0]), np.uint8(row[1])
                if seq < 300:
                    if value < 128 and value >= 0:
                        rssi[seq] = value
                        received[seq] = True
                    else:
                        error[seq] = True

        df = pd.DataFrame(data={'rssi': rssi, 'received': received, 'error': error})
        df['seq'] = df.index + 1
        df['noise'] = noise
        df['src'] = tx
        df['dst'] = rx

        dtypes = OrderedDict([
            ('seq', np.uint16),
            ('src', str),
            ('dst', str),
            ('noise', np.int8),
            ('received', bool),
            ('error', bool),
            ('rssi', np.uint8),
        ])
        df = df.astype(dtypes)
        return df

    def __load_data(self, PATH_TO_DATA):
        li = []
        for root, _, files in os.walk(PATH_TO_DATA):
            for filename in natsorted(files):
                df = self.__parser(f'{root}/{filename}')
                li.append(df)
        return li

    def __prepare_datasets(self, PATH_TO_DATA) -> pd.DataFrame:
        dfs = []
        # # self._print("================================== Preparing datasets ==================================")
        # # self._print("Data dir/path:" + PATH_TO_DATA)

        for df in self.__load_data(PATH_TO_DATA):
            df.loc[df['received'] == 0, 'rssi'] = np.nan
            dfs.append(df)
        df = dfs
        # # self._print("Loaded {} record data".format(len(df)))
        if len(df) == 0:
            # # self._print("================================== Can not loading data. Exit ==================================")
            return None

        # # self._print("================================== Replacing Node data by using Interpolation")
        df = CustomInterpolation(source='rssi', strategy='constant', constant=0).fit_transform(df)

        # # self._print("================================== Adding rssi_mean, rssi_median and rssi_std features")
        df = SyntheticFeatures(source='rssi', window_size=20).fit_transform(df)

        # # self._print("================================== Adding PRR (packet received ratio) features")
        df = PRR(source='received', window_size=20, ahead=1, target='prr').fit_transform(df)

        # # self._print('================================== Apply discrete derivation (backward difference)')
        for i in range(len(df)):
            df[i]['drssi'] = df[i]['rssi'].diff()

        df = CustomMerger().fit_transform(df)
        # # self._print("================================== Adding quality detection target column")
        df['target'] = df['prr'].apply(self._prrToLabel)

        # # self._print("=================================== Clean Data")
        df = df.dropna()

        # # self._print("Loaded {} record data".format(len(df)))
        # # self._print("================================== End Prepare Data ==================================")
        return df

    def _traceToLoadDf(self, datadir):
        data_dir = os.path.join(datadir, self.dataname, "data")
        dfs = []
        dirs = os.listdir(data_dir)
        for file in dirs:
            dfs.append(self.__prepare_datasets(os.path.join(data_dir, file)))
        self._data_df = pd.concat(dfs, axis=0, ignore_index=True)


    