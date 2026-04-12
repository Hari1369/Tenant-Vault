# import os
# from llama_cpp import Llama

# # BASE_DIR points to Tenant-Vault/
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MODEL_PATH = os.path.join(BASE_DIR, "llm_models", "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

# print("[LLM] Loading model... please wait")

# llm = Llama(
#     model_path=MODEL_PATH,
#     n_ctx=1024,
#     n_threads=4,
#     n_batch=256,
#     n_gpu_layers=0,
#     verbose=False
# )

# print("[LLM] Model loaded successfully")

# SYSTEM_PROMPT = """You are an HR assistant agent for a multi-tenant employee management system.
# You help users fetch employee data step by step.
# Rules:
# - Ask ONE question at a time
# - Be concise and professional
# - When you have DB data injected as [DB DATA], present it clearly to the user
# - Ask for specific fields (phone, email) when user wants employee details
# """

# LLM_OPTIONS = {
#     "1": "I want employee details",
#     "2": "I want to See the Domain",
#     "3": "I want to See the User",
# }

# def show_options():
#     print("\n[LLM] What would you like to do?")
#     print("  1. I want employee details")
#     print("  2. I want to See the Domain")
#     print("  3. I want to See the User")

# def ask_llm(history):

#     prompt = f"<|system|>\n{SYSTEM_PROMPT}</s>\n"

#     for msg in history:
#         role    = msg["role"]
#         content = msg["content"]

#         if role == "user":
#             prompt += f"<|user|>\n{content}</s>\n"

#         elif role == "assistant":
#             prompt += f"<|assistant|>\n{content}</s>\n"

#     prompt += "<|assistant|>\n"

#     response = llm(
#         prompt,
#         max_tokens=256,
#         temperature=0.7,
#         stop=["</s>", "<|user|>", "<|system|>"],
#         echo=False
#     )

#     return response["choices"][0]["text"].strip()


# # ─────────────────────────────────────────
# #  MAIN FLOW
# # ─────────────────────────────────────────

# history = []

# show_options()

# choice = input("\nEnter your choice (1/2/3): ").strip()

# if choice in LLM_OPTIONS:
#     selected = LLM_OPTIONS[choice]

#     history.append({
#         "role"   : "user",
#         "content": selected
#     })

#     llm_reply = ask_llm(history)           # LLM generates reply

#     print(f"\n[LLM] {llm_reply}")          # show LLM reply in terminal

#     history.append({                       # save LLM reply into history
#         "role"   : "assistant",
#         "content": llm_reply
#     })

# else:
#     print("[LLM] Invalid choice. Please enter 1, 2 or 3.")



import os
from llama_cpp import Llama

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "llm_models", "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

print("[LLM] Loading model... please wait")

llm = Llama(
    model_path    = MODEL_PATH,
    n_ctx         = 1024,
    n_threads     = 4,
    n_batch       = 256,
    n_gpu_layers  = 0,
    verbose       = False
)

print("[LLM] Model loaded successfully")


SYSTEM_PROMPT = """You are an HR assistant for a multi-tenant employee system.
You ONLY answer using the data given to you inside [DB DATA].
Rules:
- NEVER make up any data
- NEVER show fields that are not in [DB DATA]
- NEVER say 'No data provided' or 'Not available' for missing fields — just skip them completely
- ONLY display the exact fields present in [DB DATA]
- Keep the response short and clean
"""


def ask_llm(history):
    prompt = f"<|system|>\n{SYSTEM_PROMPT}</s>\n"

    for msg in history:
        role    = msg["role"]
        content = msg["content"]

        if role == "user":
            prompt += f"<|user|>\n{content}</s>\n"
        elif role == "assistant":
            prompt += f"<|assistant|>\n{content}</s>\n"
        elif role == "system":
            prompt += f"<|system|>\n{content}</s>\n"

    prompt += "<|assistant|>\n"

    response = llm(
        prompt,
        max_tokens = 256,
        temperature = 0.3,        # Lower = less hallucination
        stop        = ["</s>", "<|user|>", "<|system|>"],
        echo        = False
    )

    return response["choices"][0]["text"].strip()