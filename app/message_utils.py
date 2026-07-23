def extract_text_content(content):
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if isinstance(item.get("text"), str):
                    parts.append(item["text"])
                elif isinstance(item.get("content"), str):
                    parts.append(item["content"])
            else:
                text = getattr(item, "text", None)
                if isinstance(text, str):
                    parts.append(text)
                else:
                    parts.append(str(item))
        return " ".join(part for part in parts if part).strip()

    return str(content)
