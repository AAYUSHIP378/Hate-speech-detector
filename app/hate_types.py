# app/hate_types.py

HATE_KEYWORDS = {
    "Religion": [
        "muslim", "hindu", "islam", "christian", "mandir", "masjid",
        "allah", "ram", "jesus"
    ],

    "Gender": [
        "woman", "women", "girl", "girls", "female",
        "male", "men", "boy", "boys"
    ],

    "Caste": [
        "sc", "st", "obc", "dalit", "brahmin", "chamar"
    ],

    "Race": [
        "black", "white", "african", "asian"
    ],

    "Political": [
        "bjp", "congress", "modi", "rahul", "government", "party"
    ],

    "Abusive": [
        "ganda", "kutte", "harami", "ullu", "pagal", "idiot"
    ]
}


def detect_hate_type(text: str):

    text = text.lower()

    for hate_type, keywords in HATE_KEYWORDS.items():
        for word in keywords:
            if word in text:
                return hate_type

    return "General Hate"
