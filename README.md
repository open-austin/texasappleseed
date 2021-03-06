# Texas Appleseed 

This project orginated from [this proposal](https://github.com/open-austin/project-ideas/issues/14). 
Now the mapping component of this project lives at https://github.com/txappleseed/txappleseedmap

#### License

Released to the public domain under [the Unlicense](http://unlicense.org/) by Open Austin, 2015.

#### Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md).

#### Data

ratioDistrict.csv contains some data about disparities in punishments for various groups and school districts, to be imported into the Leaflet school district map. The column names that we were planning to map are in this format:

    ratio (ECO. DISADV.|SPEC. ED.|BLACK OR AFRICAN AMERICAN|HISPANIC/LATINO|WHITE|AMERICAN INDIAN OR ALASKA NAT|ASIAN|NATIVE HAWAIIAN/OTHER PACIFIC|TWO OR MORE RACES) (EXPULSION ACTIONS|IN SCHOOL SUSPENSIONS|OUT OF SCHOOL SUSPENSIONS|DAEP PLACEMENTS) vs average

That means the map will need 36 settings (9 groups times 4 punishments) to show all the data we want to display. Here's [the Gist of the process](https://gist.github.com/mscarey/bdec4603313dd81da530) used to make ratioDistrict.csv.
