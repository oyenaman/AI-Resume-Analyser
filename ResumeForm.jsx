import React, { useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const ResumeForm = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [atsScore, setAtsScore] = useState(null);
  const [showATS, setShowATS] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('resume', file);

    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5001/analyze', formData);
      setResults(response.data.predictions);
      setAtsScore(response.data.ats);
      setShowATS(false);
    } catch (error) {
      console.error('Error:', error);
      alert('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const chartData = {
    labels: results ? Object.keys(results) : [],
    datasets: [
      {
        label: 'Match Percentage',
        data: results ? Object.values(results) : [],
        backgroundColor: [
          '#3b82f6', // Blue
          '#10b981', // Green
          '#f59e0b', // Amber
          '#ef4444', // Red
          '#8b5cf6', // Purple
          '#ec4899', // Pink
          '#22d3ee', // Cyan
          '#f43f5e', // Rose
          '#14b8a6', // Teal
          '#eab308'  // Yellow
        ],
        borderRadius: 8,
      },
    ],
  };
  

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Resume Job Role Match' },
    },
    scales: {
      y: {
        min: 0,
        max: 100,
        ticks: {
          stepSize: 10,
        },
      },
    },
  };

  return (
<div className="max-w-2xl mx-auto p-6 bg-gray-100 rounded-2xl shadow-lg mt-10">
      <h1 className="text-3xl font-bold mb-8 text-center">AI Resume Analyzer</h1>
  
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex justify-between items-center">
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
            className="block border rounded px-4 py-2 text-sm"
          />
  
          <button
            onClick={() => setShowATS(!showATS)}
            type="button"
            className="bg-green-600 text-white px-5 py-2 rounded hover:bg-green-700 ml-4"
          >
            {showATS ? 'Hide ATS Score' : 'View ATS Score'}
          </button>
        </div>
  
        {/* Increased space between file input and Analyze button */}
        <div className="mt-6">
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700 disabled:opacity-50 w-full"
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
        </div>
      </form>
  
      {results && (
        <div className="mt-9">
          <Bar data={chartData} options={chartOptions} />
  
          {showATS && (
            <div className="mt-4 text-lg text-center font-semibold text-gray-700">
              ATS Score: {atsScore}%
            </div>
          )}
        </div>
      )}
    </div>
    );  
};

export default ResumeForm;