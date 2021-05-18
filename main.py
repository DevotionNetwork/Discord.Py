import discord
import asyncio
from discord.ext import commands
from settings import *

intents = discord.Intents(members=True, presences=True, guilds=True, messages=True, reactions=True)

bot = commands.Bot(command_prefix="*", intents=intents)


@bot.event
async def on_ready():  # Bot'un çalıştığını anlamamız için konsola bir yazı basar ve bot'un durumunu ayarlar.
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=ReadyStatus))
    print('Bot Aktif!')


@bot.event
async def on_member_join(member):  # Sunucuya yeni birisi geldiğinde Hoş geldin mesajı atar ve Basic Role verir.
    role = discord.utils.get(member.guild.roles, name=Unregister)
    channel1 = discord.utils.get(member.guild.text_channels, name=welcome)
    channel2 = discord.utils.get(member.guild.text_channels, name=welcomelog)
    
    await member.add_roles(role)
    await channel1.send(f'Aramıza hoş geldin <@{member.id}>. İyi eğlenceler :tada:', delete_after=5)
    await channel2.send(f'{member} kullanıcısı sunucuya katıldı.')


@bot.event
async def on_member_remove(member):  # Sunucudan birisi çıkış yaptığında log'a mesaj atar.
    channel = discord.utils.get(member.guild.text_channels, name="gelen-giden")

    await channel.send(f'<@{member.id}> kullanıcısı aramızdan ayrıldı. :unamused:')

@bot.command()
async def avatar(ctx, *, user: discord.Member = None):  # Avatar yani profil fotoğrafı büyütme komutudur.
    author = ctx.author

    if not user:
        user = author

    if user.is_avatar_animated():
        url = user.avatar_url_as(format="gif")
    if not user.is_avatar_animated():
        url = user.avatar_url_as(static_format="png")

    await ctx.send("{}".format(url))

@bot.command()
async def clear(ctx, amount=7):  # Toplu mesaj silme komutudur.

    await ctx.channel.purge(limit=amount)
    await ctx.channel.send(f'``{amount} mesaj başarıyla silinmiştir.``', delete_after=5)
    

@commands.has_permissions(kick_members=True)  # Sunucudan üye atma komutudur.
@bot.command()
async def kick(ctx, user: discord.Member, *, reason="**Belirtilmedi**"):
    channel = discord.utils.get(user.guild.text_channels, name=cezalog)
    kick = discord.Embed(title=f"{user.name} kullanıcısı sunucudan başarıyla **atıldı**!", description=f"**Sebep**: **{ reason }**\n **Eylemi Yapan**: **{ctx.author.mention}**").set_author(name="Kicked")
    await user.kick(reason=reason)
    await ctx.message.delete()
    await channel.send(embed=kick)
    await ctx.channel.send(
        f'{user.mention} kullanıcısı sunucudan başarıyla **atıldı**. Eylemi yapan **yetkili** :  {ctx.author.mention}',
        delete_after=7)


@commands.has_permissions(ban_members=True)  # Sunucudan üye yasaklama komutudur.
@bot.command()
async def ban(ctx, user: discord.Member, *, reason="**Belirtilmedi**"):
    channel = discord.utils.get(user.guild.text_channels, name=cezalog)
    ban = discord.Embed(title=f"{user.name} kullanıcısı sunucudan başarıyla **yasaklandı**!",
                        description=f"**Sebep**: **{reason}**\n **Eylemi Yapan**: **{ctx.author.mention}**").set_author(
        name="Banned")
    await user.ban(reason=reason)
    await ctx.message.delete()
    await channel.send(embed=ban)
    await ctx.channel.send(
        f'{user.mention} kullanıcısı sunucudan başarıyla **yasaklandı**. Eylemi yapan **yetkili** :  {ctx.author.mention}',
        delete_after=7)


@commands.has_permissions(ban_members=True)  # Sunucudan yasaklı üyelerin yasağını kaldırmak için kullanlıan komuttur.
@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for bans in banned_users:

        user = bans.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} kullanıcısının yasağı kaldırıldı.', delete_after=5)
            return


@commands.has_permissions(manage_roles=True) #Etiketlediğiniz kişiye rol verir.
@bot.command()
async def rolver(ctx, member : discord.Member, role : discord.Role):
    
    if role is None:
        await ctx.send(f'Lütfen bir rol etiketleyiniz.')

    else:
        await member.add_roles(role)
        
@bot.command()
async def davet(ctx):
    await ctx.send(f'discord.gg/devotion')

bot.run(token)


