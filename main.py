import sys
import random

def log(msg):
    print(msg, file=sys.stderr)

def generate_funny_response(text):
    jokes = [
        f"You said: '{text}', but I heard 'I'm hungry!' — go eat!",
        f"'{text}'? That's what she said.",
        f"I once knew a chatbot who said '{text}', and they never recovered.",
        f"Interesting... '{text}' sounds like a great movie title.",
        f"Echoing with style: '{text}' 🔊",
        f"That reminds me of the time I almost learned Python."
    ]
    return random.choice(jokes)

def main():
    log("Funny MCP Server started")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        log(f"Received input: {line}")
        response = generate_funny_response(line)
        print(response, flush=True)
        log(f"Responded with: {response}")

if __name__ == "__main__":
    main()
