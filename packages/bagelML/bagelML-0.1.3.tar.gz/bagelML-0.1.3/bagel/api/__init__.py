from abc import ABC, abstractmethod
from typing import Sequence, Optional, Dict, Any, List
from uuid import UUID

import pandas as pd
from bagel.api.Cluster import Cluster
from bagel.api.types import (
    ClusterMetadata,
    Document,
    Documents,
    Embeddings,
    IDs,
    Include,
    Metadatas,
    Metadata,
    Where,
    QueryResult,
    GetResult,
    WhereDocument,
    OneOrMany,
)
from bagel.config import Component
from overrides import override

DEFAULT_TENANT = "default_tenant"
DEFAULT_DATABASE = "default_database"


class API(Component, ABC):
    @abstractmethod
    def ping(self) -> int:
        """Returns the current server time in nanoseconds to check if the server is alive

        Args:
            None

        Returns:
            int: The current server time in nanoseconds

        """
        pass

    @abstractmethod
    def join_waitlist(self, email: str) -> Dict[str, str]:
        """
        Add email to waitlist
        Args:
            None

        Returns:
            dict: A dictionary of resposne
        """
        pass
    
    @abstractmethod
    def create_dataset(
            self,
            dataset_id: UUID,
            name: str,
            description: str,
            user_id: str = DEFAULT_TENANT,
            api_key: Optional[str] = None
    ) -> str:
        """Create a dataset"""
        pass
    
    @abstractmethod
    def get_dataset_info(
            self, 
            dataset_id: str,
            api_key: Optional[str] = None
    ) -> str:
        """Get information about a dataset."""
        pass

    @abstractmethod
    def upload_dataset(
            self,
            dataset_id: str, 
            chunk_number: int = 1,
            file_name: str = "",
            file_content: bytes = None,
            api_key: Optional[str] = None
    ) -> str:
        """Upload a dataset file to Bagel."""
        pass

    @abstractmethod
    def download_dataset(
            self,
            dataset_id: str,
            file_path: Optional[str] = "",
            api_key: Optional[str] = None
    ) -> str:  
        """Download the full dataset."""
        pass
    
    @abstractmethod
    def download_dataset_files(
            self,
            dataset_id: str, 
            target_dir: str,
            file_path: Optional[str] = "",
            api_key: Optional[str] = None
            ) -> bool:
        pass

    # @abstractmethod
    # def fine_tune(self, payload: str, api_key: str) -> str:
    #     """Fine tune the model"""
    #     pass
    @abstractmethod
    def create_asset(self, payload: dict, api_key: str) -> str:
        """create asset"""
        pass
    
    @abstractmethod
    def get_asset_info(self, asset_id: str, api_key: Optional[str] = None) -> str:
        """get asset by id"""
        pass
    
    @abstractmethod
    def get_assets_list(self, user_id: str, api_key: Optional[str] = None) -> str:
        """get all asset created by a user"""
        pass

    @abstractmethod
    def delete_asset(self, dataset_id: str, api_key: Optional[str] = None) -> str:
        """delete asset"""
        pass
    
    @abstractmethod
    def download_model_file(self, asset_id: str, file_name: str, api_key: Optional[str] = None) -> Document:
        """Download document"""
        pass

    @abstractmethod
    def download_model(self, asset_id: str, api_key: Optional[str] = None) -> Any:
        """download model"""
        pass
    
    @abstractmethod
    def update_asset(self, asset_id: str, payload: dict, api_key: Optional[str] = None) -> str:
        """update asset"""
        pass
    
    @abstractmethod
    def fine_tune(self, title: str, user_id: str, asset_id: str, file_name: str, 
                  base_model: str, epochs: Optional[int] = 3, learning_rate: Optional[float] = 0.001, 
                  input_column: str = None, output_column: str = None,
                  api_key: Optional[str] = None) -> str:
        """Fine tune method"""
        pass

    @abstractmethod
    def get_dataset_column_names(self, asset_id: str, file_name: str, api_key: Optional[str] = None):
        """Get dataset columns"""
        pass

    @abstractmethod
    def get_job(self, job_id, api_key) -> str:
        """get job"""
        pass

    @abstractmethod
    def get_job_by_asset_id(self, asset_id: str, api_key: Optional[str] = None) -> str:
        """get job by asset id"""
        pass
    
    @abstractmethod
    def list_jobs(self, user_id: str, api_key: Optional[str] = None) -> str:
        """list jobs"""
        pass
    
    @abstractmethod
    def file_upload(self, file_path: str, asset_id: str, api_key: Optional[str] = None) -> str:
        """file upload"""
        pass

    @abstractmethod
    def buy_asset(self, asset_id: str, user_id: str, api_key: Optional[str] = None) -> str:
        """buy asset"""
        pass

    @abstractmethod
    def get_download_url(self, asset_id: str, file_name: str, api_key: Optional[str] = None) -> dict:
        """get download URL"""
        pass

    @abstractmethod
    def get_model_files_list(self, asset_id: str, api_key: Optional[str] = None):
        """get model files"""
        pass
