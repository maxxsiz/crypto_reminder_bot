from misc import dp, bot


async def send_value_reminder(data):
    await bot.send_message(int(data['tel_id']),data)

async def send_simple_reminder(data):
    await bot.send_message(int(data['tel_id']),data)