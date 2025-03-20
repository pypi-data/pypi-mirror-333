# 构建索引
# from minhash_index import DocDeduplicator
from glan2_dedup.minhash_index import DocDeduplicator
from multiprocessing import Pool, cpu_count, freeze_support

if __name__ == "__main__":
    freeze_support()
    # 准备文档
    documents = {
        'doc1': '这是一个测试文档 about machine learning',
        'doc2': '另一个关于machine learning的文档',
        'doc3': '完全不同的内容 about something else'
    }

    # 创建并构建索引
    dedup = DocDeduplicator(num_perm=256, threshold=0.8)
    dedup.build_index(documents, 'index/minhash_index.pkl')

    # 检查新文档
    new_text = '新的machine learning文档'
    new_text = '完全不同的内容 about something else'
    results = dedup.check_duplicates(new_text)
    print(f"新文档: {new_text}")
    print(results)
    print("相似文档:")
    for doc_id, similarity in results:
        print(dedup.doc_store[doc_id])
        print(f"相似文档: {doc_id}, 相似度: {similarity:.3f}")

    # 加载现有索引
    dedup_loaded = DocDeduplicator.load_index('index/minhash_index.pkl')