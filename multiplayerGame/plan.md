>>> the game starts
> main menu... might be simple or with some dynamic background
more on dynamic background... (#feature)


_> create game_
selection...
	! 2 player >>> But actually 1 extra player will join
	! 4 player >>> ...3
	! 6 player >>> ...5
	! 8 player >>> ...7

		THE SERVER MODULE WILL BE CALLED
	>>> after which...
		# for this player only the client will join
		# automatically

_> join game_
waiting to automatically join...
>>> joined game
		WAITING FOR MATCH TO BEGIN...
			( till server sends a start)
			# try in the running 
			# timeout...
			# allow an exit button

... STARTING GAME IN 3, 2, 1...

_> start game_
		# SHOW TEAMS...
	>>> program in server that can segregate randomly...
		---> prefer... keys random.choice([1,2,3,4,5,6]) for 6
		# make a teams screen for each

	>>> send the req data for each player object to every obj. once for init...

> start sending the coords for angels...

_STRUCTURE OF DATA:_

	[ idA1 , idG1 , idA2 , idG2 , idA3, idG3]

_for guardian_

	idA1 = [int#id,(n,m)#locTomb , []#BlockChanges, []#poweruse]

_for angel_

	idG2 = [(n,m)#pos, int#health, float#stamina]


_>>>>>>>>>>>>>>>>>>>>>>>>>_
_>>>>>>>>GAMEPLAY<<<<<<<<<_
_<<<<<<<<<<<<<<<<<<<<<<<<<_
