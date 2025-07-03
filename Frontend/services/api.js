const API_BASE_URL = 'http://localhost:5000/api';

export const fetchReminders = async (date) => {
  const response = await fetch(`${API_BASE_URL}/reminders?date=${date}`);
  if (!response.ok) {
    throw new Error('Failed to fetch reminders');
  }
  return response.json();
};

export const fetchPatients = async () => {
  const response = await fetch(`${API_BASE_URL}/patients`);
  if (!response.ok) {
    throw new Error('Failed to fetch patients');
  }
  return response.json();
};
