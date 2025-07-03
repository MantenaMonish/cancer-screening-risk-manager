import React, { useState, useEffect } from 'react';
import ReminderList from './ReminderList';
import { fetchReminders } from '../services/api';
import RiskIndicator from './RiskIndicator';

const Dashboard = ({ date, setDate }) => {
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total: 0,
    high: 0,
    medium: 0,
    low: 0
  });

  useEffect(() => {
    const loadReminders = async () => {
      try {
        setLoading(true);
        const data = await fetchReminders(date);
        setReminders(data.reminders || []);
        
        // Calculate statistics
        const stats = {
          total: data.reminders?.length || 0,
          high: data.reminders?.filter(r => r.risk === 'High').length || 0,
          medium: data.reminders?.filter(r => r.risk === 'Medium').length || 0,
          low: data.reminders?.filter(r => r.risk === 'Low').length || 0
        };
        setStats(stats);
      } catch (error) {
        console.error('Error loading reminders:', error);
      } finally {
        setLoading(false);
      }
    };

    loadReminders();
  }, [date]);

  return (
    <div>
      <div className="mb-8 bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Screening Reminders Dashboard</h2>
        
        <div className="flex items-center mb-6">
          <label htmlFor="date-selector" className="mr-3 font-medium">As of:</label>
          <input
            type="date"
            id="date-selector"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="border rounded px-3 py-2"
          />
          <button 
            onClick={() => setDate(new Date().toISOString().split('T')[0])}
            className="ml-3 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Today
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
            <h3 className="text-lg font-semibold text-blue-800">Total Reminders</h3>
            <p className="text-3xl font-bold">{stats.total}</p>
          </div>
          <div className="bg-red-50 p-4 rounded-lg border border-red-100">
            <h3 className="text-lg font-semibold text-red-800">High Risk</h3>
            <p className="text-3xl font-bold">{stats.high}</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-100">
            <h3 className="text-lg font-semibold text-yellow-800">Medium Risk</h3>
            <p className="text-3xl font-bold">{stats.medium}</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg border border-green-100">
            <h3 className="text-lg font-semibold text-green-800">Low Risk</h3>
            <p className="text-3xl font-bold">{stats.low}</p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Upcoming Screenings</h2>
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : reminders.length > 0 ? (
          <ReminderList reminders={reminders} />
        ) : (
          <div className="text-center py-8 text-gray-500">
            <p>No upcoming screening reminders for this date.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;