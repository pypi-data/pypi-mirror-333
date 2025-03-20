import numpy as np

def EMA(close, timePeriod=20):
    """
    **Exponential Moving Average (EMA)**

    :param timePeriod (int): Số chu kỳ
    :returns np.array[float64]:
    """
    if not isinstance(timePeriod, int) or timePeriod <= 0 or len(close) < timePeriod:
        raise ValueError("EMA: Độ dài phải là số nguyên dương.")

    alpha = 2 / (timePeriod + 1)
    ema = np.zeros_like(close)
    ema[0] = close[0]  # Khởi tạo EMA đầu tiên bằng giá đóng cửa đầu tiên
    for i in range(1, len(close)):
        ema[i] = alpha * close[i] + (1 - alpha) * ema[i - 1]
    return ema

def SMA(close, timePeriod=20):
    """
    **Simple Moving Average (SMA)**

    :param timePeriod (int): Số chu kỳ
    :returns np.array[float64]:
    """
    if not isinstance(timePeriod, int) or timePeriod <= 0 or len(close) < timePeriod:
        raise ValueError("SMA: Độ dài phải là số nguyên dương.")
    
    sma = np.convolve(close, np.ones(timePeriod) / timePeriod, mode='valid')
    # Giữ số phần tử bằng với close
    return np.concatenate((np.full(timePeriod - 1, np.nan), sma))

def KBANDS(high, low, close, timePeriod=20, mult=1.0, atrPeriod=10, useEma=True):
    """
    **Keltner Bands (KBANDS)**

    :param timePeriod (int): Số chu kỳ
    :param mult (float):  Hệ số nhân độ lệch chuẩn
    :param atrPeriod (int): Số chu kỳ ATR
    :param useEma (bool): Sử dụng EMA hoặc SMA
    :returns (tuple): np.array[float64], np.array[float64], np.array[float64]
    """
    if not isinstance(timePeriod, int) or timePeriod <= 0 or len(close) < timePeriod:
        raise ValueError("KBANDS: Độ dài phải là số nguyên dương.")
    if useEma:
        ma = EMA(close, timePeriod)
    else:
        ma = SMA(close, timePeriod)
    atr = ATR(high, low, close, atrPeriod)
    upper = ma + mult * atr
    lower = ma - mult * atr
    return upper, ma, lower

def BBANDS(close, timePeriod=20, mult=2.0):
    """
    **Bollinger Bands (BBANDS)**

    :param timePeriod (int): Số chu kỳ
    :param mult (float): Hệ số nhân độ lệch chuẩn
    :returns (tuple): np.array[float64], np.array[float64], np.array[float64]
    """
    if not isinstance(timePeriod, int) or timePeriod <= 0 or len(close) < timePeriod:
        raise ValueError("BBANDS: Độ dài phải là số nguyên dương.")
    
    sma = SMA(close, timePeriod)
    std = np.full_like(close, np.nan)
    
    for i in range(timePeriod - 1, len(close)):
        std[i] = np.std(close[i - timePeriod + 1:i + 1])
    
    upper = sma + mult * std
    lower = sma - mult * std
    
    return upper, sma, lower

# Momentum Indicators

def RSI(close, timePeriod=14):
    """
    **Relative Strength Index (RSI)**
    :param timePeriod (int): Số chu kỳ
    :returns np.array[float64]:
    """
    # Kiểm tra giá trị timePeriod
    if not isinstance(timePeriod, int) or timePeriod <= 0 or len(close) < timePeriod:
        raise ValueError("RSI: Độ dài phải là số nguyên dương.")

    # Tính toán chênh lệch giá giữa các ngày liên tiếp
    deltas = np.diff(close)
    
    # Tách biệt các khoản tăng và giảm
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    # Khởi tạo mảng trung bình tăng và giảm
    avg_gain = np.zeros_like(deltas)
    avg_loss = np.zeros_like(deltas)
    
    # Tính trung bình tăng/giảm ban đầu cho giai đoạn đầu tiên
    avg_gain[timePeriod-1] = np.mean(gains[:timePeriod])
    avg_loss[timePeriod-1] = np.mean(losses[:timePeriod])
    
    # Tính toán trung bình tăng/giảm cho các giai đoạn tiếp theo (smoothing)
    for i in range(timePeriod, len(deltas)):
        avg_gain[i] = (avg_gain[i-1] * (timePeriod - 1) + gains[i]) / timePeriod
        avg_loss[i] = (avg_loss[i-1] * (timePeriod - 1) + losses[i]) / timePeriod
    
    # Tính chỉ số RS và RSI, bắt đầu từ timePeriod-1
    rs = np.zeros_like(avg_gain) # Initialize rs with zeros
    rs[timePeriod-1:] = np.where(avg_loss[timePeriod-1:] != 0, avg_gain[timePeriod-1:] / avg_loss[timePeriod-1:], 0)

    rsi = 100 - (100 / (1 + rs))

    # Xử lý trường hợp mất mát trung bình bằng 0 (RSI = 100)
    rsi[avg_loss == 0] = 100.0

    # Xử lý trường hợp cả tăng và giảm trung bình bằng 0 (RSI = 50)
    both_zero = (avg_gain == 0) & (avg_loss == 0)
    rsi[both_zero] = 50.0
    
    # Đệm giá trị RSI để đồng bộ với mảng giá đóng cửa gốc
    rsi_padded = np.full(len(close), np.nan)
    rsi_padded[timePeriod:] = rsi[timePeriod-1:]
    
    return rsi_padded

def MFI(high, low, close, volume, timePeriod=14):
    """
    **Money Flow Index (MFI)**

    :param timePeriod (int): Số chu kỳ
    :returns np.array[float64]:
    """
    if not isinstance(timePeriod, int) or timePeriod <= 0 or len(close) < timePeriod:
        raise ValueError("MFI: Độ dài phải là số nguyên dương.")
    
    typical_price = (high + low + close) / 3
    raw_money_flow = typical_price * volume
    flow_direction = np.sign(np.diff(typical_price, prepend=typical_price[0]))
    positive_flow = np.where(flow_direction > 0, raw_money_flow, 0)
    negative_flow = np.where(flow_direction < 0, raw_money_flow, 0)
    avg_positive = np.convolve(positive_flow, np.ones(timePeriod) / timePeriod, mode='valid')
    avg_negative = np.convolve(negative_flow, np.ones(timePeriod) / timePeriod, mode='valid')
    mfi = 100 - (100 / (1 + (avg_positive / (avg_negative + 1e-10))))
    return np.concatenate((np.full(timePeriod - 1, np.nan), mfi))

# Volatility Indicators

def ATR(high, low, close, timePeriod=14):
    """
    **Average True Range (ATR)**

    :param timePeriod (int): Số chu kỳ
    :returns np.array[float64]:
    """
    if not isinstance(timePeriod, int) or len(close) < timePeriod:
        raise ValueError("ATR: Độ dài phải là số nguyên dương.")

    # Tính True Range
    tr0 = high - low
    tr1 = np.abs(high - np.roll(close, 1))
    tr2 = np.abs(low - np.roll(close, 1))
    tr = np.maximum(tr0, np.maximum(tr1, tr2))
    tr[0] = high[0] - low[0]  #Correct the first TR value

    # Tính ATR bằng SMA
    atr = np.zeros_like(close)
    atr[:timePeriod] = np.nan # set nan value where no enough data

    atr[timePeriod-1] = np.mean(tr[:timePeriod]) # first atr value

    for i in range(timePeriod, len(close)):
        atr[i] = (atr[i-1] * (timePeriod - 1) + tr[i]) / timePeriod

    return atr

# GET Last Index

def ema(close, timePeriod=20):
    """
    **GET: Last Exponential Moving Average (EMA)**

    :param timePeriod (int): Số chu kỳ
    :returns (float): EMA hiện tại
    """
    ema = EMA(close, timePeriod=timePeriod)
    return float(ema[-1])

def sma(close, timePeriod=20):
    """
    **GET: Last Simple Moving Average (SMA)**

    :param timePeriod (int): Số chu kỳ
    :returns (float): SMA hiện tại
    """
    sma = SMA(close, timePeriod=timePeriod)
    return float(sma[-1])

def atr(high, low, close, timePeriod=14):
    """
    **GET: Last Average True Range (ATR)**

    :param timePeriod (int): Số chu kỳ
    :returns (float): ATR hiện tại
    """
    atr = ATR(high, low, close, timePeriod=timePeriod)
    return float(atr[-1])

def kbands(high, low, close, timePeriod=20, mult=1.0, atrPeriod=10, useEma=True):
    """
    **GET: Last Keltner Bands (KBANDS)**

    :param timePeriod (int): Số chu kỳ
    :param mult (float):  Hệ số nhân độ lệch chuẩn
    :param atrPeriod (int): Số chu kỳ ATR
    :param useEma (bool): Sử dụng EMA hoặc SMA
    :returns (tuple): (upper, middle, lower)
    """
    upper, ma, lower = KBANDS(high, low, close, timePeriod=timePeriod, mult=mult, atrPeriod=atrPeriod, useEma=useEma)
    return float(upper[-1]), float(ma[-1]), float(lower[-1])

def bbands(close, timePeriod=20, mult=2.0):
    """
    **GET: Last Bollinger Bands (BBANDS)**

    :param timePeriod (int): Số chu kỳ
    :param mult (float): Hệ số nhân độ lệch chuẩn
    :returns (tuple): (upper, middle, lower)
    """
    upper, sma, lower = BBANDS(close, timePeriod=timePeriod, mult=mult)
    return float(upper[-1]), float(sma[-1]), float(lower[-1])

def rsi(close, timePeriod=14):
    """
    **GET: Last Relative Strength Index (RSI)**

    :param timePeriod (int): Số chu kỳ
    :returns (float): RSI hiện tại
    """
    rsi = RSI(close, timePeriod=timePeriod)
    return float(rsi[-1])

def mfi(high, low, close, volume, timePeriod=14):
    """
    **GET: Last Money Flow Index (MFI)**

    :param timePeriod (int): Số chu kỳ
    :returns (float): MFI hiện tại
    """
    mfi = MFI(high, low, close, volume, timePeriod)
    return float(mfi[-1])