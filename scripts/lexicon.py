"""Pronunciation lexicon for the narrator. Edit per course; engine.py imports SPEECH and IPA.

SPEECH: (regex, replacement) respellings applied to narration text before synthesis.
        Use them for acronyms read letter by letter ("ETF" -> "E T F") or said as a word ("SEBI" -> "say-bee").
        Put plural forms before singular ones.
IPA:    word -> IPA string spliced straight into Kokoro's phonemes. Use it for names and non-English words
        the English phonemizer gets wrong. Check a word with:
            python3 -c "from kokoro_onnx import Kokoro as K; k=K('<models>/kokoro-v1.0.onnx','<models>/voices-v1.0.bin'); print(k.tokenizer.phonemize('Word','en-us'))"
        Use only symbols Kokoro knows (the existing entries show safe ones: ɾ ə ː ʊ dʒ ˈ).

The entries below come from the course this kit was built on (personal finance in India). Keep the generic
ones, delete what your course doesn't use, and add your own.
"""

SPEECH = [
    (r'\bETFs\b', 'E T Fs'), (r'\bETF\b', 'E T F'), (r'\bSIPs\b', 'S I Ps'), (r'\bSIP\b', 'S I P'),
    (r'\bIPOs\b', 'I P Os'), (r'\bIPO\b', 'I P O'), (r'\bFDs\b', 'F Ds'), (r'\bFD\b', 'F D'),
    (r'\bEMI\b', 'E M I'), (r'\bNAV\b', 'N A V'), (r'\bCAGR\b', 'C A G R'), (r'\bXIRR\b', 'X I R R'),
    (r'\bROE\b', 'R O E'), (r'\bEPS\b', 'E P S'), (r'\bEBITDA\b', 'ee-bit-dah'), (r'\bP/E\b', 'P E'),
    (r'\bSEBI\b', 'say-bee'), (r'\bRBI\b', 'R B I'), (r'\bUPI\b', 'U P I'), (r'\bTDS\b', 'T D S'),
    (r'\bSTCG\b', 'S T C G'), (r'\bLTCG\b', 'L T C G'), (r'\bSTT\b', 'S T T'), (r'F&O', 'F and O'),
    (r'\bREITs\b', 'reets'), (r'\bREIT\b', 'reet'), (r'\bAAA\b', 'triple A'),
]

IPA = {
    'crores': 'kəɾˈoːɾ', 'crore': 'kəɾˈoːɾ', 'lakhs': 'lˈɑːkʰs', 'lakh': 'lˈɑːkʰ', 'paise': 'pˈɛːseː',
    'rupees': 'ɾˈuːpiːz', 'rupee': 'ɾˈuːpiː', 'Kolkata': 'koːlkˈɑːtɑː', 'Nifty': 'nˈɪfti',
    'Rohan': 'ɾˈoːhən', 'Priya': 'pɾˈɪjɑː', 'Arjun': 'ˈəɾdʒʊn',
}
