from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from openai import OpenAI
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

async def chat_stream(question: str) -> AsyncGenerator[str, None]:
    """
    与OpenAI API进行流式对话
    
    Args:
        question: 用户输入的问题
    
    Yields:
        str: 流式返回的回答内容
    """
    try:
        # 创建聊天完成请求
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 或者使用其他模型，如 "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            stream=True,
            temperature=0.7,
            max_tokens=1000
        )
        
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream_chat")
async def stream_chat(param: str):
    """
    处理流式聊天请求的端点
    
    Args:
        param: 用户的问题
    
    Returns:
        StreamingResponse: 流式响应对象
    """
    return StreamingResponse(
        chat_stream(param),
        media_type="text/event-stream"
    )
