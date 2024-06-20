# Setup

### Prerequisites
- **Miniconda** (for managing the Python environment)

### Step-by-Step Instructions

#### 1. **Install Miniconda**
   - **Linux:**
     ```bash
     mkdir -p ~/miniconda3
     wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
     bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
     rm -rf ~/miniconda3/miniconda.sh
     ~/miniconda3/bin/conda init bash
     ```
   - **Mac:**
     ```bash
     mkdir -p ~/miniconda3
     curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
     bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
     rm -rf ~/miniconda3/miniconda.sh
     ~/miniconda3/bin/conda init bash
     ```

#### 2. **Set Up the Python Environment**
   - Create the environment using the `environment.yml` file:
     ```bash
     conda env create -f environment.yml
     conda activate your_environment_name  # Replace with the environment name specified in environment.yml
     ```

#### 3. **Configure Database Connection Strings**
   - **Fill the `.env` File**:
     - Copy and rename the `template.env` file to `.env`:
       ```bash
       cp template.env .env
       ```
     - Edit the `.env` file to include your database connection string. It should look something like this:
       ```
        DB_HOST = ''
        DB_PORT = ''
        DB_DATABASE_PROD = ''
        DB_DATABASE_DEV = ''
        DB_USER = ''
        DB_PASSWORD = ''
        ```

   - **Update `populate_table.py`**:
     - Open `populate_table.py` and update lines 15 and 21 with your database connection string. It should look something like this:
       ```python
        db_params = {
        'dbname': '',
        'user': '',
        'password': '',
        'host': '',
        'port': ''
        }
       ```

#### 4. **Set Up the Database**
   - Navigate to the `setup` folder:
     ```bash
     cd setup
     ```

   - Run the SQL scripts to create the tables:
     ```bash
     psql -U your_db_user -d your_db_name -f create_table/create_table.sql
     ```

#### 5. **Import Data**
   - Run the script to fetch and format the data:
     ```bash
     python populate_table/generate_db.py
     ```
   - This script will format the data and save it as `.json` files in the `populate_table` folder.

   - Populate the database with the JSON data:
     ```bash
     python populate_table/populate_table.py
     ```

#### 6. **Run the Application**
   - You can start the application using the following command:
     ```bash
     flask run
     ```


