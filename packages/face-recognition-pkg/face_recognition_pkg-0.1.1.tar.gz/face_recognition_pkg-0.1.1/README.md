# Face Recognition Package

A Python package for face detection and recognition in images and videos.

## Installation

### Basic Installation

```bash
pip install face_recognition_pkg
```

### Hardware-specific Installation

For CPU-only environments:
```bash
pip install face_recognition_pkg[cpu]
```

For GPU-accelerated environments:
```bash
pip install face_recognition_pkg[gpu]
```

## Usage

### Face Detection

```python
from src.model_face_detection.face_model import FaceDetection

# Initialize face detection
face_object = FaceDetection()

# Process a video
face_object.process_video(
    source_video_path="path/to/video.mp4", 
    target_video_path="path/to/output.mp4"
)
```

### Image Indexing and Retrieval

```python
from src.indexing.index import ImageRetriever

# Initialize image retriever with a dataset
retriever = ImageRetriever(path_to_dataset_with_images="path/to/faces/dataset")

# Search for similar faces
```

## Features

- Face detection in images and videos
- Face recognition using FAISS index (supports both CPU and GPU)
- Batch processing of videos
- Customizable detection parameters

## License

MIT