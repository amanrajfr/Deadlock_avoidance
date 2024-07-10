# Deadlock Detection and Safe Sequencing in Operating Systems

## Project Overview

This project focuses on deadlock detection and safe sequencing in Windows and Linux operating systems. The objective is to analyze and compare the effectiveness of deadlock detection mechanisms using Python for core functionality and JavaScript for system data collection.

## Objectives

- Understand deadlocks and their impact on system performance.
- Investigate deadlock detection mechanisms in Windows and Linux.
- Compare the effectiveness of these mechanisms.
- Provide recommendations for improving deadlock detection.

## Methodology

1. **Experimental Setup**: Created testing environments in both Windows and Linux.
2. **Script Development**: Developed scripts to simulate deadlocks and collect data.
3. **Banker's Algorithm**: Implemented in Python to detect deadlocks.
4. **System Information Collection**: Used JavaScript to gather and process system data.

## Tools and Technologies

- **Python**: Core functionality, including deadlock detection using the Banker's algorithm.
- **JavaScript**: System data collection and processing.
- **MySQL**: Database management for process data.
- **Pandas & Matplotlib**: Data visualization for resource usage and performance.

## Installation

### Prerequisites

- Python 3.x
- Node.js
- MySQL

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/deadlock-detection.git
    cd deadlock-detection
    ```

2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install Node.js dependencies:
    ```bash
    cd js
    npm install
    cd ..
    ```

4. Set up MySQL database:
    - Create a new database.
    - Import the provided SQL script to create necessary tables.

5. Configure database connection in the Python script (`cos1.py`):
    ```python
    db_connection = mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )
    ```

6. Run the JavaScript data collector:
    ```bash
    node js/extracr1.js
    ```

7. Run the Python script for deadlock detection:
    ```bash
    python cos1.py
    ```

## Usage

- The JavaScript script (`extracr1.js`) collects system information and writes it to a CSV file (`output.csv`).
- The Python script (`cos1.py`) reads the data from `output.csv`, performs deadlock detection using the Banker's algorithm, and visualizes the results.

## Results

- **Insights**: Key differences in deadlock detection efficiency between Windows and Linux.
- **Improvements**: Potential enhancements in current deadlock detection methods.
- **Report**: Detailed findings and recommendations in the [project report](report.pdf).

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.


## Contact

For questions or discussions, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/amanrajfr/) .
