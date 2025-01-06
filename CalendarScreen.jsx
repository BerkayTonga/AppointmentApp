import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

function CalendarScreen({ user, onLogout }) {
  const [date, setDate] = useState(new Date());
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    const fetchAppointments = async () => {
      const response = await axios.get(`/api/appointments?date=${date.toISOString()}`);
      setAppointments(response.data);
    };
    fetchAppointments();
  }, [date]);

  const handleAppointmentCreation = async (time) => {
    try {
      const response = await axios.post('/api/appointments', { date, time });
      if (response.data.success) {
        setAppointments([...appointments, response.data.appointment]);
      }
    } catch (error) {
      console.error('Error creating appointment:', error);
    }
  };

  return (
    <div className="calendar-screen">
      <header>
        <h1>Berber Name</h1>
        <div className="user-info">
          <span>{user.username}</span>
          <button onClick={onLogout}>Logout</button>
        </div>
      </header>
      <Calendar onChange={setDate} value={date} />
      <div className="appointments">
        {appointments.map((appt) => (
          <div key={appt.id}>{appt.time}</div>
        ))}
        <button onClick={() => handleAppointmentCreation('10:00')}>Add 10:00</button>
      </div>
    </div>
  );
}

export default CalendarScreen;