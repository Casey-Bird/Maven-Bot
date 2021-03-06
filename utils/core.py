

import discord, json, asyncio, random
import sqlite3 as sql



work_cooldowns = [] # Cooldown container for users who crafted recently
fish_cooldowns = [] # Cooldown container for users who crafted recently
hunt_cooldowns = [] # Cooldowns for hunting
craft_cooldowns = [] # Cooldown container for users who crafted recently
attack_cooldowns = [] # Cooldowns for users who just attacked

use_cooldown = [] # Cooldown for items used on themselves
use_target_cooldown = [] # Cooldown for any item that does damage to another user


class Configuration():
    bot_version = "0.0"

    async def Fetch_Configuration_File():
        file = open("./data/config.json")
        data = json.load(file)

        return data




class Database():

    # User creation.
    async def Create_User(user_id):

        def Create_Skills(user_id):
            skills_db = sql.connect("./data/skills_db.db")
            cursor = skills_db.cursor()
            query = f"INSERT INTO users (id) VALUES ({user_id})"
            cursor.execute(query)
            skills_db.commit()
            skills_db.close()


        def Check_Existing_Skills(user_id):
            skills_db = sql.connect("./data/skills_db.db")
            cursor = skills_db.cursor()

            query = f"SELECT * FROM users WHERE id = {user_id}"

            cursor.execute(query)
            result = cursor.fetchall()

            if not result: # Result didn't fetch anything
                Create_Skills(user_id)
            else:
                pass
            
            skills_db.close()


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
        Check_Existing_Skills(user_id)

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

    # Fetch all the skills the user owns
    async def Fetch_User_Skills(user_id):
        config = await Configuration.Fetch_Configuration_File()

        skills_db = sql.connect("./data/skills_db.db")
        cursor = skills_db.cursor()
        # Depending on skills will edit the query and check for those items...if more than 0 then add to list

        user_skills = []

        i = 1
        while i < config["max_items"]:
            try:
                get_query = f"SELECT skill{str(i)} FROM users WHERE id = {user_id}"
                cursor.execute(get_query)
                result = list(cursor.fetchall()[0])
                item_amount = result[0]
                if item_amount > 0:
                    user_skills.append(f"skill{str(i)}")
            except:
                pass

            i += 1
        
        skills_db.close()
        return user_skills

    # Fetch user's equipped skills
    async def Fetch_User_Equipped_Skills(user_id):
        config = await Configuration.Fetch_Configuration_File()

        skills_db = sql.connect("./data/skills_db.db")
        cursor = skills_db.cursor()

        user_equipped_skill = []

        i = 1
        while i < config["max_items"]:
            try:
                skill = "skill"+ str(i)

                get_query = f"SELECT {skill} FROM users WHERE id = {user_id}"
                cursor.execute(get_query)
                result = list(cursor.fetchall()[0])
                skill_amount = result[0]

                if skill_amount > 0:
                    user_equipped_skill.append(skill)
                
                i += 1
                
            except sql.OperationalError:
                break
        
        skills_db.close()
        print(user_equipped_skill)

        return user_equipped_skill

    # Fetch the entire items.json file
    async def Fetch_Itemlist():
        file = open("./data/items.json")
        data = json.load(file)

        return data

    # Fetch the entire skills.json file
    async def Fetch_Skills():
        file = open("./data/skills.json")
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
                title = f"{bot.get_emoji(999793524394430525)} Viridian Emperor {bot.get_emoji(999793524394430525)}"
                t_color = discord.Color.from_rgb(100,217,154)

            if title_name == "void":
                title = f"{bot.get_emoji(997271210285092974)} Avatar of the Void {bot.get_emoji(997271210285092974)}"
                t_color = discord.Color.from_rgb(48,22,77)

            if title_name == "frostking":
                title = f"{bot.get_emoji(997989353060040875)} Frost King {bot.get_emoji(997989353060040875)}"
                t_color = discord.Color.from_rgb(10,209,240)

            if title_name == "frostlord":
                title = f"{bot.get_emoji(998612997285097522)} Frost Lord {bot.get_emoji(998612997285097522)}"
                t_color = discord.Color.from_rgb(10,209,240)


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
        maven = 155751780674699264

        if user_id == 155751780674699264 or user_id == maven: # Maven's ID
            titles.append("demon")
        if user_id == 743597640012398643 or user_id == maven: # Nick's ID
            titles.append("instigator")
        if user_id == 173008417013760000 or user_id == maven: # VoidPapi's ID
            titles.append("void")

        if "item11" in user_items:
            titles.append("golden")
        
        if "item12" in user_items:
            titles.append("kami")

        if "item16" in user_items:
            titles.append("frostking")

        if "item18" in user_items:
            titles.append("frostlord")


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

    # Fetch Current Health
    async def Fetch_User_Health(user_id):
        stats_db = sql.connect("./data/stats_db.db")
        cursor = stats_db.cursor()

        get_query = f"SELECT health FROM users WHERE id = {user_id}"
        cursor.execute(get_query)
        result = list(cursor.fetchall()[0])
        current_health = result[0]

        stats_db.close()
        return current_health

    # Fetch an item key based on user input
    async def Fetch_Item_Key(name):
        item = name.lower()

        worldlock_names = ["world", "world lock", "lock", "wl", "wls"]
        if item in worldlock_names:
            return "item1"
        
        eggplant_name = ["eggplant", "eggplants"]
        if item in eggplant_name:
            return "item2"

        banana_name = ["banana", "bananas", "banans", "banan"]
        if item in banana_name:
            return "item3"
        
        sword_name = ["sword", "swords", "swor"]
        if item in sword_name:
            return "item4"

        seabass_name = ["sea bass", "sea", "bass", "sea basses", "seabass"]
        if item in seabass_name:
            return "item5"

        rawmeat_name = ["raw meat", "raw", "meat", "raw meats", "rawmeat"]
        if item in rawmeat_name:
            return "item6"

        lime_name = ["lime", "limes"]
        if item in lime_name:
            return "item7"

        foxfur_name = ["foxfur", "furs", "fox", "fox fur", "fox furs", "foxes"]
        if item in foxfur_name:
            return "item8"

        milk_name = ["milk", "milks"]
        if item in milk_name:
            return "item9"

        basicchest_name = ["basicchest", "basic", "basic chest", "basic chests", "basics"]
        if item in basicchest_name:
            return "item10"

        specialgolden_name = ["special golden bar", "special golden", "special", "specialgoldenbar"]
        if item in specialgolden_name:
            return "item11"

        tome_name = ["tome"]
        if item in tome_name:
            return "item12"

        wisp_name = ["forest wisp", "forest", "wisp"]
        if item in wisp_name:
            return "item13"

        voidstone_name = ["void stone", "void ston", "void stones", "voidstone", "voidstones"]
        if item in voidstone_name:
            return "item14"

        voidstone_name = ["void knife", "void knive", "void knifes", "voidknife", "voidknifes", "voidknives"]
        if item in voidstone_name:
            return "item15"

        frostcrown_name = ["frost crown", "frost crowns", "frostcrown", "frostcrowns"]
        if item in frostcrown_name:
            return "item16"

        frostcrown_name = ["frost staff", "frost staffs", "froststaff", "froststaffs"]
        if item in frostcrown_name:
            return "item17"

        frostcirclet_name = ["frost circlet", "frostcirclet", "frost circlets"]
        if item in frostcirclet_name:
            return "item18"

        suspiciousmeal_name = ["suspicious", "suspicious meal", "suspiciousmeal"]
        if item in suspiciousmeal_name:
            return "item19"

        ironore_name = ["iron ore", "iron ores", "ironore"]
        if item in ironore_name:
            return "item20"

        ironingot_name = ["iron ingot", "iron ingots", "ironingot", "ironingots"]
        if item in ironingot_name:
            return "item21"

        copperore_name = ["copper ore", "copper ores", "copperore", "copperores"]
        if item in copperore_name:
            return "item22"

        copperingot_name = ["copper ingot", "copper ingots", "copperingot", "copperingots"]
        if item in copperingot_name:
            return "item23"

        ironpickaxe_name = ["iron pickaxe", "iron pick", "ironpickaxe", "ironpickaxes", "iron picks"]
        if item in ironpickaxe_name:
            return "item24"

        goldpickaxe_name = ["gold pickaxe", "golden pickaxes", "gold pickaxe", "golden pickaxe", "golden pick", "gold pick"]
        if item in goldpickaxe_name:
            return "item25"

        bloodcrystal_name = ["blood crystal", "bloodcrystal", "blood crystals", "bloodcrystal", "bloodcrystals"]
        if item in bloodcrystal_name:
            return "item26"

        mackeral_name = ["mackeral", "mackerals"]
        if item in mackeral_name:
            return "item27"

        viridianwarrior_name = ["viridian warrior", "viridianwarrior", "viridian warriors", "viridianwarriors"]
        if item in viridianwarrior_name:
            return "item28"


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
    async def Update_User_Health(user_id, change, type):
        # TODO Need to check for overheal or not
        current_health = await Database.Fetch_User_Health(user_id)
        max_health = 100

        stats_db = sql.connect("./data/stats_db.db")
        cursor = stats_db.cursor()

        if type == "heal":
            if current_health + change > max_health:
                update_query = f"UPDATE users SET health = '{max_health}' WHERE id = {user_id}"
                cursor.execute(update_query)
            else:
                change = current_health + change
                update_query = f"UPDATE users SET health = '{change}' WHERE id = {user_id}"
                cursor.execute(update_query)
            
            stats_db.commit()
            stats_db.close()


        # ALL OF THIS NEEDS TO BE DELETED
        if type == "heal": # TODO Create embed send for healing

            if key == "item19": # Suspicious Meal
                embed = discord.Embed(title = f"{target.name} ate a strangely healthy meal...", description = f"You were healed for ?????? {use_health}", color = discord.Color.from_rgb(11,140,33))

                stats_db.commit()
                stats_db.close()
                await interaction.response.edit_message(embed = embed, view = None)

        if type == "damage":
            

            if key == "item13": # Forest Wisp
                embed = discord.Embed(title = f"{target.name} was attacked by a Forest Wisp!", description = f"**- {use_damage}** ??????")
                crit_chance = random.choice([1,1,1,1,1,1,1,1,2])
                
                if current_health - use_damage <= 0: # They just died
                    await Tools.Apply_Death(ctx, bot, target.id, severity)
                    h = 100
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                
                else: # Normal damage calculation
                    h = current_health - use_damage
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                stats_db.commit()
                stats_db.close()

                await interaction.response.edit_message(embed = embed, view = None)

            if key == "item15": # Void Knife
                if crit_chance == 2:
                    use_damage = int(use_damage * 1.5)


                embed = discord.Embed(title = f"{target.name} was stabbed by a Void Knife!", description = f"**- {use_damage}** ??????")
                
                if crit_chance == 2:
                    embed.add_field(name = "Critical Hit!", value = "1.5x extra damage.")


                if current_health - use_damage <= 0: # They just died
                    await Tools.Apply_Death(ctx, bot, target.id, severity)
                    h = 100
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                
                else: # Normal damage calculation
                    h = current_health - use_damage
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                

                await interaction.response.edit_message(embed = embed, view = None)

                stats_db.commit()
                stats_db.close()

            if key == "item17": # Frost Staff
                if crit_chance == 2: # Setting use_damage to correct value
                    use_damage = int(use_damage * 1.5)

                embed = discord.Embed(title = f"{target.name} was blasted by a Frost Staff!", description = f"**- {use_damage}** ??????")
                
                if crit_chance == 2:
                    embed.add_field(name = "Critical Hit!", value = "1.5x extra damage.")


                if current_health - use_damage <= 0: # They just died
                    await Tools.Apply_Death(ctx, bot, target.id, severity)
                    h = 100
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                
                else: # Normal damage calculation
                    h = current_health - use_damage
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                
                stats_db.commit()
                stats_db.close()
                
                if frozen_immunity == "immune":
                    pass
                else:
                    await Database.Update_Status(target.id, "frozen", "true")
                    await ctx.send(f"{target.mention}, you've been frozen! {bot.get_emoji(636124362579116032)}")

                await interaction.response.edit_message(embed = embed, view = None)

            if key == "item28": # Viridian Warrior
                warrior_amount = await Database.Fetch_Item_Amount(ctx.author.id, key)
                use_damage = warrior_amount * items["item28"]["use_damage"]

                embed = discord.Embed(title = f"{target.name} was ambushed by Viridian Warriors!", description = f"**- {use_damage}** ??????")
                await Database.Update_User_Inventory(ctx.author.id, key, "subtract", warrior_amount)

                if current_health - use_damage <= 0: # They just died
                    await Tools.Apply_Death(ctx, bot, target.id, severity)
                    h = 100
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                
                else: # Normal damage calculation
                    h = current_health - use_damage
                    update_query = f"UPDATE users SET health = '{h}' WHERE id = {target.id}"
                    cursor.execute(update_query)
                

                await interaction.response.edit_message(embed = embed, view = None)

                stats_db.commit()
                stats_db.close()

    # Give user skill stones
    async def Update_User_Skillstone(user_id):
        pass

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

    # Update Status Effects
    async def Update_Status(user_id, status, change):
        stats_db = sql.connect("./data/stats_db.db")
        cursor = stats_db.cursor()
        
        update_query = f"UPDATE users SET {status} = '{change}' WHERE id = {user_id}"
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
                    hunt_skill = skills["hunt_skill"]
                    
                    fish_skill_name, fish_skill_description, fish_skill_emoji = await Tools.Create_Skill_Title("fish", fish_skill)
                    work_skill_name, work_skill_description, work_skill_emoji = await Tools.Create_Skill_Title("work", work_skill)
                    hunt_skill_name, hunt_skill_description, hunt_skill_emoji = await Tools.Create_Skill_Title("hunt", hunt_skill)

                    skills_embed = discord.Embed(title = f"{member.name}'s Statistics", description = f"{title}", color = t_color)
                    
                    skills_embed.add_field(name = f"{bot.get_emoji(work_skill_emoji)} {work_skill_name}", value = f"{work_skill_description}", inline = False)
                    skills_embed.add_field(name = f"{bot.get_emoji(fish_skill_emoji)} {fish_skill_name}", value = f"{fish_skill_description} ", inline = False)
                    skills_embed.add_field(name = f"{bot.get_emoji(hunt_skill_emoji)} {hunt_skill_name}", value = f"{hunt_skill_description} ", inline = False)

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
                                option = discord.SelectOption(
                                    label = "Instigator", description = "Do some instigating.", emoji = bot.get_emoji(986078219730059325)
                                )
                                options.append(option)

                            if "golden" in raw_options: # If they are me.
                                option = discord.SelectOption(
                                    label = "Golden", description = "Time to show off how wealthy you are.", emoji = bot.get_emoji(985978615911051314)
                                )
                                options.append(option)

                            if "kami" in raw_options: # If they are kami.
                                option = discord.SelectOption(
                                    label = "Kami", description = "Protector and ruler of the forest.", emoji = bot.get_emoji(993848035253694484)
                                )
                                options.append(option)

                            if "void" in raw_options: # If they are voidpapi.
                                option = discord.SelectOption(
                                    label = "Void Avatar", description = "Avatar of the Void.", emoji = bot.get_emoji(997271210285092974)
                                )
                                options.append(option)

                            if "frostking" in raw_options: # If they are voidpapi.
                                option = discord.SelectOption(
                                    label = "Frost King", description = "Crown made of pure ice.", emoji = bot.get_emoji(997989353060040875)
                                )
                                options.append(option)

                            if "frostlord" in raw_options: # If they are voidpapi.
                                option = discord.SelectOption(
                                    label = "Frost Lord", description = "Represent your status as a Frost Lord.", emoji = bot.get_emoji(998612997285097522)
                                )
                                options.append(option)


                            super().__init__(
                                placeholder="Choose a title to equip.",
                                options = options
                            )


                        async def callback(self, interaction: discord.Interaction):
                            selection = self.values[0]
                            
                            if selection.lower() == "void avatar":
                                selection = "void"
                            if selection.lower() == "frost king":
                                selection = "frostking"
                            if selection.lower() == "frost lord":
                                selection = "frostlord"

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


            @discord.ui.button(
                label="Skills",
                style=discord.ButtonStyle.blurple
            )
            async def skills_button_callback(self, button: discord.Button, interaction: discord.Interaction):
                if member.id == interaction.user.id: # Continue code
                    # TODO Make "my skills" button, "skill shop" button, "buy skills" button, selection for all skills to buy
                    # TODO Make 5 selections for each slot, check user's skill inventory
                    title, t_color = await Database.Fetch_Title(bot, member.id)

                    
                    class Skillshop_Button(discord.ui.Button):
                        def __init__(self):
                            emoji = bot.get_emoji(999112808593641572)
                            super().__init__(
                                label = "Skill Shop",
                                style = discord.ButtonStyle.green,
                                emoji = emoji
                            )
                        async def callback(self, interaction: discord.Interaction):
                            user = interaction.user
                            title, t_color = await Database.Fetch_Title(bot, member.id)
                            if user.id == member.id:
                                page = 1
                                # TODO Create skillshop view with page buttons
                                # TODO Create selections for buying skills with skill stones
                                # TODO Add the ability to buy skills if they don't already own it
                                skillembed = await Tools.Generate_Skill_Shop(bot, ctx, member.id, page)
                                await interaction.response.edit_message(embed = skillembed, view = ProfileView())


                            else:
                                pass



                    skills_embed = discord.Embed(title = f"{member.name}'s Skills", description = f"{title}", color = t_color)
                    await Tools.Generate_Skill_Slots(bot, member.id, skills_embed)
                    skills_embed.set_thumbnail(url = member.avatar.url)
                    skills_embed.set_footer(text= f"{status}", icon_url= ctx.author.avatar.url)


                    view = ProfileView()
                    view.add_item(Skillshop_Button())
                    await interaction.response.edit_message(embed = skills_embed, view = view)

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
        
        fish_amount = config["fish_amount"]
        fish_skill_amount = config["fish_skill_amount"]

        chances = [1,3,1,2,1,3,1,2,1,1,1,2,1,3,1]
        chance = random.choice(chances)

        if chance == 1: # Caught sea bass
            await Database.Update_User_Inventory(user_id, "item5", "add", 1)
            await Database.Update_User_Stats(user_id, "fish_skill", "add", fish_skill_amount)

            embed = discord.Embed(title = f"{user.name} Caught a Fish!", description = f"{title}", color = t_color)
            embed.add_field(name = f"**+ {fish_amount}** {bot.get_emoji(888412218415255582)} Sea Bass", value = f"**+ {fish_skill_amount}** {bot.get_emoji(888402427647254538)} Fishing Skill", inline = False)
            embed.set_thumbnail(url = "https://i.imgur.com/z9llFQr.png")

            return embed

        if chance == 2: # Line Broke
            await Database.Update_User_Stats(user_id, "fish_skill", "subtract", 1)
            
            embed = discord.Embed(title = f"{user.name} Your Line Broke!", description = f"{title}", color = t_color)
            embed.add_field(name = f"Your line broke and you caught nothing.", value = f"**- 1** {bot.get_emoji(888402427647254538)} Fishing Skill", inline = False)

            return embed

        if chance == 3: # Caught mackeral
            await Database.Update_User_Inventory(user_id, "item27", "add", fish_amount)
            await Database.Update_User_Stats(user_id, "fish_skill", "add", fish_skill_amount)

            embed = discord.Embed(title = f"{user.name} Caught a Fish!", description = f"{title}", color = t_color)
            embed.add_field(name = f"**+ {fish_amount}** {bot.get_emoji(888412218415267840)} Mackeral", value = f"**+ {fish_skill_amount}** {bot.get_emoji(888402427647254538)} Fishing Skill", inline = False)
            embed.set_thumbnail(url = "https://i.imgur.com/YCWAbtZ.png")

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
                emoji = "???????"
            )
            async def squirrel_callback(self, button: discord.Button, interaction: discord.Interaction):
                if user_id == interaction.user.id:
                    chance = [1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                    choice = random.choice(chance)
                    
                    if choice == 1: # Normal Squirrel
                        meat_amount = random.randrange(1,5)
                        hunt_amount = config["hunt_amount"]
                        meat = int(meat_amount) * int(hunt_amount)
                        hunt_skill_amount = config["hunt_skill_amount"] * 2
                        
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
                        hunt_skill_amount = config["hunt_skill_amount"] * 4
                        
                        await Database.Update_User_Inventory(user_id, "item6", "add", meat)
                        await Database.Update_User_Stats(user_id, "hunt_skill", "add", hunt_skill_amount)

                        hunt_embed = discord.Embed(title = f"{ctx.author.name} shot a Golden Squirrel!", description = f"{title}", color = t_color)
                        hunt_embed.add_field(name = f"**+ {meat}** {bot.get_emoji(988567158487416910)} Raw Meat", value = f"**+ {hunt_skill_amount}** {bot.get_emoji(819685239306715207)} Hunting Skill", inline = False)
                    
                        await interaction.response.edit_message(embed = hunt_embed, view = None)

            @discord.ui.button(
                label = "Fox",
                style = discord.ButtonStyle.gray,
                emoji = "????"
            )
            async def fox_callback(self, button: discord.Button, interaction: discord.Interaction):
                if user_id == interaction.user.id:
                    meat = random.randrange(2,6)
                    fur = random.randrange(2,5)
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
    async def Setup_Mining(bot, member):
        title, t_color = await Database.Fetch_Title(bot, member.id)
        config = await Configuration.Fetch_Configuration_File()

        embed = discord.Embed(title = f"{member.name} Began Mining", description = f"{title}", color = t_color)
        embed.add_field(name = "Select which ore you want to mine.", value = "Do /craft to smelt your ores into ingots.")
        embed.set_thumbnail(url = member.avatar.url)

        skill_gain = config["work_skill_amount"]

        iron_emoji = bot.get_emoji(998719555591479419)
        copper_emoji = bot.get_emoji(998923967475761222)

        class Mining_View(discord.ui.View):
            
            @discord.ui.button(label = "Iron", style = discord.ButtonStyle.gray, emoji = iron_emoji)
            async def iron_option_callback(self, button: discord.Button, interaction: discord.Interaction):
                
                if member.id == interaction.user.id:
                    
                    amount = random.randrange(6,23)

                    iron_option_embed = discord.Embed(title = f"{member.name} went mining and found {bot.get_emoji(998719555591479419)} Iron Ore!", description=f"{title}", color = t_color)
                    iron_option_embed.set_thumbnail(url = "https://i.imgur.com/liGAqlO.png")
                    iron_option_embed.add_field(name = "Amount Gained:", value = f"**+ {amount}** {bot.get_emoji(998719555591479419)} Iron Ore\n**+ {skill_gain}** {bot.get_emoji(998902721996398594)} Mining Skill")


                    await Database.Update_User_Stats(interaction.user.id, "work_skill", "add", skill_gain)
                    await Database.Update_User_Inventory(interaction.user.id, "item20", "add", amount)

                    await interaction.message.edit(
                        embed = iron_option_embed,
                        view = None
                    )

                else:
                    pass

            @discord.ui.button(label = "Copper", style = discord.ButtonStyle.gray, emoji = copper_emoji)
            async def copper_option_callback(self, button: discord.Button, interaction: discord.Interaction):
                
                if member.id == interaction.user.id:
                    
                    amount = random.randrange(13,26)

                    copper_option_embed = discord.Embed(title = f"{member.name} went mining and found {bot.get_emoji(998923967475761222)} Copper Ore!", description=f"{title}", color = t_color)
                    copper_option_embed.set_thumbnail(url = "https://i.imgur.com/lMMC2A0.png")
                    copper_option_embed.add_field(name = "Amount Gained:", value = f"**+ {amount}** {bot.get_emoji(998923967475761222)} Copper Ore\n**+ {skill_gain}** {bot.get_emoji(998902721996398594)} Mining Skill")


                    await Database.Update_User_Stats(member.id, "work_skill", "add", skill_gain)
                    await Database.Update_User_Inventory(member.id, "item22", "add", amount)

                    await interaction.message.edit(
                        embed = copper_option_embed,
                        view = None
                    )

                else:
                    pass



        view = Mining_View()
        return embed, view

    # Get and Set Shop View
    async def Setup_Shop(bot, member, shop_selection, guild_id):

        if shop_selection == "normal":
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

        if shop_selection == "void":
            title, t_color = await Database.Fetch_Title(bot, member.id)
            items = await Database.Fetch_Itemlist()

            embed = discord.Embed(title = "Void Shop", description=f"{title}", color = t_color)
            void_stone_emoji = items["item14"]["emoji"]
            

            class Shop_View(discord.ui.View):
                pass

            if 1 == 1: # Void Knife

                item_name = items["item15"]["name"]
                item_description = items["item15"]["description"]
                item_emoji = items["item15"]["emoji"]
                item_rarity = items["item15"]["rarity"]
                item_value = items["item15"]["store_value"]

                embed.add_field(name = f"{bot.get_emoji(void_stone_emoji)} **{item_value:,}** - {bot.get_emoji(item_emoji)} {item_name} {bot.get_emoji(item_rarity)}", value = f"{item_description}", inline = False)


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

    # Trading items between users View
    async def Setup_Trade(bot, ctx, user, target, user_item, user_amount, target_item, target_amount):
        title, t_color = await Database.Fetch_Title(bot, user.id)
        items = await Database.Fetch_Itemlist() 

        user_item_key = await Database.Fetch_Item_Key(user_item)
        target_item_key = await Database.Fetch_Item_Key(target_item)


        user_item_amount = await Database.Fetch_Item_Amount(user.id, user_item_key)
        target_item_amount = await Database.Fetch_Item_Amount(target.id, target_item_key)


        if int(user_item_amount) >= int(user_amount): # They have the item and enough of it
            if int(target_item_amount) >= int(target_amount): # The target also has the asked items, continue to trade view.
                trade_embed = discord.Embed(title = f"{user.name} is trading with {target.name}", description = title, color = t_color)
                
                user_item_name = items[user_item_key]["name"]
                user_item_emoji = items[user_item_key]["emoji"]
                user_item_rarity = items[user_item_key]["rarity"]
                
                target_item_name = items[target_item_key]["name"]
                target_item_emoji = items[target_item_key]["emoji"]
                target_item_rarity = items[target_item_key]["rarity"]
                
                trade_embed.add_field(name = f"{user.name}'s Offer:", value = f"{bot.get_emoji(user_item_emoji)} {user_item_name} {bot.get_emoji(user_item_rarity)} - **{user_amount}**\nfor {target.name}'s:\n{bot.get_emoji(target_item_emoji)} {target_item_name} {bot.get_emoji(target_item_rarity)} - **{target_amount}**")
                

                class Trade_View(discord.ui.View):
                    # TODO Add trade details to an embed with buttons

                    @discord.ui.button(label = "Accept", style = discord.ButtonStyle.green)
                    async def accept_callback(self, button: discord.Button, interaction: discord.Interaction):
                        accept_embed = discord.Embed

                        if target.id == interaction.user.id:
                            accept_embed = discord.Embed(title = "Trade Completed!")

                            await Database.Update_User_Inventory(user.id, user_item_key, "subtract", int(user_amount))
                            await Database.Update_User_Inventory(user.id, target_item_key, "add", int(target_amount))

                            await Database.Update_User_Inventory(target.id, target_item_key, "subtract", int(target_amount))
                            await Database.Update_User_Inventory(target.id, user_item_key, "add", int(user_amount))

                            await interaction.response.edit_message(embed = accept_embed, view = None)
                        
                        else:
                            pass

                    @discord.ui.button(label = "Decline", style = discord.ButtonStyle.red)
                    async def decline_callback(self, button: discord.Button, interaction: discord.Interaction):
                        if interaction.user.id == user.id or interaction.user.id == target.id:
                            decline_embed = discord.Embed(title = "Trade Declined!")
                            await interaction.response.edit_message(embed = decline_embed, view = None)
                        else:
                            pass

                    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.grey)
                    async def cancel_callback(self, button: discord.Button, interaction: discord.Interaction):
                        if interaction.user.id == user.id or interaction.user.id == target.id:
                            cancel_embed = discord.Embed(title = "Trade Canceled!")
                            await interaction.response.edit_message(embed = cancel_embed, view = None)
                        else:
                            pass


                view = Trade_View()

                await ctx.respond(embed = trade_embed, view = view)
                await ctx.send(f"{target.mention}, you've received a trade offer!")

            else: # They did not have the item requested, or enough of it.
                await ctx.respond(f"{user.mention}, they do not have enough of that item to trade!")
        else: # They don't have the item or don't have enough of the item
            await ctx.respond(f"{user.mention}, you don't have enough of that item to trade!")

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
        stats = await Database.Fetch_Stats(user_id)

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
                        drop = random.choice([1,1,2,1,4,5,2,1,1,2,1,3,2,1,5,2,7,4,1,2,1,1,1,1,1,4,1,6,1,1,4,1,2,2,2,1,1,4,1,1,2,6,7,6,5,7,7])
                        open_embed = discord.Embed(title = f"{ctx.author.name} opened a Basic Chest!", description = title, color = t_color)

                        if drop == 1: # Milk
                            item_key = "item9"
                            item_amount = random.randrange(3,6)

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {item_amount}** {bot.get_emoji(988842419925708860)} Milk")
                            await Database.Update_User_Inventory(user_id, item_key, "add", item_amount)
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)

                        if drop == 2: # Lime
                            item_key = "item7"
                            item_amount = random.randrange(7,14)

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {item_amount}** {bot.get_emoji(988820202361864252)} Limes")
                            await Database.Update_User_Inventory(user_id, item_key, "add", item_amount)
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)

                        if drop == 3: # Special Golden Bar
                            item_key = "item11"
                            item_amount = 1

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {item_amount}** {bot.get_emoji(985978615911051314)} Special Golden Bar!")
                            await Database.Update_User_Inventory(user_id, item_key, "add", item_amount)
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)

                        if drop == 4: # Iron Ingot
                            item_key = "item21"
                            item_amount = random.randrange(1,4)

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {item_amount}** {bot.get_emoji(998910308624125972)} Iron Ingots!")
                            await Database.Update_User_Inventory(user_id, item_key, "add", item_amount)
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)

                        if drop == 5: # Iron Pickaxe
                            item_key = "item23"
                            item_amount = 1

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {item_amount}** {bot.get_emoji(998902721996398594)} Iron Pickaxe!")
                            await Database.Update_User_Inventory(user_id, item_key, "add", item_amount)
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)

                        if drop == 6: # Iron Pickaxe
                            item_key = "item10"
                            item_amount = random.randrange(1,5)

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {item_amount}** {bot.get_emoji(887651039573082122)} Basic Chests!")
                            await Database.Update_User_Inventory(user_id, item_key, "add", item_amount)
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)

                        if drop == 7: # Mining/Work Skill
                            skill_amount = random.randrange(1,4)

                            await Database.Update_User_Stats(user_id, "work_skill", "add", skill_amount)

                            open_embed.add_field(name = "**You Received:**", value = f"**+ {skill_amount}** {bot.get_emoji(998902721996398594)} Mining Skill!")
                            await Database.Update_User_Inventory(user_id, "item10", "subtract", 1)



                        await interaction.response.edit_message(embed = open_embed, view = None)

                    else:
                        pass

            
            class ViridianCrown_Button(discord.ui.Button):
                def __init__(self):
                    emoji = bot.get_emoji(999793524394430525)
                    super().__init__(
                        label = "Viridian Crown",
                        style = discord.ButtonStyle.gray,
                        emoji = emoji
                    )
                async def callback(self, interaction: discord.Interaction):
                    user = interaction.user
                    title, t_color = await Database.Fetch_Title(bot, user_id)
                    if user.id == user_id:
                        key = "item12"
                        await Database.Update_User_Health(ctx, bot, target, "heal", 1, key, interaction)
                        await Cooldowns.add_cooldown("use_self", user_id)
                    else:
                        pass


            class ForestWisp_Button(discord.ui.Button):
                pass


            class Unfreeze_Button(discord.ui.Button):
                def __init__(self):
                    emoji = bot.get_emoji(636124362579116032)
                    super().__init__(
                        label = "Unfreeze",
                        style = discord.ButtonStyle.gray,
                        emoji = emoji
                    )
                async def callback(self, interaction: discord.Interaction):
                    user = interaction.user
                    title, t_color = await Database.Fetch_Title(bot, user_id)
                    
                    chance = random.choice([1,1,1,1,1,1,2])

                    if user.id == user_id:

                        if chance == 2: # Success
                            success_embed = discord.Embed(title = f"{user.name}, you are unfrozen!")

                            await Database.Update_Status(user_id, "frozen", "false")

                            await interaction.response.edit_message(embed = success_embed, view = None)
                            await Cooldowns.add_cooldown("use_self", user_id)
                        
                        else: # Failure
                            fail_embed = discord.Embed(title = f"{user.name}, you failed to unfreeze yourself. Try again!")

                            await interaction.response.edit_message(embed = fail_embed, view = None)
                            await Cooldowns.add_cooldown("use_self", user_id)

                    else:
                        pass


            class SuspiciousMeal_Button(discord.ui.Button):
                def __init__(self):
                    emoji = bot.get_emoji(998716213674905641)
                    super().__init__(
                        label = "Suspicious Meal",
                        style = discord.ButtonStyle.gray,
                        emoji = emoji
                    )
                async def callback(self, interaction: discord.Interaction):
                    user = interaction.user
                    title, t_color = await Database.Fetch_Title(bot, user_id)
                    if user.id == user_id:
                        key = "item19"
                        use_health, use_description, use_damage = await Tools.Generate_Use_Info(key)
                        
                        embed = discord.Embed(title = f"{target.name} ate a strangely healthy meal...", description = f"You were healed for ?????? {use_health}", color = discord.Color.from_rgb(11,140,33))
                        
                        await interaction.response.edit_message(embed = embed, view = None)
                        
                        await Database.Update_User_Health(user.id, use_health, "heal")
                        await Cooldowns.add_cooldown("use_self", user_id)
                    else:
                        pass




            class Self_Menu(discord.ui.View):
                # TODO Show all usable items, with multiple pages of buttons
                
                pass


            view = Self_Menu()


            if 1 == 1: # Add buttons to view
                if user_id in use_cooldown:
                    
                    embed.add_field(name = "You are on cooldown.", value = "Reminaing time:")

                else:
                    if "item10" in self_usable:
                        basic_amount = await Database.Fetch_Item_Amount(user_id, "item10")
                        view.add_item(BasicChest_Button())
                        embed.add_field(name = f"{bot.get_emoji(887651039573082122)} Basic Chest {bot.get_emoji(880040222367289385)} - **{basic_amount}**", value = "Open this chest for goodies!", inline = False)
                    if "item12" in self_usable and user_id not in use_cooldown:
                        view.add_item(ViridianCrown_Button())
                        embed.add_field(name = f"{bot.get_emoji(999793524394430525)} Viridian Crown {bot.get_emoji(880071881301053490)}", value = "Use the power of the forest to heal others, or summon the forest to aid you in battle!", inline = False)
                    if stats["frozen"] == "true":
                        view.add_item(Unfreeze_Button())
                    if "item19" in self_usable and user_id not in use_cooldown:
                        meal_amount = await Database.Fetch_Item_Amount(user_id, "item19")
                        view.add_item(SuspiciousMeal_Button())
                        embed.add_field(name = f"{bot.get_emoji(998716213674905641)} Suspicious Meal {bot.get_emoji(880040222480543774)} - **{meal_amount}**", value = "Looks...tasty...I guess?", inline = False)

            message = await ctx.respond(embed = embed, view = view)
        
        if user_id != target_id: # Targeted Someone Else

            if stats["frozen"] == "true": # User is frozen
                frozen_embed = discord.Embed(title = f"{ctx.author.name}, you are frozen.", description = "Type /use on yourself to unfreeze!", color = discord.Color.from_rgb(38, 177, 201))
                frozen_embed.set_thumbnail(url = "https://i.imgur.com/XOP5sDN.png")
                await ctx.respond(embed = frozen_embed)
            
            else: # User is not frozen, continue use command.
                
                embed = discord.Embed(title = f"{ctx.author.name}'s usable items**:**", description = title, color = t_color)

                class ForestWisp_Button(discord.ui.Button):
                    
                    def __init__(self):
                        emoji = bot.get_emoji(993847218660446311)
                        super().__init__(
                            label = "Forest Wisp",
                            style = discord.ButtonStyle.gray,
                            emoji = emoji
                        )
                    async def callback(self, interaction: discord.Interaction):
                        user = interaction.user
                        title, t_color = await Database.Fetch_Title(bot, user_id)

                        if user.id == user_id:
                            key = "item13"
                            await Database.Update_User_Health(ctx, bot, target, "damage", 1, key, interaction)
                            await Database.Update_Status(target_id, "toxin", "true")
                            await Database.Update_User_Inventory(user_id, "item13", "subtract", 1)
                            await ctx.send(f"{target.mention}, you've been attacked!")
                
                class Sword_Button(discord.ui.Button):
                    def __init__(self):
                        emoji = bot.get_emoji(994736580793221211)
                        super().__init__(
                            label = "Sword",
                            style = discord.ButtonStyle.gray,
                            emoji = emoji
                        )
                    async def callback(self, interaction: discord.Interaction):
                        user = interaction.user
                        title, t_color = await Database.Fetch_Title(bot, user_id)

                        if user.id == user_id:
                            key = "item4"
                            await Tools.Attack(bot, ctx, user, target, key, interaction)
                            await ctx.send(f"{target.mention}, you've been attacked!")

                class ViridianCrown_Button(discord.ui.Button):
                    def __init__(self):
                        emoji = bot.get_emoji(999793524394430525)
                        super().__init__(
                            label = "Viridian Crown",
                            style = discord.ButtonStyle.gray,
                            emoji = emoji
                        )
                    async def callback(self, interaction: discord.Interaction):
                        user = interaction.user
                        title, t_color = await Database.Fetch_Title(bot, user_id)
                        if user.id == user_id:
                            key = "item12"
                            await Database.Update_User_Health(ctx, bot, target, "heal", 1, key, interaction)
                            await ctx.send(f"{target.mention}, you've been healed!")
                        else:
                            pass

                class VoidKnife_Button(discord.ui.Button):
                    def __init__(self):
                        emoji = bot.get_emoji(997288273993023529)
                        super().__init__(
                            label = "Void Knife",
                            style = discord.ButtonStyle.gray,
                            emoji = emoji
                        )
                    async def callback(self, interaction: discord.Interaction):
                        user = interaction.user
                        title, t_color = await Database.Fetch_Title(bot, user_id)

                        if user.id == user_id:
                            key = "item15"
                            await Database.Update_User_Health(ctx, bot, target, "damage", 1, key, interaction)
                            await ctx.send(f"{target.mention}, you've been attacked!")

                class FrostStaff_Button(discord.ui.Button):
                    def __init__(self):
                        emoji = bot.get_emoji(631047805133127680)
                        super().__init__(
                            label = "Frost Staff",
                            style = discord.ButtonStyle.gray,
                            emoji = emoji
                        )
                    async def callback(self, interaction: discord.Interaction):
                        user = interaction.user
                        title, t_color = await Database.Fetch_Title(bot, user_id)

                        if user.id == user_id:
                            key = "item17"
                            await Database.Update_User_Health(ctx, bot, target, "damage", 1, key, interaction)
                            await ctx.send(f"{target.mention}, you've been attacked!")

                class FrostCrown_Button(discord.ui.Button):
                    def __init__(self):
                        emoji = bot.get_emoji(997989353060040875)
                        super().__init__(
                            label = "Frost Crown",
                            style = discord.ButtonStyle.gray,
                            emoji = emoji
                        )
                    async def callback(self, interaction: discord.Interaction):
                        user = interaction.user
                        title, t_color = await Database.Fetch_Title(bot, user_id)

                        if user.id == user_id:
                            key = "item16"
                            target_circlets = await Database.Fetch_Item_Amount(target.id, "item18")
                            
                            if target_circlets > 0: # They own one, take it away
                                embed = discord.Embed(title = f"{target.name} has lost their Frost Lord blessing.", description = f"{bot.get_emoji(998612997285097522)} Frost Circlet **- 1**", color = discord.Color.from_rgb(10,209,240))

                                await Database.Update_User_Inventory(target.id, "item18", "subtract", 1)
                                await interaction.response.edit_message(embed = embed, view = None)
                            
                            else: # Give them a circlet
                                embed = discord.Embed(title = f"{target.name} has been given the power of a Frost Lord", description = f"{bot.get_emoji(998612997285097522)} Frost Circlet **+ 1**", color = discord.Color.from_rgb(10,209,240))

                                await Database.Update_User_Inventory(target.id, "item18", "add", 1)
                                await interaction.response.edit_message(embed = embed, view = None)

                class ViridianWarrior_Button(discord.ui.Button):
                    def __init__(self):
                        emoji = bot.get_emoji(999793526554501283)
                        super().__init__(
                            label = "Viridian Warrior",
                            style = discord.ButtonStyle.gray,
                            emoji = emoji
                        )
                    async def callback(self, interaction: discord.Interaction):
                        user = interaction.user
                        title, t_color = await Database.Fetch_Title(bot, user_id)
                        if user.id == user_id:
                            key = "item28"
                            await Database.Update_User_Health(ctx, bot, target, "damage", 1, key, interaction)
                            await ctx.send(f"{target.mention}, you've been attacked!")
                        else:
                            pass




                class Target_Menu(discord.ui.View):
                    # TODO Show items that can target the user
                    # Add an embed field for every usable item and the amount
                    pass
                

                view = Target_Menu()

                if user_id in use_target_cooldown:
                    pass
                
                else:
                    if "item4" in target_usable: # Sword
                        view.add_item(Sword_Button())   
                
                    if "item12" in target_usable: # Viridian Crown
                        view.add_item(ViridianCrown_Button())
                
                    if "item13" in target_usable: # Forest Wisp
                        view.add_item(ForestWisp_Button())
                
                    if "item15" in target_usable: # Forest Wisp
                        view.add_item(VoidKnife_Button())

                    if "item16" in target_usable: # Frost Crown
                        view.add_item(FrostCrown_Button())

                    if "item17" in target_usable: # Frost Staff
                        view.add_item(FrostStaff_Button())

                    if "item28" in target_usable: # Viridian Warrior
                        view.add_item(ViridianWarrior_Button())

                message = await ctx.respond(embed = embed, view = view)
                await Cooldowns.add_cooldown("use_target", user_id)

    # Adventure View
    async def Setup_Adventure(bot, ctx):
        title, t_color = await Database.Fetch_Title(bot, ctx.author.id)
        status = await Tools.Generate_Status(ctx.author.id)

        viridian_emoji = bot.get_emoji(994736483644747918)

        adventure_embed = discord.Embed(title = f"{ctx.author.name} began Adventuring!", description = title, color = t_color)
        adventure_embed.add_field(name = f"{viridian_emoji} The Viridian", value = "The Viridian is home to boundless mystical creatures and ancient spirits. The forest of a thousand paths.")
        adventure_embed.set_image(url = "https://i.imgur.com/Lr8C4RO.jpg")
        adventure_embed.set_footer(text= f"{status}", icon_url= ctx.author.avatar.url)
        

        class Adventure_Menu(discord.ui.View):
            
            @discord.ui.button(label = "The Viridian", style = discord.ButtonStyle.grey, emoji = viridian_emoji)
            async def viridian_callback(self, button: discord.Button, interaction: discord.Interaction):
                if interaction.user.id == ctx.author.id:
                    await Viridian.Setup_Viridian(ctx, bot, interaction)
                else:
                    pass

            

        Adventure_View = Adventure_Menu()
        await ctx.respond(embed = adventure_embed, view = Adventure_View)

    # Crafting View
    async def Setup_Craft(bot, ctx):
        craftable_items = []
        
        title, t_color = await Database.Fetch_Title(bot, ctx.author.id)
        items = await Database.Fetch_Itemlist()

        menu_embed = discord.Embed(title = f"Crafting Menu", description= title, color = t_color)
        menu_embed.set_image(url = "https://i.imgur.com/S0sVSbK.png")
        menu_embed.set_footer(text = "Select a category to begin crafting!")

        i = 1
        while i < 200: # Checking and adding all the craftable items
            try:
                key = "item"+f"{i}"
                recipe = list(items[key]["recipe"])
                if len(recipe) > 0:
                    craftable_items.append(key)
            except:
                pass

            i+=1


        class Smelt_Selection(discord.ui.Select):
            
            def __init__(self):
                options = [
                    discord.SelectOption(label = "Iron Ingot", description = "Craft 10x Iront Ingots.", emoji = bot.get_emoji(998910308624125972)),
                    discord.SelectOption(label = "Copper Ingot", description = "Craft 10x Copper Ingots.", emoji = bot.get_emoji(998924031258546296))
                ]

                super().__init__(
                    placeholder="Choose which item to craft.",
                    options = options
                )

            async def callback(self, interaction: discord.Interaction):
                selection = self.values[0]
                if interaction.user.id == ctx.author.id:
                    
                    if selection.lower() == "iron ingot":
                        key = "item21"
                        ore_key = "item20"
                        craft_amount = 10

                        iron_ore_amount = await Database.Fetch_Item_Amount(ctx.author.id, ore_key)
                        recipe = list(items[key]["recipe"])

                        checks = []

                        amount_required = items[key]["recipe"][ore_key] * 10
                        if iron_ore_amount >= amount_required:
                            checks.append("complete")
                        else:
                            checks.append("fail")
                            

                        if "fail" in checks: # Something went wrong with the craft
                            fail_embed = discord.Embed(title = f"{ctx.author.name} failed to craft. Make sure you have enough ingredients!", description=title, color = t_color)
                            
                            await interaction.response.edit_message(embed = fail_embed, view = None)

                        
                        else: # Continue craft
                            craft_embed = discord.Embed(title = f"{ctx.author.name} Crafted Iron", description=title, color = t_color)
                            craft_embed.add_field(name = "Craft Amount:", value = f"**+ 10** {bot.get_emoji(998910308624125972)} Iron Ingots")
                            craft_embed.set_thumbnail(url = "https://i.imgur.com/RKcUo9h.png")


                            for k,v in items[key]["recipe"].items():
                                lose_amount = v * 10
                                await Database.Update_User_Inventory(ctx.author.id, k, "subtract", lose_amount)


                            await Database.Update_User_Inventory(ctx.author.id, key, "add", craft_amount)
                            await interaction.response.edit_message(embed = craft_embed, view = None)

                    if selection.lower() == "copper ingot":
                        key = "item23"
                        ore_key = "item22"
                        craft_amount = 10

                        ore_amount = await Database.Fetch_Item_Amount(ctx.author.id, ore_key)
                        recipe = list(items[key]["recipe"])

                        checks = []

                        amount_required = items[key]["recipe"][ore_key] * 10
                        if ore_amount >= amount_required:
                            checks.append("complete")
                        else:
                            checks.append("fail")
                            

                        if "fail" in checks: # Something went wrong with the craft
                            fail_embed = discord.Embed(title = f"{ctx.author.name} failed to craft. Make sure you have enough ingredients!", description=title, color = t_color)
                            
                            
                            await interaction.response.edit_message(embed = fail_embed, view = None)

                        else: # Continue craft
                            craft_embed = discord.Embed(title = f"{ctx.author.name} Crafted Copper", description=title, color = t_color)
                            craft_embed.add_field(name = "Craft Amount:", value = f"**+ 10** {bot.get_emoji(998924031258546296)} Copper Ingots")
                            craft_embed.set_thumbnail(url = "https://i.imgur.com/tNF62fH.png")


                            for k,v in items[key]["recipe"].items():
                                lose_amount = v * 10
                                await Database.Update_User_Inventory(ctx.author.id, k, "subtract", lose_amount)


                            await Database.Update_User_Inventory(ctx.author.id, key, "add", craft_amount)
                            await interaction.response.edit_message(embed = craft_embed, view = None)

        class Cook_Selection(discord.ui.Select):
            
            def __init__(self):
                ingredient_1_amount = items["item19"]["recipe"]["item2"]
                ingredient_2_amount = items["item19"]["recipe"]["item3"]
                options = [
                    discord.SelectOption(label = "Suspicious Meal", description = f"{ingredient_1_amount}x Eggplants | {ingredient_2_amount}x Bananas", emoji = bot.get_emoji(998716213674905641))
                ]

                super().__init__(
                    placeholder="Choose which item to craft.",
                    options = options
                )

            async def callback(self, interaction: discord.Interaction):
                selection = self.values[0]
                if interaction.user.id == ctx.author.id:
                    
                    if selection.lower() == "suspicious meal":
                        key = "item19"
                        eggplant_key = "item2"
                        banana_key = "item3"
                        
                        craft_amount = 1

                        eggplant_amount = await Database.Fetch_Item_Amount(ctx.author.id, eggplant_key)
                        banana_amount = await Database.Fetch_Item_Amount(ctx.author.id, banana_key)
                        
                        recipe = list(items[key]["recipe"])

                        checks = []

                        eggplant_required = items[key]["recipe"][eggplant_key] * craft_amount
                        if eggplant_amount >= eggplant_required:
                            checks.append("complete")
                        else:
                            checks.append("fail")
                            
                        banana_required = items[key]["recipe"][banana_key] * craft_amount
                        if banana_amount >= banana_required:
                            checks.append("complete")
                        else:
                            checks.append("fail")


                        if "fail" in checks: # Something went wrong with the craft
                            fail_embed = discord.Embed(title = f"{ctx.author.name} failed to craft. Make sure you have enough ingredients!", description=title, color = t_color)
                            
                            await interaction.response.edit_message(embed = fail_embed, view = None)

                        else: # Continue craft
                            craft_embed = discord.Embed(title = f"{ctx.author.name} Crafted Suspicious Meal", description=title, color = t_color)
                            craft_embed.add_field(name = "Craft Amount:", value = f"**+ {craft_amount}** {bot.get_emoji(998716213674905641)} Suspicious Meals")
                            craft_embed.set_thumbnail(url = "https://i.imgur.com/6Ife7q0.png")


                            for k,v in items[key]["recipe"].items():
                                lose_amount = v * craft_amount
                                await Database.Update_User_Inventory(ctx.author.id, k, "subtract", lose_amount)


                            await Database.Update_User_Inventory(ctx.author.id, key, "add", craft_amount)
                            await interaction.response.edit_message(embed = craft_embed, view = None)


        class Craft_Menu(discord.ui.View): # Selection menu for choosing a crafting category
            
            smelt_emoji = bot.get_emoji(999808639558750248)
            cooking_emoji = bot.get_emoji(999809845597327450)

            @discord.ui.button(
                label="Smelting",
                style=discord.ButtonStyle.blurple,
                emoji = smelt_emoji
            )
            async def smelting_button_callback(self, button: discord.Button, interaction: discord.Interaction):
                if ctx.author.id == interaction.user.id:
                    title, t_color = await Database.Fetch_Title(bot, ctx.author.id)
                    
                    smelt_embed = discord.Embed(title = f"Smelting Menu", description = f"{title}", color = t_color)

                    smelt_embed.add_field(name = f"**10x** {bot.get_emoji(998910308624125972)} Iron Ingots", value = f"Perfectly smelted iron molded into the shape of a bar.")
                    smelt_embed.add_field(name = f"**10x** {bot.get_emoji(998924031258546296)} Copper Ingots", value = f"Copper ore smelted into an ingot of pure metal.")
                    smelt_embed.set_thumbnail(url = "https://i.imgur.com/7LykRWg.png")


                    view = Craft_Menu()
                    view.add_item(Smelt_Selection())
                    await interaction.response.edit_message(embed = smelt_embed, view = view)

            @discord.ui.button(
                label="Cooking",
                style=discord.ButtonStyle.blurple,
                emoji = cooking_emoji
            )
            async def cooking_button_callback(self, button: discord.Button, interaction: discord.Interaction):
                if ctx.author.id == interaction.user.id:
                    title, t_color = await Database.Fetch_Title(bot, ctx.author.id)
                    
                    cook_embed = discord.Embed(title = f"Cooking Menu", description = f"{title}", color = t_color)

                    cook_embed.add_field(name = f"**1** {bot.get_emoji(998716213674905641)} Suspicious Meal", value = f"Did you mean to make this...?")
                    cook_embed.set_thumbnail(url = "https://i.imgur.com/ITLn6y7.png")


                    view = Craft_Menu()
                    view.add_item(Cook_Selection())
                    await interaction.response.edit_message(embed = cook_embed, view = view)



        await ctx.respond(embed = menu_embed, view = Craft_Menu())




class Cooldowns():

    # Adds cooldowns to the cooldown container
    async def add_cooldown(cooldown, user_id):
        config = await Configuration.Fetch_Configuration_File()
        
        if cooldown == "work":
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

        if cooldown == "use_target":
            use_target_cooldown.append(user_id)
            await asyncio.sleep(config["use_target_cooldown"])
            use_target_cooldown.remove(user_id)

        if cooldown == "use_self":
            use_cooldown.append(user_id)
            await asyncio.sleep(config["use_cooldown"])
            use_cooldown.remove(user_id)

    # Retrieve cooldowns
    async def get_cooldowns(cooldown):
        if cooldown == "work":
            return work_cooldowns
        if cooldown == "fish":
            return fish_cooldowns
        if cooldown == "hunt":
            return hunt_cooldowns




class Tools():
    # Creating the emojis and health for status
    async def Generate_Status(user_id):
        stats = await Database.Fetch_Stats(user_id)
        health = stats["health"]
        # Go through stats and generate status effects
        needed_emojis = []
        status = " "

        if stats["toxin"] == "true":
            needed_emojis.append("????")

        if stats["frozen"] == "true":
            needed_emojis.append("??????")

        if len(needed_emojis) > 0:
            status_emojis = [" | "] + needed_emojis
            
            emojis = " ".join(str(x) for x in status_emojis)
            
            status = f"?????? {health}{emojis}"
        
        else:
            status = f"?????? {health}"
        
        return status

    # Creating stats title
    async def Create_Skill_Title(skill_name, skill_amount):
        if skill_name == "fish":
            skill_emoji = 888402427647254538
            skill_name = "Small Fry"
            skill_description = f"**Skill: ({skill_amount})**"
                
            return skill_name, skill_description, skill_emoji
        
        if skill_name == "work":
            if int(skill_amount) >= 0:
                skill_emoji = 998902721996398594
                skill_name = "Mining Newb"
                skill_description = f"**Skill: ({skill_amount})**"
                
                return skill_name, skill_description, skill_emoji

        if skill_name == "hunt":
            if int(skill_amount) >= 0:
                skill_emoji = 819685239306715207
                skill_name = "Bad Shot"
                skill_description = f"**Skill: ({skill_amount})**"
                
                return skill_name, skill_description, skill_emoji

    # Creating skill slots for profile
    async def Generate_Skill_Slots(bot, user_id, embed):
        skills_list = await Database.Fetch_Skills()

        skills_db = sql.connect("./data/skills_db.db")
        cursor = skills_db.cursor()

        get_query = f"SELECT slot1,slot2,slot3,slot4,slot5 FROM users WHERE id = {user_id}"
        cursor.execute(get_query)
        result = list(cursor.fetchall()[0])


        i = 0
        while i < 5:
            slot = result[i]

            if slot == "none": # If nothing is equipped
                embed.add_field(name = f"**Empty Slot**", value = f"Equip a skill to active unique effects and abilities.", inline = False)
            
            if slot == "quickstep": # Quickstep is equipped
                key = "skill1"
                skill_name = skills_list[key]["name"]
                skill_description = skills_list[key]["description"]
                skill_emoji = skills_list[key]["emoji"]
                embed.add_field(name = f"{bot.get_emoji(skill_emoji)} **{skill_name}**", value = skill_description, inline = False)

            i+=1

    # Generating the skill shop
    async def Generate_Skill_Shop(bot, ctx, user_id, page):
        embed = discord.Embed(title = "Skill Shop")
        user_skills = await Database.Fetch_User_Skills(user_id)
        skill_list = await Database.Fetch_Skills()

        if page == 1:
            stone_emoji = bot.get_emoji(999112808593641572)
            
            if 1 == 1: # Quickstep
                skill = "skill1"
                skill_name = skill_list[skill]["name"]
                skill_description = skill_list[skill]["description"]
                skill_emoji = skill_list[skill]["emoji"]
                skill_cost = str(skill_list[skill]["cost"]) + " - "
                
                if skill in user_skills: # Check if they have the skill unlocked
                    stone_emoji = bot.get_emoji(999452497070542848)
                    skill_cost = " "
                embed.add_field(name = f"{stone_emoji} {skill_cost} {bot.get_emoji(skill_emoji)} **{skill_name}**", value = f"{skill_description}")
        
        return embed

    # Generating item use information
    async def Generate_Use_Info(key):
        items = await Database.Fetch_Itemlist()
        use_health = items[key]["use_health"]
        use_description = items[key]["use_description"]
        use_damage = items[key]["use_damage"]
        
        return use_health, use_description, use_damage

    # Handle one user attacking another user (the item can also have positive effects)
    async def Attack(bot, ctx, user, target, item_key, interaction):
        
        # Grabbing important skill information about each user
        user_skills_equipped = await Database.Fetch_User_Equipped_Skills(user.id)
        target_skills_equipped = await Database.Fetch_User_Equipped_Skills(target.id)

        # Checking for immunity
        frozen_immunity = await Tools.Check_Stats_Immunity(target.id, "frozen")

        # Check for current status affecting the player. i.e. Frozen, Toxin, Etc..
        user_status = await Database.Fetch_Stats(user.id) # This is a dictionary

        # Generating important information about the item used
        use_health, use_description, use_damage = await Tools.Generate_Use_Info(item_key)

        # Pre-creating data to be used for calculation later on
        crit_chance = random.choice([1,1,1,1,1,1,1,1,2])
        severity = 1


        # TODO User should be damaged for 5 hp if under toxin affect


        # Handle skill effects BEFORE damage calculation
        if 1 == 1:

            # Quickstep
            if "skill1" in target_skills_equipped:
                quickstep_embed = discord.Embed(title = "Quickstep! Maven was fast enough to dodge the attack!", color = discord.Color.from_rgb(237, 121, 38))
                quickstep_embed.set_thumbnail(url = "https://i.imgur.com/e1Hkmo4.jpg")
                dodge_chance = random.choice([2])
                if dodge_chance == 2:
                    await interaction.response.edit_message(embed = quickstep_embed, view = None)
                    return


        # Handle damage bonuses based on skills or other factors such as crit damage.
        if 1 == 1:

            # Determine critical chance based on items or skill
            if 1 == 1:
                pass
            

            # Determine damage based on skills
            if 1 == 1:
                pass


            # Apply critical damage
            if crit_chance == 2:
                use_damage = use_damage * 1.5


        # Handle Damage Calculation based on the item
        if 1 == 1:

            # Sword
            if item_key == "item4":
                embed = discord.Embed(title = f"{target.name} was sliced by a Sword!", description = f"**- {use_damage}** ??????")
                await interaction.response.edit_message(embed = embed, view = None)

            # Viridian Crown
            if item_key == "item12":
                tome_embed = discord.Embed(title = f"{target.name} was healed by the Viridian Emperor.", description = f"You were healed for ?????? {use_health}", color = discord.Color.from_rgb(11,140,33))

                if target.id == 470650378271326208:
                    wisp_chance = random.choice([1,1,1,2])
                    if wisp_chance == 2:
                        tome_embed.add_field(name = f"A Forest Wisp comes to your aid!", value = f"**+1** {bot.get_emoji(993847218660446311)} Forest Wisp")
                        await Database.Update_User_Inventory(target.id, "item13", "add", 1)
            
                    warrior_chance = random.choice([1,1,1,1,1,2])
                    if warrior_chance == 2:
                        tome_embed.add_field(name = f"A Viridian Warrior comes to your aid!", value = f"**+1** {bot.get_emoji(999793526554501283)} Viridian Warrior")
                        await Database.Update_User_Inventory(target.id, "item28", "add", 1)

                await interaction.response.edit_message(embed = tome_embed, view = None)

            # Forest Wisp
            if item_key == "item13":
                embed = discord.Embed(title = f"{target.name} was attacked by a Forest Wisp!", description = f"**- {use_damage}** ??????")
                
                await interaction.response.edit_message(embed = embed, view = None)






        # Checking and setting current user health after attack
        await Database.Update_User_Health(target.id, -use_damage)
        await Database.Update_User_Health(target.id, use_health)

        user_health = await Database.Fetch_User_Health(user.id)
        target_health = await Database.Fetch_User_Health(target.id)

        if user_health < 0: # They died
            await Tools.Apply_Death(ctx, bot, user.id, severity)
        
        if target_health < 0: # They died
            await Tools.Apply_Death(ctx, bot, target.id, severity)


    # Calculate damage and reduce currency
    async def Apply_Death(ctx, bot, user, severity):
        message = " "
        raw_user = bot.get_user(user)
        reset_health = 100

        if severity == 1:
            severity_cost = random.randrange(1000, 3000)
            message = f"{raw_user.mention} You were forced to pay god **{severity_cost}** {bot.get_emoji(985978616741511208)} Silver, to bring you back to life."

            await Database.Update_Balance(user, "wallet", -severity_cost)
        

        if 1 == 1: # Reset Health
            stats_db = sql.connect("./data/stats_db.db")
            cursor = stats_db.cursor()
            update_query = f"UPDATE users SET health = '{reset_health}' WHERE id = {user.id}"
            cursor.execute(update_query)

            stats_db.commit()
            stats_db.close()

        await ctx.send(message)


    # Unique function for friend's server:
    async def Give_Voidstone(bot, ctx):
        if ctx.author.id == 816471695975776276: # If the user is maven bot.
            pass
        
        else:
            user_id = ctx.author.id
            random_chance = random.choice([1,1,1,1,1,1,1,1,1,1,1,1,1,2])

            if random_chance == 2:
                void_channel = bot.get_channel(997278795860029470)

                await void_channel.send(f"{ctx.author.name} found a {bot.get_emoji(997267877818286171)} Void Stone!")

                await Database.Update_User_Inventory(user_id, "item14", "add", 1)

            else:
                pass


    # Getting all the user's items and checking for status immunity
    async def Check_Stats_Immunity(user_id, status):
        immunity = "freeze"

        frost_crown = await Database.Fetch_Item_Amount(user_id, "item16")
        if frost_crown > 0:
            immunity = "immune"
        

        frost_circlet = await Database.Fetch_Item_Amount(user_id, "item18")
        if frost_circlet > 0:
            immunity = "immune"



        return immunity


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




class Viridian(): # Viridian adventure location
    
    async def Setup_Viridian(ctx, bot, interaction):
        
        pass
