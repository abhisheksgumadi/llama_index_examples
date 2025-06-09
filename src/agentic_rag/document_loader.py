from typing import List
from pathlib import Path
from llama_index.readers.file import UnstructuredReader
from llama_index.core import Document


class DocumentLoader:
    def __init__(self, documents_dir: str = "./documents/"):
        self.reader = UnstructuredReader()
        self.documents_dir = documents_dir

    def load_documents(self) -> List[Document]:
        all_files_gen = Path(self.documents_dir).rglob("*")
        all_files = [f.resolve() for f in all_files_gen]

        docs = []
        for idx, f in enumerate(all_files):
            print(f"Idx {idx}/{len(all_files)}")
            loaded_docs = self.reader.load_data(file=f, split_documents=True)

            loaded_doc = Document(
                text="\n\n".join([d.get_content() for d in loaded_docs]),
                metadata={"path": str(f)},
            )
            print(loaded_doc.metadata["path"])
            docs.append(loaded_doc)

        return docs
