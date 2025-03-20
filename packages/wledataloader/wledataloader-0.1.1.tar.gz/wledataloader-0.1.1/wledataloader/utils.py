import numpy as np
np.random.seed(1337)  # for reproducibility
import pandas as pd
import os
from typing import List, Tuple, Generator, Iterator
import csv
from natsort import natsorted
import multiprocessing as mp
from os import path

from sklearn import preprocessing
from sklearn import base
from sklearn.preprocessing import (StandardScaler, OrdinalEncoder, LabelEncoder, MinMaxScaler, OneHotEncoder)
from sklearn.model_selection import train_test_split
import os
import requests
import zipfile
from pathlib import Path
from tqdm import tqdm

def download_and_extract(url: str, save_dir: str = "downloads"):
    """
    Tải file từ URL và giải nén nếu là file ZIP.
    
    :param url: URL của file cần tải
    :param save_dir: Thư mục lưu file tải về
    :return: Đường dẫn thư mục chứa dữ liệu đã giải nén hoặc file đã tải
    """
    os.makedirs(save_dir, exist_ok=True)
    
    filename = url.split("/")[-1]
    file_path = os.path.join(save_dir, filename)
    
    # Nếu file đã tồn tại, không tải lại
    if not os.path.exists(file_path):
        print(f"Downloading {filename}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192  # 8 KB
        
        with open(file_path, "wb") as file, tqdm(
            desc=filename, total=total_size, unit='B', unit_scale=True
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=block_size):
                file.write(chunk)
                progress_bar.update(len(chunk))
        print("Download complete.")
    else:
        print("File already exists, skipping download.")
    
    # Giải nén nếu là file ZIP
    if filename.endswith(".zip"):
        extract_path = save_dir
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
        print("Extraction complete.")
        return extract_path
    
    return file_path


TupleOrList = tuple([Tuple, List])


def reduce_samples(X_train, y_train, target_count=100000):
    selected_indices = []
    
    for label in np.unique(y_train):
        indices = np.where(y_train == label)[0]
        if len(indices) > target_count:
            np.random.shuffle(indices)
            indices = indices[:target_count]
        selected_indices.extend(indices)
    
    np.random.shuffle(selected_indices)
    X_train_reduced = X_train[selected_indices]
    y_train_reduced = y_train[selected_indices]
    
    return X_train_reduced, y_train_reduced

def Interpolate_with_gaussian_noise(data: pd.Series) -> pd.Series:
  """Couldn't find a proper name. Very slow ..."""
  DTYPE = np.float32

  series = data.astype(DTYPE)
  values = series.tolist()
  processed = []

  series_size = len(values)

  prev_rssi = 0
  prev_seq = -1
  for seq, rssi in enumerate(values):
    if not np.isnan(rssi):
        avg_rssi = np.mean([prev_rssi, rssi])
        std_rssi = np.std([prev_rssi, rssi])
        std_rssi = std_rssi if std_rssi > 0 else np.nextafter(DTYPE(0), DTYPE(1))
        diff = seq - prev_seq - 1

        processed.extend(np.random.normal(avg_rssi, std_rssi, size=diff))
        processed.append(rssi)
        prev_seq, prev_rssi = seq, rssi

  avg_rssi = np.mean([prev_rssi, 0.])
  std_rssi = np.std([prev_rssi, 0.])
  diff = series_size - prev_seq - 1
  processed.extend(np.random.normal(avg_rssi, std_rssi, size=diff))

  series = pd.Series(data=processed, index=data.index, dtype=DTYPE)
  return series


def Interpolate_with_constant(data: pd.Series, constant: int = 0) -> pd.Series:
  """Interpolate missing values with constant value."""
  return data.fillna(value=constant)


class CustomInterpolation(base.BaseEstimator, base.TransformerMixin):
  """Custom interpolation function to be used in"""

  STRATEGIES_ALL = ['none', 'gaussian', 'constant']

  def __init__(self, source: str, strategy: str = 'constant', constant: float = 0, target=None):
    if strategy not in self.STRATEGIES_ALL:
      raise ValueError(f'"{strategy}" is not available strategy')

    self.strategy = strategy
    self.constant = constant

    self.source = source
    self.target = source if target is None else target

  def with_constant(self, data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df[self.target] = df[self.source].fillna(value=self.constant)
    return df

  def with_gaussian(self, data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df[self.target] = Interpolate_with_gaussian_noise(df[self.source])
    return df

  def with_none(self, data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    src = [self.source] if isinstance(self.source, [str]) else self.source
    df = df.dropna(subset=src)
    return df

  def do_interpolation(self, X: pd.DataFrame) -> pd.DataFrame:
    if self.strategy == 'constant':
      return self.with_constant(X)

    if self.strategy == 'gaussian':
      return self.with_gaussian(X)

    if self.strategy == 'none':
      return self.with_none(X)

    raise ValueError(f'"{self.strategy}" is not available strategy')

  def fit(self, X: pd.DataFrame, y=None):
    return self

  def transform(self, X, y='deprecated', copy=True):
    if isinstance(X, (List, Tuple,)):
      with mp.Pool(processes=2) as p:
          return p.map(self.do_interpolation, X)

    return self.do_interpolation(X)


class CustomSplitter(base.BaseEstimator, base.TransformerMixin):
  def __init__(self, X: TupleOrList = None, y: str = 'class', drop: TupleOrList = None):
    self.X = X
    self.y = y
    self.drop = drop

  def fit(self, X: pd.DataFrame, y=None):
    return self

  def transform(self, df: pd.DataFrame, y='deprecated', copy=True):
    df = df.copy() if copy else df
    if self.drop:
      df.drop(labels=self.drop, axis=1, inplace=True)

    if self.X:
      return df[self.X], df[self.y].ravel()

    return df.drop(self.y), df[self.y].ravel()


class CustomMerger(base.BaseEstimator, base.TransformerMixin):
  """Merge List of DataFrames"""

  def __init__(self):
    pass

  def fit(self, X: pd.DataFrame, y=None):
    return self

  def transform(self, X: pd.DataFrame, y='deprecated', copy=True):
    if isinstance(X, TupleOrList):
        return pd.concat(X, ignore_index=True).reset_index(drop=True)

    return X


class SyntheticFeatures(base.BaseEstimator, base.TransformerMixin):
  """Rolling window for mean & std features."""

  def __init__(self, source: str, window_size: int = 10, target=None):
    self.source = source
    self.target = source if target is None else target

    if not isinstance(window_size, int) or not window_size > 0:
      raise ValueError(f'Window should be positive integer. Got `{window_size}` instead.')

    self.window = window_size

  def fit(self, X, y=None):
    return self

  def do_synthetics(self, data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df[f'{self.target}_mean'] = df[self.source].rolling(self.window).mean()
    df[f'{self.target}_std'] = df[self.source].rolling(self.window).std()
    df[f'{self.target}_median'] = df[self.source].rolling(self.window).median()
    return df

  def transform(self, X: pd.DataFrame, y='deprecated', copy=True):
    if isinstance(X, (List, Tuple,)):
      with mp.Pool(processes=2) as p:
          return p.map(self.do_synthetics, X)

    return self.do_synthetics(X)


class PRR(base.BaseEstimator, base.TransformerMixin):
  """Calculate PRR based on `target`"""

  def __init__(self, source: str, window_size: int, ahead: int, target: str = 'prr'):
    self.source = source
    self.target = source if target is None else target

    if not isinstance(window_size, int) or not window_size > 0:
      raise ValueError(f'window_size should be positive integer. Got `{window_size}` instead.')

    self.window = window_size

    if not isinstance(ahead, int) or not ahead >= 0:
      raise ValueError(f'ahead should be greater or equal to zero integer. Got `{ahead}` instead.')

    self.ahead = ahead

  def fit(self, X: pd.DataFrame, y=None):
    return self

  def calculate_prr(self, dataframe):
    df = dataframe.copy()
    df[self.target] = (df[self.source].astype(bool).rolling(self.window).sum() / self.window).shift(
        -1 * self.window * self.ahead)
    return df

  def transform(self, X: pd.DataFrame, y='deprecated'):
    if isinstance(X, TupleOrList):
      with mp.Pool(processes=2) as p:
          return p.map(self.calculate_prr, X)

    return self.calculate_prr(X)


def Poly_features(df: pd.DataFrame, include: List[str], degree: int, include_bias=False, *args,
                **kwargs) -> pd.DataFrame:
  """The `PolynomialFeatures` from sklern drops/loses information about column names from pandas, which is not very convinient.
  This is a workaround for this behaviour to preserve names.
  """
  X, excluded = df.loc[:, include], df.drop(include, axis=1)
  poly = preprocessing.PolynomialFeatures(degree=degree, include_bias=include_bias, *args, **kwargs).fit(X)

  # Next line converts back to pandas, while preserving column names
  X = pd.DataFrame(poly.transform(X), columns=poly.get_feature_names_out(X.columns), index=X.index)

  data = pd.concat([X, excluded], axis=1, )
  data = data.reset_index(drop=True)

  # Transform column names. Ex. 'rssi rssi_avg' -> 'rssi*rssi_avg'
  data = data.rename(lambda cname: cname.replace(' ', '*'), axis='columns')

  return data


