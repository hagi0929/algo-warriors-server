conda env create -f environment.yml
conda init --all --dry-run --verbose
conda activate cs348-env
cp template.env .env
echo "don't forget to fill up .env :)"