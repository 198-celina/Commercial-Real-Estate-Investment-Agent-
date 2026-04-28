#!/usr/bin/env python3
"""
文档导入脚本 - 将 JSON 文档导入 Milvus 向量数据库
"""
import json
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.milvus_config import milvus_config
from rag.vector_store import vector_store


def load_documents(json_path: str) -> list:
    """加载 JSON 文档"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('documents', [])


def import_documents(documents: list):
    """导入文档到 Milvus"""
    print(f"开始导入 {len(documents)} 个文档...")
    
    for idx, doc in enumerate(documents, 1):
        title = doc.get('title', f'文档{idx}')
        content = doc.get('content', '')
        category = doc.get('category', 'unknown')
        source = doc.get('source', 'unknown')
        
        print(f"[{idx}/{len(documents)}] 导入: {title}")
        print(f"  类别: {category}")
        print(f"  来源: {source}")
        print(f"  内容长度: {len(content)} 字符")
        
        # 生成简单的向量（实际应该使用 Embedding 模型）
        # 这里使用简单的哈希向量作为演示
        embedding = generate_simple_embedding(content)
        
        try:
            vector_store.insert(
                embeddings=[embedding],
                contents=[content],
                titles=[title],
                sources=[source],
                categories=[category]
            )
            print(f"  ✅ 导入成功")
        except Exception as e:
            print(f"  ❌ 导入失败: {e}")
        
        print()
    
    print(f"导入完成！共导入 {len(documents)} 个文档")


def generate_simple_embedding(text: str, dim: int = 768) -> list:
    """
    生成简单向量（仅用于测试）
    实际应该使用专业的 Embedding 模型
    """
    import hashlib
    
    # 使用文本哈希生成伪向量
    embedding = []
    for i in range(dim):
        hash_input = f"{text}_{i}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        embedding.append((hash_value % 1000) / 1000.0)
    
    return embedding


if __name__ == "__main__":
    # 文档路径
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "sample_documents.json"
    )
    
    if not os.path.exists(json_path):
        print(f"❌ 文档文件不存在: {json_path}")
        sys.exit(1)
    
    # 加载文档
    documents = load_documents(json_path)
    print(f"✅ 加载 {len(documents)} 个文档")
    print()
    
    # 导入文档
    import_documents(documents)
