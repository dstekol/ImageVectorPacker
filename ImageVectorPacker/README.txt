This program is meant to be run on the nlpgrid system at the University of Pennsylvania.

The filepath for this program on the nlpgrid is:
/mnt/nlpgridio3/data/dstekol/ImageVectorPacker.py

The purpose of this program is to collect specified images and image vectors and compile them into a folder 
so that they are easy to transport for demo purposes.

It is used as follows:
Enter 10 native English words, separated by commas, as instructed. 
	Example: 
		dog, cat, raccoon, animal, friend, city, silver, 
Enter the name of a foreign language, as instructed.
	Example: 
		french
Enter a foreign word in the previously specified language, as instructed.
	Example [cat in french]: 
		chat 

If any of these inputs are not found in the file system, or if the you did not enter a valid input (ex. entered 9 words instead of 10),
you will be asked to reenter this input.

Once the program has finished, you will find all relevant files in the folder "demofiles", 
which is in the same directory as the ImageVectorPacker program. To run the ImageMatching demo, 
all folders/files inside the demofiles folder should be copy-pasted directly into the images folder within 
ImageMatching (the demofiles folder itself should not be copied over - only its descendants).
Once this is done, the index.html file can be opened in a browser, and the ImageMatching program will run.

Contact dstekol@seas.upenn.edu with questions.



