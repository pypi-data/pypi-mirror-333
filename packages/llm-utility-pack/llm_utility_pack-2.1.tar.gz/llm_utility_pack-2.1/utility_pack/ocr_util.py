import pytesseract, os, cv2, numpy as np, os
from deskew import determine_skew
from pytesseract import Output
from skimage import filters
from PIL import Image

os.environ['OMP_THREAD_LIMIT'] = 1

def array_img(img, denoise=True):
    pil_image_rgb = img.convert('RGB')
    img = np.array(pil_image_rgb)

    if len(img.shape) == 3:
        if img.shape[2] > 1:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if denoise:
        img = cv2.fastNlMeansDenoising(img, None)

    return img

def rotate_image(pil_image, angle):
    return pil_image.rotate(angle, expand=True)

def sauvola_binarization(pil_image, window_size=15, k=0.2):
    # Open the image using Pillow
    pil_image = pil_image.convert('L')
    
    # Convert Pillow image to numpy array
    img_array = np.array(pil_image)
    
    # Perform Sauvola thresholding
    threshold = filters.threshold_sauvola(img_array, window_size=window_size, k=k)
    
    # Apply the threshold to create a binary image
    binary = img_array > threshold
    
    # Convert back to Pillow Image
    result = Image.fromarray((binary * 255).astype(np.uint8))
    
    return result

def raw_ocr_with_topbottom_leftright(image):
    # Raw extraction
    data = pytesseract.image_to_data(image, lang='por', output_type=Output.DATAFRAME)
    
    # Clean the data
    data = data.dropna(subset=['text'])
    data['text'] = data['text'].str.strip()

    # Sort by top position, then left position
    data_sorted = data.sort_values(['top', 'left'])

    # Group by top position (approximately) to get lines
    data_sorted['line_num'] = (data_sorted['top'] / 10).astype(int)

    # Concatenate text for each line
    result = data_sorted.groupby('line_num')['text'].apply(' '.join).reset_index()

    # Final text output
    text = '\n'.join(result['text'])

    return text

def ocr_image_pipeline(pil_image):
    try:
        text = ""

        # Binarize by default
        image_sauvola = sauvola_binarization(pil_image, window_size=15, k=0.08)

        # Detect rotation
        angle = determine_skew(array_img(image_sauvola, denoise=False)) * 0.85

        if angle != 0:
            image_sauvola = rotate_image(image_sauvola, angle)

        text = raw_ocr_with_topbottom_leftright(image_sauvola)
        text = text.replace('\x0c', '').strip()

        if text == "":
            text = raw_ocr_with_topbottom_leftright(pil_image)
            text = text.replace('\x0c', '').strip()

        while '  ' in text:
            text = text.replace('  ', ' ')
        
        while '\n ' in text:
            text = text.replace('\n ', '\n')
        
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')

        return text
    except Exception as e:
        print(e, flush=True)

    return ""
