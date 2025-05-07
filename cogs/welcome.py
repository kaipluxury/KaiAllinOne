import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import os
import io

WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))
AUTOROLE_ID = int(os.getenv("AUTOROLE_ID", 0))  # Optional

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_welcome_image(self, member: discord.Member):
        base = Image.new("RGB", (600, 250), (0, 0, 0))
        draw = ImageDraw.Draw(base)

        # Load font (must exist in assets/fonts/)
        font_path = "assets/fonts/GothamBold.ttf"
        if not os.path.exists(font_path):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

        font_large = ImageFont.truetype(font_path, 36)
        font_small = ImageFont.truetype(font_path, 24)

        # Draw text
        draw.text((30, 30), "Welcome to Armani Family", font=font_large, fill="white")
        draw.text((30, 90), f"{member.name}", font=font_small, fill="white")
        draw.text((30, 130), f"#{member.guild.member_count}", font=font_small, fill="gray")

        # Load avatar
        avatar_asset = member.display_avatar.with_size(128)
        avatar_bytes = io.BytesIO()
        async def get_avatar():
            await avatar_asset.save(avatar_bytes)
        import asyncio
        asyncio.run(get_avatar())

        avatar = Image.open(io.BytesIO(avatar_bytes.getvalue())).convert("RGB").resize((100, 100))
        base.paste(avatar, (450, 75))

        buffer = io.BytesIO()
        base.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    async def send_welcome_embed(self, member):
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if not channel:
            return

        image_buffer = self.generate_welcome_image(member)
        file = discord.File(fp=image_buffer, filename="welcome.png")

        embed = discord.Embed(
            title="🎉 Welcome!",
            description=f"Hey {member.mention}, welcome to **Armani Family**.\nYou're member #{member.guild.member_count}!",
            color=discord.Color.light_gray()
        )
        embed.set_image(url="attachment://welcome.png")
        embed.set_footer(text="Armani Family | ⚡️Powered By Kai")

        await channel.send(embed=embed, file=file)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.send_welcome_embed(member)
        if AUTOROLE_ID:
            role = member.guild.get_role(AUTOROLE_ID)
            if role:
                await member.add_roles(role, reason="Auto role on join")

    @app_commands.command(name="welcome_test", description="Test the welcome image.")
    async def welcome_test(self, interaction: discord.Interaction):
        await self.send_welcome_embed(interaction.user)
        await interaction.response.send_message("✅ Test welcome sent!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
