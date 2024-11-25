# Cinema Reservation

Description

The Cinema Web Application aims to provide users with an intuitive platform where they can browse movie schedules, select showtimes, and reserve seats. The backend will be developed in Python for data management, while the frontend will leverage React and Next.js for a modern and interactive user interface.
 
Functionalities

1. Data Source:
The system will integrate with a reliable API to fetch real-time data about movies. This API will deliver:
- General Information: Titles, synopsis, duration, genres, age ratings, and user scores.
-	Showtimes: Specific dates and times for each movie available in the schedule.
-	Multimedia Resources: Promotional assets such as movie posters, banners, and links to trailers.

 
3. Data Storage and Handling:
A relational database will be used for managing all project data. The database structure will include:
•	Movies Table:
Stores essential information about the movies on the schedule, such as title, description, and duration.
•	Showtimes Table:
Links movies with their available dates and times.
•	Theaters Table:
Details each cinema hall, including its name and seating capacity.
•	Seats Table:
Tracks the availability of seats (available, reserved) for each showtime in each theater.

 
4. User account management system:
•	Database Schema:
Create a robust users table with the following fields:
o	id (Primary Key)
o	username (Unique identifier)
o	password (Securely hashed)
o	email (Unique and validated)
o	role (e.g., user, admin)
User Management
o	Browse and select available movies.
o	Choose preferred showtimes and seats.
o	View detailed price breakdown for bookings.
o	Manage their account details (e.g., update email, password).
Admin Management
o	Modify movie schedules: Adjust which movies are shown in which theaters and at what times.
o	Manage bookings: Cancel or adjust user bookings as needed.
o	Monitor user activity: View user booking history and platform engagement for insights.

 
5. Web Interface:
The web application will feature an intuitive, user-friendly interface built with the following tools:
•	React:
Used to create reusable and interactive components for dynamic content rendering.
•	Next.js:
Provides optimized performance, server-side rendering, and seamless management of dynamic routes.
Key Interface Features
•	Movie Schedule View:
Users will be able to browse the movie schedule with advanced search and filter functionalities, such as:
o	Genre Filter: Display movies based on selected genres (e.g., Action, Comedy, Drama).
o	Duration Filter: Filter movies by length (e.g., < 90 minutes, 90-120 minutes, > 120 minutes).
o	Age Rating Filter: Show only movies appropriate for specific audiences (e.g., PG, R-rated).
o	Search by Keyword: Allow users to search for movies by title or director.
•	Interactive Seat Selection:
Users can select their desired showtimes and pick seats through an intuitive, clickable seating map.
•	Streamlined Reservation Process:
The system ensures a straightforward flow, enabling users to complete seat reservations in just a few steps.
 

6. Visualizations:
Interactive Seat Map
•	A graphical display of the seating arrangement within the cinema hall.
•	Seats are visually represented and change status (available, reserved, or selected) dynamically to enhance the user experience.
•	Example color coding:
o	Green: Available seats.
o	Red: Reserved seats.
o	Blue: Selected seats.
Movie Schedule
•	The movie schedule will present a visually engaging display:
o	Movie posters or banners for each title.
o	A list of available showtimes for each movie.
o	Additional key details such as genre, duration, and rating.

