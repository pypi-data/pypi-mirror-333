
"""
Support for loading data from different sources.
- ColoradoLoader: Load data from Colorado dataset
- JsiSigfoxLoader: Load data from JSI Sigfox dataset
- PktMetaLoader: Load data from PktMeta dataset
- RutgersLoader: Load data from Rutgers dataset
- RaspColLoader: Load data from RaspCol dataset

Example:
    from WLEdataloader import ColoradoLoader
    data = ColoradoLoader()
    data.PrepareData(reload=False, extend_feature=True)
    print(data._data_df.shape)
"""
from .colorado_loader import ColoradoLoader
from .jsi_sigfox_loader import JsiSigfoxLoader
from .pktmeta_loader import PktMetaLoader
from .rutgers_loader import RutgersLoader
from .raspcol_loader import RaspColLoader       