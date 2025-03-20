import pickle
from datasketch import MinHash, MinHashLSH
from typing import List, Dict, Any
import os, tqdm
from multiprocessing import Pool, cpu_count
from functools import partial

class DocDeduplicator:
    def __init__(self, num_perm: int = 128, threshold: float = 0.7):
        """
        初始化去重器
        :param num_perm: MinHash的permutation数量
        :param threshold: Jaccard相似度阈值
        """
        self.num_perm = num_perm
        self.threshold = threshold
        self.lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
        self.doc_store: Dict[str, Any] = {}  # 存储原始文档内容

    def _create_minhash(self, text: str) -> MinHash:
        """创建MinHash对象"""
        m = MinHash(num_perm=self.num_perm)
        for word in text.split():
            m.update(word.encode('utf8'))
        return m
    
    @staticmethod
    def _process_document(doc_item: tuple[str, str], num_perm: int) -> tuple[str, MinHash]:
        """多进程处理单个文档"""
        doc_id, content = doc_item
        m = MinHash(num_perm=num_perm)
        for word in content.split():
            m.update(word.encode('utf8'))
        return doc_id, m

    def build_index(self, documents: Dict[str, str], index_path: str, num_workers: int = None):
        """构建索引并持久化（多进程优化）"""
        if num_workers is None:
            num_workers = cpu_count() - 1  # 默认使用所有可用CPU核心
            # num_workers = 2 # 默认使用所有可用CPU核心

        doc_items = list(documents.items())
        total_docs = len(doc_items)

        print(f"Building index for {total_docs} documents with {num_workers} workers...")

        # 使用多进程池和tqdm显示进度
        with Pool(processes=num_workers) as pool:
            process_func = partial(self._process_document, num_perm=self.num_perm)
            # 使用imap和tqdm组合显示进度
            results = list(tqdm.tqdm(
                # pool.imap(process_func, doc_items, chunksize=min(100, total_docs // num_workers)),
                pool.imap(process_func, doc_items, chunksize=1000),
                total=total_docs,
                desc="Processing documents"
            ))

        # 将结果插入LSH和doc_store
        for doc_id, minhash in tqdm.tqdm(results, desc="Inserting into LSH", total=total_docs):
            self.lsh.insert(doc_id, minhash)
            self.doc_store[doc_id] = documents[doc_id]

        self._save_index(index_path)
        print(f"Index saved to {index_path}")

    def check_duplicates(self, query_text: str) -> List[tuple[str, float]]:
        """
        检查重复文档
        :return: List of (doc_id, similarity_score)
        """
        query_minhash = self._create_minhash(query_text)
        similar_docs = self.lsh.query(query_minhash)
        
        results = []
        for doc_id in similar_docs:
            doc_minhash = self._create_minhash(self.doc_store[doc_id])
            similarity = query_minhash.jaccard(doc_minhash)
            if similarity >= self.threshold:
                results.append((doc_id, similarity))
        
        return sorted(results, key=lambda x: x[1], reverse=True)

    def is_duplicate(self, query_text: str) -> bool:
        """检查是否为重复文档"""
        results = self.check_duplicates(query_text)
        return len(results) > 0
    
    def _save_index(self, path: str):
        """保存索引到文件"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({
                'lsh': self.lsh,
                'doc_store': self.doc_store,
                'num_perm': self.num_perm,
                'threshold': self.threshold
            }, f)

    @classmethod
    def load_index(cls, path: str) -> 'DocDeduplicator':
        """从文件加载索引"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        dedup = cls(num_perm=data['num_perm'], threshold=data['threshold'])
        dedup.lsh = data['lsh']
        dedup.doc_store = data['doc_store']
        return dedup