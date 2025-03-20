import json
import tqdm
# from minhash_index import DocDeduplicator
from glan2_dedup.minhash_index import DocDeduplicator

def dedup(data):
    import re  
 
    # 通用的论坛名称匹配模式  
    domain_pattern = r'[a-zA-Z0-9.-]+\.(com|org|net|edu|gov|io|info|biz|co)'  
   
    # 正则表达式模式（组合多个可能的前缀和后缀）  
    prefix_pattern = (  
        r'Below you are given code written in [a-z]+ that contains the function \'stuff\', which manipulates a string, as well as an input to the function. Your job is to predict the output of \'stuff\' given the provided input.\n\n'  
        r'|Solve the following coding problem using the programming language [a-z]+:\n\n'  
        r'|Below is a question asked on the forum ' + domain_pattern + r'\. Provide a good and informational response to it like a helpful human would.\n\n'  
    )  
    suffix_pattern = (  
        r'\n\nReturn your final response as \'Final Answer: \\boxed{<answer>}\', where <answer> is the number or mathematical expression of the solution.'  
    )  
   
    # 用于去重的集合和列表  
    unique_items = []  
   
    for item in data:  
        item_unique = False  
        content = item['messages'][0]['content'].strip()            
        # 去掉前缀和后缀，并去掉结果中的前后空白字符  
        processed_content = re.sub(prefix_pattern, '', content).strip()  
        processed_content = re.sub(suffix_pattern, '', processed_content).strip()  
           
        # 新的首行和尾行替换逻辑  
        if processed_content.startswith("Return your final response within \\boxed{}."):  
            processed_content = processed_content[len("Return your final response within \\boxed{}."):].strip()  
 
        if processed_content.endswith("Please reason step by step, and put your final answer within \\boxed{}."):  
            processed_content = processed_content[:-len("Please reason step by step, and put your final answer within \\boxed{}.")].strip()  
        unique_items.append(processed_content)
        # 检查处理后的内容是否在集合中  
        # if processed_content not in unique_contents:  
        #     unique_contents.add(processed_content)  
        #     item_unique = True  
   
        # # 如果item中有任何消息内容是唯一的，添加整个item到列表中  
        # if item_unique:  
        #     unique_items.append(item)  
    print(f"Original data size: {len(data)}, Deduped data size: {len(unique_items)}")
    return unique_items
 
from multiprocessing import Pool, cpu_count, freeze_support

if __name__ == "__main__":
    # freeze_support()
    # # load data
    # data = []
    # # with open(r"D:\2025\temp\add_synthetic_openr1_openthought_aime_rej_kodcode_taco_aops_1066k.jsonl", 'r', encoding='utf-8') as reader:
    # with open(r"D:\2025\temp\add_synthetic_openr1_openthought_aime_rej_kodcode_taco_aops_1066k.jsonl", 'r', encoding='utf-8') as reader:
    #     for line in tqdm.tqdm(reader):
    #         obj = json.loads(line)
    #         data.append(obj)
    # unique_items = dedup(data)

    # 准备文档
    # documents = {
    #     str(i): item for i, item in enumerate(unique_items)
    # }

    # print(f"Unique items: {len(documents)}")
    # # 创建并构建索引
    # dedup = DocDeduplicator(num_perm=256, threshold=0.8)
    # dedup.build_index(documents, 'index/250314_syn1_opner1_openthouhgt_kodcode_xx-aime_xx-taco-syn_xx-aops.pkl')

    # 检查新文档
    new_text = '新的machine learning文档'
    new_text = '完全不同的内容 about something else'
    results = dedup.check_duplicates(new_text)

    for doc_id, similarity in results:
        print(dedup.doc_store[doc_id])
        print(f"相似文档: {doc_id}, 相似度: {similarity:.3f}")

    # 加载现有索引
    dedup_loaded = DocDeduplicator.load_index('index/minhash_index.pkl')