import streamlit as st
from PIL import Image
import io

st.title("Image Merger")

# Single file uploader for multiple images
uploaded_files = st.file_uploader("Upload exactly two images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) != 2:
        st.warning("Please upload exactly two images.")
    else:
        # Open and convert images to RGB
        images = [Image.open(file).convert("RGB") for file in uploaded_files]
        
        # Get dimensions of each image
        widths, heights = zip(*(img.size for img in images))
        total_width = sum(widths)
        max_height = max(heights)
        
        # Create a new blank image with a white background
        combined_image = Image.new("RGB", (total_width, max_height), "white")
        
        # Paste the images side by side
        x_offset = 0
        for img in images:
            combined_image.paste(img, (x_offset, 0))
            x_offset += img.width
        
        # Save the combined image as a PDF in an in-memory buffer
        pdf_buffer = io.BytesIO()
        combined_image.save(pdf_buffer, format="PDF")
        pdf_buffer.seek(0)

        st.image(combined_image, caption="Combined Image", use_column_width=True)
        
        st.success("PDF generated successfully!")
        st.download_button(
            label="Download Combined PDF",
            data=pdf_buffer,
            file_name="combined.pdf",
            mime="application/pdf"
        )
