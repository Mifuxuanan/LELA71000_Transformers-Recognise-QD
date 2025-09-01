import string

n_data = 3000 

var_set = set(string.ascii_lowercase)
pre_set = set(string.ascii_uppercase)

var_NL = ["x", "y"]
pre_NL = ["P", "Q", "R", "S"]

pre_ls = list(string.ascii_uppercase)
half = len(pre_ls) // 2
set1 = set(pre_ls[:half])
set2 = set(pre_ls[half:])

# 128
person = {
    'Accountants', 'Actors', 'Actuaries', 'Adults', 'Advisors', 'Agents', 'Allergists', 'Analysts',
    'Anthropologists', 'Archaeologists', 'Artists', 'Astronomers', 'Athletes', 'Attackers', 'Audiologists', 'Auditors',
    'Babies', 'Bailiffs', 'Bakers', 'Ballerinas', 'Barbers', 'Bartenders', 'Bloggers', 'Boxers',
    'Breadwinners', 'Butchers', 'Butlers', 'Captains', 'Cartographers', 'Cashiers', 'Chiropractors', 'Cleaners',
    'Clerks', 'Conductors', 'Cooks', 'Cricketers', 'Crooks', 'Cyclists', 'Cynics', 'Dancers',
    'Defenders', 'Dentists', 'Directors', 'Drillers', 'Drivers', 'Economists', 'Electricians', 'Engineers',
    'Epidemiologists', 'Experts', 'Farmers', 'Fighters', 'Firemen', 'Fishermen', 'Footballers', 'Foresters',
    'Ghosts', 'Grandmasters', 'Guests', 'Gymnasts', 'Hairdressers', 'Helpers', 'Historians', 'Hosts',
    'Jewelers', 'Judges', 'Jurors', 'Kings', 'Knights', 'Lawyers', 'Lecturers', 'Librarians',
    'Machinists', 'Masters', 'Mathematicians', 'Mechanics', 'Monologists', 'Musicians', 'Opticians', 'Painters',
    'Parents', 'Patients', 'Pavers', 'Philosophers', 'Photographers', 'Physicians', 'Physicists', 'Pilots',
    'Players', 'Playmakers', 'Plumbers', 'Poets', 'Policemen', 'Princes', 'Princesses', 'Principals',
    'Prisoners', 'Professors', 'Psychologists', 'Publishers', 'Quants', 'Queens', 'Researchers', 'Roofers',
    'Sailors', 'Scholars', 'Scientists', 'Scorers', 'Scribes', 'Secretaries', 'Settlers', 'Sheriffs',
    'Soldiers', 'Strategists', 'Students', 'Surgeons', 'Surveyors', 'Teachers', 'Technicians', 'Therapists',
    'Tourists', 'Traders', 'Veterinarians', 'Violinists', 'Visitors', 'Waiters', 'Warlords', 'Witches'
    }

# 88
thing = {
    "Apples", "Amulets", "Arrows", "Axes", "Backpacks", "Batteries", "Belts", "Bells", "Boots",
    "Bolts", "Books", "Boxes", "Bowls", "Bows", "Bracelets", "Bracers", "Brooches", "Buckets",
    "Candles", "Chalices", "Chests", "Cogs", "Coins", "Compasses", "Crates", "Crossbows",
    "Crowbars", "Cups", "Daggers", "Drums", "FishingRods", "Flasks", "Flutes", "Gauntlets",
    "Gems", "Glasses", "Gloves", "Greaves", "Hammers", "Hats", "Helmets", "Horns",
    "Jars", "Keys", "Lanterns", "Lockets", "Maps", "Masks", "Mirrors", "Nets",
    "Necklaces", "Notebooks", "OilFlasks", "Orbs", "Paintings", "Pauldrons", "Plates", "Pliers",
    "Pears", "Pipes", "Pouches", "Potions", "Quills", "Ropes", "Runes", "Sashes", "Satchels",
    "ScrollCases", "Scrolls", "Saws", "Screwdrivers", "Shields", "Shovels", "Spears", "Staffs",
    "Statues", "SwordSheaths", "Swords", "Tablets", "Talismans", "Tongs", "Torches", "Trinkets",
    "Trunks", "Vases", "Vials", "Wands", "Wrenches"
}

# 98
un_pre = {
    'Active', 'Alert', 'Ambitious', 'Artistic', 'Bored', 'Brave', 'Busy', 'Calm',
    'Careless', 'Cautious', 'Charming', 'Cheerful', 'Clever', 'Clumsy', 'Cold',
    'Confident', 'Creative', 'Critical', 'Curious', 'Demanding', 'Determined',
    'Diligent', 'Disorganized', 'Distracted', 'Efficient', 'Elegant', 'Energetic',
    'Experienced', 'Fair', 'Fearless', 'Focused', 'Friendly', 'Funny', 'Generous',
    'Graceful', 'Hardworking', 'Helpful', 'Honest', 'Humble', 'Idealistic',
    'Impatient', 'Junior', 'Kind', 'Late', 'Lazy', 'Loyal', 'Messy', 'Modest',
    'Motivated', 'Naive', 'Nervous', 'Neutral', 'New', 'Old', 'Open', 'Organized',
    'Passionate', 'Patient', 'Picky', 'Polite', 'Pragmatic', 'Proud', 'Punctual',
    'Quiet', 'Realistic', 'Rebellious', 'Relaxed', 'Reliable', 'Reserved', 'Rude',
    'Selfish', 'Senior', 'Serious', 'Short', 'Shy', 'Silent', 'Skilled', 'Slow',
    'Smart', 'Social', 'Strict', 'Strong', 'Stubborn', 'Stylish', 'Talented',
    'Talkative', 'Tall', 'Thoughtful', 'Tired', 'Unfair', 'Unreliable',
    'Unsocial', 'Visionary', 'Warm', 'Weak', 'Wise', 'Witty', 'Young'
    }

# 88
bin_pre = {
    'Accompany', 'Accuse', 'Admire', 'Advise', 'Align', 'Approach', 'Argue', 'Assist',
    'Betray', 'Blame', 'Brief', 'Challenge', 'Collaborate', 'Comment', 'Compare', 'Compete',
    'Compliment', 'Confront', 'Consult', 'Contact', 'Convince', 'Criticize', 'Deceive', 'Demand',
    'Discipline', 'Discuss', 'Dismiss', 'Doubt', 'Employ', 'Engage', 'Envy', 'Evaluate',
    'Fire', 'Follow', 'Fund', 'Greet', 'Guide', 'Hate', 'Help', 'Ignore',
    'Inform', 'Instruct', 'Insult', 'Interrupt', 'Invite', 'Involve', 'Judge', 'Know',
    'Lecture', 'Like', 'Listen', 'Manage', 'Mentor', 'Monitor', 'Motivate', 'Negotiate',
    'Notify', 'Observe', 'Oppose', 'Pay', 'Persuade', 'Praise', 'Prefer', 'Protect',
    'Provoke', 'Punish', 'Question', 'Refer', 'Reject', 'Remind', 'Replace', 'Report',
    'Request', 'Respect', 'Reward', 'Schedule', 'Scold', 'Shadow', 'Sponsor', 'Supervise',
    'Support', 'Teach', 'Train', 'Trust', 'Undermine', 'Love', 'Value', 'Warn'
    }

# 35
tern_pre = {
    'Allocate', 'Assign', 'Award', 'Bring', 'Contribute',
    'Convey', 'Consign', 'Delegate', 'Deliver', 'Dispatch', 'Distribute', 'Donate',
    'Entrust', 'Explain', 'Forward', 'Furnish', 'Give', 'Grant', 'Hand', 'Introduce',
    'Lend', 'Loan', 'Offer', 'Pass', 'Pay', 'Post', 'Present', 'Provide', 'Recommend',
    'Sell', 'Send', 'Share', 'Show', 'Supply','Transfer'
    }


    