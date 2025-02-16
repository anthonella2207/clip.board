import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./SupportPage.css";
import emailjs from '@emailjs/browser';

const SupportPage = () => {
  const [formData, setFormData] = useState({ name: "", email: "", message: "" });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
    setSubmitted(true);
  };

 const sendEmail = (e) => {
  e.preventDefault();

  emailjs.sendForm('service_ooob27q', 'template_eprk9q9', e.target, 'fUUgZ4BuPt-h0FxeW')
    .then((result) => {
      console.log(result.text);
      setSubmitted(true);
      setFormData({ name: "", email: "", message: "" }); // Limpiar el formulario
    }, (error) => {
      console.log(error.text);
    });
};

  return (
    <div className="support-container">
      <h1>Support & Help Center</h1>
      <p>If you have any questions or issues, feel free to reach out to us.</p>

      <h2>Frequently Asked Questions</h2>
      <div className="faq-section">
        <details>
          <summary>How does the home page work?</summary>
          <p>The home page displays top-rated, now-playing, and upcoming movies. You can filter the movies that we are showing at the moment by genre, duration, rating, or search for specific titles.</p>
        </details>
        <details>
          <summary>Can I book a seat without logging in?</summary>
          <p>No, you must be logged in to book a seat.</p>
        </details>
        <details>
          <summary>Do I need to bring my reservation number?</summary>
          <p>Yes, you must bring your reservation number when you arrive at the cinema to confirm and pay for your booking.</p>
        </details>
        <details>
          <summary>What payment methods do you accept?</summary>
          <p>We accept credit cards, PayPal, and Apple Pay.</p>
        </details>
        <details>
          <summary>How can I change my account details?</summary>
          <p>You can update your account details by visiting the profile page and editing your information, such as name, email, and password.</p>
        </details>
        <details>
          <summary>Can I browse movies without an account?</summary>
          <p>Yes, you can browse movies and view details without an account, but booking requires logging in.</p>
        </details>
        <details>
          <summary>How do I search for a specific movie?</summary>
          <p>You can use the search bar on the home page to find a specific movie by title.</p>
        </details>
        <details>
          <summary>How do I report an issue with my booking?</summary>
          <p>If you experience any issues with your booking, please contact our support team using the contact form below.</p>
        </details>
        <details>
          <summary>Can I cancel a reservation?</summary>
          <p>Yes, you can cancel a reservation on the bookings page.</p>
        </details>
      </div>

      <h3>Contact Us</h3>
      {submitted ? (
        <p>Thank you! Your message has been received. We will get back to you soon.</p>
      ) : (
        <form className="support-form" onSubmit={sendEmail}>
          <input type="text" name="name" placeholder="Your Name" required onChange={handleChange} />
          <input type="text" name="email_from" placeholder="Your Email" required onChange={handleChange} />
          <textarea name="message" placeholder="Your Message" required onChange={handleChange}></textarea>
          <button type="submit">Submit</button>
        </form>
      )}

      <Link to="/">Back to Home</Link>
    </div>
  );
};

export default SupportPage;
