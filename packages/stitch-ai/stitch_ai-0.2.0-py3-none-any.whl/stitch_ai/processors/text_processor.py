class TextProcessor:
    @staticmethod
    def chunk_text(text, chunk_size=2000, overlap=200):
        """Split text into overlapping chunks of approximately chunk_size characters"""
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            # Find the end of the chunk
            end = start + chunk_size
            
            # If this is not the last chunk, try to find a good breaking point
            if end < text_length:
                # Look for a period, question mark, or exclamation mark followed by a space
                for i in range(min(end + 100, text_length) - 1, start + chunk_size//2, -1):
                    if text[i] in '.!?' and text[i+1] == ' ':
                        end = i + 1
                        break
            else:
                end = text_length

            # Add the chunk to our list
            chunks.append(text[start:end].strip())
            
            # Move the start pointer, including overlap
            start = max(end - overlap, start + 1)
            
            # If we're near the end, just include the rest
            if text_length - start < chunk_size:
                if start < text_length:
                    chunks.append(text[start:].strip())
                break

        return chunks