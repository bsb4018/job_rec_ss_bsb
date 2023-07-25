from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    jobs_file_path: str

@dataclass
class EmbedIndexingArtifact:
    faiss_index_file_path: str