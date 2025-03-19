import logging
import pandas as pd
import pyarrow as pa
from collections import deque

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PandorasDataFrame(pd.DataFrame):
    """Custom Pandas DataFrame with Undo/Redo functionality using pyarrow."""

    _metadata = ["_history", "_future", "_max_history"]

    def __init__(self, *args, max_history=10, **kwargs):
        super().__init__(*args, **kwargs)
        self._history = deque(maxlen=max_history)  # Stores past versions
        self._future = deque(maxlen=max_history)  # Stores redo versions
        self._max_history = max_history

    def _store_state(self):
        """Save current DataFrame state as an Arrow Table before modification."""
        self._history.append(pa.Table.from_pandas(self, preserve_index=True))
        self._future.clear()  # Clear redo stack when new change is made

    def _restore_state(self, df):
        self.__dict__.update(df.__dict__)

    def undo(self):
        """Revert to the previous state if available."""
        if not self._history:
            logger.warning("No more undo steps available.")
            return

        self._future.append(pa.Table.from_pandas(self, preserve_index=True))  # Save current state for redo
        prev_state = self._history.pop()  # Get previous version
        restored_df = prev_state.to_pandas()  # Convert back to Pandas

        self._restore_state(restored_df)

    def redo(self):
        """Redo an undone operation."""
        if not self._future:
            logger.warning("No more redo steps available.")
            return

        self._history.append(pa.Table.from_pandas(self, preserve_index=True))  # Save current state for undo
        next_state = self._future.pop()  # Get redo version
        restored_df = next_state.to_pandas()  # Convert back to Pandas

        self._restore_state(restored_df)

    @property
    def history_size(self):
        """Return the number of stored undo steps."""
        return len(self._history)

    @property
    def future_size(self):
        """Return the number of stored redo steps."""
        return len(self._future)

    def clear_history(self):
        """Clear undo and redo history."""
        self._history.clear()
        self._future.clear()

    # Override Pandas modification functions to track changes
    def drop(self, *args, **kwargs):
        self._store_state()
        return super().drop(*args, **kwargs)

    def rename(self, *args, **kwargs):
        self._store_state()
        return super().rename(*args, **kwargs)

    def replace(self, *args, **kwargs):  # noqa
        self._store_state()
        return super().replace(*args, **kwargs)

    def reset_index(self, *args, **kwargs):
        self._store_state()
        return super().reset_index(*args, **kwargs)

    def set_index(self, *args, **kwargs):
        self._store_state()
        return super().set_index(*args, **kwargs)

    def fillna(self, *args, **kwargs):  # noqa
        self._store_state()
        return super().fillna(*args, **kwargs)

    def assign(self, **kwargs):
        self._store_state()
        return super().assign(**kwargs)

    def apply(self, *args, **kwargs):
        self._store_state()
        return super().apply(*args, **kwargs)


__all__ = ["PandorasDataFrame"]
