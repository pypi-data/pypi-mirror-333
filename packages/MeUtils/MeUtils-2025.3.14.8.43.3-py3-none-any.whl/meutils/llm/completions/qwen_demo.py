
from openai import OpenAI
cookies={'ssxmod_itna': 'euitD57IejxAo=DhODcmmv30j=DKDODl4BtGRDeq7tDRDFqAPiDHA17P5DU2OY2MGXxGDaieAqzRxGXxaexiNDAxq0iDCbeQ5ou2ivv3e3nemU4qRhnub1G7NQgR3+H3utAR5RMFgYDHxi8DBF4wCGYDenaDCeDQxirDD4DADibq4D1IDDkD0+m7UovW4GWDmbADYHGf78fDGpobRAfbDDCbPYDwEbpzDDzzQj5PmAqPm3DePAfIjkIoAQxb4G1fD0HaG65bzk9kMxA3d=xvUewDlFSDCKvu+gUuWEA1zSrtjeYtY+sYFrT+0x3GqliqB5Y7Di7i4nhhlwNf0xWA5DTttRPa4DG35zY=eBY3E5QiefL1XdWqbz+DreA=dh=2WeKR58GYxEwgG5/DYMADaA5+A4PADN0=a7eziDD',
 'ssxmod_itna2': 'euitD57IejxAo=DhODcmmv30j=DKDODl4BtGRDeq7tDRDFqAPiDHA17P5DU2OY2MGXxGDaieAqzexD3raKY3rh4DFxnDKW1Bh0xDlxkDasWVgcuBepTBPecj=tk1QFgt3HxjB3pxx9=sdl5aSW9DG1yipgx+wgIO0mcDAoYQfrF4/xT++xEk02A7+4mHPbOA+oTOQBaahcHEWZfG3bok7rP8PcI8uRYYIUAHo0yE6aPp54bX0EQ8rUIHKYdC/1pjy6d0WqM90CG0PoMmhv3xrXwjP37hf4EgwgGqSxAhSaPAVxzGQUop4MXgBE+OX0DUmE5/no9eKynE/hjA6ECEP=oKnQo1DIjDq/YN00voKx0nLPbb3SG4DI4ZA/25ynwKc2a6rOEIQrN3+u0AiDbI5O2MCTK+LFfvq40LOQOALmFP0=bdo3w8onWpA+dhzA0C51ahgZjkR3y7olY=k8XW1ugrtAOIxC57jtViIOUdBtt7=D/0NE1oTf0k/d5aircE6f056c4rUy=c4wrh9XnhL1bIL9XZxdAcj8/YK4cRQN7Cc=XH6BTNFiFbTaOLxhrim5Q8p40K5fPAD4Ke+CYKKim2WDyieFrU3AqcDjfiGyUvmkP10CsY=3ZeLCx6YpkcELdkcAwlitYm6sFGq1tRkPRQewwrUYKiBh42Dzlpu=EuoV4aD2w24mPiDu1DZ51o3DA9ZW3h5leHGnB5Crc1KTbP03C2qlGQBezsq0xiHBeHDxncUxHTANQktHZ1KkxS6Hy4qQklKcxsKrxAqr2rmq32tnqViiY1spUPPi2mAw5hDD'}
cookie = '; '.join([f'{i}={j}' for i,j in cookies.items()])

headers = {
    # 'authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjIxZDJiMjhmLWZmMTctNGQ2MS1hYmI0LWM2NzJhZWNjMTQ5ZCIsImV4cCI6MTc0MzkzNTk1OX0.y3oSO7aOwmzuE3GI3_aSxd9c5iXz9Krw0zJDG1FCLBQ',
             'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
             'cookie':cookie
         }
client=OpenAI(base_url='https://chat.qwen.ai/api',
         api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjIxZDJiMjhmLWZmMTctNGQ2MS1hYmI0LWM2NzJhZWNjMTQ5ZCIsImV4cCI6MTc0MzkzNTk1OX0.y3oSO7aOwmzuE3GI3_aSxd9c5iXz9Krw0zJDG1FCLBQ',
         # default_headers=headers
             )

comp=client.chat.completions.create(
    model="qwen-max-latest", 
    messages=[{"role": "user", "content": "你好"}],
    max_tokens=2,
    # extra_headers=headers, # 放在这里也可以
    extra_body={'chat_type':'t2t'},
    stream=False
)
print(comp.choices[0].message.content)
# comp