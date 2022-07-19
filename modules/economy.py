
import discord, asyncio

from utils.core import Configuration, Database, Views, Cooldowns, Tools
from discord import SlashCommandGroup
from discord.commands import slash_command
from discord.ext import commands


class Economy_Module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Economy Module Loading...")
    

    @slash_command(
        name = "profile",
        description = "View your Maven-Bot profile (stats)."
    )
    async def profile(self, ctx):
        user = ctx.author
        await Database.Create_User(user.id)

        embed, profile_view = await Views.Setup_Profile(self.bot, user, ctx)

        message = await ctx.respond(
            embed = embed,
            view = profile_view
        )


    jobs = ["Mine", "Fish", "Hunt"]
    @slash_command(
        name = "job",
        description = "Select a job to earn unique rewards, currency, and skill!"
    )
    async def job(
        self,
        ctx,
        job: discord.Option(str, description = "Pick which job you'd like to do.", choices = jobs)
    ):
        user_id = ctx.author.id
        await Database.Create_User(user_id)

        if job == "Mine":
            cooldowns = await Cooldowns.get_cooldowns("work")
            if user_id in cooldowns: # User is on cooldown
                await ctx.respond("You are on cooldown!")
            else: # User is not on cooldown
                embed, work_view = await Views.Setup_Mining(self.bot, ctx.author)
                message = await ctx.respond(
                    embed = embed,
                    view = work_view
                )
                
                await Tools.Give_LootChest(self.bot, ctx)
                await Cooldowns.add_cooldown("work", user_id)

        if job == "Fish":
            cooldowns = await Cooldowns.get_cooldowns("fish")

            if user_id in cooldowns: # User is on cooldown
                await ctx.respond("You are on cooldown!")

            
            else: # User is not on cooldown
                embed = await Views.Setup_Fish(self.bot, ctx.author)
                
                message = await ctx.respond(embed = embed)

                await Tools.Give_LootChest(self.bot, ctx)
                await Cooldowns.add_cooldown("fish", user_id)

        if job == "Hunt":
            cooldowns = await Cooldowns.get_cooldowns("hunt")

            if user_id in cooldowns: # User is on cooldown
                await ctx.respond("You are on cooldown!")

            else: # User is not on cooldown
                await Views.Setup_Hunting(self.bot, ctx, user_id)
                await Tools.Give_LootChest(self.bot, ctx)
                await Cooldowns.add_cooldown("hunt", user_id)
        

    @slash_command(
        name = "deposit",
        description = "Convert your silver into gold and deposit them into your bank."
    )
    async def deposit(self, ctx, amount: discord.Option(int, description = "How much would you like to deposit?", default = 1000)):
        user_id = ctx.author.id
        await Database.Create_User(user_id)
        title, t_color = await Database.Fetch_Title(self.bot, user_id)
        wallet, bank = await Database.Fetch_Balance(self.bot, user_id)

        if wallet >= 1000: # They do have enough to convert and deposit
            if wallet >= amount: # They have the requested amount as well
                conversion_amount = amount * 0.001
                deposit_embed = discord.Embed(title = f"Converted {self.bot.get_emoji(985978616741511208)} {amount} silver into {conversion_amount} {self.bot.get_emoji(985978615911051314)} and deposited it to their bank.", description=f"{title}", color = t_color)
                
                await Database.Update_Balance(user_id, "wallet", -amount)
                await Database.Update_Balance(user_id, "bank", +conversion_amount)

                await ctx.respond(embed=deposit_embed)

        else: # They don't have enough for that deposit
            await ctx.respond(f"{ctx.author.mention}, you do not have enough silver to deposit that much! You need {self.bot.get_emoji(985978616741511208)} **1,000** per {self.bot.get_emoji(985978615911051314)} **1**")


    @slash_command(
        name = "withdraw",
        description = "Withdraw your silver from your bank."
    )
    async def withdraw(self, ctx, amount: discord.Option(int, description = "How much would you like to withdraw?", default = 1000)):
        user_id = ctx.author.id
        await Database.Create_User(user_id)
        title, t_color = await Database.Fetch_Title(self.bot, user_id)
        wallet, bank = await Database.Fetch_Balance(self.bot, user_id)

        if bank >= 1: # They do have enough to convert and withdraw
            if bank >= amount: # They have the requested amount as well
                conversion_amount = amount * 1000
                withdraw_embed = discord.Embed(title = f"Converted {amount} {self.bot.get_emoji(985978615911051314)} gold into {self.bot.get_emoji(985978616741511208)} {conversion_amount} silver and withdrew it.", description=f"{title}", color = t_color)
                
                await Database.Update_Balance(user_id, "wallet", +conversion_amount)
                await Database.Update_Balance(user_id, "bank", -amount)

                await ctx.respond(embed=withdraw_embed)

        else: # They don't have enough for that withdraw
            await ctx.respond(f"{ctx.author.mention}, you do not have enough gold to withdraw!")


    shop_choices = ["normal", "void"]
    @slash_command(
        name = "shop",
        description = "View the shop to purchase and sell items."
    )
    async def shop(
        self,
        ctx,
        shop_selection: discord.Option(str, description = "Which shop would you like to view?", choices = shop_choices, default = "normal", required = False)
    ):
        user_id = ctx.author.id
        await Database.Create_User(user_id)
        # If the shop is normal: Get all normal items for the checked server
        embed, view = await Views.Setup_Shop(self.bot, ctx.author, shop_selection, ctx.author.guild.id)
        
        message = await ctx.respond(
            embed = embed,
            view = view
        )


    @slash_command(
        name = "inventory",
        description = "View the items in your inventory."
    )
    async def inventory(self, ctx):
        user_id = ctx.author.id
        await Database.Create_User(user_id)
        embed, view = await Views.Setup_Inventory(self.bot, ctx.author)

        message = await ctx.respond(
            embed = embed,
            view = view
        )


    @slash_command(
        name = "buy",
        description = "Purchase items from the /shop."
    )
    async def buy(
        self,
        ctx,
        item: discord.Option(str, description = "Which item would you like to purchase?", Required = True),
        amount: discord.Option(str, description = "How many do you want to buy?", Required = True)
    ):
        await Database.Create_User(ctx.author.id)
        title, t_color = await Database.Fetch_Title(self.bot, ctx.author.id)
        items = await Database.Fetch_Itemlist()
        key = await Database.Fetch_Item_Key(item) # Return something incase the item was typed wrong
        config = await Configuration.Fetch_Configuration_File()

        if key == "error":
            await ctx.respond(f"{ctx.author.mention}, you typed something wrong...try again.")
            return

        item_name = items[key]["name"]
        item_emoji = items[key]["emoji"]
        item_rarity = items[key]["rarity"]

        cost = int(amount) * items[key]["store_value"]

        embed = discord.Embed(title = f"{ctx.author.name}'s Purchase Request", description=f"{title}", color = t_color)
        embed.add_field(name = f"{self.bot.get_emoji(item_emoji)} {item_name} {self.bot.get_emoji(item_rarity)} - **({amount})**", value = f"For:\n{self.bot.get_emoji(985978616741511208)} {cost}") # How much the purchase will be
        embed.set_thumbnail(url = ctx.author.avatar.url)

        if items[key]["can_buy"] == "false": # They cannot purchase that item
            await ctx.respond(f"{ctx.author.mention}, that item is currently not buyable.")
        
        else: # Continue code
            if items[key]["shop"] == "normal":
                store_value = items[key]["store_value"]
                wallet, bank = await Database.Fetch_Balance(self.bot, ctx.author.id)

                if wallet >= int(amount) * int(store_value): # They can afford to purchase the item
                    
                    view = await Views.Setup_Purchase(self.bot, ctx.author, key, amount, cost, title, t_color)
                    message = await ctx.respond(
                        embed = embed,
                        view = view
                    )
                
                else: # They can't afford to purchase the item
                    await ctx.respond(f"{ctx.author.mention}, you can't afford that many!")
        
            if items[key]["shop"] == "void":
                void_embed = discord.Embed(title = F"{ctx.author.name} claimed a Void Item!")

                store_value = items[key]["store_value"] # Void stone value
                user_void_stones = await Database.Fetch_Item_Amount(ctx.author.id, "item14")

                if user_void_stones >= int(amount) * int(store_value): # They can afford to purchase the item
                    message = await ctx.respond(embed = void_embed)

                    if key == "item15": # Void Knife
                        await Database.Update_User_Inventory(ctx.author.id, "item14", "subtract", 50)
                        await Database.Update_User_Inventory(ctx.author.id, "item15", "add", 1)
                
                else: # They can't afford to purchase the item
                    await ctx.respond(f"{ctx.author.mention}, you can't afford that many!")


    @slash_command(
        name = "sell",
        description = "Sell items to the shop (you will be taxed)."
    )
    async def sell(
        self,
        ctx,
        item: discord.Option(str, description = "Type the name of the item you want to sell."),
        amount: discord.Option(int, description = "How many do you want to sell?")
    ):
        await Database.Create_User(ctx.author.id)
        title, t_color = await Database.Fetch_Title(self.bot, ctx.author.id)
        items = await Database.Fetch_Itemlist()
        key = await Database.Fetch_Item_Key(item) # Return something incase the item was typed wrong
        config = await Configuration.Fetch_Configuration_File()
        
        if key == "error":
            await ctx.respond(f"{ctx.author.mention}, you typed something wrong...try again.")
            return

        tax = config["sell_tax"]
        store_value = items[key]["store_value"]
        item_name = items[key]["name"]
        item_emoji = items[key]["emoji"]
        item_rarity = items[key]["rarity"]
        
        value = store_value * amount
        
        amount_to_tax = value * tax
        difference = int(amount_to_tax) - int(value)
        final_amount = int(value) - int(difference)


        user_item_amount = await Database.Fetch_Item_Amount(ctx.author.id, key)

        embed = discord.Embed(title = f"{ctx.author.name}'s Sale Request", description=f"{title}", color = t_color)
        embed.add_field(name = f"{self.bot.get_emoji(item_emoji)} {item_name} {self.bot.get_emoji(item_rarity)} - **({amount})**", value = f"Selling For:\n{final_amount}\nTax: {self.bot.get_emoji(985978616741511208)} -**({difference})**")

        if items[key]["can_sell"] == "true":
            if user_item_amount > 0: # They do have the item and can sell some
                if user_item_amount >= amount:
                    # Begin the sell view
                    view = await Views.Setup_Sell(self.bot, ctx.author, key, amount, final_amount, tax, title, t_color)
                    await ctx.respond(embed = embed, view = view)

                else: # They do not have enough of the item to sell
                    await ctx.respond(f"{ctx.author.mention}, you don't have that many to sell!")
            else: # They don't even own the item
                await ctx.respond(f"{ctx.author.mention}, you don't have any of those to sell!")
        else:
            await ctx.respond(f"{ctx.author.mention}, that item is not sellable!")


    @slash_command(
        name = "use",
        description = "Use items on yourself or other members."
    )
    async def use(
        self, 
        ctx,
        target: discord.Option(discord.Member, description = "Choose which member to target, or choose yourself.", Required = True)
    ): 
        await Database.Create_User(ctx.author.id)
        await Database.Create_User(target.id)
        await Views.Setup_Use(self.bot, ctx, target)


    admin_commands = ["addmoney", "removemoney", "additem", "removeitem"]
    @slash_command(
        name = "administrator",
        description = "Administrator commands."
    )
    async def administrator(
        self,
        ctx,
        command: discord.Option(str, description = "Which command would you like to use?", choices = admin_commands),
        member: discord.Option(discord.Member, description = "Choose which member to target."),
        value: discord.Option(str, description = "Type in keywords or a value to execute the command with.", Required = True),
        item: discord.Option(str, description = "The name of the item you are dealing with. (If nothing, type random stuff here)")
    ):
        config = await Configuration.Fetch_Configuration_File()
        admin_check = config["admins"]
        
        if ctx.author.id in admin_check:
            if command == "addmoney":
                await Database.Update_Balance(member.id, "wallet", int(value))
                await ctx.respond(f"{member.mention} received {self.bot.get_emoji(985978616741511208)} **({value})** Silver.")
            if command == "removemoney":
                await Database.Update_Balance(member.id, "wallet", -int(value))
                await ctx.respond(f"{member.mention} lost {self.bot.get_emoji(985978616741511208)} **({value})** Silver.")
            if command == "additem":
                key = await Database.Fetch_Item_Key(item)
                items = await Database.Fetch_Itemlist()
                await Database.Update_User_Inventory(member.id, key, "add", int(value))

                item_name = items[key]["name"]
                item_emoji = items[key]["emoji"]

                await ctx.respond(f"{member.mention} gained **({value})** {self.bot.get_emoji(item_emoji)} {item_name}.")
            if command == "removeitem":
                key = await Database.Fetch_Item_Key(item)
                items = await Database.Fetch_Itemlist()
                await Database.Update_User_Inventory(member.id, key, "subtract", int(value))

                item_name = items[key]["name"]
                item_emoji = items[key]["emoji"]

                await ctx.respond(f"{member.mention} lost **({value})** {self.bot.get_emoji(item_emoji)} {item_name}.")


        else:
            await ctx.respond(f"{ctx.author.mention}, you do not have permission to use that command.")


    @slash_command(
        name = "trade",
        description = "Trade items to other members."
    )
    async def trade(
        self, ctx,
        target: discord.Option(discord.Member, description = "Choose which member you want to trade with.", Required = True),
        your_item: discord.Option(str, description = "Type in the item you want to trade.", Required = True),
        your_amount: discord.Option(str, description = "How many do you want to trade?", Required = True),
        target_item: discord.Option(str, description = "Type in the item you are trading for.", Required = True),
        target_amount: discord.Option(str, description = "Type in how many of their item you want.", Required = True)
    ):
        await Database.Create_User(ctx.author.id)
        await Database.Create_User(target.id)
        await Views.Setup_Trade(self.bot, ctx, ctx.author, target, your_item, your_amount, target_item, target_amount)


    @slash_command(
        name = "adventure",
        description = "Adventure into unknown territory, beware of dangers."
    )
    async def adventure(
        self, ctx
    ):
        await Views.Setup_Adventure(self.bot, ctx)


    @slash_command(
        name = "craft",
        description = "Craft new and exciting items to help you conquer discord servers."
    )
    async def craft(
        self, ctx
    ):
        await Database.Create_User(ctx.author.id)
        await Views.Setup_Craft(self.bot, ctx)



    ### Listeners & Events ###

    # Update messages for user's level
    @commands.Cog.listener()
    async def on_message(self, message):
        user_id = message.author.id
        await Database.Create_User(user_id)
        await Database.Update_Message_Count(user_id, message, self.bot)

        if message.guild.id == 497128669412589574:
            await Tools.Give_Voidstone(self.bot, message)





def setup(bot):
    bot.add_cog(Economy_Module(bot))