import discord 
from discord.ext import commands
import json
import sqlite3
import signal
import sys

from core.classes import Cog_extension

con = sqlite3.connect('test.db')

with open('setting.json', mode='r', encoding='utf-8') as jfile:
    jdata = json.load(jfile)

point_codes = []
used_point_code = []
with open('pointCode.json', mode='r', encoding='utf-8') as pointCode:
    point_codes = json.load(pointCode)

def signal_handler(signum, frame):
    if signum == signal.SIGINT.value:
        con.close()
        print('close！')
        sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

class Event(Cog_extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print(">>SITCON camp Ready!<<")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} join!')
        channel = self.bot.get_channel(int(jdata['CHANNEL_MAINROOM']))
        await channel.send(f'{member} join!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} left!')
        channel = self.bot.get_channel(int(jdata['CHANNEL_MAINROOM']))
        await channel.send(f'{member} join!')

    @commands.Cog.listener()
    async def on_message(self, msg):
        #藉由關鍵字觸發功能檢查學員给出的序號是否合法
        guild = msg.guild

        # 把組別的身分組序號存成 list 方便使用、辨別
        groups = []
        for i in range(1,11):
            #print(int(jdata[f'CHANNEL_ROLE_{i}']))
            groups.append(guild.get_role(int(jdata[f'CHANNEL_ROLE_{i}'])))
            #print(i, groups[i-1])

        if msg.content == '測試' and msg.author != self.bot.user and msg.channel == self.bot.get_channel(int(jdata['CHANNEL_MAINROOM'])):
            
            # sqlite3 測試
            cur = con.cursor()
            cur.execute('''CREATE TABLE point_codes
               (name text, code real)''')
            cur.execute("INSERT INTO point_codes VALUES ('10',Akefb35jkh)")
            con.commit()

            flag = False
            if guild.get_role(int(jdata['CHANNEL_ROLE_1'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第一組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_2'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第二組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_3'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第三組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_4'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第四組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_5'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第五組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_6'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第六組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_7'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第七組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_8'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第八組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_9'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第九組的身分組')
            if guild.get_role(int(jdata['CHANNEL_ROLE_10'])) in msg.author.roles:
                flag = True
                await msg.channel.send('有第十組的身分組')
            if flag == False:
                await msg.channel.send('沒有組別喔QwQ')

        # point_codes 是 list，其中第 0 項是十分的兌換序號，第 1 項是二十分的兌換序號，以此類推。        
        elif msg.content in point_codes[0] and msg.author != self.bot.user and msg.channel == self.bot.get_channel(int(jdata['CHANNEL_MAINROOM'])):
            point_codes[0].remove(msg.content)
            used_point_code.append(msg.content)
            with open('pointCode.json', mode='w', encoding='utf-8') as f:
                json.dump(point_codes, f)
            #for i in groups:
                #if i in msg.author.roles:
                    # TODO 實作讀取、寫入 grades.json 的功能 

            await msg.channel.send('葛萊芬多加十分!')
        elif msg.content in point_codes[1] and msg.author != self.bot.user and msg.channel == self.bot.get_channel(int(jdata['CHANNEL_MAINROOM'])):
            point_codes[1].remove(msg.content)
            used_point_code.append(msg.content)
            with open('pointCode.json', mode='w', encoding='utf-8') as f:
                json.dump(point_codes, f)
            await msg.channel.send('葛萊芬多加二十分!')
        elif msg.content in point_codes[2] and msg.author != self.bot.user and msg.channel == self.bot.get_channel(int(jdata['CHANNEL_MAINROOM'])):
            point_codes[2].remove(msg.content)
            used_point_code.append(msg.content)
            with open('pointCode.json', mode='w', encoding='utf-8') as f:
                json.dump(point_codes, f)
            await msg.channel.send('葛萊芬多加三十分!')
        elif msg.content in used_point_code and msg.author != self.bot.user and msg.channel == self.bot.get_channel(int(jdata['CHANNEL_MAINROOM'])):
            await msg.channel.send('這序號已經使用過囉!')
        elif msg.author != self.bot.user and msg.channel == self.bot.get_channel(int(jdata['CHANNEL_MAINROOM'])):
            await msg.channel.send('輸入的序號有錯喔QQ')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #檢查指令是否有自己的 error handler，如果有就略過
        if hasattr(ctx.command, 'on_error'):
            return
        
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('還需要補上參數喔QwQ')
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send('沒有這個指令耶QwQ')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        # 藉由反應分身分組，需要再根據伺服器 emoji 與身分組 id 到 setting.json 去設定
        guild = self.bot.get_guild(data.guild_id)
        if str(data.emoji) == jdata['CHANNEL_EMOJI_1']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_1'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_2']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_2'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_3']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_3'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_4']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_4'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_5']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_5'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_6']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_6'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_7']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_7'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_8']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_8'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_9']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_9'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_10']:
            await data.member.add_roles(guild.get_role(int(jdata['CHANNEL_ROLE_10'])))

        # 辨別是否是可以使用的分數兌換碼，如果是，學員按完反應就給學員所在小組加分數
        # TODO

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
        # 藉由取消反應來刪除身分組，需要再根據伺服器 emoji 與身分組 id 到 setting.json 去設定
        guild = self.bot.get_guild(data.guild_id)
        user = guild.get_member(data.user_id)
        if str(data.emoji) == jdata['CHANNEL_EMOJI_1']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_1'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_2']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_2'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_3']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_3'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_4']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_4'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_5']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_5'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_6']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_6'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_7']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_7'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_8']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_8'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_9']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_9'])))
        elif str(data.emoji) == jdata['CHANNEL_EMOJI_10']:
            await user.remove_roles(guild.get_role(int(jdata['CHANNEL_ROLE_10'])))
    

def setup(bot):
    bot.add_cog(Event(bot))