from langchain_community.llms import LlamaCpp

llm = LlamaCpp(model_path="./llama-2-13b-chat.Q5_K_M.gguf", n_ctx=1024)

message = "hi, what is your name?"
prompt = (
    "[INST] <<SYS>>\n"
    "You are Alex, a helpful assistant. Only answer the user's latest message, concisely.\n"
    "<</SYS>>\n"
    f"{message} [/INST]"
)
response = llm.invoke(prompt, max_tokens=32, stop=["[/INST]"])
print(response)