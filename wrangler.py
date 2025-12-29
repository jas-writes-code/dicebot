import json

def thatstoolong(text: str, limit: int = 1900) -> list[str]:
    chunks = []
    remaining = text

    while len(remaining) > limit:
        # Try to split at the last double newline before limit
        split_index = remaining.rfind("\n\n", 0, limit)
        if split_index != -1:
            split_index += 2  # include the "\n\n"
            chunks.append(remaining[:split_index])
            remaining = remaining[split_index:]
            continue

        # If no "\n\n" found, try splitting at the last space before limit
        split_index = remaining.rfind(" ", 0, limit)
        if split_index != -1:
            chunks.append(remaining[:split_index])
            remaining = remaining[split_index + 1:]
            continue

        # As a last resort, hard cut
        chunks.append(remaining[:limit])
        remaining = remaining[limit:]

    # Add whatever is left
    if remaining:
        chunks.append(remaining)

    return chunks

async def find(char):
    global character
    character = None
    with open("config.json", "r") as f:
        config = json.load(f)
    for element in config["characters"]:
        if char == config["characters"][element]["name"]:
            character = config["characters"][element]
        if char in config["characters"][element]["aliases"]:
            character = config["characters"][element]
    for element in config["characters"]:
        if char == element:
            character = config["characters"][element]
    return character, character['uuid']