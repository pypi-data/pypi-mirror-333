from typing import List, Any
from sentence_transformers import SentenceTransformer
import os 
from PIL import Image
import numpy as np
from src.configuration.config import MODEL_ENCODE_IMAGES
import faiss 
import gc
class ImageRtreiver:
    def __init__(self, path_to_dataset_with_images: str, output_path: str="src/model_index_info/indexed_data/face_to_catch_index"):
        gc.collect()
        self.path_to_dataset_with_images = path_to_dataset_with_images
        self.model_for_image_encoding = SentenceTransformer(MODEL_ENCODE_IMAGES)
        
        # let's list out all the images 
        self.all_encoded_images=[]
        self.all_images = []
        for img_name in os.listdir(self.path_to_dataset_with_images):
            path =os.path.join(self.path_to_dataset_with_images, img_name)
            if ".DS_Store" not in path:
                self.all_images.append(path)
                img = Image.open(path)
                self.all_encoded_images.append(self.encode_image(img))
                
        self.index_to_faiss = self.create_faiss_index(self.all_encoded_images, self.all_images, output_path)
    
    def encode_image(self, img) -> List[Any]:
        embedding = self.model_for_image_encoding.encode(img)
        return embedding
        
    def create_faiss_index(self, embeddings, image_paths, output_path):
        m = 2 # number of centroid IDs in final compressed vectors
        bits = 2 #
        dimension = len(embeddings[0])
        quantizer = faiss.IndexFlatL2(dimension)  # we keep the same L2 distance flat index
        index = faiss.IndexIVFPQ(quantizer, dimension, 2, m, bits) 

        vectors = np.array(embeddings).astype(np.float32)
        faiss.normalize_L2(vectors)
        index.train(vectors)

        # Add vectors to the index with IDs
        index.add(vectors)

        # Save the index
        faiss.write_index(index, output_path+".index")
        print(f"Index created and saved to {output_path}")

        # Save image paths
        with open(output_path + '.paths', 'w') as f:
            for img_path in image_paths:
                f.write(img_path + 'n')

        return index

    @staticmethod
    def load_faiss_index( index_path = "src/model_index_info/indexed_data/face_to_catch_index"):
        index = faiss.read_index(index_path+".index")
        with open(index_path + '.paths', 'r') as f:
            image_paths = [line.strip() for line in f]
        print(f"Index loaded from {index_path}")
        return index, image_paths

    