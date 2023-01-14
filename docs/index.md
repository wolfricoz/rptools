##### `/help`
This command sends you to this page!

##### `/feedback [feedback]`
Wish to give suggestions or feedback for the bot? This command will send your feedback right to the dev! If you run into any issues please give as much detail as possible.

Your username and user ID are recorded when using this command.

##### ``/dice [dicetype] (amount)``
This command rolls a dice based upon the dice type you've given, for example if you put in 20; it will roll a 20 sided dice!
Amount means how much dice of 20 will be thrown. Let's say you want to throw three dices of 20, you'd do: `/dice 20 3` and it'd give you the results!

A dice may not be less than 2 sides, and not exceed 1000 sides. You can roll up to 10 dice at once.
##### `/coinflip`
This command will flip a coin for you and tell you either heads of tails, useful for deciding a yes or no situation!
### Generators
##### `/generators name [gender] [amount]`
This command is used to generate names for your character, currently the only two genders available are male and female, more generators might be added in the future

you can generate up to 25 names at a time, the default amount is 10.

Further I'd like to give thanks to Mark Kantrowitz and Bill Ross  of the CMU school of computer science for the lists with names.
source: [male](https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt), [female](https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt)
### Server templates
##### `/server template [template]`
This command applies a server template to your server by moving all the channels in the server to an archive and hiding them from non-administrative users. After this has been done it will apply the template to the server by creating the channels and sections.

You can find the templates by doing `/server template help`
##### `/server archivepurge`
This command will **PERMANENTLY** remove the channels in the archive. Only use this command if you are certain that you want to remove those channels. After deletion you can not retrieve these channels.





