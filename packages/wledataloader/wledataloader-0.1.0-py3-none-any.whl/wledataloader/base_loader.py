from .utils import *
import appdirs
class DataBase:
    """
    Base class for loading and processing data.
    """
    def __init__(self, seed=0xDEADBEEF, printable=True, rate_list=[0.9, 0.1, 0.0], save_csv=True, CACHE_DIR = appdirs.user_cache_dir("wledataloader")) -> None:
        """
        Initialize the DataBase class.
        
        "Parameters:
        - seed: Random seed for reproducibility. Default is 0xDEADBEEF.
        - printable: Boolean flag to enable/disable printing. Default is True.
        - rate_list: List of rates for PRR to label conversion. Example: [0.9, 0.1, 0.0]
        - save_csv: Boolean flag to enable/disable saving data to CSV.
        - CACHE_DIR: Cache directory for storing data (Optional). Default is user cache directory at .cache/wledataloader.
        """
        np.random.seed(seed)
        np.set_printoptions(suppress=True)
        self._printable = printable
        self.__rate_list = rate_list
        self._save_csv = save_csv
        self._data_df = pd.DataFrame()
        os.makedirs(CACHE_DIR, exist_ok=True)
        self._defaut_datadir = os.path.join(CACHE_DIR, "trace-set")
        os.makedirs(self._defaut_datadir, exist_ok=True)
        self._defaut_csvdir = os.path.join(CACHE_DIR, "storage-csv")
        os.makedirs(self._defaut_csvdir, exist_ok=True)
        self.drop_columns = ['prr']
        
    def _print(self, message, type = None):
        """
        Print the given message if the printable flag is set.
        
        Parameters:
        - message: Message to print.
        
        Returns:
        - None
        """
        if self._printable:
            if type == 'info':
                print(f"[+] {message}")
            elif type == 'error':
                print(f"[!] {message}")
            elif type == "title":
                message = message.upper()
                print(f"\n"+"="*(22+len(message)))
                print(f"========== {message} ==========")
            elif type == "process":
                print(f"--> {message}")
            else:
                print(f"{message}")
    
    def _traceToLoadDf(self, path_to_data):
        """
        Load the data from the given path. The function is implemented in the child class.
        return
        """
    
    def _prrToLabel(self, prr: float) -> int:
        """
        Convert the given PRR to a label based on the rate list.
        
        Parameters:
        - prr: Packet received ratio.
        
        Returns:
        - Label based on the rate list.
        """
        for bot_rate in self.__rate_list:
            if prr >= bot_rate:
                return self.__rate_list.index(bot_rate)
        return -1

    def RemoveClass(self, class_list):
        """ 
        Remove class from the dataset.
        
        Parameters:
        - class_list: List of classes to remove.
        """
        self._print("================== Remove class =================")
        self._data_df = self._data_df[~self._data_df['target'].isin(class_list)]
        self._print("=============== Done Remove class ===============")

    def AddPolyFeatures(self, include=['rssi', 'rssi_mean', 'rssi_std', 'rssi_median'], degree=4, include_bias=True):
        """
        Add more features to the dataset with polynomial features method.

        Parameters:
        - include: List of columns to include.
        - degree: Degree of the polynomial features.
        - include_bias: Include bias or not.
        """

        self._print("Add more features with polynomial features method", type='title')
        self._print("Drop useless features, drop lines with NaN", type='process')
        self._data_df = self._data_df.dropna()
        self._print("Apply Polynomials", type='process')
        self._data_df = Poly_features(self._data_df, include=include, degree=degree, include_bias=include_bias)
        self._print("Finish Apply Polynomials", type='process')
        self._data_df.dropna(inplace=True)
        self._data_df.drop(columns=['1'], inplace=True)

    def ReloadData(self, datadir):
        """
        Reload the data from the given path.
        
        Parameters:
        - path_to_data: Path to the data.
        
        Returns:
        - None
        """
        datapath = os.path.join(self._defaut_csvdir, f"{self.dataname}.csv")
        if os.path.exists(datapath):
            self._data_df = pd.read_csv(datapath, index_col=False, header=0)
            self._print("[-] Reloaded Data from: " + datapath)
            return True
        else:
            self._print("[!] File Data not found at: " + datapath)
            self._data_df = None
        return False
    
    def SaveData(self, datadir):
        """
        Save the data to the given path.
        
        Parameters:
        - path_to_data: Path to the data.
        
        Returns:
        - None
        """
        datapath = os.path.join(self._defaut_csvdir, f"{self.dataname}.csv")
        if not os.path.exists(datapath) and self._save_csv:
            self._print("[-] Saving data to: " + datapath)
            self._data_df.to_csv(datapath, index=False)
            return True
        else:
            self._print("[!] Skip save to csv file: " + datapath)
        
        return False
        
    def PrepareData(self, datadir=None, reload=True, extend_feature=True):
        """
        Prepare data from the given directory.
        
        Parameters:
        - datadir: Directory to load data from.
        - load_type: Type of data to load (raw or csv).
        - reload: Boolean flag to reload data.
        - extend_feature: Boolean flag to extend features.
        
        Returns:
        - Prepared DataFrame containing the data.
        """
        if datadir is None:
            datadir = self._defaut_datadir
            
        if reload:
            if self.ReloadData(datadir):
                return self._data_df

        if os.path.exists(os.path.join(datadir, self.dataname)):
            self._print("[-] Data already exists in: " + os.path.join(datadir, self.dataname))
        else:
            download_and_extract(self.download_url, datadir)

        self._traceToLoadDf(datadir)

        if extend_feature:
            self.AddPolyFeatures()
        if self._save_csv:
            self.SaveData(datadir)

        return self._data_df
    
    def TrainTestSplit(self, test_size=0.2):
        """
        Split the data into training and testing sets.
        
        Parameters:
        - test_size: Size of the testing set.
        - drop_columns: Columns to drop.
        
        Returns:
        - Training and testing sets. X_train, X_test, y_train, y_test 
        """
        print("===============   Begin Split File   ===============")
        df = self._data_df.drop(columns=self.drop_columns)
        X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['target']).to_numpy(copy=True), df['target'].to_numpy(copy=True), test_size=test_size, random_state=42)
        print("Training data shape:", X_train.shape, y_train.shape)
        print("Testing data shape:", X_test.shape, y_test.shape)
        print("Label Train count:")
        unique = np.bincount(y_train)
        print(np.asarray((unique)))
        print("Label Test count:")
        unique = np.bincount(y_test)
        print(np.asarray((unique)))
        print("===============    Split File End   ===============")
        return X_train, X_test, y_train, y_test

    def GetXY(self):
        """
        Get the data and labels.
        
        Returns:
        - Data and labels.
        """
        df = self._data_df.drop(columns=self.drop_columns)
        X = df.drop(columns=['target']).to_numpy(copy=True)
        y = df['target'].to_numpy(copy=True)
        return X, y

    def ShowBasicAnalysis(self):
        """
        Show basic analysis of the data.
        
        Returns:
        - None
        """
        print("=============== Show basic analysis ===============")
        if len(self._data_df.columns) < 10:
            print("===============  Dataframe be like  ===============")
            print(self._data_df.head(5))
        print("===============  Dataframe shape  ===============")
        print(self._data_df.shape) 
        print("===============       Data info     ===============")
        print(self._data_df.info())
        print("===============  Label distribution ===============")
        print(self._data_df["target"].value_counts())

    def ToDataFrame(self):
        """
        Return the data as a DataFrame.
        """
        return self._data_df