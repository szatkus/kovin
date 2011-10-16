#coding=utf-8
'''RPG database'''
import extsea
import random

def random_range(a, b):
	if (a == b):
		return a
	return random.randint(a, b)

def ai_dumb(char, battle):
	'''The simplest fight controller'''
	attack = []
	for name in char.attrib:
		if char.attrib[name].atype == 'attack':
			attack.append(char.attrib[name])
	if len(attack) > 0:
		target = char
		limit = 100
		while (target == char) and (limit > 0):
			target = battle.char[random_range(1, len(battle.char))-1]
			if target.team == char.team:
				target = char
			limit -= 1
		if target != char:
			i = random_range(1, len(attack))-1
			attack[i].use(char, target)

def ai_custom(char, battle):
	'''The simplest fight controller'''
	attacks = []
	for name in char.attrib:
		if char.attrib[name].atype == 'attack':
			attacks.append(char.attrib[name])
	if len(attacks) > 0:
		target = char
		limit = 100
		while (target == char) and (limit > 0):
			target = battle.char[random_range(1, len(battle.char))-1]
			if target.team == char.team:
				target = char
			limit -= 1
		attack = attacks[random_range(1, len(attacks))-1]
		if target == char:
			target = None
		#It's like dumb now
		for a in attacks:
			if ('ai_hit' in char.attrib) and (a.name == 'hit'):
				attack = a
		if 'ai_stay' in char.attrib:
			target = None
		
		if (target != None) and (attack in attacks):
			attack.use(char, target)

def create(name):
	'''Create new attribute.
	
	Example:
	strength = rpgdb.create('strength')
	
	Available attributes:
	strength
	life
	speed
	human
	wolf
	mushroom
	male
	female
	bite
	hit
	'''
	result = extsea.Attribute(name)
	#Strength
	if name == 'strength':
		strength = extsea.Attribute('strength')
		def strength_mod(self, mod):
			mod.tbonus *= self.level
		strength.mod = strength_mod
		strength.multi = 6
		strength.max_level = 8
		strength.atype = 'ability'
		strength.title = 'Siła'
		return(strength)
	
	#Life
	if name == 'life':
		life = extsea.Attribute('life')
		life.multi = 2
		life.max_level = 20
		life.atype = 'ability'
		life.title = 'Witalność'
		return(life)
	
	#Speed
	if name == 'speed':
		speed = extsea.Attribute('speed')
		speed.max_level = 13
		speed.multi = 3
		speed.atype = 'ability'
		speed.title = 'Szybkość'
		return(speed)
	
	#Magic
	if name == 'magic':
		magic = extsea.Attribute('magic')
		magic.atype = 'ability'
		magic.multi = 7
		magic.max_level = 7
		magic.title = 'Magia'
		return(magic)
	
	#Sword
	if name == 'sword':
		sword = extsea.Attribute('sword')
		sword.multi *= 4
		sword.max_level = 10
		sword.dep = ['strength']
		sword.atype = 'skill'
		return(sword)
	
	#Human
	if name == 'human':
		human = extsea.Attribute('human')
		human.affect = ['strength', 'speed', 'life']
		human.max_level = 1
		def human_mod(self, mod):
			if mod.name == 'life':
				mod.tbonus *= 10
			if mod.name == 'strength':
				mod.tbonus *= 4
			if mod.name == 'speed':
				mod.tbonus *= 5
			if mod.name == 'magic':
				mod.tbonus *= 7
		human.mod = human_mod
		human.atype = 'race'
		human.title = 'Człowiek'
		return(human)
	
	#Wolf
	if name == 'wolf':
		wolf = extsea.Attribute('wolf')
		wolf.affect = ['strength', 'speed', 'life']
		wolf.max_level = 1
		def wolf_mod(self, mod):
			if mod.name == 'life':
				mod.tbonus *= 8
			if mod.name == 'strength':
				mod.tbonus *= 5
			if mod.name == 'speed':
				mod.tbonus *= 7
		wolf.mod = wolf_mod
		wolf.atype = 'race'
		return(wolf)
	
	#Mushroom
	if name == 'mushroom':
		mushroom = extsea.Attribute('mushroom')
		mushroom.affect = ['strength', 'speed', 'life']
		mushroom.max_level = 1
		def mushroom_mod(self, mod):
			if mod.name == 'life':
				mod.tbonus *= 5
			if mod.name == 'strength':
				mod.tbonus *= 2
			if mod.name == 'speed':
				mod.tbonus *= 2
		mushroom.mod = mushroom_mod
		mushroom.atype = 'race'
		return(mushroom)
	
	#Bat
	if name == 'bat':
		result = extsea.Attribute('bat')
		result.affect = ['strength', 'speed', 'life']
		result.max_level = 1
		def mod(self, mod):
			if mod.name == 'life':
				mod.tbonus *= 3
			if mod.name == 'strength':
				mod.tbonus *= 2
			if mod.name == 'speed':
				mod.tbonus *= 8
		result.mod = mod
		result.atype = 'race'
		
	#Male
	if name == 'male':
		male = extsea.Attribute('male')
		male.affect = ['strength', 'life']
		male.max_level = 1
		def male_mod(self, mod):
			mod.tbonus *= 1.2
		male.mod = male_mod
		male.atype = 'gender'
		male.title = 'Mężczyzna'
		return(male)
	
	#Female
	if name == 'female':
		female = extsea.Attribute('female')
		female.affect = ['speed', 'magic']
		female.max_level = 1
		def female_mod(self, mod):
			mod.tbonus *= 1.2
		female.mod = female_mod
		female.atype = 'gender'
		female.title = 'Kobieta'
		return(female)
	
	#Bite
	if name == 'bite':
		bite = extsea.Attribute('bite')
		bite.dep = ['strength']
		def bite_use(self, user, target):
			dmg = target.damage(self.level)
		bite.use_func = bite_use
		bite.multi = 5
		bite.atype = 'attack'
		bite.title = 'Ugryzienie'
		return(bite)
	
	#Hit
	if name == "hit":
		hit = extsea.Attribute("hit")
		hit.dep = ["strength"]
		def hit_use(self, user, target):
			dmg = target.damage(self.level)
			self.increase()
		hit.use_func = hit_use
		hit.multi = 5
		hit.max_level = 9
		hit.atype = "attack"
		hit.title = "Uderzenie"
		return(hit)
	#Traits
	if 'trait_' in name:
		trait_name = name.split('_')[1]
		trait = extsea.Attribute(name)
		trait.affect = [trait_name]
		trait.max_level = 1
		def trait_mod(self, mod):
			mod.tbonus *= 1.1
		trait.mod = trait_mod
		trait.atype = 'trait'
		return(trait)
	
	#AI
	if 'ai_' in name:
		ai = extsea.Attribute(name)
		ai.max_level = 1
		ai.atype = 'ai'
		if name == 'ai_hit':
			ai.title = 'Uderzacz'
		return(ai)
	
	if name == 'money':
		result.max_level = 1000000
		result.atype = 'item'
		result.title = 'Pieniądze'
	
	return(result)

def createl(name, level):
	'''Create attribute with specified level.
	name - attribute's name (same as in create)
	level - initial level'''
	attrib = create(name)
	attrib.rlevel = level
	return(attrib)


def create_monster(name):
	'''Create a new monster by name.
	
	Example:
	wolf = rpgdb.create_monster('wolf')
	
	Available monsters:
	wolf
	mushroom
	bat'''
	result = extsea.Character(name)
	result.add(createl('strength', 1))
	result.add(createl('speed', 1))
	result.add(createl('life', 1))
	if name == 'wolf':
		wolf = extsea.Character('Wilk')
		wolf.add(create('wolf'))
		wolf.add(createl('strength', 4))
		wolf.add(createl('speed', 4))
		wolf.add(createl('life', 4))
		wolf.add(createl('bite', 4))
		wolf.fight = ai_dumb
		wolf.team = 2
		return(wolf)
	
	if name == 'mushroom':
		mushroom = extsea.Character('Grzyb')
		mushroom.add(create('mushroom'))
		mushroom.add(createl('strength', 1))
		mushroom.add(createl('speed', 1))
		mushroom.add(createl('life', 1))
		mushroom.add(createl('bite', 1))
		mushroom.fight = ai_dumb
		mushroom.team = 2
		return(mushroom)
	
	if name == 'bat':
		result.name = 'Nietoperz'
		result.add(create('bat'))
		result.add(createl('bite', 1))
		result.fight = ai_dumb
		result.team = 2
	
	return(result)
