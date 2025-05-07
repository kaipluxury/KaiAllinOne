import discord
from discord.ext import commands
from discord import app_commands
import datetime
import os

MODLOG_CHANNEL_ID = int(os.getenv("MODLOG_CHANNEL_ID"))

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # BAN
    @app_commands.command(name="ban", description="Ban a user with reason.")
    @app_commands.describe(member="User to ban", reason="Reason for banning")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("❌ You don't have permission to ban.", ephemeral=True)

        await member.ban(reason=reason)
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"**User:** {member.mention}\n**Moderator:** {interaction.user.mention}\n**Reason:** {reason}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Armani Family | ⚡️Powered By Kai")
        await interaction.response.send_message(embed=embed)

        log_channel = interaction.guild.get_channel(MODLOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

    # KICK
    @app_commands.command(name="kick", description="Kick a user with reason.")
    @app_commands.describe(member="User to kick", reason="Reason for kicking")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message("❌ You don't have permission to kick.", ephemeral=True)

        await member.kick(reason=reason)
        embed = discord.Embed(
            title="👢 Member Kicked",
            description=f"**User:** {member.mention}\n**Moderator:** {interaction.user.mention}\n**Reason:** {reason}",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Armani Family | ⚡️Powered By Kai")
        await interaction.response.send_message(embed=embed)

        log_channel = interaction.guild.get_channel(MODLOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

    # MUTE
    @app_commands.command(name="mute", description="Timeout a user for X minutes.")
    @app_commands.describe(member="User to timeout", minutes="Duration in minutes", reason="Reason for timeout")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ You don't have permission to mute.", ephemeral=True)

        until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)

        embed = discord.Embed(
            title="⏳ Member Timed Out",
            description=f"**User:** {member.mention}\n**Moderator:** {interaction.user.mention}\n**Duration:** {minutes} min\n**Reason:** {reason}",
            color=discord.Color.dark_gold(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Armani Family | ⚡️Powered By Kai")
        await interaction.response.send_message(embed=embed)

        log_channel = interaction.guild.get_channel(MODLOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

    # UNMUTE
    @app_commands.command(name="unmute", description="Remove a timeout from a user.")
    @app_commands.describe(member="User to untimeout")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message("❌ You don't have permission to unmute.", ephemeral=True)

        await member.timeout(None)

        embed = discord.Embed(
            title="✅ Timeout Removed",
            description=f"**User:** {member.mention}\n**Moderator:** {interaction.user.mention}",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Armani Family | ⚡️Powered By Kai")
        await interaction.response.send_message(embed=embed)

        log_channel = interaction.guild.get_channel(MODLOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

    # WARN
    @app_commands.command(name="warn", description="Warn a user for something.")
    @app_commands.describe(member="User to warn", reason="Reason for warning")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("❌ You don't have permission to warn.", ephemeral=True)

        embed = discord.Embed(
            title="⚠️ User Warned",
            description=f"**User:** {member.mention}\n**Moderator:** {interaction.user.mention}\n**Reason:** {reason}",
            color=discord.Color.yellow(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Armani Family | ⚡️Powered By Kai")
        await interaction.response.send_message(embed=embed)

        log_channel = interaction.guild.get_channel(MODLOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

    # CLEAR
    @app_commands.command(name="clear", description="Delete messages from a channel.")
    @app_commands.describe(amount="Number of messages to delete")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("❌ You don't have permission to clear messages.", ephemeral=True)

        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(
            title="🧹 Messages Deleted",
            description=f"{amount} messages cleared by {interaction.user.mention}.",
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="Armani Family | ⚡️Powered By Kai")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
