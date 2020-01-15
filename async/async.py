import asyncio
from time import sleep
import numpy as np
from random import choice, randint

async def api (x):
    value = randint(1,1000)
    await asyncio.sleep(0.01*value)
    print(f'done {0.01*value}')
    if x:
        return 'banana'
    else:
        return 'cenoura'

async def run():
    group = [choice([True, False]) for _ in range(300)]
    fruits = []
    k=0
    for i in group:
        k+=1
        fruit = loop.create_task(api(i))
        fruits.append(fruit)
        if k > 30:
            await asyncio.wait(fruits)
            fruits = []
            k=0
        
    await asyncio.wait(fruits)
    return fruits

if __name__ == "__main__":  
    loop = asyncio.get_event_loop()
    fruit = loop.run_until_complete(run())
    # for i in fruit:
    #     print(i.result())
    loop.close()
