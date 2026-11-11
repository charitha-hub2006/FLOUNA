import React, { useState, useEffect } from 'react';
import './index.css';

export default function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);

  // Load persistent search history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('flouna_search_history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        setHistory([]);
      }
    }
  }, []);

  const saveToHistory = (searchQuery) => {
    if (!searchQuery.trim()) return;
    const updated = [searchQuery, ...history.filter(item => item !== searchQuery)].slice(0, 5);
    setHistory(updated);
    localStorage.setItem('flouna_search_history', JSON.stringify(updated));
  };

  const handleSearch = async (searchQuery) => {
    const q = searchQuery !== undefined ? searchQuery : query;
    if (!q.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: q }),
      });

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      const result = await response.json();
      setData(result);
      saveToHistory(q);
    } catch (err) {
      console.error("API Request Error:", err);
      setError("Failed to fetch recommendations. Ensure backend server is running.");
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem('flouna_search_history');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        
        {/* Header Banner */}
        <header className="text-center space-y-2 py-4">
          <h1 className="text-4xl font-extrabold tracking-tight text-blue-600">FLOUNA</h1>
          <p className="text-slate-500 font-medium">AI-Powered Food Decision Engine</p>
        </header>

        {/* Search Bar Container */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-4">
          <form onSubmit={(e) => { e.preventDefault(); handleSearch(); }} className="flex gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. Vegetarian biryani under ₹300 in 30 mins with 4.0 stars"
              className="flex-1 px-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-colors disabled:opacity-50"
            >
              {loading ? 'Analyzing...' : 'Search'}
            </button>
          </form>

          {/* Recent Search History (localStorage) */}
          {history.length > 0 && (
            <div className="flex flex-wrap items-center gap-2 pt-2 text-sm text-slate-500">
              <span className="font-medium">🕒 Recent Searches:</span>
              {history.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => { setQuery(item); handleSearch(item); }}
                  className="px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-full border border-slate-200 transition-colors"
                >
                  {item}
                </button>
              ))}
              <button onClick={clearHistory} className="text-xs text-red-500 underline ml-2">Clear</button>
            </div>
          )}

          {/* Quick Test Prompt Chips */}
          <div className="flex flex-wrap items-center gap-2 pt-1 text-sm text-slate-500">
            <span className="font-medium">💡 Try asking:</span>
            <button
              onClick={() => { const q = "Mexican food under 20 in 30 mins with 4.0 stars"; setQuery(q); handleSearch(q); }}
              className="px-3 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-full border border-blue-200 transition-colors"
            >
              Mexican food under 20
            </button>
            <button
              onClick={() => { const q = "spicy chicken tikka"; setQuery(q); handleSearch(q); }}
              className="px-3 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-full border border-blue-200 transition-colors"
            >
              Spicy chicken tikka
            </button>
          </div>
        </div>

        {/* Error Alert Box */}
        {error && (
          <div className="bg-red-50 text-red-700 border border-red-200 p-4 rounded-xl font-medium">
            ⚠️ {error}
          </div>
        )}

        {/* Extracted NLP Preferences Display */}
        {data && data.extracted_preferences && (
          <div className="bg-blue-50 border border-blue-200 p-4 rounded-xl space-y-2">
            <h3 className="font-semibold text-blue-900">Extracted NLP Preferences (Structured Intent):</h3>
            <div className="flex flex-wrap gap-3 text-sm">
              <span className="bg-white px-3 py-1 rounded-md border border-blue-200 shadow-sm">
                <strong>Cuisine:</strong> {data.extracted_preferences.cuisine || "Any"}
              </span>
              <span className="bg-white px-3 py-1 rounded-md border border-blue-200 shadow-sm">
        	<strong>Budget Limit:</strong> {data.extracted_preferences.budget ? `₹${data.extracted_preferences.budget}` : "No Limit"}
                 </span>
              <span className="bg-white px-3 py-1 rounded-md border border-blue-200 shadow-sm">
                <strong>Max Delivery Time:</strong> {data.extracted_preferences.delivery_time ? `${data.extracted_preferences.delivery_time} mins` : "Any"}
              </span>
              <span className="bg-white px-3 py-1 rounded-md border border-blue-200 shadow-sm">
                <strong>Min Rating:</strong> {data.extracted_preferences.min_rating ? `${data.extracted_preferences.min_rating}★` : "Any"}
              </span>
            </div>
          </div>
        )}

        {/* Results Section */}
        {data && data.results && data.results.ranked && (
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-800">
              Ranked Options ({data.results.ranked.length} matches)
            </h2>

            {data.results.ranked.length === 0 ? (
              <div className="bg-white p-6 rounded-xl border border-slate-200 text-center text-slate-500">
                No options matched all your strict constraint filters. Try broadening your budget or delivery time!
              </div>
            ) : (
              data.results.ranked.map((item, index) => (
                <div
                  key={index}
                  className={`bg-white p-6 rounded-2xl border transition-all ${
                    index === 0 ? 'border-2 border-blue-500 shadow-md ring-2 ring-blue-100' : 'border-slate-200 shadow-sm'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      {index === 0 && (
                        <span className="inline-block bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-2">
                          ★ #1 TOP RECOMMENDATION
                        </span>
                      )}
                      <h3 className="text-xl font-bold text-slate-900">{item.name}</h3>
                      <p className="text-sm text-slate-500">{item.cuisine} • Provider: {item.provider}</p>
                    </div>
                    <div className="text-right">
			<span className="text-2xl font-black text-slate-900">₹{item.cost}</span>
                      <div className="text-sm font-semibold text-amber-500">★ {item.rating}</div>
                    </div>
                  </div>

                  <div className="mt-4 pt-4 border-t border-slate-100 flex justify-between items-center text-sm text-slate-600">
                    <div>⏱️ Est. Delivery: <strong>{item.time} mins</strong></div>
                    <div className="bg-slate-100 px-3 py-1 rounded-md text-xs font-mono font-medium">
                      Relevance Score: {item.score}
                    </div>
                  </div>

                  {/* Explainable AI Banner */}
                  {item.explanation && (
                    <div className="mt-3 bg-emerald-50 text-emerald-800 text-sm p-3 rounded-lg border border-emerald-200">
                      💡 <strong>Why recommended:</strong> {item.explanation}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}

      </div>
    </div>
  );
}
