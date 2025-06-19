import React, { useState, useEffect } from 'react';
import { AlertTriangle, Cloud, Activity, MapPin, Calendar, TrendingUp } from 'lucide-react';

const LiveAlerts = () => {
  const [cycloneData, setCycloneData] = useState([]);
  const [earthquakeData, setEarthquakeData] = useState([]);
  const [cyclonePrediction, setCyclonePrediction] = useState([]);
  const [earthquakePrediction, setEarthquakePrediction] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock API functions to simulate backend responses
  const fetchCycloneData = async () => {
    try {
      // Simulate API call - replace with actual API endpoint
      const response = await fetch('/api/cyclone-data');
      if (!response.ok) {
        throw new Error('Failed to fetch cyclone data');
      }
      const data = await response.json();
      
      // Handle different possible response structures
      if (data && data.cyclone_data) {
        return data.cyclone_data;
      } else if (Array.isArray(data)) {
        return data;
      } else {
        // Return mock data if API structure is different
        return [
          {
            id: 1,
            name: "Cyclone Alpha",
            location: "Bay of Bengal",
            intensity: "Severe",
            windSpeed: 120,
            pressure: 950,
            coordinates: { lat: 18.5, lng: 85.0 },
            lastUpdated: new Date().toISOString()
          }
        ];
      }
    } catch (error) {
      console.error('Failed to fetch cyclone data:', error);
      // Return mock data on error
      return [
        {
          id: 1,
          name: "Cyclone Alpha",
          location: "Bay of Bengal",
          intensity: "Severe",
          windSpeed: 120,
          pressure: 950,
          coordinates: { lat: 18.5, lng: 85.0 },
          lastUpdated: new Date().toISOString()
        }
      ];
    }
  };

  const fetchEarthquakeData = async () => {
    try {
      // Simulate API call - replace with actual API endpoint
      const response = await fetch('/api/earthquake-data');
      if (!response.ok) {
        throw new Error('Failed to fetch earthquake data');
      }
      const data = await response.json();
      
      // Handle different possible response structures
      if (data && data.earthquake_data) {
        return data.earthquake_data;
      } else if (Array.isArray(data)) {
        return data;
      } else {
        // Return mock data if API structure is different
        return [
          {
            id: 1,
            magnitude: 6.2,
            location: "Northern India",
            depth: 10,
            coordinates: { lat: 28.6, lng: 77.2 },
            timestamp: new Date().toISOString(),
            intensity: "Strong"
          }
        ];
      }
    } catch (error) {
      console.error('Failed to fetch earthquake data:', error);
      // Return mock data on error
      return [
        {
          id: 1,
          magnitude: 6.2,
          location: "Northern India",
          depth: 10,
          coordinates: { lat: 28.6, lng: 77.2 },
          timestamp: new Date().toISOString(),
          intensity: "Strong"
        }
      ];
    }
  };

  const fetchEarthquakePrediction = async () => {
    try {
      // Simulate API call - replace with actual API endpoint
      const response = await fetch('/api/earthquake-prediction');
      if (!response.ok) {
        throw new Error('Failed to fetch earthquake prediction');
      }
      const data = await response.json();
      
      // Handle different possible response structures
      if (data && data.predict_next_earthquake) {
        return data.predict_next_earthquake;
      } else if (data && data.prediction) {
        return data.prediction;
      } else if (Array.isArray(data)) {
        return data;
      } else {
        // Return mock data if API structure is different
        return [
          {
            id: 1,
            predictedMagnitude: 5.8,
            location: "Himalayan Region",
            probability: 0.75,
            timeframe: "Next 30 days",
            riskLevel: "High"
          }
        ];
      }
    } catch (error) {
      console.error('Error in Fetching Earthquake Prediction', error);
      // Return mock data on error
      return [
        {
          id: 1,
          predictedMagnitude: 5.8,
          location: "Himalayan Region",
          probability: 0.75,
          timeframe: "Next 30 days",
          riskLevel: "High"
        }
      ];
    }
  };

  const fetchCyclonePrediction = async () => {
    try {
      // Simulate API call - replace with actual API endpoint
      const response = await fetch('/api/cyclone-prediction');
      if (!response.ok) {
        throw new Error('Failed to fetch cyclone prediction');
      }
      const data = await response.json();
      
      // Handle different possible response structures
      if (data && data.CyclonePrediction) {
        return data.CyclonePrediction;
      } else if (data && data.prediction) {
        return data.prediction;
      } else if (Array.isArray(data)) {
        return data;
      } else {
        // Return mock data if API structure is different
        return [
          {
            id: 1,
            predictedIntensity: "Severe",
            location: "Arabian Sea",
            probability: 0.65,
            timeframe: "Next 15 days",
            riskLevel: "Medium"
          }
        ];
      }
    } catch (error) {
      console.error('Error in Getting Cyclone Prediction', error);
      // Return mock data on error
      return [
        {
          id: 1,
          predictedIntensity: "Severe",
          location: "Arabian Sea",
          probability: 0.65,
          timeframe: "Next 15 days",
          riskLevel: "Medium"
        }
      ];
    }
  };

  const loadAllData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await Promise.allSettled([
        fetchCycloneData(),
        fetchEarthquakeData(),
        fetchEarthquakePrediction(),
        fetchCyclonePrediction()
      ]);

      // Handle results safely
      const [cycloneResult, earthquakeResult, earthquakePredResult, cyclonePredResult] = results;

      if (cycloneResult.status === 'fulfilled') {
        setCycloneData(Array.isArray(cycloneResult.value) ? cycloneResult.value : []);
      }

      if (earthquakeResult.status === 'fulfilled') {
        setEarthquakeData(Array.isArray(earthquakeResult.value) ? earthquakeResult.value : []);
      }

      if (earthquakePredResult.status === 'fulfilled') {
        setEarthquakePrediction(Array.isArray(earthquakePredResult.value) ? earthquakePredResult.value : []);
      }

      if (cyclonePredResult.status === 'fulfilled') {
        setCyclonePrediction(Array.isArray(cyclonePredResult.value) ? cyclonePredResult.value : []);
      }

    } catch (error) {
      console.error('Error loading data:', error);
      setError('Failed to load disaster data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
    // Set up auto-refresh every 5 minutes
    const interval = setInterval(loadAllData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'severe':
      case 'high':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'moderate':
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low':
      case 'mild':
        return 'text-green-600 bg-green-50 border-green-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading disaster alerts...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-12">
            <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={loadAllData}
              className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Live Disaster Alerts</h1>
          <p className="text-gray-600">Real-time monitoring and predictions for natural disasters</p>
          <div className="mt-4 flex justify-center items-center space-x-2 text-sm text-gray-500">
            <Activity className="h-4 w-4" />
            <span>Last updated: {new Date().toLocaleTimeString()}</span>
          </div>
        </div>

        {/* Current Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Cyclone Alerts */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <Cloud className="h-6 w-6 mr-2 text-blue-600" />
                Active Cyclones
              </h2>
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                {cycloneData.length} Active
              </span>
            </div>
            
            {cycloneData.length > 0 ? (
              <div className="space-y-4">
                {cycloneData.map((cyclone, index) => (
                  <div key={cyclone.id || index} className={`border rounded-lg p-4 ${getSeverityColor(cyclone.intensity)}`}>
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold">{cyclone.name || `Cyclone ${index + 1}`}</h3>
                      <span className="text-xs font-medium px-2 py-1 rounded">
                        {cyclone.intensity || 'Unknown'}
                      </span>
                    </div>
                    <div className="space-y-1 text-sm">
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 mr-1" />
                        <span>{cyclone.location || 'Unknown location'}</span>
                      </div>
                      {cyclone.windSpeed && (
                        <div>Wind Speed: {cyclone.windSpeed} km/h</div>
                      )}
                      {cyclone.pressure && (
                        <div>Pressure: {cyclone.pressure} hPa</div>
                      )}
                      {cyclone.lastUpdated && (
                        <div className="flex items-center text-gray-500">
                          <Calendar className="h-4 w-4 mr-1" />
                          <span>{new Date(cyclone.lastUpdated).toLocaleString()}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Cloud className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>No active cyclones detected</p>
              </div>
            )}
          </div>

          {/* Earthquake Alerts */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <Activity className="h-6 w-6 mr-2 text-red-600" />
                Recent Earthquakes
              </h2>
              <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">
                {earthquakeData.length} Recent
              </span>
            </div>
            
            {earthquakeData.length > 0 ? (
              <div className="space-y-4">
                {earthquakeData.map((earthquake, index) => (
                  <div key={earthquake.id || index} className={`border rounded-lg p-4 ${getSeverityColor(earthquake.intensity)}`}>
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold">Magnitude {earthquake.magnitude || 'Unknown'}</h3>
                      <span className="text-xs font-medium px-2 py-1 rounded">
                        {earthquake.intensity || 'Unknown'}
                      </span>
                    </div>
                    <div className="space-y-1 text-sm">
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 mr-1" />
                        <span>{earthquake.location || 'Unknown location'}</span>
                      </div>
                      {earthquake.depth && (
                        <div>Depth: {earthquake.depth} km</div>
                      )}
                      {earthquake.timestamp && (
                        <div className="flex items-center text-gray-500">
                          <Calendar className="h-4 w-4 mr-1" />
                          <span>{new Date(earthquake.timestamp).toLocaleString()}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Activity className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>No recent earthquakes detected</p>
              </div>
            )}
          </div>
        </div>

        {/* Predictions */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Earthquake Predictions */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <TrendingUp className="h-6 w-6 mr-2 text-orange-600" />
                Earthquake Predictions
              </h2>
            </div>
            
            {earthquakePrediction.length > 0 ? (
              <div className="space-y-4">
                {earthquakePrediction.map((prediction, index) => (
                  <div key={prediction.id || index} className={`border rounded-lg p-4 ${getSeverityColor(prediction.riskLevel)}`}>
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold">
                        Magnitude {prediction.predictedMagnitude || 'Unknown'}
                      </h3>
                      <span className="text-xs font-medium px-2 py-1 rounded">
                        {prediction.riskLevel || 'Unknown'} Risk
                      </span>
                    </div>
                    <div className="space-y-1 text-sm">
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 mr-1" />
                        <span>{prediction.location || 'Unknown location'}</span>
                      </div>
                      {prediction.probability && (
                        <div>Probability: {Math.round(prediction.probability * 100)}%</div>
                      )}
                      {prediction.timeframe && (
                        <div>Timeframe: {prediction.timeframe}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <TrendingUp className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>No earthquake predictions available</p>
              </div>
            )}
          </div>

          {/* Cyclone Predictions */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <TrendingUp className="h-6 w-6 mr-2 text-blue-600" />
                Cyclone Predictions
              </h2>
            </div>
            
            {cyclonePrediction.length > 0 ? (
              <div className="space-y-4">
                {cyclonePrediction.map((prediction, index) => (
                  <div key={prediction.id || index} className={`border rounded-lg p-4 ${getSeverityColor(prediction.riskLevel)}`}>
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold">
                        {prediction.predictedIntensity || 'Unknown'} Intensity
                      </h3>
                      <span className="text-xs font-medium px-2 py-1 rounded">
                        {prediction.riskLevel || 'Unknown'} Risk
                      </span>
                    </div>
                    <div className="space-y-1 text-sm">
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 mr-1" />
                        <span>{prediction.location || 'Unknown location'}</span>
                      </div>
                      {prediction.probability && (
                        <div>Probability: {Math.round(prediction.probability * 100)}%</div>
                      )}
                      {prediction.timeframe && (
                        <div>Timeframe: {prediction.timeframe}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <TrendingUp className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>No cyclone predictions available</p>
              </div>
            )}
          </div>
        </div>

        {/* Refresh Button */}
        <div className="text-center mt-8">
          <button
            onClick={loadAllData}
            disabled={loading}
            className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Refreshing...' : 'Refresh Data'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LiveAlerts;