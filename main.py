from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from typing import Iterator
import re

def create_translation_chain():
    # 翻訳用モデルの初期化
    translate_model = ChatOllama(
        model="7shi/gemma-2-jpn-translate:2b-instruct-q8_0",
        base_url="http://ollama:11434",
        temperature=0.0,
        streaming=True
    )
    return translate_model

def create_reasoning_chain():
    # 推論用モデルの初期化
    reasoning_model = ChatOllama(
        model="deepseek-r1:1.5b",
        base_url="http://ollama:11434",
        temperature=0.7,
        streaming=True
    )
    
    # 会話履歴用のメモリを初期化
    memory = ConversationBufferMemory(return_messages=True)
    
    # プロンプトテンプレートの作成（メモリを含む）
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Please provide a detailed and thoughtful response."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # チェーンの作成
    chain = prompt | reasoning_model | StrOutputParser()
    
    return chain, memory

def translate_to_english(translate_model, text) -> Iterator[str]:
    # 日本語から英語への翻訳
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Translate Japanese to English:"),
        ("assistant", "OK"),
        ("human", "{input}")
    ])
    chain = prompt | translate_model | StrOutputParser()
    return chain.stream({"input": text})

def translate_to_japanese(translate_model, text) -> Iterator[str]:
    # 英語から日本語への翻訳
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Translate English to Japanese:"),
        ("assistant", "OK"),
        ("human", "{input}")
    ])
    chain = prompt | translate_model | StrOutputParser()
    return chain.stream({"input": text})

def get_reasoning_response(chain, memory, text) -> Iterator[str]:
    # 会話履歴を含めて推論による回答生成
    memory_variables = memory.load_memory_variables({})
    response_stream = chain.stream({
        "input": text,
        "history": memory_variables["history"]
    })
    
    # 完全な応答を構築
    full_response = ""
    for chunk in response_stream:
        full_response += chunk
        yield chunk
    
    # 会話履歴の更新
    memory.save_context({"input": text}, {"output": full_response})

def main():
    print("チャットを開始します。終了するには 'exit' と入力してください。")
    
    # 各モデルの初期化
    translate_model = create_translation_chain()
    reasoning_chain, memory = create_reasoning_chain()
    
    while True:
        # ユーザー入力の受け取り
        user_input = input("\nあなた: ")
        
        if user_input.lower() == 'exit':
            print("チャットを終了します。")
            break

        try:
            # Step 1: 日本語から英語への翻訳
            print("\nStep 1. 日本語から英語への翻訳:")
            english_query = ""
            for chunk in translate_to_english(translate_model, user_input):
                english_query += chunk
                print(chunk, end="", flush=True)
            print("\n" + "-" * 100)

            # Step 2: 英語での回答生成
            print("Step 2. 英語での回答生成:")
            english_response = ""
            for chunk in get_reasoning_response(reasoning_chain, memory, english_query):
                english_response += chunk
                print(chunk, end="", flush=True)
            print("\n" + "-" * 100)

            # Step 3: 英語から日本語への翻訳
            print("Step 3. 英語から日本語への翻訳:")
            # </think>以降のテキストを抽出
            last_think_match = re.search(r'</think>', english_response, re.DOTALL)
            if last_think_match:
                english_answer = english_response[last_think_match.end():]
            else:
                english_answer = english_response

            print("AI: ", end="", flush=True)
            for chunk in translate_to_japanese(translate_model, english_answer):
                print(chunk, end="", flush=True)
            print("\n" + "-" * 100)

        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()