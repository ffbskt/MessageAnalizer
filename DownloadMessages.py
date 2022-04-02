from telethon import TelegramClient, tl
import pickle
import time
import password  # file where saved api id and api hash only from https://core.telegram.org/api/obtaining_api_id
# Remember to use your own values from my.telegram.org!

async def get_all_dialog_id(client):
    name_id = []
    async for dialog in client.iter_dialogs():
        name_id.append([dialog.name, dialog.id])
    return  name_id

async def get_me(client):
    # Getting information about yourself
    # Just test client
    me = await client.get_me()
    print(me.stringify())


# example 'KyrgyzChat.pkl'
# Maybe we could use all_messages.append(message.to_dict()) and save as json format https://github.com/amiryousefi/telegram-analysis/blob/d682a38d3a264cfd11dfaeccebef3f58c1450401/ChannelMessages.py
async def save_object(obj, output_file):
    with open(output_file, 'wb') as outp:  # wb Overwrites any existing file. a+ append
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


async def main(dialog_id, output_file, n=None): # n None mean all, numder mean last n
    start = time.time()
    messages = []
    timer = []
    i = 0
    async for message in client.iter_messages(dialog_id, limit=n):
        rpl, fwd = None, (None, None)
        if message.forward:
            if message.forward.from_id and isinstance(message.forward.from_id, tl.types.PeerChannel):
                fwd = (message.forward.from_id.channel_id, message.forward.date)
            elif message.forward.from_id:
                fwd = (message.forward.from_id.user_id, message.forward.date, message.forward.imported)
        if message.is_reply:
            rpl = await message.get_reply_message()
            if rpl:
                rpl = rpl.id
        messages.append([message.id, message.sender_id, message.text, message.date, rpl, *fwd])#, message.forward])
        i += 1
        if i % 500 == 0:
            timer.append([i, time.time() - start])
            print(timer[-1])
    print(messages, output_file)
    await save_object(messages, output_file)
    await save_object(timer, 'timer.pkl')  # not nescecary



if __name__ == "__main__":
    api_id = password.api_id  # getpass()
    api_hash = password.api_hash  # getpass()
    client = TelegramClient('anon', api_id, api_hash)
    output_file = "Dan.pkl"
    # dialog id Krgztn -1001675883387 Dan 5276022195


    with client:
        client.loop.run_until_complete(main(dialog_id=5276022195, output_file=output_file, n=3))
        # print(client.loop.run_until_complete(get_all_dialog_id(client)))