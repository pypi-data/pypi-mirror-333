from ultralytics import YOLO
import supervision as sv
from tqdm import tqdm 
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 
from src.model_face_detection.filter_step_2 import check_again
from sentence_transformers import SentenceTransformer
from skimage.metrics import structural_similarity as ssim
from uuid import uuid1
import os
from src.indexing.index import ImageRtreiver
from sentence_transformers import SentenceTransformer
from src.configuration.config import MODEL_FACE_DETECTION, MODEL_ENCODE_IMAGES
import faiss
class faceDetection:
    def __init__(self):
        self.model = YOLO(MODEL_FACE_DETECTION)
        self.indexes, self.image_paths = ImageRtreiver.load_faiss_index(index_path="src/model_index_info/indexed_data/face_to_catch_index")
        self.image_paths = list(map(lambda x: x+".png", self.image_paths[0].split(".pngn")))
        self.model_for_image_encoding = SentenceTransformer(MODEL_ENCODE_IMAGES)
    
    def retrieve_similar_images(self, query, top_k=3):
        try:
            query_features = self.model_for_image_encoding.encode(query)
            query_features = query_features.astype(np.float32).reshape(1, -1)
            faiss.normalize_L2(query_features)
            print(f"Query features shape: {query_features.shape}")
            print(f"FAISS index dimension: {self.indexes.d}")
            self.indexes.nprobe = 1
            # faiss.normalize_L2(query_features)
            distances, indices = self.indexes.search(query_features, top_k)
            
            retrieved_images = [self.image_paths[int(idx)] for idx in indices[0]]
            return query, retrieved_images, distances
        except Exception as e:
            print(f"Error in retrieve_similar_images: {e}")
            return query, [], np.array([])

    def save_images(self, cropped_face, retrieved_images, distances, save_path):
        """Save the cropped face and the retrieved similar images with distances."""
        try:
            # Create directory if it doesn't exist
            
            fig, axes = plt.subplots(1, len(retrieved_images) + 1, figsize=(10, 5))
            
            # Plot cropped face
            axes[0].imshow(cropped_face)
            axes[0].set_title("Cropped Face")
            axes[0].axis("off")

            # Plot retrieved images with distances
            for i, img_full_path in enumerate(retrieved_images):
                try:
                    
                    if os.path.exists(img_full_path):
                        img = Image.open(img_full_path)
                        axes[i + 1].imshow(img)
                        axes[i + 1].set_title(f"Match {i+1}\nDist: {distances[0][i]:.2f}")
                        axes[i + 1].axis("off")
                    else:
                        print(f"Image not found: {img_full_path}")
                except Exception as e:
                    print(f"Error loading image {img_full_path}: {e}")

            # Save the figure
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            plt.close(fig)  # Close the figure to free memory
        except Exception as e:
            print(f"Error in save_images: {e}")
    

            
    # Example of expanding a bbox in XYXY format
    def expand_bbox(self, bbox, expansion_factor=1.5, frame_shape=None):
        """
        Expand a bounding box by a given factor while ensuring it stays within frame boundaries
        bbox format: [x1, y1, x2, y2]
        """
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        
        # Calculate expansion amount
        w_expand = (expansion_factor - 1) * width / 2
        h_expand = (expansion_factor - 1) * height / 2
        
        # Expand the box
        new_x1 = x1 - w_expand
        new_y1 = y1 - h_expand
        new_x2 = x2 + w_expand
        new_y2 = y2 + h_expand
        
        # Ensure bbox stays within frame if frame_shape is provided
        if frame_shape is not None:
            frame_height, frame_width = frame_shape[:2]
            new_x1 = max(0, new_x1)
            new_y1 = max(0, new_y1)
            new_x2 = min(frame_width - 1, new_x2)
            new_y2 = min(frame_height - 1, new_y2)
        
        return np.array([new_x1, new_y1, new_x2, new_y2]).reshape(1, -1)
    def process_video(self, source_video_path, target_video_path, confidence_threshold=0.5, iou_threshold=0.3):
        """
        Process video to detect and track faces, identifying suspects based on similarity to reference images.
        
        Args:
            source_video_path (str): Path to the source video
            target_video_path (str): Directory to save the output
            confidence_threshold (float): Confidence threshold for face detection
            iou_threshold (float): IOU threshold for detection
        """
        try:
            # Create output directory
            os.makedirs(target_video_path, exist_ok=True)
            
            # Setup tracking and video processing
            tracker = sv.ByteTrack(minimum_consecutive_frames=10, lost_track_buffer=100)
            frame_generator = sv.get_video_frames_generator(source_path=source_video_path)
            video_info = sv.VideoInfo.from_video_path(video_path=source_video_path)
            
            # Output video setup with proper naming
            video_name = os.path.basename(source_video_path).split('.')[0]
            output_video_path = os.path.join(target_video_path, f"{video_name}_processed.mp4")
            
            # Annotation setup
            round_box_annotator = sv.RoundBoxAnnotator()
            label_annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER)
            
            # Tracking state
            suspect_track_ids = set()
            suspect_faces = []  # Store [cropped_image, retrieved_imgs, distances] for suspects
            processed_track_ids = set()  # Track IDs we've already processed
            
            # SIMILARITY_THRESHOLD determines when a face is considered a match
            SIMILARITY_THRESHOLD = 0.30
            
            # Process frames
            with sv.VideoSink(target_path=output_video_path, video_info=video_info) as sink:
                for frame_count, frame in enumerate(tqdm(frame_generator, total=video_info.total_frames)):
                    # Process at full frame rate for better tracking
                    results = self.model(frame, verbose=False, conf=confidence_threshold, iou=iou_threshold)[0]
                    detections = sv.Detections.from_ultralytics(results)
                    detections = tracker.update_with_detections(detections)
                    
                    # Prepare labels for this frame
                    labels = []
                    
                    for i, (xyxy, track_id) in enumerate(zip(detections.xyxy, detections.tracker_id)):
                        # Skip if empty detection or we already know this is a suspect
                        if track_id in suspect_track_ids:
                            labels.append(f"SUSPECT #{track_id}")
                            continue
                        
                        try:
                            # Only process each track_id once for efficiency
                            if f"SUSPECT #{track_id}" not in labels:
                                processed_track_ids.add(track_id)
                                
                                # Extract and prepare face image
                                xyxy = self.expand_bbox(list(xyxy), frame_shape=frame.shape)
                                cropped_image = sv.crop_image(image=frame, xyxy=xyxy)
                                
                                # Convert to RGB for the model
                                cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
                                img = Image.fromarray(cropped_image_rgb)
                                
                                # Find similar faces
                                _, retrieved_imgs, distances = self.retrieve_similar_images(img, top_k=1)
                                # Check if we found a suspect match
                                if len(retrieved_imgs) > 0 and distances[0][0] <= SIMILARITY_THRESHOLD:
                                    # if self.second_filter_check(np.array(img), retrieved_imgs) == "identical":
                                    matched_image = cv2.imread(retrieved_imgs[0])
                                    matched_image = cv2.cvtColor(matched_image, cv2.COLOR_BGR2RGB)
                                    second_filter= check_again(cropped_image_rgb, matched_image)
                                    print(second_filter)
                                    if second_filter == True:
                                        suspect_track_ids.add(track_id)
                                        suspect_faces.append([cropped_image_rgb, retrieved_imgs, [distances[0]]])
                                        labels.append(f"SUSPECT #{track_id}")
                                    else:
                                        labels.append(str(track_id))
                                else:
                                    labels.append(str(track_id))
                            else:
                                # We've seen this ID before but it's not a suspect
                                labels.append(f"SUSPECT #{track_id}")
                                
                        except Exception as e:
                            print(f"Error processing face {i} (track_id: {track_id}) in frame {frame_count}: {e}")
                            labels.append(str(track_id))  # Default label on error
                    
                    # Annotate and write frame
                    annotated_frame = round_box_annotator.annotate(scene=frame.copy(), detections=detections)
                    annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
                    sink.write_frame(annotated_frame)
                    
               
            
            # Save suspect face comparisons
            print(f"Found {len(suspect_faces)} suspect matches")
            for idx, (cropped_image, retrieved_imgs, distances) in enumerate(suspect_faces):
                suspect_id = f"suspect_{idx}_{int(distances[0][0]*100)}"
                save_path = os.path.join(target_video_path, f"{suspect_id}.jpg")
                self.save_images(cropped_image, retrieved_imgs, distances, save_path)
                
            return {
                "output_video": output_video_path,
                "suspect_count": len(suspect_faces),
                "processed_faces": len(processed_track_ids)
            }
                
        except Exception as e:
            print(f"Error in process_video: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}