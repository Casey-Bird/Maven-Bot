
from operator import truediv
import discord, json, asyncio, random
import sqlite3 as sql

work_cooldowns = [] # Cooldown container for users who crafted recently
fish_cooldowns = [] # Cooldown container for users who crafted recently
hunt_cooldowns = [] # Cooldowns for hunting
craft_cooldowns = [] # Cooldown container for users who crafted recently
attack_cooldowns = [] # Cooldowns for users who just attacked


class Configuration():
    bot_version = "0.0"

    async def Fetch_Configuration_File():
        file = open("./data/config.json")
        data = json.load(file)

        return data



class Database():

    # User creation.
    async def Create_User(user_id):

        def Create_User_Info(user_id):
            user_db = sql.connect("./data/user_db.db")
            cursor = user_db.cursor()
            query = f"INSERT INTO users (id) VALUES ({user_id})"
            cursor.execute(query)
            user_db.commit()
            user_db.close()

            levels_db = sql.connect("./data/levels_db.db")
            cursor = levels_db.cursor()
            query = f"INSERT INTO users (id) VALUES ({user_id})"
            cursor.execute(query)
            levels_db.commit()
            levels_db.close()

            inventory_db = sql.connect("./data/inventory_db.db")
            cursor = inventory_db.cursor()
            query = f"INSERT INTO users (id) VALUES ({user_id})"
            cursor.execute(query)
            inventory_db.commit()
            inventory_db.close()

            stats_db = sql.connect("./data/stats_db.db")
            cursor = stats_db.cursor()
            query = f"INSERT INTO users (id) VALUES ({user_id})"
            cursor.execute(query)
            stats_db.commit()
            stats_db.close()

        
        def Check_Existing(user_id):
            user_db = sql.connect("./data/user_db.db")
            cursor = user_db.cursor()

            query = f"SELECT * FROM users WHERE id = {user_id}"

            cursor.execute(query)
            result = cursor.fetchall()

            if not result: # Result didn't fetch anything
                Create_User_Info(user_id)
            else:
                pass
            
            user_db.close()

        Check_Existing(user_id)

    # Fetch all the shopable items and return them
    async def Fetch_Shopables(guild_id):
        # Get the json file

        file = open("./data/items.json")
        data = json.load(file)

        config = await Configuration.Fetch_Configuration_File()
        
        normal_shop_keys = []
        
        if guild_id == 980656704763068466: # Dula Peep
            normal_shop_keys.append("item1")

        i = 1
        while i <= config["max_items"]:
            try:
                if data["item" + str(i)]["shop"] == "normal":
                    if data["item" + str(i)]["can_buy"] == "false" and data["item" + str(i)]["can_sell"] == "false":
                        pass
                    else:
                        normal_shop_keys.append(data["item" + str(i)]["key"])
            except:
                pass
            i += 1
        
        return normal_shop_keys

    # Fetch the entire items.json file
    async def Fetch_Itemlist():
        file = open("./data/items.json")
        data = json.load(file)

        return data

    # Fetch the user's level
    async def Fetch_Level(member, bot, ctx):
            user_id = member.id
            try:
                levels_db = sql.connect("./data/levels_db.db")
                cursor = levels_db.cursor()

                get_query = f"SELECT messages FROM users WHERE id = {user_id}"
                cursor.execute(get_query)
                result = list(cursor.fetchall()[0])
                message_count = result[0]

                levels_db.close()

                level = 1
                # 25 is 20k messages

                if message_count >= 0:
                    level = 1
                
                if message_count >= 20:
                    level = 2
                
                if message_count >= 100:
                    level = 3
                
                if message_count >= 500:
                    level = 4
                
                if message_count >= 1000:
                    level = 5
                
                if message_count >= 1500:
                    level = 6
                
                if message_count >= 2500:
                    level = 7
                
                if message_count >= 4000:
                    level = 8
                
                if message_count >= 5500:
                    level = 9
                
                if message_count >= 7000:
                    level = 10
                
                
                return level, message_count


            
            except:
                pass

    # Fetch and return title and title color
    async def Fetch_Title(bot, user_id):

            user_db = sql.connect("./data/user_db.db")
            cursor = user_db.cursor()

            get_query = f"SELECT title FROM users WHERE id = {user_id}"
            cursor.execute(get_query)
            result = list(cursor.fetchall()[0])
            title_name = result[0]

            user_db.close()
            title = " "
            t_color = discord.Color.dark_gray()

            if title_name == "default":
                title = " "
                t_color = discord.Color.dark_gray()

            if title_name == "demon":
                title = f"{bot.get_emoji(887992464395362304)} Demon {bot.get_emoji(887992464659611658)}"
                t_color = discord.Color.from_rgb(172, 63, 235)

            if title_name == "instigator":
                title = f"{bot.get_emoji(986078219730059325)} Instigator {bot.get_emoji(986078219730059325)}"
                t_color = discord.Color.from_rgb(191, 145, 204)

            if title_name == "golden":
                title = f"{bot.get_emoji(985978615911051314)} Golden {bot.get_emoji(985978615911051314)}"
                t_color = discord.Color.from_rgb(196,149,37)

            if title_name == "kami":
                title = f"{bot.get_emoji(993848035253694484)} Kami of the Forest {bot.get_emoji(993848035253694484)}"
                t_color = discord.Color.from_rgb(66,237,95)


            return title, t_color

    # Get wallet and bank info
    async def Fetch_Balance(bot, user_id):

        user_db = sql.connect("./data/user_db.db")
        cursor = user_db.cursor()

        get_query = f"SELECT wallet,bank FROM users WHERE id = {user_id}"
        cursor.execute(get_query)
        result = list(cursor.fetchall()[0])
        wallet = result[0]
        bank = result[1]

        user_db.close()

        return wallet,bank

    # Get all of a user's items
    async def Fetch_User_Items(user_id):
        config = await Configuration.Fetch_Configuration_File()

        inventory_db = sql.connect("./data/inventory_db.db")
        cursor = inventory_db.cursor()
        # Depending on max items will edit the query and check for those items...if more than 0 then add to list

        user_items = []

        i = 0
        while i < config["max_items"]:
            
            try:
                get_query = f"SELECT item{str(i)} FROM users WHERE id = {user_id}"
                cursor.execute(get_query)
                result = list(cursor.fetchall()[0])
                item_amount = result[0]
                if item_amount > 0:
                    user_items.append(f"item{str(i)}")

            except:
                pass

            i += 1
        
        inventory_db.close()

        return user_items

    # Get an amount from a user
    async def Fetch_Item_Amount(user_id, key):
        config = await Configuration.Fetch_Configuration_File()

        inventory_db = sql.connect("./data/inventory_db.db")
        cursor = inventory_db.cursor()


        get_query = f"SELECT {key} FROM users WHERE id = {user_id}"
        cursor.execute(get_query)
        result = list(cursor.fetchall()[0])
        item_amount = result[0]
        
        inventory_db.close()

        return item_amount

    # Get a user's title items
    async def Fetch_Title_Items(user_id):
        # Super golden bar, Demon & Instigator based on user id
        titles = []
        user_items = await Database.Fetch_User_Items(user_id)
        
        if user_id == 155751780674699264: # Maven's ID
            titles.append("demon")
        if user_id == 743597640012398643: # Nick's ID
            titles.append("instigator")
        
        if "item11" in user_items:
            titles.append("golden")
        
        if "item12" in user_items:
            titles.append("kami")

        return titles
        
    # Fetching Statistics of a user
    async def Fetch_Stats(user_id):

        stats_db = sql.connect("./data/stats_db.db")
        cursor = stats_db.cursor()

        get_query = f"SELECT health,stunned,toxin,charmed,cursed,frozen,work_skill,fish_skill,hunt_skill FROM users WHERE id = {user_id}"
        cursor.execute(get_query)
        result = list(cursor.fetchall()[0])
        health = result[0]
        stunned = result[1]
        toxin = result[2]
        charmed = result[3]
        cursed = result[4]
        frozen = result[5]
        work_skill = result[6]
        fish_skill = result[7]
        hunt_skill = result[8]


        stats_db.close()
        
        stats = {
            "health": health,
            "stunned": stunned,
            "toxin": toxin,
            "charmed": charmed,
            "cursed": cursed,
            "frozen": frozen,
            "work_skill": work_skill,
            "fish_skill": fish_skill,
            "hunt_skill": hunt_skill
        }

        return stats

    # Fetching usable items based on config and if they own the item
    async def Fetch_Usables(user_id):
        items = await Database.Fetch_Itemlist()
        config = await Configuration.Fetch_Configuration_File()
        
        self_usable_raw = []
        target_usable_raw = []

        i = 1
        while i < config["max_items"]: # Filling the arrays with item keys of usable items
            try:
                if items[f"item{i}"]["self_usable"] == "true":
                    self_usable_raw.append(f"item{i}")
                if items[f"item{i}"]["target_usable"] == "true":
                    target_usable_raw.append(f"item{i}")

            except:
                pass
            
            i += 1

        self_usable = []
        target_usable = []
        
        i = 0
        while i < config["max_items"]: # Filling new arrays with items the user actually owns
            if len(self_usable_raw) >= 1:
                key = self_usable_raw[0]
                item_amount = await Database.Fetch_Item_Amount(user_id, key)
                if item_amount > 0:
                    self_usable.append(key)
                self_usable_raw.remove(key)
            if len(target_usable_raw) >= 1:
                key = target_usable_raw[0]
                item_amount = await Database.Fetch_Item_Amount(user_id, key)
                if item_amount > 0:
                    target_usable.append(key)
                target_usable_raw.remove(key)

            i += 1

        return self_usable, target_usable

    # Fetch an item key based on user input
    async def Fetch_Item_Key(name):
        worldlock_names = ["world", "world lock", "lock", "wl", "wls"]
        if name in worldlock_names:
            return "item1"
        
        eggplant_name = ["eggplant", "eggplants"]
        if name in eggplant_name:
            return "item2"

        banana_name = ["banana", "bananas", "banans", "banan"]
        if name in banana_name:
            return "item3"
        
        knife_name = ["knife", "knif", "knives", "knifes"]
        if name in knife_name:
            return "item4"

        seabass_name = ["sea bass", "sea", "bass", "sea basses", "seabass"]
        if name in seabass_name:
            return "item5"

        rawmeat_name = ["raw meat", "raw", "meat", "raw meats", "rawmeat"]
        if name in rawmeat_name:
            return "item6"

        lime_name = ["lime", "limes"]
        if name in lime_name:
            return "item7"

        foxfur_name = ["foxfur", "furs", "fox", "fox fur", "fox furs", "foxes"]
        if name in foxfur_name:
            return "item8"

        milk_name = ["milk", "milks"]
        if name in milk_name:
            return "item9"

        basicchest_name = ["basicchest", "basic", "basic chest", "basic chests", "basics"]
        if name in basicchest_name:
            return "item10"

        specialgolden_name = ["special golden bar", "special golden", "special", "specialgoldenbar"]
        if name in specialgolden_name:
            return "item11"

        tome_name = ["tome"]
        if name in tome_name:
            return "item12"

        wisp_name = ["forest wisp"]
        if name in wisp_name:
            return "item13"

        return "error"

    # Update Balance
    async def Update_Balance(user_id, selection, amount):
        # Check selection
        # Edit the amount
        user_db = sql.connect("./data/user_db.db")
        cursor = user_db.cursor()

        get_query = f"SELECT wallet,bank FROM users WHERE id = {user_id}"
        cursor.execute(get_query)
        result = list(cursor.fetchall()[0])
        wallet = result[0]
        bank = result[1]


        if selection == "wallet":
            wallet += amount
            update_query = f"UPDATE users SET wallet = '{wallet}' WHERE id = {user_id}"
            cursor.execute(update_query)
        
        if selection == "bank":
            bank += amount
            update_query = f"UPDATE users SET bank = '{bank}' WHERE id = {user_id}"
            cursor.execute(update_query)

        user_db.commit()
        user_db.close()

    # Update how many messages they have sent & handles level ups
    async def Update_Message_Count(user_id, message, bot):
        levels_db = sql.connect("./data/levels_db.db")
        cursor = levels_db.cursor()

        get_query = f"SELECT messages FROM users WHERE id = {user_id}"
        cursor.execute(get_query)
        result = list(cursor.fetchall()[0])
        message_count = result[0]
        new_count = message_count + 1
        update_query = f"UPDATE users SET messages = '{new_count}' WHERE id = {user_id}"
        cursor.execute(update_query)
        levels_db.commit()
        levels_db.close()
    
        level = 1
        message_guild = message.guild.id
        async def Level_Up(user_id, message, level):
            if message_guild == 980656704763068466:
                inventory_db = sql.connect("./data/inventory_db.db")
                cursor = inventory_db.cursor()
                
                get_query = f"SELECT item1 FROM users WHERE id = {user_id}"
                cursor.execute(get_query)
                result = list(cursor.fetchone())[0]
                item_count = result
                new_count = item_count + 1
                update_query = f"UPDATE users SET item1 = '{new_count}' WHERE id = {user_id}"
                cursor.execute(update_query)
                inventory_db.commit()
                inventory_db.close()
                
                await message.channel.send(f"{message.author.mention}, you leveled up! You are now level **{str(level)}** and obtained **1** {bot.get_emoji(984935495832318033)}")
            else:
                await message.channel.send(f"{message.author.mention}, you leveled up! You are now level **{str(level)}**")


        if new_count == 0:
            level = 1
        
        if new_count == 20:
            level = 2
            await Level_Up(user_id, message, level)
        
        if new_count == 100:
            level = 3
            await Level_Up(user_id, message, level)
        
        if new_count == 500:
            level = 4
            await Level_Up(user_id, message, level)
        
        if new_count == 1000:
            level = 5
            await Level_Up(user_id, message, level)
        
        if new_count == 1500:
            level = 6
            await Level_Up(user_id, message, level)
        
        if new_count == 2500:
            level = 7
            await Level_Up(user_id, message, level)
        
        if new_count == 4000:
            level = 8
            await Level_Up(user_id, message, level)
        
        if new_count == 5500:
            level = 9
            await Level_Up(user_id, message, level)
        
        if new_count == 7000:
            level = 10
            await Level_Up(user_id, message, level)

    # Update user Health
    async def Update_User_Health(ctx, bot, target, type, severity, key, interaction):
        # Type: normal, overheal, damage
        # Severity: 1, 2, 3
        # Key: Which item was used
        use_health, use_description, use_damage = await Tools.Generate_Use_Info(key)

        stats_db = sql.connect("./data/stats_db.db")
        cursor = stats_db.cursor()

        get_query = f"SELECT health FROM users WHERE id = {target.id}"
        cursor.execute(get_query)
        result = list(cursor.fetchall()[0])
        current_health = result[0]

        if type == "heal": # TODO Create embed send for healing
            if current_health + use_health >= 100: # Set health to 100 and leave it be
                h = 100
                update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                cursor.execute(update_query)
            else: # Update health normally
                new_amount = current_health + use_health
                update_query = f"UPDATE users SET health = '{new_amount}' WHERE id = {target.id}"
                cursor.execute(update_query)

            if key == "item12": # Tome of the Forest
                tome_embed = discord.Embed(title = f"{target.name} was healed by a Forest Tome.", description = f"You were healed for ❤️ {use_health}", color = discord.Color.from_rgb(11,140,33))

                if target.id == 470650378271326208:
                    rando = random.choice([1,1,2])
                    if rando == 2:
                        tome_embed.add_field(name = f"A Forest Wisp comes to your aid!", value = f"**+1** {bot.get_emoji(993847218660446311)} Forest Wisp")
                        await Database.Update_User_Inventory(target.id, "item13", "add", 1)
            
                await interaction.response.edit_message(embed = tome_embed, view = None)
        

        if type == "overheal":
            pass
        

        if type == "damage":
            
            if key == "item4": # Knife
                knife_embed = discord.Embed(title = f"{target.name} was stabbed by a Knife!", description = f"**- {use_damage}** ❤️")
                crit_chance = random.choice([1,1,1,1,1,1,1,1,2])
                
                if current_health - use_damage <= 0: # They just died
                    h = 100
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                    await Tools.Apply_Death(ctx, bot, target.id, severity)
                
                else: # Normal damage calculation
                    h = current_health - use_damage
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                

                await interaction.response.edit_message(embed = knife_embed, view = None)



        stats_db.commit()
        stats_db.close()

    # Update User's Inventory
    async def Update_User_Inventory(user_id, key, change, amount):
        inventory_db = sql.connect("./data/inventory_db.db")
        cursor = inventory_db.cursor()

        if change == "add":

            inventory_db = sql.connect("./data/inventory_db.db")
            cursor = inventory_db.cursor()

            get_query = f"SELECT {key} FROM users WHERE id = {user_id}"
            cursor.execute(get_query)
            raw_result = list(cursor.fetchall()[0])
            result = raw_result[0]
            new_count = int(result) + int(amount)
            
            update_query = f"UPDATE users SET {key} = '{new_count}' WHERE id = {user_id}"
            cursor.execute(update_query)
            inventory_db.commit()
            inventory_db.close()

        if change == "subtract":

            inventory_db = sql.connect("./data/inventory_db.db")
            cursor = inventory_db.cursor()

            get_query = f"SELECT {key} FROM users WHERE id = {user_id}"
            cursor.execute(get_query)
            raw_result = list(cursor.fetchall()[0])
            result = raw_result[0]
            new_count = result - amount
            
            update_query = f"UPDATE users SET {key} = '{new_count}' WHERE id = {user_id}"
            cursor.execute(update_query)
            inventory_db.commit()
            inventory_db.close()

    # Update User's Title
    async def Update_User_Title(user_id, title):
        user_db = sql.connect("./data/user_db.db")
        cursor = user_db.cursor()
        
        query = f"UPDATE users SET title = '{title}' WHERE id = {user_id}"
        
        cursor.execute(query)
        user_db.commit()
        user_db.close()

    # Update Fish Skill
    async def Update_User_Stats(user_id, stat, change, amount):
        stats_db = sql.connect("./data/stats_db.db")
        cursor = stats_db.cursor()

        if change == "add":

            get_query = f"SELECT {stat} FROM users WHERE id = {user_id}"
            cursor.execute(get_query)
            raw_result = list(cursor.fetchall()[0])
            result = raw_result[0]
            new_count = int(result) + int(amount)
            
            update_query = f"UPDATE users SET {stat} = '{new_count}' WHERE id = {user_id}"
            cursor.execute(update_query)
            stats_db.commit()
            stats_db.close()

        if change == "subtract":

            get_query = f"SELECT {stat} FROM users WHERE id = {user_id}"
            cursor.execute(get_query)
            raw_result = list(cursor.fetchall()[0])
            result = raw_result[0]
            new_count = result - amount
            
            update_query = f"UPDATE users SET {stat} = '{new_count}' WHERE id = {user_id}"
            cursor.execute(update_query)
            stats_db.commit()
            stats_db.close()



class Views():
    
    # Get and Set Profile View
    async def Setup_Profile(bot, member, ctx):
        
        status = await Tools.Generate_Status(member.id)
        title, t_color = await Database.Fetch_Title(bot, member.id)
        wallet, bank = await Database.Fetch_Balance(bot, member.id)
        level, messages = await Database.Fetch_Level(member, bot, ctx)
        skills = await Database.Fetch_Stats(ctx.author.id)


        embed = discord.Embed(title = f"{member.name}'s Profile", description = f"{title}", color = t_color)
        embed.add_field(name = f"Wallet:", value = f"{bot.get_emoji(985978616741511208)} {wallet}", inline = False)
        embed.add_field(name = f"Bank:", value = f"{bot.get_emoji(985978615911051314)} {bank}", inline = False)
        embed.add_field(name = f"Level: {level}", value = f"**({messages})** Messages Sent")
        embed.set_thumbnail(url = member.avatar.url)
        embed.set_footer(text= f"{status}", icon_url= ctx.author.avatar.url)

        # Profile View
        class ProfileView(discord.ui.View):

            # Profile button
            @discord.ui.button(
                label="Profile",
                style=discord.ButtonStyle.blurple
            )
            async def profile_button_callback(self, button: discord.Button, interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    title, t_color = await Database.Fetch_Title(bot, member.id)
                    
                    profile_embed = discord.Embed(title = f"{member.name}'s Profile", description = f"{title}", color = t_color)
                    profile_embed.add_field(name = f"Wallet:", value = f"{bot.get_emoji(985978616741511208)} {wallet}", inline = False)
                    profile_embed.add_field(name = f"Bank:", value = f"{bot.get_emoji(985978615911051314)} {bank}", inline = False)
                    profile_embed.add_field(name = f"Level: {level}", value = f"**({messages})** Messages Sent")
                    profile_embed.set_thumbnail(url = member.avatar.url)
                    profile_embed.set_footer(text= f"{status}", icon_url= ctx.author.avatar.url)

                    await interaction.response.edit_message(embed = profile_embed, view = ProfileView())


            @discord.ui.button(
                label="Stats",
                style=discord.ButtonStyle.blurple
            )
            async def stats_button_callback(self, button: discord.Button, interaction: discord.Interaction):
                if member.id == interaction.user.id: # Continue code
                    title, t_color = await Database.Fetch_Title(bot, member.id)
                    work_skill = skills["work_skill"]
                    fish_skill = skills["fish_skill"]
                    fish_skill_name, fish_skill_description, fish_skill_emoji = await Tools.Create_Skill_Title("fish", fish_skill)

                    skills_embed = discord.Embed(title = f"{member.name}'s Skills", description = f"{title}", color = t_color)
                    skills_embed.add_field(name = f"Work Skill:", value = f"{work_skill}", inline = False)
                    skills_embed.add_field(name = f"{bot.get_emoji(fish_skill_emoji)} {fish_skill_name} ", value = f"{fish_skill_description} ", inline = False)
                    skills_embed.set_thumbnail(url = member.avatar.url)
                    skills_embed.set_footer(text= f"{status}", icon_url= ctx.author.avatar.url)

                    await interaction.response.edit_message(embed = skills_embed, view = ProfileView())

                else: # Not the correct user
                    return


            @discord.ui.button(
                label = "Title",
                style = discord.ButtonStyle.blurple
            )
            async def title_button_callback(self, button: discord.Button, interaction: discord.Interaction):
                if member.id == interaction.user.id: # Continue code
                    title, t_color = await Database.Fetch_Title(bot, member.id)
                    title_embed = discord.Embed(title = "Title Selection", description = title, color = t_color)
                    raw_options = await Database.Fetch_Title_Items(member.id)
                    
                    class TitleSelection(discord.ui.Select):
                        def __init__(self):
                            options = [
                                discord.SelectOption(label = "Default", description = "No title.")
                            ]
                            

                            if "demon" in raw_options: # If they are me.
                                option = discord.SelectOption(
                                    label = "Demon", description = "Demon King.",
                                    emoji= bot.get_emoji(887992464659611658)
                                )
                                options.append(option)

                            if "instigator" in raw_options: # If they are me.
                                demon_option = discord.SelectOption(
                                    label = "Instigator", description = "Do some instigating.", emoji = bot.get_emoji(986078219730059325)
                                )
                                options.append(demon_option)

                            if "golden" in raw_options: # If they are me.
                                demon_option = discord.SelectOption(
                                    label = "Golden", description = "Time to show off how wealthy you are.", emoji = bot.get_emoji(985978615911051314)
                                )
                                options.append(demon_option)

                            if "kami" in raw_options: # If they are me.
                                kami_option = discord.SelectOption(
                                    label = "Kami", description = "Protector and ruler of the forest.", emoji = bot.get_emoji(993848035253694484)
                                )
                                options.append(kami_option)


                            super().__init__(
                                placeholder="Choose a title to equip.",
                                options = options
                            )


                        async def callback(self, interaction: discord.Interaction):
                            selection = self.values[0]
                            complete_embed = discord.Embed(title = "Title change completed.")

                            await Database.Update_User_Title(member.id, selection.lower())
                            await interaction.response.edit_message(embed = complete_embed, view = ProfileView())
                


                    # Title View
                    class TitleView(discord.ui.View):
                        # TODO Get all their items that also have titles
                        # TODO Add them to the selection based on which titles you have
                        pass


                    view = TitleView()
                    view.add_item(TitleSelection())
                    await interaction.response.edit_message(embed = title_embed, view = view)

                else: # Not the correct user
                    return


        view = ProfileView()
        return embed, view

    # Get and Set Fish View
    async def Setup_Fish(bot, user):
        user_id = user.id
        stats = await Database.Fetch_Stats(user_id)
        title, t_color = await Database.Fetch_Title(bot, user_id)
        config = await Configuration.Fetch_Configuration_File()

        if stats["fish_skill"] >= 0:
            chances = [1,1,1,2,1,1,1,2,1,1,1,2,1,1,1]
            chance = random.choice(chances)

            if chance == 1:
                fish_amount = config["fish_amount"]
                fish_skill_amount = config["fish_skill_amount"]
                await Database.Update_User_Inventory(user_id, "item5", "add", 1)
                await Database.Update_User_Stats(user_id, "fish_skill", "add", fish_skill_amount)

                embed = discord.Embed(title = f"{user.name} Caught a Fish!", description = f"{title}", color = t_color)
                embed.add_field(name = f"**+ {fish_amount}** {bot.get_emoji(888412218415255582)} Sea Bass", value = f"**+ {fish_skill_amount}** {bot.get_emoji(888402427647254538)} Fishing Skill", inline = False)

                return embed

            if chance == 2:
                await Database.Update_User_Stats(user_id, "fish_skill", "subtract", 1)
                
                embed = discord.Embed(title = f"{user.name} Your Line Broke!", description = f"{title}", color = t_color)
                embed.add_field(name = f"Your line broke and you caught nothing.", value = f"**- 1** {bot.get_emoji(888402427647254538)} Fishing Skill", inline = False)

                return embed

    # Hunt View
    async def Setup_Hunting(bot, ctx, user_id):
        stats = await Database.Fetch_Stats(user_id)
        title, t_color = await Database.Fetch_Title(bot, user_id)
        config = await Configuration.Fetch_Configuration_File()

        # TODO Hunting skill maybe changes which animals you hunt?
        # TODO Hunt 4 Animals - Squirrels, Foxes, Elephants, Bears
        # Golden Squirrel, Fox Fur, Elephant Tusk, Bear Pelt, & Raw Meat from all

        embed = discord.Embed(title = f"{ctx.author.name} began Hunting.", description = title, color = t_color)

        class Hunt_View(discord.ui.View):

            @discord.ui.button(
                label = "Squirrel",
                style = discord.ButtonStyle.gray,
                emoji = "🐿️"
            )
            async def squirrel_callback(self, button: discord.Button, interaction: discord.Interaction):
                if user_id == interaction.user.id:
                    chance = [1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                    choice = random.choice(chance)
                    
                    if choice == 1: # Normal Squirrel
                        meat_amount = random.randrange(1,5)
                        hunt_amount = config["hunt_amount"]
                        meat = int(meat_amount) * int(hunt_amount)
                        hunt_skill_amount = config["hunt_skill_amount"]
                        
                        await Database.Update_User_Inventory(user_id, "item6", "add", meat)
                        await Database.Update_User_Stats(user_id, "hunt_skill", "add", hunt_skill_amount)

                        hunt_embed = discord.Embed(title = f"{ctx.author.name} shot a Squirrel!", description = f"{title}", color = t_color)
                        hunt_embed.add_field(name = f"**+ {meat}** {bot.get_emoji(988567158487416910)} Raw Meat", value = f"**+ {hunt_skill_amount}** {bot.get_emoji(819685239306715207)} Hunting Skill", inline = False)
                        hunt_embed.set_thumbnail(url = "https://i.imgur.com/lZguvTQ.png")
                        await interaction.response.edit_message(embed = hunt_embed, view = None)
                    
                    if choice == 2: # Golden Squirrel
                        meat_amount = random.randrange(5,10)
                        hunt_amount = config["hunt_amount"]
                        meat = int(meat_amount) * int(hunt_amount)
                        hunt_skill_amount = config["hunt_skill_amount"]
                        
                        await Database.Update_User_Inventory(user_id, "item6", "add", meat)
                        await Database.Update_User_Stats(user_id, "hunt_skill", "add", hunt_skill_amount)

                        hunt_embed = discord.Embed(title = f"{ctx.author.name} shot a Golden Squirrel!", description = f"{title}", color = t_color)
                        hunt_embed.add_field(name = f"**+ {meat}** {bot.get_emoji(988567158487416910)} Raw Meat", value = f"**+ {hunt_skill_amount}** {bot.get_emoji(819685239306715207)} Hunting Skill", inline = False)
                    
                        await interaction.response.edit_message(embed = hunt_embed, view = None)

            @discord.ui.button(
                label = "Fox",
                style = discord.ButtonStyle.gray,
                emoji = "🦊"
            )
            async def fox_callback(self, button: discord.Button, interaction: discord.Interaction):
                if user_id == interaction.user.id:
                    meat = random.randrange(2,6)
                    fur = random.randrange(1,3)
                    hunt_amount = config["hunt_amount"]
                    hunt_skill_amount = config["hunt_skill_amount"]

                    await Database.Update_User_Inventory(user_id, "item6", "add", meat)
                    await Database.Update_User_Inventory(user_id, "item8", "add", fur)
                    await Database.Update_User_Stats(user_id, "hunt_skill", "add", hunt_skill_amount)

                    hunt_embed = discord.Embed(title = f"{ctx.author.name} shot a Fox!", description = f"{title}", color = t_color)
                    hunt_embed.add_field(name = f"**+ {meat}** {bot.get_emoji(988567158487416910)} Raw Meat\n+ {fur} {bot.get_emoji(988836983856050266)} Fox Fur", value = f"**+ {hunt_skill_amount}** {bot.get_emoji(819685239306715207)} Hunting Skill", inline = False)
                    hunt_embed.set_thumbnail(url = "https://i.imgur.com/yvkNwA7.png")
                    await interaction.response.edit_message(embed = hunt_embed, view = None)


        view = Hunt_View()
        message = await ctx.respond(
            embed = embed,
            view = view
        )

    # Get and Set Work View
    async def Setup_Work(bot, member):
        title, t_color = await Database.Fetch_Title(bot, member.id)

        embed = discord.Embed(title = f"{member}'s Began Working", description = f"{title}", color = t_color)
        embed.add_field(name = "Press the button", value = "to mine silver.")
        embed.set_thumbnail(url = member.avatar.url)

        class Work_View(discord.ui.View):
            
            @discord.ui.button(label = "1", style = discord.ButtonStyle.blurple)
            async def first_option_callback(self, button: discord.Button, interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    
                    amount = random.randrange(10,100)

                    first_option_embed = discord.Embed(title = f"Nice! You mined up {bot.get_emoji(985978616741511208)} {amount} silver bars!", description=f"{title}", color = t_color)
                    await Database.Update_Balance(member.id, "wallet", amount)

                    await interaction.message.edit(
                        embed = first_option_embed,
                        view = None
                    )

                else:
                    pass

        view = Work_View()
        return embed, view

    # Get and Set Shop View
    async def Setup_Shop(bot, member, shop_selection, guild_id):
        title, t_color = await Database.Fetch_Title(bot, member.id)
        shopables = await Database.Fetch_Shopables(guild_id) # List of keys that can be bought currently
        items = await Database.Fetch_Itemlist()

        embed = discord.Embed(title = "Item Shop", description=f"{title}", color = t_color)

        i = 0
        while i < 10:
            try:
                key = shopables[i]
                
                item_name = items[key]["name"]
                item_description = items[key]["description"]
                item_emoji = items[key]["emoji"]
                item_rarity = items[key]["rarity"]
                item_value = items[key]["store_value"]

                embed.add_field(name = f"{bot.get_emoji(985978616741511208)} **{item_value:,}** - {bot.get_emoji(item_emoji)} {item_name} {bot.get_emoji(item_rarity)}", value = f"{item_description}", inline=False)

            except:
                pass
            i += 1

        class Shop_View(discord.ui.View):

            @discord.ui.button(label = "1", style = discord.ButtonStyle.blurple)
            async def first_option_callback(self, button: discord.Button, interaction: discord.Interaction):
                page1_embed = discord.Embed(title = "Item Shop", description=f"{title}", color = t_color)
                if member.id == interaction.user.id: # If the person who clicked is the author

                    i = 0
                    while i < 10:
                        try:
                            key = shopables[i]
                            
                            item_name = items[key]["name"]
                            item_description = items[key]["description"]
                            item_emoji = items[key]["emoji"]
                            item_rarity = items[key]["rarity"]
                            item_value = items[key]["store_value"]

                            page1_embed.add_field(name = f"{bot.get_emoji(985978616741511208)} **{item_value:,}** - {bot.get_emoji(item_emoji)} {item_name} {bot.get_emoji(item_rarity)}", value = f"{item_description}", inline=False)

                        except:
                            pass
                        i += 1
                    await interaction.response.edit_message(embed = page1_embed, view = Shop_View())
                else:
                    pass

            @discord.ui.button(label = "2", style = discord.ButtonStyle.blurple)
            async def second_option_callback(self, button: discord.Button, interaction: discord.Interaction):
                page2_embed = discord.Embed(title = "Item Shop", description=f"{title}", color = t_color)
                if member.id == interaction.user.id: # If the person who clicked is the author

                    i = 10
                    while i < 20:
                        try:
                            key = shopables[i]
                            
                            item_name = items[key]["name"]
                            item_description = items[key]["description"]
                            item_emoji = items[key]["emoji"]
                            item_rarity = items[key]["rarity"]
                            item_value = items[key]["store_value"]

                            page2_embed.add_field(name = f"{bot.get_emoji(985978616741511208)} **{item_value:,}** - {bot.get_emoji(item_emoji)} {item_name} {bot.get_emoji(item_rarity)}", value = f"{item_description}", inline=False)

                        except:
                            pass
                        i += 1
                    
                    await interaction.response.edit_message(embed = page2_embed, view = Shop_View())
                else:
                    pass



        view = Shop_View()
        return embed, view

    # Get and Set Inventory View
    async def Setup_Inventory(bot, member):
        title, t_color = await Database.Fetch_Title(bot, member.id)
        items = await Database.Fetch_Itemlist()
        user_items = await Database.Fetch_User_Items(member.id)
        # Display it based on page
        
        embed = discord.Embed(title = f"{member.name}'s Inventory", description=f"{title}", color = t_color)

        i = 0
        while i < len(user_items) and i < 10:
            try:
                key = user_items[i]

                item_name = items[key]["name"]
                item_description = items[key]["description"]
                item_emoji = items[key]["emoji"]
                item_rarity = items[key]["rarity"]
                amount = await Database.Fetch_Item_Amount(member.id, key)

                embed.add_field(name = f"{bot.get_emoji(item_emoji)} {item_name} {bot.get_emoji(item_rarity)} - **({amount})**", value = f"{item_description}", inline = False)
            
            except TypeError:
                pass
            i += 1

        class Inventory_View(discord.ui.View):

            @discord.ui.button(label = "1", style = discord.ButtonStyle.blurple)
            async def first_option_callback(self, button: discord.Button, interaction: discord.Interaction):
                first_embed = discord.Embed(title = f"{member.name}'s Inventory", description=f"{title}", color = t_color)

                i = 0
                while i < len(user_items) and i < 10:
                    try:
                        key = user_items[i]

                        item_name = items[key]["name"]
                        item_description = items[key]["description"]
                        item_emoji = items[key]["emoji"]
                        item_rarity = items[key]["rarity"]
                        amount = await Database.Fetch_Item_Amount(member.id, key)

                        first_embed.add_field(name = f"{bot.get_emoji(item_emoji)} {item_name} {bot.get_emoji(item_rarity)} - **({amount})**", value = f"{item_description}", inline = False)
                    
                    except TypeError:
                        pass
                    i += 1
                view = Inventory_View()
                await interaction.response.edit_message(embed = first_embed, view = view)
        
            @discord.ui.button(label = "2", style = discord.ButtonStyle.blurple)
            async def second_option_callback(self, button: discord.Button, interaction: discord.Interaction):
                second_embed = discord.Embed(title = f"{member.name}'s Inventory", description=f"{title}", color = t_color)

                i = 10# Just add + 10 to the checks I believe, or +9 whichever works
                while i < len(user_items):
                    try:
                        key = user_items[i]

                        item_name = items[key]["name"]
                        item_description = items[key]["description"]
                        item_emoji = items[key]["emoji"]
                        item_rarity = items[key]["rarity"]
                        amount = await Database.Fetch_Item_Amount(member.id, key)

                        second_embed.add_field(name = f"{bot.get_emoji(item_emoji)} {item_name} {bot.get_emoji(item_rarity)} - **({amount})**", value = f"{item_description}", inline = False)
                    
                    except TypeError:
                        pass
                    i += 1
                view = Inventory_View()
                await interaction.response.edit_message(embed = second_embed, view = view)

        return embed, Inventory_View()

    # Purchase Item View
    async def Setup_Purchase(bot, member, key, item_amount, cost, title, t_color):
        
        class Purchase_View(discord.ui.View):
            
            @discord.ui.button(label = "Accept", style = discord.ButtonStyle.green)
            async def accept_callback(self, button: discord.Button, interaction: discord.Interaction):
                if member.id == interaction.user.id:
                # Make the transaction
                    await Database.Update_Balance(member.id, "wallet", -cost)
                    await Database.Update_User_Inventory(member.id, key, "add", item_amount)

                    embed = discord.Embed(title = "Purchase Completed.", description = f"{title}", color = t_color)

                    await interaction.response.edit_message(embed = embed, view = None)
                else:
                    pass


            @discord.ui.button(label = "Decline", style = discord.ButtonStyle.red)
            async def decline_callback(self, button: discord.Button, interaction: discord.Interaction):
                if member.id == interaction.user.id:
                # Decline the transaction
                    embed = discord.Embed(title = "Purchase Declined.", description = f"{title}", color = t_color)
                    await interaction.response.edit_message(embed = embed, view = None)
                else:
                    pass
        
        return Purchase_View()

    # Selling items View
    async def Setup_Sell(bot, member, key, item_amount, value, tax, title, t_color):
        
        class Sell_View(discord.ui.View):

            @discord.ui.button(label = "Accept", style = discord.ButtonStyle.green)
            async def accept_callback(self, button: discord.Button, interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    await Database.Update_Balance(member.id, "wallet", +value)
                    await Database.Update_User_Inventory(member.id, key, "subtract", item_amount)

                    embed = discord.Embed(title = "Sale Completed.", description = f"{title}", color = t_color)

                    await interaction.response.edit_message(embed = embed, view = None)
                else:
                    pass


            @discord.ui.button(label = "Decline", style = discord.ButtonStyle.red)
            async def decline_callback(self, button: discord.Button, interaction: discord.Interaction):
                if member.id == interaction.user.id:
                    embed = discord.Embed(title = "Sale Declined.", description = f"{title}", color = t_color)
                    await interaction.response.edit_message(embed = embed, view = None)
                else:
                    pass
        
        return Sell_View()

    # Moderation Menu View
    async def Setup_ModMenu(bot,ctx, target, user):
        # TODO if the target is the same as the user, display commands like purge
        # TODO Selection menu for banning, kicking, stripping, 
        # TODO Give second selection for getting all roles in the server and selecting which to give
        # TODO Purge messages view to select how many messages

        if target.id == user.id: # Unlock utility menu
            embed = discord.Embed(title = "Mod Menu: Utility Menu", description="Select what action you would like to initiate.", color = discord.Color.from_rgb(247,83,20))
            embed.set_thumbnail(url = "https://i.imgur.com/fNwDRTv.png")

            class ModMenu_View(discord.ui.View):
                
                @discord.ui.select(
                    placeholder="Select an action.",
                    options=[
                        discord.SelectOption(label = "Purge", description = "Purge 50 messages from this channel.")
                    ]
                )
                async def selection_callback(self, select, interaction: discord.Interaction):
                    selection = select.values[0]

                    if selection == "Purge":
                        await ctx.channel.purge(limit = 50)
            


            view = ModMenu_View()
            return embed, view
            

        
        else: # Unlock targeted member menu
            embed = discord.Embed(title = "Test")

            class ModMenu_View(discord.ui.View):
                
                @discord.ui.select(
                    placeholder="Select an action.",
                    options=[
                        discord.SelectOption(label = "Kick", description = "Kick the user from the server."),
                        discord.SelectOption(label = "Ban", description = "Ban the user from the server."),
                        discord.SelectOption(label = "Strip", description = "Strip all roles from a user."),
                        discord.SelectOption(label = "Role", description = "Add a role to a user."),
                        discord.SelectOption(label = "Rollback", description = "Delete all messages from the user for the past 12 hours.")
                    ]
                )
                async def selection_callback(self, select, interaction: discord.Interaction):
                    selection = select.values[0]

                    if selection == "Kick":
                        pass
            


            view = ModMenu_View()
            return embed, view

    # TODO Using Items View
    async def Setup_Use(bot, ctx, target):
        user_id = ctx.author.id
        target_id = target.id
        items = await Database.Fetch_Itemlist()
        title, t_color = await Database.Fetch_Title(bot, user_id)

        self_usable, target_usable = await Database.Fetch_Usables(user_id) # Returns keys of items the user owns


        if user_id == target_id: # If they targeted themselves
            embed = discord.Embed(title = f"{ctx.author.name}'s usable items**:**", description = title, color = t_color)

            class BasicChest_Button(discord.ui.Button):
                def __init__(self):
                    emoji = bot.get_emoji(887651039573082122)
                    super().__init__(
                        label = "Basic Chest",
                        style = discord.ButtonStyle.gray,
                        emoji = emoji
                    )
                async def callback(self, interaction: discord.Interaction):
                    user = interaction.user
                    title, t_color = await Database.Fetch_Title(bot, user_id)
                    if user.id == user_id:
                        drop = random.choice([1,1,2,1,1,1,2,1,1,2,1,3,2,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,1,1,1,1,1,2])
                        open_embed = discord.Embed(title = f"{ctx.author.name} opened a Basic Chest!", description = title, color = t_color)

                        if drop == 1: # Milk
                            item_key = "item9"
                            item_amount = items["item10"]["drop_table"]["item9"]

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {item_amount}** {bot.get_emoji(988842419925708860)} Milk")
                            await Database.Update_User_Inventory(user_id, item_key, "add", item_amount)
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)

                        if drop == 2: # Lime
                            item_key = "item7"
                            item_amount = items["item10"]["drop_table"]["item7"]

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {item_amount}** {bot.get_emoji(988820202361864252)} Limes")
                            await Database.Update_User_Inventory(user_id, item_key, "add", item_amount)
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)

                        if drop == 3: # Special Golden Bar
                            item_key = "item11"
                            item_amount = items["item10"]["drop_table"]["item11"]

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {item_amount}** {bot.get_emoji(985978615911051314)} Special Golden Bar!")
                            await Database.Update_User_Inventory(user_id, item_key, "add", item_amount)
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)

                        await interaction.response.edit_message(embed = open_embed, view = None)

                    else:
                        pass

            
            class TomeOfTheForest_Button(discord.ui.Button):
                def __init__(self):
                    emoji = bot.get_emoji(993842394044837968)
                    super().__init__(
                        label = "Forest Tome",
                        style = discord.ButtonStyle.gray,
                        emoji = emoji
                    )
                async def callback(self, interaction: discord.Interaction):
                    user = interaction.user
                    title, t_color = await Database.Fetch_Title(bot, user_id)
                    if user.id == user_id:
                        key = "item12"
                        await Database.Update_User_Health(ctx, bot, target, "heal", 1, key, interaction)
                    else:
                        pass


            class ForestWisp_Button(discord.ui.Button):
                pass


            class Self_Menu(discord.ui.View):
                # TODO Show all usable items, with multiple pages of buttons
                
                pass


            view = Self_Menu()


            if 1 == 1: # Add buttons to view
                if "item10" in self_usable:
                    view.add_item(BasicChest_Button())
                    embed.add_field(name = f"{bot.get_emoji(887651039573082122)} Basic Chest {bot.get_emoji(880040222367289385)} - **(amount)**", value = "Open this chest for goodies!", inline = False)
                if "item12" in self_usable:
                    view.add_item(TomeOfTheForest_Button())
                    embed.add_field(name = f"{bot.get_emoji(993842394044837968)} Tome of The Forest {bot.get_emoji(880071881301053490)}", value = "Heal others or use it on yourself for a chance to create wisps!", inline = False)
          

            message = await ctx.respond(embed = embed, view = view)
        
        if user_id != target_id: # Targeted Someone Else
            embed = discord.Embed(title = f"{ctx.author.name}'s usable items**:**", description = title, color = t_color)

            class ForestWisp_Button(discord.ui.Button):
                
                pass
            

            class Knife_Button(discord.ui.Button):
                def __init__(self):
                    emoji = bot.get_emoji(986786881255641138)
                    super().__init__(
                        label = "Knife",
                        style = discord.ButtonStyle.gray,
                        emoji = emoji
                    )
                async def callback(self, interaction: discord.Interaction):
                    user = interaction.user
                    title, t_color = await Database.Fetch_Title(bot, user_id)

                    if user.id == user_id:
                        key = "item4"
                        await Database.Update_User_Health(ctx, bot, target, "damage", 1, key, interaction)


            class TomeOfTheForest_Button(discord.ui.Button):
                def __init__(self):
                    emoji = bot.get_emoji(993842394044837968)
                    super().__init__(
                        label = "Forest Tome",
                        style = discord.ButtonStyle.gray,
                        emoji = emoji
                    )
                async def callback(self, interaction: discord.Interaction):
                    user = interaction.user
                    title, t_color = await Database.Fetch_Title(bot, user_id)
                    if user.id == user_id:
                        key = "item12"
                        await Database.Update_User_Health(ctx, bot, target, "heal", 1, key, interaction)
                    else:
                        pass



            class Target_Menu(discord.ui.View):
                # TODO Show items that can target the user
                pass
            
            view = Target_Menu()


            if "item4" in target_usable: # Knife
                view.add_item(Knife_Button())   
            if "item12" in target_usable: # Tome of The Forest
                view.add_item(TomeOfTheForest_Button())
            #if "item13" in target_usable: # Tome of The Forest
            #    view.add_item(ForestWisp_Button())
            
            
            message = await ctx.respond(embed = embed, view = view)



class Cooldowns():

    # Adds cooldowns to the cooldown container
    async def add_cooldown(cooldown, user_id):
        config = await Configuration.Fetch_Configuration_File()
        
        if str(cooldown).lower() == "work":
            work_cooldowns.append(user_id)
            await asyncio.sleep(config["work_cooldown"]) # Use configuration file to determine cooldown length
            work_cooldowns.remove(user_id)
        
        if cooldown == "fish":
            fish_cooldowns.append(user_id)
            await asyncio.sleep(config["fish_cooldown"]) # Use configuration file to determine cooldown length
            fish_cooldowns.remove(user_id)
    
        if cooldown == "hunt":
            hunt_cooldowns.append(user_id)
            await asyncio.sleep(config["hunt_cooldown"]) # Use configuration file to determine cooldown length
            hunt_cooldowns.remove(user_id)

    # Retrieve cooldowns
    async def get_cooldowns(cooldown):
        if str(cooldown).lower() == "work":
            return work_cooldowns
        if cooldown == "fish":
            return fish_cooldowns
        if cooldown == "hunt":
            return hunt_cooldowns



class Tools():
    
    async def Generate_Status(user_id):
        stats = await Database.Fetch_Stats(user_id)
        health = stats["health"]
        # Go through stats and generate status effects
        needed_emojis = []
        status = " "

        if stats["toxin"] == "true":
            needed_emojis.append("🤢")

        

        if len(needed_emojis) > 0:
            status_emojis = [" | "] + needed_emojis
            
            emojis = " ".join(str(x) for x in status_emojis)
            
            status = f"❤️ {health}{emojis}"
        
        else:
            status = f"❤️ {health}"
        
        return status


    # Creating skill title
    async def Create_Skill_Title(skill_name, skill_amount):
        if skill_name == "fish":
            if int(skill_amount) >= 0:
                skill_emoji = 888402427647254538
                skill_name = "New Fisher"
                skill_description = f"**Skill: ({skill_amount})**"
                
                return skill_name, skill_description, skill_emoji


    # Generating item use information
    async def Generate_Use_Info(key):
        items = await Database.Fetch_Itemlist()
        use_health = items[key]["use_health"]
        use_description = items[key]["use_description"]
        use_damage = items[key]["use_damage"]
        
        return use_health, use_description, use_damage


    # Calculate damage and reduce currency
    async def Apply_Death(ctx, bot, user, severity):
        severity_one_cost = random.randrange(1000, 3000)
        stats_db = sql.connect("./data/stats_db.db")
        cursor = stats_db.cursor()
        death_embed = discord.Embed(title = f"{user.name} You died.")

        if severity == 1:
            death_embed.add_field(name = "You were forced to pay god silver to bring you back to life.", value = f"**- {severity_one_cost}** {bot.get_emoji(985978616741511208)} Silver")
            h = 100
            update_query = f"UPDATE users SET health = '{h}' WHERE id = {user.id}"
            cursor.execute(update_query)

            await Database.Update_Balance(user.id, "wallet", -severity_one_cost)
        
        
        await ctx.send(death_embed)

            
    # Function for giving loot chests
    async def Give_LootChest(bot, ctx):
        user_id = ctx.author.id
        config = await Configuration.Fetch_Configuration_File()

        drop_amount = config["chest_drop_amount"]
        drop_chance = config["chest_drop_chance"]
        chance = random.choice(drop_chance)

        event = config["event"]

        if event == "normal": # Normal loot crates
            if chance == 2: # Give them a crate
                await Database.Update_User_Inventory(user_id, "item10", "add", 1)
                await ctx.respond(f"{ctx.author.mention}, you found a {bot.get_emoji(887651039573082122)} **Basic Loot Chest**!")