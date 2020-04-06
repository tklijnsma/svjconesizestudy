# Cone size study for Semi-visible Jets

This package plots the substructure of boosted objects.


## Installation

```
cmsrel CMSSW_10_2_18
cd CMSSW_10_2_18/src
git clone https://github.com/tklijnsma/DataFormats-SVJFormats.git DataFormats/SVJFormats
scram b -j 8


mkdir NonPackage/ConeSizeStudy
cd NonPackage/ConeSizeStudy

virtualenv myenv
source myenv/bin/activate

git clone https://github.com/tklijnsma/svjconesizestudy.git
pip install --user -e svjconesizestudy
```

(I might have forgotten some pip installations!)


## Usage

Run `jupyter-notebook` and see [this notebook](plot3d.ipynb).
