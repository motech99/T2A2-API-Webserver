# T2A2: API Webserver

## Table of Contents

- [Problem and Solution](#r1-problem-and-solution)
- [Task Allocation and Tracking](#r2-task-allocation-and-tracking)
- [Third-Party Services and Dependencies](#r3-third-party-services-and-dependencies)
- [Database System: Benefits and Drawbacks](#r4-database-system-benefits-and-drawbacks)
- [ORM: Features and Functionalities](#r5-orm-features-and-functionalities)
- [Models and Relationships](#r6-models-and-relationships)
- [Database Implementation During Development](#r7-database-implementation-during-development)
- [API Endpoints Usage](#r8-api-endpoints-usage)

## R1 Problem and Solution

### Problem

The current state of Pokemon game development presents a challenge for both experienced and novice programmers because of the overwhelming amount of information and complexity involved. The widely used [PokéAPI](https://pokeapi.co/) provides a comprehensive dataset including tens of thousands of Pokemon, moves, items, abilities, and other complex details. This extensive amount of information can be overwhelming for developers in two main scenarios: when building new Pokemon games or experiences, and when new to Pokemon game development or programming in general.

For example, a developer named Sergio Perez tried to build a small application to display the original 151 Pokemon. Even for this seemingly simple task, he had to make multiple requests to the PokeAPI to retrieve all the necessary data. This illustrates the challenges developers face when working with such a comprehensive dataset. This article can be found here [Fetching Them All: Poke API](https://medium.com/@sergio13prez/fetching-them-all-poke-api-62ca580981a2)

### Solution

To address this issue, this is where this Pokemon API comes into play. This API provides a wealth of information about Pokemon, such as their types, abilities. It also includes details about trainers' affiliations with gyms. The goal of this API is to make Pokemon game development more accessible to aspiring programmers by presenting a simplified and well-documented interface, thus lowering the barrier to entry for beginners.

This simplified Pokemon API has the potential to lead to faster development and more diverse Pokemon games by reducing development hurdles and attracting new programmers. Ultimately, this API aims to contribute to a more vibrant Pokemon gaming ecosystem by solving the issue of information overload and promoting accessibility.

## R2 Task Allocation and Tracking

All tasks are allocated and tracked through a Trello board. This allows me to visually organise tasks using cards and lists, providing a clear overview of the project's progress. The status of each task is updated as it moves through different stages of completion. Trello's features, such as due dates, labels, and comments, help me manage deadlines and prioritise work.

### This is what it currently looks like as of **20/06/2024**. More features may be added depending on the time

![1](./docs/r2-1.png)
![2](./docs/r2-2.png)

## R3 Third-Party Services and Dependencies

## R4 Database System: Benefits and Drawbacks

## R5 ORM: Features and Functionalities

## R6 Models and Relationships

![1](./docs/pokemon-ERD.png)

The Entity Relationship Diagram (ERD) offers a clear visual representation of the database structure, making it easier to understand the relationships between different entities. It helps organise the data in a structured manner, ensuring that all necessary entities and their attributes are accounted for.

### The database consists of five main tables

### Pokemon

- **Attributes:** Pokemon_Id (PK), name, type, ability, date_caught
- **Description:** The Pokemon table contains information about each Pokémon.
- **Primary Key:** Pokemon_Id uniquely identifies each Pokémon

### Moves

- **Attributes:** Moves_Id (PK), name, power, accuracy, type, category
- **Description:** The Moves table stores information about each move that Pokémon can learn.
- **Primary Key:** Moves_Id uniquely identifies each move.

### Pokemon_Moves

- **Attributes:** Pokemon_Id (FK), Moves_Id (FK)
- **Description:** The Pokemon_Moves table establishes a many-to-many relationship between Pokémon and their moves.
- **Foreign Keys:**
  - **Pokemon_Id** references Pokemon_Id in the Pokemon table.
  - **Moves_Id** references Moves_Id in the Moves table.
- **Purpose:** Allows each Pokémon to have multiple moves and each move to be learned by multiple Pokémon.

### Trainers

- **Attributes:** Trainer_ID (PK), name, username, password, gym_id (FK)
- **Description:** The Trainers table stores information about each trainer, including their credentials for authentication and their affiliation with a specific gym.
- **Primary Key:** Trainer_ID uniquely identifies each trainer.
- **Foreign Key:** gym_id references Gym_id in the Gyms table.

### Gyms

- **Attributes:** Gym_id (PK), Name, Team
- **Description:** The gym's table captures details about each gym, including their team affiliation.
- **Primary Key:** Gym_id uniquely identifies each gym.
- **Team:** Indicates the team (Mystic, Valor, Instinct)

### Benefits of the ERD in Database Design

#### Clarity and Planning

**Visualisation:** The ERD provides a clear visual representation of the database structure, making it easier to understand the relationships between different entities.

**Organisation:** It helps organise the data in a structured manner, ensuring that all necessary entities and their attributes are accounted for.

#### Normalisation

**Avoiding Redundancy:** The ERD helps in normalising the database by eliminating redundant data. For example, moves are stored separately in the Moves table and linked to Pokémon through the Pokemon_Moves table.

**Data Integrity:** Ensures that data is stored in only one place, reducing the chances of data anomalies and maintaining consistency.

#### Defining Relationships

**Foreign Keys:** The use of foreign keys (FK) enforces referential integrity, ensuring that relationships between tables are maintained correctly. For instance, Pokemon_Id in Pokemon_Moves must match a valid Pokemon_Id in the Pokemon table.

**Relationships:** Clearly defines how entities relate to each other (one-to-many, many-to-many), aiding in the correct implementation of business rules. For example, the many-to-many relationship between Pokémon and Moves allows for flexibility in assigning moves to Pokémon.

## R7 Database Implementation During Development

## R8 API Endpoints Usage

### HTTP Verb
### Path or Route
### Required Data
### Response
