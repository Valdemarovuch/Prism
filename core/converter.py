"""Image conversion logic"""

import os
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIC support
register_heif_opener()


class ImageConverter:
    """Handles image format conversion"""
    
    @staticmethod
    def convert_image(filepath, target_format, output_dir, 
                     preserve_metadata=False, max_compression=False):
        """
        Convert a single image to target format
        
        Args:
            filepath: Path to source image
            target_format: Target format (lowercase)
            output_dir: Output directory
            preserve_metadata: Whether to preserve EXIF metadata
            max_compression: Whether to use maximum compression
            
        Returns:
            str: Path to saved file or None if error
        """
        try:
            # Open image
            img = Image.open(filepath)
            
            # Generate output path
            base_name = os.path.splitext(os.path.basename(filepath))[0]
            save_path = os.path.join(output_dir, f"{base_name}.{target_format}")
            
            # Prepare save arguments
            save_kwargs = {}
            
            # Format-specific conversions
            if target_format in ['jpg', 'jpeg']:
                img = img.convert("RGB")
                save_kwargs['quality'] = 85 if max_compression else 100
                
            elif target_format == 'png':
                save_kwargs['optimize'] = max_compression
                
            elif target_format == 'webp':
                save_kwargs['quality'] = 85 if max_compression else 100
                save_kwargs['method'] = 6
                
            elif target_format == 'gif':
                img = img.convert('P', palette=Image.ADAPTIVE)
                
            elif target_format == 'ico':
                img.save(save_path, format='ICO', sizes=[(256, 256)])
                return save_path
                
            elif target_format == 'pdf':
                img_rgb = img.convert('RGB')
                img_rgb.save(save_path, 'PDF', resolution=100.0)
                return save_path
            
            # Preserve metadata if enabled
            if preserve_metadata and hasattr(img, 'info'):
                exif_data = img.info.get('exif', b'')
                if exif_data:
                    save_kwargs['exif'] = exif_data
            
            # Save image
            img.save(save_path, **save_kwargs)
            return save_path
            
        except Exception as e:
            raise Exception(f"Error converting {filepath}: {str(e)}")
