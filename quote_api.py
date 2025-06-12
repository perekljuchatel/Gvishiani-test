import aiohttp

# quote_api.py

async def get_random_quote(api_url: str) -> str:
    """
    Получает случайную цитату из указанного API.

    Args:
        api_url (str): URL открытого API для получения цитат.

    Returns:
        str: Случайная цитата или сообщение об ошибке.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                response.raise_for_status()  # Вызовет исключение для кодов состояния HTTP 4xx/5xx
                data = await response.json()

                if isinstance(data, list) and data:
                    # Если API возвращает список (например, ZenQuotes API)
                    quote_text = data[0].get('q') or data[0].get('quote') or data[0].get('text')
                    quote_author = data[0].get('a') or data[0].get('author')
                else:
                    # Если API возвращает один объект
                    quote_text = data.get('quote') or data.get('content') or data.get('text')
                    quote_author = data.get('author')

                if quote_text:
                    if quote_author:
                        return f'"{quote_text}" - {quote_author}'
                    else:
                        return f'"{quote_text}"'
                else:
                    return "Не удалось получить цитату. Не найдено поле цитаты в ответе API."

    except aiohttp.ClientError as e:
        return f"Ошибка при подключении к API: {e}"
    except Exception as e:
        return f"Произошла непредвиденная ошибка: {e}"