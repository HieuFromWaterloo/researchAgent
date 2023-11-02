# agent will remember up to MAX_TOKEN_MEMORY previous tokens in the convo chain
MAX_TOKEN_MEMORY=1_000
# if the scraped content is too long, then we summarize every chunk of text with 10_000 tokens each
MAX_TEXT_CHUNK_LEN=10_000
LLM_TEMPERATURE=0 # no bull shit
LLM_MODEL_ARCH='gpt-3.5-turbo-16k-0613'