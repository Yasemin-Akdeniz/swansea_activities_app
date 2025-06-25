# Swansea Activities App

## Activity List for Isolated Parents and Carers

This project is a web application designed to help isolated parents and carers in Swansea find low-cost or free activities for their children. It leverages web scraping to gather activity data from various local sources, stores it in a database, and presents it through a user-friendly web interface with search and filtering capabilities.

---

## Features

* **Web Scraping:** Automatically collects activity data from multiple online sources (e.g., Swansea Council, local news blogs).
* **Data Storage:** Persists collected activity data in a local SQLite database using Flask-SQLAlchemy.
* **RESTful API:** Exposes activity data via a Flask-based API endpoint (`/activities`) for easy consumption.
* **Modern User Interface (UI):** A clean, responsive, and intuitive frontend built with Bootstrap, displaying activities in an organized card format.
* **Search & Filter Functionality:** Allows users to search for activities by title or description and filter by cost (e.g., "Free Only").

---

## Technologies Used

* **Python:** The core programming language for the backend and scraping logic.
* **Flask:** A micro web framework for building the API and serving the web application.
* **SQLAlchemy & Flask-SQLAlchemy:** For Object Relational Mapping (ORM) to interact with the SQLite database.
* **BeautifulSoup4:** A Python library for parsing HTML and XML documents, used in web scraping.
* **Requests:** A Python library for making HTTP requests to fetch web page content.
* **HTML, CSS, JavaScript:** For the frontend web interface.
* **Bootstrap 5:** A popular CSS framework for responsive and modern UI components.
* **SQLite:** A lightweight, file-based database for storing activity data.

---

## Setup and Installation

To get this project up and running on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Yasemin-Akdeniz/swansea_activities_app.git](https://github.com/Yasemin-Akdeniz/swansea_activities_app.git)
    cd swansea_activities_app
    ```

2.  **Create and Activate a Virtual Environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Install all required Python packages.
    ```bash
    pip install Flask Flask-SQLAlchemy requests beautifulsoup4
    # Alternatively, if you plan to create a requirements.txt:
    # pip install -r requirements.txt
    ```

4.  **Initialize the Database:**
    You need to create the database file and tables once.
    * Open `app.py`.
    * **Uncomment** the `create_database()` line at the bottom of the `app.py` file:
        ```python
        if __name__ == '__main__':
            create_database() # Uncomment this line ONCE
            app.run(debug=True)
        ```
    * Run `app.py` from your terminal:
        ```bash
        python app.py
        ```
    * Once you see `Database 'site.db' created successfully.`, **comment out** the `create_database()` line again in `app.py` to prevent it from trying to recreate the database on every run.

5.  **Run the Web Scraper:**
    This will fetch activities and populate your database. Make sure your Flask app (`app.py`) is running in a separate terminal.
    ```bash
    python scraper.py
    ```

6.  **Start the Flask Application:**
    Ensure `create_database()` is commented out in `app.py`.
    ```bash
    python app.py
    ```

7.  **View the Application:**
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

---

## Demo

*(After setting up and running the app, you can capture a short GIF/video demo and place it here.
Example: `![App Demo](images/app_demo.gif)`)*

---

## Future Enhancements (Potential Next Steps)

* **More Detailed Activity Information:** Enhance scraping to gather specific dates, times, exact locations, and age ranges where available.
* **Advanced Filtering:** Add filtering options for dates, specific locations, or age suitability.
* **Pagination:** Implement pagination for large datasets to improve performance and user experience.
* **Scheduled Scraping:** Automate the `scraper.py` to run at regular intervals (e.g., daily/weekly) to keep activity data up-to-date.
* **Deployment:** Deploy the application to a cloud platform (e.g., Heroku, Render, Vercel) for public access.

---

## Contributing

Feel free to fork this repository, submit pull requests, or open issues if you have suggestions or find bugs.

---

## License

This project is open-source and available under the MIT License.
