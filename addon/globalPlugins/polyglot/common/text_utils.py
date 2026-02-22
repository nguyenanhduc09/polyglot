# -*- coding: utf-8 -*-

def split_text(text: str, max_length: int) -> list[str]:
	"""
	Splits text into chunks of at most max_length characters using a recursive approach.
	Attempts to split at natural boundaries like paragraphs, sentences, and words.
	"""
	if max_length <= 0 or len(text) <= max_length:
		return [text]

	def _split(current_text: str, separators: list[str]) -> list[str]:
		if len(current_text) <= max_length:
			return [current_text]
		if not separators:
			return [current_text[i:i+max_length] for i in range(0, len(current_text), max_length)]
		
		sep = separators[0]
		if sep == '':
			return [current_text[i:i+max_length] for i in range(0, len(current_text), max_length)]
			
		chunks = current_text.split(sep)
		new_chunks = []
		for i, chunk in enumerate(chunks):
			if i < len(chunks) - 1:
				new_chunks.append(chunk + sep)
			else:
				if chunk:
					new_chunks.append(chunk)
					
		result = []
		current_chunk = ""
		
		for c in new_chunks:
			if len(c) > max_length:
				if current_chunk:
					result.append(current_chunk)
					current_chunk = ""
				# Recursively split the oversized chunk with remaining separators
				sub_chunks = _split(c, separators[1:])
				result.extend(sub_chunks)
			else:
				if len(current_chunk) + len(c) <= max_length:
					current_chunk += c
				else:
					if current_chunk:
						result.append(current_chunk)
					current_chunk = c
					
		if current_chunk:
			result.append(current_chunk)
			
		return result

	return _split(text, ['\n\n', '\n', '. ', '。', ' ', ''])
