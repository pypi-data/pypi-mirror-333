import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2

class ImageSimilarity:
    def __init__(self, model_name='resnet50', threshold=0.8):
        """Initialize the image similarity detector with a pre-trained model"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.threshold = threshold
        
        # Load pre-trained model
        if model_name == 'resnet50':
            self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        elif model_name == 'resnet18':
            self.model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        
        # Remove the final fully connected layer
        self.model = nn.Sequential(*list(self.model.children())[:-1])
        self.model.to(self.device)
        self.model.eval()
        
        # Define image preprocessing for the model
        self.preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    
    def enhance_image(self, img, enhance_method='all'):
        """Enhance image quality before processing
        
        Parameters:
        - image_path: Path to the image
        - enhance_method: One of 'denoise', 'sharpen', 'contrast', 'sr' (super-resolution), or 'all'
        
        Returns:
        - Enhanced PIL Image
        """
        # Read image with OpenCV for preprocessing
        
        # Apply image enhancements based on selected method
        if enhance_method in ['denoise', 'all']:
            # Apply denoising
         
            img = img.astype(np.uint8)
            img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        
        if enhance_method in ['sharpen', 'all']:
            # Apply sharpening
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            img = cv2.filter2D(img, -1, kernel)
        
        if enhance_method in ['contrast', 'all']:
            # Enhance contrast using CLAHE
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            lab = cv2.merge((l, a, b))
            img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        if enhance_method in ['sr', 'all']:
            # Simple upscaling (for demonstration - real super-resolution would use a dedicated model)
            # First upscale by a factor of 1.5
            new_width = int(img.shape[1] * 1.5)
            new_height = int(img.shape[0] * 1.5)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            
            # Then downscale back to the original size for better quality
            original_width = int(new_width / 1.5)
            original_height = int(new_height / 1.5)
            img = cv2.resize(img, (original_width, original_height), interpolation=cv2.INTER_AREA)
        
        # Convert back to RGB for PIL
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img_rgb)
    
    def extract_features(self, image):
        """Extract features from a preprocessed image"""
        image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            features = self.model(image_tensor)
        
        # Flatten and normalize features
        features = features.squeeze().cpu().numpy()
        features = features / np.linalg.norm(features)
        return features
    
    def compute_similarity(self, features1, features2):
        """Compute cosine similarity between two feature vectors"""
        return np.dot(features1, features2)
    
    def compare_images(self, im1, im2, enhance_method='all'):
        """Compare two images and determine if they are similar"""
        # Load and enhance images
        image1 = self.enhance_image(im1, enhance_method)
        image2 = self.enhance_image(im2, enhance_method)
        
        # Store original images for display
        try:
            orig_img1 = Image.fromarray(im1).convert("RGB")
            orig_img2 = Image.fromarray(im2).convert("RGB")
            has_originals = True
        except:
            has_originals = False
        
        # Extract features
        features1 = self.extract_features(image1)
        features2 = self.extract_features(image2)
        
        # Compute similarity
        similarity = self.compute_similarity(features1, features2)
        
        # Determine if images are similar
        is_same = similarity > self.threshold
        
        result = {
            "similarity_score": similarity,
            "is_same": is_same,
            "features1": features1,
            "features2": features2,
            "enhanced1": image1,
            "enhanced2": image2
        }
        
        if has_originals:
            result["image1"] = orig_img1
            result["image2"] = orig_img2
        
        return result
    
    def show_comparison(self, result, show_enhanced=True):
        """Display the comparison results with original and enhanced images"""
        has_originals = "image1" in result and "image2" in result
        
        if show_enhanced and has_originals:
            # Create figure with original and enhanced images
            plt.figure(figsize=(12, 8))
            
            # Display original images
            plt.subplot(2, 2, 1)
            plt.imshow(result["image1"])
            plt.title("Image 1 (Original)")
            plt.axis('off')
            
            plt.subplot(2, 2, 2)
            plt.imshow(result["image2"])
            plt.title("Image 2 (Original)")
            plt.axis('off')
            
            # Display enhanced images
            plt.subplot(2, 2, 3)
            plt.imshow(result["enhanced1"])
            plt.title("Image 1 (Enhanced)")
            plt.axis('off')
            
            plt.subplot(2, 2, 4)
            plt.imshow(result["enhanced2"])
            plt.title("Image 2 (Enhanced)")
            plt.axis('off')
        else:
            # Just show enhanced images
            plt.figure(figsize=(10, 5))
            
            plt.subplot(1, 2, 1)
            plt.imshow(result["enhanced1"])
            plt.title("Image 1")
            plt.axis('off')
            
            plt.subplot(1, 2, 2)
            plt.imshow(result["enhanced2"])
            plt.title("Image 2")
            plt.axis('off')
        
        # Add similarity information
        plt.suptitle(f"Similarity Score: {result['similarity_score']:.4f}\n"
                    f"Images are {'the same' if result['is_same'] else 'different'}", 
                    fontsize=16)
        
        plt.tight_layout()
        plt.show()


# Example usage
def check_again(im1, im2):
    # Create image similarity detector
    detector = ImageSimilarity(model_name='resnet50', threshold=0.70)
    # Compare images with enhancement
    result = detector.compare_images(im1, im2, enhance_method='all')
    # Print results
    print(f"Similarity score: {result['similarity_score']:.4f}")
    print(f"Images are {'the same' if result['is_same'] else 'different'}")
    
    return result['is_same']