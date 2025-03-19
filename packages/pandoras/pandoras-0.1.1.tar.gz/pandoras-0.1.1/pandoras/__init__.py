from .pandoras import PandorasDataFrame

import sys
import pandas as pd

sys.modules["pandoras"] = pd
pd.DataFrame = PandorasDataFrame
