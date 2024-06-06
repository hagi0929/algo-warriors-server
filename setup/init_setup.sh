conda env create -f environment.yaml
conda init --all --dry-run --verbose
conda activate cs348-proj-server
conda install -r requirements.txt
cp template.env .env
echo "don't forget to fill up .env :)"