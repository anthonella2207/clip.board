# Cinema Reservation

## Description

The Cinema Web Application aims to provide users with an intuitive platform where they can browse movie schedules, select showtimes, and reserve seats. The backend will be developed in Python for data management, while the frontend will leverage React and Next.js for a modern and interactive user interface.
 
## Functionalities

### 1. Data Source:
The system will integrate with a reliable API to fetch real-time data about movies. This API will deliver:
- General Information: Titles, synopsis, duration, genres, age ratings, and user scores.
-	Showtimes: Specific dates and times for each movie available in the schedule.
-	Multimedia Resources: Promotional assets such as movie posters, banners, and links to trailers.

 
### 3. Data Storage and Handling:
A relational database will be used for managing all project data. The database structure will include:
-	Movies Table: Stores essential information about the movies on the schedule, such as title, description, and duration.
-	Showtimes Table: Links movies with their available dates and times.
-	Theaters Table: Details each cinema hall, including its name and seating capacity.
-	Seats Table: Tracks the availability of seats (available, reserved) for each showtime in each theater.

 
### 4. User account management system:
Database Schema - Create a robust users table with the following fields:
-	id (Primary Key)
-	username (Unique identifier)
-	password (Securely hashed)
-	email (Unique and validated)
-	role (e.g., user, admin)

User Management
-	Browse and select available movies.
-	Choose preferred showtimes and seats.
-	View detailed price breakdown for bookings.
-	Manage their account details (e.g., update email, password).

Admin Management
-	Modify movie schedules: Adjust which movies are shown in which theaters and at what times.
-	Manage bookings: Cancel or adjust user bookings as needed.
-	Monitor user activity: View user booking history and platform engagement for insights.

 
### 5. Web Interface:
The web application will feature an intuitive, user-friendly interface built with the following tools:
-	React: Used to create reusable and interactive components for dynamic content rendering.
-	Next.js: Provides optimized performance, server-side rendering, and seamless management of dynamic routes.
  
Key Interface Features
Movie Schedule View: users will be able to browse the movie schedule with advanced search and filter functionalities, such as:
-	Genre Filter: Display movies based on selected genres (e.g., Action, Comedy, Drama).
-	Duration Filter: Filter movies by length (e.g., < 90 minutes, 90-120 minutes, > 120 minutes).
-	Age Rating Filter: Show only movies appropriate for specific audiences (e.g., PG, R-rated).
-	Search by Keyword: Allow users to search for movies by title or director.
-	Interactive Seat Selection: Users can select their desired showtimes and pick seats through an intuitive, clickable seating map.
-	Streamlined Reservation Process: The system ensures a straightforward flow, enabling users to complete seat reservations in just a few steps.
 

### 6. Visualizations:
Interactive Seat Map
-	A graphical display of the seating arrangement within the cinema hall.
-	Seats are visually represented and change status (available, reserved, or selected) dynamically to enhance the user experience.

Example color coding:
-	Green: Available seats.
-	Red: Reserved seats.
-	Blue: Selected seats.

Movie Schedule
The movie schedule will present a visually engaging display:
-	Movie posters or banners for each title.
-	A list of available showtimes for each movie.
-	Additional key details such as genre, duration, and rating.

