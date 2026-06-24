from datetime import datetime


def log_question(question, sources):

    with open(
        "retrieval.log",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"\n[{datetime.now()}]\n"
        )

        f.write(
            f"QUESTION: {question}\n"
        )

        for source in sources:

            f.write(
                f"PAGE: {source['page']}\n"
            )

        f.write("\n")