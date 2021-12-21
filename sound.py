
import pygame

#pygame.mixer.init() this instruction shuld be put on the start of the main file i put it here so as to make it work at first ... same thing ggoes for the last instruction 

SOUND = {}
for filename in ['chop1', 'chop2', 'hammering1', 'hammering2', 'hammering3', 'hammering4', 'hammering5',
				 'hammering6', 'treeFalling', 'thud', 'splash', 'groan', 'mining1', 'mining2', 'mining3',
				 'mining4', 'click', 'tick', 'error', 'pop', 'eating1', 'eating2', 'eating3', 'clunk',
				 'achievement', 'explosion','background']: # .wav files only these are examples of voices that can be modified afterwards
	SOUND[filename] = pygame.mixer.Sound('assets\\sounds\\%s.wav' %(filename))#in order to choose from already exsting sounds . keep in mind directory depends on the user but all in all since all of the project wuld be in one repertory then the directory culd be set

def play(sound, volume=0.8, loops=0):
	"""Plays the given sound"""
	if not muted: #muted is a parametre that shuld be in settings
		SOUND[sound].set_volume(volume)
	SOUND[sound].play(loops)

SOUND['background'].play(-1) # this should be put on the main file 
#pygame.mixer.quit() 

#this fuction would be integrated in any given act or event
