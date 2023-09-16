import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Create Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_api_key = os.getenv("SUPABASE_API_KEY")
bucket_name = os.getenv("BUCKET_NAME")
supabase = create_client(supabase_url, supabase_api_key)

# Upload file using standard upload
async def upload_file(file_path, file):
    response = await supabase.storage.from_(bucket_name).upload(file_path, file)
    if response.error:
        # Handle error
        print(f"Error: {response.error}")
    else:
        # Handle success
        print("File uploaded successfully!")
