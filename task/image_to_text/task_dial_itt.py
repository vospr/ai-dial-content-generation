import asyncio
from io import BytesIO
from pathlib import Path

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


async def _put_image() -> Attachment:
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent.parent / file_name
    mime_type_png = 'image/png'
    
    # Create DialBucketClient
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as bucket_client:
        # Open image file
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
        
        # Use BytesIO to load bytes of image
        image_io = BytesIO(image_bytes)
        
        # Upload file with client
        upload_result = await bucket_client.put_file(
            name=file_name,
            mime_type=mime_type_png,
            content=image_io
        )
        
        # Return Attachment object with title (file name), url and type (mime type)
        return Attachment(
            title=file_name,
            url=upload_result.get('url'),
            type=mime_type_png
        )


def start() -> None:
    print("="*70)
    print("Testing DIAL-style Image Analysis with Bucket Storage")
    print("="*70)
    
    # Create DialModelClient
    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="gpt-4o",
        api_key=API_KEY
    )
    
    # Upload image (use `_put_image` method )
    attachment = asyncio.run(_put_image())
    
    # Print attachment to see result
    print(f"\n📎 Uploaded Attachment:")
    print(f"   Title: {attachment.title}")
    print(f"   URL: {attachment.url}")
    print(f"   Type: {attachment.type}\n")
    
    # Call chat completion via client with list containing one Message
    message = Message(
        role=Role.USER,
        content="What do you see on this picture? Describe it in detail.",
        custom_content=CustomContent(attachments=[attachment])
    )
    
    response = client.get_completion(messages=[message])
    print(f"\n✅ GPT-4o Response: {response.content}\n")
    
    # Try with Claude model
    print("="*70)
    print("Testing with Claude-3-7-Sonnet")
    print("="*70)
    
    claude_client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="claude-3-7-sonnet@20250219",
        api_key=API_KEY
    )
    
    claude_response = claude_client.get_completion(messages=[message])
    print(f"\n✅ Claude Response: {claude_response.content}\n")
    
    # Try with Gemini model
    print("="*70)
    print("Testing with Gemini-2.5-Pro")
    print("="*70)
    
    gemini_client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="gemini-2.5-pro",
        api_key=API_KEY
    )
    
    gemini_response = gemini_client.get_completion(messages=[message])
    print(f"\n✅ Gemini Response: {gemini_response.content}\n")


start()
