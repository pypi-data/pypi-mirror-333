from typing import List, Dict, Any, Optional
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document


class MultiVectorStoreRetriever(BaseRetriever):
    """
    This aggregator retriever queries multiple vector stores
    and merges the results into a single list.
    """

    stores: List[Any]
    search_kwargs: Dict[str, Any]
    chain_type: str
    search_type: str
    metric_type: str

    def __init__(
        self,
        stores: List[Any],
        metric_type: str = 'COSINE',
        chain_type: str = 'stuff',
        search_type: str = 'similarity',
        search_kwargs: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the MultiVectorStoreRetriever.

        Args:
            stores: List of vector stores that provide an as_retriever() method
            metric_type: Similarity metric (COSINE, EUCLIDEAN, DOT_PRODUCT)
            chain_type: Chain type for the retriever
            search_type: Search type (similarity, mmr)
            search_kwargs: Dict to pass to each store's retrieve method (like 'k' for top_k)
        """
        super().__init__()
        self.stores = stores
        self.search_kwargs = search_kwargs or {}
        self.chain_type = chain_type
        self.search_type = search_type
        self.metric_type = metric_type

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """
        Get documents relevant to the query.
        Implements the required method from BaseRetriever.

        Args:
            query: Query string
            run_manager: CallbackManager for the run

        Returns:
            List of relevant documents
        """
        all_results = []
        for store in self.stores:
            retriever = store.as_retriever(
                search_type=self.search_type,
                search_kwargs=self.search_kwargs,
                chain_type=self.chain_type
            )
            # Pass the run_manager to the sub-retrievers if they support it
            if hasattr(retriever, "_get_relevant_documents"):
                callback_manager = run_manager.get_child()
                docs = retriever._get_relevant_documents(query, run_manager=callback_manager)
            else:
                docs = retriever.get_relevant_documents(query)
            all_results.extend(docs)
        return all_results

    async def _aget_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """
        Asynchronously get documents relevant to the query.
        Implements the required async method from BaseRetriever.

        Args:
            query: Query string
            run_manager: CallbackManager for the run

        Returns:
            List of relevant documents
        """
        all_results = []
        for store in self.stores:
            retriever = store.as_retriever(
                search_type=self.search_type,
                search_kwargs=self.search_kwargs,
                chain_type=self.chain_type
            )
            # Pass the run_manager to the sub-retrievers if they support it
            if hasattr(retriever, "_aget_relevant_documents"):
                callback_manager = run_manager.get_child()
                docs = await retriever._aget_relevant_documents(query, run_manager=callback_manager)
            else:
                docs = await retriever.aget_relevant_documents(query)
            all_results.extend(docs)
        return all_results
