import pickle
import geopandas as gpd


class ELRDataLoader:
    """Handles loading ELR reference data."""

    @staticmethod
    def load_elr_data(filepath: str) -> gpd.GeoDataFrame:
        """
        Load ELR reference data from pickle file.

        Parameters
        ----------
        filepath : str
            Path to the pickle file

        Returns
        -------
        gpd.GeoDataFrame
            Loaded ELR reference data

        Raises
        ------
        FileNotFoundError
            If the file doesn't exist
        """
        try:
            with open(filepath, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"ELR reference data file not found at {filepath}")
