import asyncio


def test_async_iterator_to_sync():
    async def foo():
        for i in range(10):
            print("---", i)
            yield i

    def bar():
        return asyncio.run(foo())

    for i in bar():
        print("++++", i)
