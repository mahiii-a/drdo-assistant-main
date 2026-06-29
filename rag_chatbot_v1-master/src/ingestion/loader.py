import os
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader,Docx2txtLoader,TextLoader,CSVLoader,UnstructuredExcelLoader,UnstructuredHTMLLoader
from langchain_core.documents import Document

class DocumentLoader:
    LOADER_MAP = {
        ".pdf":PyMuPDFLoader,
        ".docx":Docx2txtLoader,
        ".txt":TextLoader,
        ".csv":CSVLoader,
        ".xlsx":UnstructuredExcelLoader,
        ".html":UnstructuredHTMLLoader
    }

    def load_data(self,filepath: str)->List[Document]:
        ext=Path(filepath).suffix.lower()
        if ext not in self.LOADER_MAP:
            print(f"Unsupported format: {ext}")
            return []
        
        try:
            loader_class=self.LOADER_MAP[ext]
            loader=loader_class(filepath)
            documents= loader.load()
            for doc in documents:
                doc.metadata["source_file"]=Path(filepath).name
                doc.metadata["file_type"]=ext
            return documents
        
        except Exception as e:
            print(f"Error loading {Path(filepath)}")
            return []
        
        
        

