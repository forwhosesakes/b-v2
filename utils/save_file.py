


from functools import wraps
import aiofiles
import tempfile
from utils.logger import timed


@timed
async def save_file(file_path, file):
     async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write


def temp_file_decorator(func):
    @wraps(func)
    def wrapper(large_file: bytes, *args, **kwargs):
        with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as temp_file:
            temp_file.write(large_file)
            temp_file.flush()
            result = func(temp_file.name, *args, **kwargs)
        return result
    return wrapper
    