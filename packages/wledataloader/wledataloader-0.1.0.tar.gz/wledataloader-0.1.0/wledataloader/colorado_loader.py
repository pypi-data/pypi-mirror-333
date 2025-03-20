from .utils import *
from .base_loader import DataBase

class CuRow:
    """
    CuRow class for parsing data from the Colorado dataset.
    """
    def __init__(self, line):
        fi = line.split()
        self.x = float(fi[0])
        self.y = float(fi[1])
        self.dev = fi[2]
        self.ant = fi[3]
        self.pw = int(fi[4])
        self.seq = int(fi[5])
        self.rssi = [float(x) for x in fi[6:]]

class ColoradoLoader(DataBase):
    """
    ColoradoLoader class for loading and processing data from the Colorado dataset.
    Inherits from the DataBase class.
    """

    def __init__(self, seed=0xDEADBEEF, printable=True, rate_list=[0.9, 0.8, 0.7, 0.6, 0.5, 0.0], save_csv=True, rssi_process_type=1) -> None:
        """
        Initialize the ColoradoLoader class.

        Parameters:
        - seed: Random seed for reproducibility.
        - printable: Boolean flag to enable/disable printing.
        - rate_list: List of rates for PRR to label conversion.
        - save_csv: Boolean flag to enable/disable saving data to CSV.
        - rssi_process_type: Type of RSSI processing to apply.
            With Value = 0:
                Retains individual RSSI measurements.
                Results in a more detailed dataset with multiple rows per packet.
                Useful for detailed analysis where individual RSSI values are important.
            With Value = 1:
                Averages the RSSI measurements.
                Results in a simplified dataset with one row per packet.
                Useful for general analysis where the average RSSI value is sufficient.
        """
        self.download_url = 'http://clouds.iec-uit.com/wireless-link-estimation/Colorado.zip'
        self.dataname = 'Colorado'
        super().__init__(seed, printable, rate_list, save_csv)
        self.rssi_process_type = rssi_process_type
        self.drop_columns = ['file_name', 'x_coordinate', 'y_coordinate', 'device_name', 'direction', 'received', 'seq', 'prr']
  
    def __loadData(self, path_to_file):
        """
        Load data from the given file.
        
        Parameters:
        - path_to_file: Path to the file to load.
        
        Returns:
        - List of DataFrames containing the loaded data.
        """
        packets_in_link = {}
        filename = path_to_file.split('/')[-1]
        # self._print("================================== Load file " + filename)
        cnt = 0

        with open(os.path.join(path_to_file)) as f:
            while True:
                cnt += 1
                line = f.readline()
                if not line:
                    break
                line = CuRow(line)
                id = (filename, line.x, line.y, line.dev, line.ant, line.pw)
                if id in packets_in_link:
                    packets_in_link[id].append((id, line.seq, line.rssi))
                else:
                    packets_in_link[id] = [(id, line.seq, line.rssi)]

        for link_id in packets_in_link.keys():
            packets_in_link[link_id].sort(key=lambda x: x[1])

        # self._print("Total unique link_id: " + str(len(packets_in_link.keys())))
        # self._print("Total line: " + str(cnt))

        list_df = []
        col_names = ['file_name', 'x_coordinate', 'y_coordinate', 'device_name', 'direction', 'tx_pow', 'rssi', 'received', 'seq']
        for link_id in packets_in_link.keys():
            recv_rssi = [[], [], [], [], []]
            last_seq = 0
            pkts = packets_in_link[link_id]
            for pkt in pkts:
                info = [x for x in pkt[0]]
                seq = pkt[1]
                rssi = pkt[2]

                if self.rssi_process_type == 0:
                    for i in range(last_seq, seq):
                        for k in range(0, 5):
                            recv_rssi[k].append(info + [0, False, i])
                    for i in range(0, 5):
                        recv_rssi[i].append(info + [rssi[i], True, seq])

                if self.rssi_process_type == 1:
                    for i in range(last_seq, seq):
                        recv_rssi[0].append(info + [0, False, i])
                    recv_rssi[0].append(info + [np.mean(rssi), True, seq])

                last_seq = seq + 1

            if self.rssi_process_type == 0:
                for i in range(0, 5):
                    list_df.append(pd.DataFrame(recv_rssi[i], columns=col_names))
            if self.rssi_process_type == 1:
                list_df.append(pd.DataFrame(recv_rssi[0], columns=col_names))

        return list_df

    def __prepareDatasets(self, path_to_data) -> pd.DataFrame:
        """
        Prepare datasets from the given data path.

        Parameters:
        - path_to_data: Path to the data to prepare.

        Returns:
        - Prepared DataFrame containing the data.
        """
        # self._print("================================== Preparing datasets ==================================")
        # self._print("Data dir/path:" + path_to_data)

        dfs = self.__loadData(path_to_data)

        if len(dfs) == 0:
            # self._print("================================== Can not loading data. Exit ==================================")
            return None

        # self._print("================================== Adding PRR (packet received ratio) features")
        dfs = PRR(source='received', window_size=20, ahead=0, target='prr').fit_transform(dfs)

        # self._print("================================== Adding rssi_mean, rssi_median and rssi_std features")
        dfs = SyntheticFeatures(source='rssi', window_size=20).fit_transform(dfs)

        dfs = CustomMerger().fit_transform(dfs)

        # self._print('Apply discrete derivation (backward difference)')
        dfs['drssi'] = dfs['rssi'].diff()

        # self._print("================================== Adding quality detection target column")
        dfs['target'] = dfs['prr'].apply(self._prrToLabel)

        # self._print("=================================== Clean Data")
        dfs = dfs.dropna()
        # self._print("Loaded {} record data".format(len(dfs)))

        # self._print("================================== End Prepare Data ==================================")

        return dfs

    def _traceToLoadDf(self, datadir):
        """
        Load data from the given directory.

        Parameters:
        - data_dir: Directory to load data from.

        Returns:
        - DataFrame containing the loaded data.
        """
        data_dir = os.path.join(datadir, self.dataname, "data")
        dfs = []
        for root, _, files in os.walk(data_dir):
            for file in files:
                dfs.append(self.__prepareDatasets(os.path.join(root, file)))

        self._data_df = pd.concat(dfs, axis=0, ignore_index=True)