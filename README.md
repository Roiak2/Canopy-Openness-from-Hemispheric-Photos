# Canopy Openness from Hemispheric Photos

Canopy openness - the amount of light penetrating a canopy - is a crucial metric in understanding ecosystem dynamics and function, especially after a disturbance like a fire or a cyclone.

This package assists foresters by taking an input of hemispheric photos, calculating canopy openness for the photos, and outputting a dataframe with the results, as well as pretty plots.

### In Development

This program can be installed this way:

```
#install dependency pacakages
conda install pandas matplotlib numpy natsort scikit-image -c conda-forge 

#clone repository of package
git clone [https://github.com/Roiak2/Canopy-Openness-from-Hemispheric-Photos]

#enter into the cloned directory
cd ./Canopy-Openness-from-Hemispheric-Photos

#install onto your machine
pip install -e .
```

### Working example

After loading the program in your machine, you can go to the WorkingExample jupyter notebook found in the top directory of this repo.

That notebook contains a sample workflow for you to test the ImageLoad and FishEye modules with a sample photo (you can try it on your own pictures as well).

As the package gets developed, the working example notebook will be updated to reflect developments.

