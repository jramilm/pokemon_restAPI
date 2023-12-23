# Pokemon Resful API

## Project Details

This project is a Flask-based API for managing Pokemon data, including information about Pokemon, their types, and abilities. The API allows users to retrieve, add, update, and delete Pokemon records. Additionally, it supports searching for Pokemon based on various criteria.

## Installation Instructions

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/pokemon-api.git
   ```

2. Navigate to the project directory:

   ```bash
   cd pokemon-api
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your MySQL database and update the configuration in `app.py` with your database details.

5. Run the application:

   ```bash
   python main.py
   ```

## Usage Examples

### 1. Get all Pokemon

```bash
curl http://localhost:5000/api/pokemon
```

### 2. Get Pokemon by ID

```bash
curl http://localhost:5000/api/pokemon/1
```

### 3. Search for Pokemon

```bash
curl "http://localhost:5000/api/pokemon?search=pok_name:Bulbasaur,type_name:Grass,is_hidden:0"
```

### 4. Add Pokemon

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"pok_name\": \"Charmander\", \"pok_height\": 6, \"pok_weight\": 8, \"pok_base_experience\": 64}" http://localhost:5000/api/pokemon
```

### 5. Update Pokemon

```bash
curl -X PUT -H "Content-Type: application/json" -d "{\"pok_name\": \"Charizard\"}" http://localhost:5000/api/pokemon/4
```

### 6. Delete Pokemon

```bash
curl -X DELETE http://localhost:5000/api/pokemon/4
```

## Unit Tests

Unit tests are available to ensure the correctness of the API. To run the tests, use the following command:

```bash
python unittests.py
```

Make sure to have the required dependencies installed before running the tests. The test script (`test_app.py`) contains various test cases for different API endpoints and functionalities.


## API Usage

The API supports multiple endpoints for interacting with Pokemon data. Here are some of the key endpoints:

- **GET /api/pokemon**: Retrieve all Pokemon or search based on criteria.
- **GET /api/pokemon/{pok_id}**: Retrieve Pokemon by ID.
- **POST /api/pokemon**: Add a new Pokemon.
- **PUT /api/pokemon/{pok_id}**: Update an existing Pokemon.
- **DELETE /api/pokemon/{pok_id}**: Delete a Pokemon by ID.

For more details on the available endpoints and parameters, refer to the API documentation.

## Additional Information

- Some get methods like filtering by type and abilities are also available
- The API supports response formatting in both JSON and XML. Use the `format` parameter in the URL to specify the desired format (`json` or `xml`).
- Make sure to include valid search criteria when using the search functionality, such as `pok_name:Bulbasaur,type_name:Grass`.

## Note

This project is part of a school project and is currently incomplete. I may be motivated to update and enhance it in the future.
