import asyncio
from datetime import datetime

from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role

class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - ‘hd’ creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"

async def _save_images(attachments: list[Attachment]):
    # Create DIAL bucket client
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as bucket_client:
        # Iterate through Images from attachments, download them and then save here
        for i, attachment in enumerate(attachments, 1):
            if attachment.url:
                # Download image from bucket
                image_bytes = await bucket_client.get_file(attachment.url)
                
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_image_{timestamp}_{i}.png"
                
                # Save image locally
                with open(filename, 'wb') as f:
                    f.write(image_bytes)
                
                # Print confirmation that image has been saved locally
                print(f"✅ Image saved locally as: {filename}")


def start() -> None:
    print("="*70)
    print("Testing Text-to-Image Generation with DALL-E 3")
    print("="*70)
    
    # Create DialModelClient for DALL-E 3
    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="dall-e-3",
        api_key=API_KEY
    )
    
    # Generate image for "Sunny day on Bali"
    prompt = "Sunny day on Bali with beautiful beach, palm trees, and crystal clear water"
    
    message = Message(
        role=Role.USER,
        content=prompt
    )
    
    print(f"\n🎨 Generating image with prompt: '{prompt}'\n")
    
    # Generate image with DALL-E 3
    response = client.get_completion(
        messages=[message],
        custom_fields={
            "size": Size.square,
            "quality": Quality.hd,
            "style": Style.vivid
        }
    )
    
    # Get attachments from response and save generated image
    if response.custom_content and response.custom_content.attachments:
        print(f"\n📎 Generated {len(response.custom_content.attachments)} image(s)")
        asyncio.run(_save_images(response.custom_content.attachments))
    else:
        print("⚠️ No images were generated")
    
    print("\n" + "="*70)
    print("✅ Text-to-Image generation completed successfully!")
    print("="*70)


start()
