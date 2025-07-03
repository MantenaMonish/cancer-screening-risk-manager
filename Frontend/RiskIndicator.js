import React from 'react';

const RiskIndicator = ({ riskLevel }) => {
  const getRiskColor = () => {
    switch (riskLevel) {
      case 'High':
        return { bg: 'bg-red-100', text: 'text-red-800', label: 'High' };
      case 'Medium':
        return { bg: 'bg-yellow-100', text: 'text-yellow-800', label: 'Medium' };
      case 'Low':
        return { bg: 'bg-green-100', text: 'text-green-800', label: 'Low' };
      default:
        return { bg: 'bg-gray-100', text: 'text-gray-800', label: 'Unknown' };
    }
  };

  const color = getRiskColor();

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-medium ${color.bg} ${color.text}`}>
      {color.label}
    </span>
  );
};

export default RiskIndicator;