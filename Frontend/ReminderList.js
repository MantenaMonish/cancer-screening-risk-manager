import React from 'react';
import RiskIndicator from './RiskIndicator';

const ReminderList = ({ reminders }) => {
  // Group reminders by patient
  const remindersByPatient = reminders.reduce((acc, reminder) => {
    if (!acc[reminder.patient_id]) {
      acc[reminder.patient_id] = {
        name: reminder.name,
        reminders: []
      };
    }
    acc[reminder.patient_id].reminders.push(reminder);
    return acc;
  }, {});

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Patient
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Screening Type
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Risk Level
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Last Screening
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Due Date
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Days Until Due
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {Object.values(remindersByPatient).map((patient) => (
            <React.Fragment key={patient.reminders[0].patient_id}>
              <tr className="bg-gray-50">
                <td colSpan="6" className="px-6 py-3 font-bold text-gray-700">
                  {patient.name} (ID: {patient.reminders[0].patient_id})
                </td>
              </tr>
              {patient.reminders.map((reminder, index) => {
                const dueDate = new Date(reminder.due_date);
                const today = new Date();
                const daysUntilDue = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));
                
                return (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4"></td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {reminder.type}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <RiskIndicator riskLevel={reminder.risk} />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-500">
                      {reminder.last_screen}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {reminder.due_date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {daysUntilDue > 0 ? (
                        <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full">
                          In {daysUntilDue} days
                        </span>
                      ) : (
                        <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full">
                          Past due!
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ReminderList;