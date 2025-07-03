import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import PatientList from './components/PatientList';
import './index.css';

function App() {
  const [view, setView] = useState('dashboard');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-700 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Cancer Screening Reminder System</h1>
          <div className="flex space-x-4">
            <button 
              onClick={() => setView('dashboard')}
              className={`px-4 py-2 rounded ${view === 'dashboard' ? 'bg-white text-blue-700' : 'hover:bg-blue-600'}`}
            >
              Dashboard
            </button>
            <button 
              onClick={() => setView('patients')}
              className={`px-4 py-2 rounded ${view === 'patients' ? 'bg-white text-blue-700' : 'hover:bg-blue-600'}`}
            >
              Patient List
            </button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {view === 'dashboard' ? (
          <Dashboard date={date} setDate={setDate} />
        ) : (
          <PatientList />
        )}
      </main>

      <footer className="bg-gray-200 py-4 text-center">
        <p>Cancer Screening Reminder System © {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;