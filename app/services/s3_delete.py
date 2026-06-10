from services.s3_settings import client, BUCKET_NAME

async def delete_file_to_s3(file_name: str):

    try:
        client.remove_object(
            bucket_name=BUCKET_NAME,
            object_name=file_name,
        )
        return True

    except Exception as e:
        print(e)
        return False