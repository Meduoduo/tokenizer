import tiktoken

def openai_num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return openai_num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return openai_num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    
    if type(messages) is str:
        return len(encoding.encode(messages))

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            if value is None:
                continue
            num_tokens += len(encoding.encode(str(value)))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

# openai's token price, in USD/1000 tokens
# input cost
OPENAI_TOKEN_PRICE = {
    'gpt-3.5-turbo-0613': 0.0015,
    'gpt-3.5-turbo-16k-0613': 0.003,
    'gpt-4-0314': 0.03,
    'gpt-4-32k-0314': 0.06,
    'gpt-4-0613': 0.03,
    'gpt-4-32k-0613': 0.06,
    'gpt-3.5-turbo-0301': 0.0015,
    'gpt-3.5-turbo-0613': 0.0015,
    'gpt-3.5-turbo': 0.0015,
    'gpt-4': 0.03,
}

def get_token_cost(model: str, tokens: int) -> float:
    """Return the price of tokens in USD."""
    if model not in OPENAI_TOKEN_PRICE:
        return 0
    return tokens * OPENAI_TOKEN_PRICE[model] / 1000
    