# clip.board

## Description

Clip.board is a web-based cinema application desinged to provide users with an intuitive platform where they can browse movie schedules, select showtimes, and reserve seats. The backend is developed in Python with Flask for data management, while the frontend is builed with React for a modern and interactive user interface.
 
## Functionalities

### 1. Data Source:
Our database will integrate with a reliable API to fetch real-time data about movies. This API will deliver:
- General Information: Titles, synopsis, duration, genres, age ratings, user scores, etc.
-	Multimedia Resources: Promotional assets such as movie posters.

 
### 2. Data Storage and Handling:
A relational database will be used for managing all project data. The database structure will include:
-	Movies Table: Stores essential information about the movies on the schedule, such as title, description, duration, etc.
-	User Table: Stores essential information about the users, such as first and last name, email adress, role, etc.
-	Reservation Table: Stores essential information about reservations, such as total price, time or reservation, showtime, user, etc.
-	Showtimes Table: Links movies with their available dates and times.
-	Theaters Table: Details each cinema hall, including its name and seating capacity.
-	Seats Table: Tracks the availability of seats (available, reserved) for each showtime in each theater.
-	Showtime Table: Stores essential information about which movies play at which times and halls.
-	Logs and histories Table: Stores essential information about user actions at clip.board.

 
### 3. User account management system:
Database Schema - Create a robust users table with the following fields:
-	id (Primary Key)
-	first name (string)
-	last name (string)
-	password (string)
-	email (unique string)
-	role ('Admin', 'Client')

User Management
-	Browse and select available movies.
-	Choose preferred seats for a chosen movie.
-	View detailed prices for bookings.
-	Manage their account details (e.g., update email, password).

Admin Management
-	Manage bookings: Cancel or adjust user bookings as needed.
-	Monitor user activity: View user booking history and platform engagement for insights.
-	Get statistics for each showtime: number and percentage of available and not available seats, total income, monthly income

 
### 4. Web Interface:
The web application will feature an intuitive, user-friendly interface built with the following tools:
-	React: Used to create reusable and interactive components for dynamic content rendering.
-	React Router: Manage client-side navigation and routing within the application.
  
Key Interface Features
Movie Schedule View: users will be able to browse the movie schedule with advanced search and filter functionalities, such as:
-	Genre Filter: Display movies based on selected genres (e.g., Action, Comedy, Drama).
-	Duration Filter: Filter movies by length (e.g., < 90 minutes, 90-120 minutes, > 120 minutes).
-	Vote Average Filter: Filter movies by vote averages from 0 to 10.
-	Search by Keyword: Allow users to search for movies by title or director.
-	Interactive Seat Selection: Users can select their desired showtimes and pick seats through an intuitive, clickable seating map.
-	Streamlined Reservation Process: The system ensures a straightforward flow, enabling users to complete seat reservations in just a few steps.
 

### 5. Visualizations:
Interactive Seat Map
-	A graphical display of the seating arrangement within the cinema hall.
-	Seats are visually represented and change status (available, booked, or selected) dynamically to enhance the user experience.

Example color coding:
-	White: Available seats.
-	Red: Reserved seats.
-	Blue: Selected seats.

Movie Schedule
The movie schedule will present a visually engaging display:
-	Movie posters or banners for each title.
-	A list of available showtimes for each movie, if you select a movie.
-	Additional key details such as genre, duration, an overview and rating.

### 6. Statistical Analysis:
- Calculate number of available seats
- Calculate number of not available seats
- Calculate percentage of available seats
- Calculate percentage of not available seats
- Calculate total income and monthly income for each show
- Calculate list of available seats
- Calculate list of not available seats
