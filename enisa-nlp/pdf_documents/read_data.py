from pathlib import Path
import pandas as pd
import json

def read_plaintext_with_keywords(pdf_reports_path):
    """Return the plain text of the PDF reports together with the keywords and topics."""

    path = (Path(pdf_reports_path) / "tags.csv").resolve()
    tags = pd.read_csv(str(path))

    df = pd.DataFrame(columns=["filename", "title", "keywords", "topics", "text", "metadata"])

    path = (Path(pdf_reports_path) / "plaintext").resolve()
    idx = 0
    for path in Path(path).iterdir():
        if path.suffix == '.json':
            with path.open() as json_file:
                parsed = json.load(json_file)
                filename = path.stem

                # Some documents do not have title among metadata.
                title = parsed["metadata"]["title"] if "title" in parsed["metadata"].keys() else filename

                topics = tags[tags.name == filename].topics.get_values()[0]
                topics = topics.replace('\'', '\"')
                topics = json.loads(topics)

                keywords = tags[tags.name == filename].keywords.get_values()[0]
                keywords = keywords.replace('\'', '\"')
                keywords = json.loads(keywords)

                df.loc[idx] = [filename, title, keywords, topics, parsed["content"], parsed["metadata"]]
                idx += 1

    df['num_keywords'] = df.keywords.apply(lambda x: len(x))
    df['num_keywords'].value_counts()

    df['num_topics'] = df.topics.apply(lambda x: len(x))
    df['num_topics'].value_counts()

    return df
