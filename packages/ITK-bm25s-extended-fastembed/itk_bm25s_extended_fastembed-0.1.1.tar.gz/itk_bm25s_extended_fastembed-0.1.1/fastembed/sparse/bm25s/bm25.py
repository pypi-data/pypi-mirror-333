import os
from multiprocessing import get_all_start_methods
from pathlib import Path
from typing import Any, Iterable, Optional, Type, Union, List, Callable
from loguru import logger
import numpy as np
import mmh3

from bm25s.tokenization import Tokenizer as Bm25sTokenizer, _infer_stopwords as bm25s_infer_stopwords
from bm25s import BM25 as BM25s
import scipy.sparse as sp
from numpy.ma.core import indices

try:
    from py_rust_stemmers import SnowballStemmer
except ImportError:
    logger.debug('The rust implementation of snowball stemmer could not be imported.'
                  + ' Trying with the python implementation directly from the snowball project')
    # Try the python implementation directly from the snowball project
    from Stemmer import Stemmer as SnowballStemmer

from fastembed.common.utils import (
    define_cache_dir,
    iter_batch,
    remove_non_alphanumeric,
)
from fastembed.sparse.bm25 import supported_languages
from fastembed.parallel_processor import ParallelWorkerPool, Worker
from fastembed.sparse.sparse_embedding_base import (
    SparseEmbedding,
    SparseTextEmbeddingBase,
)

supported_bm25_models = [
    {
        "model": "bm25s/robertson",
        "description":  "BM25 as sparse embeddings meant to be used with Qdrant using BM25s implementation of the Robertson method\n\n" +
                        "Computes the term frequency component of the BM25 score using Robertson+ (original) variant\n" +
                        "Implementation: https://cs.uwaterloo.ca/~jimmylin/publications/Kamphuis_etal_ECIR2020_preprint.pdf",
        "license": "mit",
        "size_in_GB": 0.01,
        "sources": {
            "hf": "Qdrant/bm25",
        },
        "model_file": "mock.file",  # bm25 does not require a model, so we just use a mock
        "additional_files": [f"{lang}.txt" for lang in supported_languages],
        "requires_idf": False,  # As this is accounted for in the weights when embedding
    },
    {
        "model": "bm25s/lucene",
        "description":  "BM25 as sparse embeddings meant to be used with Qdrant using BM25s implementation of the Lucene method\n\n" +
                        "Computes the term frequency component of the BM25 score using Lucene variant (accurate)\n" +
                        "Implementation: https://cs.uwaterloo.ca/~jimmylin/publications/Kamphuis_etal_ECIR2020_preprint.pdf\n\n" + 
                        "The lucene method is the default method when using the bm25s library directly.",
        "license": "mit",
        "size_in_GB": 0.01,
        "sources": {
            "hf": "Qdrant/bm25",
        },
        "model_file": "mock.file",  # bm25 does not require a model, so we just use a mock
        "additional_files": [f"{lang}.txt" for lang in supported_languages],
        "requires_idf": False,  # As this is accounted for in the weights when embedding
    },
    {
        "model": "bm25s/atire",
        "description":  "BM25 as sparse embeddings meant to be used with Qdrant using BM25s implementation of the Atire method\n\n" +
                        "Computes the term frequency component of the BM25 score using ATIRE variant\n" +
                        "Implementation: https://cs.uwaterloo.ca/~jimmylin/publications/Kamphuis_etal_ECIR2020_preprint.pdf",
        "license": "mit",
        "size_in_GB": 0.01,
        "sources": {
            "hf": "Qdrant/bm25",
        },
        "model_file": "mock.file",  # bm25 does not require a model, so we just use a mock
        "additional_files": [f"{lang}.txt" for lang in supported_languages],
        "requires_idf": False,  # As this is accounted for in the weights when embedding
    },
    {
        "model": "bm25s/bm25l",
        "description":  "BM25 as sparse embeddings meant to be used with Qdrant using BM25s implementation of the BM25L method\n\n" +
                        "Computes the term frequency component of the BM25 score using BM25L variant\n" +
                        "Implementation: https://cs.uwaterloo.ca/~jimmylin/publications/Kamphuis_etal_ECIR2020_preprint.pdf",
        "license": "mit",
        "size_in_GB": 0.01,
        "sources": {
            "hf": "Qdrant/bm25",
        },
        "model_file": "mock.file",  # bm25 does not require a model, so we just use a mock
        "additional_files": [f"{lang}.txt" for lang in supported_languages],
        "requires_idf": True,
    },
    {
        "model": "bm25s/bm25plus",
        "description":  "BM25 as sparse embeddings meant to be used with Qdrant using BM25s implementation of the BM25+ method\n\n" +
                        "Computes the term frequency component of the BM25 score using BM25+ variant\n" +
                        "Implementation: https://cs.uwaterloo.ca/~jimmylin/publications/Kamphuis_etal_ECIR2020_preprint.pdf",
        "license": "mit",
        "size_in_GB": 0.01,
        "sources": {
            "hf": "Qdrant/bm25",
        },
        "model_file": "mock.file",  # bm25 does not require a model, so we just use a mock
        "additional_files": [f"{lang}.txt" for lang in supported_languages],
        "requires_idf": True,
    }
]

class Bm25(SparseTextEmbeddingBase):
    """Wraps the bm25s package implementation of various BM25 algorithms in a fastembed compatible form.
    Uses a count of tokens in the document to evaluate the importance of the token.

    WARNING: This model is expected to be used with `modifier="idf"` in the sparse vector index of Qdrant.

    Args:
        model_name (str): The name of the model to use.
        cache_dir (str, optional): The path to the cache directory.
            Can be set using the `FASTEMBED_CACHE_PATH` env variable.
            Defaults to `fastembed_cache` in the system's temp directory.
        k (float, optional): The k parameter in the BM25 formula. Defines the saturation of the term frequency.
            I.e. defines how fast the moment when additional terms stop to increase the score. Defaults to 1.2.
        b (float, optional): The b parameter in the BM25 formula. Defines the importance of the document length.
            Defaults to 0.75.
        avg_len (float, optional): The average length of the documents in the corpus. Defaults to 256.0.
        language (str): Specifies the language for the stemmer.
        disable_stemmer (bool): Disable the stemmer.
        bm25s_stopwords : Union[str, List[str]], optional
            The list of stopwords to remove from the text. If "english" or "en" is provided,
            the function will use the default English stopwords
        bm25s_stemmer : Callable, optional
            The stemmer to use for stemming the tokens. It is recommended
            to use the PyStemmer library for stemming, but you can also any callable that
            takes a list of strings and returns a list of strings.

    Raises:
        ValueError: If the model_name is not in the format <org>/<model> e.g. BAAI/bge-base-en.
    """

    def __init__(
        self,
        model_name: str,
        cache_dir: Optional[str] = None,
        k: float = 1.5,
        b: float = 0.75,
        delta: float = 0.5,
        backend="numpy",
        #avg_len: float = 256.0,
        language: str = "english",
        #token_max_length: int = 40,
        disable_stemmer: bool = False,
        #possible kwargs from SparseTextEmbeddings "factory method"
        bm25s_stopwords: str | List[str] = None,
        bm25s_stemmer: Callable = None,
        **kwargs,
    ):
        super().__init__(model_name, cache_dir, **kwargs)
        # In super (SparseTextEmbeddingBase) the self._local_files_only is set false

        if bm25s_stopwords is not None:
            self.stopwords = bm25s_infer_stopwords(bm25s_stopwords)
            self._local_files_only = True
            self.language = None
        else:
            try:
                self.stopwords = bm25s_infer_stopwords(language)
                self._local_files_only = True
                self.language = language
            except ValueError:
                logger.info(f"Stopwords for language {language} could not be inferred from bm25s. We try fastembeds own lists of stopwords")    
                if language not in supported_languages:
                    raise ValueError(f"{language} language is not supported")
                else:
                    self.language = language
                    self.stopwords = []

        model_description = self._get_model_description(model_name)
        self.cache_dir = define_cache_dir(cache_dir)

        if not self._local_files_only:
            # To only fetch the needed stopword list we overwrite the list of additional files
            model_description["additional_files"] = [f"{self.language}.txt"]
            self._model_dir = self.download_model(
                model_description, self.cache_dir, local_files_only=self._local_files_only
            )

        self.k = k
        self.b = b
        self.delta = delta
        self.method = self.model_name.split("/")[-1]
        self.backend = backend
        self.disable_stemmer = disable_stemmer

        if disable_stemmer:
            self.stemmer = None
        else:
            if bm25s_stemmer is not None:
                self.stemmer = bm25s_stemmer
            else:
                # The bm25s package is built expecting the PyStemmer implementation 
                # of Snowball stemming project instead of the py_rust_stemmers 
                # implementation used by fastembed, thus the bm25s classes expects 
                # the stemmer class to have a stemWord method (instead of the 
                # stem_word method of the py_rust_stemmers SnowballStemmer)
                # The bm25s classes also accepts a direct stemming method, which we
                # exploit here
                stemmer = SnowballStemmer(language)
                self.stemmer = stemmer.stem_word
            if not self.stopwords:
                self.stopwords = self._load_stopwords(self._model_dir, self.language)

        #self.tokenizer = SimpleTokenizer
        self.tokenizer = Bm25sTokenizer(stopwords=self.stopwords, stemmer=self.stemmer)
        
        self.bm25s_engine = BM25s(
            k1=self.k,
            b=self.b,
            delta=self.delta,
            method=self.method,
            backend=self.backend,
        )

    @classmethod
    def list_supported_models(cls) -> list[dict[str, Any]]:
        """Lists the supported models.

        Returns:
            list[dict[str, Any]]: A list of dictionaries containing the model information.
        """
        return supported_bm25_models

    @classmethod
    def _load_stopwords(cls, model_dir: Path, language: str) -> list[str]:
        stopwords_path = model_dir / f"{language}.txt"
        if not stopwords_path.exists():
            return []

        with open(stopwords_path, "r") as f:
            return f.read().splitlines()

    def _embed_documents(
        self,
        model_name: str,
        cache_dir: str,
        documents: Union[str, Iterable[str]],
        batch_size: int = 256,
        parallel: Optional[int] = None,
    ) -> Iterable[SparseEmbedding]:
        is_small = False

        if isinstance(documents, str):
            documents = [documents]
            is_small = True

        if isinstance(documents, list):
            if len(documents) < batch_size:
                is_small = True

        if parallel is None or is_small:
            #for batch in iter_batch(documents, batch_size):
            #    yield from self.raw_embed(batch)
            yield from self.raw_embed(documents)
        else:
            if parallel == 0:
                parallel = os.cpu_count()

            start_method = "forkserver" if "forkserver" in get_all_start_methods() else "spawn"
            params = {
                "model_name": model_name,
                "cache_dir": cache_dir,
                "k": self.k,
                "b": self.b,
                "delta": self.delta,
                "backend": self.backend,
                "language": self.language,
                "disable_stemmer": self.disable_stemmer,
            }
            pool = ParallelWorkerPool(
                num_workers=parallel or 1,
                worker=self._get_worker_class(),
                start_method=start_method,
            )
            for batch in pool.ordered_map(iter_batch(documents, batch_size), **params):
                for record in batch:
                    yield record

    def embed(
        self,
        documents: Union[str, Iterable[str]],
        batch_size: int = 256,
        parallel: Optional[int] = None,
        **kwargs,
    ) -> Iterable[SparseEmbedding]:
        """
        Encode a list of documents into list of embeddings.
        We use mean pooling with attention so that the model can handle variable-length inputs.

        Args:
            documents: Iterator of documents or single document to embed
            batch_size: Batch size for encoding -- higher values will use more memory, but be faster
                Batch size will only take effect, when running parallel (in such case beware of the Notice under
                parallel) 
            parallel:
                If > 1, data-parallel encoding will be used, recommended for offline encoding of large datasets.
                If 0, use all available cores.
                If None, don't use data-parallel processing, use default onnxruntime threading instead.
                Notice: parallel computation of embeddings using the BM25s package might not work as intended as the
                TF-IDF calculation will only be performed on the batch subset of the documents. For the native
                fastembed implementation of BM25 the IDF term have been ignore and the other documents only affect
                the TF score by the avg len of the documents (which per default is just a pre-fixed constant, that the
                user needs to claculate explicitly)

        Returns:
            List of embeddings, one per document
        """
        yield from self._embed_documents(
            model_name=self.model_name,
            cache_dir=str(self.cache_dir),
            documents=documents,
            batch_size=batch_size,
            parallel=parallel,
        )

    def raw_embed(
        self,
        documents: list[str],
    ) -> list[SparseEmbedding]:
        logger.debug(
            f"Fastembeds implementation of {self.model_name} is embedding a list of {len(documents)} documents.")
        bm25s_tokenized_docs = self.tokenizer.tokenize(documents, update_vocab=True, return_as="tuple")
        # Compute the BM25 scores
        self.bm25s_engine.index(bm25s_tokenized_docs)
        map_counter_id_to_hash_id = {}
        for stemmed_token, current_id in self.bm25s_engine.vocab_dict.items():
            token_id = self.compute_token_id(stemmed_token)
            map_counter_id_to_hash_id[current_id] = token_id
            
        vectorized_mapping = np.vectorize(lambda x: map_counter_id_to_hash_id.get(x, x), otypes=(np.int32,))

        embeddings = []
        
        # construct sparse array
        sparse_array = sp.csc_array((self.bm25s_engine.scores['data'],self.bm25s_engine.scores['indices'],self.bm25s_engine.scores['indptr']))
        # convert it to dictonary format
        sparse_array = sp.dok_array(sparse_array)
        for doc_id in range(sparse_array.shape[0]):
            index, bm25scores = zip(*sparse_array[[doc_id], :].items())
            _, token_id = zip(*index)
            token_hash_ids = vectorized_mapping(token_id)
            embeddings.append(SparseEmbedding(indices=token_hash_ids, values=np.array(bm25scores)))

        return embeddings


    @classmethod
    def compute_token_id(cls, token: str) -> int:
        return abs(mmh3.hash(token))

    def query_embed(self, query: Union[str, Iterable[str]], **kwargs) -> Iterable[SparseEmbedding]:
        """To emulate BM25 behaviour, we don't need to use weights in the query, and
        it's enough to just hash the tokens and assign a weight of 1.0 to them.
        """
        if isinstance(query, str):
            query = [query]

        self.tokenizer.reset_vocab()
        bm25s_tokenized_docs = self.tokenizer.tokenize(query, update_vocab=True, return_as="tuple")

        map_counter_id_to_hash_id = {}
        for stemmed_token, current_id in bm25s_tokenized_docs.vocab.items():
            token_id = self.compute_token_id(stemmed_token)
            map_counter_id_to_hash_id[current_id] = token_id

        vectorized_mapping = np.vectorize(lambda x: map_counter_id_to_hash_id.get(x, x),otypes=(np.int32,))

        for query_id in bm25s_tokenized_docs.ids:
            token_ids = vectorized_mapping(np.array(query_id))
            psedo_score = np.ones_like(token_ids)
            yield SparseEmbedding(indices=token_ids, values=psedo_score)


    @classmethod
    def _get_worker_class(cls) -> Type["Bm25Worker"]:
        return Bm25Worker


class Bm25Worker(Worker):
    def __init__(
        self,
        model_name: str,
        cache_dir: str,
        **kwargs,
    ):
        self.model = self.init_embedding(model_name, cache_dir, **kwargs)

    @classmethod
    def start(cls, model_name: str, cache_dir: str, **kwargs: Any) -> "Bm25Worker":
        return cls(model_name=model_name, cache_dir=cache_dir, **kwargs)

    def process(self, items: Iterable[tuple[int, Any]]) -> Iterable[tuple[int, Any]]:
        for idx, batch in items:
            onnx_output = self.model.raw_embed(batch)
            yield idx, onnx_output

    @staticmethod
    def init_embedding(model_name: str, cache_dir: str, **kwargs) -> Bm25:
        return Bm25(model_name=model_name, cache_dir=cache_dir, **kwargs)
