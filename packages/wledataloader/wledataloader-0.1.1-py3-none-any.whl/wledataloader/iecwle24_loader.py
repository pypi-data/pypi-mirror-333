from .utils import *
from .base_loader import DataBase

class IECWLE24Loader(DataBase):
    def __init__(self, seed=0xDEADBEEF, printable=True, rate_list=[], save_csv=True) -> None:
        self.download_url = 'http://clouds.iec-uit.com/wireless-link-estimation/RASP_COL.zip'
        self.dataname = 'RASP_COL'
        super().__init__(seed, printable, rate_list, save_csv)

    def _traceToLoadDf(self, datadir):
        self._data_df = pd.read_csv(os.path.join(datadir, "RASP_COL.csv"), index_col=False)

    def AddPolyFeatures(self, include=['Bit Rate', 'TDLS peer_no', 'TDLS peer_yes', 
                                       'Tx excessive retries', 'rx bitrate', 'rx packets', 
                                       'tx bytes', 'tx failed', 'tx packets'], degree=2, include_bias=True):
        return super().AddPolyFeatures(include, degree, include_bias)